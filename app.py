import tkinter as tk
import random
from tkinter import messagebox

class JuegoGato:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Gato")
        self.root.resizable(False, False)
        
        # Estado del juego
        self.tablero = ['' for _ in range(9)]  # Tablero vacío
        self.jugador_actual = 'X'  # Jugador siempre es X, computadora es O
        self.juego_terminado = False
        
        # Crear el tablero gráfico
        self.botones = []
        for i in range(3):
            for j in range(3):
                indice = i * 3 + j
                boton = tk.Button(root, text='', font=('Helvetica', 24), 
                                 width=5, height=2,
                                 command=lambda idx=indice: self.hacer_movimiento(idx))
                boton.grid(row=i, column=j, padx=5, pady=5)
                self.botones.append(boton)
        
        # Botón para reiniciar
        self.btn_reiniciar = tk.Button(root, text='Reiniciar Juego', 
                                     command=self.reiniciar_juego)
        self.btn_reiniciar.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Etiqueta de estado
        self.lbl_estado = tk.Label(root, text="Tu turno (X)", font=('Helvetica', 12))
        self.lbl_estado.grid(row=4, column=0, columnspan=3)
    
    def hacer_movimiento(self, indice):
        # Si el juego terminó o la casilla no está vacía, ignorar el clic
        if self.juego_terminado or self.tablero[indice] != '':
            return
        
        # Registrar movimiento del jugador
        self.tablero[indice] = self.jugador_actual
        self.botones[indice].config(text=self.jugador_actual)
        
        # Verificar si el jugador ganó
        if self.verificar_ganador():
            self.juego_terminado = True
            messagebox.showinfo("Fin del juego", "¡Has ganado!")
            self.lbl_estado.config(text="¡Has ganado!")
            return
        
        # Verificar empate
        if '' not in self.tablero:
            self.juego_terminado = True
            messagebox.showinfo("Fin del juego", "¡Empate!")
            self.lbl_estado.config(text="¡Empate!")
            return
        
        # Turno de la computadora
        self.lbl_estado.config(text="Computadora pensando...")
        self.root.update()  # Actualizar la interfaz
        
        # Simular que la computadora "piensa"
        self.root.after(500, self.movimiento_computadora)
    
    def movimiento_computadora(self):
        # Buscar casillas vacías
        casillas_vacias = [i for i, x in enumerate(self.tablero) if x == '']
        
        if not casillas_vacias:  # Si no hay casillas vacías (por si acaso)
            return
        
        # Elegir una casilla aleatoria
        indice = random.choice(casillas_vacias)
        
        # Hacer el movimiento
        self.tablero[indice] = 'O'
        self.botones[indice].config(text='O')
        
        # Verificar si la computadora ganó
        if self.verificar_ganador():
            self.juego_terminado = True
            messagebox.showinfo("Fin del juego", "¡La computadora ganó!")
            self.lbl_estado.config(text="¡La computadora ganó!")
            return
            
        # Verificar empate
        if '' not in self.tablero:
            self.juego_terminado = True
            messagebox.showinfo("Fin del juego", "¡Empate!")
            self.lbl_estado.config(text="¡Empate!")
            return
        
        # Volver al turno del jugador
        self.lbl_estado.config(text="Tu turno (X)")
    
    def verificar_ganador(self):
        # Combinaciones ganadoras (filas, columnas y diagonales)
        combinaciones = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # filas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columnas
            [0, 4, 8], [2, 4, 6]              # diagonales
        ]
        
        # Verificar cada combinación
        for combo in combinaciones:
            a, b, c = combo
            if self.tablero[a] and self.tablero[a] == self.tablero[b] == self.tablero[c]:
                # Resaltar la combinación ganadora
                self.botones[a].config(bg='light green')
                self.botones[b].config(bg='light green')
                self.botones[c].config(bg='light green')
                return True
        return False
    
    def reiniciar_juego(self):
        # Limpiar el tablero
        self.tablero = ['' for _ in range(9)]
        self.juego_terminado = False
        
        # Resetear los botones
        for boton in self.botones:
            boton.config(text='', bg='SystemButtonFace')
        
        # Resetear estado
        self.lbl_estado.config(text="Tu turno (X)")

# Iniciar el juego
if __name__ == "__main__":
    ventana = tk.Tk()
    app = JuegoGato(ventana)
    ventana.mainloop()