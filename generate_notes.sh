#!/bin/bash

# Parse command line arguments
DARK_MODE=false
COMPILE_ONCE=false
SKIP_IMAGES=false
for arg in "$@"; do
  case "$arg" in
  "--dark")
    DARK_MODE=true
    ;;
  "--once")
    COMPILE_ONCE=true
    ;;
  "--no-images")
    SKIP_IMAGES=true
    ;;
  esac
done

# Versione completa per la generazione del documento finale
echo "==================================================================="
echo "= Script per generare un documento LaTeX unificato da file multipli ="
echo "==================================================================="

# Show theme information
if [ "$DARK_MODE" = true ]; then
  echo "📝 Tema scuro selezionato"
else
  echo "📝 Tema chiaro selezionato (default)"
fi

# Show image generation status
if [ "$SKIP_IMAGES" = true ]; then
  echo "🖼️ Generazione immagini disattivata"
fi

# Prima verifica che tutti i file esistano
echo "Verifico che tutti i file necessari siano presenti..."

FILES=(
  "01-introduzione.tex"
  "02-networking.tex"
  "03-aritmetica-binaria.tex"
  "04-ip-subnetting.tex"
  "05-ipv4-vlsm.tex"
  "06-application-layer.tex"
  "07-security.tex"
  "08-wireless-1.tex"
  "09-wireless-2.tex"
  "10-wireless-protocols.tex"
  "11-routing.tex"
  "12-esercitazioni.tex"
)

# Generate the appropriate preamble
echo "Generando il preambolo appropriato..."
if [ "$DARK_MODE" = true ]; then
  ./generate_preamble.sh --dark --no-document-class
  echo "✅ Preambolo con tema scuro generato."
else
  ./generate_preamble.sh --no-document-class
  echo "✅ Preambolo con tema chiaro generato."
fi

FILES+=("preambolo_comune.tex")

MISSING=false
for FILE in "${FILES[@]}"; do
  if [ ! -f "$FILE" ]; then
    echo "⚠️ File mancante: $FILE"
    MISSING=true
  fi
done

if [ "$MISSING" = true ]; then
  echo "Alcuni file necessari mancano. Assicurati che tutti i file siano nella directory corrente."
  exit 1
fi

echo "✅ Tutti i file necessari sono presenti."

# 1. Crea il documento master
echo "Creando il documento master 'appunti_completi.tex'..."

# Choose the appropriate hypersetup based on theme
if [ "$DARK_MODE" = true ]; then
  HYPERSETUP='
\hypersetup{
    colorlinks=true,
    linkcolor=white,
    filecolor=magenta,
    urlcolor=cyan,
    pdftitle={Appunti Completi di Reti di Calcolatori},
    pdfauthor={Alessandro Amella},
    pdfpagemode=FullScreen,
}'
else
  HYPERSETUP='
\hypersetup{
    colorlinks=true,
    linkcolor=black,
    filecolor=magenta,
    urlcolor=cyan,
    pdftitle={Appunti Completi di Reti di Calcolatori},
    pdfauthor={Alessandro Amella},
    pdfpagemode=FullScreen,
}'
fi

cat >appunti_completi.tex <<EOT
\documentclass{report}

% Importa tutte le configurazioni dal preambolo comune
\input{preambolo_comune}

% Hyperref configurazione globale (sovrascrive quella nel preambolo)
$HYPERSETUP

% Titolo del documento unificato
\title{Appunti Completi di Reti di Calcolatori\\\\
  \large Basati sulle dispense del Prof. Luciano Bononi}
\author{Alessandro Amella, Gemini e Claude}
\date{\today}

\begin{document}

\maketitle
\tableofcontents
\clearpage

\chapter*{Informazioni sul Documento}
\addcontentsline{toc}{chapter}{Informazioni sul Documento}

Questo documento è la versione compilata automaticamente di tutti i miei appunti di Reti di Calcolatori per il corso di Laurea in Informatica all'Università di Bologna.

