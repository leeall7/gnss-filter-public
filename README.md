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
4. [After every update](#4-after-every-update)
5. [OBD2 adapter (optional)](#5-obd2-adapter-optional)
6. [Manual point](#6-manual-point)
7. [Sending logs and feedback](#7-sending-logs-and-feedback)
8. [Free trial and purchase](#8-free-trial-and-purchase)
9. [Troubleshooting](#9-troubleshooting)
10. [Honest limits](#10-honest-limits)

## 1. Join the test

You need a Google account (Gmail), the same one you use in Google Play on the
phone.

1. Join the testers group: **t.me/gnssfilter**
   (or send your Gmail address to **leeall7+gnsstest@gmail.com**).
2. Open the invitation link **on the phone**:
   **https://play.google.com/apps/testing/com.gnssfilter**
   and tap **Become a tester**.
3. Install the app from Google Play using the link on that page.
4. Please keep the app installed for at least **14 days** and actually drive
   with it. Google counts only testers who stay enrolled for the whole period,
   and the test helps only if the app is really used.

Adding your address to the list is not enough. Step 2 is what makes you a
tester.

## 2. First-time setup

Android lets only one app provide a verified position to other apps, and you
have to choose it yourself. This is an Android restriction, not a fault of the
app.

1. Open **Settings → About phone** and tap **Build number** 7 times. This
   enables Developer options. (On some phones: Settings → About phone →
   Software information → Build number.)
2. Open **Settings → System → Developer options → Select mock location app**
   and choose **GNSS Filter**.
3. Open GNSS Filter and allow:
   - **Precise location** (required);
   - **Notifications** (the status stays visible while the app works in the
     background);
   - **Nearby devices / Bluetooth** — only if you use an OBD2 adapter;
   - **Display over other apps** — only if you turn on the coloured status dot.
4. Tap **Start**.

If step 2 is skipped, the app shows a red card **Mock location not allowed**
with a button **Open Developer options**.

## 3. Everyday use

Tap **Start** before driving and **Stop** when you finish. The app keeps
working with the screen off or while the navigator is in the foreground; a
notification shows the current status.

| Status | Meaning |
|---|---|
| **GPS trusted** (green) | GPS has passed the checks and is passed through |
| **GPS under watch** | GPS looks fine but is still being verified |
| **Navigating by network** (orange) | GPS is not trusted; position comes from the network and the app's own estimate |
| **Holding** (red) | No reliable source right now; the last verified position is held |
| **Warming up** | The first seconds after Start |

The **Diagnostics** section at the bottom shows technical details. You do not
need it for normal use, but it helps when you report a problem.

## 4. After every update

**Android resets the mock location choice every time the app is updated or
reinstalled.** After each update repeat step 2 of the setup: Developer options
→ Select mock location app → GNSS Filter. If you forget, the app warns you with
a red card, a notification **NOT WORKING** and a vibration.

## 5. OBD2 adapter (optional)

With a Bluetooth OBD2 adapter (ELM327 type) the app reads the real wheel speed
from the car. This makes protection noticeably more reliable while GPS is
unavailable. The app works without it, only less accurately.

1. Plug the adapter into the car and pair it in the phone's **Bluetooth
   settings** (the PIN is usually 1234 or 0000).
2. In GNSS Filter open **Settings**, turn on **OBD adapter (wheel speed)**.
3. If the adapter is not found automatically, tap **Choose adapter** and pick
   it from the list.

The app calibrates itself to your car while GPS is trusted. A tyre change is
picked up automatically after a few minutes of driving.

## 6. Manual point

If you know exactly where you are and the app's position has drifted, you can
correct it: copy coordinates from a map (for example `50.4724897, 30.4469780`),
paste them into **Manual point** in Settings and tap **Set current point**.
Protection must be running.

This is a correction tool, not a way to set an arbitrary location. If the point
is far from where the app believes you are, or there is nothing to compare it
with yet, the app shows a warning and sets the point only after you explicitly
confirm.

## 7. Sending logs and feedback

Logs are the most useful thing a tester can send, especially after a trip
where something looked wrong.

1. Open **Diagnostics → Logs ↗**.
2. Choose **24 hours** or **7 days**.
3. The archive is saved to **Downloads/GnssFilter** on the phone. Send that
   file to **[CONTACT E-MAIL]**.

**The archive contains exact coordinates, time and speed of your trips.** Send
it only if you are comfortable sharing that, and only to the address above.
The app never sends logs by itself.

When reporting a problem, please add: phone model, Android version, the app
version (shown at the bottom of Diagnostics), roughly when and where it
happened, and what you expected to see.

Questions and bug reports without personal data can also be posted in
**[Issues](../../issues)** of this repository.

## 8. Free trial and purchase

20 km of active protection are free, with no feature limits. Only distance
driven while the app is actually substituting the position is counted, not
your whole mileage. A trip that is already running is never interrupted. After
the trial, the full version is a one-time purchase through Google Play, with
no subscription. The purchase is tied to your Google account and survives
reinstalling the app.

## 9. Troubleshooting

| Problem | What to do |
|---|---|
| Red card **Mock location not allowed** | Developer options → Select mock location app → GNSS Filter. Repeat after every update |
| **Start** does nothing, message about permission | Allow **Precise** location for the app (not "Approximate") |
| No notification while running | Allow notifications for the app in Android settings |
| The app stops in the background | Settings → Apps → GNSS Filter → Battery → **Unrestricted** |
| OBD: "adapter not found among paired devices" | Pair the adapter in the phone's Bluetooth settings first, then choose it in the app |
| OBD: "no data (ignition?)" | Turn the ignition on; some adapters respond only with the engine running |
| The navigator shows a wrong place after Stop | Tap **Reset mock** in the app, or restart the navigator |
| The app is in the wrong language | Android 13+: Settings → Apps → GNSS Filter → Language |

## 10. Honest limits

No app sees satellites better than the phone's own receiver. If jamming covers
all frequencies at once, there is no satellite solution; the app then navigates
by estimate and the error grows with time. Without an OBD2 adapter the estimate
is less accurate. This is physics, not a setting.

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
4. [Після кожного оновлення](#4-після-кожного-оновлення)
5. [OBD2-адаптер (за бажанням)](#5-obd2-адаптер-за-бажанням)
6. [Ручна точка](#6-ручна-точка)
7. [Логи та зворотний зв'язок](#7-логи-та-зворотний-звязок)
8. [Пробний період і покупка](#8-пробний-період-і-покупка)
9. [Якщо щось не працює](#9-якщо-щось-не-працює)
10. [Чесно про межі](#10-чесно-про-межі)

## 1. Як стати тестувальником

Потрібен обліковий запис Google (Gmail), той самий, що в Google Play на
телефоні.

1. Приєднайтесь до групи тестувальників: **t.me/gnssfilter**
   (або надішліть свою адресу Gmail на **leeall7+gnsstest@gmail.com**).
2. Відкрийте посилання-запрошення **на телефоні**:
   **https://play.google.com/apps/testing/com.gnssfilter**
   і натисніть **Стати тестувальником**.
3. Встановіть застосунок із Google Play за посиланням на тій сторінці.
4. Будь ласка, не видаляйте застосунок щонайменше **14 днів** і справді їздіть
   із ним. Google зараховує лише тих, хто лишається в тесті весь цей час, а
   користь від тесту є тільки тоді, коли застосунком користуються.

Самої адреси в списку недостатньо. Тестувальником вас робить саме крок 2.

## 2. Перше налаштування

Android дозволяє лише одному застосунку передавати перевірену позицію іншим, і
обрати його маєте ви самі. Це обмеження Android, а не вада застосунку.

1. Відкрийте **Налаштування → Про телефон** і 7 разів торкніться **Номер
   збірки**. Це вмикає меню розробника. (На деяких телефонах: Налаштування →
   Про телефон → Відомості про ПЗ → Номер збірки.)
2. Відкрийте **Налаштування → Система → Для розробників → Вибрати застосунок
   для фіктивного місцезнаходження** й оберіть **GNSS Filter**.
3. Відкрийте GNSS Filter і дозвольте:
   - **точне місцезнаходження** (обов'язково);
   - **сповіщення** (стан видно, поки застосунок працює у фоні);
   - **пристрої поблизу / Bluetooth** — лише якщо користуєтесь OBD2-адаптером;
   - **показ поверх інших застосунків** — лише якщо вмикаєте кольорову крапку
     стану.
4. Натисніть **Старт**.

Якщо пропустити крок 2, застосунок покаже червону картку **Мок-локацію не
дозволено** з кнопкою **Відкрити меню розробника**.

## 3. Щоденне користування

Натисніть **Старт** перед поїздкою і **Стоп** після неї. Застосунок працює з
вимкненим екраном і тоді, коли на екрані навігатор; поточний стан видно у
сповіщенні.

| Стан | Що означає |
|---|---|
| **GPS у довірі** (зелений) | GPS пройшов перевірки й пропускається далі |
| **GPS під наглядом** | GPS виглядає справним, але ще перевіряється |
| **Ведемо з мережі** (помаранчевий) | GPS не в довірі; позиція з мережі та власного розрахунку |
| **Утримання** (червоний) | Надійного джерела зараз немає; тримається остання перевірена позиція |
| **Прогрів** | Перші секунди після Старту |

Розділ **Діагностика** внизу екрана показує технічні подробиці. Для звичайного
користування він не потрібен, але допомагає, коли повідомляєте про проблему.

## 4. Після кожного оновлення

**Android скидає вибір застосунку для фіктивного місцезнаходження після
кожного оновлення чи перевстановлення.** Після кожного оновлення повторіть
крок 2 налаштування: Для розробників → Вибрати застосунок для фіктивного
місцезнаходження → GNSS Filter. Якщо забудете, застосунок попередить червоною
карткою, сповіщенням **НЕ ПРАЦЮЄ** і вібрацією.

## 5. OBD2-адаптер (за бажанням)

З Bluetooth OBD2-адаптером (типу ELM327) застосунок читає справжню швидкість
коліс з автомобіля. Це помітно підвищує надійність захисту, поки GPS
недоступний. Без адаптера застосунок теж працює, лише менш точно.

1. Вставте адаптер в автомобіль і спаруйте його в **налаштуваннях Bluetooth**
   телефона (PIN зазвичай 1234 або 0000).
2. У GNSS Filter відкрийте **Налаштування** й увімкніть **OBD-адаптер
   (швидкість з коліс)**.
3. Якщо адаптер не знайшовся сам, натисніть **Обрати адаптер** і виберіть його
   зі списку.

Застосунок сам підлаштовується під ваш автомобіль, поки GPS у довірі. Заміну
шин він підхоплює автоматично за кілька хвилин їзди.

## 6. Ручна точка

Якщо ви точно знаєте, де перебуваєте, а позиція в застосунку з'їхала, її можна
виправити: скопіюйте координати з карти (наприклад `50.4724897, 30.4469780`),
вставте в поле **Ручна точка** в Налаштуваннях і натисніть **Встановити
поточну точку**. Захист має бути запущений.

Це засіб уточнення, а не спосіб задати довільне місце. Якщо точка далеко від
того, де застосунок вас бачить, або звірити її поки нема з чим, застосунок
покаже попередження й поставить точку лише після вашого явного підтвердження.

## 7. Логи та зворотний зв'язок

Логи — найкорисніше, що може надіслати тестувальник, особливо після поїздки,
де щось виглядало не так.

1. Відкрийте **Діагностика → Логи ↗**.
2. Оберіть **24 години** або **7 днів**.
3. Архів збережеться в **Downloads/GnssFilter** на телефоні. Надішліть цей
   файл на **[КОНТАКТНА АДРЕСА]**.

**В архіві точні координати, час і швидкість ваших поїздок.** Надсилайте його,
лише якщо готові цим поділитись, і лише на адресу вище. Сам застосунок логи
нікуди не надсилає.

Повідомляючи про проблему, додайте: модель телефона, версію Android, версію
застосунку (внизу Діагностики), приблизно коли й де це сталось і що ви
очікували побачити.

Питання й повідомлення про помилки без особистих даних можна також лишати в
**[Issues](../../issues)** цього репозиторію.

## 8. Пробний період і покупка

20 км активного захисту безкоштовні, без обмеження функцій. Рахуються лише
кілометри, коли застосунок справді підставляє позицію, а не весь пробіг.
Поїздка, яка вже триває, ніколи не переривається. Після пробного періоду
повна версія купується один раз через Google Play, без підписки. Покупка
прив'язана до вашого облікового запису Google і зберігається після
перевстановлення.

## 9. Якщо щось не працює

| Проблема | Що зробити |
|---|---|
| Червона картка **Мок-локацію не дозволено** | Для розробників → Вибрати застосунок для фіктивного місцезнаходження → GNSS Filter. Повторювати після кожного оновлення |
| **Старт** не спрацьовує, повідомлення про дозвіл | Дозвольте застосунку **точне** місцезнаходження (не «приблизне») |
| Немає сповіщення під час роботи | Дозвольте сповіщення для застосунку в налаштуваннях Android |
| Застосунок зупиняється у фоні | Налаштування → Застосунки → GNSS Filter → Акумулятор → **Без обмежень** |
| OBD: «адаптер не знайдено серед спарених» | Спершу спаруйте адаптер у налаштуваннях Bluetooth телефона, потім оберіть його в застосунку |
| OBD: «без даних (запалювання?)» | Увімкніть запалювання; деякі адаптери відповідають лише із заведеним двигуном |
| Після Стоп навігатор показує не те місце | Натисніть **Скинути мок** у застосунку або перезапустіть навігатор |
| Застосунок не тією мовою | Android 13+: Налаштування → Застосунки → GNSS Filter → Мова |

## 10. Чесно про межі

Жоден застосунок не бачить супутників краще за приймач телефона. Якщо глушіння
накриває всі частоти одночасно, супутникового рішення не буде; тоді застосунок
веде за розрахунком, і похибка з часом зростає. Без OBD2-адаптера розрахунок
менш точний. Це фізика, а не налаштування.
