import os

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from diagrams import Cluster, Diagram, Edge
from diagrams.generic.compute import Rack
from diagrams.generic.network import Router, Subnet

# Create main diagram with a dark background
with Diagram(
    show=False,
    filename="images/reti_di_reti",
    outformat="png",
    direction="LR",
    graph_attr={
        # "bgcolor": "#121212",
        "bgcolor": "transparent",
        # "fontcolor": "white",
        "fontcolor": "black",
        "fontsize": "20",
        "pad": "0.5",
    },
):

    # Create physical network view (left side)
    with Cluster(
        # "Vista Rete Fisica", graph_attr={"bgcolor": "#1a1a1a", "fontcolor": "white"}
        "Vista Rete Fisica",
        graph_attr={"bgcolor": "white", "fontcolor": "black"},
    ):
        # Create LAN nodes with a consistent color
        lan_z = Subnet("LAN Z")
        lan_k = Subnet("LAN K")
        lan_x = Subnet("LAN X")
        lan_y = Subnet("LAN Y")

        # Create router nodes
        rz = Router("Rz")
        rk = Router("Rk")
        rx = Router("Rx")
        ry = Router("Ry")

        # Connect LANs to their routers
        lan_z >> rz
        lan_k >> rk
        lan_x >> rx
        lan_y >> ry

        # Connect routers to each other
        rz >> rk
        rk >> rx
        rx >> ry
        rz >> rx

    # Create abstract router view (right side)
    with Cluster(
        # "Vista Astratta Router", graph_attr={"bgcolor": "#1a1a1a", "fontcolor": "white"}
        "Vista Astratta Router",
        graph_attr={"bgcolor": "white", "fontcolor": "black"},
    ):
        # Create abstract router nodes
        rz_abs = Router("Rz")
        rk_abs = Router("Rk")
        rx_abs = Router("Rx")
        ry_abs = Router("Ry")

        # Connect abstract routers
        rz_abs >> rk_abs
        rk_abs >> rx_abs
        rx_abs >> ry_abs
        rz_abs >> rx_abs

print("Diagram created and saved to images/reti_di_reti.png")

# Set graph attributes for better layout
graph_attr = {
    "fontsize": "14",
    "bgcolor": "white",
    "rankdir": "LR",
    "splines": "spline",
    "pad": "0.5",
    "nodesep": "0.8",
    "ranksep": "1.5",
}

# Create the diagram
with Diagram(
    # "Percorso di un pacchetto IP attraverso diverse reti",
    show=False,
    filename="images/percorso_pacchetto",
    direction="LR",
    outformat="png",
    graph_attr=graph_attr,
):

    # Hosts
    h1 = Rack("140.217.2.10")
    h2 = Rack("130.136.2.33")

    # Routers
    ry2 = Router("Ry2\n140.217.2.254")
    ry = Router("Ry\n140.217.0.254")
    rz = Router("Rz\n190.89.0.254")
    rk = Router("Rk\n130.136.0.254")
    rk2 = Router("Rk2\n130.136.2.254")

    # Draw connections with labels
    h1 >> Edge(label="1") >> ry2
    ry2 >> Edge(label="2") >> ry
    ry >> Edge(label="3") >> rz
    rz >> Edge(label="4") >> rk
    rk >> Edge(label="5") >> rk2
    rk2 >> Edge(label="6") >> h2

    # Add network labels (not directly supported, but you can add notes)
    # For actual cloud-like networks, consider using cluster subgraphs in a more advanced implementation

print("Diagram created and saved to images/percorso_pacchetto.png")

# Create ARP protocol diagram using diagrams library
with Diagram(
    show=False,
    filename="images/arp_simulation",
    outformat="png",
    direction="LR",
    graph_attr={
        "fontsize": "14",
        "bgcolor": "white",
        "rankdir": "LR",
        "splines": "spline",
        "pad": "0.5",
    },
):
    # Create devices
    pc_a = Rack("PC_A\n192.168.1.10\nMAC: AA:BB:CC:DD:EE:01")
    pc_b = Rack("PC_B\n192.168.1.20\nMAC: AA:BB:CC:DD:EE:02")
    pc_c = Rack("PC_C\n192.168.1.30\nMAC: AA:BB:CC:DD:EE:03")

    # Connect devices showing ARP process
    # 1. ARP Request (broadcast)
    pc_a >> Edge(label="1. ARP Request\n(broadcast)", color="red") >> pc_b
    pc_a >> Edge(label="", color="red", style="dashed") >> pc_c

    # 2. ARP Reply (unicast)
    pc_b >> Edge(label="2. ARP Reply\n(unicast)", color="green") >> pc_a

    # 3. Direct communication
    pc_a >> Edge(label="3. Communication\n(using MAC)", color="blue") >> pc_b

print("ARP diagram created and saved to images/arp_simulation.png")


# Impostare lo stile e dimensioni della figura
plt.figure(figsize=(12, 10))
plt.axis("off")
ax = plt.gca()


# immagine DHCP

# Crea la cartella images se non esiste
os.makedirs("images", exist_ok=True)

# Configurazione figura
fig, ax = plt.subplots(figsize=(14, 10))
ax.set_aspect("equal")
ax.axis("off")

# Colori personalizzati
themeblue = "#3498db"
green_color = "#27ae60"
orange_color = "#e67e22"
purple_color = "#8e44ad"
gray_color = "#ecf0f1"
yellow_color = "#f1c40f"

