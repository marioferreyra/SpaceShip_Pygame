# -*- coding: utf-8 -*-

import sys
import pygame
import random
from time import sleep

BLANCO = (255, 255, 255)
ANCHO = 600
ALTO = 680
ASTERIODES = []



class Nave(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.imagen = pygame.image.load("images/nave.png")
        self.imagen_explosion = pygame.image.load("images/explosion.png")
        self.rect = self.imagen.get_rect()
        
        self.rect.centerx = ANCHO/2
        self.rect.centery = 610
    
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)

    def destruccion(self):
        self.imagen = self.imagen_explosion

    def moverDerecha(self):
        self.rect.left += 100

    def moverIzquierda(self):
        self.rect.left -= 100

    def moverArriba(self):
        self.rect.top -= 100

    def moverAbajo(self):
        self.rect.top += 100


class Asteroide(pygame.sprite.Sprite):

    def __init__(self, path_image, posX=0, posY=0):
        pygame.sprite.Sprite.__init__(self)

        self.imagen = pygame.image.load(path_image)
        self.rect = self.imagen.get_rect()

        self.rect.left = posX
        self.rect.top = posY

    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)

    def mover(self):
        self.rect.top += 10

    def detener(self):
        self.rect.top = 0


class Score(pygame.sprite.Sprite):

    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)

        self.posX = posX
        self.posY = posY
        self.puntaje = 0
        self.fuente = pygame.font.SysFont("comicsansms", 25)

    def aumentar(self):
        self.puntaje += 1

    def resetear(self):
        self.puntaje = 0

    def dibujar(self, superficie):
        texto = self.fuente.render("Score: " + str(self.puntaje), True, BLANCO)
        superficie.blit(texto, (self.posX, self.posY))




def cargarAsteriodes():
    asteroide1 = Asteroide("images/asteroide1.png", 22, 10)
    asteroide2 = Asteroide("images/asteroide2.png", 236, 10)
    asteroide3 = Asteroide("images/asteroide3.png", 450, 10)
    ASTERIODES.append(asteroide1)
    ASTERIODES.append(asteroide2)
    ASTERIODES.append(asteroide3)


def elegirAsteriode(lista_asteriodes):
    return lista_asteriodes[random.randint(0, 2)]

def botones(texto, x, y):
    pass

def gameLoop():
    # Creacion Ventana
    ventana = pygame.display.set_mode((ANCHO, ALTO))

    # Titulo de ventana
    pygame.display.set_caption("Space Ship")

    fondo = pygame.image.load("images/fondo.jpg")
    fps = pygame.time.Clock()

    en_juego = True

    nave = Nave()
    score = Score(0, 0)
    cargarAsteriodes()

    asteroide = elegirAsteriode(ASTERIODES)

    while True:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if en_juego:
                # Movimientos
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_LEFT:
                        nave.moverIzquierda()
                    elif evento.key == pygame.K_RIGHT:
                        nave.moverDerecha()
                    elif evento.key == pygame.K_UP:
                        nave.moverArriba()
                    elif evento.key == pygame.K_DOWN:
                        nave.moverAbajo()

        # Cargo el fondo
        ventana.blit(fondo, (0, 0))
        
        # Dibujo la nave
        nave.dibujar(ventana)
        score.dibujar(ventana)

        if en_juego:
            asteroide.dibujar(ventana)
            asteroide.mover()
        if asteroide.rect.colliderect(nave.rect):
            nave.destruccion()
            en_juego = False

        if asteroide.rect.top > ANCHO + 100:
            if en_juego:
                score.aumentar()
            asteroide.rect.top = 10
            asteroide = elegirAsteriode(ASTERIODES)


        fps.tick(20) # 20 FPS
        pygame.display.update()


def main():
    pygame.init()
    gameLoop()


main()
