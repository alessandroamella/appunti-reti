#!/usr/bin/env python3
"""
Script per generare diagrammi di visualizzazione delle subnet VLSM
Esempio 1: Rete 199.201.17.0/24
"""

import argparse

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import Rectangle

# Definizione globale dei colori per entrambi i temi
LIGHT_THEME_COLORS = {
    "root": "#E8E8E8",
    "N2": "#FFE66D",
    "N1": "#96CEB4",
    "N2A": "#FF6B6B",
    "N1B": "#4ECDC4",
    "N1A": "#45B7D1",
    "pie_colors": ["#FF6B6B", "#FFE66D", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57"],
}

DARK_THEME_COLORS = {
    "root": "#CCCCCC",
    "N2": "#B8860B",  # DarkGoldenRod
    "N1": "#2F4F4F",  # DarkSlateGray
    "N2A": "#8B0000",  # DarkRed
    "N1B": "#008B8B",  # DarkCyan
    "N1A": "#191970",  # MidnightBlue
    "pie_colors": ["#8B0000", "#B8860B", "#008B8B", "#191970", "#2F4F4F", "#FECA57"],
}


def setup_theme(dark_mode=False):
    """Configura il tema del grafico in base alla modalità"""
    if dark_mode:
        plt.style.use("dark_background")
        plt.rcParams["figure.facecolor"] = "black"
        plt.rcParams["axes.facecolor"] = "black"
        plt.rcParams["text.color"] = "white"
        plt.rcParams["axes.labelcolor"] = "white"
        plt.rcParams["xtick.color"] = "white"
        plt.rcParams["ytick.color"] = "white"
        plt.rcParams["grid.color"] = "gray"
        return "white", DARK_THEME_COLORS  # colore del testo e colori del tema
    else:
        plt.style.use("default")
        plt.rcParams["figure.facecolor"] = "white"
        plt.rcParams["axes.facecolor"] = "white"
        plt.rcParams["text.color"] = "black"
        plt.rcParams["axes.labelcolor"] = "black"
        plt.rcParams["xtick.color"] = "black"
        plt.rcParams["ytick.color"] = "black"
        plt.rcParams["grid.color"] = "gray"
        return "black", LIGHT_THEME_COLORS  # colore del testo e colori del tema


# Configurazione matplotlib per testo di qualità
plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 10


def create_pie_chart(dark_mode=False):
    """Crea un diagramma a torta della suddivisione dello spazio di indirizzi"""
    text_color, colors = setup_theme(dark_mode)

    # Dati delle subnet
    labels = [
        "N2A\n(42 host)\n/26",
        "N2 resto\n(77 host)",
        "N1B\n(15 host)\n/27",
        "N1A\n(6 host)\n/29",
        "N1 resto\n(88 host)",
        "Non allocato",
    ]
    sizes = [64, 64, 32, 8, 88, 0]  # Dimensioni in numero di indirizzi
    colors_list = colors["pie_colors"]
    explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0)  # "esplodi" le fette per evidenziarle

    fig, ax = plt.subplots(figsize=(10, 8))

    wedges, texts, autotexts = ax.pie(
        sizes,
        explode=explode,
        labels=labels,
        colors=colors_list,
        autopct=lambda pct: f"{pct:.1f}%\n({int(pct/100*256)} IP)",
        shadow=True,
        startangle=90,
        textprops={"fontsize": 12},
    )

    # Migliora il testo
    for autotext in autotexts:
        autotext.set_color(text_color)
        autotext.set_fontweight("bold")
        autotext.set_fontsize(10)

    ax.set_title(
        "Suddivisione dello Spazio di Indirizzi\nRete 199.201.17.0/24 (256 indirizzi totali)",
        fontsize=14,
        fontweight="bold",
        pad=20,
        color=text_color,
    )

    plt.tight_layout()
    plt.savefig(
        "images/subnet_pie_chart.png",
        bbox_inches="tight",
        facecolor="black" if dark_mode else "white",
    )
    plt.close()
    print("✓ Generato: subnet_pie_chart.png")


