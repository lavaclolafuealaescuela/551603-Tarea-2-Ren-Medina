#TAREA 2
import math

# PARTE 1 ENUNCIADO

# Clase base que representa un explosivo
class Explosive:
    """
    Clase que representa un explosivo con sus propiedades y métodos asociados.

    Atributos:
        name (str): nombre comercial.
        density (float): densidad (g/cm³).
        vod (float): velocidad de detonación (m/s).
        rws (float): potencia relativa a ANFO en peso  (%).
        water_resistance (bool): resistencia al agua.
    """

    def __init__(self, name, density, vod, rws, water_resistance):
        self.name = name
        self.density = density
        self.vod = vod
        self.rws = rws
        self.water_resistance = water_resistance

    def detonation_pressure(self):
        """
        Calcula la presión de detonación en kPa usando la ecuacion 2:
        PD = 1/4 * ρe * VOD²
        """ 
        return 0.25 * self.density * (self.vod ** 2)

    def linear_density(self, diameter_mm):
        """
        Calcula la densidad lineal (kg/m) para un diámetro de barreno dado en mm.
        """
        diameter_m = diameter_mm / 1000  # Se convierte a metros
        return (math.pi / 4) * (diameter_m ** 2) * (self.density * 1000)  # ρe de g/cm³ a kg/m³

    def anfo_equivalent(self, weight_kg):
        """
        Calcula cuántos kg de ANFO equivalen a un peso dado de este explosivo.
        """
        return (weight_kg * self.rws) / 100

    def print_water_resistance(self):
        """
        Informa si el explosivo es resistente o no al agua.
        """
        print(f"{self.name} is {'water resistant' if self.water_resistance else 'not water resistant'}.")


# PARTE 2 ENUNCIADO

# Clase que representa una tronadura de banco, heredando de Explosive
class BenchBlasting(Explosive):
    """
    Clase para calcular parámetros de una tronadura de banco.

    Atributos nuevos:
        hole_diameter (mm): diámetro de barreno.
        burden (m): burden entre filas.
        spacing (m): espaciamiento entre pozos.
        hole_depth (m): profundidad total del pozo.
        bench_height (m): altura del banco.
        subdrilling (m): pasadura.
        standoff (m): taco en collar.
    """

    def __init__(self, name, density, vod, rws, water_resistance,
                 hole_diameter, burden, spacing, hole_depth, bench_height, subdrilling, standoff):
        super().__init__(name, density, vod, rws, water_resistance)
        self.hole_diameter = hole_diameter
        self.burden = burden
        self.spacing = spacing
        self.hole_depth = hole_depth
        self.bench_height = bench_height
        self.subdrilling = subdrilling
        self.standoff = standoff

    def blasted_volume(self):
        """
        Calcula el volumen tronado por cada pozo (m³)
        V = burden * spacing * altura
        """
        return self.burden * self.spacing * self.bench_height

    def specific_consumption(self):
        """
        Calcula el consumo específico de explosivo (kg/m³)
        """
        charge_per_hole = self.linear_density(self.hole_diameter) * (self.hole_depth - self.standoff)
        return charge_per_hole / self.blasted_volume()

    def blasting_cost(self, explosive_price_per_kg, drilling_price_per_m):
        """
        Calcula el costo total de la tronadura por m³ considerando explosivo y perforación.

        Parámetros:
            explosive_price_per_kg (float): precio del explosivo ($/kg).
            drilling_price_per_m (float): costo de perforación ($/m).

        Retorna:
            float: costo total por m³.
        """
        charge_per_hole = self.linear_density(self.hole_diameter) * (self.hole_depth - self.standoff)
        total_explosive_cost = charge_per_hole * explosive_price_per_kg
        total_drilling_cost = self.hole_depth * drilling_price_per_m
        total_cost_per_hole = total_explosive_cost + total_drilling_cost

        return total_cost_per_hole / self.blasted_volume()



# PRUEBAS DE DE USO

# PARTE 1 

# Se definen dos explosivos con parámetros obtenidos de un manual de ENAEX (link: https://es.scribd.com/document/349912937/Manual-Enaex3 , página 42)

exp1 = Explosive("ANFO", 0.78, 4000, 100, False)
exp2 = Explosive("Blendex 930", 1, 3920, 93, False)

# a) Presión de detonación de cada uno
print(f"{exp1.name} PD: {exp1.detonation_pressure():.2f} kPa")  
print(f"{exp2.name} PD: {exp2.detonation_pressure():.2f} kPa")

# b) Densidad lineal para diámetro de 140 mm
print(f"{exp1.name} Linear Density: {exp1.linear_density(140):.2f} kg/m")
print(f"{exp2.name} Linear Density: {exp2.linear_density(140):.2f} kg/m")

# c) Equivalente en ANFO para 500 kg de cada explosivo
print(f"{exp1.name} equivalent in ANFO: {exp1.anfo_equivalent(500):.2f} kg")
print(f"{exp2.name} equivalent in ANFO: {exp2.anfo_equivalent(500):.2f} kg")

# d) Imprimir resistencia al agua
exp1.print_water_resistance()
exp2.print_water_resistance()

# PARTE 2

blasting = BenchBlasting("ANFO", 1.25, 6000, 80, True,
                         140, 3, 4, 10, 8, 0.5, 1)

# a) Factor de carga (consumo específico)
print(f"Blasting with {blasting.name}: Specific consumption = {blasting.specific_consumption():.2f} kg/m³")

# b) Equivalente en ANFO
anfo_consumption = (blasting.specific_consumption() * 100) / blasting.rws
print(f"ANFO equivalent consumption: {anfo_consumption:.2f} kg/m³")

# c) Costo de tronadura por m3, asumiendo precios
explosive_price_per_kg = 0.95   # $/kg
drilling_price_per_m = 15     # $/m

cost_per_m3 = blasting.blasting_cost(explosive_price_per_kg, drilling_price_per_m)
print(f"Blasting cost: ${cost_per_m3:.2f} per m³")
