import folium
import webbrowser

def generate_map():
    m = folium.Map(location=[0, 25], zoom_start=5)

    folium.Marker([0, 25], tooltip="IoT Node 1").add_to(m)
    folium.Marker([-2, 23], tooltip="IoT Node 2").add_to(m)

    m.save("map.html")
    webbrowser.open("map.html")