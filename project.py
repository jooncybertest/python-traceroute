import json
import requests
import webbrowser
import os
import time
from scapy.layers.inet import socket
from scapy.layers.inet import traceroute
from gmplot import gmplot
import sys

# Plot coordinates onto Google Maps
def plot_lat_long(gmap, latitude, longitude, sequence, color, labeled_coords):
    if latitude is not None and longitude is not None:
        coord_str = f"{latitude},{longitude}"
        if coord_str not in labeled_coords:
            print(f"Plotting: {latitude}, {longitude} with label {sequence} and color {color}")
            gmap.marker(latitude, longitude, label=str(sequence), color=color)
            labeled_coords.add(coord_str)

# Find and plot coordinates
def find_and_plot_coordinates(hostname):
    print("Getting public IP address...")
    public_ip = get_public_ip()
    if public_ip:
        print(f"Public IP address: {public_ip}")
        try:
            # Convert hostname to IP address
            print(f"Resolving hostname {hostname} to IP address...")
            ip = socket.gethostbyname(hostname)
            print(f"Hostname {hostname} resolved to IP address {ip}")

            # Perform traceroute
            print(f"Performing traceroute to {ip}...")
            res, _ = traceroute(ip, maxttl=64, verbose=0)
            print("Traceroute completed.")

            # Initialize Google Maps plotter
            gmap = gmplot.GoogleMapPlotter(0, 0, 3)

            # Store retrieved IPs
            ips = []

            # Extract IP addresses from the traceroute results
            print("Extracting IP addresses from traceroute results...")
            for item in res.get_trace()[ip]:
                ips.append(res.get_trace()[ip][item][0])
            print(f"IP addresses extracted: {ips}")

            # Define color for route line
            route_color = 'blue'

            # Find coordinates and plot them
            sequence = 1
            labeled_coords = set()  # Initialize set to store labeled coordinates
            for i, ip_address in enumerate(ips):
                print(f"Processing IP address {ip_address}...")
                if i == 0:
                    latitude, longitude = public_ip_to_coordinates(public_ip)
                    plot_lat_long(gmap, latitude, longitude, "Public IP", route_color, labeled_coords)
                else:
                    latitude, longitude = ip_to_coordinates(ip_address)
                    coord_str = f"{latitude},{longitude}"
                    if latitude is not None and longitude is not None and coord_str not in labeled_coords:
                        label_color = get_label_color(sequence) if i != 0 else route_color
                        plot_lat_long(gmap, latitude, longitude, str(sequence), label_color, labeled_coords)
                        labeled_coords.add(coord_str)
                        sequence += 1

                # Pause to avoid getting banned by 'dazzlepod.com'
                print("Pausing for 2 seconds...")
                time.sleep(2)

            # Draw lines between consecutive locations to represent the route
            print("Drawing route lines on the map...")
            for i in range(1, len(ips)):
                lat1, lng1 = ip_to_coordinates(ips[i - 1])
                lat2, lng2 = ip_to_coordinates(ips[i])
                if lat1 is not None and lng1 is not None and lat2 is not None and lng2 is not None:
                    gmap.plot([lat1, lat2], [lng1, lng2], color=route_color, edge_width=2)

            # Save the map as HTML
            cwd = os.getcwd()
            map_filename = "traceroute.html"
            print(f"Saving map as {map_filename}...")
            gmap.draw(map_filename)

            # Open the HTML in the default browser
            print(f"Opening map in browser...")
            webbrowser.open("file:///" + cwd + "/" + map_filename)
        except json.decoder.JSONDecodeError:
            print("Error: Unable to retrieve public IP address. JSON data not found.")
    else:
        print("Error: Unable to retrieve public IP address.")

# Get public IP address
def get_public_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        public_ip = s.getsockname()[0]
        s.close()
        return public_ip
    except Exception as e:
        print(f"Error: Unable to retrieve public IP address. {e}")
        return None

# Convert public IP to coordinates
def public_ip_to_coordinates(public_ip):
    print(f"Fetching coordinates for public IP {public_ip}...")
    url = f"http://dazzlepod.com/ip/{public_ip}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'latitude' in data and 'longitude' in data:
            latitude = data['latitude']
            longitude = data['longitude']
            print(f"Coordinates for public IP: {latitude}, {longitude}")
            return latitude, longitude
    print(f"Coordinates not found for public IP {public_ip}")
    return None, None

# Convert IP address to coordinates
def ip_to_coordinates(ip_address):
    print(f"Fetching coordinates for IP {ip_address}...")
    url = f"http://dazzlepod.com/ip/{ip_address}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'latitude' in data and 'longitude' in data:
            latitude = data['latitude']
            longitude = data['longitude']
            print(f"Coordinates for IP: {latitude}, {longitude}")
            return latitude, longitude
    print(f"Coordinates not found for IP {ip_address}")
    return None, None

# Get label color based on index
def get_label_color(index):
    colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'brown', 'cyan', 'magenta', 'lime']
    return colors[index % len(colors)]

# Main code
if __name__ == "__main__":
    # Check if a hostname is provided as a command line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py hostname")
        sys.exit(1)
    
    hostname = sys.argv[1]
    print(f"Starting traceroute for hostname: {hostname}")
    find_and_plot_coordinates(hostname)
    print("Traceroute process completed.")
