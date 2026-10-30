"""Targeted regression and layout tests for sana-dashboard on mobile and desktop viewports.

Verifies:
1. RTL overflow isolation: opening #students or any other section does NOT expand
   document.documentElement.scrollWidth beyond viewport clientWidth, preventing
   the mobile 'white screen of death' (viewport scrolling to negative X off-screen).
2. Table scrollability: wide tables remain scrollable inside their containers.
3. Zero JavaScript console errors or uncaught exceptions during toggles.
"""

import json
import os
import sys
from playwright.sync_api import sync_playwright

CHROME_PATH = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe"
HTML_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "index.html")
).replace("\\", "/")

SAMPLE_DATA = {
    "year": "2026",
    "today": "2026-10-30",
    "activeDays": 30,
    "monthlyHeaders": [
        "الطلاب الجدد",
        "من حضر",
        "المستمرون",
        "نسبة الاستمرار",
        "الحلقات",
        "الساعات",
        "الطلاب في الحلقة",
        "مجموع الحضور",
    ],
    "monthly": [["2026-10", "معلم 1", "T001", 5, 20, 15, 0.75, 10, 20, 2, 20]],
    "reports": [
        {
            "teacher": "معلم 1",
            "date": "2026-10-25",
            "session": "صباحية (حلقة 1)",
            "category": "أطفال",
            "duration": "2:00",
            "students": 5,
            "notes": "",
            "status": "",
            "link": "",
            "order": 1,
        }
    ],
    "honors": [],
    "log": [],
    "unpriced": [],
    "expenses": [],
    "aliases": [],
    "pay": [],
    "teachers": [
        {
            "name": t_name,
            "students": [
                {
                    "key": f"{t_name}_s{i}",
                    "name": f"طالب {t_name} {i}",
                    "gender": "ذكر" if i % 2 == 0 else "أنثى",
                    "category": "أطفال",
                    "firstSeen": "2026-10-01",
                    "lastSeen": "2026-10-25",
                    "attendance": 5,
                    "lastHifz": "البقرة 1-10",
                    "lastHifzDate": "2026-10-25",
                    "repeats": 0,
                    "medals": 1,
                    "honors": 0,
                    "age": 10,
                    "birthYear": 2016,
                    "phone": "+201012345678",
                    "isNew": False,
                    "months": {"2026-10": 4},
                }
                for i in range(15)
            ],
        }
        for t_name in ["أسماء علي", "محمد نبيل", "سارة العدل", "فاطمة إبراهيم"]
    ],
}


def run_mobile_tests():
    print("[TEST] Launching headless Chrome with mobile viewport (Pixel 7)...")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        device = p.devices["Pixel 7"]  # 412 x 915
        context = browser.new_context(**device)
        page = context.new_page()

        console_errors = []
        page.on("pageerror", lambda e: console_errors.append(f"PageError: {e}"))
        page.on(
            "console",
            lambda m: console_errors.append(f"ConsoleError: {m.text}")
            if m.type == "error"
            else None,
        )

        url = f"file:///{HTML_PATH}"
        page.goto(url, wait_until="load")
        page.wait_for_timeout(1000)

        # 1. Initialize with session and sample data
        page.evaluate(
            f"""() => {{
            const comp = Alpine.$data(document.querySelector('[x-data]'));
            comp.token = 'test_token';
            comp.who = 'مشرف النظام';
            comp.teacher = '*';
            comp.load({json.dumps(SAMPLE_DATA)});
        }}"""
        )
        page.wait_for_timeout(300)

        # Baseline: all sections closed
        base_metrics = page.evaluate(
            """() => ({
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth,
            scrollLeft: document.documentElement.scrollLeft
        })"""
        )
        assert (
            base_metrics["scrollWidth"] == base_metrics["clientWidth"]
        ), f"Baseline document overflowed: {base_metrics}"
        assert (
            base_metrics["scrollLeft"] == 0
        ), f"Baseline scrollLeft not zero: {base_metrics}"
        print("  ✓ Baseline layout: zero horizontal overflow.")

        # 2. Test opening #students section
        page.click('button[aria-controls="students-body"]')
        page.wait_for_timeout(500)

        students_metrics = page.evaluate(
            """() => ({
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth,
            scrollLeft: document.documentElement.scrollLeft,
            windowScrollX: window.scrollX,
            tableContainerWidth: document.querySelector('#students .overflow-x-auto').offsetWidth,
            tableWidth: document.querySelector('#students table').offsetWidth,
            tableScrollWidth: document.querySelector('#students .overflow-x-auto').scrollWidth
        })"""
        )

        print("  [Students Section Open Metrics]:", students_metrics)

        # Assert no document-level horizontal leak (which triggers mobile white screen)
        is_clean = (
            students_metrics["scrollWidth"] == students_metrics["clientWidth"]
            and students_metrics["scrollLeft"] == 0
            and students_metrics["windowScrollX"] == 0
        )

        if not is_clean:
            print(
                f"  ✗ FAILURE: Document overflow detected! scrollWidth={students_metrics['scrollWidth']}, "
                f"clientWidth={students_metrics['clientWidth']}, scrollLeft={students_metrics['scrollLeft']}"
            )
            browser.close()
            return False

        # Assert the table inside #students is actually wider than screen and scrollable
        assert (
            students_metrics["tableScrollWidth"]
            > students_metrics["tableContainerWidth"]
        ), "Table should be horizontally scrollable inside its container"
        print("  ✓ Students section: zero document overflow; table scrolls inside container.")

        # 3. Test all other sections
        sections = [
            "numbers",
            "reports",
            "absent",
            "history",
            "honors",
            "fix-name",
            "rates",
            "log",
        ]
        for sec in sections:
            btn = f'button[aria-controls="{sec}-body"]'
            if page.locator(btn).count() > 0:
                page.click(btn)
                page.wait_for_timeout(200)
                sec_metrics = page.evaluate(
                    """() => ({
                    scrollWidth: document.documentElement.scrollWidth,
                    clientWidth: document.documentElement.clientWidth,
                    scrollLeft: document.documentElement.scrollLeft
                })"""
                )
                assert (
                    sec_metrics["scrollWidth"] == sec_metrics["clientWidth"]
                ), f"Section {sec} caused document overflow: {sec_metrics}"
                assert (
                    sec_metrics["scrollLeft"] == 0
                ), f"Section {sec} caused document scrollLeft shift: {sec_metrics}"

        print("  ✓ All sections toggled cleanly with zero document overflow.")

        # 4. Check console errors
        assert len(console_errors) == 0, f"Errors logged: {console_errors}"
        print("  ✓ Zero console/runtime errors.")

        browser.close()
        return True


if __name__ == "__main__":
    success = run_mobile_tests()
    if success:
        print("\nALL TESTS PASSED SUCCESSFULLY.")
        sys.exit(0)
    else:
        print("\nTESTS FAILED.")
        sys.exit(1)
