# -*- coding: utf-8 -*-
"""Genera el header del README: el nombre sobre la madera de DecoudJuan OS, en claro y oscuro.

Todo es un unico SVG sin JS ni fuentes externas, porque GitHub sirve la imagen
del README dentro de un <img>: ahi corren CSS y SMIL, y nada mas. La veta es el
mismo feTurbulence que usa el portfolio (decoudjuan.github.io), asi que pesa
unos pocos KB y no una imagen.

Claro = roble, oscuro = nogal: los dos fondos del portfolio. Los detalles dorados
(marco, filete bajo el nombre, placa de freelance y bordes del dock) usan un solo
degrade de bronce en los dos temas.

El dock muestra lo que hace (los proyectos ya estan en el README). Los iconos son
Phosphor (duotone, MIT, https://phosphoricons.com), los mismos del portfolio, y
Portfolio lleva el pinguino.
"""
import io

W, H = 748, 368
CX = W // 2
SANS = "ui-sans-serif,system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'Cascadia Mono',Menlo,Consolas,monospace"

NAME = "Juan Manuel Decoud"
ROLE = "Support & AI Automation Engineer at Darwin AI · Computer Engineering, Universidad Austral"
WHERE = "BUENOS AIRES · UTC-3"
FREELANCE = "OPEN TO FREELANCE"

THEMES = {
    "light": dict(wood="#d6bc93", grain=0.2, vignette=0.22, ink="#1e1914", mut="#4f4232",
                  bar="#fbf8f2", bar_op=0.72, bar_ln="#c9b28c", tile="#fbf8f2",
                  tones=["#2f5d46", "#8a3324", "#a06a12", "#3a2c24"], plate_ink="#2e2008", live="#2f7a4f",
                  line="#94722a", frame_op=0.9),
    "dark": dict(wood="#3a2618", grain=0.45, vignette=0.45, ink="#f3e9dc", mut="#cdbba2",
                 bar="#1c1510", bar_op=0.6, bar_ln="#5a4430", tile="#3d332b",
                 tones=["#8cc4a2", "#e58f78", "#e9b65a", "#e6d8c2"], plate_ink="#2e2008", live="#2f7a4f",
                 line="#e3c77d", frame_op=0.75),
}

