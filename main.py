import json
import random
from pathlib import Path

from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle


BG = (0.035, 0.04, 0.08, 1)
CARD = (0.09, 0.10, 0.17, 1)
PURPLE = (0.48, 0.30, 0.98, 1)
WHITE = (0.95, 0.96, 1, 1)
MUTED = (0.66, 0.69, 0.78, 1)


CHALLENGES = [
    {
        "title": "A SMALL IDEA",
        "tj": "💡 Як идея навис, ки зиндагии одамонро осон мекунад.",
        "en": "💡 Invent an idea that makes people's lives easier."
    },
    {
        "title": "THINK DIFFERENT",
        "tj": "🧠 Агар метавонистӣ як мушкили ҷаҳонро ҳал кунӣ, кадомашро интихоб мекардӣ?",
        "en": "🧠 If you could solve one world problem, which would you choose?"
    },
    {
        "title": "CREATE SOMETHING",
        "tj": "✨ Як идеяи нав барои барномаи оянда навис.",
        "en": "✨ Invent an idea for a future app."
    },
    {
        "title": "HELP THE WORLD",
        "tj": "🌍 Чӣ кор кунем, ки ҷаҳон барои ҳама беҳтар шавад?",
        "en": "🌍 What could make the world a better place for everyone?"
    }
]


