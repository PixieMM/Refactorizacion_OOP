import heapq  # Importar para usar la cola de prioridad
import random

class Nodo:  # Representa un nodo en un grafo utilizado para encontrar rutas.
    def __init__(self, fila, columna, costo_g=0, costo_h=0, padre=None):
        self.fila = fila
        self.columna = columna
        self.costo_g = costo_g  # Costo acumulado desde el costo inicial hasta este nodo
        self.costo_h = costo_h  # Costo heurístico desde este nodo hasta el nodo objetivo
        self.padre = padre  # Referencia al nodo padre para reconstruir la ruta

    def costo_total(self):  # Calcula y devuelve la suma de los costos
        return self.costo_g + self.costo_h
    
    def __lt__(self, otro):  # (Menor que) Define como comparar nodos basados en su costo total. Necesario para utilizar objetos 'Nodo' en estrustura de datos como colas de prioridad.
        return self.costo_total() < otro.costo_total()

class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[0] * columnas for _ in range(filas)]
        self.nodos_abiertos = []
        self.nodos_cerrados = []

    def generar_mapa(self):  # Llena la matriz del mapa con valores aleatorios del 0 al 3, que representan diferentes tipos de terreno.
        for i in range(self.filas):
            for j in range(self.columnas):
                self.matriz[i][j] = random.randint(0, 3)  # Valores del 0 al 3 para tipos de terreno
    
    def agregar_obstaculo(self, fila, columna):  # Permite agregar obstáculo en una posición específica del mapa.
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            self.matriz[fila][columna] = -1
            return True
        else:
            print(f"Coordenadas ({fila}, {columna}) fuera de los límites del mapa.")
            return False
        
    def es_obstaculo(self, fila, columna):  # Verifica si una posición específica del mapa es un obstáculo
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            return self.matriz[fila][columna] == -1
        else:
            return False

    def calcular_costo_h(self, nodo_actual, nodo_objetivo):  # Calcular el costo heurístico.
        return abs(nodo_actual.fila - nodo_objetivo.fila) + abs(nodo_actual.columna - nodo_objetivo.columna)
    
    def buscar_ruta(self, fila_inicio, columna_inicio, fila_objetivo, columna_objetivo):  # Implementa el algoritmo A* para encontrar el camino más corto de inicio a objetivo.
        nodo_inicio = Nodo(fila_inicio, columna_inicio)  # Crea nodos de inicio
        nodo_objetivo = Nodo(fila_objetivo, columna_objetivo)  # y objetivo

        heapq.heappush(self.nodos_abiertos, nodo_inicio)  # Usado para agregar el nodo de inicio a la cola prioridad 'nodos_abiertos'.
        nodos_visitados = set()  # Mantiene un conjunto de 'nodos_visitados' para evitar revisar nodos más de una vez.
        while self.nodos_abiertos:  # En el bucle 'while', extrae y evalúa el nodo con el costo total más bajo
            nodo_actual = heapq.heappop(self.nodos_abiertos)
            nodos_visitados.add((nodo_actual.fila, nodo_actual.columna))

            if nodo_actual.fila == nodo_objetivo.fila and nodo_actual.columna == nodo_objetivo.columna:
                # *Reconstruir y devolver la ruta encontrada
                return self.reconstruir_ruta(nodo_actual)  # Si encuentra el nodo objetivo, llama a 'reconstruir_ruta' para obtener y devolver la ruta encontrada.
            
            vecinos = self.obtener_vecinos(nodo_actual)  # Obtener los vecinos válidos del 'nodo_actual' usando 'obtener_vecinos'
            for vecino in vecinos:
                if (vecino.fila, vecino.columna) in nodos_visitados:
                    continue
                
                nuevo_costo_g = nodo_actual.costo_g + 1  # Costo uniforme (distancia de paso 1)
                
                if (vecino.fila, vecino.columna) not in [(n.fila, n.columna) for n in self.nodos_abiertos] or nuevo_costo_g < vecino.costo_g:
                    vecino.costo_g = nuevo_costo_g
                    vecino.costo_h = self.calcular_costo_h(vecino, nodo_objetivo)
                    vecino.padre = nodo_actual
                    
                    heapq.heappush(self.nodos_abiertos, vecino)

        # Si no se encontró ruta válida, devuelve None
        return None

    def obtener_vecinos(self, nodo):  # Retorna una lista de vecinos válidos (nodos adyacentes) al nodo dado 'nodo'
        vecinos = []
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Movimientos arriba, abajo, izquierda, derecha

        for mov in movimientos:
            fila_vecino = nodo.fila + mov[0]
            columna_vecino = nodo.columna + mov[1]

            if 0 <= fila_vecino < self.filas and 0 <= columna_vecino < self.columnas and not self.es_obstaculo(fila_vecino, columna_vecino):
                vecino = Nodo(fila_vecino, columna_vecino)
                vecinos.append(vecino)
        return vecinos
    
    def reconstruir_ruta(self, nodo_actual):  # Reconstruye y devuelve la ruta desde el nodo inicial hasta el nodo objetivo
        ruta = []
        while nodo_actual is not None:
            ruta.append((nodo_actual.fila, nodo_actual.columna))
            nodo_actual = nodo_actual.padre
        ruta.reverse()
        return ruta 

    def visualizar_mapa(self, ruta=None, punto_inicio=None, punto_objetivo=None):  # Imprime el mapa en la consola, marcando opcionalmente la ruta, el punto inicio y el punto objetivo con caracteres especiales.
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if punto_inicio and fila == punto_inicio[0] and columna == punto_inicio[1]:
                    print("I", end=" ")  # Marcar punto de inicio con I
                if punto_objetivo and fila == punto_objetivo[0] and columna == punto_objetivo[1]:
                    print("O", end=" ")  # Marcar punto objetivo con O
                if ruta and (fila, columna) in ruta:
                    print("*", end=" ")  # Marcar camino con *
                elif self.matriz[fila][columna] == -1: 
                    print("X", end=" ")  # Marcar los obstáculos
                else:
                    print(".", end=" ")  # Marcar las celdas vacías
            print()

