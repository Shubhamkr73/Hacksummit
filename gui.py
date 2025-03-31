from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, RoundedRectangle
from json import dump


class DynamicForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=15, **kwargs)

        with self.canvas.before:
            Color(0.12, 0.12, 0.12, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.control_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        
        self.control_layout.add_widget(Label(text="Number of Items:", font_size=22, color=(1, 1, 1, 1)))

        self.num_input = TextInput(
            text="1", multiline=False, size_hint_x=0.2, font_size=22,
            background_color=(0.2, 0.6, 1, 1), foreground_color=(1, 1, 1, 1),
            padding=[10, 10]
        )
        self.num_input.bind(text=self.update_fields)
        self.control_layout.add_widget(self.num_input)

        self.add_widget(self.control_layout)

        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.field_layout = GridLayout(cols=1, size_hint_y=None, spacing=15, padding=10)
        self.field_layout.bind(minimum_height=self.field_layout.setter('height'))
        self.scroll_view.add_widget(self.field_layout)

        self.add_widget(self.scroll_view)

        self.submit_btn = Button(
            text="Save Data",
            size_hint_y=None, height=60,
            background_color=(0, 0.8, 0.6, 1), 
            color=(1, 1, 1, 1),  
            font_size=24,
            bold=True
        )
        self.submit_btn.bind(on_press=self.save_data)
        self.add_widget(self.submit_btn)

        self.fields = []
        self.update_fields()

    def update_fields(self, *args):
        """Dynamically updates the form fields."""
        try:
            num_items = max(1, int(self.num_input.text))
        except ValueError:
            num_items = 1  

        self.field_layout.clear_widgets()
        self.fields = []

        for i in range(num_items):
            item_box = BoxLayout(orientation="vertical", size_hint_y=None, height=220, padding=15, spacing=10)

            with item_box.canvas.before:
                Color(0.15, 0.15, 0.15, 1)  
                item_box.rect = RoundedRectangle(size=item_box.size, pos=item_box.pos, radius=[10])
            item_box.bind(size=self.update_rect, pos=self.update_rect)

            title = Label(text=f"Item {i+1}", font_size=20, bold=True, color=(1, 1, 1, 1), size_hint_y=None, height=40)

            name = TextInput(
                hint_text=f"Enter Name {i+1}", multiline=False, font_size=18,
                background_color=(0.3, 0.3, 0.3, 1), foreground_color=(1, 1, 1, 1),
                padding=[10, 10]
            )
            desc = TextInput(
                hint_text=f"Enter Description {i+1}", multiline=True, font_size=18,
                background_color=(0.3, 0.3, 0.3, 1), foreground_color=(1, 1, 1, 1),
                padding=[10, 10]
            )
            link = TextInput(
                hint_text=f"Enter Link {i+1}", multiline=False, font_size=18,
                background_color=(0.3, 0.3, 0.3, 1), foreground_color=(1, 1, 1, 1),
                padding=[10, 10]
            )

            name.bind(text=self.reset_background)
            desc.bind(text=self.reset_background)
            link.bind(text=self.reset_background)

            item_box.add_widget(title)
            item_box.add_widget(name)
            item_box.add_widget(desc)
            item_box.add_widget(link)

            self.fields.append({"name": name, "desc": desc, "link": link})
            self.field_layout.add_widget(item_box)

    def reset_background(self, instance, value):
        """Resets the background color when the user starts typing."""
        instance.background_color = (0.3, 0.3, 0.3, 1)

    def show_warning_popup(self, message):
        """Displays a warning popup."""
        popup_layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        popup_label = Label(text=message, font_size=20, color=(1, 0, 0, 1)) 
        close_btn = Button(text="Close", size_hint_y=None, height=50, font_size=18, background_color=(1, 0, 0, 1))

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_btn)

        popup = Popup(title="Warning", content=popup_layout, size_hint=(None, None), size=(400, 250))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def save_data(self, instance):
        """Saves entered data to a JSON file after validation."""
        data = []
        is_valid = True

        for f in self.fields:
            name_text = f["name"].text.strip()
            desc_text = f["desc"].text.strip()
            link_text = f["link"].text.strip()

            if not name_text or not desc_text or not link_text:
                is_valid = False

                if not name_text:
                    f["name"].background_color = (1, 0.2, 0.2, 1)  
                if not desc_text:
                    f["desc"].background_color = (1, 0.2, 0.2, 1)
                if not link_text:
                    f["link"].background_color = (1, 0.2, 0.2, 1)

            data.append({"name": name_text, "desc": desc_text, "link": link_text})

        if is_valid:
            with open('data.json', 'w') as file:
                dump(data, file)
            self.show_warning_popup("Data saved successfully!")
        else:
            self.show_warning_popup("Please fill in all fields!")

    def update_rect(self, *args):
        """Updates background elements when size changes."""
        self.rect.size = self.size
        self.rect.pos = self.pos


class DynamicFormApp(App):
    def build(self):
        return DynamicForm()


if __name__ == "__main__":
    DynamicFormApp().run()
