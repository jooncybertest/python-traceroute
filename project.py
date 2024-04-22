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
def plot_lat_long(latitude, longitude, sequence):
    # Initialize Google Maps plotter
    gmap = gmplot.GoogleMapPlotter(latitude, longitude, 3)
    
    # Handle path issue for Windows
    if ":\\" in gmap.coloricon:
        gmap.coloricon = gmap.coloricon.replace('/', '\\')
        gmap.coloricon = gmap.coloricon.replace('\\', '\\\\')
    
    # Plot the coordinates with labels indicating the sequence
    gmap.marker(latitude, longitude, sequence, color='cornflowerblue')
    
    # Save the map as HTML
    cwd = os.getcwd()
    gmap.draw("traceroute.html")
    
    # Open the HTML in the default browser
    webbrowser.open("file:///" + cwd + "/traceroute.html")

# Find and plot coordinates
def find_and_plot_coordinates(hostname):
    # Get public IP address
    response = requests.get("https://dazzlepod.com/ip/me")
    if response.status_code == 200:
        try:
            public_ip = response.json()['ip']
            # Convert hostname to IP address
            ip = socket.gethostbyname(hostname)

            # Perform traceroute
            res, _ = traceroute(ip, maxttl=64, verbose=0)

            # Store retrieved IPs
            ips = []

            # Extract IP addresses from the traceroute results
            for item in res.get_trace()[ip]:
                ips.append(res.get_trace()[ip][item][0])

            # Find coordinates and plot them
            for i, ip_address in enumerate(ips):
                if i == 0:
                    latitude, longitude = public_ip_to_coordinates(public_ip)
                    plot_lat_long(latitude, longitude, "Public IP")
                else:
                    latitude, longitude = ip_to_coordinates(ip_address)
                    plot_lat_long(latitude, longitude, f"Hop {i}")

                # Pause to avoid getting banned by 'dazzlepod.com'
                time.sleep(2)
        except json.decoder.JSONDecodeError:
            print("Error: Unable to retrieve public IP address. JSON data not found.")
    else:
        print("Error: Unable to retrieve public IP address.")

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

# Main code
if __name__ == "__main__":
    # Check if a hostname is provided as a command line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py hostname")
        sys.exit(1)
    
    hostname = sys.argv[1]
    find_and_plot_coordinates(hostname)
