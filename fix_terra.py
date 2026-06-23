"""
Remap vivid orange-terracotta (#d46c47 avg) → #C75F62 on all 6 agent PNGs.
Skin tones are spared because they have lower saturation and less red-dominance.
"""
from PIL import Image
import numpy as np

# Target #C75F62 = rgb(199, 95, 98)
T_R, T_G, T_B = 199, 95, 98

agents = ['general', 'commercial', 'marketing', 'recrutement', 'support', 'facturation']

for agent in agents:
    path = f'assets/agents/agent-ia-{agent}.png'
    img = Image.open(path).convert('RGB')
    data = np.array(img, dtype=np.int32)

    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]

    # Vivid orange-terracotta detection:
    # - R very dominant (R > G*1.6 AND R > B*2.5)
    # - Saturation implied by channel ratio
    # - Not too dark (R > 140)
    # This captures the text/icon terracotta but NOT skin tones (skin has lower R/G ratio)
    mask = (
        (r > 140) &
        (r > (g * 1.55).astype(np.int32)) &
        (r > (b * 2.2).astype(np.int32)) &
        (g < 160) &
        (b < 130)
    )

    n = mask.sum()
    if n == 0:
        print(f'{agent}: no pixels matched')
        continue

    # Per-pixel brightness factor relative to target brightness (199 = T_R)
    src_r = data[:,:,0].astype(np.float32)
    src_g = data[:,:,1].astype(np.float32)
    src_b = data[:,:,2].astype(np.float32)
    src_brightness = src_r  # R is max for terracotta pixels → use as brightness reference

    avg_src_r = float(src_r[mask].mean())
    bf = src_brightness / (avg_src_r if avg_src_r > 0 else 1.0)  # brightness factor

    new_r = np.clip(T_R * bf, 40, 255).astype(np.int32)
    new_g = np.clip(T_G * bf, 20, 180).astype(np.int32)
    new_b = np.clip(T_B * bf, 20, 180).astype(np.int32)

    data[:,:,0] = np.where(mask, new_r, data[:,:,0])
    data[:,:,1] = np.where(mask, new_g, data[:,:,1])
    data[:,:,2] = np.where(mask, new_b, data[:,:,2])

    result = Image.fromarray(data.astype(np.uint8))
    result.save(path)

    avg_after = data[mask].mean(axis=0)
    print(f'✓ {agent:15}  {n:6} px → avg after=#{int(avg_after[0]):02x}{int(avg_after[1]):02x}{int(avg_after[2]):02x}')
