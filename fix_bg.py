from PIL import Image
import numpy as np

TARGET = np.array([61, 32, 48])  # #3d2030 deep plum
THRESHOLD = 55

agents = ['general', 'commercial', 'marketing', 'recrutement', 'support', 'facturation']

for agent in agents:
    path = f'assets/agents/agent-ia-{agent}.png'
    img = Image.open(path).convert('RGB')
    data = np.array(img, dtype=np.int32)

    # Sample bg color from multiple corners/edges (avoid character area)
    samples = [
        data[0, 0], data[0, -1], data[-1, 0], data[-1, -1],
        data[0, data.shape[1]//2], data[-1, data.shape[1]//2],
        data[data.shape[0]//2, 0], data[data.shape[0]//2, -1],
    ]
    bg_color = np.median(samples, axis=0).astype(int)

    diff = data - bg_color
    dist = np.sqrt(np.sum(diff**2, axis=2))
    mask = dist < THRESHOLD

    # Replace background pixels
    data[mask] = TARGET

    result = Image.fromarray(data.astype(np.uint8))
    result.save(path)
    print(f'✓ {agent} — bg détecté: rgb{tuple(bg_color)} → #3d2030')
