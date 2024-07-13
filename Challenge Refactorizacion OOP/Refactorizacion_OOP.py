import heapq
import random

class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[0] * columnas for _ in range(filas)]

    def generar_mapa(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                self.matriz[i][j] = random.randint(0, 3)

    def agregar_obstaculo(self, fila, columna):
        if self.es_celda_valida(fila, columna):
            self.matriz[fila][columna] = -1
            return True
        return False

    def eliminar_obstaculo(self, fila, columna):
        if self.es_celda_valida(fila, columna):
            self.matriz[fila][columna] = 0
            return True
        return False

    def visualizar_mapa(self, ruta=None, punto_inicio=None, punto_objetivo=None):
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if punto_inicio and (fila, columna) == punto_inicio:
                    print("I", end=" ")
                elif punto_objetivo and (fila, columna) == punto_objetivo:
                    print("O", end=" ")
                elif ruta and (fila, columna) in ruta:
                    print("*", end=" ")
                elif self.matriz[fila][columna] == -1:
                    print("X", end=" ")
                else:
                    print(".", end=" ")
            print()

    def es_celda_valida(self, fila, columna):
        return 0 <= fila < self.filas and 0 <= columna < self.columnas

    def es_celda_accesible(self, fila, columna):
        return self.es_celda_valida(fila, columna) and self.matriz[fila][columna] != -1

class CalculadoraRuta:
    def __init__(self, mapa):
        self.mapa = mapa

    @staticmethod
    def calcular_costo_h(nodo_actual, nodo_objetivo):
        return abs(nodo_actual[0] - nodo_objetivo[0]) + abs(nodo_actual[1] - nodo_objetivo[1])

    @staticmethod
    def calcular_costo(nodo_actual, nodo_vecino):
        return 1  # Costo uniforme para movimientos simples

    def buscar_ruta(self, inicio, objetivo):
        nodos_abiertos = []
        nodos_cerrados = set()
        heapq.heappush(nodos_abiertos, (0, inicio, []))

        while nodos_abiertos:
            costo_actual, nodo_actual, camino = heapq.heappop(nodos_abiertos)

            if nodo_actual == objetivo:
                return camino + [nodo_actual]

            if nodo_actual in nodos_cerrados:
                continue

            nodos_cerrados.add(nodo_actual)

            for vecino in self.obtener_vecinos(nodo_actual):
                if vecino in nodos_cerrados:
                    continue

                nuevo_costo = costo_actual + self.calcular_costo(nodo_actual, vecino)
                costo_h = self.calcular_costo_h(vecino, objetivo)
                costo_total = nuevo_costo + costo_h

                heapq.heappush(nodos_abiertos, (costo_total, vecino, camino + [nodo_actual]))

        return None  # No se encontró ruta

    def obtener_vecinos(self, nodo):
        fila, columna = nodo
        vecinos = []
        for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nueva_fila, nueva_columna = fila + df, columna + dc
            if self.mapa.es_celda_accesible(nueva_fila, nueva_columna):
                vecinos.append((nueva_fila, nueva_columna))
        return vecinos

def pedir_coordenadas(mapa, mensaje):
    while True:
        try:
            fila = int(input(f"{mensaje} - Fila: "))
            columna = int(input(f"{mensaje} - Columna: "))
            if mapa.es_celda_valida(fila, columna):
                return fila, columna
            print("Coordenadas fuera de los límites del mapa. Intente de nuevo.")
        except ValueError:
            print("Por favor, ingrese números enteros válidos.")

def main():
    mapa = Mapa(7, 7)
    mapa.generar_mapa()

    calculadora = CalculadoraRuta(mapa)

    punto_inicio = pedir_coordenadas(mapa, "Ingrese el punto de inicio")
    punto_objetivo = pedir_coordenadas(mapa, "Ingrese el punto objetivo")

    while True:

        print("\nMapa actual:")
        mapa.visualizar_mapa(punto_inicio=punto_inicio, punto_objetivo=punto_objetivo)

        opcion = input("¿Desea agregar un obstáculo? (s/n): ").lower()
        if opcion != 's':
            eliminar = input('Desea eliminar un obstaculo?').lower()
            if eliminar == 's':
                eliminar_fila = input('Ingrese la fila del obstaculo; ')
                eliminar_columna = input('Ingrese la columna del obstaculo; ')
                mapa.eliminar_obstaculo(eliminar_fila, eliminar_columna)
            else:
                break
        else:
            fila, columna = pedir_coordenadas(mapa, "Ingrese la posición del obstáculo")
            mapa.agregar_obstaculo(fila, columna)
            print("\nMapa generado con obstáculos:")
            mapa.visualizar_mapa(punto_inicio=punto_inicio, punto_objetivo=punto_objetivo)

    print("\nMapa generado con obstáculos:")
    mapa.visualizar_mapa(punto_inicio=punto_inicio, punto_objetivo=punto_objetivo)

    ruta = calculadora.buscar_ruta(punto_inicio, punto_objetivo)

    if ruta:
        print("\nMapa con la ruta encontrada:")
        mapa.visualizar_mapa(ruta, punto_inicio, punto_objetivo)
    else:
        print("\nNo se pudo encontrar una ruta válida.")

if __name__ == "__main__":
    main()