# Creazione dei nodi
# Client DHCP
client_rect = patches.Rectangle(
    (-1, 8), 2, 1.2, facecolor=gray_color, edgecolor="black", linewidth=1, zorder=2
)
ax.add_patch(client_rect)
plt.text(0, 8.6, "Client DHCP", ha="center", va="center", fontweight="bold")
plt.text(0, 8.2, "IP: ???", ha="center", va="center", fontfamily="monospace")

# Server DHCP
server_rect = patches.Rectangle(
    (9, 8), 2, 1.5, facecolor=yellow_color, edgecolor="black", linewidth=1, zorder=2
)
ax.add_patch(server_rect)
plt.text(10, 8.75, "Server DHCP", ha="center", va="center", fontweight="bold")
plt.text(10, 8.25, "IP: 192.168.1.1", ha="center", va="center", fontfamily="monospace")

# Altro server
other_rect = patches.Rectangle(
    (4, 3), 2, 1.2, facecolor=gray_color, edgecolor="black", linewidth=1, zorder=2
)
ax.add_patch(other_rect)
plt.text(5, 3.6, "Altro server", ha="center", va="center", fontweight="bold")
plt.text(5, 3.2, "IP: 192.168.1.2", ha="center", va="center", fontfamily="monospace")

# Linea di rete
plt.plot([-2, 12], [6, 6], "k-", linewidth=2, zorder=1)
plt.plot([0, 0], [8, 6], "k-", linewidth=2, zorder=1)
plt.plot([10, 10], [8, 6], "k-", linewidth=2, zorder=1)
plt.plot([5, 5], [3, 6], "k-", linewidth=2, zorder=1)

# Messaggi DHCP con frecce
# 1. DISCOVER (Broadcast)
plt.arrow(
    0,
    6.1,
    9.5,
    0,
    color=themeblue,
    linestyle="--",
    linewidth=2,
    head_width=0.2,
    head_length=0.3,
    length_includes_head=True,
    zorder=3,
)
discover_rect = patches.Rectangle(
    (3, 7), 4, 0.7, facecolor=themeblue, edgecolor="black", linewidth=1, zorder=3
)
ax.add_patch(discover_rect)
plt.text(
    5,
    7.35,
    "1. DHCP DISCOVER (Broadcast)",
    ha="center",
    va="center",
    fontweight="bold",
    color="white",
)
plt.text(
    5,
    6.7,
    '"Chi è il server DHCP? Ho bisogno di un IP"',
    ha="center",
    va="center",
    fontsize=12,
    style="italic",
)

# 2. OFFER
plt.arrow(
    10,
    5.9,
    -9.5,
    0,
    color=green_color,
    linewidth=2,
    head_width=0.2,
    head_length=0.3,
    length_includes_head=True,
    zorder=3,
)
offer_rect = patches.Rectangle(
    (3, 5),
    4,
    0.7,
    facecolor=green_color,
    edgecolor="black",
    linewidth=1,
    zorder=3,
)
ax.add_patch(offer_rect)
plt.text(
    5, 5.35, "2. DHCP OFFER", ha="center", va="center", fontweight="bold", color="white"
)
plt.text(
    5,
    4.7,
    '"Ti offro IP 192.168.1.10, netmask 255.255.255.0"',
    ha="center",
    va="center",
    fontsize=12,
    style="italic",
)

# 3. REQUEST (Broadcast)
plt.arrow(
    0,
    2.9,
    9.5,
    0,
    color=orange_color,
    linewidth=2,
    head_width=0.2,
    head_length=0.3,
    length_includes_head=True,
    zorder=3,
)
request_rect = patches.Rectangle(
    (3, 2),
    4,
    0.7,
    facecolor=orange_color,
    edgecolor="black",
    linewidth=1,
    zorder=3,
)
ax.add_patch(request_rect)
plt.text(
    5,
    2.35,
    "3. DHCP REQUEST (Broadcast)",
    ha="center",
    va="center",
    fontweight="bold",
    color="white",
)
plt.text(
    5,
    1.7,
    '"Accetto IP 192.168.1.10 dal server 192.168.1.1"',
    ha="center",
    va="center",
    fontsize=12,
    style="italic",
)

# 4. ACK
plt.arrow(
    10,
    1.1,
    -9.5,
    0,
    color=purple_color,
    linewidth=2,
    head_width=0.2,
    head_length=0.3,
    length_includes_head=True,
    zorder=3,
)
ack_rect = patches.Rectangle(
    (3, 0.3),
    4,
    0.7,
    facecolor=purple_color,
    edgecolor="black",
    linewidth=1,
    zorder=3,
)
ax.add_patch(ack_rect)
plt.text(
    5, 0.65, "4. DHCP ACK", ha="center", va="center", fontweight="bold", color="white"
)
plt.text(
    5,
    0.1,
    '"IP 192.168.1.10 è tuo per 24 ore"',
    ha="center",
    va="center",
    fontsize=12,
    style="italic",
)

# Impostazioni finali
plt.xlim(-2, 12)
plt.ylim(-0.5, 10)

# Salva l'immagine
plt.tight_layout()
plt.savefig("images/dhcp_process.png", dpi=300, bbox_inches="tight", facecolor="white")

print("✅ Immagine 'images/dhcp_process.png' creata con successo!")
