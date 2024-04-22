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
def plot_lat_long(gmap, latitude, longitude, sequence, color):
    # Check if latitude and longitude are not None
    if latitude is not None and longitude is not None:
        # Introduce a small offset to longitude and latitude to ensure uniqueness
        offset = 0.0001 * sequence
        latitude += offset
        longitude += offset
        
        # Plot the coordinates with labels indicating the sequence
        gmap.marker(latitude, longitude, label=str(sequence), color=color)

# Find and plot coordinates
def find_and_plot_coordinates(hostname):
    # Get public IP address
    public_ip = get_public_ip()
    if public_ip:
        try:
            # Convert hostname to IP address
            ip = socket.gethostbyname(hostname)

            # Perform traceroute
            res, _ = traceroute(ip, maxttl=64, verbose=0)

            # Initialize Google Maps plotter
            gmap = gmplot.GoogleMapPlotter(0, 0, 3)

            # Store retrieved IPs
            ips = []

            # Extract IP addresses from the traceroute results
            for item in res.get_trace()[ip]:
                ips.append(res.get_trace()[ip][item][0])

            # Define color for route line
            route_color = 'blue'

            # Find coordinates and plot them
            sequence = 1
            for i, ip_address in enumerate(ips):
                if i == 0:
                    latitude, longitude = public_ip_to_coordinates(public_ip)
                    plot_lat_long(gmap, latitude, longitude, "Public IP", route_color)
                else:
                    latitude, longitude = ip_to_coordinates(ip_address)
                    if latitude is not None and longitude is not None:
                        label_color = get_label_color(i)
                        plot_lat_long(gmap, latitude, longitude, str(sequence), label_color)
                        sequence += 1

                # Pause to avoid getting banned by 'dazzlepod.com'
                time.sleep(2)

            # Draw lines between consecutive locations to represent the route
            for i in range(1, len(ips)):
                lat1, lng1 = ip_to_coordinates(ips[i - 1])
                lat2, lng2 = ip_to_coordinates(ips[i])
                if lat1 is not None and lng1 is not None and lat2 is not None and lng2 is not None:
                    gmap.plot([lat1, lat2], [lng1, lng2], color=route_color, edge_width=2)

            # Save the map as HTML
            cwd = os.getcwd()
            gmap.draw("traceroute.html")

            # Open the HTML in the default browser
            webbrowser.open("file:///" + cwd + "/traceroute.html")
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
    url = f"http://dazzlepod.com/ip/{public_ip}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'latitude' in data and 'longitude' in data:
            latitude = data['latitude']
            longitude = data['longitude']
            return latitude, longitude
        else:
            print("Latitude or longitude not found in JSON response.")
    else:
        print("Error: Unable to retrieve JSON data from dazzlepod.com")
    return None, None

# Convert IP address to coordinates
def ip_to_coordinates(ip_address):
    url = f"http://dazzlepod.com/ip/{ip_address}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'latitude' in data and 'longitude' in data:
            latitude = data['latitude']
            longitude = data['longitude']
            return latitude, longitude
        else:
            print("Latitude or longitude not found in JSON response.")
    else:
        print("Error: Unable to retrieve JSON data from dazzlepod.com")
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
    find_and_plot_coordinates(hostname)
