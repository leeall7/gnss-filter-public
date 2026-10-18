# Політика конфіденційності — GNSS Nav для iPhone

Чинна з 18 жовтня 2026 року (попередня редакція — з 16 жовтня 2026). Розробник: ФОП Лі Олександр, Україна. Контакт: gnssfilter@gmail.com.

**Коротко.** GNSS Nav — навігатор, стійкий до глушіння й підміни GPS. Усе обчислюється на вашому
iPhone. Застосунок не має реєстрації, реклами й аналітики, сам нічого не збирає про вас і не передає ваші поїздки
розробникові чи третім сторонам — технічні логи потрапляють до розробника, лише якщо ви самі їх надішлете (розділ «Логи»).

## Які дані застосунок використовує і де вони лишаються

| Дані | Навіщо | Де зберігаються |
|---|---|---|
| **Геолокація** (GPS та мережеве визначення позиції iOS), зокрема у фоні під час поїздки | перевірка GPS, числення, ведення маршрутом | лише на телефоні |
| **Датчики руху** (гіроскоп, акселерометр, активність, барометр) | числення, курс, виявлення руху; барометр — зміна висоти в технічному лозі | лише на телефоні |
| **Мікрофон і розпізнавання мовлення** — лише коли ви натискаєте «Голосом» / мікрофон у пошуку | голосовий ввід адреси | звук обробляє служба розпізнавання мовлення Apple; застосунок отримує лише текст, звук не зберігає |
| **OBD-адаптер через Bluetooth** (швидкість коліс, передача, VIN авто) | числення, калібрування для вашого авто | лише на телефоні; VIN — ключ до збережених калібрувань |
| **Офлайн-вміст** (мапи, маршрути, пошук) | робота без інтернету | завантажується з публічного репозиторію GitHub на телефон |
| **Покупка** повної версії | разова покупка через Apple | обробляє Apple (App Store); розробник не отримує платіжних даних |
| **Пробний період** (лічильник кілометрів без GPS) | обмеження пробної версії | на телефоні (Keychain), не синхронізується |
| **Улюблені й нещодавні місця**, налаштування | зручність | лише на телефоні |

## Логи

