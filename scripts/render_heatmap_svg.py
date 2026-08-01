import json
import os
from datetime import datetime

PALETTE = ['#0b0c10', '#0a2a2a', '#003d3d', '#00805a', '#00CCAA', '#00FFCC']
CELL = 12
GAP = 3
STEP = CELL + GAP

BG_COLOR = '#0b0c10'
TEXT_COLOR = '#FFFFFF'
ACCENT_COLOR = '#00FFCC'
MUTED_COLOR = '#7d8590'
FRAME_COLOR = '#FF0055'

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'contributions.json')
OUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'contrib-heatmap.svg')

COL_T = 0.018
ROW_T = 0.045
CELL_DUR = 0.42

def level_for(count):
    if count == 0: return 0
    if count <= 5: return 1
    if count <= 15: return 2
    if count <= 30: return 3
    if count <= 50: return 4
    return 5

def main():
    with open(DATA_PATH, 'r') as f:
        data = json.load(f)
    
    days = data['days']
    stats = data['stats']
    
    # Render SVG
    svg_width = 800
    svg_height = 250
    
    svg = [f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(f'''
    <style>
      .bg {{ fill: {BG_COLOR}; }}
      .frame {{ stroke: {FRAME_COLOR}; stroke-width: 2; fill: none; }}
      .title {{ font-family: monospace; font-size: 14px; fill: {ACCENT_COLOR}; font-weight: bold; }}
      .text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 10px; fill: {TEXT_COLOR}; }}
      .muted {{ fill: {MUTED_COLOR}; }}
      .stats {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 12px; fill: {TEXT_COLOR}; font-weight: 500; }}
      .cell {{ opacity: 0; animation: fadeIn {CELL_DUR}s ease-in-out forwards; }}
      @keyframes fadeIn {{
        from {{ opacity: 0; transform: scale(0.8); }}
        to {{ opacity: 1; transform: scale(1); }}
      }}
    </style>
    ''')
    
    # Background and frame
    svg.append(f'<rect class="bg frame" x="1" y="1" width="{svg_width-2}" height="{svg_height-2}" rx="6" />')
    
    # Title
    svg.append(f'<text x="20" y="30" class="title">amar57603@github ~ $ ./contributions.sh</text>')
    
    # Calculate grid position
    grid_x = 40
    grid_y = 60
    
    # Day labels
    day_labels = ['Mon', 'Wed', 'Fri']
    for i, label in enumerate(day_labels):
        y = grid_y + (i * 2 + 1) * STEP + 10
        svg.append(f'<text x="{grid_x - 10}" y="{y}" class="text muted" text-anchor="end">{label}</text>')
    
    # Organize days into columns
    columns = []
    current_col = []
    
    for day in days:
        current_col.append(day)
        if len(current_col) == 7:
            columns.append(current_col)
            current_col = []
    if current_col:
        columns.append(current_col)
        
    # Keep only the last 53 columns to fit standard GitHub layout
    columns = columns[-53:]
    
    # Draw cells
    month_labels = []
    last_month = None
    
    for c_idx, col in enumerate(columns):
        x = grid_x + c_idx * STEP
        
        # Check for month change
        if col:
            first_day = col[0]['date']
            dt = datetime.strptime(first_day, '%Y-%m-%d')
            month = dt.strftime('%b')
            if month != last_month:
                month_labels.append((x, month))
                last_month = month
                
        for r_idx, day in enumerate(col):
            y = grid_y + r_idx * STEP
            level = level_for(day['count'])
            color = PALETTE[level]
            
            # Animation delay
            delay = c_idx * COL_T + r_idx * ROW_T
            
            svg.append(f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{color}" style="animation-delay: {delay}s;" />')
            
    # Draw month labels
    for x, month in month_labels:
        svg.append(f'<text x="{x}" y="{grid_y - 10}" class="text muted">{month}</text>')
        
    # Legend
    legend_x = grid_x + len(columns) * STEP - 100
    legend_y = grid_y + 7 * STEP + 15
    svg.append(f'<text x="{legend_x - 10}" y="{legend_y + 9}" class="text muted" text-anchor="end">Less</text>')
    for i, color in enumerate(PALETTE):
        svg.append(f'<rect x="{legend_x + i * STEP}" y="{legend_y}" width="{CELL}" height="{CELL}" rx="2" fill="{color}" />')
    svg.append(f'<text x="{legend_x + len(PALETTE) * STEP + 10}" y="{legend_y + 9}" class="text muted">More</text>')
    
    # Stats footer
    stats_y = svg_height - 20
    stats_text = (
        f"Total: <tspan fill='{ACCENT_COLOR}'>{stats['total']}</tspan>   "
        f"Current Streak: <tspan fill='{ACCENT_COLOR}'>{stats['current_streak']} days</tspan>   "
        f"Longest Streak: <tspan fill='{ACCENT_COLOR}'>{stats['longest_streak']} days</tspan>   "
        f"Best Day: <tspan fill='{ACCENT_COLOR}'>{stats['best_count']} ({stats['best_day']})</tspan>"
    )
    svg.append(f'<text x="20" y="{stats_y}" class="stats">{stats_text}</text>')
    
    svg.append('</svg>')
    
    with open(OUT_PATH, 'w') as f:
        f.write('\\n'.join(svg))
        
    print(f"Generated heatmap SVG at {OUT_PATH}")

if __name__ == '__main__':
    main()
