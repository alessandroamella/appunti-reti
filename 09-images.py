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


def generate_tdm_graph(filename="tdm_multiplexing.png"):
    """
    Generates a 3D graph illustrating Time Division Multiplexing (TDM).
    Shows input signals stacked on Z-axis and the multiplexed output
    as segments on a lower Z-level, transmitted sequentially over time.
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")
    plt.style.use("dark_background")  # Modern dark background

    # --- Parameters for TDM ---
    total_time = 4  # seconds
    num_samples = 400
    t = np.linspace(0, total_time, num_samples)

    # Define individual signals
    signal_colors = ["red", "green", "blue", "orange"]
    signal_labels = [
        "Signal A (1Hz)",
        "Signal B (2Hz)",
        "Signal C (3Hz)",
        "Signal D (4Hz)",
    ]
    frequencies = [1, 2, 3, 4]
    num_signals = len(frequencies)

    # Z-axis for input signals (representing distinct "Source" levels)
    input_z_levels = np.linspace(2.5, 0.5, num_signals)  # Higher Z for first signal

    # Plotting individual input signals
    for i in range(num_signals):
        sig = np.sin(2 * np.pi * frequencies[i] * t)
        ax.plot(
            t,
            [input_z_levels[i]] * num_samples,
            sig,
            color=signal_colors[i],
            label=signal_labels[i],
            linewidth=1.5,
            alpha=0.8,
        )

    # --- Constructing the multiplexed output ---
    output_z_level = -1.0  # Z-axis for the multiplexed output
    time_points_per_slot = num_samples // num_signals

    # Plotting segments of the multiplexed signal
    # The following lists were declared but never used, so they are removed.
    # multiplexed_t = []
    # multiplexed_sig = []
    # multiplexed_colors = []

    for i in range(num_signals):
        start_idx = i * time_points_per_slot
        end_idx = (i + 1) * time_points_per_slot

        # Ensure the last segment goes to the end of time
        if i == num_signals - 1:
            segment_t = t[start_idx:]
            segment_sig = np.sin(2 * np.pi * frequencies[i] * segment_t)
        else:
            segment_t = t[start_idx:end_idx]
            segment_sig = np.sin(2 * np.pi * frequencies[i] * segment_t)

        ax.plot(
            segment_t,
            [output_z_level] * len(segment_t),
            segment_sig,
            color=signal_colors[i],
            linewidth=3,
            alpha=0.9,
            label=(
                f'Output Slot {i+1} (from {signal_labels[i].split(" ")[0]})'
                if i == 0
                else None
            ),
        )  # Label only first output segment

        # Optional: Add small vertical lines to indicate time slot boundaries
        if i < num_signals - 1:
            ax.plot(
                [t[end_idx], t[end_idx]],
                [output_z_level, output_z_level],
                [-1.2, 1.2],
                color="gray",
                linestyle="--",
                linewidth=0.8,
                alpha=0.6,
            )

    # --- Set up the plot ---
    ax.set_xlabel("Time (s)", labelpad=15, fontsize=12, color="white")
    ax.set_ylabel("Channel / Source Level", labelpad=15, fontsize=12, color="white")
    ax.set_zlabel("Amplitude", labelpad=15, fontsize=12, color="white")
    ax.set_title("Time Division Multiplexing (TDM)", fontsize=16, color="white")

    # Customize Y-axis ticks to show meaning
    y_tick_positions = [output_z_level] + list(input_z_levels)
    y_tick_labels = ["Multiplexed Output"] + [
        f"Source {chr(65+i)}" for i in range(num_signals)
    ]
    ax.set_yticks(y_tick_positions)
    ax.set_yticklabels(y_tick_labels, fontsize=10, color="white")
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="z", colors="white")

    ax.set_ylim(min(y_tick_positions) - 0.5, max(y_tick_positions) + 0.5)
    ax.set_zlim(-1.5, 1.5)
    ax.set_xlim(0, total_time)

    # Adjust view angle for better 3D visualization
    ax.view_init(elev=25, azim=-60)

    # Add a legend for the input signals
    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.25, 0.95),
        frameon=False,
        fontsize=10,
        facecolor="none",
        edgecolor="none",
        labelcolor="white",
    )

    plt.tight_layout()
    plt.savefig(f"images/{filename}", dpi=300, bbox_inches="tight", transparent=True)
    print(f"Generated {filename}")
    plt.close()


def generate_tfdm_graph(filename="tfdm_multiplexing.png"):
    """
    Generates a 3D graph illustrating Time and Frequency Division Multiplexing (TFDM).
    Shows different signals as peaks in the Time-Frequency-Amplitude space.
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")
    plt.style.use("dark_background")  # Modern dark background

    # --- Parameters for TFDM ---
    time_res = 200  # number of points for time axis
    freq_res = 150  # number of points for frequency axis

    t = np.linspace(0, 5, time_res)  # Time (X-axis)
    f = np.linspace(0, 10, freq_res)  # Frequency (Y-axis)
    T, F = np.meshgrid(t, f)

    # Initialize amplitude/power (Z-axis) to zeros
    Z = np.zeros_like(T)

    # Define individual signals as Gaussian bumps in Time-Frequency space
    # (t_center, f_center, t_std_dev, f_std_dev, amplitude)
    signals = [
        (1.0, 2.0, 0.2, 0.5, 1.0),  # Signal 1: Early time, low freq
        (2.5, 7.0, 0.2, 0.5, 1.0),  # Signal 2: Mid time, high freq
        (
            1.5,
            4.0,
            0.2,
            0.5,
            1.0,
        ),  # Signal 3: Overlaps in time with S1, but different freq
        (4.0, 3.0, 0.2, 0.5, 1.0),  # Signal 4: Late time, mid freq (distinct from S3)
        (2.0, 8.5, 0.2, 0.5, 1.0),  # Signal 5: Overlaps in time with S2, different freq
    ]

    # Add each signal's "power" to the Z-matrix
    for tc, fc, ts, fs, amp in signals:
        Z += amp * np.exp(-((T - tc) ** 2 / (2 * ts**2) + (F - fc) ** 2 / (2 * fs**2)))

    # --- Plotting the 3D surface ---
    surf = ax.plot_surface(T, F, Z, cmap="viridis", edgecolor="none", alpha=0.9)

    # --- Set up the plot ---
    ax.set_xlabel("Time (s)", labelpad=15, fontsize=12, color="white")
    ax.set_ylabel("Frequency (Hz)", labelpad=15, fontsize=12, color="white")
    ax.set_zlabel("Amplitude / Power", labelpad=15, fontsize=12, color="white")
    ax.set_title(
        "Time and Frequency Division Multiplexing (TFDM)", fontsize=16, color="white"
    )

    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")
    ax.tick_params(axis="z", colors="white")

    ax.set_zlim(0, 1.2)  # Set Z-axis limit
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 10)

    # Adjust view angle for better 3D visualization
    ax.view_init(elev=35, azim=-120)

    # Add a color bar
    cbar = fig.colorbar(surf, shrink=0.5, aspect=10, pad=0.1)
    cbar.set_label("Signal Intensity", color="white", fontsize=10)
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="white")

    plt.tight_layout()
    plt.savefig(f"images/{filename}", dpi=300, bbox_inches="tight", transparent=True)
    print(f"Generated {filename}")
    plt.close()


generate_tdm_graph()
generate_tfdm_graph()
