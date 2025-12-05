import tkinter as tk
from tkinter import messagebox
from module import JuegoImpostor

def main():
    root = tk.Tk()
    juego = JuegoImpostor()
    
    root.title("Juego del Impostor")
    root.geometry("400x500")
    
    def limpiar():
        for w in root.winfo_children():
            w.destroy()
    
    def mostrar_inicio():
        limpiar()
        tk.Label(root, text=" IMPOSTOR", font=("Arial", 24)).pack(pady=20)
        tk.Label(root, text="Reglas:\n1. Todos ven su palabra en privado\n2. Inocentes tienen misma palabra\n3. Impostor tiene palabra diferente\n4. Descubran al impostor").pack(pady=10)
        tk.Button(root, text="Comenzar", command=configurar, bg="#4CAF50", fg="white").pack(pady=20)
    
    def configurar():
        limpiar()
        tk.Label(root, text="Agregar Jugadores", font=("Arial", 16)).pack()
        
        lista = tk.Listbox(root, height=6)
        lista.pack(pady=10)
        
        entrada = tk.Entry(root)
        entrada.pack(pady=5)
        
        def agregar_jugador():
            nombre = entrada.get().strip()
            if juego.agregar_jugador(nombre):
                lista.insert(tk.END, nombre)
                entrada.delete(0, tk.END)
        
        def quitar_jugador():
            seleccion = lista.curselection()
            if seleccion:
                index = seleccion[0]
                if juego.quitar_jugador(index):
                    lista.delete(index)
        
        entrada.bind("<Return>", lambda e: agregar_jugador())
        tk.Button(root, text="+ Agregar", command=agregar_jugador).pack()
        tk.Button(root, text="- Quitar", command=quitar_jugador).pack(pady=5)
        
        def iniciar_juego():
            if juego.iniciar_juego():
                mostrar_turno()
            else:
                messagebox.showerror("Error", "Mínimo 3 jugadores")
        
        tk.Button(root, text="Comenzar Juego", command=iniciar_juego, bg="#2196F3", fg="white").pack(pady=20)
    
    def mostrar_turno():
        limpiar()
        jugador = juego.jugadores[juego.turno]
        
        tk.Label(root, text=f"Turno de:", font=("Arial", 18)).pack(pady=10)
        tk.Label(root, text=jugador, font=("Arial", 24, "bold"), fg="#E91E63").pack()
        
        tk.Label(root, text="\nPresiona para ver tu palabra\n(No dejes que otros vean)").pack(pady=20)
        
        def mostrar_palabra():
            palabra = juego.pal_impostor if juego.turno == juego.impostor else juego.pal_inocente
            rol = "IMPOSTOR" if juego.turno == juego.impostor else "INOCENTE"
            
            messagebox.showinfo(f"Palabra de {jugador}", 
                              f"Eres: {rol}\n\nTu palabra es:\n\n{palabra}\n\n\n(No la reveles a otros)")
            
            juego.turno += 1
            if juego.turno < len(juego.jugadores):
                mostrar_turno()
            else:
                discusion()
        
        tk.Button(root, text="Ver Mi Palabra", command=mostrar_palabra, 
                 bg="#FF9800", fg="white", font=("Arial", 14), height=2).pack(pady=30)
        
        if juego.turno == len(juego.jugadores)-1:
            tk.Button(root, text="Saltar a Discusión", command=discusion).pack()
    
    def discusion():
        limpiar()
        tk.Label(root, text="DISCUSIÓN", font=("Arial", 20)).pack(pady=20)
        tk.Label(root, text="\nHagan preguntas sin decir sus palabras\nTienen 2 minutos para discutir").pack()
        
        juego.tiempo = 120
        label_tiempo = tk.Label(root, text="02:00", font=("Arial", 32))
        label_tiempo.pack(pady=20)
        
        def iniciar_temporizador():
            def actualizar_tiempo():
                if juego.tiempo > 0:
                    mins = juego.tiempo // 60
                    segs = juego.tiempo % 60
                    label_tiempo.config(text=f"{mins:02d}:{segs:02d}")
                    juego.tiempo -= 1
                    root.after(1000, actualizar_tiempo)
                else:
                    label_tiempo.config(text="00:00", fg="red")
                    votacion()
            actualizar_tiempo()
        
        tk.Button(root, text="Iniciar Temporizador", command=iniciar_temporizador).pack()
        tk.Button(root, text="Saltar a Votación", command=votacion, bg="#9C27B0", fg="white").pack(pady=10)
    
    def votacion():
        limpiar()
        juego.votante_actual = 0
        mostrar_voto()
    
    def mostrar_voto():
        limpiar()
        votante = juego.jugadores[juego.votante_actual]
        
        tk.Label(root, text="VOTACIÓN", font=("Arial", 20)).pack(pady=10)
        tk.Label(root, text=f"Vota {votante}", font=("Arial", 16)).pack()
        tk.Label(root, text="¿Quién es el impostor?").pack(pady=20)
        
        for i, jugador in enumerate(juego.jugadores):
            if i != juego.votante_actual:
                def registrar(j=jugador):
                    juego.votos[j] += 1
                    juego.votante_actual += 1
                    if juego.votante_actual < len(juego.jugadores):
                        mostrar_voto()
                    else:
                        resultados()
                tk.Button(root, text=f"Votar por {jugador}", command=registrar).pack(pady=5)
        
        def abstenerse():
            juego.votante_actual += 1
            if juego.votante_actual < len(juego.jugadores):
                mostrar_voto()
            else:
                resultados()
        
        tk.Button(root, text="Abstenerse", command=abstenerse).pack(pady=10)
    
    def resultados():
        limpiar()
        impostor = juego.jugadores[juego.impostor]
        max_votos = max(juego.votos.values())
        mas_votados = [j for j,v in juego.votos.items() if v == max_votos]
        
        tk.Label(root, text="RESULTADOS", font=("Arial", 20)).pack(pady=20)
        
        for jugador, votos in juego.votos.items():
            color = "red" if jugador == impostor else "black"
            tk.Label(root, text=f"{jugador}: {votos} votos", fg=color).pack()
        
        tk.Label(root, text=f"\nPalabra inocentes: {juego.pal_inocente}\nPalabra impostor: {juego.pal_impostor}").pack(pady=10)
        
        if len(mas_votados) == 1 and mas_votados[0] == impostor:
            resultado = "¡Inocentes ganan!"
            color_res = "green"
        else:
            resultado = "¡Impostor gana!"
            color_res = "red"
        
        tk.Label(root, text=resultado, font=("Arial", 16, "bold"), fg=color_res).pack(pady=20)
        tk.Button(root, text="Jugar otra vez", command=mostrar_inicio, bg="#4CAF50", fg="white").pack()
    
    mostrar_inicio()
    root.mainloop()

if __name__ == "__main__":
    main()