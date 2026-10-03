# Privacy Policy — GNSS Filter

Last updated: 3 October 2026

*Українська версія — нижче / Ukrainian version below. · [גרסה בעברית — למטה](#מדיניות-פרטיות--gnss-filter-בעברית).*

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
| Vehicle identification number (VIN), read from the car through the OBD adapter; if the car does not report it, the adapter's Bluetooth address is used instead | Keeping the speed calibration separately for each car (the real speed always differs from the speedometer) | On the device only: in the app settings and in the local logs. Not stored in Block Store and never transmitted by the app; it leaves the device only if you share a log yourself |
| Accelerometer, gyroscope, barometer (phone sensors) | Motion detection, heading, altitude | On the device only |
| Internet access | Downloading ephemeris (satellite orbits) from the open IGS scientific archives: `igs.bkg.bund.de`, `igs.ign.fr`; a short time check against the same servers at app start, when the network reconnects and every few hours while running (only the time from the HTTPS response header is used); map tiles (see below); the optional roads map for snapping — a single file from the project's public repository on GitHub (`github.com`, `objects.githubusercontent.com`), downloaded only when the user requests it in the advanced menu; Google Play services for the purchase and Block Store (see below) | For ephemeris and the time check the app sends nothing; it is a plain HTTPS file request, identical for everyone. As with any request to a web server, the server sees the device's IP address |
| Local logs (`Android/data/com.gnssfilter/files/logs/`, 14 days): positions and movements, signal measurements, the vehicle's VIN | Diagnostics and field testing | On the device only; the app never sends them anywhere by itself. The user may manually export or share a log file at their own discretion; the exported archive is encrypted with the developer's public key, so only the developer can read it |
| Map tiles (OpenStreetMap) — only when you open the "Adjust car position on the map" screen. The Google Play version does not use satellite imagery | Letting you place the car and its heading on a map by hand | The tile servers receive requests for the map tiles you are viewing, as with any online map. The screen opens centred on the car, so these requests reveal the approximate area you are in (roughly a few hundred metres) to the tile provider (OpenStreetMap Foundation; in test builds distributed outside Google Play with the satellite layer enabled, also Esri). No trip, identifier or exact coordinates are sent; tiles you have viewed are kept in the app's private storage (up to 300 MB) so the map also works without internet; without internet the screen draws roads from the road network file already on the phone |
| Roads map (`…/files/roads/`, up to ~130 MB): road geometry from OpenStreetMap, no user data | Snapping the position to known roads (optional, advanced menu) | On the device only; downloaded from the project's public GitHub repository or copied manually |

The app **does not collect, transmit or sell** any data to third parties.
No analytics, no advertising SDKs, no trackers.

## Permissions

- **Precise/approximate location** — core function.
- **Bluetooth** — connection to an OBD adapter (optional, enabled by the user).
- **Foreground service + notifications** — so the app keeps working and its
  active status stays visible while the screen is off or other apps are open.
- **Internet** (INTERNET, ACCESS_NETWORK_STATE) — for downloading ephemeris
  from the open IGS archives, a short time check against the same servers (at
  app start, when the network reconnects and every few hours while running), and,
  while the map screen is open, map tiles, and — only on the user's request in
  the advanced menu — the roads map file from the project's public GitHub
  repository;
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

Востаннє оновлено: 03.10.2026

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
| Ідентифікаційний номер авто (VIN), зчитаний через OBD-адаптер; якщо авто його не повідомляє — замість нього адреса Bluetooth адаптера | Щоб калібрування швидкості зберігалось окремо для кожного авто (реальна швидкість завжди відрізняється від спідометра) | Лише на пристрої: у налаштуваннях застосунку й у локальних логах. У Block Store не зберігається, застосунок його нікуди не передає; з пристрою він потрапляє лише тоді, коли ви самі надсилаєте лог |
| Акселерометр, гіроскоп, барометр (сенсори телефону) | Детектор руху, курс, висота | Лише на пристрої |
| Доступ до інтернету | Завантаження ефемерид (орбіт супутників) з відкритих наукових архівів IGS: `igs.bkg.bund.de`, `igs.ign.fr`; коротка звірка часу з тими самими серверами на старті, при появі мережі й раз на кілька годин під час роботи (береться лише час із заголовка HTTPS-відповіді); тайли карти (див. нижче); необов'язкова карта доріг для прив'язки — один файл з публічного репозиторію проєкту на GitHub (`github.com`, `objects.githubusercontent.com`), лише на запит користувача в меню для досвідчених; сервіси Google Play для покупки й Block Store (див. нижче) | Для ефемерид і звірки часу застосунок нічого не надсилає; це звичайний HTTPS-запит на файл, однаковий для всіх. Як і за будь-якого звернення до вебсервера, сервер бачить IP-адресу пристрою |
| Локальні логи (`Android/data/com.gnssfilter/files/logs/`, 14 діб): позиції й переміщення, виміри сигналу, VIN авто | Діагностика й польові випробування | Лише на пристрої; застосунок сам їх нікуди не надсилає. Користувач може вручну експортувати чи поділитись файлом логу на власний розсуд; вивантажений архів шифрується публічним ключем розробника — прочитати його може лише розробник |
| Тайли карти (OpenStreetMap) — лише коли ви відкриваєте екран «Уточнити позицію авто на карті». Версія з Google Play супутникових знімків не використовує | Щоб поставити авто і його курс на карті вручну | Сервери карти отримують запити на фрагменти карти, які ви переглядаєте, як у будь-якій онлайн-карті. Екран відкривається з центром у позиції авто, тож ці запити розкривають постачальнику карти (OpenStreetMap Foundation; у тестових збірках поза Google Play з увімкненим супутниковим шаром — також Esri) приблизну місцевість, де ви є (порядку кількох сотень метрів). Трек, ідентифікатори чи точні координати не передаються; переглянуті тайли зберігаються в закритій теці застосунку (до 300 МБ), щоб карта працювала й без інтернету; без інтернету екран малює дороги зі схеми доріг, яка вже є на телефоні |
| Карта доріг (`…/files/roads/`, до ~130 МБ): геометрія доріг з OpenStreetMap, без даних користувача | Прив'язка позиції до відомих доріг (необов'язково, меню для досвідчених) | Лише на пристрої; завантажується з публічного репозиторію проєкту на GitHub або копіюється вручну |

