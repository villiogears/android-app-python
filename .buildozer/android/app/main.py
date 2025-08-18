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

# Delay-import OpenCV / numpy to avoid native .so load at module import time
# which can crash the app on some Android configurations. The real import is
# attempted on demand by `ensure_cv2_np()` below.
cv2 = None
np = None
has_cv2 = False
has_np = False


class MainApp(App):
	"""シンプルな Kivy アプリ + OpenCV による撮影時トーン編集。"""
	title = "Kivy Android Camera with Tone Edit"

	def build(self):
		# カメラを最大化表示し、下部にコントロールをオーバーレイする
		from kivy.uix.floatlayout import FloatLayout
		root = FloatLayout()

		# カメラ（画面いっぱい）
		# 権限要求前に即起動すると Android でクラッシュする可能性があるので play=False にする
		self.camera = Camera(play=False, index=0, resolution=(1280, 720), size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
		root.add_widget(self.camera)

		# capture() で参照する可能性がある preview を定義しておく（UI へは配置していない）
		self.preview = Image()

		# コントロール（下部にオーバーレイ）
		ctrl_box = BoxLayout(orientation='vertical', size_hint=(1, 0.22), pos_hint={'x': 0, 'y': 0}, padding=6, spacing=6)

		# スライダー：明るさ、コントラスト、ウォーム（小型化）
		self.brightness_slider = Slider(min=-100, max=100, value=0)
		self.contrast_slider = Slider(min=50, max=300, value=100)
		self.warmth_slider = Slider(min=-100, max=100, value=0)

		# ラベルとスライダーを水平に並べて場所を節約
		s_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=24, spacing=8)
		s_row.add_widget(Label(text='B', size_hint_x=None, width=24))
		s_row.add_widget(self.brightness_slider)
		s_row.add_widget(Label(text='C', size_hint_x=None, width=24))
		s_row.add_widget(self.contrast_slider)
		s_row.add_widget(Label(text='W', size_hint_x=None, width=24))
		s_row.add_widget(self.warmth_slider)

		ctrl_box.add_widget(s_row)

		# ボタン類（Capture は即時保存も行う）。回転・ミラー切替を追加
		btns = BoxLayout(size_hint_y=None, height=44, spacing=8)
		capture_btn = Button(text='Capture', size_hint_x=0.33)
		save_btn = Button(text='Save', size_hint_x=0.33)
		self.rotate_btn = Button(text='Rotate: 0°', size_hint_x=0.17)
		self.mirror_btn = Button(text='Mirror: off', size_hint_x=0.17)
		capture_btn.bind(on_release=self.capture)
		save_btn.bind(on_release=self.save_current)
		self.rotate_btn.bind(on_release=self.toggle_rotate)
		self.mirror_btn.bind(on_release=self.toggle_mirror)
		btns.add_widget(capture_btn)
		btns.add_widget(save_btn)
		btns.add_widget(self.rotate_btn)
		btns.add_widget(self.mirror_btn)

		ctrl_box.add_widget(btns)

		# 初期向き設定
		self.rotate_angle = 0  # 0,90,180,270
		self.mirror = False

		# 背景をやや透過させ操作部が見えるように（見た目のため）
		ctrl_box.canvas.before.clear()
		root.add_widget(ctrl_box)

		self.last_processed = None
		return root

	def on_start(self):
		# 権限ダイアログを表示する処理は削除しました。
		# 権限の有無にかかわらずカメラ起動を試みます（例外は無視）。
		try:
			self.camera.play = True
		except Exception:
			# 起動に失敗した場合は安全に無視（アプリは落とさない）
			pass

	def ensure_cv2_np(self):
		"""Attempt to import cv2 and numpy on demand and set flags.

		This reduces the chance of crashing at module import time due to
		native library load failures. Safe to call multiple times.
		"""
		global cv2, np, has_cv2, has_np
		# try cv2
		if not has_cv2:
			try:
				import cv2 as _cv2
				cv2 = _cv2
				has_cv2 = True
			except Exception:
				cv2 = None
				has_cv2 = False
		# try numpy
		if not has_np:
			try:
				import numpy as _np
				np = _np
				has_np = True
			except Exception:
				np = None
				has_np = False

	def texture_to_bgr(self, texture):
		# Kivy texture (rgba) -> OpenCV BGR ndarray
		if not texture:
			return None
		# ensure numpy available
		self.ensure_cv2_np()
		w, h = texture.size
		pixels = texture.pixels  # bytes in 'rgba'
		if not has_np:
			return None
		arr = np.frombuffer(pixels, dtype=np.uint8)
		if arr.size != w * h * 4:
			# 不正な場合は安定化
			return None
		arr = arr.reshape((h, w, 4))
		rgba = arr[:, :, :3]  # R,G,B
		# Kivy は通常上向きなので不要だが色順は RGB -> convert to BGR
		bgr = rgba[..., ::-1].copy()
		return bgr

	def bgr_to_texture(self, img_bgr):
		# OpenCV BGR -> Kivy Texture (RGB)
		if img_bgr is None:
			return None
		# ensure cv2 available
		self.ensure_cv2_np()
		if not has_cv2:
			return None
		img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
		h, w = img_rgb.shape[:2]
		buf = img_rgb.tobytes()
		tex = Texture.create(size=(w, h), colorfmt='rgb')
		tex.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
		# カメラ画像は上下が逆のことがあるので反転
		tex.flip_vertical()
		return tex

	def apply_tone(self, img_bgr, brightness=0, contrast=1.0, warmth=0.0):
		# brightness: -100..100 -> beta
		# contrast: 0.5..3.0 -> alpha
		# warmth: -1.0..1.0 -> increase red / decrease blue
		if img_bgr is None:
			return None
		# ensure cv2/numpy
		self.ensure_cv2_np()
		if not has_cv2 or not has_np:
			return img_bgr
		# コントラスト・明るさ
		alpha = float(contrast)
		beta = float(brightness)
		adjusted = cv2.convertScaleAbs(img_bgr, alpha=alpha, beta=beta)
		# ウォーム処理（単純に R と B をスケール）
		if abs(warmth) > 1e-6:
			wm = float(warmth)
			b, g, r = cv2.split(adjusted)
			# 範囲外はクリップされる
			r = cv2.multiply(r.astype(np.float32), 1.0 + wm)
			b = cv2.multiply(b.astype(np.float32), 1.0 - wm)
			# back to uint8 and merge
			r = np.clip(r, 0, 255).astype(np.uint8)
			b = np.clip(b, 0, 255).astype(np.uint8)
			adjusted = cv2.merge((b, g, r))
		return adjusted

	def apply_orientation(self, img):
		# 回転とミラーを適用
		if img is None:
			return img
		if self.rotate_angle == 90:
			img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
		elif self.rotate_angle == 180:
			img = cv2.rotate(img, cv2.ROTATE_180)
		elif self.rotate_angle == 270:
			img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
		if self.mirror:
			img = cv2.flip(img, 1)  # 水平方向に反転
		return img

	def toggle_rotate(self, instance):
		# 0 -> 90 -> 180 -> 270 -> 0 ...
		self.rotate_angle = {0:90, 90:180, 180:270, 270:0}[self.rotate_angle]
		self.rotate_btn.text = f'Rotate: {self.rotate_angle}°'

	def toggle_mirror(self, instance):
		self.mirror = not self.mirror
		self.mirror_btn.text = 'Mirror: on' if self.mirror else 'Mirror: off'

	def capture(self, instance):
		# 例外を捕捉してクラッシュを防ぐ
		try:
			tex = None
			try:
				tex = self.camera.texture
			except Exception:
				tex = None
			if not tex:
				print('No camera texture available (camera not started or permission denied)')
				return
			# ensure numpy/cv2 availability before processing
			self.ensure_cv2_np()
			if not has_np:
				print('numpy not available; cannot process image')
				return
			img = self.texture_to_bgr(tex)
			if img is None:
				return
			brightness = self.brightness_slider.value
			contrast = self.contrast_slider.value / 100.0
			warmth = self.warmth_slider.value / 100.0

			# OpenCV が無ければトーン処理/保存をスキップして生データのまま保存（到達し得る形で）
			if has_cv2:
				processed = self.apply_tone(img, brightness=brightness, contrast=contrast, warmth=warmth)
				processed_oriented = self.apply_orientation(processed)
			else:
				processed_oriented = img

			self.last_processed = processed_oriented
			tex_out = None
			if has_cv2:
				tex_out = self.bgr_to_texture(processed_oriented)
			if tex_out:
				try:
					self.preview.texture = tex_out
				except Exception:
					pass
			# 保存も行う（ユーザーは Save で再保存可能）
			self._save_to_storage(processed_oriented)
		except Exception as e:
			# ここで例外を握り潰してクラッシュさせない（logcat で原因確認）
			print('capture failed:', e)

	def save_current(self, instance):
		# UI からの明示的保存（最後の向き済み画像を保存）
		if self.last_processed is None:
			print('No image to save')
			return
		self._save_to_storage(self.last_processed)

	def _save_to_storage(self, img_bgr):
		# 保存ロジックを共通化（OpenCV が必須）
		if img_bgr is None:
			return
		# ensure cv2 availability for writing
		self.ensure_cv2_np()
		if not has_cv2:
			print('cv2 not available; cannot write image')
			return
		dirpath = '/storage/emulated/0/Pictures'
		try:
			os.makedirs(dirpath, exist_ok=True)
		except Exception:
			dirpath = os.path.join(os.getcwd(), 'captures')
			os.makedirs(dirpath, exist_ok=True)
		filename = 'kivy_capture_{}.jpg'.format(int(time.time()))
		path = os.path.join(dirpath, filename)
		try:
			cv2.imwrite(path, img_bgr)
			print('Saved to', path)
		except Exception as e:
			print('Failed to save:', e)

	def on_pause(self):
		# フォアグラウンドを離れるときはカメラを停止してリソースを解放
		try:
			self.camera.play = False
		except Exception:
			pass
		return True

	def on_stop(self):
		try:
			self.camera.play = False
		except Exception:
			pass
