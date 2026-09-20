# Privacy Policy — GNSS Filter

Last updated: 20 September 2026

*Українська версія — нижче / Ukrainian version below.*

## What the app does

GNSS Filter verifies the GPS position on the user's device (cross-checks it
against the network, motion and heading) and, when the real signal is spoofed
or jammed, provides the navigator with a computed position instead of the
fake GPS one. All processing happens **exclusively on the user's device**.

## What data is used and why

| Data | Purpose | Where it goes |
|---|---|---|
| Precise location (GPS) | Core function — verifying and filtering the position | On the device only; never transmitted |
| Network data (cell towers, Wi-Fi, via the system Network Location Provider) | Independent cross-check of GPS | On the device only |
| Bluetooth (connection to the vehicle's OBD adapter) | Independent evidence of speed from the wheels | On the device only, directly from the adapter in the vehicle |
| Accelerometer, gyroscope, barometer (phone sensors) | Motion detection, heading, altitude | On the device only |
| Internet access | Only downloading ephemeris (satellite orbits) from the open IGS scientific archives: `igs.bkg.bund.de`, `igs.ign.fr` | The app sends nothing; it is a plain HTTPS file request, identical for everyone. As with any request to a web server, the server sees the device's IP address |
| Local logs (`Android/data/com.gnssfilter/files/logs/`, 14 days) | Diagnostics and field testing | On the device only; the app never sends them anywhere by itself. The user may manually export or share a log file at their own discretion |

The app **does not collect, transmit or sell** any data to third parties.
No analytics, no advertising SDKs, no trackers.

## Permissions

- **Precise/approximate location** — core function.
- **Bluetooth** — connection to an OBD adapter (optional, enabled by the user).
- **Foreground service + notifications** — so the app keeps working and its
  active status stays visible while the screen is off or other apps are open.
- **Internet** (INTERNET, ACCESS_NETWORK_STATE) — only for downloading
  ephemeris from the open IGS archives. No coordinates, identifiers or any
  other user data are included in these requests.
- **Display over other apps** (SYSTEM_ALERT_WINDOW) — an optional coloured
  status dot over the screen; turned on/off by the user.
- **Mock location** (ACCESS_MOCK_LOCATION) — technically required so the app
  can provide the verified position to other apps (navigators) through the
  system test location provider when the real GPS is not trusted.

## Purchases

The full version is unlocked by a one-time purchase through **Google Play
Billing**. The payment and payment data are processed by Google Play — the
app only receives confirmation of the purchase and never sees or stores any
payment details. Use of Google Play Billing is governed by Google's own
privacy policy: https://policies.google.com/privacy

## Accounts

The app does not require registration or signing in to any account for its
core function.

## Data storage

All settings, the trial counter and the purchase status are stored **locally
on the device** (SharedPreferences). Uninstalling the app removes this data
from the device; the purchase status is not lost, because Google Play keeps
it separately, tied to the device's Google account.

## Changes to this policy

Material changes to this policy will be announced by updating this document
with a new date at the top.

## Contact

[leeall7+gnssconf@gmail.com: contact e-mail address for privacy questions]

---

# Політика конфіденційності — GNSS Filter (українською)

Востаннє оновлено: 20.09.2026

## Що робить застосунок

GNSS Filter перевіряє позицію GPS на пристрої користувача (звіряє з мережею,
рухом, курсом) і, коли справжній сигнал підмінений або придушений, видає
навігатору розраховану позицію замість підробленого GPS. Уся обробка
відбувається **виключно на пристрої користувача**.

## Які дані використовуються і чому

| Дані | Навіщо | Куди йдуть |
|---|---|---|
| Точна геолокація (GPS) | Основна функція — перевірка й фільтрація позиції | Лише на пристрої; нікуди не передається |
| Дані мережі (вишки, Wi-Fi, через системний Network Location Provider) | Незалежна звірка з GPS | Лише на пристрої |
| Bluetooth (підключення до OBD-адаптера авто) | Незалежний доказ швидкості руху з коліс | Лише на пристрої, напряму з адаптера в авто |
| Акселерометр, гіроскоп, барометр (сенсори телефону) | Детектор руху, курс, висота | Лише на пристрої |
| Доступ до інтернету | Лише завантаження ефемерид (орбіт супутників) з відкритих наукових архівів IGS: `igs.bkg.bund.de`, `igs.ign.fr` | Застосунок нічого не надсилає; це звичайний HTTPS-запит на файл, однаковий для всіх. Як і за будь-якого звернення до вебсервера, сервер бачить IP-адресу пристрою |
| Локальні логи (`Android/data/com.gnssfilter/files/logs/`, 14 діб) | Діагностика й польові випробування | Лише на пристрої; застосунок сам їх нікуди не надсилає. Користувач може вручну експортувати чи поділитись файлом логу на власний розсуд |

Застосунок **не збирає, не передає і не продає** жодні дані третім сторонам.
Немає аналітики, немає рекламних SDK, немає трекерів.

## Дозволи

- **Точна/приблизна локація** — основна функція.
- **Bluetooth** — підключення до OBD-адаптера (опційно, вмикається користувачем).
- **Foreground service + сповіщення** — щоб застосунок продовжував працювати
  й було видно його активний стан, поки екран вимкнено чи відкриті інші застосунки.
- **Інтернет** (INTERNET, ACCESS_NETWORK_STATE) — лише для завантаження
  ефемерид із відкритих архівів IGS. Координати, ідентифікатори чи будь-які
  інші дані користувача в цих запитах не передаються.
- **Показ поверх інших вікон** (SYSTEM_ALERT_WINDOW) — опційна кольорова
  крапка стану поверх екрана; вмикається/вимикається користувачем.
- **Мок-локація** (ACCESS_MOCK_LOCATION) — технічно необхідний дозвіл,
  щоб застосунок міг видавати перевірену позицію іншим застосункам
  (навігаторам) через системний тестовий провайдер локації, коли справжній
  GPS не в довірі.

## Покупки

Повна версія розблоковується разовою покупкою через **Google Play Billing**.
Сам платіж і платіжні дані обробляє Google Play — застосунок отримує лише
підтвердження факту покупки, не бачить і не зберігає жодних платіжних
реквізитів. Використання Google Play Billing регулюється власною політикою
конфіденційності Google: https://policies.google.com/privacy

## Акаунти

Застосунок не вимагає реєстрації чи входу в будь-який акаунт для роботи
основної функції.

## Зберігання даних

Усі налаштування, лічильник пробного ліміту й статус покупки зберігаються
**локально на пристрої** (SharedPreferences). Видалення застосунку видаляє
ці дані з пристрою; статус покупки при цьому не втрачається, оскільки його
окремо зберігає сам Google Play, прив'язано до Google-акаунту пристрою.

## Зміни цієї політики

Про суттєві зміни цієї політики буде повідомлено оновленням цього документа
з новою датою вгорі.

## Контакти

[leeall7+gnssconf@gmail.com: контактна електронна адреса для питань щодо конфіденційності]
