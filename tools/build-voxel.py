# Run: python3 tools/build-voxel.py  -> regenerates assets/images/hero-voxel.svg
"""Original isometric voxel illustration for Pranay's hero.
Scene: Pranay (teal striped sweater, khaki trousers, glasses, beard) at a
whiteboard mapping a user flow, with a plant, a side table, laptop and mug."""
import colorsys, os, random
random.seed(7)
V = {}  # (x,y,z) -> hex colour

def box(x0, y0, z0, dx, dy, dz, c):
    for x in range(x0, x0+dx):
        for y in range(y0, y0+dy):
            for z in range(z0, z0+dz):
                V[(x, y, z)] = c

def put(x, y, z, c): V[(x, y, z)] = c

# ---------- palette ----------
DARK = '#2B2B2B'; STEEL = '#4A4A4A'; WHITE = '#F7F7F5'; LINE = '#B9B9B9'
RED = '#E5383B'; BLUE = '#3D7BF7'; AMBER = '#F2B33D'; GREEN = '#2FA866'; PURPLE = '#7A5AF5'
TEAL = '#1F5566'; TEAL_D = '#18434F'; STRIPE = '#E9EEF2'
KHAKI = '#C9A77A'; SKIN = '#C48A60'; SKIN_D = '#A9714B'
HAIR = '#1D1916'; BEARD = '#2A2019'; SHOE = '#ECECEC'; SOLE = '#5A5A5A'
WOOD = '#E2C49A'; POT = '#EFEDE8'; LEAF = '#5FAE4E'; LEAF_D = '#3E8A3A'; LEAF_L = '#8CCB5E'

# ---------- whiteboard (front faces +y, so its face is drawn as left faces) ----------
BX, BY, BZ, BW, BH = 2, 6, 14, 23, 21
box(BX, BY, BZ, BW, 1, BH, DARK)                 # frame
box(BX+1, BY, BZ+1, BW-2, 1, BH-2, WHITE)        # board surface
box(BX, BY+1, BZ-1, BW, 2, 1, STEEL)             # marker tray
box(BX+3, BY, 0, 1, 1, BZ, STEEL); box(BX+BW-4, BY, 0, 1, 1, BZ, STEEL)   # stand posts
box(BX+1, BY-2, 0, 5, 5, 1, STEEL); box(BX+BW-6, BY-2, 0, 5, 5, 1, STEEL)  # feet
put(BX+6, BY+1, BZ, RED); put(BX+8, BY+1, BZ, BLUE)                       # markers in tray

def board(u, v, c):  # u: 0..BW-1 along x, v: 0..BH-1 up
    put(BX+u, BY, BZ+v, c)
def rect(u0, v0, w, h, c):
    for u in range(u0, u0+w):
        for v in range(v0, v0+h): board(u, v, c)
# a small user flow: start -> step -> decision -> two outcomes
rect(2, 15, 4, 3, RED)
for u in range(6, 9): board(u, 16, LINE)
rect(9, 15, 5, 3, BLUE)
for v in range(11, 15): board(11, v, LINE)
rect(9, 8, 5, 3, AMBER)
for u in range(14, 16): board(u, 9, LINE)
rect(16, 8, 4, 3, GREEN)
for v in range(5, 8): board(11, v, LINE)
rect(9, 2, 5, 3, PURPLE)
rect(16, 15, 4, 1, LINE); rect(16, 13, 3, 1, LINE)   # scribbled notes

