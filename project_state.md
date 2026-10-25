# حالة المشروع — sana-dashboard

**الإصدار:** `1.2.0`، منشور على GitHub (`kamalyaser31/sana-dashboard`، عام) وPages: https://kamalyaser31.github.io/sana-dashboard/، و`API_URL` يشير إلى النشر `AKfycbwxv2ue…` (النسخة 10).
**تاريخ التحديث:** `2026-10-24`

## البنية

- `index.html` وحده: Alpine.js 3.14.8 وTailwind 3.4.17 من CDN، RTL. منقول من `DashboardPage.html` في `sana-reports-automation` (المرحلة D3 من `PLAN_STUDENTS_SHEET.md` هناك، القرارات S-38…S-46).
- `call(action, args, done)` يرسل `{action, token, test, year, args}` إلى `API_URL` بـ `fetch` ونوع `text/plain`، والرد `{ok, data, outcome}` أو `{ok: false, error, auth}`؛ و`auth` يمحو الجلسة ويعيد قسم الدخول.
- الجلسة `{token, who}` في `sessionStorage` (`sana_dashboard_session`)، فتبقى بعد إعادة التحميل وتذهب بإغلاق التبويب.
- كل طالب يحمل `teacher`، والمفتاح `k(s)` = المعلم|المفتاح، لأن «كل المعلمين» يجمع طلاباً بالاسم نفسه عند معلمَين.
- معرّفات حقول الصفوف بترتيب الصف (`g-0`، `by-0`، `ph-0`)، لا بالمفتاح.
- قسم الرواتب: `data.payOpen` يختار بين استمارة «افتح الرواتب» (`unlockPay`) والجداول وزر «أقفل الرواتب» (`lockPay`)؛ و`payData()` يقبل `pay` فارغاً؛ و`focusSoon` ينقل المؤشر بعد أن يُظهر x-show العنصر.

## الاختبار

لا اختبار في المستودع. جُرّبت في Chromium بلا واجهة على `fetch` بديل (سكربت Playwright في مساحة العمل المؤقتة): الدخول الخطأ والصحيح، وانتقال المؤشر، وبقاء الجلسة، وانتهاؤها، وكل عنصر له اسم، وكل جدول له caption، ولا معرّف مكرر، ولا خطأ في الصفحة.

## العمل المعلّق

لا شيء. وبعد كل تعديل في السكربت: `clasp push` ثم `clasp deploy -i` بمعرّف النشر نفسه.