# Función para pedir al usuario que ingrese las coordenadas de los obstáculos
def pedir_obstaculos(mapa):
    while True:
        try:
            fila_inicio = int(input("Ingrese la fila del punto de inicio: "))
            columna_inicio = int(input("Ingrese la columna del punto de inicio: "))
            fila_objetivo = int(input("Ingrese la fila del punto objetivo: "))
            columna_objetivo = int(input("Ingrese la columna del punto objetivo: "))
            if (0 <= fila_inicio < mapa.filas and 0 <= columna_inicio < mapa.columnas and
                    0 <= fila_objetivo < mapa.filas and 0 <= columna_objetivo < mapa.columnas):
                break
            else:
                print("Coordenadas fuera de los límites del mapa. Inténtalo de nuevo.")
        except ValueError:
            print("Por favor, ingrese números enteros válidos para las coordenadas.")

    punto_inicio = (fila_inicio, columna_inicio)
    punto_objetivo = (fila_objetivo, columna_objetivo)

    while True:
        fila_obstaculo = int(input("Ingrese la fila del obstáculo (-1 para salir):"))
        if fila_obstaculo == -1:
            break
        columna_obstaculo = int(input("Ingresa la columna del obstáculo: "))
        if not mapa.agregar_obstaculo(fila_obstaculo, columna_obstaculo):
            print("Coordenadas inválidas. Inténtalo de nuevo.")

    return punto_inicio, punto_objetivo

mapa = Mapa(7, 7)  # 2. Se instancia el objeto 'Mapa' con sus dimensiones.

# Generar valores aleatorios para cada celda del mapa
mapa.generar_mapa()

# Pedir al usuario que ingrese los obstáculos
print("Ingrese las coordenadas de los obstáculos (fuera de los límites para salir):")
punto_inicio, punto_objetivo = pedir_obstaculos(mapa)

# Visualizar el mapa en la terminal antes de buscar la ruta
print("\nMapa generado con obstáculos:")
mapa.visualizar_mapa()

# 8. Actualizar mapa con los nuevos puntos de inicio y objetivo
ruta = mapa.buscar_ruta(punto_inicio[0], punto_inicio[1], punto_objetivo[0], punto_objetivo[1])

# 9. Mostrar el mapa con la ruta resaltada
print("\nMapa con la ruta encontrada:")
mapa.visualizar_mapa(ruta, punto_inicio, punto_objetivo)
