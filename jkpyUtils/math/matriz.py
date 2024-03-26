
class Matriz:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[0] * columnas for _ in range(filas)]

    def __str__(self):
        return '\n'.join(['\t'.join(map(str, fila)) for fila in self.matriz])

    def __getitem__(self, indice):
        return self.matriz[indice]

    def __setitem__(self, indice, valor):
        self.matriz[indice] = valor

    def __mul__(self, otra_matriz):
        if self.columnas != otra_matriz.filas:
            raise ValueError("Las matrices no tienen las dimensiones adecuadas para la multiplicación.")
        
        resultado = Matriz(self.filas, otra_matriz.columnas)
        
        for i in range(self.filas):
            for j in range(otra_matriz.columnas):
                for k in range(self.columnas):
                    resultado[i][j] += self[i][k] * otra_matriz[k][j]
        
        return resultado

    def __add__(self, otra_matriz):
        if self.filas != otra_matriz.filas or self.columnas != otra_matriz.columnas:
            raise ValueError("Las matrices deben tener las mismas dimensiones para la suma.")
        
        resultado = Matriz(self.filas, self.columnas)
        
        for i in range(self.filas):
            for j in range(self.columnas):
            

                resultado[i][j] = self[i][j] + otra_matriz[i][j]
        
        return resultado

    def __eq__(self, otra_matriz):
        if self.filas != otra_matriz.filas or self.columnas != otra_matriz.columnas:
            return False
        
        for i in range(self.filas):
            for j in range(self.columnas):
                if self[i][j] != otra_matriz[i][j]:
                    return False
        
        return True









if __name__ == '__main__':
    matriz1 = Matriz(3, 3)
    matriz1[0] = [2, 0,  0]
    matriz1[1] = [2, 2, 0]
    matriz1[2] = [3, 2, 1]

    matriz2 = Matriz(3, 4)
    matriz2[0] = [1, 3, 4, 5]
    matriz2[1] = [0, 1, 4, 2]
    matriz2[2] = [0, 0, 1, 3]

    print("Matriz 1 M1:")
    print(matriz1)

    print("\nMatriz 2 M2:")
    print(matriz2)

    print("\nResultado de la suma M1+M1:")
    print(matriz1 + matriz1)

    print("\nResultado de la multiplicación M1*M2:")
    mr = matriz1 * matriz2
    print(matriz1 * matriz2)
    
    # Resultado esperado
    m3 = Matriz(3,4)
    m3[0] = [2, 6, 8, 10]
    m3[1] = [2, 8, 16, 14]
    m3[2] = [3, 11, 21, 22]
    
    if mr == m3:
        print("¡Resultados correctos!")
    else:
        raise Exception("¡Resultados incorrectos en la multiplicación!")