Під час поїздки застосунок веде технічні логи (CSV): позиції, час, вердикти, дані OBD (зокрема VIN і назву
адаптера), датчики, назви пунктів призначення й розпізнані голосові запити, модель телефона й версію iOS, заряд батареї,
а також журнал подій — зокрема тексти голосових підказок і вказівок маневрів маршруту (і маршрутів Apple в онлайн-режимі).
Вони **зберігаються лише на телефоні** (не потрапляють у резервні копії) 14 днів, а потім видаляються самі. Їх можна
видалити будь-коли: «Деталі → Очистити логи». Файли логів видно й вам: застосунок «Файли» → «На iPhone» → GNSS Nav
(або спільний доступ до файлів у Finder на комп'ютері).

Логи передаються розробникові **лише якщо ви самі натиснете «Надіслати логи»** і виберете, куди їх
надіслати. Перед надсиланням архів шифрується публічним ключем розробника (AES-256-GCM, RSA-OAEP):
прочитати його може лише розробник. Якщо шифрування не вдалося, застосунок попереджає, і архів
звичайний.

## Що йде через інтернет

- **Завантаження офлайн-вмісту** з GitHub (releases репозиторію `gnss-filter-public`): GitHub бачить вашу
  IP-адресу, як будь-який сайт. Розробник доступу до цих запитів не має.
- **Покупка** — через Apple.
- **Мережеве визначення позиції** — стандартна служба iOS (Apple).
- **Голосовий ввід адреси** (лише коли ви його запускаєте): сказане розпізнає служба мовлення Apple (на телефоні або на
  серверах Apple) — так само, як диктування iOS. Обробляє Apple за власною політикою конфіденційності; розробник звуку не отримує; розпізнаний текст
  записується в технічний лог і потрапляє до розробника лише разом із логами, якщо ви їх надішлете.
- **Службові перевірки без ваших даних:** точний час — короткий запит HTTPS до raw.githubusercontent.com (GitHub, заголовок Date); чи справді є
  інтернет після його втрати — короткий запит до captive.apple.com (так перевіряє мережу й сама iOS). Жодних даних про вас
  чи поїздку в цих запитах немає.
- **Онлайн-режим** (типово увімкнений після вашої згоди у вікні-попередженні, вимикається в «Деталях»): мапа, затори, маршрути й пошук — від Apple
  (MapKit). Щоб показати мапу й побудувати маршрут, iOS надсилає Apple ділянку мапи, старт і пункт призначення, запит
  пошуку — так само, як застосунок «Мапи». Обробляє це Apple за власною політикою конфіденційності; розробник цих
  запитів не бачить. Без інтернету (або з вимкненим онлайн-режимом) — офлайн-мапа й маршрути; запитів мапи, маршрутів і пошуку
  Apple не отримує.

Більше нічого застосунок у мережу не надсилає. Мапи, маршрути й пошук працюють офлайн.

## Дозволи iOS

Геолокація (під час використання; у фоні — для ведення під час поїздки, із системним індикатором),
Bluetooth (OBD-адаптер), рух і фітнес (датчики), мікрофон і розпізнавання мовлення (лише для голосового вводу). Усі дозволи можна відкликати в Параметрах; без них
відповідні функції не працюють.

## Діти

Застосунок не призначений для дітей до 13 років і не збирає їхніх даних.

## Видалення даних

Усі дані лежать на телефоні: видаліть застосунок — зникне все, крім лічильника пробного періоду в
Keychain і випадкового ідентифікатора цього iPhone там же (за ним застосунок розпізнає, що резервну копію відновлено на
інший телефон, і калібрує гіроскоп заново; обидва лишаються лише на цьому iPhone до його стирання, у резервні копії й iCloud
не потрапляють, нікуди не надсилаються) і запису про покупку в Apple.
Налаштування, калібрування й улюблені місця можуть бути також у вашій власній резервній копії iPhone (iCloud чи комп'ютер).
Файл перенесення налаштувань (кнопка «Експорт») містить улюблені місця, «Дім / Робота», нещодавні місця, налаштування й
калібрування OBD з VIN авто; його створюєте й передаєте ви самі — застосунок нікуди його не надсилає.

## Зміни

Нова редакція публікується за цією ж адресою з новою датою.

---

# Privacy Policy — GNSS Nav for iPhone

Effective 18 October 2026 (previous version: 16 October 2026). Developer: Oleksandr Li (private entrepreneur), Ukraine. Contact: gnssfilter@gmail.com.

**In short.** GNSS Nav is a car navigator that keeps working when GPS is jammed or spoofed. Everything is
computed on your iPhone. There is no account, no ads, no analytics; the app collects nothing about you on its own and
never sends your trips to the developer or to third parties — technical logs reach the developer only if you send them yourself (see Logs).

**Data the app uses, and where it stays:** location (GPS and iOS network positioning, also in the
background during a drive), motion sensors (including the barometer), microphone and speech recognition (voice address
input only), data from an optional OBD-II Bluetooth adapter (wheel speed,
gear, vehicle VIN used as a key for saved calibration), offline content downloaded from a public GitHub
repository, the one-time purchase handled by Apple, the trial-distance counter (Keychain), favourites and
settings. All of it stays on the device.

**Logs.** During a drive the app writes technical CSV logs (positions, time, verdicts, OBD data including
VIN and adapter name, sensors, destination names and recognised voice queries, device model, iOS version, battery level,
and an event journal with the texts of voice prompts and route maneuver instructions, including Apple Maps routes in online mode).
They stay on the device (excluded from backups) for 14 days and are then deleted; you can delete
them any time (Details → Clear logs). You can see the log files yourself in the Files app (On My iPhone → GNSS Nav)
or via file sharing in Finder on a computer. Logs leave the device only when you tap "Send logs" and choose a
destination; the archive is encrypted with the developer's public key (AES-256-GCM, RSA-OAEP) so only the
developer can read it. If encryption fails, the app warns you and the archive is plain.

**Network use.** Offline content is downloaded from GitHub releases (GitHub sees your IP address like any
website; the developer has no access to those requests). Purchases go through Apple. Network positioning
is a standard iOS service. **Online mode** (on by default after you accept the notice, can be turned off): map, traffic,
routes and search come from Apple (MapKit); to show the map and compute a route iOS sends Apple the map area, start,
destination and search query, as the Maps app does — processed by Apple under its privacy policy; the developer does
not see these requests. In offline mode Apple receives no map, route or search requests. **Voice address input** (only when you start it): what you say is recognised by Apple's speech
service (on the device or on Apple servers), as with iOS dictation; the app receives only text and stores no audio; the developer never
receives audio, and the recognised text is written to the technical log and reaches the developer only if you send logs. **Service checks without your data:** a short HTTPS request to raw.githubusercontent.com (GitHub) for accurate time (Date header) and,
after the internet was lost, a short request to captive.apple.com to confirm it is back (as iOS itself does). Nothing else
is sent; maps, routing and search work offline.

**Permissions:** Location (while in use; in the background during a drive, with the system indicator),
Bluetooth (OBD adapter), Motion & Fitness, Microphone and Speech Recognition (voice input only). You can revoke them in Settings.

**Children:** not intended for children under 13; no data about them is collected.

**Deletion:** delete the app and everything is gone, except the trial counter in Keychain and a random identifier of this
iPhone there (it lets the app notice a backup restored onto a different phone and recalibrate the gyroscope; both are kept
only on this iPhone until it is erased, are not included in backups or iCloud and are never sent anywhere) and the purchase
record at Apple. Settings, calibration and favourites may also remain in your own iPhone backup (iCloud or computer).
The settings transfer file (“Export” button) contains favourite places, Home / Work, recent places, settings and OBD
calibration with the car's VIN; you create and share it yourself — the app never sends it anywhere.

**Changes:** a new version is published at this address with a new date.
