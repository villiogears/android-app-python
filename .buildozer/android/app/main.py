from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import platform
try:
    if platform == 'android':
        from jnius import autoclass, cast
        from android import activity
        from plyer import permission
    else:
        autoclass = cast = activity = permission = None
except ImportError:
    autoclass = cast = activity = permission = None
from functools import partial
from datetime import datetime
from os.path import exists
import os

# camera4kivyをインポート
try:
    from camera4kivy import XCamera
    CAMERA4KIVY_AVAILABLE = True
except ImportError:
    from kivy.uix.camera import Camera as XCamera
    CAMERA4KIVY_AVAILABLE = False


class CameraApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Androidではカメラセンサーの回転補正を行う
        if platform == 'android':
            self.camera_rotation = 0  # Androidでは0°から開始して自動補正
        else:
            self.camera_rotation = 90  # PCでは右向きから開始

        # camera4kivyの利用可能状態をチェック
        self.camera4kivy_available = CAMERA4KIVY_AVAILABLE
        if self.camera4kivy_available:
            print("camera4kivy is available - using advanced camera features")
        else:
            print("camera4kivy not available - using standard Kivy camera")

    def build(self):
        # Main layout - カメラを最大化するためにFloatLayoutを使用
        from kivy.uix.floatlayout import FloatLayout
        layout = FloatLayout()

        # Camera widget - camera4kivyを使用
        if self.camera4kivy_available:
            # camera4kivyを使用する場合
            self.camera = XCamera(
                play=False,
                size_hint=(1, 1),
                pos_hint={'x': 0, 'y': 0},
                orientation='same'  # デバイスの向きに合わせる
            )
            # camera4kivyの設定
            if platform == 'android':
                self.camera.resolution = (1920, 1080)  # FHD解像度
                self.camera.fps = 30
            else:
                self.camera.resolution = (1280, 720)   # HD解像度
                self.camera.fps = 30
        else:
            # camera4kivyが利用できない場合のフォールバック
            self.camera = XCamera(
                play=False,
                size_hint=(1, 1),
                pos_hint={'x': 0, 'y': 0}
            )
            if platform == 'android':
                self.camera.resolution = (1920, 1080)
            else:
                self.camera.resolution = (1280, 720)

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
        rotation_text = f'🔄 {self.camera_rotation}°'
        self.rotation_btn = Button(text=rotation_text, size_hint_x=0.5)
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

    def init_camera(self, dt):
        try:
            # camera4kivyを使用する場合
            if self.camera4kivy_available:
                print("Initializing camera with camera4kivy...")
                Clock.schedule_once(self.start_camera_safe, 1)
            else:
                # 標準Kivy Cameraの場合
                if platform == 'android':
                    if permission and hasattr(permission, 'check_permission'):
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
                        # plyerが利用できない場合
                        Clock.schedule_once(self.start_camera_safe, 1)
                else:
                    Clock.schedule_once(self.start_camera_safe, 1)
        except Exception as e:
            print(f"Camera initialization error: {e}")
            Clock.schedule_once(self.start_camera_safe, 1)

    def start_camera_safe(self, dt):
        try:
            self.camera.play = True
            if self.camera4kivy_available:
                # camera4kivyの場合、Androidのカメラ回転補正を行う
                if platform == 'android':
                    self.setup_android_camera_orientation()
                else:
                    self.apply_camera_rotation()
                print("Camera started successfully with camera4kivy")
            else:
                # 標準Kivy Cameraの場合も、表示回転のみ適用
                self.apply_camera_rotation()
                print("Camera started successfully (standard)")
        except Exception as e:
            print(f"Failed to start camera: {e}")
            self.show_camera_error()

    def setup_android_camera_orientation(self):
        """Androidカメラの自動回転補正を設定"""
        try:
            if platform == 'android' and self.camera4kivy_available:
                # camera4kivyのカメラにorientationを設定
                # Androidでは通常、背面カメラは270°のorientationが必要（デバイスによる）
                if hasattr(self.camera, 'orientation'):
                    # 背面カメラの場合（通常は270°）
                    self.camera.orientation = 270
                    print(f"Set camera orientation to 270° for Android")
                else:
                    # orientationが利用できない場合は手動回転を適用
                    self.camera.rotation = 0
                    print("Camera orientation not available, using manual rotation")

                # 少し待ってから回転を適用
                Clock.schedule_once(lambda dt: self.apply_camera_rotation(), 0.5)
            else:
                self.apply_camera_rotation()
        except Exception as e:
            print(f"Android camera orientation setup error: {e}")
            self.apply_camera_rotation()

    def apply_android_rotation(self):
        """Android特有のカメラ回転処理"""
        try:
            if self.camera4kivy_available and hasattr(self.camera, 'orientation'):
                # orientationを更新（背面カメラは通常270°）
                base_orientation = 270
                # ユーザーの回転要求に応じてorientationを調整
                if self.camera_rotation == 90:
                    self.camera.orientation = base_orientation  # 通常の向き
                elif self.camera_rotation == 180:
                    self.camera.orientation = base_orientation + 90  # 180°回転
                elif self.camera_rotation == 270:
                    self.camera.orientation = base_orientation + 180  # 270°回転
                elif self.camera_rotation == 0:
                    self.camera.orientation = base_orientation + 270  # 360°/0°回転

                print(f"Android camera orientation set to {self.camera.orientation}° (base: {base_orientation}° + user: {self.camera_rotation}°)")
            else:
                # orientationが利用できない場合は通常の回転を適用
                self.apply_camera_rotation()
        except Exception as e:
            print(f"Android rotation error: {e}")
            self.apply_camera_rotation()

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
        # camera4kivyを使用したキャプチャ
        if self.camera4kivy_available:
            try:
                # camera4kivyのキャプチャ機能を使用
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'photo_{timestamp}.png'

                if platform == 'android':
                    filepath = f'/storage/emulated/0/DCIM/Camera/{filename}'
                else:
                    filepath = filename

                # Ensure directory exists
                os.makedirs(os.path.dirname(filepath), exist_ok=True)

                # camera4kivyのキャプチャ機能を使用
                if hasattr(self.camera, 'capture'):
                    self.camera.capture(filepath)
                    print(f'Image saved to: {filepath} (camera4kivy)')
                else:
                    # フォールバック
                    self.camera.export_to_png(filepath)
                    print(f'Image saved to: {filepath} (fallback)')

            except Exception as e:
                print(f"Capture error: {e}")
        else:
            # camera4kivyが利用できない場合のフォールバック
            try:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'photo_{timestamp}.png'

                if platform == 'android':
                    filepath = f'/storage/emulated/0/DCIM/Camera/{filename}'
                else:
                    filepath = filename

                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                self.camera.export_to_png(filepath)
                print(f'Image saved to: {filepath} (standard)')
            except Exception as e:
                print(f"Capture fallback error: {e}")

    def rotate_camera(self, instance):
        """カメラの表示のみを回転させる - Androidではorientationを考慮"""
        # 回転角度を90度ずつ変更
        self.camera_rotation = (self.camera_rotation + 90) % 360
        self.rotation_btn.text = f'🔄 {self.camera_rotation}°'

        # Androidの場合、orientationによる自動補正を考慮して回転を適用
        if platform == 'android' and self.camera4kivy_available:
            self.apply_android_rotation()
        else:
            # 表示回転のみを即座に適用（カメラの実際の向きは変更しない）
            self.apply_camera_rotation()

        print(f"Display rotation changed to {self.camera_rotation}° (preview only)")

    def zoom_in(self, instance):
        """camera4kivyのズーム機能を使用"""
        if self.camera4kivy_available and hasattr(self.camera, 'zoom'):
            current_zoom = getattr(self.camera, 'zoom', 1.0)
            self.camera.zoom = min(current_zoom + 0.1, 2.0)
            print(f"Zoom in: {self.camera.zoom}")
        elif hasattr(self.camera, 'zoom'):
            current_zoom = getattr(self.camera, 'zoom', 1.0)
            self.camera.zoom = min(current_zoom + 0.1, 2.0)
            print(f"Zoom in: {self.camera.zoom} (standard)")

    def zoom_out(self, instance):
        """camera4kivyのズーム機能を使用"""
        if self.camera4kivy_available and hasattr(self.camera, 'zoom'):
            current_zoom = getattr(self.camera, 'zoom', 1.0)
            self.camera.zoom = max(current_zoom - 0.1, 0.1)
            print(f"Zoom out: {self.camera.zoom}")
        elif hasattr(self.camera, 'zoom'):
            current_zoom = getattr(self.camera, 'zoom', 1.0)
            self.camera.zoom = max(current_zoom - 0.1, 0.1)
            print(f"Zoom out: {self.camera.zoom} (standard)")

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
        """camera4kivyの解像度切り替え機能を使用"""
        if self.camera4kivy_available:
            current_res = self.camera.resolution
            if current_res == (640, 480):
                self.camera.resolution = (1280, 720)
                self.res_btn.text = 'HD'
            elif current_res == (1280, 720):
                self.camera.resolution = (1920, 1080)
                self.res_btn.text = 'FHD'
            elif current_res == (1920, 1080):
                self.camera.resolution = (3840, 2160)  # 4K
                self.res_btn.text = '4K'
            else:
                self.camera.resolution = (640, 480)
                self.res_btn.text = 'SD'
            print(f"Resolution changed to: {self.camera.resolution}")
        else:
            # 標準Kivy Cameraの場合
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
