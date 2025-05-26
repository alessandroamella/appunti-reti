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
    15, 10.5, "Evitamento della Congestione", color=annotation_phase_color, fontsize=10
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
plt.savefig("images/cwnd_timeout.png", facecolor=fig1.get_facecolor())
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
    4.5, 8.5, "Evitamento della Congestione", color=annotation_phase_color, fontsize=10
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
    7.5,
    "Evitamento della Congestione (CWND dimezzato)",
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
plt.savefig("images/cwnd_fastrecovery.png", facecolor=fig2.get_facecolor())
print("Grafico cwnd_fastrecovery.png generato.")

# plt.show() # Opzionale, per visualizzare i grafici


def generate_tdm_graph(filename="tdm_multiplexing.png"):
    """
    Genera un grafico 3D che illustra la Time Multiplexing (TDM).
    Mostra i segnali di ingresso impilati sull'asse Z e l'uscita multiplexata
    come segmenti su un livello Z inferiore, trasmessi sequenzialmente nel tempo.
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")
    (
        plt.style.use("dark_background")
        if is_dark_theme
        else plt.style.use("seaborn-v0_8-whitegrid")
    )

    # --- Parametri per TDM ---
    tempo_totale = 4  # secondi
    num_campioni = 400
    t = np.linspace(0, tempo_totale, num_campioni)

    # Definisci i singoli segnali
    colori_segnale = ["red", "green", "blue", "orange"]
    etichette_segnale = [
        "Segnale A (1Hz)",
        "Segnale B (2Hz)",
        "Segnale C (3Hz)",
        "Segnale D (4Hz)",
    ]
    frequenze = [1, 2, 3, 4]
    num_segnali = len(frequenze)

    # Asse Z per i segnali di ingresso (rappresentanti distinti livelli "Sorgente")
    livelli_z_ingresso = np.linspace(
        2.5, 0.5, num_segnali
    )  # Z più alto per il primo segnale

    # Disegna i singoli segnali di ingresso
    for i in range(num_segnali):
        sig = np.sin(2 * np.pi * frequenze[i] * t)
        ax.plot(
            t,
            [livelli_z_ingresso[i]] * num_campioni,
            sig,
            color=colori_segnale[i],
            label=etichette_segnale[i],
            linewidth=1.5,
            alpha=0.8,
        )

    # --- Costruzione dell'uscita multiplexata ---
    livello_z_uscita = -1.0  # Asse Z per l'uscita multiplexata
    punti_tempo_per_slot = num_campioni // num_segnali

    for i in range(num_segnali):
        start_idx = i * punti_tempo_per_slot
        end_idx = (i + 1) * punti_tempo_per_slot

        # Assicurati che l'ultimo segmento arrivi alla fine del tempo
        if i == num_segnali - 1:
            segment_t = t[start_idx:]
            segment_sig = np.sin(2 * np.pi * frequenze[i] * segment_t)
        else:
            segment_t = t[start_idx:end_idx]
            segment_sig = np.sin(2 * np.pi * frequenze[i] * segment_t)

        ax.plot(
            segment_t,
            [livello_z_uscita] * len(segment_t),
            segment_sig,
            color=colori_segnale[i],
            linewidth=3,
            alpha=0.9,
            label=(
                f"Slot di Uscita {i+1} (da {etichette_segnale[i].split(' ')[0]})"
                if i == 0
                else None
            ),
        )  # Etichetta solo il primo segmento di output

        # Opzionale: Aggiungi piccole linee verticali per indicare i confini degli slot temporali
        if i < num_segnali - 1:
            ax.plot(
                [t[end_idx], t[end_idx]],
                [livello_z_uscita, livello_z_uscita],
                [-1.2, 1.2],
                color="gray",
                linestyle="--",
                linewidth=0.8,
                alpha=0.6,
            )

    # --- Configura il plot ---
    ax.set_xlabel("Tempo (s)", labelpad=15, fontsize=12, color=text_color)
    ax.set_ylabel(
        "Livello Canale / Sorgente", labelpad=25, fontsize=12, color=text_color
    )
    ax.set_zlabel("Ampiezza", labelpad=15, fontsize=12, color=text_color)
    ax.set_title("Time Multiplexing (TDM)", fontsize=16, color=title_color)

    # Personalizza i tick dell'asse Y per mostrare il significato
    posizioni_tick_y = [livello_z_uscita] + list(livelli_z_ingresso)
    etichette_tick_y = ["Uscita Multiplexata"] + [
        f"Sorgente {chr(65+i)}" for i in range(num_segnali)
    ]
    ax.set_yticks(posizioni_tick_y)
    ax.set_yticklabels(etichette_tick_y, fontsize=10, color=text_color)
    ax.tick_params(axis="x", colors=text_color)
    ax.tick_params(axis="z", colors=text_color)

    ax.set_ylim(min(posizioni_tick_y) - 0.5, max(posizioni_tick_y) + 0.5)
    ax.set_zlim(-1.5, 1.5)
    ax.set_xlim(0, tempo_totale)

    # Regola l'angolo di visualizzazione per una migliore visualizzazione 3D
    ax.view_init(elev=25, azim=-60)

    # Aggiungi una legenda per i segnali di ingresso
    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.25, 0.95),
        frameon=False if is_dark_theme else True,  # Frame on for light theme
        fontsize=10,
        facecolor="none" if is_dark_theme else plot_bg_color,
        edgecolor="none" if is_dark_theme else "gray",
        labelcolor=legend_label_color,
    )

    fig.patch.set_facecolor(plot_bg_color)
    ax.set_facecolor(axes_bg_color)

    plt.tight_layout()
    plt.savefig(
        f"images/{filename}",
        dpi=300,
        bbox_inches="tight",
        transparent=False if is_dark_theme else False,
    )  # transparent should be consistent or false
    print(f"Generato {filename}")
    plt.close()


def generate_tfdm_graph(filename="tfdm_multiplexing.png"):
    """
    Genera un grafico 3D che illustra la Time and Frequency Multiplexing (TFDM).
    Mostra diversi segnali come picchi nello spazio Tempo-Frequenza-Ampiezza.
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")
    (
        plt.style.use("dark_background")
        if is_dark_theme
        else plt.style.use("seaborn-v0_8-whitegrid")
    )

    # --- Parametri per TFDM ---
    risoluzione_tempo = 200  # numero di punti per l'asse del tempo
    risoluzione_frequenza = 150  # numero di punti per l'asse della frequenza

    t = np.linspace(0, 5, risoluzione_tempo)  # Tempo (asse X)
    f = np.linspace(0, 10, risoluzione_frequenza)  # Frequenza (asse Y)
    T, F = np.meshgrid(t, f)

    # Inizializza l'ampiezza/potenza (asse Z) a zero
    Z = np.zeros_like(T)

    # Definisci i singoli segnali come "bernoccoli" gaussiani nello spazio Tempo-Frequenza
    # (t_centro, f_centro, dev_std_t, dev_std_f, ampiezza)
    segnali = [
        (1.0, 2.0, 0.2, 0.5, 1.0),  # Segnale 1: Tempo iniziale, bassa freq
        (2.5, 7.0, 0.2, 0.5, 1.0),  # Segnale 2: Tempo intermedio, alta freq
        (
            1.5,
            4.0,
            0.2,
            0.5,
            1.0,
        ),  # Segnale 3: Si sovrappone nel tempo con S1, ma frequenza diversa
        (
            4.0,
            3.0,
            0.2,
            0.5,
            1.0,
        ),  # Segnale 4: Tempo tardo, media freq (distinto da S3)
        (
            2.0,
            8.5,
            0.2,
            0.5,
            1.0,
        ),  # Segnale 5: Si sovrappone nel tempo con S2, frequenza diversa
    ]

    # Aggiungi la "potenza" di ciascun segnale alla matrice Z
    for tc, fc, ts, fs, amp in segnali:
        Z += amp * np.exp(-((T - tc) ** 2 / (2 * ts**2) + (F - fc) ** 2 / (2 * fs**2)))

    # --- Disegna la superficie 3D ---
    surf = ax.plot_surface(T, F, Z, cmap="viridis", edgecolor="none", alpha=0.9)

    # --- Configura il plot ---
    ax.set_xlabel("Tempo (s)", labelpad=15, fontsize=12, color=text_color)
    ax.set_ylabel("Frequenza (Hz)", labelpad=15, fontsize=12, color=text_color)
    ax.set_zlabel("Ampiezza / Potenza", labelpad=15, fontsize=12, color=text_color)
    ax.set_title(
        "Time and Frequency Multiplexing (TFDM)",
        fontsize=16,
        color=title_color,
    )

    ax.tick_params(axis="x", colors=text_color)
    ax.tick_params(axis="y", colors=text_color)
    ax.tick_params(axis="z", colors=text_color)

    ax.set_zlim(0, 1.2)  # Imposta limite asse Z
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 10)

    # Regola l'angolo di visualizzazione per una migliore visualizzazione 3D
    ax.view_init(elev=35, azim=-120)

    # Aggiungi una barra colori
    cbar = fig.colorbar(surf, shrink=0.5, aspect=10, pad=0.1)
    cbar.set_label("Intensità Segnale", color=cbar_label_color, fontsize=10)
    cbar.ax.yaxis.set_tick_params(color=cbar_tick_color)
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color=cbar_tick_color)

    fig.patch.set_facecolor(plot_bg_color)
    ax.set_facecolor(axes_bg_color)

    plt.tight_layout()
    plt.savefig(
        f"images/{filename}",
        dpi=300,
        bbox_inches="tight",
        transparent=False if is_dark_theme else False,
    )
    print(f"Generato {filename}")
    plt.close()


