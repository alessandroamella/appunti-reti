import os

import matplotlib.pyplot as plt
import numpy as np

# Creare la cartella images se non esiste
if not os.path.exists("images"):
    os.makedirs("images")

# --- Grafico 1: Comparazione Throughput ---
G = np.logspace(-3, 5, 500)  # Offered load

# Pure ALOHA: S = G * exp(-2G)
S_aloha = G * np.exp(-2 * G)

# Slotted ALOHA: S = G * exp(-G)
S_slotted_aloha = G * np.exp(-G)

# Per CSMA (semplificazioni, forme qualitative)
# Assumiamo 'a' (propagation_time / transmission_time) piccolo
# Per CSMA (non persistente, a=0.01) qualitativo
a_csma = 0.05  # Valore qualitativo per dare forma
S_pure_csma = G / (G * (1 + 2 * a_csma) + np.exp(-a_csma * G))  # Approssimazione
S_pure_csma_peak = (
    G * np.exp(-G * a_csma) / (G * (1 + a_csma) + np.exp(-G * a_csma))
)  # Altra forma per picco più alto
# Normalizzazione per aspetto simile alla slide
S_pure_csma_peak = S_pure_csma_peak / np.max(S_pure_csma_peak) * 0.95

# Per Slotted CSMA qualitativo
S_slotted_csma = G / (G * (1 + a_csma) + np.exp(-a_csma * G))
# Normalizzazione per aspetto simile alla slide
S_slotted_csma = S_slotted_csma / np.max(S_slotted_csma) * 0.99


plt.style.use("dark_background")
fig1, ax1 = plt.subplots(figsize=(10, 6))

ax1.plot(G, S_aloha, label="Pure Aloha", color="red")
ax1.plot(G, S_slotted_aloha, label="Slotted Aloha", color="cyan")
ax1.plot(G, S_pure_csma_peak, label="Pure CSMA", color="blue")
ax1.plot(G, S_slotted_csma, label="Slotted CSMA", color="lime")


ax1.set_xscale("log")
ax1.set_xlabel("Offered Load: G")
ax1.set_ylabel("S (Throughput)")
ax1.set_title("Analytical Results - Throughput Comparison")
ax1.legend()
ax1.grid(True, linestyle="--", alpha=0.5)
ax1.set_ylim(0, 1)
ax1.set_xlim(1e-3, 1e5)

plt.tight_layout()
plt.savefig("images/throughput_comparison.png")
print("Grafico 'throughput_comparison.png' generato.")

# --- Grafico 2: Controllo della Contesa ---
num_stations = np.array([4, 8, 16, 32, 64, 128, 256, 512])
# Dati qualitativi per simulare il trend della slide
# L'utilizzo del canale diminuisce con il numero di stazioni a causa delle collisioni
# Valori fittizi per simulare il trend, non basati su una formula precisa qui
channel_utilization = np.array([0.65, 0.55, 0.48, 0.40, 0.33, 0.25, 0.20, 0.15])
# Aggiungiamo una leggera variazione per i "baffi" dell'errore, sebbene non siano errori reali qui
error = channel_utilization * 0.05  # 5% variazione fittizia

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
    label="Congestion Control OFF (Simulated)",
)

ax2.set_xscale("log", base=2)  # La slide usa potenze di 2 per le stazioni
ax2.set_xticks(num_stations)
ax2.get_xaxis().set_major_formatter(plt.ScalarFormatter())


ax2.set_xlabel("Number of Stations")
ax2.set_ylabel("Channel Utilization")
ax2.set_title("Channel Utilization for Standard 802.11 DCF (Simulated Trend)")
ax2.legend()
ax2.grid(True, linestyle="--", alpha=0.5)
ax2.set_ylim(0, 0.75)

plt.tight_layout()
plt.savefig("images/contention_control.png")
print("Grafico 'contention_control.png' generato.")
# plt.show() # Uncomment to display plots if running interactively
