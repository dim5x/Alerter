import os

# Считываем настройки
# Локальные имеют приоритет над глобальными
def get_settings(options):
    
    settings = {}

    if os.path.exists('local.config'):
        with open('local.config') as file:
            lines = file.read().splitlines()
            for line in lines:
                key, value = line.split(':')
                settings.update({key: value})

    with open('global.config') as file:
        lines = file.read().splitlines()
        for line in lines:
            key, value = line.split(':')
            if key not in settings:
                settings.update({key: value})

    if isinstance(options, str):
        return settings[options]
    elif isinstance(options, list):
        result =[]
        for option in options:
            if settings[option].isdigit():
                result.append(int(settings[option]))
            else:
                result.append(settings[option])
        return result
