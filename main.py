from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.core.window import Window
import os
import time
import noisereduce as nr
import numpy as np
import sounddevice as sd
import soundfile as sf
import threading
import tempfile
import queue
from collections import deque
from kivy.clock import Clock

class NoiseCancelLayout(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(orientation="vertical", spacing=8, padding=8, **kwargs)

		self.status = Label(text="Ready")
		self.add_widget(self.status)

		controls = BoxLayout(size_hint_y=None, height="40dp", spacing=8)
		self.start_live_btn = Button(text="Start Live")
		self.stop_live_btn = Button(text="Stop Live", disabled=True)
		self.save_btn = Button(text="Save Snapshot", disabled=True)

		self.start_live_btn.bind(on_release=lambda *_: self.start_live())
		self.stop_live_btn.bind(on_release=lambda *_: self.stop_live())
		self.save_btn.bind(on_release=lambda *_: self.save_snapshot())

		controls.add_widget(self.start_live_btn)
		controls.add_widget(self.stop_live_btn)
		controls.add_widget(self.save_btn)
		self.add_widget(controls)

		# slider for prop_decrease parameter of noisereduce
		slider_box = BoxLayout(size_hint_y=None, height="48dp", spacing=8)
		self.prop_label = Label(text="Aggressiveness: 0.8", size_hint_x=0.35)
		self.prop_slider = Slider(min=0.0, max=1.0, value=0.8)
		self.prop_slider.bind(value=self.on_slider)
		slider_box.add_widget(self.prop_label)
		slider_box.add_widget(self.prop_slider)
		self.add_widget(slider_box)

		# config for real-time processing
		self.fs = 16000  # sampling rate
		self.blocksize = 1024  # frames per callback
		self.buffer_seconds = 1.0  # rolling buffer size for NR (seconds)
		self.buffer_size = int(self.buffer_seconds * self.fs)

		self._in_q = queue.Queue()
		self._out_q = queue.Queue()
		self._ring = deque()  # store recent chunks for rolling buffer
		self._ring_samples = 0

		self._input_stream = None
		self._output_stream = None
		self._proc_thread = None
		self._running = False

		# snapshot filename (latest processed data)
		self.snapshot = None

	def on_slider(self, instance, value):
		self.prop_label.text = f"Aggressiveness: {value:.2f}"

	# UI helpers to update status from threads
	def _set_status(self, text):
		Clock.schedule_once(lambda dt: setattr(self.status, "text", text))

	def start_live(self):
		if self._running:
			return
		self._running = True
		self.start_live_btn.disabled = True
		self.stop_live_btn.disabled = False
		self.save_btn.disabled = True
		self._set_status("Starting live noise-cancelled monitoring...")

		# start output stream first (its callback will pull processed frames)
		def out_callback(outdata, frames, time_info, status):
			# outdata is (frames, channels)
			try:
				chunk = self._out_q.get_nowait()
				# ensure chunk length matches frames
				if len(chunk) < frames:
					# pad
					buf = np.zeros(frames, dtype=np.float32)
					buf[: len(chunk)] = chunk
					chunk = buf
				elif len(chunk) > frames:
					chunk = chunk[:frames]
				outdata[:, 0] = chunk.reshape(-1, 1)
			except queue.Empty:
				outdata.fill(0)

		try:
			self._output_stream = sd.OutputStream(samplerate=self.fs, channels=1, blocksize=self.blocksize, callback=out_callback)
			self._output_stream.start()
		except Exception as e:
			self._set_status(f"Output stream error: {e}")
			self._running = False
			self.start_live_btn.disabled = False
			self.stop_live_btn.disabled = True
			return

		# input callback: push frames to processing queue
		def in_callback(indata, frames, time_info, status):
			# convert to mono float32
			arr = indata.copy().astype(np.float32)
			if arr.ndim > 1:
				arr = arr[:, 0]
			else:
				arr = arr.reshape(-1)
			try:
				self._in_q.put_nowait(arr)
			except queue.Full:
				pass

		try:
			self._input_stream = sd.InputStream(samplerate=self.fs, channels=1, blocksize=self.blocksize, callback=in_callback)
			self._input_stream.start()
		except Exception as e:
			self._set_status(f"Input stream error: {e}")
			# cleanup output
			try:
				self._output_stream.stop()
				self._output_stream.close()
			except Exception:
				pass
			self._running = False
			self.start_live_btn.disabled = False
			self.stop_live_btn.disabled = True
			return

		# start processing thread
		self._proc_thread = threading.Thread(target=self._processing_loop, daemon=True)
		self._proc_thread.start()
		self._set_status("Live noise cancellation running")
		self.save_btn.disabled = False

	def stop_live(self):
		if not self._running:
			return
		self._set_status("Stopping live...")
		self._running = False

		# stop input stream
		try:
			if self._input_stream:
				self._input_stream.stop()
				self._input_stream.close()
				self._input_stream = None
		except Exception:
			pass

		# allow processing thread to finish
		if self._proc_thread:
			self._proc_thread.join(timeout=1.0)
			self._proc_thread = None

		# stop output stream
		try:
			if self._output_stream:
				self._output_stream.stop()
				self._output_stream.close()
				self._output_stream = None
		except Exception:
			pass

		# clear queues
		with self._in_q.mutex:
			self._in_q.queue.clear()
		with self._out_q.mutex:
			self._out_q.queue.clear()
		self._ring.clear()
		self._ring_samples = 0

		self.start_live_btn.disabled = False
		self.stop_live_btn.disabled = True
		self.save_btn.disabled = False if self.snapshot else True
		self._set_status("Live stopped")

	def save_snapshot(self):
		# save the latest processed snapshot (if any) to a temp file
		if self.snapshot is None:
			self._set_status("No snapshot available")
			return
		try:
			tf = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
			sf.write(tf.name, self.snapshot, self.fs)
			self._set_status(f"Saved snapshot -> {tf.name}")
		except Exception as e:
			self._set_status(f"Save error: {e}")

	def _processing_loop(self):
		"""
		Consume incoming chunks, maintain a rolling buffer, run noisereduce on that buffer,
		and push the most recent processed block to the output queue. This is best-effort
		"real-time" processing — reduce_noise is applied to a rolling window.
		"""
		while self._running:
			try:
				chunk = self._in_q.get(timeout=0.1)
			except queue.Empty:
				continue

			# append chunk to ring
			self._ring.append(chunk)
			self._ring_samples += len(chunk)
			# trim to buffer_size
			while self._ring_samples > self.buffer_size:
				rem = self._ring[0]
				if self._ring_samples - len(rem) >= self.buffer_size:
					self._ring.popleft()
					self._ring_samples -= len(rem)
				else:
					# need to trim first element partially
					need = self._ring_samples - self.buffer_size
					# drop leading `need` samples from first element
					first = self._ring.popleft()
					first = first[need:]
					self._ring.appendleft(first)
					self._ring_samples -= need
					break

			# form buffer
			if len(self._ring) == 0:
				continue
			buf = np.concatenate(list(self._ring)).astype(np.float32)

			# run noise reduction on the rolling buffer
			try:
				prop = float(self.prop_slider.value)
				# stationary=False allows some adaptivity; adjust as needed
				reduced = nr.reduce_noise(y=buf, sr=self.fs, prop_decrease=prop, stationary=False)
			except Exception as e:
				# on error, fallback to passthrough
				reduced = buf

			# take the last chunk-length samples as the processed output
			out_chunk = reduced[-len(chunk) :].astype(np.float32)

			# save a snapshot (latest processed few seconds) for user to save later
			# keep a copy of the most recent buffer (not too frequent)
			self.snapshot = reduced.copy()

			# push to output queue; avoid blocking if consumer is slow
			try:
				self._out_q.put_nowait(out_chunk)
			except queue.Full:
				# drop if full
				pass

		# thread exiting
		return

class NoiseCancelApp(App):
	def build(self):
		Window.clearcolor = (0.95, 0.95, 0.95, 1)
		return NoiseCancelLayout()

if __name__ == "__main__":
	NoiseCancelApp().run()
