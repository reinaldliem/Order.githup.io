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

W, H = 1800, 2700
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
MAST_BOT = U(820)
d.rectangle([0, 0, CW, MAST_BOT], fill=INK)

track(d, (LEFT, U(112)), "LOWONGAN KERJA", MONO(26), PAPER, U(9))
d.text((RIGHT, U(112)), "DIBUKA SEGERA", font=MONO_B(24), fill=AMBER, anchor="ra")
rule(d, LEFT, U(158), RIGHT, STEEL, 3)


# --- tower crane, drawn in steel behind the type -----------------------------
def crane():
    mx, top, base = U(1540), U(258), U(720)
    r1, r2 = mx - U(26), mx + U(26)
    # mast rails
    d.rectangle([r1, top, r1 + U(7), base], fill=STEEL)
    d.rectangle([r2 - U(7), top, r2, base], fill=STEEL)
    # lattice bracing
    step = U(62)
    y = top
    flip = True
    while y + step <= base:
        a, b = (r1, y), (r2, y + step)
        c_, e_ = (r2, y), (r1, y + step)
        line(d, a, b, STEEL, 4) if flip else line(d, c_, e_, STEEL, 4)
        d.rectangle([r1, y, r2, y + U(3)], fill=STEEL)
        flip = not flip
        y += step
    d.rectangle([r1, base - U(3), r2, base], fill=STEEL)

    # jib (left) and counter-jib (right)
    jl, jr = U(1128), U(1688)
    jt, jb = U(262), U(290)
    d.rectangle([jl, jt, mx, jt + U(6)], fill=STEEL)
    d.rectangle([jl, jb, mx, jb + U(6)], fill=STEEL)
    x = jl
    up = True
    while x + U(70) <= mx:
        line(d, (x, jb), (x + U(70), jt), STEEL, 4) if up else \
            line(d, (x, jt), (x + U(70), jb), STEEL, 4)
        up = not up
        x += U(70)
    d.rectangle([mx, jt, jr, jt + U(6)], fill=STEEL)
    d.rectangle([mx, jb, jr, jb + U(6)], fill=STEEL)
    d.rectangle([jr - U(58), jt - U(14), jr, jb + U(20)], fill=STEEL)   # counterweight

    # apex and tie bars
    apex = (mx, U(176))
    line(d, (r1, jt), apex, STEEL, 5)
    line(d, (r2, jt), apex, STEEL, 5)
    line(d, apex, (jl + U(16), jt), STEEL, 4)
    line(d, apex, (jr - U(20), jt), STEEL, 4)

    # trolley, cable and hook block
    hx = U(1352)
    d.rectangle([hx - U(26), jt - U(4), hx + U(26), jb + U(4)], fill=STEEL)
    line(d, (hx, jb), (hx, U(408)), STEEL, 4)
    d.rectangle([hx - U(24), U(408), hx + U(24), U(446)], fill=AMBER)


crane()

# --- the monument ------------------------------------------------------------
DSIZE = 260
CAP_IN = 0.178 * DSIZE
fd = DISPLAY(DSIZE)
track(d, (LEFT, U(230 - CAP_IN)), "SALES", fd, PAPER, U(8))
track(d, (LEFT, U(500 - CAP_IN)), "BANGUNAN", fd, AMBER, U(8))

rule(d, LEFT, U(742), RIGHT, ONINK, 2)
d.text((LEFT, U(766)), "PENEMPATAN", font=MONO(22), fill=MUTED, anchor="la")
d.text((RIGHT, U(762)), "SEMARANG · SALATIGA · AMBARAWA",
       font=BODY_B(26), fill=PAPER, anchor="ra")


# ============================================================================
# II.  THE YARD — material bangunan, digambar sebagai spesimen di atas datum
# ============================================================================
GROUND = U(1176)
SLOTW, NSLOT = U(250), 5
SGAP = (COLW - SLOTW * NSLOT) / (NSLOT - 1)


def slot_x(i):
    return LEFT + i * (SLOTW + SGAP)


def bata(x0):
    """Palet bata dengan susunan running bond."""
    pal_t = GROUND - U(20)
    d.rectangle([x0 + U(6), pal_t, x0 + SLOTW - U(6), GROUND - U(3)], fill=INK)
    for fx in (x0 + U(14), x0 + SLOTW / 2 - U(9), x0 + SLOTW - U(32)):
        d.rectangle([fx, GROUND - U(3), fx + U(18), GROUND], fill=INK)
    bw, bh, g = U(52), U(21), U(5)
    accent = {(1, 2), (3, 0), (4, 3)}
    for r in range(6):
        yb = pal_t - (r + 1) * (bh + g)
        shift = bw / 2 if r % 2 else 0
        for c in range(4):
            bx = x0 + U(15) + c * (bw + g) + shift
            if bx + bw > x0 + SLOTW - U(8):
                continue
            col = AMBER if (r, c) in accent else INK
            d.rectangle([bx, yb, bx + bw, yb + bh], fill=col)


