# Run: python3 tools/build-voxel.py  -> regenerates assets/images/hero-voxel.svg
"""Original isometric voxel illustration for Pranay's hero (desk scene).
Pranay (teal sweater with white stripes, khaki trousers, glasses, beard)
sits at his desk designing a user flow on a laptop. Plant, mug, notebook,
sticky notes and a few floating building blocks."""
import colorsys, os, random
random.seed(11)
V = {}  # (x, y, z) -> hex colour.  Viewer looks from +x, +y, +z.
GLOW = set()  # voxels whose right face is drawn unshaded (the lit screen)

def box(x0, y0, z0, dx, dy, dz, c):
    for x in range(x0, x0 + dx):
        for y in range(y0, y0 + dy):
            for z in range(z0, z0 + dz):
                V[(x, y, z)] = c

def put(x, y, z, c): V[(x, y, z)] = c

# ---------- palette ----------
DARK = '#2B2B2B'; STEEL = '#3F4146'; WHITE = '#F7F7F5'; LINE = '#BDBDBD'
RED = '#E5383B'; BLUE = '#3D7BF7'; AMBER = '#F2B33D'; GREEN = '#2FA866'; PURPLE = '#7A5AF5'
TEAL = '#1F5566'; TEAL_D = '#18434F'; STRIPE = '#E9EEF2'
KHAKI = '#C9A77A'; KHAKI_D = '#B8955F'; SKIN = '#C48A60'; SKIN_D = '#A9714B'
HAIR = '#1D1916'; BEARD = '#2A2019'; SHOE = '#ECECEC'; SOLE = '#5A5A5A'
WOOD = '#E6C79C'; WOOD_D = '#D4B080'; POT = '#EFEDE8'
LEAF = '#5FAE4E'; LEAF_D = '#3E8A3A'; LEAF_L = '#8CCB5E'
CHAIR = '#34363B'; CHAIR_SEAT = '#4A4D55'

# ---------- desk (long side runs along y) ----------
DX, DY, DZ = 0, 0, 13          # top surface voxels at z = 13
box(DX, DY, DZ, 15, 27, 1, WOOD)
box(DX, DY, DZ - 1, 15, 27, 1, WOOD_D)           # thicker edge
for (x, y) in ((DX, DY), (DX + 14, DY), (DX, DY + 26), (DX + 14, DY + 26)):
    box(x, y, 0, 1, 1, DZ - 1, STEEL)
box(DX, DY, 0, 1, 27, 1, STEEL); box(DX + 14, DY, 0, 1, 1, 1, STEEL)  # floor rails
box(DX, DY + 26, 0, 15, 1, 1, STEEL)

# ---------- laptop (screen faces +x, towards the viewer's right) ----------
LX, LY0, LW = 3, 7, 13
box(LX + 1, LY0, 14, 7, LW, 1, '#C9CCD1')                # base / keyboard deck
box(LX + 3, LY0 + 2, 14, 3, LW - 4, 1, '#AEB2B9')       # keyboard area (slightly darker)
box(LX, LY0, 14, 1, LW, 11, '#3A3D42')                   # lid + bezel
SX = LX                                                  # screen pixels live on x = LX
def scr(u, v, c):  # u along y (0..LW-1), v up from z = 15
    put(SX, LY0 + u, 15 + v, c); GLOW.add((SX, LY0 + u, 15 + v))
for u in range(1, LW - 1):
    for v in range(1, 9): scr(u, v, '#F4F6F9')           # canvas
for v in range(1, 9): scr(1, v, '#2E3138')               # tool sidebar
for u in range(2, LW - 1): scr(u, 8, '#E1E4EA')          # top bar
scr(LW - 2, 8, RED)                                      # little "share" button
# user flow on the canvas
scr(3, 6, RED); scr(4, 6, RED)
scr(5, 6, LINE)
scr(6, 6, BLUE); scr(7, 6, BLUE)
scr(6, 5, LINE); scr(7, 5, LINE)
scr(6, 4, AMBER); scr(7, 4, AMBER)
scr(8, 4, LINE)
scr(9, 4, GREEN); scr(10, 4, GREEN)
scr(6, 3, LINE)
scr(6, 2, PURPLE); scr(7, 2, PURPLE)

