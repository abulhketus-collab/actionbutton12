# ActionButton12 🔘

[![iOS](https://img.shields.io/badge/iOS-12.0%20--%2012.5.8-blue.svg)](https://apple.com)
[![Architecture](https://img.shields.io/badge/Arch-arm64-green.svg)](https://apple.com)
[![Author](https://img.shields.io/badge/Author-@cocxace-orange.svg)](https://github.com/abulhketus-collab)
[![Package](https://img.shields.io/badge/Package-com.cocxace.actionbutton12-purple.svg)](https://github.com/abulhketus-collab/actionbutton12)
[![Sileo](https://img.shields.io/badge/Sileo-Compatible-success.svg)](https://abulhketus-collab.github.io/actionbutton12/)

**ActionButton12** — полнофункциональный Theos-твик для **iOS 12 (12.0 — 12.5.8)**, переносящий опыт **Action Button** с iPhone 15 Pro на классические устройства Apple (оптимизировано для **iPhone 5s / A7 chip**, rootful джейлбрейк, Sileo).

Автор: **@cocxace**

---

## ✨ Возможности (Features)

- ⚡ **Быстрый HUD Action Button**: полупрозрачная матовая панель поверх SpringBoard с мягким размытием и скруглением (`cornerRadius 20`, фон `white: 0.1, alpha: 0.85`).
- 🔘 **Сетка 2x2 настраиваемых действий**:
  - 🔦 **Фонарик** (`AVCaptureDevice toggleTorch`)
  - 📷 **Камера** (`SBUIController launchApplicationWithIdentifier:@"com.apple.camera"`)
  - 🎙 **Диктофон** (`launchApplicationWithIdentifier:@"com.apple.VoiceMemos"`)
  - 📸 **Скриншот** (`notify_post("com.apple.springboard.takeScreenshot")`)
  - 📶 **Wi-Fi переключатель** (`SBWiFiManager`)
  - 📡 **Bluetooth переключатель** (`BluetoothManager`)
- 🎚 **Плавные интерактивные ползунки (Sliders)**:
  - Плавная регулировка яркости экрана (`UIScreen.mainScreen.brightness`) в реальном времени.
  - Плавная регулировка системной громкости (`AVSystemController.sharedAVSystemController`).
  - Минималистичный стиль ползунков с динамической подсветкой и иконками.
- 📳 **Тактильный и звуковой отклик**:
  - `AudioServicesPlaySystemSound(1519)` при вызове и взаимодействии (актуально для устройств без Taptic Engine).
- ⚙️ **Встроенные настройки в Settings.app (PreferenceBundle)**:
  - Включение / выключение твика.
  - Выбор триггера: Долгое нажатие Power (0.6 сек) / Двойное нажатие Home / Оба одновременно.
  - Настройка каждого из 4 слотов сетки на любое действие.
  - Включение / выключение панели ползунков.
  - Быстрый респринг (`sbreload` / `killall -9 SpringBoard`).
  - Подпись: *"ActionButton12 by @cocxace"*.

---

## 📲 Установка (Installation)

### Способ 1: Через Sileo / Zebra / Cydia (Репозиторий APT)
1. Добавьте в Sileo источник:
   ```text
   https://abulhketus-collab.github.io/actionbutton12/
   ```
   *Или откройте в Safari на iPhone:* [Открыть в Sileo](sileo://source/https://abulhketus-collab.github.io/actionbutton12/)
2. Найдите в поиске **ActionButton12**.
3. Нажмите **Установить** и выполните респринг.

### Способ 2: Установка готового .deb файла вручную
1. Скачайте готовый пакет из папки `debs/`:
   [debs/com.cocxace.actionbutton12_1.0.0_iphoneos-arm.deb](debs/com.cocxace.actionbutton12_1.0.0_iphoneos-arm.deb)
2. Откройте в **Filza File Manager** на iPhone и нажмите **Установить**.
3. Или установите через терминал/SSH:
   ```bash
   dpkg -i com.cocxace.actionbutton12_1.0.0_iphoneos-arm.deb
   killall -9 SpringBoard
   ```

---

## 📁 Структура проекта (Repository Structure)

```text
├── Tweak.xm                  # Logos-хуки SpringBoard, Power button & Home double tap
├── Tweak.m                   # Сгенерированный Objective-C код хуков Substrate
├── AB12Common.h              # Константы, енамы действий и пути настроек
├── AB12HUDView.h / .m        # UIWindow, анимации scale/alpha, сетка 2x2 и ползунки
├── AB12Manager.h / .m        # Менеджер фонарика, камеры, звука, скриншотов, Wi-Fi и BT
├── ActionButton12.plist      # Фильтр бандлов (com.apple.springboard)
├── Makefile                  # Конфигурация Theos (ARCHS = arm64, target iOS 12)
├── control                   # Метаданные Debian-пакета (Author: cocxace)
├── Resources/                # Векторные и растровые PNG иконки действий и ползунков
├── actionbutton12prefs/      # PreferenceBundle для Настроек iOS (PSListController)
│   ├── AB12RootListController.h / .m
│   └── Resources/Root.plist & Info.plist
├── debs/                     # Готовый .deb релиз для Cydia/Sileo
├── Packages & Release        # Индексы APT-репозитория
└── index.html                # Веб-страница репозитория для Safari/Sileo
```

---

## 🛠 Сборка из исходников (Building)

### Требования:
- Theos или кросс-компилятор Clang для iOS (LLVM Clang 14+ / 20)
- iOS 12.0 — 12.4 SDK (`iPhoneOS12.4.sdk`)
- Архитектура: `arm64` (A7 64-bit Mach-O)

### Сборка через Theos:
```bash
make clean
make package FINALPACKAGE=1
```

Готовый пакет будет создан в папке `packages/` (и `debs/`).

---

## 👤 Автор (Credits)

- Создатель и разработчик: **@cocxace**
- GitHub: [abulhketus-collab](https://github.com/abulhketus-collab)
