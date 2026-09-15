# -*- coding: utf-8 -*-
"""Genera la card del header del README: VISUAL.MAP + SYSTEM.INFO, en claro y oscuro.

Todo es un unico SVG sin JS ni fuentes externas, porque GitHub sirve la imagen
del README dentro de un <img>: ahi corren CSS y SMIL, y nada mas.

La VISUAL.MAP cicla cuatro figuras hechas con la misma nube de puntos. El ciclo
es un disolvido -- cada figura se arma escalando y se deshace -- y no un morph
punto a punto: eso ultimo pide dos <animate> por punto y duplica el peso del
archivo, que en un README se paga en cada visita.
"""
import io, math, random

# --- lienzo ---------------------------------------------------------------
PAD, GAP = 14, 16
MAP_W, PANEL_W, BODY_H = 300, 404, 340
W = PAD * 2 + MAP_W + GAP + PANEL_W
H = PAD * 2 + BODY_H
SEED = 7
CX, CY = 150, 170          # centro de la VISUAL.MAP

# --- nube -----------------------------------------------------------------
# los puntos van por figura: a igual cantidad, un trazo grueso se ralea
# y uno fino se empasta.
CYCLE = 18.0               # segundos de vuelta completa
TWINKLE = 0.30             # fraccion de puntos que titila
K_GROUPS = 7               # fases de titileo, para que no lateen todos juntos

RADS = [0.62, 0.95, 1.45]
OPS = [1.0, 0.82, 0.55, 0.3]


# --- figuras --------------------------------------------------------------
def glyph():
    """El </> de dev. Trazo grueso: es la figura ancla, tiene que pesar."""
    polys = [
        [(112, 96), (56, 170), (112, 244)],   # <
        [(128, 252), (172, 88)],              # /
        [(188, 96), (244, 170), (188, 244)],  # >
    ]
    s = 1.12
    return [[(CX + (x - CX) * s, CY + (y - CY) * s) for x, y in p] for p in polys], 9.5, 2000


