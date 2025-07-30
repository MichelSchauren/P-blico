import pygame as pg
from pygame.locals import *
import os

# Dimensões da tela
LARGURA = 448
ALTURA = 560

FUNDO = (0, 0, 0 ) # Fundo preto
TITULO_JOGO = 'PacMan' # Título do jogo
FPS = 40 # Frames por segundo / velocidade do jogo
FONTE = 'gabriela' # Fonte padrão do jogo

# Velocidades
VEL_PACMAN = 11
VEL_FANTASMA = 0.1

PONTOS_FRUTA = [100, 300, 500, 700, 1000, 2000, 3000, 5000]

# Cores
BRANCO = (255, 255, 255)
AMARELO = (244, 233, 51)

# Arquivos
DIRETORIO_LOCAL = os.path.dirname(__file__)
DIRETORIO_IMAGENS = os.path.join(DIRETORIO_LOCAL, 'imagens')
DIRETORIO_AUDIOS = os.path.join(DIRETORIO_LOCAL, 'audios')

# Imagens
SPRITESHEET = pg.image.load(os.path.join(DIRETORIO_IMAGENS, 'spritesheet.png'))
TELA_INICIAL_LOGO = 'pacman-logo-1.png'

# Audios
MUSICA_TELA_INICIAL = 'intermission.wav'
MUNCH1 = os.path.join(DIRETORIO_AUDIOS, 'munch_1.wav')
MUNCH2 = os.path.join(DIRETORIO_AUDIOS, 'munch_2.wav')
GAME_START = os.path.join(DIRETORIO_AUDIOS, 'game_start.wav')
RETREATING = os.path.join(DIRETORIO_AUDIOS, 'retreating.wav')
DEATH1 = os.path.join(DIRETORIO_AUDIOS, 'death_1.wav')
DEATH2 = os.path.join(DIRETORIO_AUDIOS, 'death_2.wav')
POWER = os.path.join(DIRETORIO_AUDIOS, 'power_pellet.wav')
EAT_GHOST = os.path.join(DIRETORIO_AUDIOS, 'eat_ghost.wav')
EAT_FRUTA = os.path.join(DIRETORIO_AUDIOS, 'eat_fruit.wav')
LEVEL_COMPLETO = os.path.join(DIRETORIO_AUDIOS, 'extend.wav')

# Canais (mixer)
pg.mixer.init()
CANAL_1 = pg.mixer.Channel(0)
CANAL_2 = pg.mixer.Channel(1)
CANAL_3 = pg.mixer.Channel(2)
CANAL_SIRENE = pg.mixer.Channel(3)

# Teclas de movimentação
TECLA_DIRECOES = [K_RIGHT, K_LEFT, K_UP, K_DOWN]

# Mapa
MAPA = [
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMM",
    "M............MM............M",
    "M.MMMM.MMMMM.MM.MMMMM.MMMM.M",
    "MoMMMM.MMMMM.MM.MMMMM.MMMMoM",
    "M.MMMM.MMMMM.MM.MMMMM.MMMM.M",
    "M..........................M",
    "M.MMMM.MM.MMMMMMMM.MM.MMMM.M",
    "M.MMMM.MM.MMMMMMMM.MM.MMMM.M",
    "M......MM....MM....MM......M",
    "MMMMMM.MMMMM MM MMMMM.MMMMMM",
    "MMMMMM.MMMMM MM MMMMM.MMMMMM",
    "    MM.MM          MM.MM    ",
    "MMMMMM.MM MMMMMMMM MM.MMMMMM",
    "MMMMMM.MM MMMMMMMM MM.MMMMMM",
    "      .   MM    MM   .      ",
    "MMMMMM.MM MMMMMMMM MM.MMMMMM",
    "MMMMMM.MM MMMMMMMM MM.MMMMMM",
    "    MM.MM          MM.MM    ",
    "MMMMMM.MM MMMMMMMM MM.MMMMMM",
    "MMMMMM.MM MMMMMMMM MM.MMMMMM",
    "M............MM............M",
    "M.MMMM.MMMMM.MM.MMMMM.MMMM.M",
    "M.MMMM.MMMMM.MM.MMMMM.MMMM.M",
    "Mo..MM.              .MM..oM",
    "MMM.MM.MM.MMMMMMMM.MM.MM.MMM",
    "MMM.MM.MM.MMMMMMMM.MM.MM.MMM",
    "M......MM....MM....MM......M",
    "M.MMMMMMMMMM.MM.MMMMMMMMMM.M",
    "M.MMMMMMMMMM.MM.MMMMMMMMMM.M",
    "M..........................M",
    "MMMMMMMMMMMMMMMMMMMMMMMMMMMM"
]

# coisas que talvez eu precise
'''# Adicionar fruta
        if len(self.pontos) <= 200 and self.adicionar_fruta:
            try:
                fruta = spr.Fruta(self.nivel-1)
            except:
                fruta = spr.Fruta(random.randint(8))
            fruta.rect.center = (const.LARGURA//2, const.ALTURA//2 + 32)
            
            self.fruta_atual.add(fruta)
            self.todas_sprites.add(self.fruta_atual)
            self.adicionar_fruta = False
        # Pegar fruta
        for fruta in self.fruta_atual:
            if self.pacman.rect_menor.colliderect(fruta):
                try:
                    fruta.image = spr.Numero().numeros_frutas[self.nivel-1]
                    self.pontuacao += const.PONTOS_FRUTA[self.nivel-1]
                except:
                    fruta.image = spr.Numero().numeros_frutas[8]
                    self.pontuacao += const.PONTOS_FRUTA[5000]
                    self.frutas_pegas.append(fruta)
                    self.frutas_pegas.pop(0)
                self.desenhar_sprites()
                const.CANAL_1.play(pg.mixer.Sound(const.EAT_FRUTA))
                pg.time.delay(500)
                fruta.kill()
                
# Pega os rects ao redor do fantasma
            fantasma_rect_direita = pg.Rect(fantasma.rect_menor.x + 16, fantasma.rect_menor.y, 16, 16)
            fantasma_rect_esquerda = pg.Rect(fantasma.rect_menor.x - 16, fantasma.rect_menor.y, 16, 16)
            fantasma_rect_cima = pg.Rect(fantasma.rect_menor.x, fantasma.rect_menor.y - 16, 16, 16)
            fantasma_rect_baixo = pg.Rect(fantasma.rect_menor.x, fantasma.rect_menor.y + 16, 16, 16)
            # Retira aqueles rects que colidem com alguma parede
            fantasma_rects = [fantasma_rect_direita, fantasma_rect_esquerda, fantasma_rect_cima, fantasma_rect_baixo]
            fantasma_rects_naocolididos = fantasma_rects
            print(f'{fantasma_rects} todos os rects')
            for pos, fantasma_rect in enumerate(fantasma_rects):
                for parede in self.paredes:
                    if fantasma_rect.colliderect(parede.rect):
                        pass
                    else:
                        fantasma_rects_naocolididos.append(fantasma_rect)
                        continue
            print(f'{fantasma_rects_naocolididos} não colidirao')
            # Cria os pontos de partida
            pontos_partida = []
            for fantasma_rect in fantasma_rects:
                pontos_partida.append(fantasma_rect.center)
            # Escolhe uma direção e movimenta o fantasma
            fantasma.escolher_direcao(pontos_partida)
            print(f'{fantasma.rect.topleft} nova posição')
            pg.time.delay(5000)'''