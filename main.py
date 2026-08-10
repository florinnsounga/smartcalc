"""
SmartCalc By Florin Pro
"One app, many solutions."

Application mobile de calculs multiples — Python + Kivy.
Thème sombre / doré, inspiré de la maquette officielle.

Modules :
- Calculatrice (simple)
- IntimeGirls (cycle menstruel)
- Calcul d'âge
- Convertisseur (unités)
- Scientifique
- Pourcentage
- Jours entre dates
"""

import math
import sys
from datetime import datetime, timedelta

# Correction pour Windows : sans cela, si l'ecran est en zoom > 100%,
# les clics de souris ne s'alignent pas avec les boutons affiches.
if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner


# ----------------------------------------------------------------------
# THEME
# ----------------------------------------------------------------------
# Couleurs inspirées de la maquette SmartCalc By Florin Pro
BG_DARK = (0.043, 0.058, 0.094, 1)      # fond bleu nuit très sombre
CARD_DARK = (0.086, 0.106, 0.157, 1)    # cartes légèrement plus claires
GOLD = (0.88, 0.68, 0.24, 1)            # doré (titre, accents)
WHITE = (1, 1, 1, 1)
GREY_TEXT = (0.75, 0.78, 0.85, 1)

MODULE_COLORS = {
    "calc": (0.18, 0.75, 0.45, 1),        # vert - Calculatrice
    "intime": (0.86, 0.27, 0.42, 1),      # rose/rouge - IntimeGirls
    "age": (0.88, 0.48, 0.20, 1),         # orange - Calcul d'age
    "convert": (0.23, 0.48, 0.86, 1),     # bleu - Convertisseur
    "sci": (0.45, 0.32, 0.88, 1),         # violet - Scientifique
    "percent": (0.88, 0.66, 0.20, 1),     # or - Pourcentage
    "days": (0.18, 0.62, 0.60, 1),        # teal - Jours entre dates
}


