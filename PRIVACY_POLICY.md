# Privacy Policy — GNSS Filter

Last updated: 27 September 2026

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
| Internet access | Downloading ephemeris (satellite orbits) from the open IGS scientific archives: `igs.bkg.bund.de`, `igs.ign.fr`; a short time check at app start (the same servers; only the time from the HTTPS response header is used); map tiles (see below); Google Play services for the purchase and Block Store (see below) | For ephemeris and the time check the app sends nothing; it is a plain HTTPS file request, identical for everyone. As with any request to a web server, the server sees the device's IP address |
| Local logs (`Android/data/com.gnssfilter/files/logs/`, 14 days) | Diagnostics and field testing | On the device only; the app never sends them anywhere by itself. The user may manually export or share a log file at their own discretion |
| Map tiles (OpenStreetMap) — only when you open the "Adjust car position on the map" screen. The Google Play version does not use satellite imagery | Letting you place the car and its heading on a map by hand | The tile servers receive requests for the map tiles you are viewing, as with any online map. The screen opens centred on the car, so these requests reveal the approximate area you are in (roughly a few hundred metres) to the tile provider (OpenStreetMap Foundation; in test builds distributed outside Google Play with the satellite layer enabled, also Esri). No trip, identifier or exact coordinates are sent; tiles are cached in the app's cache folder |
| Cell-tower records (`…/files/cells/`, up to 20 MB): identifiers and signal of the serving and neighbouring cells, the network fix, the app's own position at that moment, and the **number** of visible Wi-Fi networks (no Wi-Fi identifiers) | On-device learning of tower positions and network-fix behaviour, to improve positioning without GPS | **On the device only. Never transmitted anywhere** — the Google Play version has no function to send them; the developer has no access to it |

The app **does not collect, transmit or sell** any data to third parties.
No analytics, no advertising SDKs, no trackers.

## Permissions

- **Precise/approximate location** — core function.
- **Bluetooth** — connection to an OBD adapter (optional, enabled by the user).
- **Foreground service + notifications** — so the app keeps working and its
  active status stays visible while the screen is off or other apps are open.
- **Internet** (INTERNET, ACCESS_NETWORK_STATE) — for downloading ephemeris
  from the open IGS archives, a short time check against the same servers at
  app start, and, while the map screen is open, map tiles;
  Google Play services use it for the purchase and Block Store. Ephemeris and
  time-check requests contain no coordinates, identifiers or any other user data; map
  tile requests reveal only the approximate area shown on the map.
- **Wi-Fi state** (ACCESS_WIFI_STATE) — only the number of visible Wi-Fi
  networks is used; network names and identifiers are neither used nor stored.
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

One value — the trial counter (a single number: kilometres of the free trial
already used) — is additionally kept in the Block Store of Google Play
services on the same device, so that the trial is not restarted by clearing
the app's data or reinstalling it. If Google backup is enabled on the device,
this number is included in the user's own encrypted Google backup. It
contains no location or identifiers, and the developer has no access to it.

The same storage also keeps the app's sensor calibrations — the normal
receiver gain level per frequency band, the vehicle speed-sensor correction
factors and the gyroscope zero offset — and the two distance totals shown on
the main screen (total distance driven with the app and distance without
satellite navigation), so they are not lost when the app is reinstalled.
These are a few numbers describing the phone, the car and the total mileage;
they contain no location, no trip history and no identifiers.

## Changes to this policy

Material changes to this policy will be announced by updating this document
with a new date at the top.

## Contact

gnssfilter@gmail.com

---

# Політика конфіденційності — GNSS Filter (українською)

