import datetime, json, os, re, sys
import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get('GH_PROFILE_USER', 'amar57603')
URL = f'https://github.com/users/{USERNAME}/contributions'
OUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'contributions.json')

def fetch_days():
    resp = requests.get(URL, headers={'User-Agent': 'profile-readme-bot/1.0'}, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    cells = soup.select('td.ContributionCalendar-day')
    if not cells:
        print('no calendar cells found', file=sys.stderr)
        sys.exit(1)
    days = []
    for td in cells:
        date = td.get('data-date')
        if not date: continue
        td_id = td.get('id')
        tooltip_el = soup.find('tool-tip', attrs={'for': td_id}) if td_id else None
        text = tooltip_el.get_text(strip=True) if tooltip_el else ''
        if re.search(r'no contributions', text, re.I):
            count = 0
        else:
            m = re.match(r'(\d+)', text)
            count = int(m.group(1)) if m else 0
        days.append({'date': date, 'count': count})
    days.sort(key=lambda d: d['date'])
    return days

def compute_current_streak(days):
    streak = 0
    for day in reversed(days):
        if day['count'] > 0:
            streak += 1
        else:
            break
    return streak

def compute_longest_streak(days):
    longest = 0
    current = 0
    for day in days:
        if day['count'] > 0:
            current += 1
            if current > longest:
                longest = current
        else:
            current = 0
    return longest

def compute_stats(days):
    total = sum(d['count'] for d in days)
    current_streak = compute_current_streak(days)
    longest_streak = compute_longest_streak(days)
    best_day = ''
    best_count = 0
    for d in days:
        if d['count'] > best_count:
            best_count = d['count']
            best_day = d['date']
    return {
        'total': total,
        'current_streak': current_streak,
        'longest_streak': longest_streak,
        'best_day': best_day,
        'best_count': best_count
    }

def main():
    days = fetch_days()
    stats = compute_stats(days)
    
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, 'w') as f:
        json.dump({'days': days, 'stats': stats}, f, indent=2)
    print(f"Saved contributions for {USERNAME} to {OUT_PATH}")

if __name__ == '__main__':
    main()
