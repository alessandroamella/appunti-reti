import os

import matplotlib.pyplot as plt
import numpy as np

# Creare la directory images se non esiste
if not os.path.exists("images"):
    os.makedirs("images")

plt.style.use("dark_background")  # Stile scuro

# --- Grafico CWND con Timeout ---
time_timeout = np.array(
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
ssthresh_timeout_2 = 7  # ssthresh = cwnd_before_loss / 2 = 14/2

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(
    time_timeout,
    cwnd_timeout,
    marker="o",
    linestyle="-",
    color="cyan",
    markersize=4,
    label="CWND",
)
ax1.hlines(
    ssthresh_timeout_1,
    3,
    10,
    colors="red",
    linestyles="--",
    label=f"ssthresh = {ssthresh_timeout_1}",
)
ax1.hlines(
    ssthresh_timeout_2,
    13.6,
    17,
    colors="orange",
    linestyles="--",
    label=f"ssthresh = {ssthresh_timeout_2} (post-timeout)",
)

# Etichette fasi
ax1.text(1.5, 6, "Slow Start", color="yellow", fontsize=10)
ax1.text(5, 11.5, "Congestion Avoidance", color="yellow", fontsize=10)
ax1.text(
    10.5,
    7,
    "Timeout!",
    color="pink",
    fontsize=10,
    rotation=90,
    va="bottom",
    ha="center",
)
ax1.text(11.8, 6, "Slow Start", color="yellow", fontsize=10)
ax1.text(15, 10.5, "Congestion Avoidance", color="yellow", fontsize=10)


ax1.set_xlabel("Tempo (RTTs)", color="white")
ax1.set_ylabel("Congestion Window (segmenti)", color="white")
ax1.set_title("Evoluzione di CWND con Evento di Timeout", color="lightskyblue")
ax1.legend()
ax1.grid(True, linestyle=":", alpha=0.5)
ax1.tick_params(colors="white")
fig1.patch.set_facecolor("#141414")  # Sfondo del plot
ax1.set_facecolor("#1e1e1e")  # Sfondo degli assi

plt.tight_layout()
plt.savefig("images/cwnd_timeout.png", facecolor=fig1.get_facecolor())
print("Grafico cwnd_timeout.png generato.")

# --- Grafico CWND con Fast Recovery ---
time_fr = np.array(
    [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        7.5,  # Fast Retransmit/Recovery
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
)  # Congestion Avoidance
ssthresh_fr_1 = 8
ssthresh_fr_2 = 4  # ssthresh = cwnd_before_loss / 2 = 8/2

fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(
    time_fr,
    cwnd_fr,
    marker="o",
    linestyle="-",
    color="lime",
    markersize=4,
    label="CWND",
)
ax2.hlines(
    ssthresh_fr_1,
    3,
    7,
    colors="red",
    linestyles="--",
    label=f"ssthresh = {ssthresh_fr_1}",
)
# ax2.hlines(ssthresh_fr_2, 7.6, 12.6, colors='orange', linestyles='--', label=f'new ssthresh = {ssthresh_fr_2}')

# Etichette fasi
ax2.text(1.5, 6, "Slow Start", color="yellow", fontsize=10)
ax2.text(4.5, 8.5, "Congestion Avoidance", color="yellow", fontsize=10)
ax2.text(7.5, 6, "3 DupACKs\nFast Recovery", color="pink", fontsize=10, ha="center")
ax2.text(9, 7.5, "Congestion Avoidance (cwnd dimezzato)", color="yellow", fontsize=10)


ax2.set_xlabel("Tempo (RTTs)", color="white")
ax2.set_ylabel("Congestion Window (segmenti)", color="white")
ax2.set_title("Evoluzione di CWND con Fast Recovery", color="lightskyblue")
ax2.legend()
ax2.grid(True, linestyle=":", alpha=0.5)
ax2.tick_params(colors="white")
fig2.patch.set_facecolor("#141414")
ax2.set_facecolor("#1e1e1e")

plt.tight_layout()
plt.savefig("images/cwnd_fastrecovery.png", facecolor=fig2.get_facecolor())
print("Grafico cwnd_fastrecovery.png generato.")

# plt.show() # Opzionale, per vedere i grafici
