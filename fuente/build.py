#!/usr/bin/env python3
"""Monta el sitio estático de TextiConect: une cada fragmento de src/ con la plantilla común."""
import re
from pathlib import Path

RAIZ = Path(__file__).parent
SRC = RAIZ / "src"
SITIO = RAIZ.parent

PAGINAS = [
    # archivo, etiqueta corta del menú, título del menú, <title>, descripción
    ("index.html", "Inicio", "El caso TextiConect", "TextiConect: plan de digitalización",
     "Plan de digitalización y convergencia IT/OT para TextiConect S.L."),
    ("1-diagnostico.html", "Punto 1", "Diagnóstico inicial", "1. Diagnóstico inicial",
     "Problemas del funcionamiento actual de TextiConect y su causa."),
    ("2-it-ot.html", "Punto 2", "Identificación IT/OT", "2. Identificación IT/OT",
     "Qué es IT y qué es OT en TextiConect y dónde está cada entorno."),
    ("3-propuesta.html", "Punto 3", "Propuesta tecnológica", "3. Propuesta de implantación tecnológica",
     "Tecnologías IT y OT elegidas, por qué y qué problema resuelve cada una."),
    ("4-convergencia.html", "Punto 4", "Convergencia IT-OT", "4. Convergencia IT-OT",
     "Cómo se integran los entornos IT y OT de TextiConect y qué beneficios aporta."),
    ("5-impacto.html", "Punto 5", "Impacto organizativo y cultural", "5. Impacto organizativo y cultural",
     "Cambios necesarios en la organización, resistencias previsibles y soluciones."),
    ("6-situacion.html", "Punto 6", "Situación práctica", "6. Situación práctica",
     "Cómo responde el plan al cliente que quiere personalizar online y seguir su pedido."),
    ("7-data-driven.html", "Punto 7", "Ciclo Data-Driven", "7. Ciclo Data-Driven",
     "Qué datos se capturan, cómo se integran, qué se analiza y qué se decide."),
    ("glosario.html", "Anexo", "Glosario y fuentes", "Glosario y fuentes",
     "Términos usados en el plan y fuentes consultadas."),
]

EQUIPO = "Marcos Ramos, Gonzalo Redondo, Jaime Ramos y Victor Cerveros"

# Iconos de trazo dibujados para este trabajo (24 × 24)
ICONOS = {
    "camiseta": '<path d="M8 3 4 6l2 4 2-1v12h8V9l2 1 2-4-4-3c-1 2-7 2-8 0z"/>',
    "telefono": '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
    "hoja": '<rect x="3" y="4" width="18" height="16" rx="1"/><path d="M3 9h18M3 14h18M9 4v16"/>',
    "tableta": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M11 17.5h2"/>',
    "nube": '<path d="M7 18h10a4 4 0 0 0 .5-8 6 6 0 0 0-11.5 1.5A3.5 3.5 0 0 0 7 18z"/>',
    "qr": '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><path d="M14 14h3v3h-3zM20 14v1M14 20h1M18 18h3v3"/>',
    "maquina": '<path d="M2 20h20M5 20V8h11a3 3 0 0 1 3 3v3h-4v-3H9v9"/><path d="M17 14v3.5"/><circle cx="7.5" cy="5" r="1.5"/><path d="M7.5 6.5V8"/>',
    "impresora": '<rect x="3" y="8" width="18" height="9" rx="1"/><path d="M7 8V4h10v4M7 14h10v6H7z"/>',
    "camion": '<path d="M2 7h11v9H2zM13 10h4l3 3v3h-7z"/><circle cx="6" cy="17.5" r="1.5"/><circle cx="16.5" cy="17.5" r="1.5"/>',
    "grafico": '<path d="M3 20h18M6 20v-8M11 20V5M16 20v-11"/>',
    "persona": '<circle cx="12" cy="8" r="3.5"/><path d="M5 21a7 7 0 0 1 14 0"/>',
    "correo": '<rect x="3" y="5" width="18" height="14" rx="1"/><path d="m3 7 9 6 9-6"/>',
    "caja": '<path d="m3 8 9-5 9 5v8l-9 5-9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
    "pantalla": '<rect x="3" y="4" width="18" height="12" rx="1"/><path d="M8 20h8M12 16v4"/>',
    "factura": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
    "candado": '<rect x="5" y="11" width="14" height="9" rx="1"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "lapiz": '<path d="M4 20l1-4L16 5l3 3L8 19z"/><path d="M14 7l3 3"/>',
}


