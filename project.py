import json
import requests
import webbrowser
import os
import time
import socket
from scapy.layers.inet import traceroute
from gmplot import gmplot
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Plot coordinates onto Google Maps
def plot_lat_long(gmap, latitude, longitude, sequence, color, labeled_coords):
    if latitude is not None and longitude is not None:
        sequence = int(sequence)
        offset = 0.0001 * sequence
        latitude += offset
        longitude += offset
        coord_str = f"{latitude},{longitude}"
        if coord_str not in labeled_coords:
            gmap.marker(latitude, longitude, label=str(sequence), color=color)
            labeled_coords.add(coord_str)

# Convert IP address to coordinates
def ip_to_coordinates(ip_address):
    url = f"http://dazzlepod.com/ip/{ip_address}.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            if latitude is not None and longitude is not None:
                return latitude, longitude
            else:
                logging.warning("Latitude or longitude not found in JSON response.")
        else:
            logging.error("Error: Unable to retrieve JSON data from dazzlepod.com")
    except Exception as e:
        logging.error(f"Error occurred while fetching coordinates for {ip_address}: {e}")
    return None, None

# Find and plot coordinates
def find_and_plot_coordinates(hostname):
    public_ip = get_public_ip()
    if public_ip:
        try:
            ip = socket.gethostbyname(hostname)
            res, _ = traceroute(ip, maxttl=64, verbose=0)
            gmap = gmplot.GoogleMapPlotter(0, 0, 3)
            ips = [res.get_trace()[ip][item][0] for item in res.get_trace()[ip]]
            route_color = 'blue'
            labeled_coords = set()  # Set to store labeled coordinates
            sequence = 1
            for i, ip_address in enumerate(ips):
                if i == 0:
                    latitude, longitude = public_ip_to_coordinates(public_ip)
                    plot_lat_long(gmap, latitude, longitude, "Public IP", route_color, labeled_coords)
                else:
                    latitude, longitude = ip_to_coordinates(ip_address)
                    if latitude is not None and longitude is not None:
                        label_color = get_label_color(i)
                        plot_lat_long(gmap, latitude, longitude, str(sequence), label_color, labeled_coords)
                        sequence += 1
                time.sleep(2)
            for i in range(1, len(ips)):
                lat1, lng1 = ip_to_coordinates(ips[i - 1])
                lat2, lng2 = ip_to_coordinates(ips[i])
                if lat1 is not None and lng1 is not None and lat2 is not None and lng2 is not None:
                    gmap.plot([lat1, lat2], [lng1, lng2], color=route_color, edge_width=2)
            cwd = os.getcwd()
            gmap.draw("traceroute.html")
            webbrowser.open("file:///" + cwd + "/traceroute.html")
        except Exception as e:
            logging.error(f"Error occurred during traceroute: {e}")
    else:
        logging.error("Error: Unable to retrieve public IP address.")

# Get public IP address
def get_public_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        public_ip = s.getsockname()[0]
        s.close()
        return public_ip
    except Exception as e:
        logging.error(f"Error: Unable to retrieve public IP address. {e}")
        return None

# Get label color based on index
def get_label_color(index):
    colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'brown', 'cyan', 'magenta', 'lime']
    return colors[index % len(colors)]

# Main code
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py hostname")
        sys.exit(1)
    hostname = sys.argv[1]
    find_and_plot_coordinates(hostname)
