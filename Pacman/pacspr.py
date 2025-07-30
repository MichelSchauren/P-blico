import pygame as pg
from pygame import sprite
import constantes as const
import random

class Parede(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)

        self.map = const.SPRITESHEET.subsurface((0, 0), (224, 248)).convert_alpha()
        self.image = self.map.subsurface((x*8, y*8), (8, 8))
        self.image = pg.transform.scale(self.image, (8*2, 8*2))
        self.rect = self.image.get_rect()
        self.rect.x = x*8*2
        self.rect.y = y*8*2 + 32

class Pontos(sprite.Sprite):
    def __init__(self, x, y, pontuacao):
        sprite.Sprite.__init__(self)

        self.map = const.SPRITESHEET.subsurface((0, 0), (224, 248)).convert_alpha()
        if pontuacao == 10:
            self.image = self.map.subsurface((8, 8), (8, 8))
        else:
            self.image = self.map.subsurface((8, 24), (8, 8))
        self.image = pg.transform.scale(self.image, (8*2, 8*2))
        self.rect = self.image.get_rect() 
        self.rect.x = x*8*2
        self.rect.y = y*8*2 + 32

        self.pontuacao = pontuacao

class Vazio(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.map = const.SPRITESHEET.subsurface((0, 0), (224, 248)).convert_alpha()
        self.image = self.map.subsurface((12*8, 14*8), (8, 8))
        self.image = pg.transform.scale(self.image, (8*2, 8*2))
        self.rect = self.image.get_rect() 
        self.rect.x = x*8*2
        self.rect.y = y*8*2 + 32

class Pacman(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)

        self.imagens = []
        self.imagens_morte = []

        for y in range(4):
            lista = []
            for x in range(2):
                img = const.SPRITESHEET.subsurface((456 + 16*x, 0 + 16*y), (16, 16)).convert_alpha()
                img = pg.transform.scale(img, (16*2, 16*2))
                lista.append(img)
            img3 = const.SPRITESHEET.subsurface((488, 0), (16, 16)).convert_alpha()
            img3 = pg.transform.scale(img3, (16*2, 16*2))
            lista.append(img3)
            self.imagens.append(lista)

        for x in range(12):
            img = const.SPRITESHEET.subsurface((488 + 16*x, 0), (16, 16)).convert_alpha()
            img = pg.transform.scale(img, (16*2, 16*2))
            self.imagens_morte.append(img)

        self.atual = 0
        self.morrecao = 0
        self.frame = 0
        self.direcao = const.TECLA_DIRECOES[0]
        self.nova_direcao = const.TECLA_DIRECOES[0]
        self.colididos = []
        self.comeco = True

        self.image = self.imagens[const.TECLA_DIRECOES.index(self.direcao)][self.atual]
        self.full_rect = self.image.get_rect()
        self.full_rect.topleft = (const.LARGURA//2 - 16, 180*2 + 32)
        self.rect_menor = self.full_rect.inflate(-16, -16)
        self.rect_menor.center = self.full_rect.center
        self.rect = self.full_rect
    
    def update(self):
        self.animar()
        # Movimentar
        if not self.pegar_linha(self.nova_direcao) in self.colididos and not self.comeco:
            self.direcao = self.nova_direcao
            
        if not self.pegar_linha(self.direcao) in self.colididos and not self.comeco:
            # Mover de acordo com o frame / Sistema de velocidade
            if self.frame == const.VEL_PACMAN:
                self.frame = 0
            else:
                self.frame += 1
                self.movimentar(self.rect, self.direcao)
                self.movimentar(self.rect_menor, self.direcao)

        self.teletransportar()

    def animar(self):
        # Animação de comer
        if not self.pegar_linha(self.direcao) in self.colididos: # Caso o pacman não esteja parado
            self.atual += 0.25
            if self.atual >= 3:
                self.atual = 0
            self.image = self.imagens[const.TECLA_DIRECOES.index(self.direcao)][int(self.atual)]

    def teletransportar(self):
        # teletransporte
        if self.rect_menor.centerx >= const.LARGURA:
            self.rect_menor.centerx = 0
            self.rect.center = self.rect_menor.center
        elif self.rect_menor.centerx <= 0:
            self.rect_menor.centerx = const.LARGURA
            self.rect.center = self.rect_menor.center 

    def movimentar(self, rect, direcao, n=1):
        if direcao == const.TECLA_DIRECOES[0]:
            rect.x += n*4
        elif direcao == const.TECLA_DIRECOES[1]:
            rect.x += -n*4
        elif direcao == const.TECLA_DIRECOES[2]:
            rect.y += -n*4
        elif direcao == const.TECLA_DIRECOES[3]:
            rect.y += n*4

    def morrer(self):
        if self.morrecao >= 11:
            self.morrecao = 0
        self.morrecao += 0.25
        self.image = self.imagens_morte[int(self.morrecao)]

    def pegar_linha(self, key):
        if key == const.TECLA_DIRECOES[0]:
            return pg.Rect(self.rect_menor.right + 1, self.rect_menor.top, 1, 16)
        elif key == const.TECLA_DIRECOES[1]:
            return pg.Rect(self.rect_menor.left - 1, self.rect_menor.top, 1, 16)
        elif key == const.TECLA_DIRECOES[2]:
            return pg.Rect(self.rect_menor.left, self.rect_menor.top - 1, 16, 1)
        elif key == const.TECLA_DIRECOES[3]:
            return pg.Rect(self.rect_menor.left, self.rect_menor.bottom + 1, 16, 1)
        else:
            print('erro ao pegar_ponto')
            return pg.Rect(self.rect_menor.right + 1, self.rect_menor.top, 1, 16)

class Fantasma(sprite.Sprite):
    def __init__(self, fantasma, pos, ponto_dispersao, tempo_prisao, velocidade):
        super().__init__()

        self.velocidade = velocidade
        self.frame = 0
        self.tempo_prisao = tempo_prisao
        self.n_fantasma = fantasma
        self.ponto_dispersao = ponto_dispersao
        self.porta_prisao = (const.LARGURA//2, const.ALTURA//2 - 64)

        self.fantasma_sprites = []
        for d in range(4):
            lista = []
            for a in range(2):
                img = const.SPRITESHEET.subsurface((456 + 16*a + 32*d, 65 + 16*self.n_fantasma), (16, 16)).convert_alpha()
                img = pg.transform.scale(img, (16*2, 16*2))
                lista.append(img)
            self.fantasma_sprites.append(lista)

        self.fantasma_medo = []
        for x in range(4):
            img = const.SPRITESHEET.subsurface((584 + 16*x, 65), (16, 16)).convert_alpha()
            img = pg.transform.scale(img, (16*2, 16*2))
            self.fantasma_medo.append(img)

        self.fantasma_morto = []
        for x in range(4):
            img = const.SPRITESHEET.subsurface((584 + 16*x, 81), (16, 16)).convert_alpha()
            img = pg.transform.scale(img, (16*2, 16*2))
            self.fantasma_morto.append(img)

        self.medo = False
        self.morto = False
        self.dispersao = False
        self.atual = 0
        self.direcao = 0
        

        self.image = self.fantasma_sprites[self.direcao][self.atual]
        self.full_rect = self.image.get_rect()
        self.full_rect.topleft = pos
        self.rect_menor = self.full_rect.inflate(-16, -16)
        self.rect_menor.center = self.full_rect.center
        self.rect = self.full_rect

    def update(self):
        self.animar()
        self.teletranportar()
        self.prender()

    def animar(self):
        # Animação
        self.atual += 0.4
        if self.atual >= 2:
            self.atual = 0

        if self.medo and not self.morto:
            self.image = self.fantasma_medo[int(self.atual)]
        elif self.morto:
            self.image = self.fantasma_morto[self.direcao]
        else:
            self.image = self.fantasma_sprites[self.direcao][int(self.atual)]

    def teletranportar(self):
        # teletransporte
        if self.rect_menor.centerx >= const.LARGURA:
            self.rect_menor.centerx = 8
            self.rect.center = self.rect_menor.center
        elif self.rect_menor.centerx <= 0:
            self.rect_menor.centerx = const.LARGURA - 8
            self.rect.center = self.rect_menor.center 

    def movimentar(self, rect, direcao, n=1):
        if direcao == 0:
            rect.x += n*4
        elif direcao == 1:
            rect.x += -n*4
        elif direcao == 2:
            rect.y += -n*4
        elif direcao == 3:
            rect.y += n*4

    def pegar_linha(self, n):
        if n == 0:
            return pg.Rect(self.rect_menor.right + 1, self.rect_menor.top, 1, 16)
        elif n == 1:
            return pg.Rect(self.rect_menor.left - 1, self.rect_menor.top, 1, 16)
        elif n == 2:
            return pg.Rect(self.rect_menor.left, self.rect_menor.top - 1, 16, 1)
        elif n == 3:
            return pg.Rect(self.rect_menor.left, self.rect_menor.bottom + 1, 16, 1)
        else:
            print('erro ao pegar_ponto')
            return pg.Rect(self.rect_menor.right + 1, self.rect_menor.top, 1, 16)

    def escolher_direcao(self, nao_colididos, ponto_destino):
        try:
            pontos_partida = self.retirar_direcao_traseira(nao_colididos) # Pontos de partida possiveis
            ponto_partida = pontos_partida[0] # Ponto de partida padrao
            distancia = self.calcular_distancia(ponto_partida['ponto'], ponto_destino) # distancia padrao
            # calcula a distancia de cada ponto e caso seja a menor substitui a distancia anterior
            for ponto in pontos_partida:
                nova_distancia = self.calcular_distancia(ponto['ponto'], ponto_destino)
                if not self.medo:
                    if nova_distancia < distancia:
                        distancia = nova_distancia
                        ponto_partida = ponto
                else:
                    if nova_distancia > distancia:
                        distancia = nova_distancia
                        ponto_partida = ponto
            # Atualiza a direção do fantasma
            self.direcao = ponto_partida['direcao']
        except:
            if self.direcao in [0, 2]:
                self.direcao += 1
            else:
                self.direcao += -1

    def retirar_direcao_traseira(self, nao_colididos):
        linhas_novas = []
        for linha in nao_colididos:
            if linha[0] > self.rect.centerx and self.direcao != 1:
                linhas_novas.append({'ponto': linha, 'direcao': 0})
            elif linha[0] < self.rect.centerx and self.direcao != 0:
                linhas_novas.append({'ponto': linha, 'direcao': 1})
            elif linha[1] < self.rect.centery and self.direcao != 3:
                linhas_novas.append({'ponto': linha, 'direcao': 2})
            elif linha[1] > self.rect.centery and self.direcao != 2:
                linhas_novas.append({'ponto': linha, 'direcao': 3})
        return linhas_novas

    def calcular_distancia(self, pontoA, pontoB):
        # Calcula distancia entre dois pontos
        delta_x = abs(pontoA[0] - pontoB[0])
        delta_y = abs(pontoA[1] - pontoB[1])
        result = (delta_x**2 + delta_y**2)**(1/2)
        return result
    
    def ponto_destino(self, pacman, blinky):
        if self.medo:# Ponto mais distante do pacman
            return pacman.rect.center
        elif self.morto:# Porta da prisão
            return self.porta_prisao
        elif self.dispersao:
            return self.ponto_dispersao
        else:# Ponto relativo a personalidade do fantasma

            if self.n_fantasma == 0: # Blinky
                return pacman.rect.center
            
            elif self.n_fantasma == 1: # Pinky
                if 0 <= self.frente_pacman(pacman, 4)[0] <= const.LARGURA and 0 <= self.frente_pacman(pacman, 4)[1] <= const.LARGURA:
                    return self.frente_pacman(pacman, 4)
                else:
                    return pacman.rect.center
                
            elif self.n_fantasma == 2: # Inky
                ponto1 = self.frente_pacman(pacman, 2)
                ponto2 = blinky.rect.center
                deltaX = ponto2[0] - ponto1[0]
                deltaY = ponto2[1] - ponto1[1]
                pontoFinal = (ponto2[0] - deltaX*2, ponto2[1] - deltaY*2)
                return pontoFinal
                
            elif self.n_fantasma == 3: # Clayde
                if self.calcular_distancia(self.rect.center, pacman.rect.center) > 16*8:
                    return pacman.rect.center
                else:
                    return self.ponto_dispersao
                
            else:
                print('erro no ponto_destino')
                return pacman.rect.center
            
    def frente_pacman(self, pacman, n):
        if pacman.direcao == const.TECLA_DIRECOES[0]:
            return (pacman.rect.center[0] + 16*n, pacman.rect.center[1])
        elif pacman.direcao == const.TECLA_DIRECOES[1]:
            return (pacman.rect.center[0] - 16*n, pacman.rect.center[1])
        elif pacman.direcao == const.TECLA_DIRECOES[2]:
            return (pacman.rect.center[0], pacman.rect.center[1] - 16*n)
        elif pacman.direcao == const.TECLA_DIRECOES[3]:
            return (pacman.rect.center[0], pacman.rect.center[1] + 16*n)
        
    def prender(self):
        # Tempo de prisão
        if self.tempo_prisao == 0:
            self.rect.center = self.porta_prisao
            self.rect_menor.center = self.rect.center
        if self.tempo_prisao >= 0:
            self.tempo_prisao -= 1

class Vida(sprite.Sprite):
    def __init__(self, v):
        super().__init__()

        self.image = const.SPRITESHEET.subsurface((584, 16), (16, 16)).convert_alpha()
        self.image = pg.transform.scale(self.image, (16*2, 16*2))
        self.rect = self.image.get_rect()
        self.rect.topleft = (32*v, const.ALTURA - 32)

class Fruta(sprite.Sprite):
    def __init__(self, f):
        super().__init__()

        self.image = const.SPRITESHEET.subsurface((488 + 16*f, 48), (16, 16)).convert_alpha()
        self.image = pg.transform.scale(self.image, (16*2, 16*2))
        self.rect = self.image.get_rect()
        self.rect.center = (const.LARGURA//2, const.ALTURA//2 + 32)

class Numero(sprite.Sprite):
    def __init__(self, classe, n):
        super().__init__()

        self.numeros_fantasmas = []
        self.numeros_frutas = []

        # Imagens de numeros dos fantasmas [200, 400, 800, 1600, 8200]
        for f in range(5):
            i = 0
            if f == 4:
                i = 5
            img = const.SPRITESHEET.subsurface((456 + 16*f, 129), (16 + i, 16)).convert_alpha()
            img = pg.transform.scale(img, (16*2, 16*2))
            self.numeros_fantasmas.append(img)
        # Imagens de numeros das frutas [100, 300, 500, 700]
        for f in range(4): 
            img = const.SPRITESHEET.subsurface((456 + 16*f, 144), (16, 16)).convert_alpha()
            img = pg.transform.scale(img, (16*2, 16*2))
            self.numeros_frutas.append(img)
        for f in range(4): # [1000, 2000, 3000, 5000]
            img = const.SPRITESHEET.subsurface((518, 144 + 16*f), (19, 16)).convert_alpha()
            img = pg.transform.scale(img, (19*2, 16*2))
            self.numeros_frutas.append(img)
        # Criar image e rect
        if classe == 'fantasma':
            self.image = self.numeros_fantasmas[n]
        elif classe == 'fruta':
            self.image = self.numeros_frutas[n]
        else:
            self.image = self.numeros_fantasmas[0] # Padrão
        self.rect = self.image.get_rect()
        self.rect.center = (const.LARGURA//2, const.ALTURA//2 + 32)