#!/bin/bash

# Nome del file di output
OUTPUT_FILE="preambolo_comune.tex"

# Flag per includere o meno \documentclass
INCLUDE_DOCUMENT_CLASS=true

# Impostazioni predefinite per il tema LIGHT
THEME_NAME="Stile Chiaro"
ACTOR_TEXT_COLOR="black"
BLOCK_TEXT_COLOR="black"
INTRUDER_TEXT_COLOR="black"
PROCESS_TEXT_COLOR="black"
# datagram text=black (comune)
# key text=black (implicito, font=\tiny) (comune)
# cloud, host, servernode text=lighttext (colore definito diversamente)

# Colore del blu che cambia in base al tema
THEME_BLUE_RGB="0,51,153" # Blu scuro per tema chiaro

NODO_BASE_DRAW="black"
NODO_BASE_FILL="gray!20"
NODO_BASE_TEXT="black"
NODO_TESTO_TEXT="black"
LINEA_DRAW="black"
BLOCCO_TEMPO_DRAW="black"
BLOCCO_TEMPO_FILL="blue!30"
BLOCCO_TEMPO_VERDE_FILL="green!30"
BLOCCO_TEMPO_ROSSO_FILL="red!30"
BLOCCO_TEMPO_TEXT="black"
BLOCCO_TEMPO_HATCH_PATTERN_COLOR="gray!50"
NODE_STYLE_TEXT="black"
# important_node_style text=black (comune)
# info_box text=maintext (colore definito diversamente)

# Nuovo colore di sfondo personalizzato
BG_CUSTOM_FILL="gray!20"
BG_CUSTOM_TEXT="black"
BG_CUSTOM_RGB="0.9,0.9,0.9" # RGB equivalente a gray!20 (per \rowcolor)
BG_CUSTOM_2_FILL="gray!15"
BG_CUSTOM_2_TEXT="black"
BG_CUSTOM_2_RGB="0.925,0.925,0.925" # RGB equivalente a gray!15 (per \rowcolor)
PRIMARY_TEXT_RGB="0,0,0"            # Colore primario del testo (per light theme)

COLOR_DEF_LIGHTTEXT="\\definecolor{lighttext}{rgb}{0.98,0.98,0.98}"
COLOR_DEF_DARKTEXT="\\definecolor{darktext}{rgb}{0.1,0.1,0.1}" # Solo per light
COLOR_DEF_BGCOLOR="\\definecolor{bgcolor}{RGB}{250,250,250}"
COLOR_DEF_MAINTEXT="\\definecolor{maintext}{RGB}{30,30,30}"
COLOR_DEF_ACCENTCOLOR="\\definecolor{accentcolor}{RGB}{0,100,200}"
COLOR_DEF_NODECOLOR="\\definecolor{nodecolor}{RGB}{200,220,240}"
COLOR_DEF_LINKCOLOR="\\definecolor{linkcolor}{RGB}{80,80,80}"
COLOR_DEF_HIGHLIGHTCOLOR="\\definecolor{highlightcolor}{RGB}{255,180,0}"
COLOR_DEF_PRIMARYTEXT="\\definecolor{primarytext}{RGB}{${PRIMARY_TEXT_RGB}}"
HYPERSETUP_LINKCOLOR="darktext"
HYPERSETUP_URLCOLOR="darktext"

PAGECOLOR_CMD="\\pagecolor{white}"
COLOR_CMD="\\color{black}"

MINTED_STYLE="default"
MINTED_BGCOLOR="gray!10"

