#!/usr/bin/env python3
"""
LOAD-BEARING LIGHT — recruitment poster, A4 portrait @ 300dpi.

Conceptual section: the Semarang -> Ambarawa -> Salatiga corridor drawn as a
structural elevation, coursed in brick, rising from the coastal datum (+3 m)
to the highland shelf (+591 m). The sales route as a load path.
"""

import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ----------------------------------------------------------------------------
# CANVAS — A4 portrait, 300 dpi
# ----------------------------------------------------------------------------
W, H = 2480, 3508
SS = 2                                     # supersample factor
CW, CH = W * SS, H * SS

# ----------------------------------------------------------------------------
# ISI DI SINI — satu-satunya bagian yang perlu diubah
# ----------------------------------------------------------------------------
NAMA_PERUSAHAAN = "NAMA PERUSAHAAN"
ALAMAT          = "Alamat kantor / toko — Kota, Jawa Tengah"
KONTAK          = "0812-XXXX-XXXX"
JAM_KERJA       = "WHATSAPP / TELEPON — JAM KERJA 08.00–17.00"

FONTS = "/root/.claude/skills/canvas-design/canvas-fonts"

# ----------------------------------------------------------------------------
# QUARRIED PALETTE — four tones, disciplined ratio
# ----------------------------------------------------------------------------
PAPER  = (232, 226, 214)      # limestone ground
INK    = (24, 27, 29)         # slate, reads as shadow
CLAY   = (176, 71, 42)        # fired clay — used with restraint
MORTAR = (141, 133, 120)      # cured mortar grey
FAINT  = (208, 201, 188)      # ruled-field hairline

MARGIN = 168 * SS
LEFT   = MARGIN
RIGHT  = CW - MARGIN
COLW   = RIGHT - LEFT


def f(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size * SS)


# type registers
DISPLAY = lambda s: f("BigShoulders-Bold.ttf", s)
MONO    = lambda s: f("GeistMono-Regular.ttf", s)
MONO_B  = lambda s: f("GeistMono-Bold.ttf", s)
BODY    = lambda s: f("WorkSans-Regular.ttf", s)

img = Image.new("RGB", (CW, CH), PAPER)
d = ImageDraw.Draw(img)

random.seed(1873)   # Ambarawa station, opened 1873


# ----------------------------------------------------------------------------
# helpers  (all y-values below are quoted in 1x px; U() scales them)
# ----------------------------------------------------------------------------
def U(v):
    return int(v * SS)


def track(draw, xy, text, font, fill, tracking=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor="la")
        x += draw.textlength(ch, font=font) + tracking


def track_w(draw, text, font, tracking=0):
    if not text:
        return 0
    return sum(draw.textlength(c, font=font) for c in text) + tracking * (len(text) - 1)


def rule(draw, x0, y, x1, fill=INK, w=1):
    draw.rectangle([x0, y, x1, y + U(w) - 1], fill=fill)


def vrule(draw, x, y0, y1, fill=FAINT, w=1):
    draw.rectangle([x, y0, x + U(w) - 1, y1], fill=fill)


def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


# ============================================================================
# I.  THE RULED FIELD — surveyor's rails, drawn before anything is filled
# ============================================================================
TOP_RAIL, BOT_RAIL = U(96), U(3412)

vrule(d, LEFT - U(44), TOP_RAIL, BOT_RAIL, MORTAR)
for i in range(65):
    y = TOP_RAIL + (BOT_RAIL - TOP_RAIL) * i / 64
    major = (i % 8 == 0)
    ln = U(18 if major else 8)
    d.rectangle([LEFT - U(44) - ln, y, LEFT - U(44) - SS, y + SS - 1],
                fill=INK if major else MORTAR)

vrule(d, RIGHT + U(44), TOP_RAIL, BOT_RAIL, FAINT)


# ============================================================================
# II.  HEADER REGISTER — instrumentation, set for other draughtsmen
# ============================================================================
track(d, (LEFT, U(150)), "LOWONGAN KERJA", MONO(13), INK, U(5.2))
d.text((RIGHT, U(150)), "DOK. REKRUTMEN / SEK. MATERIAL BANGUNAN",
       font=MONO(13), fill=MORTAR, anchor="ra")

rule(d, LEFT, U(186), RIGHT, INK, 2)

track(d, (LEFT, U(206)), "DIBUKA SEGERA — KUOTA TERBATAS", MONO(12), CLAY, U(3.4))
d.text((RIGHT, U(206)), "REV. 01 / HAL. 1 DARI 1", font=MONO(12), fill=MORTAR, anchor="ra")


