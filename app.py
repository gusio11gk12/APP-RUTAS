from flask import Flask, request, jsonify, render_template
import heapq
import math

app = Flask(__name__)

# Define las coordenadas de las ciudades (una por cada estado de México)
coord = {
    'Aguascalientes': [21.87641043660486, -102.26438663286967],
    'BajaCalifornia': [31.8679699,-116.6263433],
    'BajaCaliforniaSur': [24.14437, -110.3005],
    'Campeche': [19.8301, -90.53491],
    'Chiapas': [16.75, -93.1167],
    'Chihuahua': [28.6353, -106.0889],
    'CDMX': [19.432713075976878, -99.13318344772986],
    'Coahuila': [25.4260, -101.0053],
    'Colima': [19.2452, -103.725],
    'Durango': [24.0277, -104.6532],
    'Guanajuato': [21.0190, -101.2574],
    'Guerrero': [17.5506, -99.5024],
    'Hidalgo': [20.1011, -98.7624],
    'Jalisco': [20.6767, -103.3475],
    'Mexico': [19.327661,-99.541816],
    'Michoacan': [19.701400113725654, -101.20829680213464],
    'Morelos': [18.6813, -99.1013],
    'Nayarit': [21.5085, -104.895],
    'NuevoLeon': [25.6714, -100.309],
    'Oaxaca': [17.0732, -96.7266],
    'Puebla': [19.0414, -98.2063],
    'Queretaro': [20.5930,-100.391],
    'QuintanaRoo': [21.1631, -86.8023],
    'SanLuisPotosi': [22.1565, -100.9855],
    'Sinaloa': [24.8091, -107.394],
    'Sonora': [29.0729, -110.9559],
    'Tabasco': [17.9892, -92.9475],
    'Tamaulipas': [25.4348, -99.134],
    'Tlaxcala': [19.3181, -98.2375],
    'Veracruz': [19.1738, -96.1342],
    'Yucatan': [20.967, -89.6237],
    'Zacatecas': [22.7709, -102.5833]
}

# Define la función de distancia Haversine
def haversine(coord1, coord2):
    R = 6371.0 # Radio de la Tierra en kilómetros
    lat1 = math.radians(coord1[0])
    lon1 = math.radians(coord1[1])
    lat2 = math.radians(coord2[0])
    lon2 = math.radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

# Implementación del algoritmo de Dijkstra
def dijkstra(start, end, coord):
    dist = {node: float('inf') for node in coord}
    dist[start] = 0
    prev = {node: None for node in coord}
    pq = [(0, start)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        if current_dist > dist[current_node]:
            continue

        for neighbor in coord:
            if neighbor != current_node:
                distance = haversine(coord[current_node], coord[neighbor])
                new_dist = current_dist + distance

                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = current_node
                    heapq.heappush(pq, (new_dist, neighbor))

    path = []
    node = end
    while prev[node] is not None:
        path.insert(0, node)
        node = prev[node]
    if path:
        path.insert(0, node)
    return path, dist[end]

@app.route('/')
def index():
    ciudades = list(coord.keys())
    return render_template('index.html', ciudades=ciudades)

@app.route('/get_routes', methods=['POST'])
def obtener_ruta():
    data = request.json
    ciudad_inicio = data['start']
    ciudad_final = data['end']
    if ciudad_inicio not in coord or ciudad_final not in coord:
        return jsonify({'error': 'Ciudad no encontrada'}), 404

    # Ejecuta el algoritmo de Dijkstra
    mejor_ruta, distancia_total = dijkstra(ciudad_inicio, ciudad_final, coord)

    # Obtener coordenadas de las ciudades a lo largo de la ruta
    coordenadas_ruta = [coord[ciudad] for ciudad in mejor_ruta]

    return jsonify({
        'mejor_ruta': mejor_ruta,
        'distancia_total': distancia_total,
        'coordenadas_ruta': coordenadas_ruta
    })

if __name__ == '__main__':
    app.run(debug=True)