# Parsing degli argomenti in qualsiasi ordine
while [[ $# -gt 0 ]]; do
  case "$1" in
  --dark)
    THEME_NAME="Stile Scuro"
    ACTOR_TEXT_COLOR="white"
    BLOCK_TEXT_COLOR="white"
    INTRUDER_TEXT_COLOR="white"
    PROCESS_TEXT_COLOR="white"

    NODO_BASE_DRAW="white"
    NODO_BASE_FILL="gray!60!black"
    NODO_BASE_TEXT="white"
    NODO_TESTO_TEXT="white"
    LINEA_DRAW="white"
    BLOCCO_TEMPO_DRAW="white"
    BLOCCO_TEMPO_FILL="blue!70!black"
    BLOCCO_TEMPO_VERDE_FILL="green!70!black"
    BLOCCO_TEMPO_ROSSO_FILL="red!70!black"
    BLOCCO_TEMPO_TEXT="white"
    BLOCCO_TEMPO_HATCH_PATTERN_COLOR="gray"
    NODE_STYLE_TEXT="white"

    BG_CUSTOM_FILL="gray!80!black"
    BG_CUSTOM_TEXT="white"
    BG_CUSTOM_RGB="0.2,0.2,0.2"
    BG_CUSTOM_2_FILL="gray!85!black"
    BG_CUSTOM_2_TEXT="white"
    BG_CUSTOM_2_RGB="0.15,0.15,0.15"
    PRIMARY_TEXT_RGB="255,255,255"
    THEME_BLUE_RGB="102,178,255"

    COLOR_DEF_LIGHTTEXT="\\definecolor{lighttext}{rgb}{0.98,0.98,0.98}"
    COLOR_DEF_DARKTEXT="\\definecolor{darktext}{rgb}{0.9,0.9,0.9}"
    COLOR_DEF_BGCOLOR="\\definecolor{bgcolor}{RGB}{20,20,20}"
    COLOR_DEF_MAINTEXT="\\definecolor{maintext}{RGB}{230,230,230}"
    COLOR_DEF_ACCENTCOLOR="\\definecolor{accentcolor}{RGB}{70,170,255}"
    COLOR_DEF_NODECOLOR="\\definecolor{nodecolor}{RGB}{60,100,160}"
    COLOR_DEF_LINKCOLOR="\\definecolor{linkcolor}{RGB}{150,150,150}"
    COLOR_DEF_HIGHLIGHTCOLOR="\\definecolor{highlightcolor}{RGB}{255,220,100}"
    COLOR_DEF_PRIMARYTEXT="\\definecolor{primarytext}{RGB}{${PRIMARY_TEXT_RGB}}"
    HYPERSETUP_LINKCOLOR="white"
    HYPERSETUP_URLCOLOR="cyan"

    PAGECOLOR_CMD="\\pagecolor{black}"
    COLOR_CMD="\\color{white}"

    MINTED_STYLE="monokai"
    MINTED_BGCOLOR="black!80"
    ;;
  --no-document-class)
    INCLUDE_DOCUMENT_CLASS=false
    ;;
  *)
    echo "Argomento non riconosciuto: $1"
    echo "Uso: $0 [--dark] [--no-document-class]"
    exit 1
    ;;
  esac
  shift
done

# Inizia a scrivere il file
# Il 'cat << \'EOF\'' con l'apostrofo evita l'espansione delle variabili bash $ all'interno dell'heredoc
# se non sono esplicitamente referenziate come $VARIABILE.
# Per le variabili LaTeX che usano $, dobbiamo fare l'escape: \$
# Tuttavia, qui stiamo generando codice LaTeX, quindi i \$ sono interpretati da LaTeX, non da bash.

cat >"$OUTPUT_FILE" <<EOF
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% PREAMBOLO COMUNE PER APPUNTI (${THEME_NAME})
%
% Questo file contiene tutte le impostazioni e i pacchetti comuni.
% NON contiene \\begin{document} o \\end{document}.
%
% Istruzioni per la compilazione del file principale:
% pdflatex -shell-escape nomefile_principale.tex
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

EOF

# Aggiungi \documentclass solo se richiesto
if $INCLUDE_DOCUMENT_CLASS; then
  cat >>"$OUTPUT_FILE" <<EOF
\\documentclass{article}

EOF
fi

cat >>"$OUTPUT_FILE" <<EOF
% --- Encoding e lingua ---
\\usepackage[utf8]{inputenc}
\\usepackage[italian]{babel}

% --- Margini e layout ---
\\usepackage{geometry}
\\geometry{a4paper, margin=1in}

% --- Font sans-serif (come Helvetica) ---
\\usepackage[scaled]{helvet}
\\renewcommand{\\familydefault}{\\sfdefault}
\\usepackage[T1]{fontenc}

% --- Matematica ---
\\usepackage{amsmath}
\\usepackage{amssymb}

% --- Liste personalizzate ---
\\usepackage{enumitem}
% \\setlist{nosep}