Застосунок **не збирає, не передає і не продає** жодні дані третім сторонам.
Немає аналітики, немає рекламних SDK, немає трекерів.

## Дозволи

- **Точна/приблизна локація** — основна функція.
- **Bluetooth** — підключення до OBD-адаптера (опційно, вмикається користувачем).
- **Foreground service + сповіщення** — щоб застосунок продовжував працювати
  й було видно його активний стан, поки екран вимкнено чи відкриті інші застосунки.
- **Інтернет** (INTERNET, ACCESS_NETWORK_STATE) — для завантаження ефемерид
  із відкритих архівів IGS, короткої звірки часу з тими самими серверами (на
  старті, при появі мережі й раз на кілька годин під час роботи) і, поки відкрито
  екран карти, тайлів карти, і — лише на запит користувача в меню для
  досвідчених — файлу карти доріг з публічного репозиторію проєкту на GitHub;
  сервіси
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

---

# מדיניות פרטיות — GNSS Filter (בעברית)

עודכן לאחרונה: 3 באוקטובר 2026

*תרגום מהנוסח האנגלי שלמעלה. התרגום אינו של דובר שפת אם; במקרה של אי-התאמה —
הנוסח האנגלי קובע.*

## מה האפליקציה עושה

GNSS Filter מאמתת את מיקום ה-GPS במכשיר של המשתמש (משווה אותו לרשת, לתנועה
ולכיוון) וכאשר האות האמיתי מזויף או משובש, מספקת לאפליקציית הניווט מיקום
מחושב במקום מיקום ה-GPS הכוזב. כל העיבוד מתבצע **אך ורק במכשיר של המשתמש**.

## אילו נתונים משמשים ולמה

