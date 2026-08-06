#!/usr/bin/env python3
"""
SITE SIGNAL — poster lowongan kerja, format WhatsApp (portrait 1800x2700).

Palet industri konstruksi: navy tua, kuning safety, biru baja, beton.
Semua ilustrasi digambar sendiri dengan primitif vektor (bukan foto stok),
jadi bebas masalah lisensi.

Fokus: SYARAT dan BENEFIT, dengan tipografi besar untuk layar ponsel.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ----------------------------------------------------------------------------
# ISI DI SINI — satu-satunya bagian yang perlu diubah
# ----------------------------------------------------------------------------
NAMA_PERUSAHAAN = "CV HALIM IMANNUEL MAKMUR"
KONTAK          = "0852-1968-0709"

FONTS = "/root/.claude/skills/canvas-design/canvas-fonts"

W, H = 1800, 2800
SS = 2
CW, CH = W * SS, H * SS

# ----------------------------------------------------------------------------
# PALET — beton, baja, dan kuning keselamatan
# ----------------------------------------------------------------------------
PAPER = (237, 240, 242)      # beton terang
INK   = (17, 31, 43)         # navy tua
AMBER = (242, 169, 26)       # kuning safety
STEEL = (62, 100, 128)       # biru baja
MUTED = (128, 143, 152)      # abu dingin
FAINT = (213, 219, 223)
ONINK = (43, 62, 79)         # garis di atas navy

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


def line(draw, p0, p1, fill, w):
    draw.line([p0, p1], fill=fill, width=int(w * SS))


# ============================================================================
# I.  MASTHEAD — a dark site board, full bleed
# ============================================================================
MAST_BOT = U(930)
d.rectangle([0, 0, CW, MAST_BOT], fill=INK)

track(d, (LEFT, U(112)), "LOWONGAN KERJA", MONO(26), PAPER, U(9))
d.text((RIGHT, U(112)), "DIBUKA SEGERA", font=MONO_B(24), fill=AMBER, anchor="ra")
rule(d, LEFT, U(158), RIGHT, STEEL, 3)


# --- the monument ------------------------------------------------------------
DSIZE = 370
CAP_IN = 0.178 * DSIZE
fd = DISPLAY(DSIZE)
track(d, (LEFT, U(225 - CAP_IN)), "SALES", fd, PAPER, U(8))
track(d, (LEFT, U(570 - CAP_IN)), "BANGUNAN", fd, AMBER, U(8))

# penempatan mengisi udara di samping baris pertama
d.text((RIGHT, U(244)), "PENEMPATAN", font=MONO(22), fill=MUTED, anchor="ra")
for i, kota in enumerate(("SEMARANG", "SALATIGA", "AMBARAWA")):
    d.text((RIGHT, U(284 + i * 48)), kota, font=BODY_B(40), fill=PAPER, anchor="ra")
d.rectangle([RIGHT + U(1), U(288), RIGHT + U(1), U(288)], fill=INK)


# ============================================================================
# II.  PERKAKAS & SANITASI — empat spesimen berdiri di atas satu datum
# ============================================================================
GROUND = U(1250)
NSLOT = 4
SLOTW = U(310)
SGAP = (COLW - SLOTW * NSLOT) / (NSLOT - 1)


def slot_x(i):
    return LEFT + i * (SLOTW + SGAP)


def keran(x0):
    """Keran taman: tiang, badan katup, cerat melengkung, gagang T."""
    cx = x0 + SLOTW * 0.36
    d.rectangle([cx - U(54), GROUND - U(20), cx + U(54), GROUND], fill=INK)
    d.rectangle([cx - U(25), GROUND - U(150), cx + U(25), GROUND - U(20)], fill=INK)
    d.rounded_rectangle([cx - U(40), GROUND - U(205), cx + U(40), GROUND - U(145)],
                        radius=U(16), fill=INK)
    # cerat
    d.rectangle([cx + U(34), GROUND - U(190), cx + U(118), GROUND - U(158)], fill=INK)
    d.rectangle([cx + U(86), GROUND - U(190), cx + U(118), GROUND - U(96)], fill=INK)
    d.rectangle([cx + U(80), GROUND - U(102), cx + U(124), GROUND - U(84)], fill=STEEL)
    # tetes air
    dx, dy = cx + U(102), GROUND - U(52)
    d.ellipse([dx - U(11), dy - U(9), dx + U(11), dy + U(13)], fill=STEEL)
    d.polygon([(dx - U(9), dy - U(4)), (dx + U(9), dy - U(4)), (dx, dy - U(24))],
              fill=STEEL)
    # gagang
    d.rectangle([cx - U(9), GROUND - U(243), cx + U(9), GROUND - U(198)], fill=INK)
    d.rounded_rectangle([cx - U(52), GROUND - U(262), cx + U(52), GROUND - U(236)],
                        radius=U(12), fill=AMBER)


def tandon(x0):
    """Tandon air di atas dudukan baja."""
    cx = x0 + SLOTW / 2
    # dudukan
    d.polygon([(cx - U(88), GROUND - U(38)), (cx - U(66), GROUND - U(38)),
               (cx - U(52), GROUND), (cx - U(76), GROUND)], fill=INK)
    d.polygon([(cx + U(66), GROUND - U(38)), (cx + U(88), GROUND - U(38)),
               (cx + U(76), GROUND), (cx + U(52), GROUND)], fill=INK)
    d.rectangle([cx - U(96), GROUND - U(50), cx + U(96), GROUND - U(34)], fill=INK)
    # badan tangki
    d.rounded_rectangle([cx - U(78), GROUND - U(252), cx + U(78), GROUND - U(50)],
                        radius=U(44), fill=AMBER)
    for gy in (U(196), U(160), U(124)):
        d.rectangle([cx - U(78), GROUND - gy, cx + U(78), GROUND - gy + U(9)], fill=INK)
    # tutup
    d.rectangle([cx - U(24), GROUND - U(272), cx + U(24), GROUND - U(246)], fill=INK)


def palu(x0):
    """Palu cakar."""
    cx = x0 + SLOTW * 0.46
    d.rectangle([cx - U(16), GROUND - U(200), cx + U(16), GROUND], fill=INK)
    d.rounded_rectangle([cx - U(20), GROUND - U(88), cx + U(20), GROUND - U(4)],
                        radius=U(10), fill=AMBER)
    d.rectangle([cx - U(28), GROUND - U(252), cx + U(92), GROUND - U(208)], fill=INK)
    d.rectangle([cx + U(78), GROUND - U(258), cx + U(98), GROUND - U(202)], fill=INK)
    d.arc([cx - U(74), GROUND - U(258), cx + U(18), GROUND - U(166)],
          182, 274, fill=INK, width=int(21 * SS))


def obeng(x0):
    """Obeng min."""
    cx = x0 + SLOTW / 2
    d.polygon([(cx - U(13), GROUND - U(26)), (cx + U(13), GROUND - U(26)),
               (cx + U(9), GROUND), (cx - U(9), GROUND)], fill=STEEL)
    d.rectangle([cx - U(9), GROUND - U(150), cx + U(9), GROUND - U(22)], fill=STEEL)
    d.rectangle([cx - U(17), GROUND - U(166), cx + U(17), GROUND - U(146)], fill=INK)
    d.rounded_rectangle([cx - U(43), GROUND - U(272), cx + U(43), GROUND - U(158)],
                        radius=U(32), fill=AMBER)
    for i in range(3):
        gx = cx - U(28) + i * U(25)
        d.rectangle([gx, GROUND - U(252), gx + U(8), GROUND - U(180)], fill=INK)


MATERIALS = [(keran, "KERAN"), (tandon, "TANDON"),
             (palu, "PALU"), (obeng, "OBENG")]

for i, (fn_, label) in enumerate(MATERIALS):
    fn_(slot_x(i))

rule(d, LEFT, GROUND, RIGHT, INK, 4)

flab = MONO(21)
for i, (_, label) in enumerate(MATERIALS):
    cx = slot_x(i) + SLOTW / 2
    d.rectangle([cx - SS, GROUND + U(8), cx + SS * 2 - 1, GROUND + U(20)], fill=MUTED)
    track(d, (cx - track_w(d, label, flab, U(4)) / 2, GROUND + U(30)),
          label, flab, MUTED, U(4))


# ============================================================================
# III.  SYARAT
# ============================================================================
rule(d, LEFT, U(1360), RIGHT, INK, 4)
track(d, (LEFT, U(1388)), "SYARAT", MONO_B(34), INK, U(9))
d.text((RIGHT, U(1392)), "01", font=MONO_B(26), fill=MUTED, anchor="ra")

SYARAT = [
    "Pengalaman min. 1 tahun di bidang bangunan",
    "Kemampuan komunikasi & negosiasi yang baik",
    "Bertanggung jawab dan jujur",
    "Siap bekerja di bawah tekanan dan target",
    "Bersedia ditempatkan di Semarang, Salatiga, Ambarawa",
    "Diutamakan berdomisili di Semarang",
]

fs, fn = BODY(50), MONO_B(30)
sy = 1474
for i, s in enumerate(SYARAT):
    yy = U(sy + i * 82)
    d.rectangle([LEFT, yy + U(4), LEFT + U(58), yy + U(52)], fill=AMBER)
    d.text((LEFT + U(29), yy + U(28)), f"{i + 1:02d}", font=fn, fill=INK, anchor="mm")
    d.text((LEFT + U(88), yy), s, font=fs, fill=INK, anchor="la")
    if i < len(SYARAT) - 1:
        rule(d, LEFT + U(88), U(sy + i * 82 + 66), RIGHT, FAINT, 1)


# ============================================================================
# IV.  BENEFIT
# ============================================================================
BY0, BY1 = U(2000), U(2444)
d.rectangle([LEFT, BY0, RIGHT, BY1], fill=INK)
d.rectangle([LEFT, BY0, LEFT + U(14), BY1], fill=AMBER)

track(d, (LEFT + U(58), BY0 + U(44)), "BENEFIT", MONO_B(34), PAPER, U(9))
d.text((RIGHT - U(56), BY0 + U(48)), "02", font=MONO_B(26), fill=MUTED, anchor="ra")
rule(d, LEFT + U(58), BY0 + U(102), RIGHT - U(56), ONINK, 2)

BENEFIT = [
    "Gaji pokok + insentif yang menarik",
    "Bonus pencapaian target",
    "Tunjangan operasional lapangan",
    "Jenjang karier & pelatihan produk",
]

fbn = BODY(50)
for i, b in enumerate(BENEFIT):
    yy = BY0 + U(148) + i * U(68)
    d.rectangle([LEFT + U(58), yy + U(24), LEFT + U(58) + U(30), yy + U(28)], fill=AMBER)
    d.text((LEFT + U(114), yy), b, font=fbn, fill=PAPER, anchor="la")


# ============================================================================
# V.  FOOTING — kontak sebagai instrumen paling nyaring
# ============================================================================
rule(d, LEFT, U(2510), RIGHT, INK, 4)

lab = "HUBUNGI / WHATSAPP"
flb = MONO_B(24)
lw = track_w(d, lab, flb, U(7)) + U(28)
d.rectangle([LEFT, U(2532), LEFT + lw, U(2576)], fill=AMBER)
track(d, (LEFT + U(14), U(2542)), lab, flb, INK, U(7))
d.text((LEFT, U(2578)), KONTAK, font=DISPLAY(108), fill=INK, anchor="la")

d.text((RIGHT, U(2594)), NAMA_PERUSAHAAN, font=BODY_B(34), fill=INK, anchor="ra")
d.text((RIGHT, U(2642)), "PROSES SELEKSI TIDAK DIPUNGUT BIAYA",
       font=MONO(22), fill=MUTED, anchor="ra")


# ============================================================================
# VI.  FINISH
# ============================================================================
img = img.resize((W, H), Image.LANCZOS)
grain = Image.effect_noise((W, H), 12).convert("L").filter(ImageFilter.GaussianBlur(0.4))
img = Image.blend(img, Image.merge("RGB", (grain,) * 3), 0.032)

out = "/home/user/Order.githup.io/poster/lowongan-sales-bangunan"
img.save(out + ".png", dpi=(300, 300))
img.save(out + ".pdf", "PDF", resolution=200.0)
print("ok", img.size)
