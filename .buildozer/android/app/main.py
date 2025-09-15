from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.label import Label
import time
Builder.load_string("""
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        size_hint: (1, 0.8)
        # Let the camera texture fill the widget area and not revert to its native size
        allow_stretch: True
        keep_ratio: True
        play: False
        canvas.before:
            PushMatrix
            Rotate:
                angle: -90
                origin: self.center
        canvas.after:
            PopMatrix
    BoxLayout:
        size_hint_y: None
        height: '48dp'
        spacing: '8dp'
        padding: '8dp'
        Label:
            text: 'Save to:'
            size_hint_x: None
            width: '80dp'
        TextInput:
            id: save_path
            text: app.user_data_dir + '/photos'
            multiline: False
            halign: 'left'
            valign: 'middle'
            write_tab: False
            on_text_validate: root.on_path_change(self.text)
        Button:
            text: 'Choose...'
            size_hint_x: None
            width: '100dp'
            on_press: root.open_folder_chooser()
    
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
    Button:
        text: 'Download'
        size_hint_y: None
        height: '48dp'
        on_press: root.download()
    
""")

class CameraClick(BoxLayout):
    def on_path_change(self, path):
        # optional hook if UI needs to respond when path changes
        pass

    def open_folder_chooser(self):
        # Show a simple FileChooser popup to pick a folder (works on desktop).
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(path='.', dirselect=True)
        btn_box = BoxLayout(size_hint_y=None, height='40dp')
        select_btn = Button(text='Select')
        cancel_btn = Button(text='Cancel')

        def do_select(instance):
            selection = filechooser.selection
            if selection:
                # pick first selected path (dirselect=True -> selection is folder)
                self.ids['save_path'].text = selection[0]
            popup.dismiss()

        def do_cancel(instance):
            popup.dismiss()

        select_btn.bind(on_press=do_select)
        cancel_btn.bind(on_press=do_cancel)
        btn_box.add_widget(select_btn)
        btn_box.add_widget(cancel_btn)
        content.add_widget(filechooser)
        content.add_widget(btn_box)
        popup = Popup(title='Choose folder', content=content, size_hint=(0.9, 0.9))
        popup.open()

    def capture(self):
        """
        Function to capture the images and give them the names
        according to their captured time and date.
        """
        import os
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        app = App.get_running_app()
        save_dir = self.ids.get('save_path').text if 'save_path' in self.ids else app.user_data_dir
        # ensure directory exists
        try:
            os.makedirs(save_dir, exist_ok=True)
        except Exception as e:
            print('Failed to create directory', save_dir, e)
            save_dir = app.user_data_dir

        filename = os.path.join(save_dir, "IMG_{}.png".format(timestr))
        camera.export_to_png(filename)
        print(f"Captured -> {filename}")

    def download(self):
        """
        Copy the most recently saved image from the save_path to the user's Downloads folder.
        On desktop use ~/Downloads, on Android try /sdcard/Download as a best-effort.
        """
        import os, shutil
        app = App.get_running_app()
        save_dir = self.ids.get('save_path').text if 'save_path' in self.ids else app.user_data_dir
        if not os.path.isdir(save_dir):
            self._show_message(f"Save directory not found: {save_dir}")
            return

        # find latest PNG in save_dir
        pngs = [os.path.join(save_dir, f) for f in os.listdir(save_dir) if f.lower().endswith('.png')]
        if not pngs:
            self._show_message('No PNG images found in save directory')
            return
        latest = max(pngs, key=os.path.getmtime)

        # determine downloads folder
        if os.name == 'nt':
            downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
        else:
            # POSIX (Linux / Android)
            downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
            # on Android, try common external path
            if not os.path.isdir(downloads):
                downloads = '/sdcard/Download'

        try:
            os.makedirs(downloads, exist_ok=True)
            dest = os.path.join(downloads, os.path.basename(latest))
            shutil.copy2(latest, dest)
            self._show_message(f'Copied to: {dest}')
        except Exception as e:
            self._show_message(f'Failed to copy: {e}')

    def _show_message(self, text):
        p = Popup(title='Info', content=Label(text=text), size_hint=(0.8, 0.3))
        p.open()


class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()