def create_linear_diagram(dark_mode=False):
    """Crea un diagramma lineare che mostra la suddivisione sequenziale"""
    text_color, colors = setup_theme(dark_mode)

    fig, ax = plt.subplots(figsize=(14, 8))

    # Definizione delle subnet con i loro range
    subnets = [
        {
            "name": "N2A",
            "start": 0,
            "end": 63,
            "color": colors["N2A"],
            "mask": "/26",
            "hosts": 42,
        },
        {
            "name": "N2 resto",
            "start": 64,
            "end": 127,
            "color": colors["N2"],
            "mask": "/25",
            "hosts": 77,
        },
        {
            "name": "N1B",
            "start": 128,
            "end": 159,
            "color": colors["N1B"],
            "mask": "/27",
            "hosts": 15,
        },
        {
            "name": "N1A",
            "start": 160,
            "end": 167,
            "color": colors["N1A"],
            "mask": "/29",
            "hosts": 6,
        },
        {
            "name": "N1 resto",
            "start": 168,
            "end": 255,
            "color": colors["N1"],
            "mask": "/25",
            "hosts": 88,
        },
    ]

    # Disegna la barra principale
    main_rect = Rectangle(
        (0, 2),
        256,
        1,
        linewidth=2,
        edgecolor=text_color,
        facecolor="lightgray",
        alpha=0.3,
    )
    ax.add_patch(main_rect)
    ax.text(
        128,
        2.5,
        "199.201.17.0/24 (256 indirizzi)",
        ha="center",
        va="center",
        fontweight="bold",
        fontsize=14,
        color=text_color,
    )

    # Disegna le subnet
    y_pos = 0.5
    for subnet in subnets:
        width = subnet["end"] - subnet["start"] + 1
        rect = Rectangle(
            (subnet["start"], y_pos),
            width,
            1,
            linewidth=1.5,
            edgecolor=text_color,
            facecolor=subnet["color"],
            alpha=0.7,
        )
        ax.add_patch(rect)

        # Etichetta della subnet
        center_x = subnet["start"] + width / 2
        ax.text(
            center_x,
            y_pos + 0.5,
            f"{subnet['name']}\n{subnet['mask']}\n{subnet['hosts']} host",
            ha="center",
            va="center",
            fontweight="bold",
            fontsize=11,
            color=text_color,
        )

        # Linee di collegamento
        ax.plot(
            [center_x, center_x],
            [y_pos + 1, 2],
            color=text_color,
            linestyle="--",
            alpha=0.5,
            linewidth=1,
        )

    # Aggiungi scale numeriche
    major_ticks = [0, 64, 128, 192, 256]
    minor_ticks = list(range(0, 257, 32))

    ax.set_xlim(-10, 266)
    ax.set_ylim(0, 4)
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_xlabel(
        "Indirizzi IP (199.201.17.x)", fontsize=14, color=text_color, labelpad=45
    )
    ax.set_yticks([])
    ax.grid(True, which="major", alpha=0.7)
    ax.grid(True, which="minor", alpha=0.3)

    # Aggiungi etichette degli indirizzi chiave
    key_addresses = [0, 63, 64, 127, 128, 159, 160, 167, 168, 255]
    # Process pairs of addresses to show boundaries
    for i in range(1, len(key_addresses) - 1, 2):
        boundary = key_addresses[i]  # This is where one subnet ends
        next_start = key_addresses[i + 1]  # This is where next subnet starts
        # Draw vertical line at the boundary
        ax.axvline(x=boundary, color="red", linestyle=":", alpha=0.7)
        # Add combined label for the boundary
        ax.text(
            boundary + 4,
            -0.15,
            f".{boundary} - .{next_start}",
            rotation=45,
            ha="right",
            va="top",
            fontsize=10,
            color=text_color,
        )

    ax.set_title(
        "Suddivisione Lineare delle Subnet\nRete 199.201.17.0/24",
        fontsize=14,
        fontweight="bold",
        pad=20,
        color=text_color,
    )

    plt.tight_layout()
    plt.savefig(
        "images/subnet_linear_diagram.png",
        bbox_inches="tight",
        facecolor="black" if dark_mode else "white",
    )
    plt.close()
    print("✓ Generato: subnet_linear_diagram.png")