# ============================================================================
# III.  THE MONUMENT — type constructed, not set
# ============================================================================
# BigShoulders sits its cap-top at 0.178em and its baseline at 0.997em below
# the drawing origin; both lines are set from their cap-tops so the leading is
# optical, not nominal.
DSIZE = 440
CAP_IN, BASE_IN = 0.178 * DSIZE, 0.997 * DSIZE
fd = DISPLAY(DSIZE)
t1, t2 = "SALES", "BANGUNAN"

CAP1, CAP2 = 296, 700
track(d, (LEFT, U(CAP1 - CAP_IN)), t1, fd, INK, U(6))
track(d, (LEFT, U(CAP2 - CAP_IN)), t2, fd, CLAY, U(6))
w1 = track_w(d, t1, fd, U(6))

d.text((LEFT + w1 + U(46), U(CAP1)), "01", font=MONO(20), fill=CLAY, anchor="la")
d.text((LEFT + w1 + U(46), U(CAP1 + 38)), "POSISI", font=MONO(13), fill=MORTAR, anchor="la")
d.text((RIGHT, U(CAP1 + 4)), "TERBUKA UNTUK PRIA / WANITA",
       font=MONO(13), fill=MORTAR, anchor="ra")

BASE2 = CAP2 - CAP_IN + BASE_IN                      # 1060
rule(d, LEFT, U(BASE2 + 36), RIGHT, INK, 1)
track(d, (LEFT, U(BASE2 + 60)), "PENEMPATAN", MONO(13), MORTAR, U(4.6))
d.text((RIGHT, U(BASE2 + 60)), "SEMARANG · SALATIGA · AMBARAWA",
       font=f("WorkSans-Bold.ttf", 21), fill=INK, anchor="ra")


# ============================================================================
# IV.  THE SECTION — coursed elevation, coast to highland shelf.
#      Marks accumulate; density is proportional to elevation.
# ============================================================================
SEC_TOP, SEC_BOT = U(1256), U(1636)
SEC_H = SEC_BOT - SEC_TOP
EMAX = 660.0

d.text((LEFT, U(1206)), "KORIDOR OPERASIONAL", font=MONO(13), fill=MORTAR)
d.text((RIGHT, U(1206)), "DIUTAMAKAN DOMISILI SEMARANG",
       font=MONO_B(13), fill=CLAY, anchor="ra")

# elevation gridlines — ruled first, the field beneath the masonry
for e in (150, 300, 450, 600):
    gy = SEC_BOT - SEC_H * (e / EMAX)
    rule(d, LEFT, gy, RIGHT, FAINT, 1)
    d.text((LEFT + U(6), gy - U(22)), f"+{e} M", font=MONO(11), fill=MORTAR, anchor="la")

STATIONS = [(0.10, 3, "SEMARANG"), (0.50, 474, "AMBARAWA"), (0.90, 591, "SALATIGA")]

