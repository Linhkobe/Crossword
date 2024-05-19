from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivymd.uix.list import MDList,OneLineAvatarListItem,ImageLeftWidget
from kivy.uix.camera import Camera
import time
import os
import subprocess
from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout


Window.size = (450,900)


Builder.load_file("homescreen.kv")


class WelcomeScreen(Screen):
   pass


class RotatingCamera(Camera):
   def on_texture(self, instance, texture):
       # Rotate the texture by 90 degrees clockwise
       if texture:
           img = PilImage.frombytes('RGBA', texture.size, texture.pixels)
           img = img.rotate(-90, expand=True)
           buf = img.tobytes()
           texture = Texture.create(size=img.size, colorfmt='rgba')
           texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
           self.texture = texture


class Homescreen(MDScreen):
   def __init__(self,**kwargs):
       super().__init__(**kwargs)
       
       self.mycamera = self.ids.camera
       self.myimage = Image()
       self.resultbox = self.ids.resultbox
       self.mybox = self.ids.mybox


        # Join files
       # self.image_folder = os.path.join(os.getcwd(), "kivy_test", "kivymdCamera")
       # self.backend_folder = os.path.join(os.getcwd(), "kivy_test", "backend")




   def captureyouface(self):
       # CREATE TIMESTAMP NOT FOR YOU FILE IMAGE
       timenow = time.strftime("%Y%m%d_%H%M%S")
       # timenow = time.strftime("%Y%m%d_%H%M%S")


       # # AND EXPORT YOU CAMERA CAPTURE TO PNG IMAGE
       self.mycamera.export_to_png("myimage_{}.png".format(timenow))
       # timenow = time.strftime("%Y%m%d_%H%M%S")
       # image_path = os.path.join(self.image_folder, "myimage_{}.png".format(timenow))


       # # Export image
       # self.mycamera.export_to_png(image_path)


       # # Call backend scripts
       # subprocess.run(["python", os.path.join(self.backend_folder, "detectionDeGrilleCW.py"), image_path])
       # subprocess.run(["python", os.path.join(self.backend_folder, "main_definition_ocr.py"), image_path])
       self.myimage.source = "myimage_{}.png".format(timenow)
       self.resultbox.add_widget(
           OneLineAvatarListItem(
               ImageLeftWidget(
                   source="myimage_{}.png".format(timenow),
                   size_hint_x=0.3,
                   size_hint_y=1,


                   # AND SET YOU WIDHT AND HEIGT YOU PHOTO
                   size=(300,300)


                   )
               #   ,
               # text=self.ids.name.text
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
