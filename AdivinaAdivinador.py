import random

print("tengo hambre we")

def adivina_el_numero():
    print("¡Bienvenido al juego 'Adivina el número'!")
    print("Estoy pensando en un número entre 1 y 100. Tienes 10 intentos para adivinarlo.")
    
    numero_secreto = random.randint(1, 100)  # Genera un número aleatorio entre 1 y 100
    intentos = 0
    max_intentos = 10

    while intentos < max_intentos:
        intento = int(input(f"Intento {intentos + 1}/{max_intentos}. Ingresa tu número: "))
        intentos += 1

        if intento < numero_secreto:
            print("El número es más grande. ¡Intenta de nuevo!")
        elif intento > numero_secreto:
            print("El número es más pequeño. ¡Intenta de nuevo!")
        else:
            print(f"¡Felicidades! Adivinaste el número {numero_secreto} en {intentos} intentos.")
            break
    else:
        print(f"¡Lo siento! Has usado todos tus intentos. El número era {numero_secreto}.")

# Llamar a la función para empezar el juego
adivina_el_numero()