def generate_cdma_graph(filename="cdma_multiplexing.png"):
    """
    Genera un grafico che illustra la Code Division Multiple Access (CDMA).
    Mostra come diversi utenti condividono lo stesso canale usando codici ortogonali,
    con i segnali originali, i codici di spreading e i segnali trasmessi.
    """
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(
        3, 2, figsize=(16, 12)
    )  # Aumentato le dimensioni per una migliore leggibilità

    # --- Colori adattivi per il tema ---
    title_fontsize = 17  # Titoli più grandi
    label_fontsize = 15  # Etichette più grandi
    legend_fontsize = 13  # Legenda più grande
    if is_dark_theme:
        user1_color = "cyan"  # Molto visibile su sfondo scuro
        user2_color = "orange"  # Contrasto eccellente
        combined_color = "magenta"  # Vivace e ben visibile
        decoded_color = "lime"  # Verde brillante
        reference_color = "lightblue"  # Blu chiaro per riferimento
    else:
        user1_color = "blue"
        user2_color = "red"
        combined_color = "purple"
        decoded_color = "green"
        reference_color = "blue"

    # --- Parametri per CDMA ---
    # num_bits = 8
    chip_rate = 8  # 8 chip per bit

    # Dati degli utenti (sequenze di bit)
    user1_data = np.array([1, -1, 1, 1, -1, 1, -1, -1])  # 8 bit
    user2_data = np.array([-1, 1, 1, -1, 1, -1, 1, 1])  # 8 bit

    # Codici di spreading Walsh (ortogonali)
    code1 = np.array([1, 1, 1, 1, 1, 1, 1, 1])  # Codice utente 1
    code2 = np.array([1, -1, 1, -1, 1, -1, 1, -1])  # Codice utente 2

    # Genera i segnali espansi
    def expand_signal(data, code):
        expanded = []
        for bit in data:
            expanded.extend(bit * code)
        return np.array(expanded)

    user1_expanded = expand_signal(user1_data, code1)
    user2_expanded = expand_signal(user2_data, code2)
    combined_signal = user1_expanded + user2_expanded

    # Funzione per creare segnali a gradini
    def create_step_signal(data, time_per_sample):
        signal = []
        time = []
        for i, value in enumerate(data):
            signal.extend([value, value])
            time.extend([i * time_per_sample, (i + 1) * time_per_sample])
        return np.array(time), np.array(signal)

    # --- Subplot 1: Dati originali Utente 1 ---
    user1_step_t, user1_step = create_step_signal(user1_data, 1)
    ax1.plot(
        user1_step_t, user1_step, color=user1_color, linewidth=3, label="Dati Utente 1"
    )
    ax1.set_title(
        "Dati Originali - Utente 1", color=title_color, fontsize=title_fontsize
    )
    ax1.set_ylabel("Ampiezza", color=text_color, fontsize=label_fontsize)
    ax1.grid(True, alpha=0.3, color=grid_color)
    ax1.set_ylim(-1.5, 1.5)
    ax1.tick_params(colors=text_color, labelsize=label_fontsize)
    ax1.set_facecolor(axes_bg_color)

    # --- Subplot 2: Dati originali Utente 2 ---
    user2_step_t, user2_step = create_step_signal(user2_data, 1)
    ax2.plot(
        user2_step_t, user2_step, color=user2_color, linewidth=3, label="Dati Utente 2"
    )
    ax2.set_title(
        "Dati Originali - Utente 2", color=title_color, fontsize=title_fontsize
    )
    ax2.set_ylabel("Ampiezza", color=text_color, fontsize=label_fontsize)
    ax2.grid(True, alpha=0.3, color=grid_color)
    ax2.set_ylim(-1.5, 1.5)
    ax2.tick_params(colors=text_color, labelsize=label_fontsize)
    ax2.set_facecolor(axes_bg_color)

    # --- Subplot 3: Segnale espanso Utente 1 ---
    t_chips1, chips1 = create_step_signal(user1_expanded, 1 / chip_rate)
    ax3.plot(
        t_chips1, chips1, color=user1_color, linewidth=2.5, label="Utente 1 * Codice 1"
    )
    ax3.set_title(
        "Segnale Espanso - Utente 1 (dopo spreading)",
        color=title_color,
        fontsize=title_fontsize,
    )
    ax3.set_ylabel("Ampiezza", color=text_color, fontsize=label_fontsize)
    ax3.grid(True, alpha=0.3, color=grid_color)
    ax3.set_ylim(-1.5, 1.5)
    ax3.tick_params(colors=text_color, labelsize=label_fontsize)
    ax3.set_facecolor(axes_bg_color)

    # --- Subplot 4: Segnale espanso Utente 2 ---
    t_chips2, chips2 = create_step_signal(user2_expanded, 1 / chip_rate)
    ax4.plot(
        t_chips2, chips2, color=user2_color, linewidth=2.5, label="Utente 2 * Codice 2"
    )
    ax4.set_title(
        "Segnale Espanso - Utente 2 (dopo spreading)",
        color=title_color,
        fontsize=title_fontsize,
    )
    ax4.set_ylabel("Ampiezza", color=text_color, fontsize=label_fontsize)
    ax4.grid(True, alpha=0.3, color=grid_color)
    ax4.set_ylim(-1.5, 1.5)
    ax4.tick_params(colors=text_color, labelsize=label_fontsize)
    ax4.set_facecolor(axes_bg_color)

    # --- Subplot 5: Segnale combinato trasmesso ---
    t_combined, combined_step = create_step_signal(combined_signal, 1 / chip_rate)
    ax5.plot(
        t_combined,
        combined_step,
        color=combined_color,
        linewidth=3,
        label="Segnale Combinato",
    )
    ax5.set_title(
        "Segnale Trasmesso (Somma dei Segnali Espansi)",
        color=title_color,
        fontsize=title_fontsize,
    )
    ax5.set_xlabel("Tempo (bit periods)", color=text_color, fontsize=label_fontsize)
    ax5.set_ylabel("Ampiezza", color=text_color, fontsize=label_fontsize)
    ax5.grid(True, alpha=0.3, color=grid_color)
    ax5.set_ylim(-2.5, 2.5)
    ax5.tick_params(colors=text_color, labelsize=label_fontsize)
    ax5.set_facecolor(axes_bg_color)

    # --- Subplot 6: Decodifica (correlazione con codice utente 1) ---
    def correlate_and_decode(received_signal, code, chip_rate):
        decoded_bits = []
        samples_per_bit = len(code)

        for i in range(len(received_signal) // samples_per_bit):
            start_idx = i * samples_per_bit
            end_idx = (i + 1) * samples_per_bit
            bit_segment = received_signal[start_idx:end_idx]

            # Correlazione con il codice
            correlation = np.sum(bit_segment * code) / len(code)
            # Decisione: se positivo -> +1, se negativo -> -1
            decoded_bit = 1 if correlation > 0 else -1
            decoded_bits.append(decoded_bit)

        return np.array(decoded_bits)

    decoded_user1 = correlate_and_decode(combined_signal, code1, chip_rate)
    decoded_t, decoded_step = create_step_signal(decoded_user1, 1)

    ax6.plot(
        decoded_t,
        decoded_step,
        color=decoded_color,
        linewidth=3,
        label="Dati Decodificati Utente 1",
    )
    ax6.plot(
        user1_step_t,
        user1_step,
        "--",
        color=reference_color,
        alpha=0.8,
        linewidth=2,
        label="Dati Originali (riferimento)",
    )
    ax6.set_title(
        "Decodifica Utente 1 (Correlazione con Codice 1)",
        color=title_color,
        fontsize=title_fontsize,
    )
    ax6.set_xlabel("Tempo (bit periods)", color=text_color, fontsize=label_fontsize)
    ax6.set_ylabel("Ampiezza", color=text_color, fontsize=label_fontsize)
    ax6.grid(True, alpha=0.3, color=grid_color)
    ax6.set_ylim(-1.5, 1.5)
    ax6.legend(
        labelcolor=legend_label_color, fontsize=legend_fontsize, loc="upper left"
    )
    ax6.tick_params(colors=text_color, labelsize=label_fontsize)
    ax6.set_facecolor(axes_bg_color)

    # Configura l'aspetto generale
    fig.suptitle(
        "Code Division Multiple Access (CDMA)", fontsize=18, color=title_color, y=0.95
    )
    fig.patch.set_facecolor(plot_bg_color)

    plt.tight_layout()
    plt.subplots_adjust(top=0.91)
    plt.savefig(
        f"images/{filename}",
        dpi=300,
        bbox_inches="tight",
        transparent=False,
        facecolor=fig.get_facecolor(),
    )
    print(f"Generato {filename}")
    plt.close()


# Genera i grafici
generate_tdm_graph()
generate_tfdm_graph()
generate_cdma_graph()


# terzo

# Configurazione
fs = 1000  # Frequenza di campionamento
T = 1  # Durata di un bit
t = np.linspace(0, 4 * T, 4 * fs)  # 4 bit di durata
fc = 50  # Frequenza portante
data_bits = [1, 0, 1, 0]  # Sequenza di bit da modulare

# Creazione della figura con più spazio verticale per 'terzo' e differenziazione tema
if is_dark_theme:
    figsize_terzo = (14, 16)  # Più spazio verticale per dark theme
    fig_bg_color = plot_bg_color
    suptitle_color = title_color
else:
    figsize_terzo = (14, 14)  # Leggermente più spazio per light theme
    fig_bg_color = plot_bg_color
    suptitle_color = title_color

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=figsize_terzo)
fig.patch.set_facecolor(fig_bg_color)
fig.suptitle(
    "Confronto Modulazioni Digitali: ASK, FSK, PSK",
    fontsize=16,
    fontweight="bold",
    color=suptitle_color,
)

