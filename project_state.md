# حالة المشروع — sana-dashboard

**الإصدار:** `1.9.0`، منشور على GitHub (`kamalyaser31/sana-dashboard`، عام) وPages: https://kamalyaser31.github.io/sana-dashboard/، و`API_URL` يشير إلى النشر `AKfycbwxv2ue…` (النسخة 35).
**تاريخ التحديث:** `2026-10-29`

## البنية

- `index.html`: Alpine.js 3.14.8 وTailwind 3.4.17 من CDN، RTL، وقراراتها S-38…S-46 في `PLAN_STUDENTS_SHEET.md` بمستودع السكربت. ولا روابط تنقل في أعلاها (2026-10-27).
- `call(action, args, done)` يرسل `{action, token, test, year, args}` إلى `API_URL` بـ `fetch` ونوع `text/plain`، والرد `{ok, data, outcome}` أو `{ok: false, error, auth}`؛ و`auth` يمحو الجلسة ويعيد قسم الدخول.
- الجلسة `{token, who}` في `sessionStorage` (`sana_dashboard_session`)، فتبقى بعد إعادة التحميل وتذهب بإغلاق التبويب.
- كل طالب يحمل `teacher`، والمفتاح `k(s)` = المعلم|المفتاح، لأن «كل المعلمين» يجمع طلاباً بالاسم نفسه عند معلمَين.
- معرّفات حقول الصفوف بترتيب الصف (`g-0`، `by-0`، `ph-0`)، لا بالمفتاح.
- قسم «تقارير الحلقات» (`#reports`): `repTeacher` ('*' لكل المعلمين) و`repMonth`؛ `reportRows()` يرتب الأحدث أولاً: بالتاريخ، ثم الصف الأخير من الشيت، ثم المعلم؛ و`reportTotals()` من الصفوف التي لا حالة لها؛ و`refreshReports()` يرسل `refreshReports`. ونوع الحلقة رابط إلى `r.link` إن وُجد (يردّه السكربت `https` وحده).
- عمود «إجراء» (S-59): `startEditReport` يفتح نموذج المدة (ساعات ودقائق) وعدد الطلاب تحت الجدول وينقل التركيز إلى الساعات، و`saveReport` يرسل `editReport`؛ و`askDeleteReport` يُظهر «تأكيد الحذف» وينقل التركيز إليه، و`deleteReport` يرسل `deleteReport`. ويُرسل `reportRef(r)` (المعلم والشهر و`row` و`stamp`)، ويُكتب «شهر ثابت» مكان الزرين حين `editable` باطل.
- قسم «التكريمات» (`#honors`، S-60): نموذج `honTeacher` و`honKey` و`honDate` (نص `yyyy-mm-dd`، مبدئياً `data.today`) و`honReason` يرسل `addHonor`؛ و`honMonth` يختار تكريمات الشهر من `data.honors`، ولكل صف «احذف» ثم «تأكيد الحذف» (`pendingHonor`) يرسل `deleteHonor`، و«شهر ثابت» حين `editable` باطل؛ و`honorRanking()` يرتب الطلاب بعدد تكريماتهم. وعمود «التكريمات» من `s.honors`. وفي الرواتب `honorAmountInput` يذهب مع `savePay`.
- `donors.html` (S-61):
  - البطاقتان مقصورتان: الشهر على `CARD_KEYS` الثلاثة، والسنة على `TOTAL_COLUMNS` الثلاثة.
  - و`TERMS` يملأ قسم «معاني الأرقام».
  - وفي آخرها، خارج `<main>`، قسم «تبرّع وتواصل»: الرقم `+201037398740` نصاً ورابط `wa.me`، بلا وسيلة دفع (كمال 2026-10-28، نقضاً لقرار 2026-10-27).