# Phosphor duotone (viewBox 256): [(d, opacidad o None), ...]
ICONS = {
    "Robot": [('M200,56H56A24,24,0,0,0,32,80V192a24,24,0,0,0,24,24H200a24,24,0,0,0,24-24V80A24,24,0,0,0,200,56ZM164,184H92a20,20,0,0,1,0-40h72a20,20,0,0,1,0,40Z', '0.2'), ('M200,48H136V16a8,8,0,0,0-16,0V48H56A32,32,0,0,0,24,80V192a32,32,0,0,0,32,32H200a32,32,0,0,0,32-32V80A32,32,0,0,0,200,48Zm16,144a16,16,0,0,1-16,16H56a16,16,0,0,1-16-16V80A16,16,0,0,1,56,64H200a16,16,0,0,1,16,16ZM72,108a12,12,0,1,1,12,12A12,12,0,0,1,72,108Zm88,0a12,12,0,1,1,12,12A12,12,0,0,1,160,108Zm4,28H92a28,28,0,0,0,0,56h72a28,28,0,0,0,0-56Zm-24,16v24H116V152ZM80,164a12,12,0,0,1,12-12h8v24H92A12,12,0,0,1,80,164Zm84,12h-8V152h8a12,12,0,0,1,0,24Z', None)],
    "PlugsConnected": [('M185,127,127,185a24,24,0,0,1-33.94,0L71,162.91A24,24,0,0,1,71,129L129,71a24,24,0,0,1,33.94,0L185,93.09A24,24,0,0,1,185,127Z', '0.2'), ('M237.66,18.34a8,8,0,0,0-11.32,0l-52.4,52.41-5.37-5.38a32.05,32.05,0,0,0-45.26,0L100,88.69l-6.34-6.35A8,8,0,0,0,82.34,93.66L88.69,100,65.37,123.31a32,32,0,0,0,0,45.26l5.38,5.37-52.41,52.4a8,8,0,0,0,11.32,11.32l52.4-52.41,5.37,5.38a32.06,32.06,0,0,0,45.26,0L156,167.31l6.34,6.35a8,8,0,0,0,11.32-11.32L167.31,156l23.32-23.31a32,32,0,0,0,0-45.26l-5.38-5.37,52.41-52.4A8,8,0,0,0,237.66,18.34Zm-116.29,161a16,16,0,0,1-22.62,0L76.69,157.25a16,16,0,0,1,0-22.62L100,111.31,144.69,156Zm57.94-57.94h0L156,144.69,111.31,100l23.32-23.31a16,16,0,0,1,22.62,0l22.06,22a16,16,0,0,1,0,22.63ZM88.57,35A8,8,0,0,1,103.43,29l8,20A8,8,0,0,1,96.57,55ZM24.57,93A8,8,0,0,1,35,88.57l20,8A8,8,0,0,1,49,111.43l-20-8A8,8,0,0,1,24.57,93ZM231.43,163a8,8,0,0,1-10.4,4.46l-20-8A8,8,0,1,1,207,144.57l20,8A8,8,0,0,1,231.43,163Zm-64,58.06A8,8,0,0,1,152.57,227l-8-20A8,8,0,0,1,159.43,201Z', None)],
    "Code": [('M240,128l-48,40H64L16,128,64,88H192Z', '0.2'), ('M69.12,94.15,28.5,128l40.62,33.85a8,8,0,1,1-10.24,12.29l-48-40a8,8,0,0,1,0-12.29l48-40a8,8,0,0,1,10.24,12.3Zm176,27.7-48-40a8,8,0,1,0-10.24,12.3L227.5,128l-40.62,33.85a8,8,0,1,0,10.24,12.29l48-40a8,8,0,0,0,0-12.29ZM162.73,32.48a8,8,0,0,0-10.25,4.79l-64,176a8,8,0,0,0,4.79,10.26A8.14,8.14,0,0,0,96,224a8,8,0,0,0,7.52-5.27l64-176A8,8,0,0,0,162.73,32.48Z', None)],
    "Headset": [('M80,144v40a16,16,0,0,1-16,16H48a16,16,0,0,1-16-16V128H64A16,16,0,0,1,80,144Zm112-16a16,16,0,0,0-16,16v40a16,16,0,0,0,16,16h32V128Z', '0.2'), ('M201.89,54.66A104.08,104.08,0,0,0,24,128v56a24,24,0,0,0,24,24H64a24,24,0,0,0,24-24V144a24,24,0,0,0-24-24H40.36A88.12,88.12,0,0,1,190.54,65.93,87.39,87.39,0,0,1,215.65,120H192a24,24,0,0,0-24,24v40a24,24,0,0,0,24,24h24a24,24,0,0,1-24,24H136a8,8,0,0,0,0,16h56a40,40,0,0,0,40-40V128A103.41,103.41,0,0,0,201.89,54.66ZM64,136a8,8,0,0,1,8,8v40a8,8,0,0,1-8,8H48a8,8,0,0,1-8-8V136Zm128,56a8,8,0,0,1-8-8V144a8,8,0,0,1,8-8h24v56Z', None)],
}

# lo que hace, no los proyectos (esos van abajo en el README): etiqueta, icono, tono
DOCK = [
    ("Portfolio", None, None),          # el pinguino de DecoudJuan OS
    ("AI Automation", "Robot", 2),
    ("Integrations", "PlugsConnected", 0),
    ("Full-Stack", "Code", 1),
    ("Tech Support L2", "Headset", 3),
]
TILE, STEP = 50, 116
DOCK_Y = 250

