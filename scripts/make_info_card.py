import os

svg_content = """<svg xmlns="http://www.w3.org/2000/svg" width="490" height="280">
  <defs>
    <style>
      .bg { fill: #0b0c10; stroke: #FF0055; stroke-width: 1px; rx: 8px; }
      .text { font-family: Consolas, Monaco, 'Courier New', monospace; font-size: 14px; }
      .title { fill: #00FFCC; font-weight: bold; }
      .sep { fill: #FF0055; }
      .key { fill: #FF0055; }
      .val { fill: #FFFFFF; }
      
      .line {
        opacity: 0;
        animation: fadeSlide 0.5s ease-out forwards;
      }
      
      @keyframes fadeSlide {
        from {
          opacity: 0;
          transform: translateY(-5px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }
      
      .l0 { animation-delay: 0.0s; }
      .l1 { animation-delay: 0.15s; }
      .l2 { animation-delay: 0.30s; }
      .l3 { animation-delay: 0.45s; }
      .l4 { animation-delay: 0.60s; }
      .l5 { animation-delay: 0.75s; }
      .l6 { animation-delay: 0.90s; }
      .l7 { animation-delay: 1.05s; }
    </style>
  </defs>

  <rect width="100%" height="100%" class="bg" />

  <g transform="translate(20, 40)" class="text">
    <g class="line l0"><text class="title">amar57603@github</text></g>
    <g class="line l1" transform="translate(0, 20)"><text class="sep">─────────────────────</text></g>
    
    <g class="line l2" transform="translate(0, 50)">
      <text class="key">Role</text>
      <text class="val" x="65">Final-year CS &amp; AI @ UTeM</text>
    </g>
    <g class="line l3" transform="translate(0, 80)">
      <text class="key">Focus</text>
      <text class="val" x="65">Machine Learning, Data Science</text>
    </g>
    <g class="line l4" transform="translate(0, 110)">
      <text class="key">Stack</text>
      <text class="val" x="65">Python · PyTorch · TensorFlow · React · Next.js</text>
    </g>
    <g class="line l5" transform="translate(0, 140)">
      <text class="key">Cloud</text>
      <text class="val" x="65">GCP · Cloudflare · Supabase · Upstash</text>
    </g>
    <g class="line l6" transform="translate(0, 170)">
      <text class="key">Tools</text>
      <text class="val" x="65">Arduino · Raspberry Pi · Linux</text>
    </g>
    <g class="line l7" transform="translate(0, 200)">
      <text class="key">Editor</text>
      <text class="val" x="65">VS Code</text>
    </g>
  </g>
</svg>
"""

# Output to root directory which is one level up from scripts
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
output_path = os.path.join(root_dir, 'info-card.svg')

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(svg_content)
    
print(f"Generated info-card.svg at {output_path}")
