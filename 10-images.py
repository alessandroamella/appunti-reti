import os

import matplotlib.pyplot as plt
import numpy as np

# Creare la cartella 'images' se non esiste
if not os.path.exists("images"):
    os.makedirs("images")

# --- Grafico 1: Comparazione del Throughput ---
G = np.logspace(-3, 5, 500)  # Carico offerto

# Aloha Puro: S = G * exp(-2G)
S_aloha = G * np.exp(-2 * G)

# Aloha a Slot: S = G * exp(-G)
S_slotted_aloha = G * np.exp(-G)

# Per CSMA (semplificazioni, forme qualitative)
# Assumiamo 'a' (tempo di propagazione / tempo di trasmissione) piccolo
# Per CSMA Puro (non persistente, a=0.01) qualitativo
a_csma = 0.05  # Valore qualitativo per dare forma
S_pure_csma = G / (G * (1 + 2 * a_csma) + np.exp(-a_csma * G))  # Approssimazione
S_pure_csma_peak = (
    G * np.exp(-G * a_csma) / (G * (1 + a_csma) + np.exp(-G * a_csma))
)  # Altra forma per un picco più alto
# Normalizzazione per un aspetto simile alla slide
S_pure_csma_peak = S_pure_csma_peak / np.max(S_pure_csma_peak) * 0.95

# Per CSMA a Slot qualitativo
S_slotted_csma = G / (G * (1 + a_csma) + np.exp(-a_csma * G))
# Normalizzazione per un aspetto simile alla slide
S_slotted_csma = S_slotted_csma / np.max(S_slotted_csma) * 0.99


plt.style.use("dark_background")
fig1, ax1 = plt.subplots(figsize=(10, 6))

ax1.plot(G, S_aloha, label="Aloha Puro", color="red")
ax1.plot(G, S_slotted_aloha, label="Aloha a Slot", color="cyan")
ax1.plot(G, S_pure_csma_peak, label="CSMA Puro", color="pink")
ax1.plot(G, S_slotted_csma, label="CSMA a Slot", color="lime")


ax1.set_xscale("log")
ax1.set_xlabel("Carico Offerto: G")
ax1.set_ylabel("S (Throughput)")
ax1.set_title("Risultati Analitici - Comparazione del Throughput")
ax1.legend()
ax1.grid(True, linestyle="--", alpha=0.5)
ax1.set_ylim(0, 1)
ax1.set_xlim(1e-3, 1e5)

plt.tight_layout()
plt.savefig("images/throughput_comparison.png", dpi=300)
print("Grafico 'throughput_comparison.png' generato.")

# --- Grafico 2: Controllo della Contesa ---
num_stations = np.array([4, 8, 16, 32, 64, 128, 256, 512])
# Dati qualitativi per simulare l'andamento della slide
# L'utilizzo del canale diminuisce con il numero di stazioni a causa delle collisioni
# Valori fittizi per simulare l'andamento, non basati su una formula precisa qui
channel_utilization = np.array([0.65, 0.55, 0.48, 0.40, 0.33, 0.25, 0.20, 0.15])
# Aggiungiamo una leggera variazione per le 'barre di errore', sebbene qui non rappresentino errori reali
error = channel_utilization * 0.05  # Variazione fittizia del 5%

plt.style.use("dark_background")
fig2, ax2 = plt.subplots(figsize=(10, 6))

ax2.errorbar(
    num_stations,
    channel_utilization,
    yerr=error,
    fmt="-o",
    color="cyan",
    ecolor="lightgray",
    elinewidth=1,
    capsize=3,
    label="Controllo Congestione DISATTIVATO (Simulato)",
)

ax2.set_xscale("log", base=2)  # La slide utilizza potenze di 2 per le stazioni
ax2.set_xticks(num_stations)
ax2.get_xaxis().set_major_formatter(plt.ScalarFormatter())


ax2.set_xlabel("Numero di Stazioni")
ax2.set_ylabel("Utilizzo del Canale")
ax2.set_title("Utilizzo del Canale per DCF 802.11 Standard (Andamento Simulato)")
ax2.legend()
ax2.grid(True, linestyle="--", alpha=0.5)
ax2.set_ylim(0, 0.75)

plt.tight_layout()
plt.savefig("images/contention_control.png", dpi=300)
print("Grafico 'contention_control.png' generato.")
# plt.show() # Decommentare per visualizzare i grafici se eseguito interattivamente