class Card(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*CARD)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(20)]
            )
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *_):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MindSparkApp(App):

    def build(self):
        self.title = "MINDSPARK"
        Window.clearcolor = BG

        self.lang = "en"
        self.index = random.randrange(len(CHALLENGES))
        self.data_file = Path(self.user_data_dir) / "answers.json"
        self.answers = self.load_answers()

        self.root_box = BoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(12)
        )

        self.header = Label(
            text="[b]MIND[/b][color=8055FF]SPARK[/color]",
            markup=True,
            font_size=dp(27),
            size_hint_y=None,
            height=dp(48),
            halign="left"
        )
        self.header.bind(size=self.header.setter("text_size"))
        self.root_box.add_widget(self.header)

        self.subtitle = Label(
            text="IDEAS CAN CHANGE THE WORLD",
            color=MUTED,
            font_size=dp(11),
            size_hint_y=None,
            height=dp(25),
            halign="left"
        )
        self.subtitle.bind(size=self.subtitle.setter("text_size"))
        self.root_box.add_widget(self.subtitle)

        self.scroll = ScrollView()
        self.content = BoxLayout(
            orientation="vertical",
            spacing=dp(14),
            size_hint_y=None
        )
        self.content.bind(
            minimum_height=self.content.setter("height")
        )

        self.scroll.add_widget(self.content)
        self.root_box.add_widget(self.scroll)

        self.draw_home()
        return self.root_box

    def load_answers(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return []

    def save_answers(self):
        self.data_file.parent.mkdir(
            parents=True, exist_ok=True
        )
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(
                self.answers, f, ensure_ascii=False, indent=2
            )

    def make_label(self, text, size=dp(15), color=WHITE,
                   height=None, markup=False):
        label = Label(
            text=text,
            font_size=size,
            color=color,
            markup=markup,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=height or dp(48)
        )
        label.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", (value[0], None))
        )
        return label

    def make_button(self, text, callback, color=PURPLE):
        button = Button(
            text=text,
            size_hint_y=None,
            height=dp(50),
            background_normal="",
            background_color=color,
            color=WHITE,
            font_size=dp(15)
        )
        button.bind(on_release=callback)
        return button

    def draw_home(self):
        self.content.clear_widgets()

        challenge = CHALLENGES[self.index]
        question = challenge[
            "tj" if self.lang == "tj" else "en"
        ]

        self.content.add_widget(
            self.make_label(
                "TODAY'S CHALLENGE",
                dp(12), (0.65, 0.55, 1, 1), dp(28)
            )
        )

        card = Card(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(225)
        )

        card.add_widget(
            self.make_label(
                challenge["title"], dp(12),
                (0.65, 0.55, 1, 1), dp(30)
            )
        )

        card.add_widget(
            self.make_label(
                question, dp(19), WHITE, dp(115)
            )
        )

        card.add_widget(
            self.make_label(
                "✦ YOUR IDEAS MATTER",
                dp(11), MUTED, dp(25)
            )
        )

        self.content.add_widget(card)

        self.answer_input = TextInput(
            hint_text=(
                "Идеяи худро навис..."
                if self.lang == "tj"
                else "Write your idea here..."
            ),
            multiline=True,
            size_hint_y=None,
            height=dp(125),
            padding=dp(14),
            background_normal="",
            background_active="",
            background_color=CARD,
            foreground_color=WHITE,
            hint_text_color=MUTED,
            cursor_color=PURPLE,
            font_size=dp(16)
        )
        self.content.add_widget(self.answer_input)

        self.status = self.make_label(
            "", dp(13), (0.5, 0.9, 0.7, 1), dp(30)
        )
        self.content.add_widget(self.status)

        self.content.add_widget(
            self.make_button(
                "✦  SAVE MY IDEA" if self.lang == "en"
                else "✦  НИГОҲ ДОШТАНИ ИДЕЯ",
                self.submit_answer
            )
        )

        self.content.add_widget(
            self.make_button(
                "↻  NEXT CHALLENGE" if self.lang == "en"
                else "↻  СУПОРИШИ НАВ",
                self.next_challenge,
                (0.15, 0.16, 0.25, 1)
            )
        )

        self.content.add_widget(
            self.make_button(
                "🌍  MY IDEAS" if self.lang == "en"
                else "🌍  ИДЕЯҲОИ МАН",
                self.show_answers,
                (0.15, 0.16, 0.25, 1)
            )
        )

        self.content.add_widget(
            self.make_button(
                "🌐  Тоҷикӣ / English",
                self.toggle_language,
                (0.15, 0.16, 0.25, 1)
            )
        )

        self.content.add_widget(
            self.make_label(
                f"YOUR IDEAS: {len(self.answers)}",
                dp(12), MUTED, dp(38)
            )
        )

    def submit_answer(self, *_):
        answer = self.answer_input.text.strip()

        if not answer:
            self.status.text = (
                "Аввал идея навис!"
                if self.lang == "tj"
                else "Write an idea first!"
            )
            return

        self.answers.append({
            "challenge": CHALLENGES[self.index]["title"],
            "answer": answer
        })

        self.save_answers()

        self.status.text = (
            "✓ Идея нигоҳ дошта шуд!"
            if self.lang == "tj"
            else "✓ Idea saved successfully!"
        )

        self.answer_input.text = ""

    def next_challenge(self, *_):
        old_index = self.index

        while len(CHALLENGES) > 1 and self.index == old_index:
            self.index = random.randrange(len(CHALLENGES))

        self.draw_home()

    def toggle_language(self, *_):
        self.lang = "tj" if self.lang == "en" else "en"
        self.draw_home()

    def show_answers(self, *_):
        self.content.clear_widgets()

        self.content.add_widget(
            self.make_label(
                "ИДЕЯҲОИ МАН" if self.lang == "tj"
                else "MY IDEAS",
                dp(22), WHITE, dp(55)
            )
        )

        if not self.answers:
            self.content.add_widget(
                self.make_label(
                    "Ҳоло ягон идея нест."
                    if self.lang == "tj"
                    else "No ideas saved yet.",
                    dp(15), MUTED, dp(60)
                )
            )

        for number, item in enumerate(reversed(self.answers), 1):
            card = Card(
                orientation="vertical",
                padding=dp(14),
                spacing=dp(8),
                size_hint_y=None,
                height=dp(125)
            )
            card.add_widget(
                self.make_label(
                    f"IDEA #{len(self.answers) - number + 1}",
                    dp(12), (0.65, 0.55, 1, 1), dp(25)
                )
            )
            card.add_widget(
                self.make_label(
                    item["answer"], dp(15), WHITE, dp(70)
                )
            )
            self.content.add_widget(card)

        self.content.add_widget(
            self.make_button(
                "← BACK" if self.lang == "en"
                else "← БАРГАШТАН",
                lambda *_: self.draw_home(),
                (0.15, 0.16, 0.25, 1)
            )
        )


if __name__ == "__main__":
    MindSparkApp().run()