% --- Immagini e Grafica ---
\\usepackage{float}
% \\usepackage{graphicx}
\\usepackage{tikz}
\\usetikzlibrary{shapes.geometric, shapes.symbols, positioning, arrows.meta, calc, fit, backgrounds, patterns, decorations.pathreplacing, shapes.misc}

% Ensure the key shape from shapes.symbols is loaded
\\tikzset{key/.append style={shape=key}}

% Pacchetto aggiuntivo per i grafici con ambiente axis
\\usepackage{pgfplots}
\\pgfplotsset{compat=1.18}

% Pacchetto xcolor (necessario per \definecolor e TikZ)
\\usepackage[table]{xcolor}

% Multicolonna e multirow per tabelle
\\usepackage{multicol}
\\usepackage{multirow}

% Definizioni colori tema-specifiche
${COLOR_DEF_LIGHTTEXT}
${COLOR_DEF_DARKTEXT}
${COLOR_DEF_BGCOLOR}
${COLOR_DEF_MAINTEXT}
${COLOR_DEF_ACCENTCOLOR}
${COLOR_DEF_NODECOLOR}
${COLOR_DEF_LINKCOLOR}
${COLOR_DEF_HIGHLIGHTCOLOR}
${COLOR_DEF_PRIMARYTEXT}
\\definecolor{themeblue}{RGB}{${THEME_BLUE_RGB}}

% Definizione del colore di sfondo personalizzato per tabelle
\\definecolor{bg_custom}{rgb}{${BG_CUSTOM_RGB}} % Colore personalizzato per tabelle
\\definecolor{bg_custom_2}{rgb}{${BG_CUSTOM_2_RGB}} % Colore personalizzato per tabelle (variante)

% Stili TikZ
\\tikzset{
    actor/.style={rectangle, draw, fill=blue!20, text=${ACTOR_TEXT_COLOR}, minimum height=1cm, minimum width=2cm, text centered},
    arrow/.style={-{Stealth[length=3mm, width=2mm]}, thick, orange},
    block/.style={rectangle, draw, fill=gray!20, text=${BLOCK_TEXT_COLOR}, minimum height=0.8cm, minimum width=2.5cm, text centered},
    channel/.style={draw, thick, loosely dashed, blue!50},
    cloud/.style={ellipse, draw=gray, fill=gray!10, minimum height=3em, minimum width=5em, text=lighttext},
    computer/.style={rectangle, draw, fill=blue!30, minimum width=0.8cm, minimum height=0.6cm, text centered},
    dataflow/.style={->, >=Stealth, thick, rounded corners},
    datagram/.style={rectangle, draw=yellow, fill=yellow!10, minimum width=2.5cm, text=black, font=\\small, align=center},
    host/.style={rectangle, rounded corners, draw=cyan, fill=blue!20, minimum height=2em, minimum width=3em, text=lighttext},
    intruder/.style={star, star points=7, star point ratio=0.5, draw, fill=red!50, text=${INTRUDER_TEXT_COLOR}, minimum size=1.5cm, text centered},
    % Custom key shape that doesn't rely on the built-in key shape
    key/.style={rectangle, rounded corners=0.15cm, draw, fill=yellow!50, minimum size=0.5cm, font=\\tiny},
    line/.style={thick, gray!80},
    message_l/.style={<-, >=Stealth, thick},
    message_r/.style={->, >=Stealth, thick},
    process/.style={rectangle, draw, fill=green!20, text=${PROCESS_TEXT_COLOR}, rounded corners, minimum height=0.8cm, text centered},
    r_arrow/.style={{Stealth[length=3mm, width=2mm]}-, thick, orange},
    server/.style={rectangle, draw, fill=green!50, minimum width=0.8cm, minimum height=1cm, text centered},
    servernode/.style={cylinder, shape border rotate=90, draw=orange, fill=orange!20, aspect=0.5, minimum height=2.5em, text=lighttext},
    % Theme specific styles
    nodo_base/.style={rectangle, rounded corners, draw=${NODO_BASE_DRAW}, fill=${NODO_BASE_FILL}, text=${NODO_BASE_TEXT}, minimum height=1.5em, minimum width=4em, text centered},
    nodo_testo/.style={text=${NODO_TESTO_TEXT}, font=\\footnotesize},
    linea/.style={draw=${LINEA_DRAW}, -{Stealth[length=2mm, width=1.5mm]}},
    linea_doppia/.style={draw=${LINEA_DRAW}, <->, Stealth-Stealth},
    blocco_tempo/.style={rectangle, draw=${BLOCCO_TEMPO_DRAW}, fill=${BLOCCO_TEMPO_FILL}, text=${BLOCCO_TEMPO_TEXT}, minimum height=0.6cm, font=\\tiny, anchor=south west},
    blocco_tempo_verde/.style={rectangle, draw=${BLOCCO_TEMPO_DRAW}, fill=${BLOCCO_TEMPO_VERDE_FILL}, text=${BLOCCO_TEMPO_TEXT}, minimum height=0.6cm, font=\\tiny, anchor=south west},
    blocco_tempo_rosso/.style={rectangle, draw=${BLOCCO_TEMPO_DRAW}, fill=${BLOCCO_TEMPO_ROSSO_FILL}, text=${BLOCCO_TEMPO_TEXT}, minimum height=0.6cm, font=\\tiny, anchor=south west},
    blocco_tempo_hatch/.style={rectangle, draw=${BLOCCO_TEMPO_DRAW}, pattern=north east lines, pattern color=${BLOCCO_TEMPO_HATCH_PATTERN_COLOR}, text=${BLOCCO_TEMPO_TEXT}, minimum height=0.6cm, font=\\tiny, anchor=south west},
    % Additional theme styles
    node_style/.style={circle, draw=accentcolor, fill=nodecolor, text=${NODE_STYLE_TEXT}, minimum size=7mm, font=\\sffamily\\small},
    important_node_style/.style={node_style, fill=highlightcolor!60!nodecolor, text=black, font=\\sffamily\\small\\bfseries}, % text=black in both
    link_style/.style={-{Stealth[length=2mm, width=1.5mm]}, draw=linkcolor, thick},
    highlight_link_style/.style={-{Stealth[length=2mm, width=1.5mm]}, draw=highlightcolor, very thick},
    info_box/.style={rectangle, draw=accentcolor, fill=bgcolor, rounded corners, inner sep=5pt, text width=6cm, font=\\sffamily\\footnotesize, text=maintext},
    zone_style/.style={rectangle, draw=accentcolor, dashed, fill=nodecolor!30, fill opacity=0.5, rounded corners, minimum width=3cm, minimum height=2cm},
    % Nuovo stile con il colore di sfondo personalizzato
    bg_custom/.style={rectangle, draw, fill=${BG_CUSTOM_FILL}, text=${BG_CUSTOM_TEXT}, rounded corners, inner sep=5pt},
    bg_custom_2/.style={rectangle, draw, fill=${BG_CUSTOM_2_FILL}, text=${BG_CUSTOM_2_TEXT}, rounded corners, inner sep=5pt}
}