# ----------------------------------------------------------------------
# INTERFACE (Kivy Language)
# ----------------------------------------------------------------------
KV = """
#:import dp kivy.metrics.dp

<ScreenBG@BoxLayout>:
    canvas.before:
        Color:
            rgba: %s
        Rectangle:
            pos: self.pos
            size: self.size

<TopBar@BoxLayout>:
    size_hint_y: None
    height: dp(50)
    RoundButton:
        text: "< Retour"
        background_color: 0.22, 0.24, 0.30, 1
        on_release: app.root.current = "home"

<RoundButton@Button>:
    background_normal: ''
    background_color: %s
    color: 1, 1, 1, 1
    font_size: '17sp'
    size_hint_y: None
    height: dp(52)

<ScreenTitle@Label>:
    size_hint_y: None
    height: dp(45)
    font_size: '24sp'
    bold: True
    color: %s

<FieldLabel@Label>:
    size_hint_y: None
    height: dp(24)
    font_size: '14sp'
    color: %s
    halign: 'left'
    text_size: self.size

<ResultLabel@Label>:
    size_hint_y: None
    height: dp(90)
    font_size: '20sp'
    color: %s
    halign: 'left'
    valign: 'top'
    text_size: self.size

<DarkInput@TextInput>:
    multiline: False
    size_hint_y: None
    height: dp(48)
    background_color: 0.13, 0.15, 0.21, 1
    foreground_color: 1, 1, 1, 1
    cursor_color: %s
    padding: dp(12), dp(12)

<ModuleCard@Button>:
    background_normal: ''
    background_color: 0, 0, 0, 0
    size_hint_y: None
    height: dp(90)
    module_color: 1, 1, 1, 1
    icon_text: "?"
    title_text: ""
    canvas.before:
        Color:
            rgba: %s
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(14)]
    BoxLayout:
        pos: self.parent.pos if self.parent else (0,0)
        size: self.parent.size if self.parent else (0,0)
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(4)
        Label:
            text: self.parent.parent.icon_text if self.parent.parent else ''
            size_hint_y: None
            height: dp(34)
            font_size: '20sp'
            bold: True
            color: self.parent.parent.module_color if self.parent.parent else (1,1,1,1)
            canvas.before:
                Color:
                    rgba: self.parent.parent.module_color if self.parent.parent else (1,1,1,1)
                Ellipse:
                    pos: self.center_x - dp(18), self.top - dp(38)
                    size: dp(36), dp(36)
            color: 1, 1, 1, 1
        Label:
            text: self.parent.parent.title_text if self.parent.parent else ''
            font_size: '13sp'
            color: 1, 1, 1, 1
            bold: True

ScreenManager:
    HomeScreen:
    SimpleCalcScreen:
    ScientificCalcScreen:
    AgeCalcScreen:
    DayCalcScreen:
    ConverterScreen:
    PercentageScreen:
    CycleCalcScreen:

<HomeScreen>:
    name: "home"
    ScreenBG:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(6)

        Label:
            text: "SmartCalc"
            size_hint_y: None
            height: dp(46)
            font_size: '34sp'
            bold: True
            color: 1, 1, 1, 1

        Label:
            text: "by Florin Pro"
            size_hint_y: None
            height: dp(30)
            font_size: '20sp'
            italic: True
            color: %s

        Label:
            text: "One app, many solutions."
            size_hint_y: None
            height: dp(26)
            font_size: '13sp'
            color: %s

        Widget:
            size_hint_y: None
            height: dp(10)

        GridLayout:
            cols: 2
            spacing: dp(12)
            size_hint_y: None
            height: dp(300)

            ModuleCard:
                icon_text: "123"
                title_text: "Calculatrice"
                module_color: %s
                on_release: app.root.current = "simple"

            ModuleCard:
                icon_text: "IG"
                title_text: "IntimeGirls"
                module_color: %s
                on_release: app.root.current = "cycle"

            ModuleCard:
                icon_text: "AGE"
                title_text: "Calcul d'age"
                module_color: %s
                on_release: app.root.current = "age"

            ModuleCard:
                icon_text: "<->"
                title_text: "Convertisseur"
                module_color: %s
                on_release: app.root.current = "convert"

            ModuleCard:
                icon_text: "fx"
                title_text: "Scientifique"
                module_color: %s
                on_release: app.root.current = "scientific"

            ModuleCard:
                icon_text: "%%"
                title_text: "Pourcentage"
                module_color: %s
                on_release: app.root.current = "percent"

        ModuleCard:
            icon_text: "date"
            title_text: "Jours entre dates"
            module_color: %s
            size_hint_y: None
            height: dp(70)
            on_release: app.root.current = "day"

        Widget:


<SimpleCalcScreen>:
    name: "simple"
    display: display
    ScreenBG:
        orientation: 'vertical'
        padding: dp(15)
        spacing: dp(10)
        TopBar:
        ScreenTitle:
            text: "Calculatrice"
        ResultLabel:
            id: display
            text: "0"
            font_size: '30sp'
            halign: 'right'
            text_size: self.size
            height: dp(70)
        GridLayout:
            cols: 4
            spacing: dp(8)
            RoundButton:
                text: "C"
                background_color: 0.75, 0.25, 0.25, 1
                on_release: app.simple_calc.clear()
            RoundButton:
                text: "/"
                on_release: app.simple_calc.press("/")
            RoundButton:
                text: "*"
                on_release: app.simple_calc.press("*")
            RoundButton:
                text: "<-"
                on_release: app.simple_calc.backspace()
            RoundButton:
                text: "7"
                on_release: app.simple_calc.press("7")
            RoundButton:
                text: "8"
                on_release: app.simple_calc.press("8")
            RoundButton:
                text: "9"
                on_release: app.simple_calc.press("9")
            RoundButton:
                text: "-"
                on_release: app.simple_calc.press("-")
            RoundButton:
                text: "4"
                on_release: app.simple_calc.press("4")
            RoundButton:
                text: "5"
                on_release: app.simple_calc.press("5")
            RoundButton:
                text: "6"
                on_release: app.simple_calc.press("6")
            RoundButton:
                text: "+"
                on_release: app.simple_calc.press("+")
            RoundButton:
                text: "1"
                on_release: app.simple_calc.press("1")
            RoundButton:
                text: "2"
                on_release: app.simple_calc.press("2")
            RoundButton:
                text: "3"
                on_release: app.simple_calc.press("3")
            RoundButton:
                text: "="
                background_color: 0.18, 0.75, 0.45, 1
                on_release: app.simple_calc.equals()
            RoundButton:
                text: "0"
                on_release: app.simple_calc.press("0")
            RoundButton:
                text: "."
                on_release: app.simple_calc.press(".")
            RoundButton:
                text: "%%"
                on_release: app.simple_calc.press("%%")


<ScientificCalcScreen>:
    name: "scientific"
    display: display
    ScreenBG:
        orientation: 'vertical'
        padding: dp(15)
        spacing: dp(10)
        TopBar:
        ScreenTitle:
            text: "Scientifique"
        ResultLabel:
            id: display
            text: "0"
            font_size: '30sp'
            halign: 'right'
            text_size: self.size
            height: dp(70)
        GridLayout:
            cols: 4
            spacing: dp(6)
            RoundButton:
                text: "sin"
                on_release: app.sci_calc.apply_function("sin")
            RoundButton:
                text: "cos"
                on_release: app.sci_calc.apply_function("cos")
            RoundButton:
                text: "tan"
                on_release: app.sci_calc.apply_function("tan")
            RoundButton:
                text: "C"
                background_color: 0.75, 0.25, 0.25, 1
                on_release: app.sci_calc.clear()
            RoundButton:
                text: "sqrt"
                on_release: app.sci_calc.apply_function("sqrt")
            RoundButton:
                text: "^"
                on_release: app.sci_calc.press("**")
            RoundButton:
                text: "log"
                on_release: app.sci_calc.apply_function("log10")
            RoundButton:
                text: "ln"
                on_release: app.sci_calc.apply_function("log")
            RoundButton:
                text: "7"
                on_release: app.sci_calc.press("7")
            RoundButton:
                text: "8"
                on_release: app.sci_calc.press("8")
            RoundButton:
                text: "9"
                on_release: app.sci_calc.press("9")
            RoundButton:
                text: "/"
                on_release: app.sci_calc.press("/")
            RoundButton:
                text: "4"
                on_release: app.sci_calc.press("4")
            RoundButton:
                text: "5"
                on_release: app.sci_calc.press("5")
            RoundButton:
                text: "6"
                on_release: app.sci_calc.press("6")
            RoundButton:
                text: "*"
                on_release: app.sci_calc.press("*")
            RoundButton:
                text: "1"
                on_release: app.sci_calc.press("1")
            RoundButton:
                text: "2"
                on_release: app.sci_calc.press("2")
            RoundButton:
                text: "3"
                on_release: app.sci_calc.press("3")
            RoundButton:
                text: "-"
                on_release: app.sci_calc.press("-")
            RoundButton:
                text: "0"
                on_release: app.sci_calc.press("0")
            RoundButton:
                text: "."
                on_release: app.sci_calc.press(".")
            RoundButton:
                text: "="
                background_color: 0.18, 0.75, 0.45, 1
                on_release: app.sci_calc.equals()
            RoundButton:
                text: "+"
                on_release: app.sci_calc.press("+")


<AgeCalcScreen>:
    name: "age"
    result_label: result_label
    day_input: day_input
    month_input: month_input
    year_input: year_input
    ScreenBG:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)
        TopBar:
        ScreenTitle:
            text: "Calcul d'age"
        FieldLabel:
            text: "Date de naissance (JJ/MM/AAAA)"
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(8)
            DarkInput:
                id: day_input
                hint_text: "JJ"
                input_filter: "int"
            DarkInput:
                id: month_input
                hint_text: "MM"
                input_filter: "int"
            DarkInput:
                id: year_input
                hint_text: "AAAA"
                input_filter: "int"
        RoundButton:
            text: "Calculer"
            background_color: 0.88, 0.48, 0.20, 1
            on_release: app.age_calc.compute()
        ResultLabel:
            id: result_label
            text: ""


<DayCalcScreen>:
    name: "day"
    result_label: result_label
    start_input: start_input
    end_input: end_input
    ScreenBG:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)
        TopBar:
        ScreenTitle:
            text: "Jours entre dates"
        FieldLabel:
            text: "Date de debut (JJ/MM/AAAA)"
        DarkInput:
            id: start_input
            hint_text: "ex: 01/01/2026"
        FieldLabel:
            text: "Date de fin (JJ/MM/AAAA)"
        DarkInput:
            id: end_input
            hint_text: "ex: 25/07/2026"
        RoundButton:
            text: "Calculer"
            background_color: 0.18, 0.62, 0.60, 1
            on_release: app.day_calc.compute()
        ResultLabel:
            id: result_label
            text: ""


<ConverterScreen>:
    name: "convert"
    result_label: result_label
    value_input: value_input
    category_spinner: category_spinner
    from_spinner: from_spinner
    to_spinner: to_spinner
    ScreenBG:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)
        TopBar:
        ScreenTitle:
            text: "Convertisseur"
        FieldLabel:
            text: "Categorie"
        Spinner:
            id: category_spinner
            text: "Longueur"
            values: ["Longueur", "Poids", "Temperature"]
            size_hint_y: None
            height: dp(45)
            on_text: app.converter.on_category_change()
        FieldLabel:
            text: "Valeur a convertir"
        DarkInput:
            id: value_input
            hint_text: "ex: 10"
            input_filter: "float"
        BoxLayout:
            size_hint_y: None
            height: dp(45)
            spacing: dp(8)
            Spinner:
                id: from_spinner
                text: "m"
                values: ["m", "km", "cm", "mile"]
            Label:
                text: "->"
                size_hint_x: None
                width: dp(30)
                color: 1, 1, 1, 1
            Spinner:
                id: to_spinner
                text: "km"
                values: ["m", "km", "cm", "mile"]
        RoundButton:
            text: "Convertir"
            background_color: 0.23, 0.48, 0.86, 1
            on_release: app.converter.compute()
        ResultLabel:
            id: result_label
            text: ""


<PercentageScreen>:
    name: "percent"
    result_label: result_label
    value_input: value_input
    percent_input: percent_input
    ScreenBG:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)
        TopBar:
        ScreenTitle:
            text: "Pourcentage"
        FieldLabel:
            text: "Valeur"
        DarkInput:
            id: value_input
            hint_text: "ex: 200"
            input_filter: "float"
        FieldLabel:
            text: "Pourcentage (%%)"
        DarkInput:
            id: percent_input
            hint_text: "ex: 15"
            input_filter: "float"
        RoundButton:
            text: "X%% de la valeur"
            background_color: 0.88, 0.66, 0.20, 1
            on_release: app.percentage.compute("of")
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(8)
            RoundButton:
                text: "Augmenter de X%%"
                background_color: 0.88, 0.66, 0.20, 1
                on_release: app.percentage.compute("increase")
            RoundButton:
                text: "Diminuer de X%%"
                background_color: 0.88, 0.66, 0.20, 1
                on_release: app.percentage.compute("decrease")
        ResultLabel:
            id: result_label
            text: ""


<CycleCalcScreen>:
    name: "cycle"
    result_label: result_label
    day_input: day_input
    month_input: month_input
    year_input: year_input
    length_input: length_input
    ScreenBG:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)
        TopBar:
        ScreenTitle:
            text: "IntimeGirls"
        FieldLabel:
            text: "Date des dernieres regles (JJ/MM/AAAA)"
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(8)
            DarkInput:
                id: day_input
                hint_text: "JJ"
                input_filter: "int"
            DarkInput:
                id: month_input
                hint_text: "MM"
                input_filter: "int"
            DarkInput:
                id: year_input
                hint_text: "AAAA"
                input_filter: "int"
        FieldLabel:
            text: "Duree moyenne du cycle (jours)"
        DarkInput:
            id: length_input
            hint_text: "ex: 28"
            input_filter: "int"
        RoundButton:
            text: "Calculer"
            background_color: 0.86, 0.27, 0.42, 1
            on_release: app.cycle_calc.compute()
        ResultLabel:
            id: result_label
            text: ""
""" % (
    BG_DARK, GOLD, GOLD,        # ScreenBG, RoundButton, ScreenTitle
    GREY_TEXT, GOLD, GOLD,      # FieldLabel, ResultLabel, DarkInput cursor
    CARD_DARK,                  # ModuleCard background
    GOLD, GREY_TEXT,            # "by Florin Pro", "One app..."
    MODULE_COLORS["calc"], MODULE_COLORS["intime"], MODULE_COLORS["age"],
    MODULE_COLORS["convert"], MODULE_COLORS["sci"], MODULE_COLORS["percent"],
    MODULE_COLORS["days"],
)


