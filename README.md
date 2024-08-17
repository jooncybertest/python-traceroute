# Traceroute Visualization Tool

This project visualizes the path of network packets across the internet by performing a traceroute and plotting the geographic locations of each hop onto Google Maps. It provides an interactive and informative way to understand the journey of data from your device to a specified hostname.

## 🚀 Features
-**Interactive Network Visualization:** Plots the geographic coordinates of each hop in a traceroute on a Google Map, allowing users to visually track the path of their data across the internet. <br>
-**Real-Time IP Geolocation:** Converts IP addresses to geographical coordinates using the Dazzlepod API, ensuring accurate and up-to-date location data for each hop. <br>
-**Customizable and Extensible:** Includes customizable marker labels and route colors, with error handling and rate-limiting to ensure reliable operation. <br>

## 🛠️ Tech Stack-
**Python:** Core language used for network operations and data handling. <br>
-**Scapy:** Used for performing traceroute operations. <br>
-**GMPlot:** Python library for plotting data on Google Maps. <br>
-**Dazzlepod API:** Provides geolocation data for IP addresses. <br>
-**Web Technologies:** Webbrowser module for rendering HTML maps. <br>

## 📦 Installation### Prerequisites

Ensure you have the following installed:

- Python 3.x
- pip (Python package manager)

### Installation 
Steps1.**Clone the repository:**    
    ```bash
    git clone https://github.com/your-username/traceroute-visualization-tool.git
    cd traceroute-visualization-tool
    ```
2.**Install the required Python packages:**    
    ```bash
    pip install -r requirements.txt
    ```
3.**Run the script:**    
    ```bash
    python script.py [hostname]
    ```
    Replace `[hostname]` with the domain or IP address you want to trace.
    
## 🎯 Usage1.**Perform a traceroute:**   
  - Run the script with the desired hostname or IP address. <br>
   - The script will perform a traceroute, convert the resulting IPs to geographic coordinates, and plot them on a Google Map. <br>

2.**View the results:**   - Once the traceroute is complete, an HTML file (`traceroute.html`) will be generated and automatically opened in your default web browser, showing the path of the packets.

## 📁 Project Structure
```bash
src/
├── script.py                # Main script to run the traceroute and plot the map
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
