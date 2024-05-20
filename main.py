from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget
from kivy.uix.camera import Camera
import time
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.metrics import dp

Window.size = (450, 900)

Builder.load_file("homescreen.kv")

class WelcomeScreen(Screen):
    pass

class RotatingCamera(Camera):
    def on_texture(self, instance, texture):
        if texture:
            img = PilImage.frombytes('RGBA', texture.size, texture.pixels)
            img = img.rotate(-90, expand=True)
            buf = img.tobytes()
            texture = Texture.create(size=img.size, colorfmt='rgba')
            texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
            self.texture = texture

class Homescreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mycamera = self.ids.camera
        self.myimage = Image()
        self.resultbox = self.ids.resultbox
        self.mybox = self.ids.mybox

    def captureyouface(self):
        timenow = time.strftime("%Y%m%d_%H%M%S")
        self.mycamera.export_to_png("myimage_{}.png".format(timenow))
        self.myimage.source = "myimage_{}.png".format(timenow)
        self.resultbox.add_widget(
            OneLineAvatarListItem(
                ImageLeftWidget(
                    source="myimage_{}.png".format(timenow),
                    size_hint_x=0.3,
                    size_hint_y=1,
                    size=(300, 300)
                )
            )
        )

class GridScreen(Screen):
    def generate_grid(self, rows, cols):
        self.ids.grid_container.clear_widgets()
        grid = GridLayout(cols=cols, row_default_height=dp(40), size_hint_y=None)
        for i in range(rows * cols):
            grid.add_widget(Button())
        grid.height = grid.minimum_height
        self.ids.grid_container.add_widget(grid)

    def reset_grid(self):
        self.ids.grid_container.clear_widgets()

class CrosswordApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(Homescreen(name='home'))
        sm.add_widget(GridScreen(name='gridscreen'))
        return sm

CrosswordApp().run()
