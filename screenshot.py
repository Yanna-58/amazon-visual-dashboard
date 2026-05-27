import asyncio
from playwright.async_api import async_playwright
import os

OUTPUT_DIR = r"c:\Users\Administrator\Desktop\亚马逊看板_资源包\软著申请材料"
HTML_FILE = r"file:///c:/Users/Administrator/Desktop/亚马逊看板_资源包/亚马逊视觉数据看板_v3.2(最新版).html"

async def take_screenshots():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1400, "height": 900})

        # Step 1: Homepage
        await page.goto(HTML_FILE, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "step1_homepage.png"))
        print("Step 1: Homepage done")

        # Step 2: Data import page
        try:
            import_btn = await page.query_selector('text=数据导入')
            if import_btn:
                await import_btn.click()
                await asyncio.sleep(1)
                await page.screenshot(path=os.path.join(OUTPUT_DIR, "step2_import.png"))
                print("Step 2: Import page done")
        except Exception as e:
            print(f"Step 2 error: {e}")

        # Step 3: Dashboard (click dashboard tab)
        try:
            dash_tab = await page.query_selector('text=新品追踪') or await page.query_selector('[data-tab="dashboard"]')
            if dash_tab:
                await dash_tab.click()
                await asyncio.sleep(1)
            else:
                # Try clicking by text
                tabs = await page.query_selector_all('a, button, [role="tab"]')
                for tab in tabs:
                    text = await tab.inner_text()
                    if '新品' in text or 'Dashboard' in text or '总览' in text:
                        await tab.click()
                        await asyncio.sleep(1)
                        break
            await page.screenshot(path=os.path.join(OUTPUT_DIR, "step3_dashboard.png"))
            print("Step 3: Dashboard done")
        except Exception as e:
            print(f"Step 3 error: {e}")
            
        # Step 4: Products page
        try:
            prod_tab = await page.query_selector('text=产品总览') or await page.query_selector('[data-tab="products"]')
            if not prod_tab:
                tabs = await page.query_selector_all('a, button, [role="tab"]')
                for tab in tabs:
                    text = await tab.inner_text()
                    if '产品' in text or 'Products' in text or 'ASIN' in text:
                        await tab.click()
                        await asyncio.sleep(1)
                        break
            else:
                await prod_tab.click()
                await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUTPUT_DIR, "step4_products.png"))
            print("Step 4: Products done")
        except Exception as e:
            print(f"Step 4 error: {e}")

        # Step 5: Comparison/优化对比 page
        try:
            comp_tab = await page.query_selector('text=优化对比') or await page.query_selector('[data-tab="compare"]')
            if not comp_tab:
                tabs = await page.query_selector_all('a, button, [role="tab"]')
                for tab in tabs:
                    text = await tab.inner_text()
                    if '优化' in text or '对比' in text or 'Compare' in text:
                        await tab.click()
                        await asyncio.sleep(1)
                        break
            else:
                await comp_tab.click()
                await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUTPUT_DIR, "step5_compare.png"))
            print("Step 5: Compare done")
        except Exception as e:
            print(f"Step 5 error: {e}")

        # Step 6: Full page screenshot for overview
        await page.goto(HTML_FILE, wait_until="networkidle")
        await asyncio.sleep(1)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "step6_fullpage.png"), full_page=True)
        print("Step 6: Full page done")

        await browser.close()
        print("All screenshots saved to:", OUTPUT_DIR)

asyncio.run(take_screenshots())
