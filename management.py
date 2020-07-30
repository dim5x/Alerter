# import os


# Считываем настройки
# Локальные имеют приоритет над глобальными
def get_option(name):
    options = {}

    with open('../local.config') as file:
        lines = file.read().splitlines()
        for line in lines:
            key, value = line.split(':')
            options.update({key: value})

    with open('global.config') as file:
        lines = file.read().splitlines()
        for line in lines:
            key, value = line.split(':')
            if key not in options:
                options.update({key: value})

    return options[name]

def get_alerter_settings():
    return get_option('alerter_host'), int(get_option('alerter_port'))