# Ensure the images directory exists
import os

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.generic.database import SQL
from diagrams.generic.device import Mobile
from diagrams.generic.storage import Storage
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.programming.language import Python

if not os.path.exists("images"):
    os.makedirs("images")


def create_cookie_flow():
    """Creates a diagram showing the cookie interaction flow"""
    with Diagram(
        "Cookie Interaction Flow",
        filename="images/cookie_flow",
        show=False,
        direction="LR",  # Left to Right direction
        outformat="png",
        graph_attr={
            "splines": "ortho",
            "nodesep": "1",
            "ranksep": "1.5",
            "fontsize": "20",
        },
    ):
        # Create main components
        client = Client("Client")
        server = Server("Server")
        db = SQL("Database")
        cookie = Storage("Cookie\nFile")

        # Initial request
        client - Edge(label="1. Initial HTTP Request") >> server

        # Set cookie response
        server - Edge(label="2. HTTP Response + Set-Cookie: ID=1678") >> client

        # Internal operations
        server - Edge(label="Create ID") >> db
        client - Edge(label="Save Cookie") >> cookie

        # Subsequent request with cookie
        client - Edge(label="3. HTTP Request + Cookie: ID=1678") >> server
        cookie - Edge(label="Read Cookie") >> client
        server - Edge(label="Retrieve Info") >> db
        server - Edge(label="4. Personalized Response") >> client


def create_email_flow():
    """Creates a diagram showing email flow between Alice and Bob"""
    with Diagram(
        "Email Flow",
        filename="images/email_flow",
        show=False,
        direction="LR",
        outformat="png",
        graph_attr={
            "splines": "ortho",
            "nodesep": "1",
            "ranksep": "1.5",
            "fontsize": "20",
        },
    ):
        # Create components
        alice_ua = Client("Alice's UA")
        alice_server = Server("Alice's\nMail Server")
        bob_server = Server("Bob's\nMail Server")
        bob_ua = Client("Bob's UA")

        # Draw connections
        alice_ua - Edge(label="1. Compose & Send") >> alice_server
        alice_server - Edge(label="2. SMTP (TCP)") >> bob_server
        bob_server - Edge(label="Message in queue") >> alice_server
        bob_server - Edge(label="3. Bob retrieves mail") >> bob_ua


if __name__ == "__main__":
    create_cookie_flow()
    create_email_flow()
    print("Images generated in images/ directory")