| נתונים | מטרה | לאן הם מגיעים |
|---|---|---|
| מיקום מדויק (GPS) | הפונקציה העיקרית — אימות וסינון המיקום | במכשיר בלבד; אינו מועבר לעולם |
| נתוני רשת (אנטנות סלולריות, Wi-Fi, דרך ספק מיקום הרשת של המערכת) | בדיקה בלתי תלויה של ה-GPS | במכשיר בלבד |
| Bluetooth (חיבור למתאם ה-OBD של הרכב) | ראיה בלתי תלויה למהירות מהגלגלים | במכשיר בלבד, ישירות מהמתאם שברכב |
| מספר זיהוי הרכב (VIN), הנקרא מהרכב דרך מתאם ה-OBD; אם הרכב אינו מדווח אותו, משמשת במקומו כתובת ה-Bluetooth של המתאם | שמירת כיול המהירות בנפרד לכל רכב (המהירות האמיתית תמיד שונה ממד המהירות) | במכשיר בלבד: בהגדרות האפליקציה וביומנים המקומיים. אינו נשמר ב-Block Store ואינו מועבר לעולם על ידי האפליקציה; הוא יוצא מהמכשיר רק אם אתם משתפים יומן בעצמכם |
| מד תאוצה, ג'ירוסקופ, ברומטר (חיישני הטלפון) | זיהוי תנועה, כיוון, גובה | במכשיר בלבד |
| גישה לאינטרנט | הורדת אפמריס (מסלולי לוויינים) מהארכיונים המדעיים הפתוחים של IGS: ‏`igs.bkg.bund.de`, ‏`igs.ign.fr`; בדיקת שעה קצרה מול אותם שרתים בהפעלת האפליקציה, כשהרשת מתחברת מחדש ומדי כמה שעות בזמן הפעולה (נעשה שימוש רק בשעה מכותרת תגובת ה-HTTPS); אריחי מפה (ראו למטה); מפת הכבישים האופציונלית להצמדה — קובץ יחיד מהמאגר הציבורי של הפרויקט ב-GitHub ‏(`github.com`, ‏`objects.githubusercontent.com`), שיורד רק כשהמשתמש מבקש זאת בתפריט המתקדם; שירותי Google Play לרכישה ול-Block Store (ראו למטה) | עבור האפמריס ובדיקת השעה האפליקציה אינה שולחת דבר; זו בקשת קובץ HTTPS פשוטה, זהה לכולם. כמו בכל בקשה לשרת אינטרנט, השרת רואה את כתובת ה-IP של המכשיר |
| יומנים מקומיים (`Android/data/com.gnssfilter/files/logs/`, ‏14 יום): מיקומים ותנועות, מדידות אות, ה-VIN של הרכב | אבחון ובדיקות שטח | במכשיר בלבד; האפליקציה אף פעם לא שולחת אותם בעצמה. המשתמש רשאי לייצא או לשתף קובץ יומן ידנית לפי שיקול דעתו; הארכיון המיוצא מוצפן במפתח הציבורי של המפתח, כך שרק המפתח יכול לקרוא אותו |
| אריחי מפה (OpenStreetMap) — רק כשאתם פותחים את מסך "כוונון מיקום הרכב על המפה". הגרסה ב-Google Play אינה משתמשת בצילומי לוויין | מאפשר למקם את הרכב ואת כיוונו על המפה ידנית | שרתי האריחים מקבלים בקשות לאריחים שאתם צופים בהם, כמו בכל מפה מקוונת. המסך נפתח כשמרכזו ברכב, ולכן הבקשות חושפות את האזור המשוער שבו אתם נמצאים (בערך כמה מאות מטרים) לספק האריחים (OpenStreetMap Foundation; בגרסאות בדיקה המופצות מחוץ ל-Google Play עם שכבת הלוויין מופעלת — גם Esri). שום נסיעה, מזהה או קואורדינטות מדויקות אינם נשלחים; אריחים שצפיתם בהם נשמרים באחסון הפרטי של האפליקציה (עד 300 MB) כדי שהמפה תעבוד גם ללא אינטרנט; ללא אינטרנט המסך מצייר כבישים ממפת הכבישים שכבר נמצאת בטלפון |
| מפת כבישים (`…/files/roads/`, עד כ-130 MB): גאומטריית כבישים מ-OpenStreetMap, ללא נתוני משתמש | הצמדת המיקום לכבישים ידועים (אופציונלי, תפריט מתקדם) | במכשיר בלבד; יורדת מהמאגר הציבורי של הפרויקט ב-GitHub או מועתקת ידנית |

האפליקציה **אינה אוספת, מעבירה או מוכרת** נתונים כלשהם לצדדים שלישיים.
ללא אנליטיקה, ללא SDK של פרסום, ללא רכיבי מעקב.

## הרשאות