# 1. Segnale digitale originale
digital_signal = np.zeros_like(t)
for i, bit in enumerate(data_bits):
    start_idx = i * fs
    end_idx = (i + 1) * fs
    digital_signal[start_idx:end_idx] = bit

ax1.plot(t, digital_signal, "b-", linewidth=3, label="Dati digitali")
ax1.set_ylim(-0.5, 1.5)
ax1.set_ylabel("Ampiezza", fontsize=12, color=text_color)
ax1.set_title(
    "Segnale Digitale Originale", fontsize=14, fontweight="bold", color=title_color
)
ax1.grid(True, alpha=0.3, color=grid_color)
ax1.legend(labelcolor=legend_label_color)
ax1.set_facecolor(axes_bg_color)
ax1.tick_params(axis="x", colors=text_color)
ax1.tick_params(axis="y", colors=text_color)

# Aggiunta etichette bit
for i, bit in enumerate(data_bits):
    ax1.text(
        i * T + T / 2,
        bit + 0.1,
        f"Bit {bit}",
        ha="center",
        fontsize=10,
        fontweight="bold",
    )

# 2. ASK (Amplitude Shift Keying)
ask_signal = np.zeros_like(t)
for i, bit in enumerate(data_bits):
    start_idx = i * fs
    end_idx = (i + 1) * fs
    t_bit = t[start_idx:end_idx]
    if bit == 1:
        ask_signal[start_idx:end_idx] = np.sin(2 * np.pi * fc * t_bit)
    else:
        ask_signal[start_idx:end_idx] = 0  # Spento per '0'

