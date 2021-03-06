from core import settingsloader
from core import cache_handler
import os


if __name__ == "__main__":
    x = input("Clear and refresh settings.ini (y/[any])? ")
    if x.lower() in ['y', 'yes']:
        # clear current settings
        os.remove("settings.ini")
        settings = settingsloader.load_settings()

    x = input("Clear and refresh cache_data.pkl (y/[any])? ")
    if x.lower() in ['y', 'yes']:
        data = cache_handler.generate_new_caches({})
        cache_handler.save_data(data)
