# GNSS Filter

**English** · [Українська](#українська)

GNSS Filter protects navigation on Android when GPS is jammed or spoofed. It
checks the satellite position against independent sources and gives your
navigator (Google Maps, Waze, etc.) only a position it has verified. When GPS
cannot be trusted, it keeps navigating by its own estimate instead of showing
a fake location.

- Android 10 or newer
- Interface: English and Ukrainian
- All processing happens on the phone. Location data is never sent anywhere.
  [Privacy Policy](PRIVACY_POLICY.md)

> This repository contains instructions and the privacy policy only.
> The source code is not published.

## Contents

1. [Join the test](#1-join-the-test)
2. [First-time setup](#2-first-time-setup)
3. [Everyday use](#3-everyday-use)
4. [If the app was reinstalled](#4-if-the-app-was-reinstalled)
5. [OBD2 adapter (recommended)](#5-obd2-adapter-recommended)
6. [Car position on the map](#6-car-position-on-the-map)
7. [Sending logs and feedback](#7-sending-logs-and-feedback)
8. [Free trial and purchase](#8-free-trial-and-purchase)
9. [Troubleshooting](#9-troubleshooting)
10. [Honest limits](#10-honest-limits)
11. [Terms of distribution](#11-terms-of-distribution)

## 1. Join the test

You need a Google account (Gmail), the same one you use in Google Play on the
phone.

1. Write to **[t.me/gnssfilter](https://t.me/gnssfilter)** and send the Gmail
   address you use on your phone. We add it to the tester list by hand, so it
   may take a little while — no need to write twice.
2. Once you get a reply confirming you're on the list, open this link **on
   the phone**: **https://play.google.com/apps/testing/com.gnssfilter**
   and tap **Become a tester**.
3. Install the app from Google Play using the link on that page.
4. Please keep the app installed for at least **14 days** and actually drive
   with it. Google counts only testers who stay enrolled for the whole period,
   and the test helps only if the app is really used.

Sending your address is not enough by itself — step 2 is what actually makes
you a tester.

## 2. First-time setup

Android lets only one app provide a verified position to other apps, and you
have to choose it yourself. This is an Android restriction, not a fault of the
app.

1. Open **Settings → About phone** and tap **Build number** 7 times. This
   enables Developer options. (On some phones: Settings → About phone →
   Software information → Build number.)
2. Open **Settings → System → Developer options → Select mock location app**
   and choose **GNSS Filter**.
3. In the same **Developer options** menu turn on **Force full GNSS
   measurements**. It keeps the receiver tracking all constellations and
   frequencies without power-saving pauses. On Android 12 and newer the app
   requests this mode by itself, so there the switch is a safety net; on
   Android 10–11 it is the only way to get it. The cost is somewhat higher
   battery use while GPS is active. The name may differ slightly between
   phone makers.
4. Open GNSS Filter and allow:
   - **Precise location** (required);
   - **Notifications** (the status stays visible while the app works in the
     background);
   - **Nearby devices / Bluetooth** — only if you use an OBD2 adapter;
   - **Display over other apps** — only if you turn on the coloured status dot.
5. Tap **Start**.

If step 2 is skipped, the app shows a red card **Mock location not allowed**
with a button **Open Developer options**.

## 3. Everyday use

Tap **Start** before driving and **Stop** when you finish. The app keeps
working with the screen off or while the navigator is in the foreground; a
notification shows the current status.

**Which navigator.** Best compatibility so far is with **Waze**: it follows the
position smoothly under interference. Google Maps may show "searching for GPS"
and move the marker in jumps while GPS is jammed; we are working on it.

| Status | Meaning |
|---|---|
| **GPS trusted** (green) | GPS has passed the checks and is passed through |
| **GPS under watch** | GPS looks fine but is still being verified |
| **Navigating by network** (orange) | GPS is not trusted; position comes from the network and the app's own estimate |
| **Holding** (red) | No reliable source right now; the last verified position is held |
| **Warming up** | The first seconds after Start |

The **Diagnostics** section at the bottom shows technical details. You do not
need it for normal use, but it helps when you report a problem.

## 4. If the app was reinstalled

The mock location app is selected **once**: Android keeps this choice when the
app is updated. Repeat step 2 of the setup (Developer options → Select mock
location app → GNSS Filter) only if the app was **uninstalled and installed
again**, or its **data was cleared**. If the choice is lost, the app warns you
with a red card, a notification **NOT WORKING** and a vibration.

## 5. OBD2 adapter (recommended)

**The highest reliability under GPS interference is achieved only with a
Bluetooth OBD2 adapter.** With it the app reads the real wheel speed from the
car, which a jammer cannot fake. While GPS is unavailable this is what keeps
the estimated position accurate.

Without an adapter the app still detects spoofing and jamming and still falls
back to the network position. But it does not know how fast the car is moving:
its own estimate then only briefly continues the motion at the last known
speed, so between network fixes the position is rough and may lag.

**Which adapter to choose**

- It must be **ELM327-compatible** and use **classic Bluetooth** (sold as
  "Bluetooth", "for Android", Bluetooth 2.0/3.0).
- **Tested by us:** ELM327 Bluetooth **v1.5**, two-board version, chip
  **PIC18F25K80**. If you can choose, take this one.
- **Will not work:** Wi-Fi adapters, and adapters with Bluetooth LE only
  (usually sold as "for iPhone / iOS", "Bluetooth 4.0"). Dual-mode adapters
  (classic + LE) are fine.
- **At your own risk:** cheap single-board clones marked **v2.1**. Many of them
  support fewer car protocols and may fail to connect to older cars (roughly
  before 2008). We have not tested them.
- The car must have an OBD2 port (petrol cars in the EU since 2001, diesel
  since 2004). Some electric cars do not answer standard OBD2 requests.

If the adapter suits, the OBD line on the main screen shows **connected** and
the speed.

1. Plug the adapter into the car and pair it in the phone's **Bluetooth
   settings** (the PIN is usually 1234 or 0000).
2. In GNSS Filter open **Settings**, turn on **OBD adapter (wheel speed)**.
3. If the adapter is not found automatically, tap **Choose adapter** and pick
   it from the list.

The app calibrates itself to your car while GPS is trusted. A tyre change is
picked up automatically after a few minutes of driving.

## 6. Car position on the map

The main screen has two numbered buttons: **1 Start** and, right below it,
**2 Adjust car position on the map**. Press them in that order.

If you know exactly where the car is and the app's position has drifted, or the
app does not know which way the car is facing, tap **2**. The map opens centred
on the app's current position:

- drag the map so that the centre mark is where the car really is;
- turn the arrow to the direction the car is facing;
- tap **Accept**.

If you only turned the arrow and did not move the map, only the direction is
applied. When GPS is jammed and the app does not yet know the direction, it
offers this screen by itself once per session.

This is a correction tool, not a way to set an arbitrary location, so it is
limited:

- the point must be **within 5 km** of the position the app already knows. A
  point farther away is rejected, and there is no way to confirm it anyway;
- right after **Start**, while the app has no GPS or network fix yet, there is
  nothing to compare the point with, so it is not accepted. Wait for the first
  fix and try again;
- while protection is stopped, the point is not accepted at all.

In each case the app shows a message with the reason.

## 7. Sending logs and feedback

Logs are the most useful thing a tester can send, especially after a trip
where something looked wrong.

1. Open **Diagnostics → Logs ↗**.
2. Choose **24 hours** or **7 days**.
3. The archive is saved to **Downloads/GnssFilter** on the phone. Send that
   file to **[t.me/gnssfilter](https://t.me/gnssfilter)** or to
   **gnssfilter@gmail.com**.

**The archive contains exact coordinates, time and speed of your trips.** Send
it only if you are comfortable sharing that, and only to the address above.
The app never sends logs by itself.

When reporting a problem, please add: phone model, Android version, the app
version (shown at the bottom of Diagnostics), roughly when and where it
happened, and what you expected to see.

Questions and bug reports without personal data can also be posted in
**[Issues](../../issues)** of this repository.

## 8. Free trial and purchase

50 km of active protection are free, with no feature limits. Only distance
driven while the app is actually substituting the position is counted, not
your whole mileage. A trip that is already running is never interrupted. After
the trial, the full version is a one-time purchase through Google Play, with
no subscription. The purchase is tied to your Google account and survives
reinstalling the app.

## 9. Troubleshooting

| Problem | What to do |
|---|---|
| Red card **Mock location not allowed** | Developer options → Select mock location app → GNSS Filter. Needed once; again only after reinstalling the app or clearing its data |
| **Start** does nothing, message about permission | Allow **Precise** location for the app (not "Approximate") |
| No notification while running | Allow notifications for the app in Android settings |
| The app stops in the background | Settings → Apps → GNSS Filter → Battery → **Unrestricted** |
| OBD: "adapter not found among paired devices" | Pair the adapter in the phone's Bluetooth settings first, then choose it in the app |
| OBD: "no data (ignition?)" | Turn the ignition on; some adapters respond only with the engine running |
| The navigator shows a wrong place after Stop | Open GNSS Filter once — it removes any leftover mock location by itself — or restart the navigator |
| A taxi or delivery driver app reports location spoofing | Press **Stop**. If it still complains, set Developer options → "Select mock location app" to "No app" (choose GNSS Filter again before the next drive). Such apps do not allow work while any mock location app is active (see section 10) |
| The app is in the wrong language | Android 13+: Settings → Apps → GNSS Filter → Language |

## 10. Honest limits

No app sees satellites better than the phone's own receiver. If jamming covers
all frequencies at once, there is no satellite solution; the app then navigates
by estimate and the error grows with time. Without an OBD2 adapter the app does
not know the speed, so this estimate is only a short bridge between network
fixes. This is physics, not a setting.

**Taxi and delivery drivers.** Taxi and courier driver apps do not allow work
while GNSS Filter is active. The app does not distort your position, it only
refines it, but it passes the position to the navigator through the same
system mechanism (mock location) that these services treat as location
spoofing. Press **Stop** while working in such an app. If the driver app still
complains, set Developer options → "Select mock location app" to "No app" and
choose GNSS Filter again before your next drive.

## 11. Terms of distribution

- The app is provided **as is**, without any warranty that it will work in
  every situation, on every phone or with every car. It is an aid to
  navigation, not a replacement for your own attention on the road.
- Updates are released **gradually**: each new version is first checked by a
  limited number of users and only then made available to everyone.
- **Refunds.** The purchase is made through Google Play, and Google processes
  the payment. Within 48 hours of the purchase you can request a refund
  directly in Google Play; the decision is made by Google under its own
  rules. After that period the developer does not issue refunds. The full
  version is unlocked immediately after payment, so please use the free trial
  (50 km of active protection, all features) to check the app on your phone
  and in your car **before** buying.
- These terms do not limit any rights you have under consumer protection law.

---

# Українська

[English](#gnss-filter) · **Українська**

GNSS Filter захищає навігацію на Android, коли GPS глушать або підміняють.
Застосунок звіряє супутникову позицію з незалежними джерелами й віддає
навігатору (Google Maps, Waze тощо) лише перевірену позицію. Коли GPS довіряти
не можна, він веде далі за власним розрахунком, а не показує чуже місце.

- Android 10 або новіший
- Інтерфейс: українська та англійська
- Уся обробка відбувається на телефоні. Дані про місцезнаходження нікуди не
  надсилаються. [Політика конфіденційності](PRIVACY_POLICY.md)

> У цьому репозиторії лише інструкції та політика конфіденційності.
> Вихідний код не публікується.

## Зміст

1. [Як стати тестувальником](#1-як-стати-тестувальником)
2. [Перше налаштування](#2-перше-налаштування)
3. [Щоденне користування](#3-щоденне-користування)
4. [Якщо застосунок перевстановили](#4-якщо-застосунок-перевстановили)
5. [OBD2-адаптер (бажано)](#5-obd2-адаптер-бажано)
6. [Позиція авто на карті](#6-позиція-авто-на-карті)
7. [Логи та зворотний зв'язок](#7-логи-та-зворотний-звязок)
8. [Пробний період і покупка](#8-пробний-період-і-покупка)
9. [Якщо щось не працює](#9-якщо-щось-не-працює)
10. [Чесно про межі](#10-чесно-про-межі)
11. [Умови розповсюдження](#11-умови-розповсюдження)

## 1. Як стати тестувальником

Потрібен обліковий запис Google (Gmail), той самий, що в Google Play на
телефоні.

1. Напишіть у **[t.me/gnssfilter](https://t.me/gnssfilter)** і надішліть Gmail-адресу,
   яку використовуєте на телефоні. Ми додаємо адреси до списку вручну, тож це
   може зайняти трохи часу — писати вдруге не треба.
2. Коли отримаєте підтвердження, що вас додано, відкрийте на телефоні:
   **https://play.google.com/apps/testing/com.gnssfilter**
   і натисніть **Стати тестувальником**.
3. Встановіть застосунок із Google Play за посиланням на тій сторінці.
4. Будь ласка, не видаляйте застосунок щонайменше **14 днів** і справді їздіть
   із ним. Google зараховує лише тих, хто лишається в тесті весь цей час, а
   користь від тесту є тільки тоді, коли застосунком користуються.

Самого надсилання адреси недостатньо — тестувальником вас робить саме крок 2.

## 2. Перше налаштування

Android дозволяє лише одному застосунку передавати перевірену позицію іншим, і
обрати його маєте ви самі. Це обмеження Android, а не вада застосунку.

1. Відкрийте **Налаштування → Про телефон** і 7 разів торкніться **Номер
   збірки**. Це вмикає меню розробника. (На деяких телефонах: Налаштування →
   Про телефон → Відомості про ПЗ → Номер збірки.)
2. Відкрийте **Налаштування → Система → Для розробників → Вибрати застосунок
   для фіктивного місцезнаходження** й оберіть **GNSS Filter**.
3. У тому самому меню **Для розробників** увімкніть **Примусове ввімкнення
   вимірювання всіх GNSS** (Force full GNSS measurements). Тоді приймач
   відстежує всі сузір'я й частоти без енергоощадних пауз. На Android 12 і
   новіших застосунок просить цей режим сам, тож там перемикач — підстраховка;
   на Android 10–11 це єдиний спосіб його отримати. Ціна — дещо більша витрата
   акумулятора, поки працює GPS. У різних виробників назва пункту може трохи
   відрізнятись.
4. Відкрийте GNSS Filter і дозвольте:
   - **точне місцезнаходження** (обов'язково);
   - **сповіщення** (стан видно, поки застосунок працює у фоні);
   - **пристрої поблизу / Bluetooth** — лише якщо користуєтесь OBD2-адаптером;
   - **показ поверх інших застосунків** — лише якщо вмикаєте кольорову крапку
     стану.
5. Натисніть **Старт**.

Якщо пропустити крок 2, застосунок покаже червону картку **Мок-локацію не
дозволено** з кнопкою **Відкрити меню розробника**.

## 3. Щоденне користування

Натисніть **Старт** перед поїздкою і **Стоп** після неї. Застосунок працює з
вимкненим екраном і тоді, коли на екрані навігатор; поточний стан видно у
сповіщенні.

**Який навігатор.** Найкраща сумісність наразі — з **Waze**: під завадою він
веде позицію плавно. Google Maps, поки GPS глушать, може показувати «пошук GPS»
і рухати позначку ривками; ми над цим працюємо.

| Стан | Що означає |
|---|---|
| **GPS у довірі** (зелений) | GPS пройшов перевірки й пропускається далі |
| **GPS під наглядом** | GPS виглядає справним, але ще перевіряється |
| **Ведемо з мережі** (помаранчевий) | GPS не в довірі; позиція з мережі та власного розрахунку |
| **Утримання** (червоний) | Надійного джерела зараз немає; тримається остання перевірена позиція |
| **Прогрів** | Перші секунди після Старту |

Розділ **Діагностика** внизу екрана показує технічні подробиці. Для звичайного
користування він не потрібен, але допомагає, коли повідомляєте про проблему.

## 4. Якщо застосунок перевстановили

Застосунок для фіктивного місцезнаходження обирається **один раз**: під час
оновлення Android цей вибір зберігає. Повторити крок 2 налаштування (Для
розробників → Вибрати застосунок для фіктивного місцезнаходження → GNSS Filter)
потрібно лише тоді, коли застосунок **видалили й встановили заново** або
**очистили його дані**. Якщо вибір злетів, застосунок попередить червоною
карткою, сповіщенням **НЕ ПРАЦЮЄ** і вібрацією.

## 5. OBD2-адаптер (бажано)

**Найвища достовірність під завадами GPS досягається лише з Bluetooth
OBD2-адаптером.** З ним застосунок читає справжню швидкість коліс з
автомобіля, а її глушилка підробити не може. Саме це тримає точність
розрахованої позиції, поки GPS недоступний.

Без адаптера застосунок так само виявляє підміну й глушіння і так само
переходить на позицію з мережі. Але він не знає, з якою швидкістю їде авто:
власний розрахунок тоді лише коротко продовжує рух за останньою відомою
швидкістю, тож між мережевими фіксами позиція груба й може запізнюватись.

**Який адаптер обрати**

- Він має бути **сумісний з ELM327** і працювати через **класичний Bluetooth**
  (продається як «Bluetooth», «для Android», Bluetooth 2.0/3.0).
- **Перевірено нами:** ELM327 Bluetooth **v1.5**, двоплатний, чіп
  **PIC18F25K80**. Якщо є вибір, беріть саме такий.
- **Не підійдуть:** Wi-Fi-адаптери та адаптери лише з Bluetooth LE (зазвичай
  продаються як «для iPhone / iOS», «Bluetooth 4.0»). Двохрежимні (класичний +
  LE) підходять.
- **На власний ризик:** дешеві одноплатні клони з позначкою **v2.1**. Багато з
  них підтримують менше автомобільних протоколів і можуть не з'єднатися зі
  старшими авто (приблизно до 2008 року). Ми їх не перевіряли.
- В автомобілі має бути роз'єм OBD2 (бензинові авто в ЄС з 2001 року, дизельні
  з 2004). Деякі електромобілі не відповідають на стандартні запити OBD2.

Якщо адаптер підходить, рядок OBD на головному екрані показує **з'єднано** і
швидкість.

1. Вставте адаптер в автомобіль і спаруйте його в **налаштуваннях Bluetooth**
   телефона (PIN зазвичай 1234 або 0000).
2. У GNSS Filter відкрийте **Налаштування** й увімкніть **OBD-адаптер
   (швидкість з коліс)**.
3. Якщо адаптер не знайшовся сам, натисніть **Обрати адаптер** і виберіть його
   зі списку.

Застосунок сам підлаштовується під ваш автомобіль, поки GPS у довірі. Заміну
шин він підхоплює автоматично за кілька хвилин їзди.

## 6. Позиція авто на карті

На головному екрані — дві пронумеровані кнопки: **1 Старт** і одразу під нею
**2 Уточнити позицію авто на карті**. Натискайте їх у такому порядку.

Якщо ви точно знаєте, де стоїть авто, а позиція в застосунку з'їхала, або
застосунок не знає, куди авто повернуте, натисніть **2**. Карта відкриється з
центром у поточній позиції застосунку:

- посуньте карту, щоб позначка в центрі стала там, де авто насправді;
- поверніть стрілку туди, куди дивиться авто;
- натисніть **Прийняти**.

Якщо ви лише повернули стрілку й не рухали карту, застосовується тільки
напрямок. Коли GPS глушать і застосунок ще не знає напрямку, він сам
запропонує цей екран — один раз за сеанс.

Це засіб уточнення, а не спосіб задати довільне місце, тому він обмежений:

- точка має бути **в межах 5 км** від позиції, яку застосунок уже знає. Дальшу
  точку він відхилить, і підтвердити її «все одно» неможливо;
- одразу після **Старту**, поки немає ні GPS-, ні мережевого фікса, звірити
  точку нема з чим, тому вона не приймається. Дочекайтесь першого фікса й
  спробуйте ще раз;
- коли захист зупинено, точка не приймається взагалі.

У кожному випадку застосунок показує повідомлення з причиною.

## 7. Логи та зворотний зв'язок

Логи — найкорисніше, що може надіслати тестувальник, особливо після поїздки,
де щось виглядало не так.

1. Відкрийте **Діагностика → Логи ↗**.
2. Оберіть **24 години** або **7 днів**.
3. Архів збережеться в **Downloads/GnssFilter** на телефоні. Надішліть цей
   файл у **[t.me/gnssfilter](https://t.me/gnssfilter)** або на
   **gnssfilter@gmail.com**.

**В архіві точні координати, час і швидкість ваших поїздок.** Надсилайте його,
лише якщо готові цим поділитись, і лише на адресу вище. Сам застосунок логи
нікуди не надсилає.

Повідомляючи про проблему, додайте: модель телефона, версію Android, версію
застосунку (внизу Діагностики), приблизно коли й де це сталось і що ви
очікували побачити.

Питання й повідомлення про помилки без особистих даних можна також лишати в
**[Issues](../../issues)** цього репозиторію.

## 8. Пробний період і покупка

50 км активного захисту безкоштовні, без обмеження функцій. Рахуються лише
кілометри, коли застосунок справді підставляє позицію, а не весь пробіг.
Поїздка, яка вже триває, ніколи не переривається. Після пробного періоду
повна версія купується один раз через Google Play, без підписки. Покупка
прив'язана до вашого облікового запису Google і зберігається після
перевстановлення.

## 9. Якщо щось не працює

| Проблема | Що зробити |
|---|---|
| Червона картка **Мок-локацію не дозволено** | Для розробників → Вибрати застосунок для фіктивного місцезнаходження → GNSS Filter. Потрібно один раз; повторно — лише після перевстановлення застосунку або очищення його даних |
| **Старт** не спрацьовує, повідомлення про дозвіл | Дозвольте застосунку **точне** місцезнаходження (не «приблизне») |
| Немає сповіщення під час роботи | Дозвольте сповіщення для застосунку в налаштуваннях Android |
| Застосунок зупиняється у фоні | Налаштування → Застосунки → GNSS Filter → Акумулятор → **Без обмежень** |
| OBD: «адаптер не знайдено серед спарених» | Спершу спаруйте адаптер у налаштуваннях Bluetooth телефона, потім оберіть його в застосунку |
| OBD: «без даних (запалювання?)» | Увімкніть запалювання; деякі адаптери відповідають лише із заведеним двигуном |
| Після Стоп навігатор показує не те місце | Відкрийте GNSS Filter — він сам прибере залишки фіктивного місцезнаходження — або перезапустіть навігатор |
| Застосунок водія таксі чи доставки повідомляє про підміну геолокації | Натисніть **Стоп**. Якщо скаржиться далі — у параметрах розробника для «Вибрати застосунок для фіктивних місцезнаходжень» оберіть «Немає» (перед наступною поїздкою знову оберіть GNSS Filter). Такі застосунки не дозволяють працювати, поки активний будь-який застосунок фіктивного місцезнаходження (див. розділ 10) |
| Застосунок не тією мовою | Android 13+: Налаштування → Застосунки → GNSS Filter → Мова |

## 10. Чесно про межі

Жоден застосунок не бачить супутників краще за приймач телефона. Якщо глушіння
накриває всі частоти одночасно, супутникового рішення не буде; тоді застосунок
веде за розрахунком, і похибка з часом зростає. Без OBD2-адаптера застосунок
не знає швидкості, тож цей розрахунок — лише короткий місток між мережевими
фіксами. Це фізика, а не налаштування.

**Водіям таксі й доставки.** Застосунки для водіїв таксі й кур'єрів не
дозволяють працювати, поки увімкнений GNSS Filter. Він не спотворює позицію, а
лише уточнює її, але передає її навігатору тим самим системним механізмом
(фіктивне місцезнаходження), який ці сервіси вважають підміною геолокації. На
час роботи в такому застосунку натисніть **Стоп**. Якщо застосунок водія все
одно скаржиться — у параметрах розробника для «Вибрати застосунок для фіктивних
місцезнаходжень» оберіть «Немає», а перед наступною поїздкою знову GNSS Filter.

## 11. Умови розповсюдження

- Застосунок надається **як є**, без гарантії, що він працюватиме в кожній
  ситуації, на кожному телефоні й з кожним автомобілем. Це допомога в
  навігації, а не заміна вашої власної уваги на дорозі.
- Оновлення виходять **поступово**: кожну нову версію спершу перевіряє
  обмежене число користувачів, і лише після цього вона стає доступна всім.
- **Повернення коштів.** Покупка здійснюється через Google Play, платіж
  обробляє Google. Протягом 48 годин після покупки ви можете подати запит на
  повернення безпосередньо в Google Play; рішення ухвалює Google за своїми
  правилами. Після цього строку розробник повернень не здійснює. Повна версія
  відкривається одразу після оплати, тому, будь ласка, скористайтеся
  безкоштовним пробним періодом (50 км активного захисту, усі функції), щоб
  перевірити застосунок на своєму телефоні й у своєму авто **до** покупки.
- Ці умови не обмежують прав, які вам надає законодавство про захист прав
  споживачів.