# ----------------------------------------------------------------------
# ECRANS
# ----------------------------------------------------------------------
class HomeScreen(Screen):
    pass


class SimpleCalcScreen(Screen):
    pass


class ScientificCalcScreen(Screen):
    pass


class AgeCalcScreen(Screen):
    pass


class DayCalcScreen(Screen):
    pass


class ConverterScreen(Screen):
    pass


class PercentageScreen(Screen):
    pass


class CycleCalcScreen(Screen):
    pass


# ----------------------------------------------------------------------
# LOGIQUE : Calculatrice simple
# ----------------------------------------------------------------------
class SimpleCalcLogic:
    def __init__(self, app):
        self.app = app
        self.expression = ""

    def _screen(self):
        return self.app.root.get_screen("simple")

    def press(self, char):
        self.expression += char
        self._screen().display.text = self.expression

    def backspace(self):
        self.expression = self.expression[:-1]
        self._screen().display.text = self.expression or "0"

    def clear(self):
        self.expression = ""
        self._screen().display.text = "0"

    def equals(self):
        try:
            allowed = "0123456789.+-*/%() "
            if any(c not in allowed for c in self.expression):
                raise ValueError
            result = eval(self.expression, {"__builtins__": {}})
            self.expression = str(result)
            self._screen().display.text = self.expression
        except Exception:
            self._screen().display.text = "Erreur"
            self.expression = ""