# ---------- Pranay ----------
PX, PY = 28, 11            # body occupies x 28..34, y 11..13; faces +y (towards viewer-left)
# shoes
box(PX, PY, 0, 3, 4, 1, SOLE); box(PX+4, PY, 0, 3, 4, 1, SOLE)
box(PX, PY, 1, 3, 4, 1, SHOE); box(PX+4, PY, 1, 3, 4, 1, SHOE)
# trousers
box(PX, PY, 2, 3, 3, 11, KHAKI); box(PX+4, PY, 2, 3, 3, 11, KHAKI); box(PX+3, PY, 9, 1, 3, 4, KHAKI)
put(PX+6, PY+1, 7, '#B8955F'); put(PX+6, PY+1, 6, '#B8955F')         # cargo pocket hint
# sweater
box(PX, PY, 13, 7, 3, 11, TEAL)
box(PX, PY, 13, 7, 3, 1, TEAL_D)                                      # ribbed hem
for x in range(PX+2, PX+5): put(x, PY+2, 23, STRIPE)                 # white collar
put(PX+2, PY+2, 22, STRIPE); put(PX+4, PY+2, 22, STRIPE)
put(PX+3, PY+2, 21, DARK); put(PX+3, PY+2, 20, DARK)                  # sunglasses hooked on collar
# right arm (his right = +x side), hanging, with white stripes
box(PX+7, PY, 13, 2, 3, 10, TEAL)
for z in (19, 17): box(PX+7, PY, z, 2, 3, 1, STRIPE)
box(PX+7, PY, 11, 2, 3, 2, SKIN)
# left arm reaching to the board, holding a marker
box(PX-2, PY, 20, 2, 3, 3, TEAL)
box(PX-9, PY+1, 21, 7, 2, 2, TEAL)
put(PX-5, PY+1, 21, STRIPE); put(PX-5, PY+1, 22, STRIPE); put(PX-5, PY+2, 21, STRIPE); put(PX-5, PY+2, 22, STRIPE)
put(PX-7, PY+1, 21, STRIPE); put(PX-7, PY+1, 22, STRIPE); put(PX-7, PY+2, 21, STRIPE); put(PX-7, PY+2, 22, STRIPE)
box(PX-11, PY+1, 21, 2, 2, 2, SKIN)
box(PX-13, PY+1, 22, 2, 1, 1, RED)                                     # marker
# neck + head
box(PX+2, PY, 24, 3, 3, 1, SKIN)
HX, HY, HZ = PX+1, PY-1, 25       # head x 29..33, y 10..14, z 25..31
box(HX, HY, HZ, 5, 5, 7, SKIN)
put(HX+5, HY+2, HZ+3, SKIN); put(HX+5, HY+2, HZ+2, SKIN_D)            # ear
# beard (front, sides, jaw)
for x in range(HX, HX+5): put(x, HY+4, HZ, BEARD)
for x in (HX, HX+1, HX+3, HX+4): put(x, HY+4, HZ+1, BEARD)
put(HX, HY+4, HZ+2, BEARD); put(HX+4, HY+4, HZ+2, BEARD)
for y in range(HY+1, HY+4):
    for z in (HZ, HZ+1, HZ+2): put(HX+4, y, z, BEARD); put(HX, y, z, BEARD)
put(HX+2, HY+4, HZ+1, '#7A4A3A')                                        # mouth
put(HX+2, HY+4, HZ+2, SKIN_D)                                            # nose
# glasses
for x in range(HX, HX+5): put(x, HY+4, HZ+4, DARK)
put(HX, HY+4, HZ+3, DARK); put(HX+2, HY+4, HZ+3, DARK); put(HX+4, HY+4, HZ+3, DARK)
put(HX+1, HY+4, HZ+3, '#AFC2CC'); put(HX+3, HY+4, HZ+3, '#AFC2CC')
for y in range(HY+2, HY+4): put(HX+4, y, HZ+4, DARK)                    # temple arm on visible side
# hair: short fade on sides, volume on top
for x in range(HX, HX+5):
    for y in range(HY, HY+5): put(x, y, HZ+7, HAIR)
for x in range(HX, HX+5): put(x, HY, HZ+6, HAIR); put(x, HY, HZ+5, HAIR)
for y in range(HY, HY+4): put(HX+4, y, HZ+6, HAIR); put(HX, y, HZ+6, HAIR)
for x in range(HX, HX+5):
    for y in range(HY+1, HY+5): put(x, y, HZ+8, HAIR)
for x in range(HX+1, HX+5): put(x, HY+4, HZ+9, HAIR); put(x, HY+3, HZ+9, HAIR)

