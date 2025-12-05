import random

class JuegoImpostor:
    def __init__(self):
        self.jugadores = []
        self.palabras = [
            ("HUEVO", "GALLINA"), ("ARENA", "DESIERTO"), ("OLA", "OCÉANO"), 
            ("CANDADO", "SECRETO"), ("FRÍO", "VERDAD"), ("HUECO", "PROMESA"),
            ("RED", "SILENCIO"), ("CRISTAL", "MIEDO"), ("HILO", "DESTINO"), 
            ("POLVO", "OLVIDO"), ("RAÍZ", "IDENTIDAD"), ("ALAS", "DESEO"), 
            ("LLUVIA", "BANCO"), ("PIANO", "CIELO"), ("RELOJ", "BOSQUE"), 
            ("LIBRO", "VIENTO"), ("ESPADA", "NUBE"), ("SILLA", "RÍO"), 
            ("LLAVE", "ESTRELLA"), ("VENTANA", "SUSURRO"), ("ESPEJO", "ECOS"),
              ("PUERTA", "SOMBRA"), ("BRÚJULA", "MEMORIA")
        ]
        self.turno = 0
        self.impostor = 0
        self.pal_inocente = ""
        self.pal_impostor = ""
        self.votos = {}
        self.tiempo = 120
        self.votante_actual = 0
    
    def agregar_jugador(self, nombre):
        if nombre and len(self.jugadores) < 8:
            self.jugadores.append(nombre)
            return True
        return False
    
    def quitar_jugador(self, index):
        if 0 <= index < len(self.jugadores):
            del self.jugadores[index]
            return True
        return False
    
    def iniciar_juego(self):
        if len(self.jugadores) < 3:
            return False
        
        self.pal_inocente, self.pal_impostor = random.choice(self.palabras)
        self.impostor = random.randint(0, len(self.jugadores)-1)
        self.votos = {j:0 for j in self.jugadores}
        self.turno = 0
        self.votante_actual = 0
        return True