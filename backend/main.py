# main.py
from datetime import datetime, timedelta
import os
import http
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import APIRouter


from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["cozy-vitality-production.up.railway.app"],  # 設定允許的來源
    allow_credentials=True,
    allow_methods=["*"],  # 允許的 HTTP 方法
    allow_headers=["*"],  # 允許的 HTTP 標頭
)

api_router = APIRouter()

# 設置緩存及有效期
memory_cache = {
    "holiday_data": {"data": None, "last_updated": None},
    "party_world_data": {"data": None, "last_updated": None}
}

CACHE_EXPIRATION = timedelta(days=1)  # 緩存有效期設定為 1 天


def fetch_with_memory_cache(key, fetch_func):
    now = datetime.now()

    # 如果緩存未過期，直接返回
    if (
        memory_cache[key]["data"]
        and memory_cache[key]["last_updated"]
        and now - memory_cache[key]["last_updated"] < CACHE_EXPIRATION
    ):
        return memory_cache[key]["data"]

    # 緩存過期或不存在時，重新爬取並更新
    data = fetch_func()
    memory_cache[key]["data"] = data
    memory_cache[key]["last_updated"] = now
    return data

def format_dates(raw_data: str) -> list:
    """
    將原始的日期資料進行格式化。
    """
    if not raw_data:
        return []

    # 使用 "、" 拆分資料
    parts = raw_data.split("、")
    result = []

    for part in parts:
        # 根據每段的長度進行處理
        if len(part) <= 2:
            result.append(part)
        else:
            # 長度超過 2 的部分進一步拆分，每 2 位為一組
            sub_parts = [part[i:i+2] for i in range(0, len(part), 2)]
            result.extend(sub_parts)

    return result

def process_member_dates(member_date_raw: list) -> list:
    """
    處理會員日資料，確保每月僅有一個條目，並正規化日期格式。
    """
    formatted_dates = []
    for raw_date in member_date_raw[:12]:  # 僅取前 12 個欄位（對應 12 個月）
        formatted = format_dates(raw_date)
        # 合併日期清單成一個字串，使用 "、" 分隔，例如: ["1", "8", "15"] -> "1、8、15"
        formatted_dates.append("、".join(formatted))

    return formatted_dates

def holiday_table():
    try:
        response = requests.get("https://www.holiday.com.tw/act/member/index.aspx")
        response.raise_for_status()  # 如果有錯誤會拋出例外
        soup = BeautifulSoup(response.content, "html.parser")

        tables = soup.find_all("div", class_="table-responsive component")
        if not tables:
            raise ValueError("未找到表格")

        result = []

        # 迭代每個表格
        for table_div in tables:
            table = table_div.find("table")
            if not table:
                continue

            # 提取地區名稱（表格標題）
            area_header = table.find("thead").find("tr").find("th")
            area_name = area_header.get_text(strip=True) if area_header else "未知地區"

            # 初始化地區的詳細數據
            area_details = []

            # 提取表格內容
            tbody = table.find("tbody")
            rows = tbody.find_all("tr") if tbody else []

            for row in rows:
                cells = row.find_all("td")
                if not cells:
                    continue

                # 提取商店名稱和月份數據
                store_name = row.find("th").get_text(strip=True)  # 商店名稱
                raw_dates = [cell.get_text(strip=True).replace("\n", ",") for cell in cells]
                member_date = [" , ".join(format_dates(d)) for d in raw_dates]  # 格式化處理日期

                # 保存該商店的數據
                area_details.append({
                    "store": store_name,
                    "member_date": member_date
                })

            # 將地區和詳細數據添加到結果
            result.append({
                "area": area_name,
                "details": area_details
            })

        # 返回結果
        return result
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")

def party_world_table():
    try:
        response = requests.get("https://www.cashboxparty.com/act/ktv/20200904/")
        response.raise_for_status()

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.content, "html.parser")

        tables = soup.find_all("table", class_="ps-table--vendor")
        result = {
            "2024": [],
            "2025": []
        }

        for table in tables:
            tbody = table.find("tbody")
            rows = tbody.find_all("tr") if tbody else []

            thead = table.find("thead")
            header_cells = thead.find_all("th") if thead else []

            year_indices = {}
            for index, cell in enumerate(header_cells):
                year = cell.get_text(strip=True).replace("\n", "").replace(" ", "")
                if "2024年" in year:
                    year_indices["2024"] = index
                elif "2025年" in year:
                    year_indices["2025"] = index

            if not year_indices:
                raise ValueError("未找到 2024 年或 2025 年的資料欄位")

            for row in rows:
                cells = row.find_all("td")
                if not cells:
                    continue

                store_name = cells[0].get_text(strip=True)  # 第一列為商店名稱

                # 提取每個年份的資料
                for year, index in year_indices.items():
                    if index < len(cells):  # 確保索引有效
                        member_date_raw = [
                            cell.get_text(strip=True).replace("\n", ",").replace("<br>", ",")
                            for cell in cells[1:]  # 修改成從第二列開始提取資料
                        ]
                        # 處理並格式化會員日資料
                        member_date = process_member_dates(member_date_raw)

                        # 確保年份鍵存在於結果字典中
                        if year not in result:
                            result[year] = []

                        result[year].append({
                            "store": store_name,
                            "member_date": member_date
                        })

        return result
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"HTTP 請求失敗: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"資料爬取失敗: {e}")

@api_router.post("/")
def read_root():
    return JSONResponse(content={"message": "Hello World"}, status_code=http.HTTPStatus.OK)

@api_router.get("/holiday_data")
def get_holiday():
    return fetch_with_memory_cache("holiday_data", holiday_table)

@api_router.get("/party_world_data")
def get_party_world():
    return fetch_with_memory_cache("party_world_data", party_world_table)


app.include_router(api_router, prefix="/api")

# app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # 動態取得 Railway 分配的埠號
    port = int(os.environ.get("PORT", 8000))
    print(f"Running on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