def create_hierarchy_diagram(dark_mode=False):
    """Crea un diagramma gerarchico delle subnet"""
    text_color, colors = setup_theme(dark_mode)

    # Aumento le dimensioni della figura e aggiungo più padding
    fig, ax = plt.subplots(figsize=(14, 12))

    # Creiamo un grafo direzionale
    G = nx.DiGraph()

    # Aggiungiamo i nodi con le loro proprietà
    nodes = {
        "N\n199.201.17.0/24": {"level": 0, "color": colors["root"], "size": 20000},
        "N2\n199.201.17.0/25\n(119 host)": {
            "level": 1,
            "color": colors["N2"],
            "size": 18000,
        },
        "N1\n199.201.17.128/25\n(64 host)": {
            "level": 1,
            "color": colors["N1"],
            "size": 18000,
        },
        "N2A\n199.201.17.0/26\n(42 host)": {
            "level": 2,
            "color": colors["N2A"],
            "size": 16000,
        },
        "N1B\n199.201.17.128/27\n(15 host)": {
            "level": 2,
            "color": colors["N1B"],
            "size": 16000,
        },
        "N1A\n199.201.17.160/29\n(6 host)": {
            "level": 2,
            "color": colors["N1A"],
            "size": 16000,
        },
    }

    # Aggiungiamo i nodi al grafo
    for node, props in nodes.items():
        G.add_node(node, **props)

    # Aggiungiamo gli archi (relazioni gerarchiche)
    edges = [
        ("N\n199.201.17.0/24", "N2\n199.201.17.0/25\n(119 host)"),
        ("N\n199.201.17.0/24", "N1\n199.201.17.128/25\n(64 host)"),
        ("N2\n199.201.17.0/25\n(119 host)", "N2A\n199.201.17.0/26\n(42 host)"),
        ("N1\n199.201.17.128/25\n(64 host)", "N1B\n199.201.17.128/27\n(15 host)"),
        ("N1\n199.201.17.128/25\n(64 host)", "N1A\n199.201.17.160/29\n(6 host)"),
    ]

    G.add_edges_from(edges)

    # Calcoliamo le posizioni usando un layout gerarchico
    pos = {}
    level_nodes = {}

    # Raggruppiamo i nodi per livello
    for node, props in nodes.items():
        level = props["level"]
        if level not in level_nodes:
            level_nodes[level] = []
        level_nodes[level].append(node)

    # Assegniamo le posizioni con più spazio verticale
    for level, node_list in level_nodes.items():
        y = 1 - level * 0.5  # Ridotto il moltiplicatore per dare più spazio
        if len(node_list) == 1:
            pos[node_list[0]] = (0, y)
        else:
            x_positions = np.linspace(
                -0.2, 0.2, len(node_list)
            )  # Aumentato lo spread orizzontale
            for i, node in enumerate(node_list):
                pos[node] = (x_positions[i], y)

    # Disegniamo il grafo
    node_colors = [nodes[node]["color"] for node in G.nodes()]
    node_sizes = [nodes[node]["size"] for node in G.nodes()]

    nx.draw(
        G,
        pos,
        ax=ax,
        node_color=node_colors,
        node_size=node_sizes,
        with_labels=True,
        font_size=14,
        font_weight="bold",
        font_color=text_color,
        edge_color=text_color,
        arrows=True,
        arrowsize=25,
        arrowstyle="->,head_width=0.8,head_length=1",
        node_shape="o",
    )

    ax.set_title(
        "Gerarchia delle Subnet\nRete 199.201.17.0/24",
        fontsize=16,
        fontweight="bold",
        pad=60,
        color=text_color,
    )
    ax.axis("off")

    # Aggiungo più padding intorno alla figura
    plt.tight_layout(pad=3.0)
    plt.savefig(
        "images/subnet_hierarchy.png",
        bbox_inches="tight",
        facecolor="black" if dark_mode else "white",
    )
    plt.close()
    print("✓ Generato: subnet_hierarchy.png")