# ---------- things on the desk ----------
# plant (back corner)
box(1, 1, 14, 4, 4, 4, POT); box(1, 1, 17, 4, 4, 1, '#DAD6CE')
for _ in range(80):
    x = random.randint(0, 6); y = random.randint(0, 6); z = random.randint(18, 26)
    if abs(x - 3) + abs(y - 3) + abs(z - 21) * 0.55 < 5.2:
        put(x, y, z, random.choice([LEAF, LEAF, LEAF_D, LEAF_L]))
for z in range(18, 20): put(3, 3, z, LEAF_D)
# notebook + pen
box(7, 1, 14, 6, 4, 1, '#F0E6C8'); box(7, 1, 15, 6, 4, 1, '#F7F1DF')
box(8, 2, 16, 4, 1, 1, DARK)
# sticky notes with tiny flow scribbles
box(10, 24, 14, 3, 2, 1, '#FFE27A'); put(11, 24, 15, '#FFE27A')
box(6, 23, 14, 3, 3, 1, '#9FD8F5')
# mug
box(9, 21, 14, 2, 2, 3, '#2F6F4F'); put(9, 21, 16, '#3E2A1E'); put(10, 21, 16, '#3E2A1E')
put(11, 22, 15, '#2F6F4F')
# small desk lamp-free plant stack of books
box(2, 22, 14, 4, 3, 1, BLUE); box(2, 22, 15, 4, 3, 1, AMBER); box(2, 22, 16, 4, 3, 1, RED)

# ---------- chair ----------
CX = 17
box(CX, 9, 8, 6, 9, 1, CHAIR_SEAT)                       # seat
box(CX + 5, 10, 9, 1, 7, 6, CHAIR)                       # backrest
box(CX + 2, 12, 2, 2, 2, 6, STEEL)                       # gas post
box(CX - 1, 12, 1, 8, 2, 1, STEEL); box(CX + 2, 9, 1, 2, 8, 1, STEEL)  # star base
for (x, y) in ((CX - 1, 12), (CX + 6, 13), (CX + 2, 9), (CX + 3, 16)):
    put(x, y, 0, DARK)

# ---------- Pranay, seated, facing -x (towards the laptop) ----------
# torso: thickness along x (18..20), width along y (10..16)
TX0, TY0 = 18, 10
box(TX0, TY0, 9, 3, 7, 11, TEAL)
box(TX0, TY0, 9, 3, 7, 1, TEAL_D)                        # ribbed hem
for y in range(TY0 + 1, TY0 + 6): put(TX0 + 2, y, 19, STRIPE)   # collar seen from behind
put(TX0, TY0 + 3, 19, STRIPE)
# thighs (forward along -x) and lower legs
box(12, TY0, 9, 7, 3, 2, KHAKI); box(12, TY0 + 4, 9, 7, 3, 2, KHAKI)
box(12, TY0, 1, 2, 3, 8, KHAKI); box(12, TY0 + 4, 1, 2, 3, 8, KHAKI)
put(15, TY0 + 6, 10, KHAKI_D)                            # cargo pocket
box(10, TY0, 0, 4, 3, 1, SOLE); box(10, TY0 + 4, 0, 4, 3, 1, SOLE)
box(10, TY0, 1, 4, 3, 1, SHOE); box(10, TY0 + 4, 1, 4, 3, 1, SHOE)
# arms: upper arms down the sides, forearms forward to the keyboard
for ay in (TY0 - 2, TY0 + 7):
    box(TX0, ay, 14, 3, 2, 6, TEAL)                      # upper arm
    box(TX0, ay, 17, 3, 2, 1, STRIPE)                    # stripe
    box(11, ay, 14, 7, 2, 2, TEAL)                       # forearm
    box(13, ay, 14, 1, 2, 2, STRIPE)                     # stripe
    box(15, ay, 14, 1, 2, 2, STRIPE)
    box(9, ay, 15, 2, 2, 1, SKIN)                        # hand on keyboard
# neck
box(19, 12, 20, 2, 3, 1, SKIN)
# head: x 17..21, y 11..15, z 21..27
HX, HY, HZ = 17, 11, 21
box(HX, HY, HZ, 5, 5, 7, SKIN)
# profile (+y side, y = 15): beard, ear, glasses arm, nose
for x in range(HX, HX + 4):
    for z in (HZ, HZ + 1): put(x, HY + 4, z, BEARD)
for z in (HZ + 2, HZ + 3): put(HX + 3, HY + 4, z, BEARD)   # sideburn
put(HX, HY + 4, HZ + 2, BEARD)                              # moustache corner
for x in range(HX, HX + 5):
    for y in range(HY, HY + 5): put(x, y, HZ, BEARD)        # beard underside/jaw
