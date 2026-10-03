# Політика конфіденційності — GNSS Nav для iPhone

Чинна з 2 жовтня 2026 року. Розробник: ФОП Лі Олександр, Україна. Контакт: gnssfilter@gmail.com.

**Коротко.** GNSS Nav — навігатор, стійкий до глушіння й підміни GPS. Усе обчислюється на вашому
iPhone. Застосунок не має реєстрації, реклами й аналітики, не передає ваші поїздки розробникові чи
третім сторонам і нічого не збирає про вас.

## Які дані застосунок використовує і де вони лишаються

| Дані | Навіщо | Де зберігаються |
|---|---|---|
| **Геолокація** (GPS та мережеве визначення позиції iOS), зокрема у фоні під час поїздки | перевірка GPS, числення, ведення маршрутом | лише на телефоні |
| **Датчики руху** (гіроскоп, акселерометр, компас, активність) | числення, курс, виявлення руху | лише на телефоні |
| **OBD-адаптер через Bluetooth** (швидкість коліс, передача, VIN авто) | числення, калібрування для вашого авто | лише на телефоні; VIN — ключ до збережених калібрувань |
| **Офлайн-вміст** (мапи, маршрути, пошук) | робота без інтернету | завантажується з публічного репозиторію GitHub на телефон |
| **Покупка** повної версії | разова покупка через Apple | обробляє Apple (App Store); розробник не отримує платіжних даних |
| **Пробний період** (лічильник кілометрів без GPS) | обмеження пробної версії | на телефоні (Keychain), не синхронізується |
| **Улюблені й нещодавні місця**, налаштування | зручність | лише на телефоні |

## Логи

Під час поїздки застосунок веде технічні логи (CSV): позиції, час, вердикти, дані OBD (зокрема VIN і назву
адаптера), датчики. Вони **зберігаються лише на телефоні** 14 днів, а потім видаляються самі. Їх можна
видалити будь-коли: «Деталі → Очистити логи».

Логи передаються розробникові **лише якщо ви самі натиснете «Надіслати логи»** і виберете, куди їх
надіслати. Перед надсиланням архів шифрується публічним ключем розробника (AES-256-GCM, RSA-OAEP):
прочитати його може лише розробник. Якщо шифрування не вдалося, застосунок попереджає, і архів
звичайний.

## Що йде через інтернет

- **Завантаження офлайн-вмісту** з GitHub (releases репозиторію `gnss-filter-public`): GitHub бачить вашу
  IP-адресу, як будь-який сайт. Розробник доступу до цих запитів не має.
- **Покупка** — через Apple.
- **Мережеве визначення позиції** — стандартна служба iOS (Apple).
- **Онлайн-режим** (типово увімкнений, вимикається в «Деталях»): мапа, затори, маршрути й пошук — від Apple
  (MapKit). Щоб показати мапу й побудувати маршрут, iOS надсилає Apple ділянку мапи, старт і пункт призначення, запит
  пошуку — так само, як застосунок «Мапи». Обробляє це Apple за власною політикою конфіденційності; розробник цих
  запитів не бачить. Без інтернету (або з вимкненим онлайн-режимом) — офлайн-мапа й маршрути, нічого не передається.

Більше нічого застосунок у мережу не надсилає. Мапи, маршрути й пошук працюють офлайн.

## Дозволи iOS

Геолокація (під час використання; у фоні — для ведення під час поїздки, із системним індикатором),
Bluetooth (OBD-адаптер), рух і фітнес (датчики). Усі дозволи можна відкликати в Параметрах; без них
відповідні функції не працюють.

## Діти

Застосунок не призначений для дітей до 13 років і не збирає їхніх даних.

## Видалення даних

Усі дані лежать на телефоні: видаліть застосунок — зникне все, крім лічильника пробного періоду в
Keychain (він видаляється разом з резервною копією пристрою) і запису про покупку в Apple.

## Зміни

Нова редакція публікується за цією ж адресою з новою датою.

---

# Privacy Policy — GNSS Nav for iPhone

Effective 2 October 2026. Developer: Oleksandr Li (private entrepreneur), Ukraine. Contact: gnssfilter@gmail.com.

**In short.** GNSS Nav is a car navigator that keeps working when GPS is jammed or spoofed. Everything is
computed on your iPhone. There is no account, no ads, no analytics; your trips are never sent to the
developer or to third parties; the app collects nothing about you.

**Data the app uses, and where it stays:** location (GPS and iOS network positioning, also in the
background during a drive), motion sensors, data from an optional OBD-II Bluetooth adapter (wheel speed,
gear, vehicle VIN used as a key for saved calibration), offline content downloaded from a public GitHub
repository, the one-time purchase handled by Apple, the trial-distance counter (Keychain), favourites and
settings. All of it stays on the device.

**Logs.** During a drive the app writes technical CSV logs (positions, time, verdicts, OBD data including
VIN and adapter name, sensors). They stay on the device for 14 days and are then deleted; you can delete
them any time (Details → Clear logs). Logs leave the device only when you tap "Send logs" and choose a
destination; the archive is encrypted with the developer's public key (AES-256-GCM, RSA-OAEP) so only the
developer can read it. If encryption fails, the app warns you and the archive is plain.

**Network use.** Offline content is downloaded from GitHub releases (GitHub sees your IP address like any
website; the developer has no access to those requests). Purchases go through Apple. Network positioning
is a standard iOS service. **Online mode** (on by default, can be turned off): map, traffic,
routes and search come from Apple (MapKit); to show the map and compute a route iOS sends Apple the map area, start,
destination and search query, as the Maps app does — processed by Apple under its privacy policy; the developer does
not see these requests. Offline mode sends nothing. Nothing else is sent; maps, routing and search work offline.

**Permissions:** Location (while in use; in the background during a drive, with the system indicator),
Bluetooth (OBD adapter), Motion & Fitness. You can revoke them in Settings.

**Children:** not intended for children under 13; no data about them is collected.

**Deletion:** delete the app and everything is gone, except the trial counter in Keychain (removed with
the device backup) and the purchase record at Apple.

**Changes:** a new version is published at this address with a new date.