ax2.plot(t, ask_signal, "r-", linewidth=2, label="ASK")
ax2.set_ylabel("Ampiezza", fontsize=12, color=text_color)
ax2.set_title(
    "ASK - Amplitude Shift Keying\n(Semplice ON/OFF, suscettibile a interferenze)",
    fontsize=14,
    fontweight="bold",
    color="red" if not is_dark_theme else "lightcoral",
)
ax2.grid(True, alpha=0.3, color=grid_color)
ax2.legend(labelcolor=legend_label_color)
ax2.set_facecolor(axes_bg_color)
ax2.tick_params(axis="x", colors=text_color)
ax2.tick_params(axis="y", colors=text_color)

# Evidenziazione delle caratteristiche ASK
ax2.text(
    0.5 * T,
    0.7,
    "ON",
    ha="center",
    fontsize=10,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7),
)
ax2.text(
    1.5 * T,
    0,
    "OFF",
    ha="center",
    fontsize=10,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.7),
)

# 3. FSK (Frequency Shift Keying)
f1 = fc - 20  # Frequenza per '0'
f2 = fc + 20  # Frequenza per '1'
fsk_signal = np.zeros_like(t)

for i, bit in enumerate(data_bits):
    start_idx = i * fs
    end_idx = (i + 1) * fs
    t_bit = t[start_idx:end_idx]
    if bit == 1:
        fsk_signal[start_idx:end_idx] = np.sin(2 * np.pi * f2 * t_bit)
    else:
        fsk_signal[start_idx:end_idx] = np.sin(2 * np.pi * f1 * t_bit)