# ----------------------------------------------------------------------
# LOGIQUE : Calculatrice scientifique
# ----------------------------------------------------------------------
class ScientificCalcLogic:
    def __init__(self, app):
        self.app = app
        self.expression = ""

    def _screen(self):
        return self.app.root.get_screen("scientific")

    def press(self, char):
        self.expression += char
        self._screen().display.text = self.expression

    def clear(self):
        self.expression = ""
        self._screen().display.text = "0"

    def apply_function(self, func_name):
        try:
            value = float(self.expression) if self.expression else 0.0
            if func_name == "sin":
                result = math.sin(math.radians(value))
            elif func_name == "cos":
                result = math.cos(math.radians(value))
            elif func_name == "tan":
                result = math.tan(math.radians(value))
            elif func_name == "sqrt":
                result = math.sqrt(value)
            elif func_name == "log10":
                result = math.log10(value)
            elif func_name == "log":
                result = math.log(value)
            else:
                result = value
            self.expression = str(round(result, 6))
            self._screen().display.text = self.expression
        except Exception:
            self._screen().display.text = "Erreur"
            self.expression = ""

    def equals(self):
        try:
            allowed = "0123456789.+-*/() "
            if any(c not in allowed for c in self.expression):
                raise ValueError
            result = eval(self.expression, {"__builtins__": {}})
            self.expression = str(result)
            self._screen().display.text = self.expression
        except Exception:
            self._screen().display.text = "Erreur"
            self.expression = ""


