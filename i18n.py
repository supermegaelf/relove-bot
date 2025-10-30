import json
from pathlib import Path

LOCALES_DIR = Path(__file__).parent / "locales"

class I18n:
    def __init__(self):
        self.locales = {}
        self.load_locales()
    
    def load_locales(self):
        for locale_file in LOCALES_DIR.glob("*.json"):
            locale_code = locale_file.stem
            with open(locale_file, 'r', encoding='utf-8') as f:
                self.locales[locale_code] = json.load(f)
    
    def get(self, key: str, locale: str = "ru") -> str:
        value = self.locales.get(locale, self.locales["ru"]).get(key, key)
        if isinstance(value, list):
            return "\n\n".join(value)
        return value
    
    def has_locale(self, locale: str) -> bool:
        return locale in self.locales

i18n = I18n()

def get_text(key: str, locale: str = "ru") -> str:
    return i18n.get(key, locale)

