import pygame
import pygame.display
from pygame.locals import *
from sys import exit
import random

pygame.init()

# Conf. Tela
largura = 640
altura = 480
tela = pygame.display.set_mode((largura, altura))
fundo = (0, 0, 0)
titulo = pygame.display.set_caption('Jogo')

# Conf. Textos
fonte = pygame.font.SysFont("Monospace", 15, True, True)
pontos = 0

# Conf. Cobra
cobra = {'x': 320, 'y':240, 'tamanho': [20, 20], 'velocidade': [0, 0], 'corpo': [[320, 240]], 'colidiu': False, 'cor1': (20, 255, 0), 'cor2': (20, 0, 255)}

# Conf. Maça
maca = {'x': int(random.randint(0, 31)*20), 'y': int(random.randint(0, 23)*20), 'tamanho': [20, 20]}

def gerar_degrade(cor1, cor2, n, i):
    degrade = []
    if n == 1:
        degrade = list(cor1)
        return degrade
    else:
        r = int(cor1[0] + (cor2[0] - cor1[0]) * i / (n - 1))
        g = int(cor1[1] + (cor2[1] - cor1[1]) * i / (n - 1))
        b = int(cor1[2] + (cor2[2] - cor1[2]) * i / (n - 1))
        degrade = [r, g, b]
        return degrade

rodando = True
while rodando:
    tela.fill(fundo)
    pygame.time.Clock().tick(10)

    mensagem = f"Pontuação: {pontos}"
    formatacao_texto = fonte.render(mensagem, True, (255, 255, 255))

    for event in pygame.event.get():
        if event.type == QUIT:
            rodando = False
    
    # Movimentação da cobra
        if event.type == KEYDOWN:
            cobra['velocidade'][0] = 0
            cobra['velocidade'][1] = 0
            if event.key == K_LEFT or event.key == K_a:
                cobra['velocidade'][0] = -20
            if event.key == K_RIGHT or event.key == K_d:
                cobra['velocidade'][0] = 20 
            if event.key == K_UP or event.key == K_w:
                cobra['velocidade'][1] = -20
            if event.key == K_DOWN or event.key == K_s:
                cobra['velocidade'][1] = 20

    cobra['x'] += cobra['velocidade'][0]
    cobra['y'] += cobra['velocidade'][1]
    cabeça = [cobra['x'], cobra['y']]
    if cabeça in cobra['corpo'] and (cobra['velocidade'][0] != 0 or cobra['velocidade'][1] != 0):
        cobra['colidiu'] = True
    else:
        cobra['corpo'].insert(0, cabeça)

    # Comer maçã
    if [maca['x'], maca['y']] in cobra['corpo']:
        maca['x'] = int(random.randint(0, 31)*20)
        maca['y'] = int(random.randint(0, 23)*20)
        pontos += 1
    else:
        cobra['corpo'].pop()

    # Desenhar
    for pos, c in enumerate(cobra['corpo']):
        degrade = gerar_degrade(cobra['cor1'], cobra['cor2'], len(cobra['corpo']), pos)
        pygame.draw.rect(tela, (degrade[0], degrade[1], degrade[2]), (c[0], c[1], cobra['tamanho'][0], cobra['tamanho'][1]))
        
    pygame.draw.rect(tela, (255, 0, 0), (maca['x'], maca['y'], maca['tamanho'][0], maca['tamanho'][1]))
    tela.blit(formatacao_texto, (40, 40))

    #Sistema de derrota
    if cobra['x'] >= largura or cobra['x'] < 0 or cobra['y'] >= altura or cobra['y'] < 0 or cobra['colidiu'] == True:

        cobra['x'] = 320
        cobra['y'] = 240
        cobra['velocidade'][0] = 0
        cobra['velocidade'][1] = 0
        cobra['corpo'] = [[cobra['x'], cobra['y']]]
        cobra['colidiu'] = False
        pontos = 0

        rodando_derrota = True
        while rodando_derrota:
            tela.fill((255, 10, 10))
            mensagem = f"Se fudeu!       (press C to play)"
            formatacao_texto = fonte.render(mensagem, True, (255, 255, 255))

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

                if event.type == KEYDOWN:
                    if event.key == K_c:
                        rodando_derrota = False

            tela.blit(formatacao_texto, (180, 200))
            
            pygame.display.update()

    pygame.display.update()
    
pygame.quit()