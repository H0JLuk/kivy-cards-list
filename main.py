from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView

from kivy.properties import ObjectProperty, StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock


class ScreenManagement(ScreenManager):
  card_list_screen = ObjectProperty(None)
  card_item_screen = ObjectProperty(None)

class Header(BoxLayout):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  manager = ObjectProperty(None)

class CardListScreen(Screen):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.load_data()
    print('product', self.data[0])
    # print('ids', self.ids)
    # Clock.schedule_interval(self.load_data, 1)

  def on_enter(self, *args):
    print('HEREEE !!!', self.ids)
    return super().on_enter(*args)

  def load_data(self, *args):
    store = JsonStore("card_data.json")

    product_list = []
    for key in range(store.count()):
      product_item = store.get(key)
      product_list.append(product_item)
    self.data = product_list

  def on_enter(self, *args):
    # CardListItem()
    super().on_enter(*args)
    # print('ids', self.ids)
    # if not self.ids.product_list.children:
    #   self.ids.product_list.add_widget(
    #     CardListItem(
    #       on_release=self.controller.on_tap_card
    #     )
    #   )


class CardListItem(BoxLayout):
  pass


# --------------------------------------------------
class CardItemScreen(Screen):
  pass


kv = Builder.load_file("main.kv")
class CardApp(App):
  def build(self):
    return kv




# if __name__ == '__main__':
#   CardApp().run()

Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        id: box_lay
        Button:
            text: 'Goto settings'
            on_press: root.manager.current = 'settings'
        Button:
            id: btn
            text: 'Quit'

<SettingsScreen>:
    BoxLayout:
        Button:
            id: btn_2
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
""")

# Declare both screens
class MenuScreen(Screen):
  def on_enter(self, *args):
    print('hereee', self.ids)
    return super().on_enter(*args)

class SettingsScreen(Screen):
  pass

class TestApp(App):

  def build(self):
    # Create the screen manager
    sm = ScreenManager()
    sm.add_widget(MenuScreen(name='menu'))
    sm.add_widget(SettingsScreen(name='settings'))

    return sm

if __name__ == '__main__':
  TestApp().run()
