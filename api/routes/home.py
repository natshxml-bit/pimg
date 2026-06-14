from flask import Blueprint, jsonify
from bs4 import BeautifulSoup
import cloudscraper

# Bikin router (Blueprint)
home_bp = Blueprint('home', __name__)

TARGET_URL = 'https://web1.mgkomik.cc/'

@home_bp.route('/', methods=['GET'])
def get_home():
    try:
        # Bikin scraper buat nembus Cloudflare
        scraper = cloudscraper.create_scraper(browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        })
        
        # Fetch HTML
        response = scraper.get(TARGET_URL)
        
        if response.status_code != 200:
            return jsonify({
                "status": False,
                "message": f"Gagal fetch data, HTTP Status: {response.status_code}"
            }), response.status_code

        soup = BeautifulSoup(response.text, 'html.parser')
        
        projectUpdate = []
        komikUpdate = []
        trending = []

        # 1. Scraping Section: Project Update
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

        # 2. Scraping Section: Komik Update
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

        # 3. Scraping Section: Komik Trending
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
        return jsonify({
            "status": False,
            "message": "Gagal scraping data",
            "error": str(e)
        }), 500
