# this will allow this program to interpret JSON object. See example JSON:http://dazzlepod.com/ip/128.173.239.242.json
import json

# the tools needed to access a URL and get data.
import requests

# allows operations such opening a default browser at a given URL
import webbrowser, os

# for pausing our requests to a web service that takes IP and returns latitude,longitude
import time

# scapy is an extensive networking library for python. We are going to be using its 'traceroute()'
from scapy.layers.inet import socket
from scapy.layers.inet import traceroute

# this is to plot our lat/long data onto Google Maps  https://pypi.org/project/gmplot/
from gmplot import gmplot   

# adding for arguments
import sys 



# plots 3 coordinates onto Google Maps - hardcoded for in-class example
def plot_lat_long():
   
    # the initial lat long and the zoom levels for the map (3 is zoomed out)
    gmap = gmplot.GoogleMapPlotter(42.0167, 23.1000, 3)
    
    #Handle path issue for windows, so that marker images can optionally be found using gmplot
    if ":\\" in gmap.coloricon:
        gmap.coloricon = gmap.coloricon.replace('/', '\\')
        gmap.coloricon = gmap.coloricon.replace('\\', '\\\\')
        
    
    # placing large dots on the lat longs
    # for your homework you will pass in coordinates retrieved from dazzlepod. 
    # for this in-class example, we will plot a hard-coded list of coordinates
    lats = [42.0167, 40.0967, 44.0567]
    longs = [23.1000, 22.6000, 25.8000 ]
    gmap.scatter( lats, longs, '#FF00FF', 
                              size = 40000, marker = False) 

        

    # get the currentdirectory
    cwd = os.getcwd()
    
    # saving the map as an HTML into the project directory
    gmap.draw("traceroute.html")
    
    # opening the HTML via default browser
    webbrowser.open("file:///" + cwd +"/traceroute.html")


# find the latitude and longitude 
def find_and_plot_coordinates():
    
    # tool for finding latitutde and longitude of ip address
    url = "http://dazzlepod.com/ip/{}.json".format(ips[3])
    
    # debugging the URLs
    print(url)
    response = requests.get(url)
    data = response.json()
    # making sure the wesbsite gave us lat and long
    if 'latitude' in data and 'longitude' in data:
        print(data['latitude'],data['longitude'])
                         
    # pausing for 2 seconds to make sure we don't get banned by 'dazzlepod.com'
    time.sleep(SLEEP_SECONDS)
            
    #calls function to plot the lats and longs
    plot_lat_long()





#will need to slow down the request frequency from 'dazzlepod.com' to find latitude and longitude
SLEEP_SECONDS = 2
#hostname to traceroute to, hardcoded for in-class example
hostname = 'www.aubg.bg'


# converting request hostname into IP address
ip = socket.gethostbyname(hostname)

# a good explanation of how traceroute works: https://www.youtube.com/watch?v=G05y9UKT69s
# add maxttl=100 or more if you want to traceroute even deeper.
#'res' -- results from traceroute 
res, _ = traceroute(ip,maxttl=64,verbose = 0)

# will store retrieved IPs here.
ips = []

# going through the traceroute results and extracting IP addresses into the array
for item in res.get_trace()[ip]:
    ips.append(res.get_trace()[ip][item][0])
    
#find coordinates and plot them   
find_and_plot_coordinates()