def icono(nombre: str, extra: str = "") -> str:
    clase = "ico" + (f" {extra}" if extra else "")
    return f'<svg class="{clase}" viewBox="0 0 24 24" aria-hidden="true">{ICONOS[nombre]}</svg>'


PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,400;0,500;0,700;1,400&family=Barlow+Semi+Condensed:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/estilos.css">
</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="rail" data-abierto="false">
  <a class="rail__titulo" href="index.html">TextiConect<span>Plan de digitalización y convergencia IT/OT de un taller textil</span></a>
  <button class="menu-boton" type="button" aria-expanded="false" aria-controls="menu">Menú</button>
  <nav id="menu" aria-label="Puntos del trabajo">
    <ul>
{menu}
    </ul>
  </nav>
  <p class="rail__pie"><strong>Equipo</strong><br>{equipo}<br><br>UD1, Digitalización en los sistemas productivos<br>Curso 2026-2027</p>
</header>
<div class="pagina">
<main class="contenido" id="contenido">
{cuerpo}
{siguiente}
<p class="pie">Trabajo de clase elaborado por {equipo}. TextiConect S.L. es una empresa ficticia; los esquemas e iconos son de elaboración propia.</p>
</main>
</div>
<script src="assets/sitio.js"></script>
</body>
</html>
"""


def menu(actual: str) -> str:
    filas = []
    for archivo, corta, larga, _, _ in PAGINAS:
        marca = ' aria-current="page"' if archivo == actual else ""
        filas.append(f'      <li><a href="{archivo}"{marca}><small>{corta}</small>{larga}</a></li>')
    return "\n".join(filas)


def siguiente(i: int) -> str:
    partes = []
    if i > 0:
        a = PAGINAS[i - 1]
        partes.append(f'<a href="{a[0]}"><small>Anterior</small>{a[1]}: {a[2]}</a>')
    if i < len(PAGINAS) - 1:
        s = PAGINAS[i + 1]
        partes.append(f'<a class="der" href="{s[0]}"><small>Siguiente</small>{s[1]}: {s[2]}</a>')
    return '<nav class="siguiente" aria-label="Página anterior y siguiente">' + "".join(partes) + "</nav>"


def main() -> None:
    for i, (archivo, _, _, titulo, descripcion) in enumerate(PAGINAS):
        cuerpo = (SRC / archivo).read_text(encoding="utf-8")
        # iconos: {{i:nombre}} o {{i:nombre:clase}}
        cuerpo = re.sub(r"\{\{i:([a-z]+)(?::([a-z\- ]+))?\}\}", lambda m: icono(m.group(1), m.group(2) or ""), cuerpo)
        # espacio de no separación entre la cifra y el signo de porcentaje
        cuerpo = re.sub(r"(\d) %", r"\1&nbsp;%", cuerpo)
        titulo_completo = titulo if archivo == "index.html" else f"{titulo} | TextiConect"
        html = PLANTILLA.format(
            titulo=titulo_completo,
            descripcion=descripcion,
            menu=menu(archivo),
            equipo=EQUIPO,
            cuerpo=cuerpo,
            siguiente=siguiente(i),
        )
        (SITIO / archivo).write_text(html, encoding="utf-8")
        print("ok", archivo, len(html))
    (SITIO / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    main()