for y in range(HY, HY + 5):
    for z in (HZ, HZ + 1): put(HX, y, z, BEARD)             # beard at front
put(HX + 3, HY + 5, HZ + 3, SKIN); put(HX + 3, HY + 5, HZ + 2, SKIN_D)   # ear
for x in range(HX, HX + 3): put(x, HY + 4, HZ + 4, DARK)    # glasses arm
put(HX - 1, HY + 3, HZ + 4, DARK); put(HX - 1, HY + 4, HZ + 4, DARK)    # lens rim (profile)
put(HX - 1, HY + 3, HZ + 3, '#AFC2CC')                      # lens glint
put(HX - 1, HY + 2, HZ + 3, SKIN_D)                          # nose tip
# hair: short fade on back and sides, volume on top
for x in range(HX, HX + 5):
    for y in range(HY, HY + 5): put(x, y, HZ + 6, HAIR)
for y in range(HY, HY + 5): put(HX + 4, y, HZ + 5, HAIR)   # back of head (fade)
for x in range(HX + 1, HX + 5): put(x, HY + 4, HZ + 5, HAIR) # side
for x in range(HX, HX + 4):
    for y in range(HY, HY + 5): put(x, y, HZ + 7, HAIR)
for y in range(HY + 1, HY + 4): put(HX, y, HZ + 8, HAIR); put(HX + 1, y, HZ + 8, HAIR)  # quiff

# ---------- floating building blocks ----------
for (x, y, z, c) in ((2, 10, 34, RED), (2, 11, 34, '#F07A7C'), (2, 10, 35, BLUE),
                     (8, 26, 26, GREEN), (34, 10, 18, AMBER), (-2, 20, 22, PURPLE),
                     (14, 4, 30, LEAF_L), (24, 6, 28, BLUE)):
    put(x, y, z, c)

# ---------- renderer ----------
A = 7.0
def P(X, Y, Z): return ((X - Y) * A * 0.866, (X + Y) * A * 0.5 - Z * A)
def shade(h, f):
    h = h.lstrip('#'); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0, min(1, l * f if f < 1 else l + (1 - l) * (f - 1)))
    r, g, b = colorsys.hls_to_rgb(hh, l, s)
    return '#%02x%02x%02x' % (round(r * 255), round(g * 255), round(b * 255))

polys = []
for (x, y, z) in sorted(V, key=lambda k: (k[0] + k[1] + k[2], k[2])):
    c = V[(x, y, z)]
    if (x, y, z + 1) not in V:
        polys.append((shade(c, 1.12), [(x, y, z + 1), (x + 1, y, z + 1), (x + 1, y + 1, z + 1), (x, y + 1, z + 1)]))
    if (x, y + 1, z) not in V:
        polys.append((c, [(x, y + 1, z), (x + 1, y + 1, z), (x + 1, y + 1, z + 1), (x, y + 1, z + 1)]))
    if (x + 1, y, z) not in V:
        polys.append((c if (x, y, z) in GLOW else shade(c, 0.8), [(x + 1, y, z), (x + 1, y + 1, z), (x + 1, y + 1, z + 1), (x + 1, y, z + 1)]))
polys = [(c, [P(*p) for p in pts]) for c, pts in polys]

xs = [p[0] for _, pts in polys for p in pts]; ys = [p[1] for _, pts in polys for p in pts]
pad = 10; minx, miny = min(xs) - pad, min(ys) - pad
W, H = max(xs) - minx + pad, max(ys) - miny + pad + 24
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="Voxel illustration of Pranay at his desk designing a user flow on a laptop">',
       '<title>Pranay designing a user flow at his desk</title>',
       '<defs><radialGradient id="sh" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#000" stop-opacity=".16"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>']
cx, cy = P(12, 14, 0)
out.append(f'<ellipse cx="{cx - minx:.1f}" cy="{cy - miny + 6:.1f}" rx="{W * 0.47:.0f}" ry="{W * 0.15:.0f}" fill="url(#sh)"/>')
for col, pts in polys:
    d = ' '.join(f'{px - minx:.1f},{py - miny:.1f}' for px, py in pts)
    out.append(f'<polygon points="{d}" fill="{col}" stroke="{col}" stroke-width="1.1" stroke-linejoin="round"/>')
out.append('</svg>')
dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'images', 'hero-voxel.svg')
open(dest, 'w').write('\n'.join(out))
print(len(V), 'voxels', len(polys), 'faces', f'{W:.0f}x{H:.0f}')