% --- Tabelle Avanzate ---
\\usepackage{array}
\\usepackage{booktabs}
\\usepackage{longtable}

\\usepackage{siunitx} % Per unità di misura come GHz, dBm, ecc.

% --- Hyperlink e Metadati PDF ---
\\usepackage{hyperref}

\\usepackage{graphicx} % Caricato anche qui in entrambi i preamboli

\\hypersetup{
    colorlinks=true,
    linkcolor=${HYPERSETUP_LINKCOLOR},
    filecolor=magenta,
    urlcolor=${HYPERSETUP_URLCOLOR},
    citecolor=green,
    % pdftitle, pdfauthor, ecc. verranno impostati nel file principale
    pdfpagemode=FullScreen,
    bookmarksopen=true,
    bookmarksnumbered=true
}

% --- Licenza del documento ---
\\usepackage[
  type={CC},
  modifier={by-sa},
  version={4.0},
]{doclicense}

% --- Colori e Sfondo ---
${PAGECOLOR_CMD}
${COLOR_CMD}

% --- Evidenziazione del Codice ---
\\usepackage{minted}
\\setminted{
    frame=lines,
    framesep=2mm,
    fontsize=\\small,
    breaklines=true,
    style=${MINTED_STYLE},
    bgcolor=${MINTED_BGCOLOR}
}
\\usemintedstyle{${MINTED_STYLE}}
EOF

echo "File '$OUTPUT_FILE' generato con ${THEME_NAME}."
if ! $INCLUDE_DOCUMENT_CLASS; then
  echo "Nota: \\documentclass{article} non incluso nel preambolo."
fi