ax3.plot(t, fsk_signal, "g-", linewidth=2, label="FSK")
ax3.set_ylabel("Ampiezza", fontsize=12, color=text_color)
ax3.set_title(
    "FSK - Frequency Shift Keying\n(Due frequenze per '1' e '0', più robusta di ASK)",
    fontsize=14,
    fontweight="bold",
    color="green" if not is_dark_theme else "lightgreen",
)
ax3.grid(True, alpha=0.3, color=grid_color)
ax3.legend(labelcolor=legend_label_color)
ax3.set_facecolor(axes_bg_color)
ax3.tick_params(axis="x", colors=text_color)
ax3.tick_params(axis="y", colors=text_color)

# Etichette frequenze
ax3.text(
    0.5 * T,
    0.7,
    f"f₂={f2}Hz",
    ha="center",
    fontsize=9,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7),
)
ax3.text(
    1.5 * T,
    0.7,
    f"f₁={f1}Hz",
    ha="center",
    fontsize=9,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.7),
)

# 4. PSK (Phase Shift Keying)
psk_signal = np.zeros_like(t)
for i, bit in enumerate(data_bits):
    start_idx = i * fs
    end_idx = (i + 1) * fs
    t_bit = t[start_idx:end_idx]
    if bit == 1:
        psk_signal[start_idx:end_idx] = np.sin(2 * np.pi * fc * t_bit)  # Fase 0°
    else:
        psk_signal[start_idx:end_idx] = np.sin(
            2 * np.pi * fc * t_bit + np.pi
        )  # Fase 180°