Востаннє оновлено: 27.09.2026

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
| Доступ до інтернету | Завантаження ефемерид (орбіт супутників) з відкритих наукових архівів IGS: `igs.bkg.bund.de`, `igs.ign.fr`; коротка звірка часу на старті (ті самі сервери; береться лише час із заголовка HTTPS-відповіді); тайли карти (див. нижче); сервіси Google Play для покупки й Block Store (див. нижче) | Для ефемерид і звірки часу застосунок нічого не надсилає; це звичайний HTTPS-запит на файл, однаковий для всіх. Як і за будь-якого звернення до вебсервера, сервер бачить IP-адресу пристрою |
| Локальні логи (`Android/data/com.gnssfilter/files/logs/`, 14 діб) | Діагностика й польові випробування | Лише на пристрої; застосунок сам їх нікуди не надсилає. Користувач може вручну експортувати чи поділитись файлом логу на власний розсуд |
| Тайли карти (OpenStreetMap) — лише коли ви відкриваєте екран «Уточнити позицію авто на карті». Версія з Google Play супутникових знімків не використовує | Щоб поставити авто і його курс на карті вручну | Сервери карти отримують запити на фрагменти карти, які ви переглядаєте, як у будь-якій онлайн-карті. Екран відкривається з центром у позиції авто, тож ці запити розкривають постачальнику карти (OpenStreetMap Foundation; у тестових збірках поза Google Play з увімкненим супутниковим шаром — також Esri) приблизну місцевість, де ви є (порядку кількох сотень метрів). Трек, ідентифікатори чи точні координати не передаються; тайли кешуються в теці кешу застосунку |
| Записи про базові станції (`…/files/cells/`, до 20 МБ): ідентифікатори й сигнал обслуговуючої та сусідніх сот, мережевий фікс, власна позиція застосунку в цей момент і **кількість** видимих Wi-Fi-мереж (без ідентифікаторів Wi-Fi) | Навчання на пристрої: розташування вишок і поведінка мережевих фіксів, для кращого визначення позиції без GPS | **Лише на пристрої. Нікуди не передаються** — у версії з Google Play функції надсилання немає; розробник доступу до них не має |

Застосунок **не збирає, не передає і не продає** жодні дані третім сторонам.
Немає аналітики, немає рекламних SDK, немає трекерів.

## Дозволи

- **Точна/приблизна локація** — основна функція.
- **Bluetooth** — підключення до OBD-адаптера (опційно, вмикається користувачем).
- **Foreground service + сповіщення** — щоб застосунок продовжував працювати
  й було видно його активний стан, поки екран вимкнено чи відкриті інші застосунки.
- **Інтернет** (INTERNET, ACCESS_NETWORK_STATE) — для завантаження ефемерид
  із відкритих архівів IGS, короткої звірки часу з тими самими серверами на
  старті і, поки відкрито екран карти, тайлів карти; сервіси
  Google Play використовують його для покупки й Block Store. У запитах ефемерид
  і звірки часу немає координат, ідентифікаторів чи інших даних користувача; запити тайлів
  розкривають лише приблизну місцевість, показану на карті.
- **Стан Wi-Fi** (ACCESS_WIFI_STATE) — використовується лише кількість видимих
  Wi-Fi-мереж; назви й ідентифікатори мереж не використовуються і не зберігаються.
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

Одне значення — лічильник пробного періоду (одне число: скільки кілометрів
безкоштовного періоду вже використано) — додатково зберігається у сховищі
Block Store сервісів Google Play на тому самому пристрої, щоб пробний період
не починався заново після очищення даних застосунку чи перевстановлення. Якщо
на пристрої ввімкнене резервне копіювання Google, це число потрапляє до
власної зашифрованої резервної копії користувача. Воно не містить ні
місцезнаходження, ні ідентифікаторів, і розробник доступу до нього не має.

У тому самому сховищі зберігаються калібрування датчиків — нормальний рівень
підсилення приймача за смугами частот, поправки до швидкості з OBD і зсув
нуля гіроскопа, — а також два підсумки пробігу з головного екрана (усього з
застосунком і без супутникової навігації), щоб вони не губилися під час
перевстановлення. Це кілька чисел, що описують телефон, автомобіль і загальний
пробіг; вони не містять ні місцезнаходження, ні історії поїздок, ні
ідентифікаторів.

## Зміни цієї політики

Про суттєві зміни цієї політики буде повідомлено оновленням цього документа
з новою датою вгорі.

## Контакти

gnssfilter@gmail.com