# ----------------------------------------------------------------------
# LOGIQUE : Calcul d'âge
# ----------------------------------------------------------------------
class AgeCalcLogic:
    def __init__(self, app):
        self.app = app

    def compute(self):
        screen = self.app.root.get_screen("age")
        try:
            day = int(screen.day_input.text)
            month = int(screen.month_input.text)
            year = int(screen.year_input.text)
            birth_date = datetime(year, month, day)
            today = datetime.today()

            years = today.year - birth_date.year
            months = today.month - birth_date.month
            days = today.day - birth_date.day

            if days < 0:
                months -= 1
                prev_month = today.month - 1 or 12
                prev_year = today.year if today.month > 1 else today.year - 1
                days_in_prev_month = (datetime(prev_year, prev_month % 12 + 1, 1) - timedelta(days=1)).day
                days += days_in_prev_month
            if months < 0:
                years -= 1
                months += 12

            screen.result_label.text = (
                f"Tu as {years} ans, {months} mois et {days} jours."
            )
        except Exception:
            screen.result_label.text = "Date invalide."


# ----------------------------------------------------------------------
# LOGIQUE : Calcul de jours entre deux dates
# ----------------------------------------------------------------------
class DayCalcLogic:
    def __init__(self, app):
        self.app = app

    def compute(self):
        screen = self.app.root.get_screen("day")
        try:
            start = datetime.strptime(screen.start_input.text.strip(), "%d/%m/%Y")
            end = datetime.strptime(screen.end_input.text.strip(), "%d/%m/%Y")
            delta = abs((end - start).days)
            screen.result_label.text = f"Difference : {delta} jour(s)."
        except Exception:
            screen.result_label.text = "Format de date invalide (JJ/MM/AAAA)."