def ring():
    """Anillo con nucleo: el estado en reposo."""
    def circle(r, n=110):
        return [(CX + r * math.cos(2 * math.pi * i / n),
                 CY + r * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
    spokes = []
    for i in range(12):
        a = 2 * math.pi * i / 12
        spokes.append([(CX + 46 * math.cos(a), CY + 46 * math.sin(a)),
                       (CX + 62 * math.cos(a), CY + 62 * math.sin(a))])
    return [circle(96), circle(38)] + spokes, 5.0, 1150


def grid():
    """Reticula de nodos y aristas: la figura 'sistema'."""
    step, n = 50, 4
    x0 = CX - step * (n - 1) / 2
    y0 = CY - step * (n - 1) / 2
    paths = []
    for i in range(n):
        paths.append([(x0, y0 + i * step), (x0 + step * (n - 1), y0 + i * step)])
        paths.append([(x0 + i * step, y0), (x0 + i * step, y0 + step * (n - 1))])
    # diagonales sueltas, para que no sea una malla perfecta
    paths.append([(x0, y0), (x0 + step * (n - 1), y0 + step * (n - 1))])
    paths.append([(x0 + step * (n - 1), y0), (x0, y0 + step * (n - 1))])
    return paths, 4.2, 1150


def serpentine():
    """La onda que le da el nombre a FS/SERPENTINE."""
    paths = []
    for k, amp in ((0, 64), (1, 40)):
        pts = []
        for i in range(161):
            t = i / 160
            x = CX - 115 + 230 * t
            y = CY + amp * math.sin(2 * math.pi * (1.5 * t) + k * math.pi / 2)
            pts.append((x, y))
        paths.append(pts)
    return paths, 5.5, 1050


SHAPES = [("GLYPH-CLOUD", glyph), ("ORBIT", ring),
          ("LATTICE", grid), ("SERPENTINE", serpentine)]


# --- muestreo -------------------------------------------------------------
def sample(paths, half, n_pts, rnd):
    """Reparte n_pts a lo largo de las polilineas, con grosor y jitter."""
    segs = []
    for poly in paths:
        for a, b in zip(poly, poly[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            if L > 0.01:
                segs.append((a, b, L))
    total = sum(s[2] for s in segs)

    pts = []
    for a, b, L in segs:
        dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        px, py = -dy, dx                                   # perpendicular unitaria
        for _ in range(max(1, int(round(n_pts * L / total)))):
            t = rnd.random() * L
            if rnd.random() < 0.10:                        # los que se escapan
                off = math.copysign(half * (1.1 + rnd.random() * 1.5), rnd.random() - 0.5)
            else:
                # potencia < 1 aplana el centro: densidad pareja a lo ancho
                off = math.copysign(half * rnd.random() ** 0.72, rnd.random() - 0.5)
            jit = rnd.gauss(0, 1.6)                        # jitter sobre el eje
            pts.append((a[0] + dx * t + px * off + dx * jit,
                        a[1] + dy * t + py * off + dy * jit,
                        min(1.0, abs(off) / (half * 1.25)),
                        rnd.random()))
    rnd.shuffle(pts)
    return pts


def classify(edge, roll):
    r = 2 if roll < 0.05 else (1 if roll < 0.26 else 0)
    # el dorado es minoria y vive en el centro; el resto es azul que se apaga
    if edge < 0.30 and roll < 0.34:
        c = 0
    elif edge < 0.55:
        c = 1
    elif edge < 0.80:
        c = 2
    else:
        c = 3
    return r, c


def phase_delay(i, n):
    """Retardo negativo para que la figura 0 este a la vista en t=0.

    Con un retardo que caiga fuera de la ventana visible de cada figura, el
    primer fotograma sale en blanco: es lo que ve quien abre el README y lo que
    captura cualquier miniatura.
    """
    return -CYCLE * ((0.12 - 1.0 / n * i) % 1.0)


# --- contenido del panel --------------------------------------------------
ROWS = [
    ("Subject",       "Juan M. Decoud"),
    ("Role",          "Support & AI Automation Eng."),
    ("Origin",        "Buenos Aires, AR"),
    ("Education",     "Computer Eng. / U. Austral"),
    ("Status",        "Building / Shipping"),
    (None, None),
    ("Core.Lang",     "Python / TypeScript / Rust"),
    ("Core.Web",      "React / NestJS / PySide6"),
    ("Core.Data",     "PostgreSQL / SQLite / Prisma"),
    ("Core.Infra",    "Azure / Docker / Actions"),
    ("Core.Auto",     "n8n / Zapier / HubSpot"),
    (None, None),
    ("Grid.Site",     "decoudjuan.github.io"),
    ("Grid.LinkedIn", "/in/decoudjuan"),
    ("Grid.GitHub",   "DecoudJuan"),
]

THEMES = {
    "dark":  dict(bg="#0f1319", card="#11151c", frame="#2c3646", label="#5d6b80",
                  dim="#39465a", value="#c6d0de", accent="#e6c46a", scan="#4a6fa5",
                  live="#5ea87a", cols=["#e6c46a", "#8fb0de", "#5e82b8", "#3f5a85"]),
    "light": dict(bg="#ffffff", card="#f6f7f9", frame="#c8cfda", label="#7b8698",
                  dim="#aab3c0", value="#2b3340", accent="#a8801f", scan="#7d97bd",
                  live="#2f7a4f", cols=["#a8801f", "#3f6aa8", "#6d8cb6", "#9aabc4"]),
}

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(theme):
    t = THEMES[theme]
    n = len(SHAPES)
    slot = 100.0 / n          # porcentaje del ciclo por figura
    o = io.StringIO()
    o.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" '
            'height="%d" role="img" aria-label="Juan M. Decoud - Support and AI Automation '
            'Engineer, Buenos Aires. Python, TypeScript, Rust.">\n' % (W, H, W, H))

    # --- estilos ---
    o.write('<style>')
    for i, c in enumerate(t["cols"]):
        # fill-opacity es la base; la animacion mueve `opacity`, y se multiplican
        o.write('.c%d{fill:%s;fill-opacity:%s}' % (i, c, OPS[i]))
    o.write('@keyframes tw{0%,100%{opacity:.30}50%{opacity:1}}')
    for i in range(K_GROUPS):
        o.write('.k%d{animation:tw %.2fs ease-in-out infinite;animation-delay:-%.2fs}'
                % (i, 2.6 + 0.47 * i, i * 0.83))
    # cada figura esta viva un turno: entra escalando, se sostiene, se deshace
    o.write('@keyframes cy{0%%{opacity:0;transform:scale(.93)}'
            '%.1f%%{opacity:1;transform:scale(1)}'
            '%.1f%%{opacity:1;transform:scale(1)}'
            '%.1f%%{opacity:0;transform:scale(1.06)}'
            '100%%{opacity:0;transform:scale(.93)}}'
            % (slot * 0.22, slot * 0.80, slot))
    for i in range(n):
        o.write('.s%d{animation:cy %.1fs ease-in-out infinite;animation-delay:%.2fs;'
                'transform-box:view-box;transform-origin:%dpx %dpx}'
                % (i, CYCLE, phase_delay(i, n), CX, CY))
    # el nombre de la figura entra y sale con ella, pero sin escalar:
    # el scale de `cy` se resuelve contra el view-box y correria el texto
    o.write('@keyframes cyo{0%%{opacity:0}%.1f%%{opacity:1}%.1f%%{opacity:1}'
            '%.1f%%{opacity:0}100%%{opacity:0}}'
            % (slot * 0.22, slot * 0.80, slot))
    for i in range(n):
        o.write('.n%d{animation:cyo %.1fs ease-in-out infinite;animation-delay:%.2fs}'
                % (i, CYCLE, phase_delay(i, n)))
    o.write('@keyframes sweep{from{transform:translateY(-16%)}to{transform:translateY(116%)}}')
    o.write('.sweep{animation:sweep 7s linear infinite}')
    o.write('@keyframes blink{0%,100%{opacity:1}50%{opacity:.25}}')
    o.write('.live{animation:blink 2s ease-in-out infinite}')
    o.write('.fr{fill:none;stroke:%s;stroke-width:1.1}' % t["frame"])
    o.write('text{font-family:%s;letter-spacing:.9px}' % MONO)
    o.write('.lb{font-size:9px;fill:%s}' % t["label"])
    o.write('.dm{font-size:9px;fill:%s}' % t["dim"])
    o.write('.vl{font-size:10px;fill:%s}' % t["value"])
    o.write('.ac{font-size:9px;fill:%s}' % t["accent"])
    # quien pidio menos movimiento ve la primera figura, quieta
    shape_sel = ",".join(".s%d,.n%d" % (i, i) for i in range(n))
    o.write('@media(prefers-reduced-motion:reduce){'
            '[class*="k"],.live{animation:none}.sweep{display:none}'
            '%s{animation:none;opacity:0}.s0,.n0{opacity:1}}' % shape_sel)
    o.write('</style>\n')

    o.write('<rect width="%d" height="%d" fill="%s"/>\n' % (W, H, t["bg"]))

    # ---------------- panel izquierdo: VISUAL.MAP ----------------
    o.write('<g transform="translate(%d,%d)">\n' % (PAD, PAD))
    o.write('<rect width="%d" height="%d" rx="6" fill="%s" stroke="%s" stroke-width="1"/>\n'
            % (MAP_W, BODY_H, t["card"], t["frame"]))
    m, l = 13, 19
    for sx, sy, cx, cy in ((1, 1, m, m), (-1, 1, MAP_W - m, m),
                           (1, -1, m, BODY_H - m), (-1, -1, MAP_W - m, BODY_H - m)):
        o.write('<path class="fr" d="M%d %dV%dH%d"/>' % (cx, cy + sy * l, cy, cx + sx * l))
    o.write('\n')

    rnd = random.Random(SEED)
    total = 0
    counts = []
    for i, (name, fn) in enumerate(SHAPES):
        paths, half, n_pts = fn()
        kept = 0
        o.write('<g class="s%d">' % i)
        for x, y, edge, roll in sample(paths, half, n_pts, rnd):
            if not (m + 4 < x < MAP_W - m - 4 and m + 16 < y < BODY_H - m - 16):
                continue
            r, c = classify(edge, roll)
            # el radio va como atributo: la propiedad CSS de geometria `r` no existe
            # en renderers viejos y los circulos saldrian invisibles
            k = ' k%d' % (int(roll * 1000) % K_GROUPS) if roll < TWINKLE else ''
            o.write('<circle class="c%d%s" cx="%.1f" cy="%.1f" r="%s"/>' % (c, k, x, y, RADS[r]))
            kept += 1
        counts.append(kept)
        total += kept
        o.write('</g>\n')

    o.write('<linearGradient id="sw-%s" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="%s" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="%s" stop-opacity=".5"/>'
            '<stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>\n'
            % (theme, t["scan"], t["scan"], t["scan"]))
    o.write('<rect class="sweep" x="%d" y="0" width="%d" height="46" fill="url(#sw-%s)"/>\n'
            % (m + 4, MAP_W - 2 * m - 8, theme))
    o.write('<text class="lb" x="%d" y="%d">VISUAL.MAP</text>' % (m + 26, m + 2))
    o.write('<text class="dm" x="%d" y="%d" text-anchor="end">%dx%d / 1-BIT</text>'
            % (MAP_W - m - 26, m + 2, MAP_W, BODY_H))
    # el pie nombra la figura que esta en pantalla
    for i, (name, _) in enumerate(SHAPES):
        o.write('<text class="dm n%d" x="%d" y="%d">PTS %d / %s</text>'
                % (i, m + 26, BODY_H - m - 2, counts[i], name))
    o.write('\n</g>\n')

    # ---------------- panel derecho: SYSTEM.INFO ----------------
    o.write('<g transform="translate(%d,%d)">\n' % (PAD + MAP_W + GAP, PAD))
    o.write('<rect width="%d" height="%d" rx="6" fill="%s" stroke="%s" stroke-width="1"/>\n'
            % (PANEL_W, BODY_H, t["card"], t["frame"]))
    ix, iw = 18, PANEL_W - 36
    o.write('<text class="lb" x="%d" y="26">SYSTEM.INFO</text>' % ix)
    # @DecoudJuan mide ~70px en 9px mono; el badge arranca bien a su izquierda
    o.write('<circle class="live" cx="%d" cy="22" r="3" fill="%s"/>' % (ix + iw - 118, t["live"]))
    o.write('<text class="dm" x="%d" y="26">LIVE</text>' % (ix + iw - 108))
    o.write('<text class="ac" x="%d" y="26" text-anchor="end">@DecoudJuan</text>\n' % (ix + iw))
    o.write('<line x1="%d" y1="36" x2="%d" y2="36" stroke="%s"/>\n' % (ix, ix + iw, t["frame"]))

    y = 56
    for label, value in ROWS:
        if label is None:
            y += 9
            continue
        o.write('<text class="lb" x="%d" y="%d">%s</text>' % (ix, y, esc(label)))
        o.write('<text class="vl" x="%d" y="%d" text-anchor="end">%s</text>\n'
                % (ix + iw, y, esc(value)))
        y += 19

    o.write('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>\n'
            % (ix, BODY_H - 30, ix + iw, BODY_H - 30, t["frame"]))
    o.write('<circle class="live" cx="%d" cy="%d" r="3" fill="%s"/>'
            % (ix + 4, BODY_H - 17, t["live"]))
    o.write('<text class="dm" x="%d" y="%d">ALL SYSTEMS NOMINAL</text>' % (ix + 14, BODY_H - 13))
    o.write('<text class="dm" x="%d" y="%d" text-anchor="end">UTC-3 / BUENOS AIRES</text>\n'
            % (ix + iw, BODY_H - 13))
    o.write('</g>\n</svg>\n')
    return o.getvalue(), total


if __name__ == "__main__":
    for theme in THEMES:
        svg, total = build(theme)
        path = "header-%s.svg" % theme
        io.open(path, "w", encoding="utf-8").write(svg)
        print(path, len(svg) // 1024, "KB,", total, "puntos,",
              len(SHAPES), "figuras")
