import os
import sys

import matplotlib.pyplot as plt
import numpy as np

# --- Configurazione del tema ---
# Verifica se il parametro --dark è passato
is_dark_theme = "--dark" in sys.argv

if is_dark_theme:
    # Stile per tema scuro
    plt.style.use("dark_background")
    plot_bg_color = "#000"  # Sfondo generale del plot
    axes_bg_color = "#000"  # Sfondo degli assi
    text_color = "white"
    title_color = "lightskyblue"
    line_color_cwnd1 = "cyan"
    line_color_cwnd2 = "lime"
    ssthresh_color_1 = "red"
    ssthresh_color_2 = "orange"
    annotation_phase_color = (
        "yellow"  # Colore per "Avvio Lento", "Evitamento della Congestione"
    )
    annotation_event_color = "pink"  # Colore per "Timeout!", "3 ACK Duplicati"
    grid_color = "white"
    legend_label_color = "white"
    cbar_label_color = "white"
    cbar_tick_color = "white"
else:
    # Stile per tema chiaro
    plt.style.use("seaborn-v0_8-whitegrid")  # Un buon stile predefinito chiaro
    plot_bg_color = "white"
    axes_bg_color = "#f5f5f5"  # Grigio molto chiaro per gli assi
    text_color = "black"
    title_color = "darkblue"
    line_color_cwnd1 = "blue"
    line_color_cwnd2 = "darkgreen"
    ssthresh_color_1 = "firebrick"  # Rosso più scuro
    ssthresh_color_2 = "darkorange"
    annotation_phase_color = "darkslategray"
    annotation_event_color = "purple"
    grid_color = "lightgray"
    legend_label_color = "black"
    cbar_label_color = "black"
    cbar_tick_color = "black"

# Creare la directory images se non esiste
if not os.path.exists("images"):
    os.makedirs("images")

# --- Grafico CWND con Timeout ---
tempo_timeout = np.array(
    [
        0,
        1,
        2,
        3,
        3.5,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        10.5,  # Timeout
        10.6,
        11.6,
        12.6,
        13.6,
        14.1,
        15,
        16,
        17,
    ]
)
cwnd_timeout = np.array(
    [
        1,
        2,
        4,
        8,
        8,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        14,  # Timeout -> cwnd=1
        1,
        2,
        4,
        8,
        8,
        9,
        10,
        11,
    ]
)
ssthresh_timeout_1 = 8
ssthresh_timeout_2 = 7  # ssthresh = cwnd_prima_della_perdita / 2 = 14/2

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(
    tempo_timeout,
    cwnd_timeout,
    marker="o",
    linestyle="-",
    color=line_color_cwnd1,
    markersize=4,
    label="CWND",
)
ax1.hlines(
    ssthresh_timeout_1,
    3,
    10,
    colors=ssthresh_color_1,
    linestyles="--",
    label=f"ssthresh = {ssthresh_timeout_1}",
)
ax1.hlines(
    ssthresh_timeout_2,
    13.6,
    17,
    colors=ssthresh_color_2,
    linestyles="--",
    label=f"ssthresh = {ssthresh_timeout_2} (dopo-timeout)",
)

# Etichette fasi
ax1.text(1.5, 6, "Avvio Lento", color=annotation_phase_color, fontsize=10)
ax1.text(
    5, 11.5, "Evitamento della Congestione", color=annotation_phase_color, fontsize=10
)
ax1.text(
    10.5,
    7,
    "Timeout!",
    color=annotation_event_color,
    fontsize=10,
    rotation=90,
    va="bottom",
    ha="center",
)
ax1.text(11.8, 6, "Avvio Lento", color=annotation_phase_color, fontsize=10)
ax1.text(
    15, 10.5, "Evitamento della\nCongestione", color=annotation_phase_color, fontsize=10
)


ax1.set_xlabel("Tempo (RTT)", color=text_color)
ax1.set_ylabel("Finestra di Congestione (segmenti)", color=text_color)
ax1.set_title("Evoluzione di CWND con Evento di Timeout", color=title_color)
ax1.legend(labelcolor=legend_label_color)
ax1.grid(True, linestyle=":", alpha=0.5, color=grid_color)
ax1.tick_params(axis="x", colors=text_color)
ax1.tick_params(axis="y", colors=text_color)
fig1.patch.set_facecolor(plot_bg_color)  # Sfondo del plot
ax1.set_facecolor(axes_bg_color)  # Sfondo degli assi

plt.tight_layout()
plt.savefig("images/cwnd_timeout.png", dpi=300, facecolor=fig1.get_facecolor())
print("Grafico cwnd_timeout.png generato.")

# --- Grafico CWND con Recupero Veloce ---
tempo_fr = np.array(
    [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        7.5,  # Ritrasmissione/Recupero Veloce
        7.6,
        8.6,
        9.6,
        10.6,
        11.6,
        12.6,
    ]
)
cwnd_fr = np.array(
    [1, 2, 4, 8, 8, 8, 8, 8, 4, 4, 5, 6, 7, 8, 8]  # CWND si dimezza
)  # Evitamento della Congestione
ssthresh_fr_1 = 8
ssthresh_fr_2 = 4  # ssthresh = cwnd_prima_della_perdita / 2 = 8/2

fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(
    tempo_fr,
    cwnd_fr,
    marker="o",
    linestyle="-",
    color=line_color_cwnd2,
    markersize=4,
    label="CWND",
)
ax2.hlines(
    ssthresh_fr_1,
    3,
    7,
    colors=ssthresh_color_1,
    linestyles="--",
    label=f"ssthresh = {ssthresh_fr_1}",
)
# ax2.hlines(ssthresh_fr_2, 7.6, 12.6, colors=ssthresh_color_2, linestyles='--', label=f'new ssthresh = {ssthresh_fr_2}')

# Etichette fasi
ax2.text(1.5, 6, "Avvio Lento", color=annotation_phase_color, fontsize=10)
ax2.text(
    4.5, 8.8, "Evitamento della Congestione", color=annotation_phase_color, fontsize=10
)
ax2.text(
    7.5,
    6,
    "3 ACK Duplicati\nRecupero Veloce",
    color=annotation_event_color,
    fontsize=10,
    ha="center",
)
ax2.text(
    9,
    6.5,
    "Evitamento della Congestione\n(CWND dimezzato)",
    color=annotation_phase_color,
    fontsize=10,
)


ax2.set_xlabel("Tempo (RTT)", color=text_color)
ax2.set_ylabel("Finestra di Congestione (segmenti)", color=text_color)
ax2.set_title("Evoluzione di CWND con Recupero Veloce", color=title_color)
ax2.legend(labelcolor=legend_label_color)
ax2.grid(True, linestyle=":", alpha=0.5, color=grid_color)
ax2.tick_params(axis="x", colors=text_color)
ax2.tick_params(axis="y", colors=text_color)
fig2.patch.set_facecolor(plot_bg_color)
ax2.set_facecolor(axes_bg_color)

plt.tight_layout()
plt.savefig("images/cwnd_fastrecovery.png", dpi=300, facecolor=fig2.get_facecolor())
print("Grafico cwnd_fastrecovery.png generato.")

# plt.show() # Opzionale, per visualizzare i grafici
