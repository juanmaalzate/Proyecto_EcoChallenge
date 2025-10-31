import pygame
import random
import sys
import json
import csv
import os
import math

pygame.init()

ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("EcoChallenge")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 120, 255)
VERDE = (0, 160, 0)
ROJO = (230, 50, 50)
GRIS = (160, 160, 160)
NARANJA = (255, 160, 0)

FUENTE = pygame.font.SysFont("arial", 24)

# Cargar residuos desde JSON
ruta_json = os.path.join(os.path.dirname(__file__), 'data', 'residuos.json')
with open(ruta_json, 'r', encoding='utf-8') as f:
    residuos = json.load(f)

# Variables del juego
puntaje = 0
vidas = 3
game_over = False

# Residuo
residuo = random.choice(residuos)
x = random.randint(35, ANCHO-35)
y = 110
radio = 35
vel = 2.5

# Canecas
canecas = [
    {"x": 70 + (120+20)*0, "y": ALTO-130, "w":120, "h":90, "nombre":"Orgánicos", "cat":"organicos", "color":VERDE},
    {"x": 70 + (120+20)*1, "y": ALTO-130, "w":120, "h":90, "nombre":"Reciclables", "cat":"reciclables", "color":AZUL},
    {"x": 70 + (120+20)*2, "y": ALTO-130, "w":120, "h":90, "nombre":"No Recicl.", "cat":"no_reciclables", "color":GRIS},
    {"x": 70 + (120+20)*3, "y": ALTO-130, "w":120, "h":90, "nombre":"Peligrosos", "cat":"peligrosos", "color":ROJO},
]

reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            if not game_over:
                with open(os.path.join(os.path.dirname(__file__), 'scores.csv'),'a',newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([puntaje])
            ejecutando = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                if not game_over:
                    with open(os.path.join(os.path.dirname(__file__), 'scores.csv'),'a',newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([puntaje])
                ejecutando = False
            if game_over and e.key == pygame.K_RETURN:
                puntaje = 0
                vidas = 3
                game_over = False
                residuo = random.choice(residuos)
                x = random.randint(35, ANCHO-35)
                y = 110
                vel = 2.5

    VENTANA.fill(BLANCO)

    # HUD o el panel superior
    pygame.draw.rect(VENTANA, BLANCO, (0,0,ANCHO,70))
    pygame.draw.line(VENTANA, NEGRO, (0,70), (ANCHO,70),1)
    t = FUENTE.render("Puntaje: "+str(puntaje), True, NEGRO)
    VENTANA.blit(t,(30,22))
    vidas_txt = "X"*max(0,vidas) + "-"*max(0,3-vidas)
    t2 = FUENTE.render("Vidas "+vidas_txt, True, NEGRO)
    VENTANA.blit(t2,(ANCHO-t2.get_width()-30,22))

    # Dibujar canecas
    for c in canecas:
        rect = pygame.Rect(c["x"],c["y"],c["w"],c["h"])
        pygame.draw.rect(VENTANA, c["color"], rect)
        pygame.draw.rect(VENTANA, NEGRO, rect,3)
        t = FUENTE.render(c["nombre"], True, NEGRO)
        r = t.get_rect(center=(c["x"]+c["w"]//2, c["y"]+c["h"]+20))
        VENTANA.blit(t,r)

    # Dibujar residuo
    color = NARANJA
    if residuo["forma"]=="circulo":
        color = NARANJA
        pygame.draw.circle(VENTANA, color, (int(x), int(y)), radio)
        pygame.draw.circle(VENTANA, NEGRO, (int(x), int(y)), radio,3)
    elif residuo["forma"]=="rectangulo":
        color = AZUL
        pygame.draw.rect(VENTANA, color, (x-radio,y-radio,radio*2,radio*2))
        pygame.draw.rect(VENTANA, NEGRO, (x-radio,y-radio,radio*2,radio*2),3)
    elif residuo["forma"]=="triangulo":
        color = GRIS
        pts = [(x,y-radio),(x-radio,y+radio),(x+radio,y+radio)]
        pygame.draw.polygon(VENTANA,color,pts)
        pygame.draw.polygon(VENTANA,NEGRO,pts,3)
    elif residuo["forma"]=="rombo":
        color = (120,200,255)
        pts = [(x,y-radio),(x-radio,y),(x,y+radio),(x+radio,y)]
        pygame.draw.polygon(VENTANA,color,pts)
        pygame.draw.polygon(VENTANA,NEGRO,pts,3)
    elif residuo["forma"]=="estrella":
        color = ROJO
        pts = []
        for i in range(10):
            ang = i*math.pi/5
            r = radio if i%2==0 else radio*0.45
            px = int(x + r*math.sin(ang))
            py = int(y - r*math.cos(ang))
            pts.append((px,py))
        pygame.draw.polygon(VENTANA,color,pts)
        pygame.draw.polygon(VENTANA,NEGRO,pts,2)
    else:
        pygame.draw.circle(VENTANA,color,(x,y),radio)
        pygame.draw.circle(VENTANA,NEGRO,(x,y),radio,3)
    t = FUENTE.render(residuo["nombre"], True, NEGRO)
    r = t.get_rect(center=(x, y+radio+30))
    VENTANA.blit(t,r)

    # Juego solo si no es game over
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= 6
        if keys[pygame.K_RIGHT]:
            x += 6
        y += vel

        # Colisiones con bordes
        x = max(radio, min(ANCHO-radio, x))
        y = min(y, ALTO-radio)

        tocado = False
        for c in canecas:
            rect = pygame.Rect(c["x"],c["y"],c["w"],c["h"])
            if rect.collidepoint(x, y+radio):
                tocado=True
                if c["cat"]==residuo["categoria"]:
                    puntaje +=1
                else:
                    vidas -=1
                residuo = random.choice(residuos)
                x = random.randint(35, ANCHO-35)
                y = 110
                vel = 2.5 + 0.15*max(0,puntaje)
                break

        # Caída al vacío
        if y >= ALTO-40 and not tocado:
            vidas -=1
            residuo = random.choice(residuos)
            x = random.randint(35, ANCHO-35)
            y = 110
            vel = 2.5 + 0.15*max(0,puntaje)

        if vidas <=0:
            game_over = True
            with open(os.path.join(os.path.dirname(__file__), 'scores.csv'),'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow([puntaje])

    else:
        overlay = pygame.Surface((ANCHO,ALTO),pygame.SRCALPHA)
        overlay.fill((0,0,0,160))
        VENTANA.blit(overlay,(0,0))
        go = FUENTE.render("GAME OVER",True,BLANCO)
        VENTANA.blit(go, go.get_rect(center=(ANCHO//2,ALTO//2-20)))
        t = FUENTE.render("Puntaje: "+str(puntaje),True,BLANCO)
        VENTANA.blit(t, t.get_rect(center=(ANCHO//2,ALTO//2+15)))
        hint = FUENTE.render("ENTER para reiniciar",True,BLANCO)
        VENTANA.blit(hint, hint.get_rect(center=(ANCHO//2,ALTO//2+50)))

    pygame.display.update()
    reloj.tick(60)

pygame.quit()
sys.exit()
