from flask import Blueprint, jsonify
from bs4 import BeautifulSoup
from curl_cffi import requests
import os
import traceback

home_bp = Blueprint('home', __name__)

TARGET_URL = 'https://web1.mgkomik.cc/'

@home_bp.route('/', methods=['GET'])
def get_home():
    try:
        # Ambil proxy dari environment variable
        proxy_url = os.getenv('PROXY_URL')
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None

        # Debug log (bisa dilihat di Vercel Logs)
        print(f"[DEBUG] Proxy aktif: {'YES' if proxies else 'NO'}")
        print(f"[DEBUG] Target URL: {TARGET_URL}")

        # Request ke target pakai curl_cffi + proxy
        response = requests.get(
            TARGET_URL,
            impersonate="chrome110",
            proxies=proxies,
            timeout=30
        )

        print(f"[DEBUG] Status Code: {response.status_code}")
        print(f"[DEBUG] Content-Length: {len(response.text)}")

        if response.status_code != 200:
            return jsonify({
                "status": False,
                "message": f"Gagal fetch data, HTTP Status: {response.status_code}",
                "body_preview": response.text[:300] if hasattr(response, 'text') else "no text"
            }), response.status_code

        soup = BeautifulSoup(response.text, 'html.parser')

        projectUpdate = []
        komikUpdate = []
        trending = []

        # 1. Project Update
        for el in soup.select('.project-grid .project-card'):
            chapters = []
            for chapEl in el.select('.project-chapter-row'):
                capsule = chapEl.select_one('.project-chapter-capsule')
                date_el = chapEl.select_one('.project-chapter-date')
                chapters.append({
                    "chapter": capsule.text.strip() if capsule else "",
                    "url": capsule['href'] if capsule else "",
                    "date": date_el.text.strip() if date_el else ""
                })

            title_el = el.select_one('.project-title')
            cover_el = el.select_one('.project-cover')
            status_el = el.select_one('.manga-status-badge')
            flag_el = el.select_one('.flag-badge img')

            projectUpdate.append({
                "title": title_el.text.strip() if title_el else "",
                "slug": el.get('data-slug', ''),
                "cover": cover_el['src'] if cover_el else "",
                "status": status_el.text.strip() if status_el else "",
                "type_flag": flag_el['alt'] if flag_el else "",
                "chapters": chapters
            })

        # 2. Komik Update
        for el in soup.select('.manga-grid .manga-card'):
            chapters = []
            for chapEl in el.select('.chapter-row'):
                capsule = chapEl.select_one('.chapter-capsule')
                date_el = chapEl.select_one('.chapter-date')
                chapters.append({
                    "chapter": capsule.text.strip() if capsule else "",
                    "url": capsule['href'] if capsule else "",
                    "date": date_el.text.strip() if date_el else ""
                })

            title_el = el.select_one('.manga-title')
            cover_el = el.select_one('.manga-cover')
            status_el = el.select_one('.manga-status-badge')
            flag_el = el.select_one('.flag-badge img')

            komikUpdate.append({
                "title": title_el.text.strip() if title_el else "",
                "slug": el.get('data-slug', ''),
                "cover": cover_el['src'] if cover_el else "",
                "status": status_el.text.strip() if status_el else "",
                "type_flag": flag_el['alt'] if flag_el else "",
                "chapters": chapters
            })

        # 3. Trending
        for el in soup.select('.trending-list .trending-item'):
            chapters = []
            for chapEl in el.select('.trending-chapter-item'):
                capsule = chapEl.select_one('.trending-chapter-link')
                date_el = chapEl.select_one('.trending-chapter-date')
                chapters.append({
                    "chapter": capsule.text.strip() if capsule else "",
                    "url": capsule['href'] if capsule else "",
                    "date": date_el.text.strip() if date_el else ""
                })

            title_el = el.select_one('.trending-title')
            cover_el = el.select_one('.trending-cover')

            trending.append({
                "title": title_el.text.strip() if title_el else "",
                "url": title_el['href'] if title_el else "",
                "cover": cover_el['src'] if cover_el else "",
                "chapters": chapters
            })

        return jsonify({
            "status": True,
            "message": "Berhasil mengambil data home",
            "data": {
                "projectUpdate": projectUpdate,
                "komikUpdate": komikUpdate,
                "trending": trending
            }
        })

    except Exception as e:
        print(f"[DEBUG] ERROR: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "status": False,
            "message": "Gagal scraping data",
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