def semen(x0):
    """Tumpukan sak semen."""
    sw, sh, rad = U(112), U(70), U(18)
    pos = [(x0 + U(8), GROUND - sh), (x0 + U(130), GROUND - sh),
           (x0 + U(69), GROUND - sh * 2 - U(9))]
    for i, (sx, sy) in enumerate(pos):
        d.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=rad, fill=INK)
        d.rectangle([sx + U(6), sy + sh / 2 - U(5), sx + sw - U(6),
                     sy + sh / 2 + U(5)], fill=AMBER if i == 2 else STEEL)
        line(d, (sx + U(14), sy + U(11)), (sx + sw - U(14), sy + U(11)), ONINK, 3)


def pipa(x0):
    """Susunan pipa, tampak ujung."""
    dia = U(62)
    for r, n in enumerate((4, 3, 2)):
        yb = GROUND - (r + 1) * dia
        xs = x0 + (SLOTW - n * dia) / 2
        for c in range(n):
            px = xs + c * dia
            box = [px + U(3), yb + U(3), px + dia - U(3), yb + dia - U(3)]
            fill = AMBER if (r, c) == (1, 1) else PAPER
            d.ellipse(box, fill=fill, outline=INK, width=int(7 * SS))
            inn = U(15)
            d.ellipse([box[0] + inn, box[1] + inn, box[2] - inn, box[3] - inn],
                      outline=STEEL, width=int(4 * SS))


def genteng(x0):
    """Tumpukan genteng miring."""
    w, slant, t = U(196), U(54), U(17)
    xs = x0 + (SLOTW - w) / 2
    for i in range(6):
        yb = GROUND - U(10) - i * U(32)
        col = AMBER if i == 5 else INK
        d.polygon([(xs, yb), (xs + w, yb - slant),
                   (xs + w, yb - slant + t), (xs, yb + t)], fill=col)
    d.rectangle([xs - U(8), GROUND - U(10), xs + U(22), GROUND], fill=STEEL)
    d.rectangle([xs + w - U(22), GROUND - U(10), xs + w + U(8), GROUND], fill=STEEL)


def cat(x0):
    """Kaleng cat dengan pegangan yang menyatu ke bibir kaleng."""
    for ox, col, band in ((U(10), INK, PAPER), (U(136), AMBER, INK)):
        bw_, bh_, rim = U(104), U(122), U(15)
        bx = x0 + ox
        by = GROUND - bh_
        # gagang, ujungnya bertemu bibir kaleng
        d.arc([bx + U(4), by - U(56), bx + bw_ - U(4), by + U(56)],
              180, 360, fill=STEEL, width=int(7 * SS))
        # badan silinder
        d.rectangle([bx, by, bx + bw_, GROUND - rim], fill=col)
        d.ellipse([bx, GROUND - rim * 2, bx + bw_, GROUND], fill=col)
        # bibir kaleng
        d.ellipse([bx, by - rim, bx + bw_, by + rim], fill=col,
                  outline=STEEL if col is INK else INK, width=int(5 * SS))
        d.ellipse([bx + U(16), by - rim + U(7), bx + bw_ - U(16), by + rim - U(7)],
                  outline=STEEL if col is INK else INK, width=int(3 * SS))
        # pita label
        d.rectangle([bx + U(11), by + U(46), bx + bw_ - U(11), by + U(60)], fill=band)


MATERIALS = [(bata, "BATA"), (semen, "SEMEN"), (pipa, "PIPA"),
             (genteng, "GENTENG"), (cat, "CAT")]

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
rule(d, LEFT, U(1290), RIGHT, INK, 4)
track(d, (LEFT, U(1318)), "SYARAT", MONO_B(34), INK, U(9))
d.text((RIGHT, U(1322)), "01", font=MONO_B(26), fill=MUTED, anchor="ra")

SYARAT = [
    "Pengalaman min. 1 tahun di bidang bangunan",
    "Kemampuan komunikasi & negosiasi yang baik",
    "Bertanggung jawab dan jujur",
    "Siap bekerja di bawah tekanan dan target",
    "Bersedia ditempatkan di Semarang, Salatiga, Ambarawa",
    "Diutamakan berdomisili di Semarang",
]

fs, fn = BODY(50), MONO_B(30)
sy = 1404
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
BY0, BY1 = U(1920), U(2364)
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
rule(d, LEFT, U(2430), RIGHT, INK, 4)

lab = "HUBUNGI / WHATSAPP"
flb = MONO_B(24)
lw = track_w(d, lab, flb, U(7)) + U(28)
d.rectangle([LEFT, U(2452), LEFT + lw, U(2496)], fill=AMBER)
track(d, (LEFT + U(14), U(2462)), lab, flb, INK, U(7))
d.text((LEFT, U(2500)), KONTAK, font=DISPLAY(108), fill=INK, anchor="la")

d.text((RIGHT, U(2516)), NAMA_PERUSAHAAN, font=BODY_B(34), fill=INK, anchor="ra")
d.text((RIGHT, U(2564)), "PROSES SELEKSI TIDAK DIPUNGUT BIAYA",
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
