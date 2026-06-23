from PIL import Image
import numpy as np
from collections import deque

TARGET = (61, 32, 48)   # #3d2030 — deep plum cible
TOLERANCE = 45

def color_dist(a, b):
    return np.sqrt(sum((int(a[i]) - int(b[i]))**2 for i in range(3)))

def flood_fill(data, seeds, bg_color, tol):
    h, w = data.shape[:2]
    visited = np.zeros((h, w), dtype=bool)
    mask = np.zeros((h, w), dtype=bool)
    queue = deque()
    for sy, sx in seeds:
        if 0 <= sy < h and 0 <= sx < w and not visited[sy, sx]:
            queue.append((sy, sx))
            visited[sy, sx] = True
    while queue:
        y, x = queue.popleft()
        if color_dist(data[y, x], bg_color) < tol:
            mask[y, x] = True
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                ny, nx = y+dy, x+dx
                if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                    visited[ny, nx] = True
                    queue.append((ny, nx))
    return mask

agents = ['general', 'commercial', 'marketing', 'recrutement', 'support', 'facturation']

for agent in agents:
    path = f'assets/agents/agent-ia-{agent}.png'
    img = Image.open(path).convert('RGB')
    data = np.array(img)
    h, w = data.shape[:2]

    # Sample bg from top-right zone (above title text, right of character)
    zone_y = int(h * 0.06)
    zone_x = int(w * 0.72)
    bg_color = tuple(data[zone_y, zone_x].tolist())

    # Seeds: multiple background anchor points
    seeds = [
        (int(h*0.06), int(w*0.72)),
        (int(h*0.06), int(w*0.85)),
        (int(h*0.95), int(w*0.72)),
        (int(h*0.95), int(w*0.85)),
        (int(h*0.5),  int(w*0.92)),
        (int(h*0.06), int(w*0.5)),
    ]

    mask = flood_fill(data, seeds, bg_color, TOLERANCE)

    data[mask] = TARGET

    result = Image.fromarray(data.astype(np.uint8))
    result.save(path)
    bg_hex = '#{:02x}{:02x}{:02x}'.format(*bg_color)
    pct = mask.sum() / (h*w) * 100
    print(f'✓ {agent:15} bg={bg_hex}  pixels remplacés={pct:.1f}%')
