#!/bin/bash

# Versione completa per la generazione del documento finale
echo "==================================================================="
echo "= Script per generare un documento LaTeX unificato da file multipli ="
echo "==================================================================="

# Prima verifica che tutti i file esistano
echo "Verifico che tutti i file necessari siano presenti..."

FILES=(
  "01-introduzione.tex"
  "02-networking.tex"
  "03-ip-subnetting.tex"
  "04-ipv4-vlsm.tex"
  "05-application-layer.tex"
  "06-security.tex"
  "07-wireless-1.tex"
  "07-wireless-2.tex"
  "08-wireless-protocols.tex"
  "09-routing.tex"
  "10-esercitazioni.tex"
  "preambolo_comune.tex"
)

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

cat >appunti_completi.tex <<'EOT'
\documentclass{report}

% Importa tutte le configurazioni dal preambolo comune modificato
\input{preambolo_comune_modificato}

% Hyperref configurazione globale (sovrascrive quella nel preambolo)
\hypersetup{
    colorlinks=true,
    linkcolor=white,
    filecolor=magenta,
    urlcolor=cyan,
    pdftitle={Appunti Completi di Reti di Calcolatori},
    pdfauthor={Alessandro Amella},
    pdfpagemode=FullScreen,
}

% Titolo del documento unificato
\title{\Appunti Completi di Reti di Calcolatori\\
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

\chapter{Indirizzamento IP, Subnetting e Instradamento}
\input{03-ip-subnetting-content}

\chapter{Progettazione Reti IPv4 e Subnetting}
\input{04-ipv4-vlsm-content}

\chapter{Livello Applicazione}
\input{05-application-layer-content}

\chapter{Sicurezza nelle Reti di Calcolatori}
\input{06-security-content}

\chapter{Sistemi Wireless: Livello Fisico e Segnali}
\input{07-wireless-1-content}

\chapter{Sistemi Wireless: Spettro Fisico, Canali Logici, Modulazione Digitale}
\input{07-wireless-2-content}

\chapter{Protocolli MAC Wireless}
\input{08-wireless-protocols-content}

\chapter{Reti Wireless: Routing e Trasporto}
\input{09-routing-content}

\chapter{Esercitazioni}
\input{10-esercitazioni-content}

\end{document}
EOT

echo "✅ appunti_completi.tex creato."

# 2. Crea preambolo_comune_modificato.tex senza la riga \documentclass
echo "Creando preambolo_comune_modificato.tex..."
sed '/\\documentclass/d' preambolo_comune.tex >preambolo_comune_modificato.tex
echo "✅ preambolo_comune_modificato.tex creato."

# 3. Per ogni file .tex, estrai il contenuto e correggi l'indentazione minted
echo "Estraendo contenuto dai file e correggendo l'indentazione minted..."

for FILE in "${FILES[@]:0:10}"; do
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
done

echo "✅ Estrazione e correzione completate."

# 4. Compila il documento automaticamente
echo
echo "==================================================================="
echo "Compilando il documento..."
pdflatex -shell-escape appunti_completi.tex

echo "Compilando una seconda volta per l'indice..."
pdflatex -shell-escape appunti_completi.tex

echo "✅ Compilazione completata."
echo "Il documento PDF è stato generato come 'appunti_completi.pdf'"

echo "==================================================================="
echo "Processo completato con successo!"
echo "==================================================================="
