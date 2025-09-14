from kivy.app import App
from kivy.clock import Clock
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
import cv2
import numpy as np


class CameraApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Androidではデフォルトで90度回転
        if platform == 'android':
            self.camera_rotation = 90
        else:
            self.camera_rotation = 0  # カメラの回転角度を追跡
        self.rotated_texture = None  # 回転したテクスチャを保持
    def build(self):
        # Main layout - カメラを最大化するためにFloatLayoutを使用
        from kivy.uix.floatlayout import FloatLayout
        layout = FloatLayout()
        
        # Camera widget - カメラの初期化を遅らせる、サイズを最大化、向きを修正
        # Androidではより高い解像度を使用
        if platform == 'android':
            camera_resolution = (1920, 1080)  # FHD解像度
        else:
            camera_resolution = (1280, 720)   # HD解像度
            
        self.camera = Camera(
            play=False, 
            resolution=camera_resolution,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        # Androidでのカメラ向き修正 - 初期orientationを設定
        if platform == 'android':
            if self.camera_rotation == 0:
                self.camera.orientation = 'portrait'
            elif self.camera_rotation == 90:
                self.camera.orientation = 'landscape'
            elif self.camera_rotation == 180:
                self.camera.orientation = 'portrait'
            else:  # 270
                self.camera.orientation = 'landscape'
        
        # カメラのtexture更新イベントを監視して回転処理を追加
        self.camera.bind(on_texture=self.on_texture_update)
        
        layout.add_widget(self.camera)
        
        # Control buttons - カメラの上にオーバーレイ、半透明にしてカメラビューを邪魔しない
        button_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.15),
            pos_hint={'x': 0, 'y': 0.85}
        )
        
        # 背景を半透明にする
        from kivy.graphics import Color, Rectangle
        with button_layout.canvas.before:
            Color(0, 0, 0, 0.3)  # 黒、30%透明
            Rectangle(pos=button_layout.pos, size=button_layout.size)
        button_layout.bind(pos=self.update_rect, size=self.update_rect)
        
        # Top row buttons
        top_buttons = BoxLayout(size_hint_y=0.5)
        
        # Capture button
        capture_btn = Button(text='📷 Capture', size_hint_x=0.5)
        capture_btn.bind(on_press=self.capture)
        top_buttons.add_widget(capture_btn)
        
        # Flash toggle button
        self.flash_btn = Button(text='⚡ Flash: Off', size_hint_x=0.5)
        self.flash_btn.bind(on_press=self.toggle_flash)
        top_buttons.add_widget(self.flash_btn)
        
        button_layout.add_widget(top_buttons)
        
        # Middle row buttons - 回転コントロールを追加
        middle_buttons = BoxLayout(size_hint_y=0.5)
        
        # Rotation button
        self.rotation_btn = Button(text=f'🔄 {self.camera_rotation}°', size_hint_x=0.5)
        self.rotation_btn.bind(on_press=self.rotate_camera)
        middle_buttons.add_widget(self.rotation_btn)
        
        # Placeholder button for balance
        placeholder_btn = Button(text='', size_hint_x=0.5, background_color=(0, 0, 0, 0))
        middle_buttons.add_widget(placeholder_btn)
        
        button_layout.add_widget(middle_buttons)
        
        # Bottom row buttons
        bottom_buttons = BoxLayout(size_hint_y=0.5)
        
        # Resolution toggle
        self.res_btn = Button(text='HD', size_hint_x=0.5)
        self.res_btn.bind(on_press=self.toggle_resolution)
        bottom_buttons.add_widget(self.res_btn)
        
        # Settings button
        settings_btn = Button(text='⚙️', size_hint_x=0.5)
        settings_btn.bind(on_press=self.show_settings)
        bottom_buttons.add_widget(settings_btn)
        
        button_layout.add_widget(bottom_buttons)
        
        layout.add_widget(button_layout)
        
        # ズームコントロールを画面右側に配置（位置を調整）
        zoom_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.08, 0.2),
            pos_hint={'x': 0.92, 'y': 0.25}
        )
        
        zoom_in_btn = Button(text='🔍+', size_hint_y=0.5, background_color=(0, 0, 0, 0.5), font_size=20)
        zoom_in_btn.bind(on_press=self.zoom_in)
        zoom_layout.add_widget(zoom_in_btn)
        
        zoom_out_btn = Button(text='🔍-', size_hint_y=0.5, background_color=(0, 0, 0, 0.5), font_size=20)
        zoom_out_btn.bind(on_press=self.zoom_out)
        zoom_layout.add_widget(zoom_out_btn)
        
        layout.add_widget(zoom_layout)
        
        # カメラの初期化を遅らせる
        Clock.schedule_once(self.init_camera, 3)
        
        return layout
    
    def update_rect(self, instance, value):
        # 半透明背景の更新
        instance.canvas.before.clear()
        from kivy.graphics import Color, Rectangle
        with instance.canvas.before:
            Color(0, 0, 0, 0.3)
            Rectangle(pos=instance.pos, size=instance.size)
    
    def on_texture_update(self, instance, texture):
        """カメラのtextureが更新されたときにフレームを回転させる"""
        if texture:
            try:
                # textureからフレームを取得
                frame = self.texture_to_frame(texture)
                
                # フレームを回転（常に現在の回転角度を適用）
                rotated_frame = self.rotate_frame(frame, self.camera_rotation)
                
                # 回転したフレームをtextureに設定
                self.frame_to_texture(rotated_frame, texture)
                
            except Exception as e:
                print(f"Frame rotation error: {e}")
    
    def texture_to_frame(self, texture):
        """Kivy textureをOpenCVフレームに変換"""
        # textureのサイズを取得
        width, height = texture.size
        
        # textureのピクセルデータを取得
        pixels = texture.pixels
        
        # RGBAからBGRに変換してOpenCV形式に
        frame = np.frombuffer(pixels, dtype=np.uint8).reshape(height, width, 4)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        
        return frame
    
    def rotate_frame(self, frame, angle):
        """フレームを指定角度で回転"""
        if angle == 0:
            return frame
        elif angle == 90:
            return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            return cv2.rotate(frame, cv2.ROTATE_180)
        elif angle == 270:
            return cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            # 任意の角度での回転
            height, width = frame.shape[:2]
            center = (width // 2, height // 2)
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            return cv2.warpAffine(frame, rotation_matrix, (width, height))
    
    def frame_to_texture(self, frame, texture):
        """OpenCVフレームをKivy textureに変換"""
        # BGRからRGBAに変換
        frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        
        # フレームを1次元配列に変換
        pixels = frame_rgba.tobytes()
        
        # textureにピクセルデータを設定
        texture.blit_buffer(pixels, colorfmt='rgba', bufferfmt='ubyte')
    
    def init_camera(self, dt):
        try:
            # カメラ権限を確認してから初期化
            if platform == 'android':
                from plyer import permissions
                if permissions.check_permission('android.permission.CAMERA'):
                    Clock.schedule_once(self.start_camera_safe, 1)
                else:
                    def on_permissions(result):
                        if result:
                            Clock.schedule_once(self.start_camera_safe, 1)
                        else:
                            print("Camera permission denied")
                            self.show_camera_error()
                    permissions.request_permission('android.permission.CAMERA', on_permissions)
            else:
                Clock.schedule_once(self.start_camera_safe, 1)
        except Exception as e:
            print(f"Camera initialization error: {e}")
            Clock.schedule_once(self.start_camera_safe, 1)
    
    def start_camera_safe(self, dt):
        try:
            self.camera.play = True
            # Androidでのカメラ向き修正 - rotationプロパティを使用
            if platform == 'android':
                self.apply_camera_rotation()
            print("Camera started successfully")
        except Exception as e:
            print(f"Failed to start camera: {e}")
            self.show_camera_error()
    
    def apply_camera_rotation(self):
        """カメラの回転を適用する"""
        try:
            # orientationに基づいてカメラの向きを設定
            if self.camera_rotation == 0:
                self.camera.orientation = 'portrait'
            elif self.camera_rotation == 90:
                self.camera.orientation = 'landscape'
            elif self.camera_rotation == 180:
                self.camera.orientation = 'portrait'
            else:  # 270
                self.camera.orientation = 'landscape'

            # Cameraウィジェットのrotationも設定
            self.camera.rotation = self.camera_rotation

            # 回転変更を強制的に適用するためにカメラを再起動
            if self.camera.play:
                self.camera.play = False
                Clock.schedule_once(lambda dt: setattr(self.camera, 'play', True), 0.1)

            print(f"Applied camera rotation: {self.camera_rotation}°")
        except Exception as e:
            print(f"Camera rotation error: {e}")

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
        self.root.add_widget(error_layout)
    
    def retry_camera(self, instance):
        # カメラを再試行
        Clock.schedule_once(self.init_camera, 0.1)
    
    def capture(self, instance):
        # Capture image
        if self.camera.texture:
            try:
                # textureからフレームを取得
                frame = self.texture_to_frame(self.camera.texture)
                
                # 現在の回転角度を考慮してフレームを回転
                if self.camera_rotation != 0:
                    frame = self.rotate_frame(frame, -self.camera_rotation)  # 保存時は逆回転
                
                # 画像を保存
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
                
                # Save frame as image
                cv2.imwrite(filepath, frame)
                print(f'Image saved to: {filepath}')
                
            except Exception as e:
                print(f"Capture error: {e}")
                # フォールバックとして元の方法を使用
                try:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f'photo_{timestamp}.png'
                    
                    if platform == 'android':
                        filepath = f'/storage/emulated/0/DCIM/Camera/{filename}'
                    else:
                        filepath = filename
                    
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    self.camera.export_to_png(filepath)
                    print(f'Image saved to: {filepath} (fallback)')
                except Exception as e2:
                    print(f"Capture fallback error: {e2}")
    
    def rotate_camera(self, instance):
        """カメラの向きを90度回転させる"""
        # 回転角度を90度ずつ変更（0° → 90° → 180° → 270° → 0°）
        self.camera_rotation = (self.camera_rotation + 90) % 360
        self.rotation_btn.text = f'🔄 {self.camera_rotation}°'

        # 回転を即座に適用
    def rotate_camera(self, instance):
        """カメラの向きを90度回転させる"""
        # 回転角度を90度ずつ変更（0° → 90° → 180° → 270° → 0°）
        self.camera_rotation = (self.camera_rotation + 90) % 360
        self.rotation_btn.text = f'🔄 {self.camera_rotation}°'

        # 回転を即座に適用
        self.apply_camera_rotation()

        print(f"Camera rotation changed to {self.camera_rotation}°")

    def zoom_in(self, instance):
        if hasattr(self.camera, 'zoom'):
            current_zoom = getattr(self.camera, 'zoom', 1.0)
            self.camera.zoom = min(current_zoom + 0.1, 2.0)
    
    def zoom_out(self, instance):
        if hasattr(self.camera, 'zoom'):
            current_zoom = getattr(self.camera, 'zoom', 1.0)
            self.camera.zoom = max(current_zoom - 0.1, 0.1)
    
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


if __name__ == '__main__':
    CameraApp().run()
