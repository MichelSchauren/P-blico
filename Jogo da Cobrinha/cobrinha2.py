import pygame
from pygame.locals import *
import random

pygame.init()

# Configurações do jogo:
largura_tela = 1200
altura_tela = 600
quanidade_macas = 30
FPS = 5

# Conf. TELA
tela = pygame.display.set_mode((largura_tela, altura_tela))
titulo = pygame.display.set_caption('Cobrinha 2')
fundo = (0, 0, 0)

# Conf. TEXTO
fonte = pygame.font.SysFont("Monospace", 20, True, True)

# Criar CLASSES
class Cobra:
    def __init__(self, nome, x, y, cor, direcoes):
        self.nome = nome
        self.x = x
        self.y = y
        self.tamanho = [20, 20]
        self.cor = cor
        self.pontos = 0
        self.texto_pontos = fonte.render(f'Cobra {self.nome} pontos: {self.pontos}', True, self.cor)
        self.direcoes = direcoes
        self.velocidade = [0, 0]
        self.cabeca = [self.x, self.y]
        self.corpo = [self.cabeca]
        self.colidiu = False
        self.comeu = False

    def update(self):
        if self.velocidade != [0, 0]:
            # Mover cobra
            self.x += self.velocidade[0]
            self.y += self.velocidade[1]   
            self.cabeca = [self.x, self.y]
            self.corpo.insert(0, self.cabeca)
            # Colisão
            if self.x < 0 or self.x > largura_tela or self.y < 0 or self.y > altura_tela or self.cabeca in self.corpo[1:]:
                self.colidiu = True
            
            # Aumentar cobra
            for i in range(quanidade_macas): 
                if self.cabeca == [macas[i].x, macas[i].y]:
                    macas[i].update()
                    self.pontos += 1
                    self.texto_pontos = fonte.render(f'Cobra {self.nome} pontos: {self.pontos}', True, self.cor)
                    self.comeu = True
            if self.comeu == False:
                self.corpo.pop()
            self.comeu = False

    def mudar_direcao(self, evento, direçao):
        if evento == direçao[0] and (self.velocidade[0] != 20 or len(self.corpo) == 1):
            self.velocidade = [-20, 0]
        if evento == direçao[1] and (self.velocidade[0] != -20 or len(self.corpo) == 1):
            self.velocidade = [20, 0]
        if evento == direçao[2] and (self.velocidade[1] != 20 or len(self.corpo) == 1):
            self.velocidade = [0, -20]
        if evento == direçao[3] and (self.velocidade[1] != -20 or len(self.corpo) == 1):
            self.velocidade = [0, 20]

class Maca:
    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.tamanho = [20, 20]
        self.cor = cor

    def update(self):
        self.x = random.randrange(0, largura_tela, 20)
        self.y = random.randrange(0, altura_tela, 20)

# Criar COBRAS - paramêtros --> (nome, posição_x, posição_y, cor, teclas_de_direções [esquerda, direita, cima, baixo] )
cobras = []
def adicionarCobras():
    cobras.append(Cobra('VERDE', largura_tela-100, altura_tela-100, (30, 240, 30), [K_LEFT, K_RIGHT, K_UP, K_DOWN]))
    cobras.append(Cobra('AZUL', 100, 100, (30, 30, 240), [K_a, K_d, K_w, K_s]))
    cobras.append(Cobra('AMARELO', 100, altura_tela-100, (240, 240, 30), [K_KP4, K_KP6, K_KP8, K_KP5]))
adicionarCobras()

# Criar MAÇAS
macas = []
for i in range(quanidade_macas):
    macas.append(Maca(random.randrange(0, largura_tela, 20), random.randrange(0, altura_tela, 20), (255, 0, 0)))

# Função de derrota
def vitoria(mensagem, cor):
    rodando_derrota = True
    while rodando_derrota:
        formatacao_texto = fonte.render(f'{mensagem} Press SPACE to play', True, cor)

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    rodando_derrota = False

        tela.blit(formatacao_texto, (largura_tela//2-200, altura_tela//2-20))
        
        pygame.display.update()

rodando = True
while rodando:
    pygame.time.Clock().tick(FPS) # Velocidade do jogo
    tela.fill(fundo) # Pinta a toda a tela de preto

    for event in pygame.event.get():
        if event.type == QUIT: # Evento de sair do jogo
            rodando = False
        
        if event.type == KEYDOWN: # Precionar uma tecla
            for cobra in cobras:
                if event.key in cobra.direcoes:
                    cobra.mudar_direcao(event.key, cobra.direcoes) # Muda a direção da cobra

    # Colisões com inimigos
    for cobra in cobras:
        inimigos = [c for c in cobras if c != cobra]
        for inimigo in inimigos:
            inimigo_corpo = inimigo.corpo[1:]
            if cobra.cabeca in inimigo_corpo:
                cobra.colidiu = True
    # Desenhar objetos na tela
    for i in range(quanidade_macas):
        pygame.draw.rect(tela, macas[i].cor, (macas[i].x, macas[i].y, macas[i].tamanho[0], macas[i].tamanho[1])) 
    for cobra in cobras:
        for c in cobra.corpo:
            pygame.draw.rect(tela, cobra.cor, (c[0], c[1], cobra.tamanho[0], cobra.tamanho[1]))
        cobra.update()
    # escrever texto
    for pos, cobra in enumerate(cobras):
        tela.blit(cobra.texto_pontos, (40, 20*(pos+1)))

    # Derrota
    for cobra in cobras:
        if len(cobras) == 1:
            vitoria(f'{cobra.nome} GANHOU!', cobra.cor)
            # Redefinir objetos
            cobras.clear()
            adicionarCobras()
            macas.clear()
            for i in range(quanidade_macas):
                macas.append(Maca(random.randrange(0, largura_tela, 20), random.randrange(0, altura_tela, 20), (255, 0, 0)))
        if cobra.colidiu:
            cobras.remove(cobra)

    pygame.display.flip()

pygame.quit()
