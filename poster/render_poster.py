#!/usr/bin/env python3
"""
LOAD-BEARING LIGHT — poster lowongan kerja, format WhatsApp (portrait 18:25).

Fokus: SYARAT dan BENEFIT. Tipografi besar agar terbaca di layar ponsel.
Pita bata di bawah judul adalah sisa dari seksi elevasi koridor
Semarang -> Ambarawa -> Salatiga: pesisir di kiri, dataran tinggi di kanan.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ----------------------------------------------------------------------------
# ISI DI SINI — satu-satunya bagian yang perlu diubah
# ----------------------------------------------------------------------------
NAMA_PERUSAHAAN = "CV HALIM IMANNUEL MAKMUR"
KONTAK          = "0852-1968-0709"

FONTS = "/root/.claude/skills/canvas-design/canvas-fonts"

# ----------------------------------------------------------------------------
# CANVAS — portrait, dioptimalkan untuk pratinjau WhatsApp
# ----------------------------------------------------------------------------
W, H = 1800, 2500
SS = 2
CW, CH = W * SS, H * SS

# ----------------------------------------------------------------------------
# QUARRIED PALETTE — four tones, disciplined ratio
# ----------------------------------------------------------------------------
PAPER  = (232, 226, 214)
INK    = (24, 27, 29)
CLAY   = (176, 71, 42)
MORTAR = (141, 133, 120)
FAINT  = (208, 201, 188)

MARGIN = 105 * SS
LEFT   = MARGIN
RIGHT  = CW - MARGIN
COLW   = RIGHT - LEFT


def f(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", int(size * SS))


DISPLAY = lambda s: f("BigShoulders-Bold.ttf", s)
MONO    = lambda s: f("GeistMono-Regular.ttf", s)
MONO_B  = lambda s: f("GeistMono-Bold.ttf", s)
BODY    = lambda s: f("WorkSans-Regular.ttf", s)
BODY_B  = lambda s: f("WorkSans-Bold.ttf", s)

img = Image.new("RGB", (CW, CH), PAPER)
d = ImageDraw.Draw(img)


# ----------------------------------------------------------------------------
# helpers (y-values quoted in 1x px; U() scales to the supersampled canvas)
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


# ============================================================================
# I.  HEADER
# ============================================================================
track(d, (LEFT, U(118)), "LOWONGAN KERJA", MONO(26), INK, U(9))
d.text((RIGHT, U(118)), "DIBUKA SEGERA", font=MONO_B(24), fill=CLAY, anchor="ra")
rule(d, LEFT, U(162), RIGHT, INK, 4)


# ============================================================================
# II.  THE MONUMENT
# ============================================================================
DSIZE = 310
CAP_IN, BASE_IN = 0.178 * DSIZE, 0.997 * DSIZE
fd = DISPLAY(DSIZE)

CAP1, CAP2 = 225, 519
track(d, (LEFT, U(CAP1 - CAP_IN)), "SALES", fd, INK, U(8))
track(d, (LEFT, U(CAP2 - CAP_IN)), "BANGUNAN", fd, CLAY, U(8))


# ============================================================================
# III.  THE COURSED BAND — coast at the left, highland shelf at the right
# ============================================================================
BAND_TOP, BAND_BOT = U(846), U(950)
d.text((LEFT, U(806)), "PENEMPATAN", font=MONO(22), fill=MORTAR, anchor="la")
d.text((RIGHT, U(806)), "DIUTAMAKAN DOMISILI SEMARANG",
       font=MONO_B(22), fill=CLAY, anchor="ra")

BW, BH, GAP = U(30), U(15), U(3)
n_cols = int(COLW // (BW + GAP))
off = (COLW - (n_cols * (BW + GAP) - GAP)) / 2
n_rows = int((BAND_BOT - BAND_TOP) // (BH + GAP))

for r in range(n_rows):
    yb = BAND_BOT - (r + 1) * (BH + GAP)
    for c in range(n_cols):
        x0 = LEFT + off + c * (BW + GAP) + (BW / 2 if r % 2 else 0)
        x1 = min(x0 + BW, RIGHT)
        if x1 - x0 < U(4):
            continue
        # tone climbs west to east, and settles with depth
        t = (c + 0.5) / n_cols
        fade = (0.16 + 0.74 * t) * (0.74 + 0.26 * (r / max(n_rows - 1, 1)))
        col = tuple(int(PAPER[i] + (INK[i] - PAPER[i]) * fade) for i in range(3))
        d.rectangle([x0, yb, x1, yb + BH], fill=col)

rule(d, LEFT, BAND_BOT, RIGHT, INK, 4)

# stations read off the datum, below the course — the band stays unbroken
STATIONS = [(0.10, "SEMARANG"), (0.50, "AMBARAWA"), (0.90, "SALATIGA")]
for p_, name in STATIONS:
    x = LEFT + COLW * p_
    d.rectangle([x - SS, BAND_BOT + U(8), x + SS * 2 - 1, BAND_BOT + U(24)], fill=INK)
    fnm = MONO_B(27)
    track(d, (x - track_w(d, name, fnm, U(5)) / 2, U(972)), name, fnm, INK, U(5))


# ============================================================================
# IV.  SYARAT — the first of two subjects
# ============================================================================
rule(d, LEFT, U(1048), RIGHT, INK, 4)
track(d, (LEFT, U(1076)), "SYARAT", MONO_B(34), INK, U(9))
d.text((RIGHT, U(1080)), "§ 01", font=MONO(26), fill=MORTAR, anchor="ra")

SYARAT = [
    "Pengalaman min. 1 tahun di bidang bangunan",
    "Kemampuan komunikasi & negosiasi yang baik",
    "Bertanggung jawab dan jujur",
    "Siap bekerja di bawah tekanan dan target",
    "Bersedia ditempatkan di Semarang, Salatiga, Ambarawa",
    "Diutamakan berdomisili di Semarang",
]

fs = BODY(50)
fn = MONO_B(32)
sy = 1162
for i, s in enumerate(SYARAT):
    yy = U(sy + i * 82)
    d.text((LEFT, yy + U(9)), f"{i + 1:02d}", font=fn, fill=CLAY, anchor="la")
    d.text((LEFT + U(86), yy), s, font=fs, fill=INK, anchor="la")
    if i < len(SYARAT) - 1:
        rule(d, LEFT + U(86), U(sy + i * 82 + 66), RIGHT, FAINT, 1)


# ============================================================================
# V.  BENEFIT — carried on ink
# ============================================================================
BY0, BY1 = U(1706), U(2150)
d.rectangle([LEFT, BY0, RIGHT, BY1], fill=INK)

track(d, (LEFT + U(56), BY0 + U(44)), "BENEFIT", MONO_B(34), PAPER, U(9))
d.text((RIGHT - U(56), BY0 + U(48)), "§ 02", font=MONO(26), fill=MORTAR, anchor="ra")
rule(d, LEFT + U(56), BY0 + U(102), RIGHT - U(56), (58, 62, 64), 2)

BENEFIT = [
    "Gaji pokok + insentif yang menarik",
    "Bonus pencapaian target",
    "Tunjangan operasional lapangan",
    "Jenjang karier & pelatihan produk",
]

fbn = BODY(50)
for i, b in enumerate(BENEFIT):
    yy = BY0 + U(148) + i * U(68)
    d.rectangle([LEFT + U(56), yy + U(25), LEFT + U(56) + U(34), yy + U(28)], fill=CLAY)
    d.text((LEFT + U(112), yy), b, font=fbn, fill=PAPER, anchor="la")


# ============================================================================
# VI.  FOOTING — the contact is the loudest instrument
# ============================================================================
rule(d, LEFT, U(2224), RIGHT, INK, 4)

track(d, (LEFT, U(2254)), "HUBUNGI / WHATSAPP", MONO_B(24), CLAY, U(7))
d.text((LEFT, U(2282)), KONTAK, font=DISPLAY(108), fill=INK, anchor="la")

d.text((RIGHT, U(2304)), NAMA_PERUSAHAAN, font=BODY_B(34), fill=INK, anchor="ra")
d.text((RIGHT, U(2352)), "PROSES SELEKSI TIDAK DIPUNGUT BIAYA",
       font=MONO(22), fill=MORTAR, anchor="ra")


# ============================================================================
# VII.  MATERIAL FINISH
# ============================================================================
img = img.resize((W, H), Image.LANCZOS)

grain = Image.effect_noise((W, H), 13).convert("L").filter(ImageFilter.GaussianBlur(0.4))
img = Image.blend(img, Image.merge("RGB", (grain,) * 3), 0.04)

vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.rectangle([0, 0, W, H], fill=22)
vd.rectangle([55, 55, W - 55, H - 55], fill=0)
vig = vig.filter(ImageFilter.GaussianBlur(70))
img = Image.composite(Image.new("RGB", (W, H), (196, 189, 176)), img, vig)

out = "/home/user/Order.githup.io/poster/lowongan-sales-bangunan"
img.save(out + ".png", dpi=(300, 300))
img.save(out + ".pdf", "PDF", resolution=200.0)
print("ok", img.size)
