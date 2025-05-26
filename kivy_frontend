from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests
from utils import berechne_insulinmenge

class InsulinBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.bz_input = TextInput(hint_text='Blutzuckerwert eingeben (mg/dL)', multiline=False, input_filter='int')
        self.be_input = TextInput(hint_text='Broteinheiten (BE) eingeben', multiline=False, input_filter='float')
        self.result_label = Label(text='Ergebnis wird hier angezeigt.')

        self.calc_button = Button(text='Insulin berechnen')
        self.calc_button.bind(on_press=self.berechne)

        self.add_widget(self.bz_input)
        self.add_widget(self.be_input)
        self.add_widget(self.calc_button)
        self.add_widget(self.result_label)

    def berechne(self, instance):
        try:
            bz = int(self.bz_input.text)
            be = float(self.be_input.text)
            menge, bemerkung = berechne_insulinmenge(bz, be)
            self.result_label.text = f"Insulin: {menge:.2f} IE\n{bemerkung}"
        except ValueError:
            self.result_label.text = "Ungültige Eingabe. Bitte Werte überprüfen."

class InsulinApp(App):
    def build(self):
        return InsulinBox()

if __name__ == '__main__':
    InsulinApp().run()
