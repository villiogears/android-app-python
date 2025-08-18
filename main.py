from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class MainApp(App):
	"""シンプルな Kivy アプリのサンプル。

	- 画面にラベルとボタンを表示します。
	- ボタンを押すとラベルのテキストが変化します。
	"""

	title = "Kivy Android Example"

	def build(self):
		root = BoxLayout(orientation='vertical', padding=10, spacing=10)
		self.label = Label(text='Hello, Kivy on Android!', font_size='20sp')
		btn = Button(text='Tap me')
		btn.bind(on_release=self.on_button)
		root.add_widget(self.label)
		root.add_widget(btn)
		return root

	def on_button(self, instance):
		self.label.text = 'ボタンが押されました'


if __name__ == '__main__':
	MainApp().run()
