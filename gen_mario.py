sprite = [
    ". . . R R R R R . . . .",
    ". . R R R R R R R R R .",
    ". . W W W S S W S . . .",
    ". W S W S S S W S S S .",
    ". W S W W S S S W S S S",
    ". W W S S S S W W W W .",
    ". . . S S S S S S S . .",
    ". . R R B R R R . . . .",
    ". R R R B R R B R R . .",
    "R R R R B B B B R R R R",
    "S S R B S B B S B R S S",
    "S S S B B B B B B S S S",
    "S S B B B B B B B B S S",
    ". . B B B . . B B B . .",
    ". W W W . . . . W W W .",
    "W W W W . . . . W W W W"
]

colors = {
    'R': '#FF0055', # Neon Pink
    'B': '#0055F6', # Classic Mario Blue
    'S': '#F6AC6B', # Skin tone
    'W': '#00FFCC', # Neon Cyan (Shoes/Hair) for Cyberpunk vibe!
}

# Generate SVG
pixel_size = 2
mario_width = 12 * pixel_size
mario_height = 16 * pixel_size

mario_group = f'<g id="mario">\n'
for y, row in enumerate(sprite):
    pixels = row.split()
    for x, p in enumerate(pixels):
        if p in colors:
            mario_group += f'  <rect x="{x*pixel_size}" y="{y*pixel_size}" width="{pixel_size}" height="{pixel_size}" fill="{colors[p]}" />\n'
mario_group += '</g>\n'

pipe = f'''
    <!-- Pipe (Cyan) -->
    <g transform="translate(400, 10)">
        <rect x="0" y="0" width="40" height="15" fill="#00FFCC" rx="2" />
        <rect x="5" y="15" width="30" height="15" fill="#00FFCC" />
        <!-- Highlights -->
        <rect x="5" y="2" width="5" height="11" fill="#FFFFFF" opacity="0.5" />
        <rect x="10" y="15" width="5" height="15" fill="#FFFFFF" opacity="0.5" />
    </g>
'''

svg = f'''<svg width="800" height="40" viewBox="0 0 800 40" xmlns="http://www.w3.org/2000/svg">
    <style>
        .scene {{
            animation: move-scene 8s linear infinite;
        }}
        @keyframes move-scene {{
            0% {{ transform: translateX(-50px); }}
            100% {{ transform: translateX(850px); }}
        }}
        .mario-jump {{
            animation: jump 8s linear infinite;
        }}
        @keyframes jump {{
            0%, 45% {{ transform: translateY(10px); }}
            48% {{ transform: translateY(-15px); }}
            52% {{ transform: translateY(-15px); }}
            55%, 100% {{ transform: translateY(10px); }}
        }}
    </style>
    
    <!-- Ground Line -->
    <rect x="0" y="38" width="800" height="2" fill="#FF0055" />
    <rect x="0" y="35" width="800" height="1" fill="#00FFCC" opacity="0.5" />

    {pipe}

    <g class="scene">
        <g class="mario-jump">
            {mario_group}
        </g>
    </g>
</svg>
'''

with open("assets/mario.svg", "w", encoding="utf-8") as f:
    f.write(svg)