def create_address_blocks(dark_mode=False):
    """Crea un diagramma a blocchi degli indirizzi"""
    text_color, colors = setup_theme(dark_mode)

    fig, ax = plt.subplots(figsize=(16, 10))

    # Configurazione griglia 16x16 per rappresentare 256 indirizzi
    grid_size = 16

    # Mappa degli indirizzi alle subnet
    subnet_map = {}

    # N2A: 0-63
    for i in range(64):
        subnet_map[i] = {"name": "N2A", "color": colors["N2A"]}

    # N2 resto: 64-127
    for i in range(64, 128):
        subnet_map[i] = {"name": "N2", "color": colors["N2"]}

    # N1B: 128-159
    for i in range(128, 160):
        subnet_map[i] = {"name": "N1B", "color": colors["N1B"]}

    # N1A: 160-167
    for i in range(160, 168):
        subnet_map[i] = {"name": "N1A", "color": colors["N1A"]}

    # N1 resto: 168-255
    for i in range(168, 256):
        subnet_map[i] = {"name": "N1", "color": colors["N1"]}

    # Disegna la griglia
    for i in range(256):
        row = i // grid_size
        col = i % grid_size

        if i in subnet_map:
            color = subnet_map[i]["color"]
            alpha = 0.8
        else:
            color = "lightgray"
            alpha = 0.3

        rect = Rectangle(
            (col, grid_size - 1 - row),
            1,
            1,
            facecolor=color,
            alpha=alpha,
            edgecolor=text_color,
            linewidth=0.5,
        )
        ax.add_patch(rect)

        # Aggiungi il numero dell'indirizzo per alcuni blocchi chiave
        if i % 16 == 0 or i in [63, 127, 159, 167, 255]:
            ax.text(
                col + 0.5,
                grid_size - 1 - row + 0.5,
                str(i),
                ha="center",
                va="center",
                fontsize=6,
                fontweight="bold",
                color=text_color,
            )

    # Aggiungi legenda
    legend_elements = [
        patches.Patch(color=colors["N2A"], alpha=0.8, label="N2A (0-63) /26"),
        patches.Patch(color=colors["N2"], alpha=0.8, label="N2 resto (64-127)"),
        patches.Patch(color=colors["N1B"], alpha=0.8, label="N1B (128-159) /27"),
        patches.Patch(color=colors["N1A"], alpha=0.8, label="N1A (160-167) /29"),
        patches.Patch(color=colors["N1"], alpha=0.8, label="N1 resto (168-255)"),
    ]

    ax.legend(
        handles=legend_elements,
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        labelcolor=text_color,
    )

    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_aspect("equal")
    ax.set_title(
        "Mappa degli Indirizzi IP\nRete 199.201.17.0/24 (griglia 16×16 = 256 indirizzi)",
        fontsize=14,
        fontweight="bold",
        pad=20,
        color=text_color,
    )

    # Rimuovi i tick
    ax.set_xticks([])
    ax.set_yticks([])

    # Aggiungi etichette degli assi
    ax.text(
        grid_size / 2,
        -0.5,
        "Ogni quadrato = 1 indirizzo IP",
        ha="center",
        va="top",
        fontsize=10,
        style="italic",
        color=text_color,
    )

    plt.tight_layout()
    plt.savefig(
        "images/subnet_address_blocks.png",
        bbox_inches="tight",
        facecolor="black" if dark_mode else "white",
    )
    plt.close()
    print("✓ Generato: subnet_address_blocks.png")


def main():
    """Funzione principale che genera tutti i diagrammi"""
    parser = argparse.ArgumentParser(
        description="Genera diagrammi di visualizzazione delle subnet VLSM"
    )
    parser.add_argument(
        "--dark", action="store_true", help="Usa il tema scuro per i diagrammi"
    )
    args = parser.parse_args()

    print("Generazione diagrammi subnet VLSM...")
    print("=" * 50)

    create_pie_chart(args.dark)
    create_linear_diagram(args.dark)
    create_hierarchy_diagram(args.dark)
    create_address_blocks(args.dark)

    print("=" * 50)
    print("✅ Tutti i diagrammi sono stati generati con successo!")
    print("\nFile generati:")
    print("- subnet_pie_chart.png")
    print("- subnet_linear_diagram.png")
    print("- subnet_hierarchy.png")
    print("- subnet_address_blocks.png")


if __name__ == "__main__":
    main()