\begin{itemize}
  \item \textbf{Fonte}: Tutti gli appunti sono disponibili come file separati nella repository GitHub: 
        \url{https://github.com/alessandroamella/appunti-reti}
  \item \textbf{Generazione}: Questo PDF è stato generato automaticamente utilizzando uno script che unisce tutti i singoli file .tex degli appunti.
  \item \textbf{Aggiornamenti}: Per la versione più recente degli appunti, visita la pagina delle release:
        \url{https://github.com/alessandroamella/appunti-reti/releases/latest}
  \item \textbf{Uso di AI}: Ho usato Gemini e Claude a manetta.
\end{itemize}

\doclicenseThis

Sentiti libero di utilizzare, condividere o contribuire a questi appunti attraverso la repository GitHub.

\clearpage

\chapter{Introduzione alle Reti di Calcolatori}
\input{01-introduzione-content}

\chapter{Principi di Networking}
\input{02-networking-content}

\chapter{Aritmetica Binaria}
\input{03-aritmetica-binaria-content}

\chapter{Indirizzamento IP, Subnetting e Instradamento}
\input{04-ip-subnetting-content}

\chapter{Progettazione Reti IPv4 e Subnetting}
\input{05-ipv4-vlsm-content}

\chapter{Livello Applicazione}
\input{06-application-layer-content}

\chapter{Sicurezza nelle Reti di Calcolatori}
\input{07-security-content}

\chapter{Wireless: Livello Fisico e Segnali}
\input{08-wireless-1-content}

\chapter{Wireless: Spettro Fisico, Canali Logici, Modulazione Digitale}
\input{09-wireless-2-content}

\chapter{Protocolli MAC Wireless}
\input{10-wireless-protocols-content}

\chapter{Reti Wireless: Routing e Trasporto}
\input{11-routing-content}

\chapter{Esercitazioni}
\input{12-esercitazioni-content}

\end{document}
EOT

echo "✅ appunti_completi.tex creato."

# 3. Per ogni file .tex, estrai il contenuto e correggi l'indentazione minted
echo "Estraendo contenuto dai file e correggendo l'indentazione minted..."

for FILE in "${FILES[@]}"; do
  # Process only files that start with digits
  if [[ $FILE =~ ^[0-9] ]]; then
    CONTENT_FILE="${FILE%.tex}-content.tex"
    TEMP_FILE="${FILE%.tex}-temp.tex"
    echo "Elaborazione di $FILE -> $CONTENT_FILE"

    # Estrai contenuto tra \begin{document} e \end{document}
    sed -n '/\\begin{document}/,/\\end{document}/p' "$FILE" |
      # Rimuovi righe specifiche
      grep -v '\\begin{document}\|\\end{document}\|\\maketitle\|\\tableofcontents\|\\newpage' >"$TEMP_FILE"

    # Correggi l'indentazione dei blocchi minted
    echo "Correggendo l'indentazione minted in $TEMP_FILE..."
    ./fix_minted_indent.sh "$TEMP_FILE" >"$CONTENT_FILE"

    # Rimuovi il file temporaneo
    rm "$TEMP_FILE"

    echo "✅ $CONTENT_FILE creato con indentazione minted corretta."
  fi
done

echo "✅ Estrazione e correzione completate."

# 4. Esegui tutti i file Python per generare le immagini
echo
echo "==================================================================="
if [ "$SKIP_IMAGES" = true ]; then
  echo "Generazione immagini saltata (parametro --no-images attivo)."
else
  echo "Esecuzione di tutti gli script Python per generare immagini..."

  PYTHON_FILES=($(find . -maxdepth 1 -name "*.py"))

  if [ ${#PYTHON_FILES[@]} -eq 0 ]; then
    echo "Nessun file Python trovato nella directory corrente."
  else
    echo "Trovati ${#PYTHON_FILES[@]} file Python da eseguire."

    for PY_FILE in "${PYTHON_FILES[@]}"; do
      echo "Eseguendo $PY_FILE..."
      python3 "$PY_FILE"

      if [ $? -eq 0 ]; then
        echo "✅ $PY_FILE eseguito con successo."
      else
        echo "⚠️ $PY_FILE ha restituito un errore."
      fi
    done

    echo "✅ Esecuzione degli script Python completata."
  fi
fi

# 5. Compila il documento automaticamente
echo
echo "==================================================================="
echo "Compilando il documento..."
pdflatex -shell-escape appunti_completi.tex

if [ "$COMPILE_ONCE" = false ]; then
  echo "Compilando una seconda volta per l'indice..."
  pdflatex -shell-escape appunti_completi.tex
fi

echo "✅ Compilazione completata."
echo "Il documento PDF è stato generato come 'appunti_completi.pdf'"

echo "==================================================================="
echo "Processo completato con successo!"
echo "==================================================================="