# ---------- side table with laptop + mug ----------
TX, TY = 40, 1
box(TX, TY, 12, 13, 9, 1, WOOD)
for (x, y) in ((TX, TY), (TX+12, TY), (TX, TY+8), (TX+12, TY+8)): box(x, y, 0, 1, 1, 12, DARK)
box(TX+2, TY+3, 13, 7, 5, 1, '#C9CCD1')                                 # laptop base
box(TX+2, TY+2, 13, 7, 1, 6, '#3A3D42')                                 # lid
box(TX+3, TY+2, 14, 5, 1, 4, '#EEF1F5')                                 # screen
put(TX+3, TY+2, 17, RED); put(TX+4, TY+2, 17, LINE); put(TX+5, TY+2, 17, LINE)
put(TX+3, TY+2, 15, BLUE); put(TX+4, TY+2, 15, BLUE); put(TX+6, TY+2, 16, LINE)
box(TX+10, TY+5, 13, 2, 2, 3, '#2F6F4F')                                 # mug
put(TX+10, TY+5, 15, '#3E2A1E'); put(TX+11, TY+5, 15, '#3E2A1E')
box(TX+10, TY+1, 13, 2, 3, 1, '#F0E6C8')                                 # notebook
put(TX+9, TY+1, 14, DARK)

# ---------- plant ----------
box(5, 16, 0, 5, 5, 6, POT); box(5, 16, 5, 5, 5, 1, '#DAD6CE')
for _ in range(70):
    x = random.randint(3, 11); y = random.randint(14, 22); z = random.randint(6, 15)
    if abs(x-7) + abs(y-18) + abs(z-10)*0.6 < 6.5:
        put(x, y, z, random.choice([LEAF, LEAF, LEAF_D, LEAF_L]))
for z in range(6, 9): put(7, 18, z, LEAF_D)

# ---------- a few floating building blocks ----------
for (x, y, z, c) in ((16, 2, 40, RED), (17, 2, 40, '#F07A7C'), (16, 2, 41, BLUE),
                     (46, 4, 30, GREEN), (52, 12, 22, AMBER), (0, 22, 24, PURPLE), (38, 14, 38, LEAF_L)):
    put(x, y, z, c)

# ---------- renderer ----------
A = 7.0
def P(X, Y, Z): return ((X - Y) * A * 0.866 * 2 / 1.732 * 0.866, (X + Y) * A * 0.5 - Z * A)
def shade(h, f):
    h = h.lstrip('#'); r, g, b = (int(h[i:i+2], 16)/255 for i in (0, 2, 4))
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0, min(1, l * f if f < 1 else l + (1-l)*(f-1)))
    r, g, b = colorsys.hls_to_rgb(hh, l, s)
    return '#%02x%02x%02x' % (round(r*255), round(g*255), round(b*255))

polys = []
for (x, y, z) in sorted(V, key=lambda k: (k[0]+k[1]+k[2], k[2])):
    c = V[(x, y, z)]
    faces = []
    if (x, y, z+1) not in V: faces.append(([(x,y,z+1),(x+1,y,z+1),(x+1,y+1,z+1),(x,y+1,z+1)], shade(c, 1.12)))
    if (x, y+1, z) not in V: faces.append(([(x,y+1,z),(x+1,y+1,z),(x+1,y+1,z+1),(x,y+1,z+1)], c))
    if (x+1, y, z) not in V: faces.append(([(x+1,y,z),(x+1,y+1,z),(x+1,y+1,z+1),(x+1,y,z+1)], shade(c, 0.78)))
    for pts, col in faces:
        polys.append((col, [P(*p) for p in pts]))

xs = [p[0] for _, pts in polys for p in pts]; ys = [p[1] for _, pts in polys for p in pts]
pad = 10; minx, miny = min(xs)-pad, min(ys)-pad; W, H = max(xs)-minx+pad, max(ys)-miny+pad+30
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="Voxel illustration of Pranay at a whiteboard mapping a user flow">',
       '<title>Pranay mapping a user flow</title>',
       '<defs><radialGradient id="sh" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#000" stop-opacity=".16"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>']
# soft floor shadow
cx, cy = P(28, 14, 0); out.append(f'<ellipse cx="{cx-minx:.1f}" cy="{cy-miny+4:.1f}" rx="{W*0.46:.0f}" ry="{W*0.12:.0f}" fill="url(#sh)"/>')
for col, pts in polys:
    d = ' '.join(f'{px-minx:.1f},{py-miny:.1f}' for px, py in pts)
    out.append(f'<polygon points="{d}" fill="{col}" stroke="{col}" stroke-width="1.1" stroke-linejoin="round"/>')
out.append('</svg>')
open(os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'hero-voxel.svg'), 'w').write('\n'.join(out))
print(len(V), 'voxels', len(polys), 'faces', f'{W:.0f}x{H:.0f}')