# ----------------------------------------------------------------------
# LOGIQUE : Convertisseur d'unites
# ----------------------------------------------------------------------
class ConverterLogic:
    UNITS = {
        "Longueur": {
            "m": 1.0, "km": 1000.0, "cm": 0.01, "mile": 1609.344,
        },
        "Poids": {
            "kg": 1.0, "g": 0.001, "lb": 0.453592,
        },
        "Temperature": None,  # cas special
    }

    def __init__(self, app):
        self.app = app

    def _screen(self):
        return self.app.root.get_screen("convert")

    def on_category_change(self):
        screen = self._screen()
        category = screen.category_spinner.text
        if category == "Temperature":
            values = ["C", "F", "K"]
        else:
            values = list(self.UNITS[category].keys())
        screen.from_spinner.values = values
        screen.to_spinner.values = values
        screen.from_spinner.text = values[0]
        screen.to_spinner.text = values[1]

    def compute(self):
        screen = self._screen()
        try:
            value = float(screen.value_input.text)
            category = screen.category_spinner.text
            unit_from = screen.from_spinner.text
            unit_to = screen.to_spinner.text

            if category == "Temperature":
                result = self._convert_temperature(value, unit_from, unit_to)
            else:
                factors = self.UNITS[category]
                base_value = value * factors[unit_from]
                result = base_value / factors[unit_to]

            screen.result_label.text = f"{value} {unit_from} = {result:.4f} {unit_to}"
        except Exception:
            screen.result_label.text = "Valeur invalide."

    def _convert_temperature(self, value, unit_from, unit_to):
        # Conversion via Celsius comme pivot
        if unit_from == "C":
            celsius = value
        elif unit_from == "F":
            celsius = (value - 32) * 5 / 9
        else:  # K
            celsius = value - 273.15

        if unit_to == "C":
            return celsius
        elif unit_to == "F":
            return celsius * 9 / 5 + 32
        else:  # K
            return celsius + 273.15


# ----------------------------------------------------------------------
# LOGIQUE : Pourcentage
# ----------------------------------------------------------------------
class PercentageLogic:
    def __init__(self, app):
        self.app = app

    def compute(self, mode):
        screen = self.app.root.get_screen("percent")
        try:
            value = float(screen.value_input.text)
            percent = float(screen.percent_input.text)

            if mode == "of":
                result = value * percent / 100
                screen.result_label.text = f"{percent}% de {value} = {result:.2f}"
            elif mode == "increase":
                result = value * (1 + percent / 100)
                screen.result_label.text = (
                    f"{value} augmente de {percent}% = {result:.2f}"
                )
            else:  # decrease
                result = value * (1 - percent / 100)
                screen.result_label.text = (
                    f"{value} diminue de {percent}% = {result:.2f}"
                )
        except Exception:
            screen.result_label.text = "Valeurs invalides."


# ----------------------------------------------------------------------
# LOGIQUE : IntimeGirls (cycle menstruel)
# ----------------------------------------------------------------------
class CycleCalcLogic:
    def __init__(self, app):
        self.app = app

    def compute(self):
        screen = self.app.root.get_screen("cycle")
        try:
            day = int(screen.day_input.text)
            month = int(screen.month_input.text)
            year = int(screen.year_input.text)
            cycle_length = int(screen.length_input.text)

            last_period = datetime(year, month, day)
            next_period = last_period + timedelta(days=cycle_length)
            ovulation = next_period - timedelta(days=14)
            fertile_start = ovulation - timedelta(days=5)
            fertile_end = ovulation + timedelta(days=1)

            screen.result_label.text = (
                f"Prochaines regles estimees : {next_period.strftime('%d/%m/%Y')}\n"
                f"Ovulation estimee : {ovulation.strftime('%d/%m/%Y')}\n"
                f"Periode fertile : du {fertile_start.strftime('%d/%m/%Y')} "
                f"au {fertile_end.strftime('%d/%m/%Y')}"
            )
        except Exception:
            screen.result_label.text = "Donnees invalides."


# ----------------------------------------------------------------------
# APPLICATION PRINCIPALE
# ----------------------------------------------------------------------
class SmartCalcApp(App):
    def build(self):
        self.title = "SmartCalc By Florin Pro"
        root = Builder.load_string(KV)

        self.simple_calc = SimpleCalcLogic(self)
        self.sci_calc = ScientificCalcLogic(self)
        self.age_calc = AgeCalcLogic(self)
        self.day_calc = DayCalcLogic(self)
        self.converter = ConverterLogic(self)
        self.percentage = PercentageLogic(self)
        self.cycle_calc = CycleCalcLogic(self)

        return root


if __name__ == "__main__":
    SmartCalcApp().run()