ax4.plot(t, psk_signal, "m-", linewidth=2, label="PSK")
ax4.set_ylabel("Ampiezza", fontsize=12, color=text_color)
ax4.set_xlabel("Tempo (s)", fontsize=12, color=text_color)
ax4.set_title(
    "PSK - Phase Shift Keying\n(Varia la fase della portante, più robusta e complessa)",
    fontsize=14,
    fontweight="bold",
    color="purple" if not is_dark_theme else "plum",
)
ax4.grid(True, alpha=0.3, color=grid_color)
ax4.legend(labelcolor=legend_label_color)
ax4.set_facecolor(axes_bg_color)
ax4.tick_params(axis="x", colors=text_color)
ax4.tick_params(axis="y", colors=text_color)

# Etichette fasi
ax4.text(
    0.5 * T,
    0.7,
    "Fase 0°",
    ha="center",
    fontsize=9,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7),
)
ax4.text(
    1.5 * T,
    -0.7,
    "Fase 180°",
    ha="center",
    fontsize=9,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.7),
)

# Aggiunta di linee verticali per separare i bit
for i in range(1, len(data_bits)):
    for ax in [ax1, ax2, ax3, ax4]:
        ax.axvline(x=i * T, color=text_color, linestyle="--", alpha=0.5)

if is_dark_theme:
    text_box_facecolor = "darkgray"
    text_box_textcolor = "white"
    text_box_alpha = 0.9
else:
    text_box_facecolor = "lightyellow"
    text_box_textcolor = "black"
    text_box_alpha = 0.8


plt.tight_layout()
# Più spazio in basso per il terzo grafico con differenziazione dark/light
if is_dark_theme:
    plt.subplots_adjust(
        bottom=0.22, hspace=0.4
    )  # Più spazio verticale tra grafici per dark
else:
    plt.subplots_adjust(bottom=0.25, hspace=0.35)  # Leggermente meno spazio per light

plt.savefig(
    "images/modulation_comparison.png",
    dpi=300,
    bbox_inches="tight",
    facecolor=fig_bg_color,
)
# plt.show()

print("Immagine salvata come 'modulation_comparison.png'")