- **מיקום מדויק/משוער** — הפונקציה העיקרית.
- **Bluetooth** — חיבור למתאם OBD (אופציונלי, מופעל על ידי המשתמש).
- **שירות בחזית + התראות** — כדי שהאפליקציה תמשיך לפעול והמצב הפעיל שלה יישאר
  גלוי כשהמסך כבוי או כשאפליקציות אחרות פתוחות.
- **אינטרנט** (INTERNET, ACCESS_NETWORK_STATE) — להורדת אפמריס מארכיוני IGS
  הפתוחים, לבדיקת שעה קצרה מול אותם שרתים (בהפעלת האפליקציה, כשהרשת מתחברת
  מחדש ומדי כמה שעות בזמן הפעולה), לאריחי מפה בזמן שמסך המפה פתוח, ורק לבקשת
  המשתמש בתפריט המתקדם — לקובץ מפת הכבישים מהמאגר הציבורי של הפרויקט ב-GitHub;
  שירותי Google Play משתמשים בו לרכישה ול-Block Store. בקשות האפמריס ובדיקת
  השעה אינן מכילות קואורדינטות, מזהים או נתוני משתמש אחרים; בקשות אריחי המפה
  חושפות רק את האזור המשוער המוצג במפה.
- **מצב Wi-Fi** (ACCESS_WIFI_STATE) — נעשה שימוש רק במספר רשתות ה-Wi-Fi
  הנראות; שמות ומזהי רשתות אינם בשימוש ואינם נשמרים.
- **הצגה מעל אפליקציות אחרות** (SYSTEM_ALERT_WINDOW) — נקודת מצב צבעונית
  אופציונלית מעל המסך; מופעלת ומכובה על ידי המשתמש.
- **מיקום מדומה** (ACCESS_MOCK_LOCATION) — נדרש טכנית כדי שהאפליקציה תוכל
  לספק את המיקום המאומת לאפליקציות אחרות (אפליקציות ניווט) דרך ספק מיקום
  הבדיקה של המערכת, כאשר אין אמון ב-GPS האמיתי.

## רכישות

הגרסה המלאה נפתחת ברכישה חד-פעמית דרך **Google Play Billing**. התשלום ונתוני
התשלום מעובדים על ידי Google Play — האפליקציה מקבלת רק אישור על הרכישה ולעולם
אינה רואה או שומרת פרטי תשלום. השימוש ב-Google Play Billing כפוף למדיניות
הפרטיות של Google עצמה: https://policies.google.com/privacy

## חשבונות

האפליקציה אינה דורשת הרשמה או כניסה לחשבון כלשהו לצורך הפונקציה העיקרית שלה.

## אחסון נתונים

כל ההגדרות, מונה הניסיון ומצב הרכישה נשמרים **באופן מקומי במכשיר**
(SharedPreferences). הסרת האפליקציה מוחקת נתונים אלה מהמכשיר; מצב הרכישה אינו
אובד, כי Google Play שומרת אותו בנפרד, בקשר לחשבון Google של המכשיר.

ערך אחד — מונה הניסיון (מספר יחיד: הקילומטרים של הניסיון החינמי שכבר נוצלו) —
נשמר בנוסף ב-Block Store של שירותי Google Play באותו מכשיר, כדי שהניסיון לא
יתחיל מחדש עקב מחיקת נתוני האפליקציה או התקנה מחדש. אם גיבוי Google מופעל
במכשיר, המספר הזה נכלל בגיבוי ה-Google המוצפן של המשתמש עצמו. הוא אינו מכיל
מיקום או מזהים, ולמפתח אין גישה אליו.

באותו אחסון נשמרים גם כיולי החיישנים של האפליקציה — רמת ההגבר הרגילה של המקלט
לכל רצועת תדר, מקדמי התיקון של חיישן המהירות של הרכב והיסט האפס של הג'ירוסקופ —
ושני סכומי המרחק המוצגים במסך הראשי (סך המרחק שנסעתם עם האפליקציה והמרחק ללא
ניווט לווייני), כדי שלא יאבדו בהתקנה מחדש של האפליקציה. אלה כמה מספרים
המתארים את הטלפון, הרכב ואת הקילומטראז' הכולל; הם אינם מכילים מיקום, היסטוריית
נסיעות או מזהים.

## שינויים במדיניות זו

שינויים מהותיים במדיניות זו יפורסמו על ידי עדכון מסמך זה עם תאריך חדש בראשו.

## יצירת קשר

gnssfilter@gmail.com
