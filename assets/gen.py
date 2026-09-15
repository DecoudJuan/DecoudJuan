# -*- coding: utf-8 -*-
"""Genera la card del header del README: VISUAL.MAP + SYSTEM.INFO, en claro y oscuro.

Todo es un unico SVG sin JS ni fuentes externas, porque GitHub sirve la imagen
del README dentro de un <img>: ahi corren CSS y SMIL, y nada mas.

La VISUAL.MAP cicla cuatro figuras y los puntos VIAJAN de una a la otra: es la
misma nube reacomodandose, no un disolvido. Cada punto lleva sus tres destinos
en custom properties y un unico @keyframes los usa. Eso se eligio sobre SMIL
(<animateTransform> por punto) por dos razones: pesa la mitad, y se puede apagar
con prefers-reduced-motion, cosa que a SMIL no se le puede pedir desde CSS.

El destino se guarda como desplazamiento relativo a la primera figura, que es la
que va en cx/cy. Si el navegador no resolviera las variables, la card se queda
quieta en el </> en vez de amontonar todos los puntos en el origen.
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
N_PTS = 1500               # la misma nube en todas las figuras: los puntos viajan
CYCLE = 20.0               # segundos de vuelta completa
HOLD = 0.18                # del ciclo, cuanto se queda quieta cada figura
                           # (con 4 figuras el turno es 25%: 18% quieta, 7% viajando)
TWINKLE = 0.30             # fraccion de puntos que titila
K_GROUPS = 7               # fases de titileo, para que no lateen todos juntos

RADS = [0.62, 0.95, 1.45]
OPS = [1.0, 0.82, 0.55, 0.3]


# --- figuras --------------------------------------------------------------
def glyph():
    """El </> de dev. Es la figura ancla y la que queda si algo falla."""
    polys = [
        [(112, 96), (56, 170), (112, 244)],   # <
        [(128, 252), (172, 88)],              # /
        [(188, 96), (244, 170), (188, 244)],  # >
    ]
    s = 1.12
    return [[(CX + (x - CX) * s, CY + (y - CY) * s) for x, y in p] for p in polys], 8.6


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
    return [circle(96), circle(38)] + spokes, 5.0


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
    return paths, 4.2


def serpentine():
    """La onda que le da el nombre a FS/SERPENTINE."""
    paths = []
    for k, amp in ((0, 64), (1, 40)):
        pts = []
        for i in range(161):
            t = i / 160
            paths_x = CX - 115 + 230 * t
            pts.append((paths_x, CY + amp * math.sin(2 * math.pi * 1.5 * t + k * math.pi / 2)))
        paths.append(pts)
    return paths, 5.5


SHAPES = [("GLYPH-CLOUD", glyph), ("ORBIT", ring),
          ("LATTICE", grid), ("SERPENTINE", serpentine)]


# --- muestreo -------------------------------------------------------------
def sample(paths, half, n_pts, rnd):
    """Exactamente n_pts sobre las polilineas, con grosor y jitter.

    Devuelve (x, y, borde 0..1). El borde solo se usa en la primera figura,
    para pintar: el color de un punto no cambia cuando viaja.
    """
    segs = []
    for poly in paths:
        for a, b in zip(poly, poly[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            if L > 0.01:
                segs.append((a, b, L))
    total = sum(s[2] for s in segs)

    pts = []
    while len(pts) < n_pts:
        for a, b, L in segs:
            dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
            px, py = -dy, dx                               # perpendicular unitaria
            for _ in range(max(1, int(round(n_pts * L / total)))):
                if len(pts) >= n_pts:
                    break
                t = rnd.random() * L
                if rnd.random() < 0.10:                    # los que se escapan
                    off = math.copysign(half * (1.1 + rnd.random() * 1.5), rnd.random() - 0.5)
                else:
                    # potencia < 1 aplana el centro: densidad pareja a lo ancho
                    off = math.copysign(half * rnd.random() ** 0.72, rnd.random() - 0.5)
                jit = rnd.gauss(0, 1.6)                    # jitter sobre el eje
                x = a[0] + dx * t + px * off + dx * jit
                y = a[1] + dy * t + py * off + dy * jit
                # recortar aca y no al escribir: las cuatro figuras tienen que
                # terminar con la misma cantidad de puntos para poder emparejarse
                x = min(max(x, 20.0), MAP_W - 20.0)
                y = min(max(y, 32.0), BODY_H - 32.0)
                pts.append((x, y, min(1.0, abs(off) / (half * 1.25))))
    return pts[:n_pts]


def by_angle(pts):
    """Ordena por angulo alrededor del centro.

    Es lo que empareja un punto de una figura con el de la siguiente: al viajar
    cada uno se queda en su sector, la nube gira y se reacomoda en vez de
    cruzarse en diagonal contra si misma.
    """
    return sorted(pts, key=lambda p: (math.atan2(p[1] - CY, p[0] - CX),
                                      math.hypot(p[0] - CX, p[1] - CY)))


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


def keyframes_move(n):
    """El viaje: quieto en cada figura, y el traslado entre una y la siguiente."""
    slot = 1.0 / n
    out = ["@keyframes mv{"]
    for i in range(n):
        a, b = 100 * slot * i, 100 * (slot * i + HOLD)
        tr = "translate(0,0)" if i == 0 else "translate(var(--p%d))" % i
        out.append("%.4g%%,%.4g%%{transform:%s}" % (a, b, tr))
    out.append("100%{transform:translate(0,0)}}")
    return "".join(out)


def build(theme):
    t = THEMES[theme]
    n = len(SHAPES)
    rnd = random.Random(SEED)

    # las cuatro figuras, emparejadas punto a punto por sector angular
    clouds = [by_angle(sample(*fn(), N_PTS, rnd)) for _, fn in SHAPES]

    o = io.StringIO()
    o.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" '
            'height="%d" role="img" aria-label="Juan M. Decoud - Support and AI Automation '
            'Engineer, Buenos Aires. Python, TypeScript, Rust.">\n' % (W, H, W, H))

    # --- estilos ---
    o.write('<style>')
    for i, c in enumerate(t["cols"]):
        # fill-opacity es la base; el titileo mueve `opacity`, y se multiplican
        o.write('.c%d{fill:%s;fill-opacity:%s}' % (i, c, OPS[i]))
    o.write(keyframes_move(n))
    o.write('@keyframes tw{0%,100%{opacity:.35}50%{opacity:1}}')
    # el viaje solo, y el viaje mas titileo: van juntos en una sola declaracion
    # porque `animation` es shorthand y dos reglas sueltas se pisarian
    o.write('.mv{animation:mv %.1fs ease-in-out infinite}' % CYCLE)
    for i in range(K_GROUPS):
        o.write('.mk%d{animation:mv %.1fs ease-in-out %.2fs infinite,'
                'tw %.2fs ease-in-out -%.2fs infinite}'
                % (i, CYCLE, -0.06 * i, 2.6 + 0.47 * i, i * 0.83))
    o.write('@keyframes lbl{0%,18%{opacity:1}21%,97%{opacity:0}100%{opacity:1}}')
    for i in range(n):
        o.write('.n%d{animation:lbl %.1fs linear %.2fs infinite}'
                % (i, CYCLE, -CYCLE * i / n))
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
    # quien pidio menos movimiento ve el </> quieto, con su rotulo
    labels = ",".join(".n%d" % i for i in range(n))
    o.write('@media(prefers-reduced-motion:reduce){'
            '.mv,[class*="mk"],.live{animation:none}.sweep{display:none}'
            '%s{animation:none;opacity:0}.n0{opacity:1}}' % labels)
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
    o.write('\n<g>')
    for j in range(N_PTS):
        x, y, edge = clouds[0][j]
        roll = rnd.random()
        r, c = classify(edge, roll)
        cls = 'mk%d' % (int(roll * 1000) % K_GROUPS) if roll < TWINKLE else 'mv'
        # destinos relativos a la primera figura: si las variables no se
        # resolvieran, el punto se queda donde esta y no salta al origen
        # con coma: translate() la exige entre argumentos, y sin ella el
        # transform entero es invalido y se descarta en silencio
        dest = ";".join("--p%d:%.1fpx,%.1fpx" % (i, clouds[i][j][0] - x, clouds[i][j][1] - y)
                        for i in range(1, len(clouds)))
        # el radio va como atributo: la propiedad CSS de geometria `r` no existe
        # en renderers viejos y los circulos saldrian invisibles
        o.write('<circle class="c%d %s" cx="%.1f" cy="%.1f" r="%s" style="%s"/>'
                % (c, cls, x, y, RADS[r], dest))
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
                % (i, m + 26, BODY_H - m - 2, N_PTS, name))
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
    return o.getvalue()


if __name__ == "__main__":
    for theme in THEMES:
        svg = build(theme)
        path = "header-%s.svg" % theme
        io.open(path, "w", encoding="utf-8").write(svg)
        print(path, len(svg) // 1024, "KB,", N_PTS, "puntos,", len(SHAPES), "figuras")