- صفحة عامة بلا كلمة مرور ولا API، Alpine وTailwind من CDN. `YEARS` يربط كل سنة برابطي CSV لتبويبي الملف العام المنشور؛ و`readTab` يجد صف الرؤوس بأول خانة («المعلم» أو «الشهر») ويقرأ الأعمدة بأسمائها، فلا يضرّه عمود جديد؛ ويأخذ صفوف «الأكاديمية» وحدها، والأخير إن تكرر الشهر. والشهر ثابت بعد الخامس من الشهر التالي (`isFrozen`)، والخانة الفارغة «لا يُحسب». والرسوم SVG من `chart(c)`: عمود لكل شهر من اليمين، لون واحد `#2a78d6`، وقيمة آخر شهر وأعلاه مكتوبتان، و`<title>` لكل عمود؛ والرسم مخفي عن قارئ الشاشة ومعه جدول `sr-only`.
- قسم «الرواتب والمصروفات» (`#rates`): جدول المستحقات ظاهر بعد فتح الرواتب، وزر «عدّل الأسعار» (`payEditing`، `aria-expanded`) يفتح استمارة `#pay-edit`: الأسعار والثابتة ومبلغ التكريم والمصروفات الأخرى (`expMonth`، `expAmount` يُملأ من `data.expenses` بـ `expenseOf`)، بزر «احفظ الأسعار» (U-02): `changedRates()` و`changedFixed()` و`changedHonorAmount()` و`changedExpense()`، و`savePay()` يرسلها طلباً واحداً (`rn`/`rv`، `fn`/`fv`، `honorAmount`، `em`/`ea`). ولا قسم «مصروفات» ولا «سجل أسعار».
- النشطون والغائبون: `isActive(s)` = `daysAway(s) <= data.activeDays` (أو بلا تاريخ). «الطلاب» (`filteredStudents()`) للنشطين، و«الطلاب الغائبون» (`#absent`، `absentStudents()`، `absTeacher`، `absSearch`) لغيرهم بمعرّفات `ag-`/`aby-`/`aph-`. و`changedStudents(active)` و`saveStudents(active)` لكل قسم حفظه، ويرفض أكثر من `MAX_STUDENTS` (50). و«تصحيح اسم» (الخطأ) و`honorStudents()` من النشطين، والاسم الصحيح من الكل.
- `downloadStudents(list, title, teacher)`: CSV بـ BOM في المتصفح، والخانة التي تبدأ بـ `= + - @` أو أرقام طويلة تُسبق بـ tab لئلا يقرأها Excel رقماً أو صيغة.
- «سجل الطالب» (`#history`): `hisTeacher` و`hisKey`، و`historyRows()` تصل كل `s.recent` بصف «تقارير الحلقات» للمعلم في اليوم و`session` كما يكتبه `_sessionLabel` («صباحية (حلقة 2)»)، وتفضّل المحسوب ذا الرابط.
- رسالة الشهر: `msgMonth` (المبدئي الشهر الماضي) و`monthMessage(s, month)` من `s.months` و`lastHifz` (إن لم يكن `lastHifzDate` بعد الشهر) وتكريمات الشهر من `data.honors`، والضمير بالجنس؛ و`monthLink(s)` رابط `wa.me`.
- قسم الرواتب: `data.payOpen` يختار بين استمارة «افتح الرواتب» (`unlockPay`) والجداول وزر «أقفل الرواتب» (`lockPay`)؛ و`payData()` يقبل `pay` فارغاً؛ و`focusSoon` ينقل المؤشر بعد أن يُظهر x-show العنصر.

## الاختبار

لا اختبار في المستودع. جُرّبت في Chromium بلا واجهة على `fetch` بديل (سكربت Playwright في مساحة العمل المؤقتة): الدخول الخطأ والصحيح، وانتقال المؤشر، وبقاء الجلسة، وانتهاؤها، وكل عنصر له اسم، وكل جدول له caption، ولا معرّف مكرر، ولا خطأ في الصفحة.

## العمل المعلّق

في [task.md](./task.md). وبعد كل تعديل في السكربت: `clasp push` ثم `clasp deploy -i` بمعرّف النشر نفسه.