BW, BH, GAP = U(26), U(13), U(3)
n_cols = int(COLW // (BW + GAP))
off = (COLW - (n_cols * (BW + GAP) - GAP)) / 2


def profile(t):
    """Smooth interpolated terrain across the corridor, t in [0,1]."""
    pts = [(0.0, 2.0)] + [(p, e) for p, e, _ in STATIONS] + [(1.0, 604.0)]
    for i in range(len(pts) - 1):
        x0, e0 = pts[i]
        x1, e1 = pts[i + 1]
        if x0 <= t <= x1:
            u = (t - x0) / (x1 - x0)
            u = u * u * (3 - 2 * u)          # smoothstep — settled, not sharp
            return e0 + (e1 - e0) * u
    return pts[-1][1]


col_rows = []
for c in range(n_cols):
    t = (c + 0.5) / n_cols
    h = SEC_H * (profile(t) / EMAX)
    col_rows.append(max(1, int(h // (BH + GAP))))

max_rows = max(col_rows)
for r in range(max_rows):
    yb = SEC_BOT - (r + 1) * (BH + GAP)
    for c in range(n_cols):
        if r >= col_rows[c]:
            continue
        x0 = LEFT + off + c * (BW + GAP) + (BW / 2 if r % 2 else 0)
        x1 = min(x0 + BW, RIGHT)                 # cut brick at the boundary
        if x1 - x0 < U(4):
            continue
        # the footing course is always solid — a foundation may not read hollow
        if r == col_rows[c] - 1 and r > 0:       # surface course traces terrain
            d.rectangle([x0, yb, x1, yb + BH], outline=CLAY, width=SS)
        else:
            fade = 0.34 + 0.66 * (1 - r / max(col_rows[c], 1))
            col = tuple(int(PAPER[i] + (INK[i] - PAPER[i]) * fade) for i in range(3))
            d.rectangle([x0, yb, x1, yb + BH], fill=col)

# datum
rule(d, LEFT, SEC_BOT, RIGHT, INK, 2)

# station markers — crosshair, plumb line, elevation figure
for p, e, name in STATIONS:
    x = LEFT + COLW * p
    ytop = SEC_BOT - SEC_H * (e / EMAX)
    # the survey line is cut through the masonry, not laid over it
    for yy in range(int(ytop), int(SEC_BOT), U(11)):
        d.rectangle([x - SS, yy, x + SS * 2 - 1, min(yy + U(5), SEC_BOT)], fill=PAPER)
    r = U(9)
    # annotation clears the hatch, as a draughtsman would mask it
    d.rectangle([x - r * 2.4, ytop - r * 2.4, x + r * 2.4, ytop + r * 2.4], fill=PAPER)
    d.ellipse([x - r, ytop - r, x + r, ytop + r], outline=INK, width=2 * SS)
    d.rectangle([x - r * 2, ytop, x + r * 2, ytop + SS - 1], fill=INK)
    d.rectangle([x, ytop - r * 2, x + SS - 1, ytop + r * 2], fill=INK)
    d.text((x, ytop - U(30)), f"+{e} M", font=MONO_B(14), fill=CLAY, anchor="ms")
    track(d, (x - track_w(d, name, MONO(14), U(3.6)) / 2, SEC_BOT + U(22)),
          name, MONO(14), INK, U(3.6))

d.text((LEFT, SEC_BOT + U(68)), "DATUM ±0.00 M.D.P.L.", font=MONO(12), fill=MORTAR)
d.text((RIGHT, SEC_BOT + U(68)), "SEKSI A—A′ · SKALA VERT. TIDAK SEBANDING",
       font=MONO(12), fill=MORTAR, anchor="ra")


# ============================================================================
# V.  INSTRUMENTATION — where the specifics live
# ============================================================================
rule(d, LEFT, U(1782), RIGHT, INK, 2)
track(d, (LEFT, U(1808)), "KUALIFIKASI", MONO_B(15), INK, U(5))
d.text((RIGHT, U(1808)), "§ 01", font=MONO(14), fill=MORTAR, anchor="ra")

QUALS = [
    "Minimal 1 tahun pengalaman di bidang bangunan atau material konstruksi.",
    "Memiliki kemampuan komunikasi dan negosiasi yang baik.",
    "Bertanggung jawab, jujur, dan disiplin.",
    "Siap bekerja di bawah tekanan dan dengan sistem target.",
    "Bersedia ditempatkan di area Semarang, Salatiga, dan Ambarawa.",
    "Diutamakan berdomisili di Semarang.",
    "Pendidikan minimal SMA / SMK sederajat.",
    "Memiliki SIM C dan kendaraan pribadi.",
    "Mampu mengoperasikan Ms. Excel dan WhatsApp Business.",
    "Memahami produk material bangunan menjadi nilai tambah.",
]

QY = U(1870)
GUT = U(72)
cw = (COLW - GUT) / 2
fb = BODY(21)
half = (len(QUALS) + 1) // 2
LH = U(30)

vrule(d, LEFT + cw + GUT / 2, QY - U(14), QY + U(300), FAINT)

for ci in range(2):
    cx = LEFT + ci * (cw + GUT)
    cy = QY
    for i, q in enumerate(QUALS[ci * half:(ci + 1) * half]):
        idx = ci * half + i + 1
        d.text((cx, cy + U(3)), f"{idx:02d}", font=MONO_B(15), fill=CLAY, anchor="la")
        lines = wrap(d, q, fb, cw - U(56))
        for j, ln in enumerate(lines):
            d.text((cx + U(56), cy + j * LH), ln, font=fb, fill=INK, anchor="la")
        cy += len(lines) * LH + U(30)
        rule(d, cx, cy - U(16), cx + cw, FAINT, 1)


# ============================================================================
# VI.  THE BEARING BLOCK — what is carried, carried on ink
# ============================================================================
BY0, BY1 = U(2226), U(2694)
d.rectangle([LEFT, BY0, RIGHT, BY1], fill=INK)

track(d, (LEFT + U(48), BY0 + U(42)), "YANG ANDA DAPATKAN", MONO_B(15), PAPER, U(5))
d.text((RIGHT - U(48), BY0 + U(42)), "§ 02", font=MONO(14), fill=MORTAR, anchor="ra")
rule(d, LEFT + U(48), BY0 + U(78), RIGHT - U(48), (58, 62, 64), 1)

BENS = [
    ("GAJI POKOK",             "Dibayar tepat waktu setiap bulan."),
    ("INSENTIF MENARIK",       "Komisi progresif atas setiap penjualan."),
    ("BONUS TARGET",           "Apresiasi tambahan saat target tercapai."),
    ("TUNJANGAN OPERASIONAL",  "Dukungan transport dan komunikasi lapangan."),
    ("JENJANG KARIER",         "Pelatihan produk dan peluang promosi."),
    ("TIM YANG SOLID",         "Pendampingan langsung dari rekan senior."),
]

bcw = (RIGHT - LEFT - U(96) - GUT) / 2
for i, (head, sub) in enumerate(BENS):
    bx = LEFT + U(48) + (i % 2) * (bcw + GUT)
    yy = BY0 + U(128) + (i // 2) * U(124)
    d.rectangle([bx, yy + U(9), bx + U(22), yy + U(11)], fill=CLAY)
    track(d, (bx + U(38), yy), head, MONO_B(15), PAPER, U(2.4))
    d.text((bx + U(38), yy + U(32)), sub, font=BODY(18), fill=MORTAR, anchor="la")


# ============================================================================
# VII.  FOOTING — heaviest at the base
# ============================================================================
rule(d, LEFT, U(2766), RIGHT, INK, 2)
track(d, (LEFT, U(2792)), "CARA MELAMAR", MONO_B(15), INK, U(5))
d.text((RIGHT, U(2792)), "§ 03", font=MONO(14), fill=MORTAR, anchor="ra")

steps = [
    ("01", "Siapkan CV, fotokopi KTP, dan pas foto terbaru."),
    ("02", "Kirim berkas melalui WhatsApp ke nomor di samping."),
    ("03", "Tulis subjek: LAMARAN SALES — (NAMA) — (KOTA)."),
]
for i, (n, s) in enumerate(steps):
    yy = U(2856) + i * U(46)
    d.text((LEFT, yy + U(3)), n, font=MONO_B(15), fill=CLAY, anchor="la")
    d.text((LEFT + U(56), yy), s, font=BODY(21), fill=INK, anchor="la")

# contact — the loudest instrument in the lower register
d.text((RIGHT, U(2840)), "HUBUNGI", font=MONO(13), fill=MORTAR, anchor="ra")
d.text((RIGHT, U(2866)), KONTAK, font=DISPLAY(78), fill=INK, anchor="ra")
d.text((RIGHT, U(2962)), JAM_KERJA, font=MONO(12), fill=MORTAR, anchor="ra")

# company plate — the second monument, balancing the first
rule(d, LEFT, U(3054), RIGHT, INK, 1)
track(d, (LEFT, U(3080)), NAMA_PERUSAHAAN, DISPLAY(66), INK, U(3))
d.text((LEFT, U(3176)), ALAMAT, font=BODY(19), fill=MORTAR, anchor="la")

d.text((RIGHT, U(3098)), "PROSES SELEKSI TIDAK DIPUNGUT BIAYA APAPUN",
       font=MONO_B(13), fill=CLAY, anchor="ra")
d.text((RIGHT, U(3130)), "WASPADA TERHADAP PENIPUAN LOWONGAN KERJA",
       font=MONO(13), fill=MORTAR, anchor="ra")

# baseline register
rule(d, LEFT, U(3306), RIGHT, MORTAR, 1)
track(d, (LEFT, U(3324)), "LOAD-BEARING LIGHT", MONO(11), MORTAR, U(3))
d.text((CW / 2, U(3324)), "SEKSI A—A′ · KORIDOR SEMARANG—SALATIGA",
       font=MONO(11), fill=MORTAR, anchor="ma")
d.text((RIGHT, U(3324)), "±0.00 → +591.00 M", font=MONO(11), fill=MORTAR, anchor="ra")


# ============================================================================
# VIII.  MATERIAL FINISH — the tooth of the paper, the memory of pressure
# ============================================================================
img = img.resize((W, H), Image.LANCZOS)

grain = Image.effect_noise((W, H), 13).convert("L").filter(ImageFilter.GaussianBlur(0.4))
img = Image.blend(img, Image.merge("RGB", (grain,) * 3), 0.045)

vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.rectangle([0, 0, W, H], fill=24)
vd.rectangle([70, 70, W - 70, H - 70], fill=0)
vig = vig.filter(ImageFilter.GaussianBlur(90))
img = Image.composite(Image.new("RGB", (W, H), (196, 189, 176)), img, vig)

img.save("/home/user/Order.githup.io/poster/lowongan-sales-bangunan.png", dpi=(300, 300))
img.save("/home/user/Order.githup.io/poster/lowongan-sales-bangunan.pdf",
         "PDF", resolution=300.0)
print("ok", img.size)
