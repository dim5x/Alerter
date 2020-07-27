import os 

# Считываем настройки
# Локальные имеют приоритет над глобальными
def get_option(name):
    with open('local.config') as file:
        lines = file.read().splitlines()
    
    options  = {}

    for line in lines:
        key, value = line.split(':')
        options.update({key:value})

    with open ('global.config') as file:
        lines = file.read().splitlines()

    for line in lines:
        key, value = line.split(':')
        if not key in options:
            options.update({key:value})

    return options[name]
