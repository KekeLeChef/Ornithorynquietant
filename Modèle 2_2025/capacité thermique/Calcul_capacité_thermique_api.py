import ee

# Initialiser Earth Engine
ee.Authenticate()
ee.Initialize(project='healthy-dragon-462713-p4')


nb_pixel=1468125
# Dictionnaire des propriétés thermiques par type de sol (ESA WorldCover 2020) (capacité thermique massqiue en J/kh/K)
SOIL_PROPERTIES = {
    10: {"name": "Tree cover",      "cp": 1900, "rho": 1000},
    20: {"name": "Shrubland",       "cp": 1600, "rho": 1100},
    30: {"name": "Grassland",       "cp": 1800, "rho": 1100},
    40: {"name": "Cropland",        "cp": 1500, "rho": 1300},
    50: {"name": "Built-up",        "cp": 840,  "rho": 2200},
    60: {"name": "Bare / sparse",   "cp": 800,  "rho": 1800},
    70: {"name": "Snow / ice",      "cp": 2100, "rho": 917},
    80: {"name": "Water",           "cp": 4186, "rho": 1000},
    90: {"name": "Wetlands",        "cp": 4200, "rho": 1000},
    95: {"name": "Mangroves",       "cp": 3500, "rho": 1000},
    100: {"name": "Moss / lichen",  "cp": 1500, "rho": 1200},
    0: {"name": "Water",           "cp": 4186, "rho": 1000},
}

def get_landcover_histogram(lat, lon):
    point = ee.Geometry.Point(lon, lat)
    region = point.buffer(5000).bounds()  # carré de 10 km

    # Jeu de données ESA WorldCover 2020
    dataset = ee.Image("ESA/WorldCover/v100/2020")
    landcover = dataset.select("Map")

    stats = landcover.reduceRegion(
        reducer=ee.Reducer.frequencyHistogram(),
        geometry=region,
        scale=10,  # Résolution 10m
        maxPixels=1e9
    )

    histogram = stats.get('Map').getInfo()
    return histogram

def compute_thermal_capacity(histogram):
    var=0
    som=0
    pixel_area = 10 * 10  # m² pour 10m x 10m pixels
    thickness = 0.05  # 5 cm en mètres
    total_capacity = 0

    print("\n--- Détails par type de sol ---")
    for items in histogram.items():
        som+=items[1]
        if items[0] == "80":
            var=1
    print(som)
    if som != nb_pixel and var==1:
        histogram['80']=histogram['80']+ (nb_pixel - som)
    else:
        histogram['80']= nb_pixel - som

    for class_id, count in histogram.items():
        class_id = int(class_id)
        if class_id in SOIL_PROPERTIES:
            prop = SOIL_PROPERTIES[class_id]
            volume = pixel_area * thickness * count  # m³
            capacity = volume * prop['rho'] * prop['cp']  # J/K
            total_capacity += capacity
            print(f"{prop['name']:17} | {int(count):5d} pixels | {capacity:.2e} J/K")

    print("\n✅ Capacité thermique totale : {:.2e} J/K".format(total_capacity))
    return total_capacity

# Exemple : Nemo
latitude = 47.2388
longitude = 0

print(f"🌍 Calcul de la capacité thermique autour de ({latitude}, {longitude})...")
histogram = get_landcover_histogram(latitude, longitude)
capacity = compute_thermal_capacity(histogram)
