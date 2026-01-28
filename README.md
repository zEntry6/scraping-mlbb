# Mobile Legends Heroes Scraper 🎮

Web scraper untuk mengambil data heroes Mobile Legends lengkap dengan skills, win/pick/ban rates, combos, dan counter information.

## Features ✨

- ✅ Scrape **131 heroes** dengan data lengkap
- ✅ **Win Rate, Pick Rate, Ban Rate** untuk setiap hero
- ✅ **782+ skills** dengan deskripsi lengkap, type, dan cooldown
- ✅ **Skill combinations** untuk setiap hero
- ✅ **Counter data** untuk 6 heroes terbaru (limitasi dari Mobile Legends API)
- ✅ Web interface modern untuk melihat data
- ✅ REST API endpoints

## Screenshots

![Web Interface](docs/screenshot.png)

## Tech Stack 🛠️

- **Python 3.13+**
- **Patchright/Playwright** - Browser automation untuk scraping dynamic content
- **Flask** - Web framework untuk REST API dan UI
- **SQLite** - Database storage
- **Beautiful Soup** - HTML parsing (tidak dipakai lagi, diganti browser automation)

## Installation 📦

1. Clone repository:
```bash
git clone https://github.com/yourusername/scraping-mlbb.git
cd scraping-mlbb
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Chromium browser untuk Playwright:
```bash
python -m playwright install chromium
```

## Usage 🚀

### 1. Scraping Data

Jalankan scraper untuk mengambil semua data heroes:

```bash
python main.py
```

Proses ini akan:
- Scrape list semua heroes (131 heroes)
- Scrape detail setiap hero (skills, rates, counter)
- Menyimpan ke database `mlbb.db`
- Estimasi waktu: ~25-30 menit

### 2. Menjalankan Web Interface

Jalankan Flask web server:

```bash
python web_app.py
```

Buka browser: **http://127.0.0.1:5000**

### 3. Melihat Summary Data

```bash
python final_summary.py
```

Output:
```
✅ 1. HEROES: 131 heroes
✅ 2. RATES: 131 heroes (Win Rate, Pick Rate, Ban Rate)
✅ 3. SKILLS: 782 skills dari 131 heroes
✅ 4. COMBOS: 131 skill combinations
⚠️  5. COUNTER DATA: 6 heroes (newest heroes only)
```

### 4. Show Sample Data

```bash
python show_results.py
```

## Project Structure 📁

```
scraping-mlbb/
├── main.py                 # Main orchestration script
├── web_app.py             # Flask web application
├── final_summary.py       # Display data statistics
├── show_results.py        # Show sample heroes data
├── requirements.txt       # Python dependencies
├── mlbb.db               # SQLite database (generated)
│
├── config/               # Configuration
│   ├── constants.py      # Constants and URLs
│   └── settings.py       # Settings
│
├── fetchers/            # API fetchers
│   ├── hero_fetcher.py  # Fetch heroes list from API
│   └── rank_fetcher.py  # Fetch rank data
│
├── scrapers/            # Web scrapers
│   ├── hero_list_scraper.py    # Scrape heroes list
│   ├── hero_detail_scraper.py  # Scrape hero details
│   └── rank_scraper.py         # Scrape rank data
│
├── parsers/             # Data parsers
│   ├── hero_parser.py   # Parse hero data
│   └── rank_parser.py   # Parse rank data
│
├── storage/             # Database layer
│   ├── db.py           # Database schema
│   ├── hero_repo.py    # Hero repository
│   ├── meta_repo.py    # Meta repository
│   └── rank_repo.py    # Rank repository
│
├── utils/              # Utilities
│   ├── helpers.py      # Helper functions
│   └── logger.py       # Logging setup
│
└── templates/          # Web templates
    └── index.html      # Main web interface
```

## Database Schema 🗄️

### `heroes`
- `heroid` (INTEGER PRIMARY KEY)
- `name` (TEXT)
- `role` (TEXT)
- `channelid` (TEXT)

### `hero_details`
- `heroid` (INTEGER PRIMARY KEY)
- `win_rate` (REAL)
- `pick_rate` (REAL)
- `ban_rate` (REAL)
- `counters` (TEXT) - Heroes yang di-counter
- `countered_by` (TEXT) - Heroes yang meng-counter
- `synergy` (TEXT) - Heroes yang cocok

### `hero_skills`
- `id` (INTEGER PRIMARY KEY)
- `heroid` (INTEGER)
- `skill_name` (TEXT)
- `skill_desc` (TEXT)
- `skill_type` (TEXT)
- `cooldown` (TEXT)

### `hero_combos`
- `heroid` (INTEGER PRIMARY KEY)
- `combo` (TEXT)

## API Endpoints 🔌

### Get All Heroes
```
GET /api/heroes
```

Response:
```json
[
  {
    "heroid": 131,
    "name": "Sora",
    "role": "fighter, assassin",
    "win_rate": 33.47,
    "pick_rate": 81.40,
    "ban_rate": 66.78,
    "skills": [...],
    "combo": "..."
  }
]
```

### Get Single Hero
```
GET /api/hero/<heroid>
```

### Get Statistics
```
GET /api/stats
```

Response:
```json
{
  "total_heroes": 131,
  "total_skills": 782,
  "total_combos": 131,
  "heroes_with_counter": 6
}
```

## Web Features 🌐

- 🔍 **Search** - Cari heroes by name
- 🎯 **Filter** - Filter by role (Tank, Fighter, Assassin, Mage, Marksman, Support)
- 📊 **Statistics** - Dashboard dengan statistik lengkap
- 🃏 **Hero Cards** - Preview hero dengan rates dan skills
- 📖 **Detail Modal** - Full information dengan all skills, combos, counter data

## Known Limitations ⚠️

1. **Counter Data**: Hanya tersedia untuk 6 heroes terbaru (126-131)
   - Alasan: Mobile Legends official API hanya provide data untuk heroes terbaru
   - Heroes: Suyou, Lukas, Kalea, Zetian, Obsidia, Sora

2. **Scraping Time**: Full scrape memakan waktu ~25-30 menit
   - Browser automation per hero membutuhkan waktu
   - Wait time untuk load dynamic content

3. **Rate Limiting**: Jangan scrape terlalu sering
   - Gunakan data yang sudah di-scrape
   - Re-scrape only when necessary

## Development Notes 🔧

### Counter Data Issue
Counter data extraction menggunakan browser automation dengan network interception:
- API endpoint: `https://api.gms.moontontech.com/api/gms/source/2669606/2756564`
- Intercept via `page.on("response")` listener
- Parse relation object: `strong`, `weak`, `assist`

### Skills Extraction
Skills extraction menggunakan:
- Regex pattern untuk extract dari HTML
- Priority-based filtering (hero name prioritized)
- Expanded keywords detection
- Max 6 skills per hero

### Why Browser Automation?
- Skills loaded dynamically via JavaScript
- Counter data only available via API interception
- HTML scraping tidak sufficient untuk dynamic content

## Contributing 🤝

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License 📄

This project is licensed under the MIT License.

## Disclaimer ⚖️

This scraper is for **educational purposes only**. Pastikan untuk:
- Follow Mobile Legends Terms of Service
- Don't overload their servers
- Use data responsibly
- Rate limit your requests

## Credits 👏

Data source: [Mobile Legends Official Website](https://www.mobilelegends.com)

## Support ☕

If you find this useful, consider:
- ⭐ Star this repository
- 🐛 Report bugs
- 💡 Suggest features
- 🔀 Submit pull requests

---

Made with ❤️ for Mobile Legends community
