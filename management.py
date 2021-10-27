# This Python file uses the following encoding: utf-8
"""Модуль для управления настройками."""
import os
import socket


# Считываем настройки
# Локальные имеют приоритет над глобальными
def get_settings(*options) -> list:
    """Получить настройки из файлов конфигурации."""
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

        result = []
        for option in options:
            if settings[option].isdigit():
                result.append(int(settings[option]))
            else:
                result.append(settings[option])
        return result


def get_ip_address():
    """Получить ИП-адрес."""
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP almost always uses SOCK_STREAM
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