# el pinguino del portfolio (viewBox 240), sin animacion
PENGUIN = """
<clipPath id="pmc"><rect width="240" height="240"/></clipPath>
<g clip-path="url(#pmc)"><path fill="#1e2228" d="M0.3 262C-1.6 198 44 162 120 162C196 162 241.6 198 239.7 262Z"/><path fill="#fff" d="M64.9 262C63 214 93.4 196 120 196C146.6 196 177 214 175.1 262Z"/></g>
<path fill="#1e2228" d="M120 30C66 30 28 64 28 116C28 158 62 186 120 186C178 186 212 158 212 116C212 64 174 30 120 30Z"/>
<path fill="#fff" d="M31 124C31 86 50 70 76 70C100 70 112 88 114 108C116 115 124 115 126 108C128 88 140 70 164 70C190 70 209 86 209 124C209 162 172 184 120 184C68 184 31 162 31 124Z"/>
<ellipse fill="#1e2228" cx="76" cy="107" rx="11" ry="13"/><ellipse fill="#1e2228" cx="164" cy="107" rx="11" ry="13"/>
<ellipse fill="#fff" cx="71.2" cy="101" rx="3.6" ry="5"/><ellipse fill="#fff" cx="159.2" cy="101" rx="3.6" ry="5"/>
<path fill="#f0951f" stroke="#1e2228" stroke-width="3.5" d="M99 120C101 111 110 107 120 107C130 107 139 111 141 120C141 132 132 150 120 157C108 150 99 132 99 120Z"/>
<path fill="none" stroke="#1e2228" stroke-width="23" stroke-linecap="round" d="M30 106C30 -10 210 -10 210 106"/>
<path fill="none" stroke="#f1f3f5" stroke-width="15" stroke-linecap="round" d="M30 106C30 -10 210 -10 210 106"/>
<rect fill="#f1f3f5" stroke="#1e2228" stroke-width="5" x="13" y="84" width="37" height="68" rx="18"/>
<rect fill="#f1f3f5" stroke="#1e2228" stroke-width="5" x="190" y="84" width="37" height="68" rx="18"/>
<g fill="none" stroke="#000" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"><path d="M26 88C26 78 32 74 48 74L100 74C110 74 114 80 114 91C114 106 112 120 108 127C104 134 92 137 72 137C50 137 36 134 31 126C27 119 26 97 26 88Z"/><path d="M214 88C214 78 208 74 192 74L140 74C130 74 126 80 126 91C126 106 128 120 132 127C136 134 148 137 168 137C190 137 204 134 209 126C213 119 214 97 214 88Z"/><path d="M114 85C117 81 123 81 126 85"/></g>
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(theme):
    t = THEMES[theme]
    o = io.StringIO()
    o.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" '
            'aria-label="Juan Manuel Decoud. Support and AI Automation Engineer at Darwin AI, Universidad Austral, '
            'Buenos Aires. Open to freelance.">\n' % (W, H, W, H))

    # --- estilos ---
    o.write('<style>')
    o.write('text{font-family:%s}.mono{font-family:%s;letter-spacing:1.6px}' % (SANS, MONO))
    o.write('.ink{fill:%s}.mut{fill:%s}' % (t["ink"], t["mut"]))
    o.write('@keyframes rise{from{opacity:0;transform:translateY(8px)}}')
    o.write('@keyframes draw{from{transform:scaleX(0)}}')
    o.write('@keyframes pop{from{opacity:0;transform:translateY(12px) scale(.9)}}')
    o.write('@keyframes live{0%,100%{opacity:1}50%{opacity:.35}}')
    o.write('.r{animation:rise .6s cubic-bezier(.22,1,.36,1) backwards}')
    o.write('.d1{animation-delay:.08s}.d2{animation-delay:.16s}.d3{animation-delay:.26s}')
    o.write('.rule{transform-box:fill-box;transform-origin:center;animation:draw .8s cubic-bezier(.22,1,.36,1) .2s backwards}')
    o.write('.dk{transform-box:fill-box;transform-origin:50% 100%;animation:pop .5s cubic-bezier(.34,1.56,.64,1) backwards}')
    for i in range(len(DOCK)):
        o.write('.k%d{animation-delay:%.2fs}' % (i, 0.4 + 0.06 * i))
    o.write('.live{animation:live 2.4s ease-in-out infinite}')
    o.write('@media(prefers-reduced-motion:reduce){.r,.rule,.dk,.live{animation:none}}')
    o.write('</style>\n')

    # --- defs: veta, vineta y bronce ---
    o.write('<defs>'
            '<filter id="g" x="0" y="0" width="100%%" height="100%%"><feTurbulence type="fractalNoise" '
            'baseFrequency="0.0042857 0.11" numOctaves="4" seed="11" stitchTiles="stitch"/>'
            '<feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1.6 0 0 0 -0.62"/></filter>'
            '<radialGradient id="vg" cx="50%%" cy="42%%" r="75%%"><stop offset=".45" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="%s"/></radialGradient>'
            '<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ecd48c"/>'
            '<stop offset=".5" stop-color="#c9a24f"/><stop offset="1" stop-color="#94722a"/></linearGradient>'
            '<linearGradient id="goldh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c9a24f" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="%s"/><stop offset="1" stop-color="#c9a24f" stop-opacity="0"/></linearGradient>'
            '<clipPath id="card"><rect width="%d" height="%d" rx="14"/></clipPath>'
            '</defs>\n' % (t["vignette"], t["line"], W, H))

    # --- madera ---
    o.write('<g clip-path="url(#card)">')
    o.write('<rect width="%d" height="%d" fill="%s"/>' % (W, H, t["wood"]))
    o.write('<rect width="%d" height="%d" filter="url(#g)" opacity="%s"/>' % (W, H, t["grain"]))
    o.write('<rect width="%d" height="%d" fill="url(#vg)"/>' % (W, H))
    o.write('</g>\n')
    # marco dorado fino, adentro del borde
    o.write('<rect x="10.5" y="10.5" width="%d" height="%d" rx="9" fill="none" stroke="url(#gold)" '
            'stroke-opacity="%s"/>\n' % (W - 21, H - 21, t["frame_op"]))

    # --- texto ---
    o.write('<g class="r"><text class="mono mut" x="%d" y="60" font-size="11" text-anchor="middle">%s</text></g>\n'
            % (CX, esc(WHERE)))
    o.write('<g class="r d1"><text class="ink" x="%d" y="122" font-size="56" font-weight="800" letter-spacing="-1.6" '
            'text-anchor="middle">%s</text></g>\n' % (CX, esc(NAME)))
    o.write('<rect class="rule" x="%d" y="138" width="180" height="2" fill="url(#goldh)"/>\n' % (CX - 90))
    o.write('<g class="r d2"><text class="ink" x="%d" y="170" font-size="15.5" font-weight="500" '
            'text-anchor="middle">%s</text></g>\n' % (CX, esc(ROLE)))

    # placa de bronce: abierto a freelance
    pw = 178
    o.write('<g class="r d3"><rect x="%d" y="188" width="%d" height="28" rx="14" fill="url(#gold)" stroke="#8a6a24"/>'
            '<circle class="live" cx="%d" cy="202" r="3.6" fill="%s"/>'
            '<text class="mono" x="%d" y="206" font-size="10.5" font-weight="700" fill="%s">%s</text></g>\n'
            % (CX - pw // 2, pw, CX - pw // 2 + 18, t["live"], CX - pw // 2 + 30, t["plate_ink"], FREELANCE))

    # --- dock ---
    n = len(DOCK)
    dw = STEP * (n - 1) + TILE + 44
    dx = CX - dw // 2
    o.write('<rect x="%d" y="%d" width="%d" height="%d" rx="22" fill="%s" fill-opacity="%s" stroke="%s"/>\n'
            % (dx, DOCK_Y - 12, dw, TILE + 46, t["bar"], t["bar_op"], t["bar_ln"]))
    x0 = CX - (STEP * (n - 1)) // 2 - TILE // 2
    for i, (label, icon, tone) in enumerate(DOCK):
        x = x0 + i * STEP
        o.write('<g class="dk k%d">' % i)
        if icon is None:
            o.write('<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="#e7b866" stroke="url(#gold)"/>'
                    % (x, DOCK_Y, TILE, TILE))
            o.write('<svg x="%d" y="%d" width="%d" height="%d" viewBox="0 0 240 240">%s</svg>'
                    % (x + 5, DOCK_Y + 6, TILE - 10, TILE - 10, PENGUIN))
        else:
            col = t["tones"][tone]
            o.write('<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="%s" stroke="url(#gold)"/>'
                    % (x, DOCK_Y, TILE, TILE, t["tile"]))
            s = (TILE - 18) / 256
            o.write('<g transform="translate(%.1f %.1f) scale(%.4f)" fill="%s">' % (x + 9, DOCK_Y + 9, s, col))
            for d, op in ICONS[icon]:
                o.write('<path d="%s"%s/>' % (d, ' opacity="%s"' % op if op else ''))
            o.write('</g>')
        o.write('<text class="mut" x="%d" y="%d" font-size="11" font-weight="500" text-anchor="middle">%s</text>'
                % (x + TILE // 2, DOCK_Y + TILE + 18, esc(label)))
        o.write('</g>\n')

    o.write('</svg>\n')
    return o.getvalue()


if __name__ == "__main__":
    for theme in THEMES:
        svg = build(theme)
        path = "header-%s.svg" % theme
        io.open(path, "w", encoding="utf-8").write(svg)
        print(path, round(len(svg.encode("utf-8")) / 1024, 1), "KB")
