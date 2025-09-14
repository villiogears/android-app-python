from kivy.app import App
from kivy.clock import Clock
from kivy.uix.stacklayout im    def init_camera(self, dt):
        try:
            # カメラ権限を確認してから初期化
            if platform == 'android':
                from plyer import permission
                if permission.check_permission('android.permission.CAMERA'):
                    Clock.schedule_once(self.start_camera_safe, 1)
                else:
                    def on_permissions(result):
                        if result:
                            Clock.schedule_once(self.start_camera_safe, 1)
                        else:
                            print("Camera permission denied")
                            self.show_camera_error()
                    permission.request_permission('android.permission.CAMERA', on_permissions)
            else:
                Clock.schedule_once(self.start_camera_safe, 1)
        except Exception as e:
            print(f"Camera initialization error: {e}")
            Clock.schedule_once(self.start_camera_safe, 1)m kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.utils import platform
try:
    if platform == 'android':
        from jnius import autoclass, cast
        from android import activity
    else:
        autoclass = cast = activity = None
except ImportError:
    autoclass = cast = activity = None
from functools import partial
from datetime import datetime
from os.path import exists
import os


class CameraApp(App):
    def build(self):
        # Main layout
        layout = BoxLayout(orientation='vertical')
        
        # Camera widget - カメラの初期化を遅らせる
        self.camera = Camera(play=False, resolution=(640, 480))
        layout.add_widget(self.camera)
        
        # Control buttons
        button_layout = BoxLayout(size_hint_y=0.15, orientation='vertical')
        
        # Top row buttons
        top_buttons = BoxLayout(size_hint_y=0.5)
        
        # Capture button
        capture_btn = Button(text='📷 Capture')
        capture_btn.bind(on_press=self.capture)
        top_buttons.add_widget(capture_btn)
        
        # Flash toggle button
        self.flash_btn = Button(text='⚡ Flash: Off')
        self.flash_btn.bind(on_press=self.toggle_flash)
        top_buttons.add_widget(self.flash_btn)
        
        button_layout.add_widget(top_buttons)
        
        # Bottom row buttons
        bottom_buttons = BoxLayout(size_hint_y=0.5)
        
        # Zoom controls
        zoom_layout = BoxLayout(size_hint_x=0.4)
        zoom_out_btn = Button(text='🔍-', size_hint_x=0.5)
        zoom_out_btn.bind(on_press=self.zoom_out)
        zoom_layout.add_widget(zoom_out_btn)
        
        zoom_in_btn = Button(text='🔍+', size_hint_x=0.5)
        zoom_in_btn.bind(on_press=self.zoom_in)
        zoom_layout.add_widget(zoom_in_btn)
        
        bottom_buttons.add_widget(zoom_layout)
        
        # Resolution toggle
        self.res_btn = Button(text='HD', size_hint_x=0.3)
        self.res_btn.bind(on_press=self.toggle_resolution)
        bottom_buttons.add_widget(self.res_btn)
        
        # Settings button
        settings_btn = Button(text='⚙️', size_hint_x=0.3)
        settings_btn.bind(on_press=self.show_settings)
        bottom_buttons.add_widget(settings_btn)
        
        button_layout.add_widget(bottom_buttons)
        
        # カメラの初期化を遅らせる
        Clock.schedule_once(self.init_camera, 3)
        
        return layout
    
    def init_camera(self, dt):
        try:
            # カメラ権限を確認してから初期化
            if platform == 'android':
                from plyer import permission
                if permission.check_permission('android.permission.CAMERA'):
                    self.start_camera()
                else:
                    def on_permissions(result):
                        if result:
                            self.start_camera()
                        else:
                            print("Camera permission denied")
                    permission.request_permission('android.permission.CAMERA', on_permissions)
            else:
                self.start_camera()
        except Exception as e:
            print(f"Camera initialization error: {e}")
            # 権限チェックをスキップしてカメラを開始
            self.start_camera()
    
    def start_camera(self):
        try:
            self.camera.play = True
            print("Camera started successfully")
        except Exception as e:
            print(f"Failed to start camera: {e}")
            # カメラが利用できない場合のフォールバック
            self.show_camera_error()
    
    def show_camera_error(self):
        # カメラエラーのメッセージを表示
        error_label = Label(
            text="カメラが利用できません\n権限を確認してください",
            font_size=20,
            halign='center',
            valign='middle'
        )
        error_label.bind(size=error_label.setter('text_size'))
        
        # 再試行ボタン
        retry_btn = Button(text="再試行", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        retry_btn.bind(on_press=self.retry_camera)
        
        # エラーレイアウト
        error_layout = BoxLayout(orientation='vertical')
        error_layout.add_widget(error_label)
        error_layout.add_widget(retry_btn)
        
        # メインカメラを非表示にしてエラーメッセージを表示
        self.camera.opacity = 0
        self.layout.add_widget(error_layout)
    
    def retry_camera(self, instance):
        # カメラを再試行
        Clock.schedule_once(self.init_camera, 0.1)
    
    def capture(self, instance):
        # Capture image
        if self.camera.texture:
            # Save image
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'photo_{timestamp}.png'
            
            # For Android, save to external storage
            if platform == 'android':
                # Use Android's external storage directory
                filepath = f'/storage/emulated/0/DCIM/Camera/{filename}'
            else:
                # For desktop testing
                filepath = filename
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Save texture as image
            self.camera.export_to_png(filepath)
            print(f'Image saved to: {filepath}')
    
    def toggle_flash(self, instance):
        # Toggle flash (Android only)
        if platform == 'android':
            try:
                # Android flash control using jnius
                CameraClass = autoclass('android.hardware.Camera')
                Parameters = autoclass('android.hardware.Camera$Parameters')
                
                # This is a simplified example - actual implementation may vary
                print('Flash toggle attempted')
            except:
                print('Flash control not available')
    
    def zoom_in(self, instance):
        if hasattr(self.camera, 'zoom'):
            current_zoom = getattr(self.camera, 'zoom', 1.0)
            self.camera.zoom = min(current_zoom + 0.1, 2.0)
    
    def zoom_out(self, instance):
        if hasattr(self.camera, 'zoom'):
            current_zoom = getattr(self.camera, 'zoom', 1.0)
            self.camera.zoom = max(current_zoom - 0.1, 0.1)
    
    def toggle_resolution(self, instance):
        current_res = self.camera.resolution
        if current_res == (640, 480):
            self.camera.resolution = (1280, 720)
            self.res_btn.text = 'HD'
        elif current_res == (1280, 720):
            self.camera.resolution = (1920, 1080)
            self.res_btn.text = 'FHD'
        else:
            self.camera.resolution = (640, 480)
            self.res_btn.text = 'SD'
    
    def show_settings(self, instance):
        # Placeholder for settings menu
        print('Settings menu would open here')


