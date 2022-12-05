from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView

from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore

PRODUCTS_DATA_FILE_NAME = 'card_data.json'

Builder.load_string("""
#:import hex kivy.utils.get_color_from_hex

<CardListScreen>:
  BoxLayout:
    orientation: "vertical"

    canvas.before:
      Color:
        rgba: hex('#999999')
      Rectangle:
        size: self.size

    Label:
      text: 'Продукты'
      bold: True
      font_style: 'H4'
      adaptive_height: True
      padding_x: '24dp'
      size_hint: 1, .1 # TODO: исправить на фикс высоту

    ScrollView:
      padding: '24dp'
      spacing: '24dp'
      do_scroll_x: False
      do_scroll_y: True
      BoxLayout:
        id: scrollable_list
        orientation: 'vertical'
        spacing: '70dp'
        size_hint_y: None
        height: self.minimum_height

<CardItemScreen>:
  BoxLayout:
    orientation: "vertical"
    canvas.before:
      Color:
        rgba: hex('#999999')
      Rectangle:
        size: self.size


    BoxLayout:
      size_hint: 1, None
      height: '50dp'
      pos_hint: {"top": 1}

      Button:
        text: 'Назад'
        size_hint: None, 1
        size_x: '10dp'
        on_press: root.on_back_press()
      
      Label:
        text: 'Информация о продукте'
        pos_hint: {'center_x': .5}

    BoxLayout:
      orientation: 'vertical'
      y: '-56dp'
      spacing: '12dp'
      padding: '24dp'

      Label:
        id: title
        text_size: self.width, None
        size_hint: 1, None
        halign: "center"

      AsyncImage:
        id: image
        size_hint: 1, None
        height: root.height / 1.8
        source: 'root.image'
        md_bg_color: 'grey'

      ScrollView:
        adaptive_height: True
        Label:
          id: content
          adaptive_height: True
          text_size: self.width, None
          size_hint: 1, None
          height: self.texture_size[1]

<CardListItem>:
  orientation: 'vertical'
  size_hint: 1, None
  height: '300dp'
  elevation: 4
  radius: 12
  padding: 12

  AsyncImage:
    size_hint: 1, None
    height: root.height / 1.8
    radius: 6
    source: root.image

  Label:
    text: root.title
    bold: True
    adaptive_height: True
    text_size: self.width, None
    size_hint: 1, None
    halign: "center"
    font_style: 'H6'

  Button:
    size_hint: None, None
    size: ['110dp', '60dp']
    pos_hint: {'center_x': .5}
    # padding: 6, 6
    text: "Read more"
    radius: 10
    on_press:
      print('ids', app.root.screens[1].ids)
      app.root.screens[1].ids.title.text = root.title
      app.root.screens[1].ids.content.text = root.description
      app.root.screens[1].ids.image.source = root.image

      app.root.transition.direction = 'left'
      app.root.current = 'card_item'
""")

# Declare both screens
class CardListScreen(Screen):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.__load_data()

  def on_enter(self, *args):
    super().on_enter(*args)

    if not self.ids.scrollable_list.children:
      for index, item in enumerate(self.data):
        self.ids.scrollable_list.add_widget(
          CardListItem(
            title=item.get('title'),
            description=item.get('description'),
            image=item.get('image'),
          )
        )

  def __load_data(self, *args):
    store = JsonStore(PRODUCTS_DATA_FILE_NAME)

    product_list = []
    for key in range(store.count()):
      product_item = store.get(key)
      product_list.append(product_item)
    self.data = product_list


class CardItemScreen(Screen):
  def on_enter(self, *args):
    return super().on_enter(*args);

  def on_back_press(self):
    self.manager.transition.direction = 'right'
    self.manager.current = 'card_list'


class CardListItem(BoxLayout):
  title = StringProperty()
  description = StringProperty()
  image = StringProperty()


class TestApp(App):
  def build(self):
    self.title = 'Product Application'
    sm = ScreenManager()
    sm.add_widget(CardListScreen(name='card_list'))
    sm.add_widget(CardItemScreen(name='card_item'))
    return sm

if __name__ == '__main__':
  TestApp().run()