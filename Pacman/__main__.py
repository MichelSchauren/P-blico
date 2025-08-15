import pygame as pg
from pygame.locals import *
import constantes as const
import pacspr as spr
import os
from sys import exit
import random

class Game:
    def __init__(self):
        # Tela do jogo
        pg.init() # Inicializar o pygame
        pg.mixer.init() # Inicializar o mixer/audio do pygame
        pg.mixer.set_reserved(4) # Reserva 4 canais de audio
        self.tela = pg.display.set_mode((const.LARGURA, const.ALTURA)) # Defini uma tela
        pg.display.set_caption(const.TITULO_JOGO) # Defini o título do jogo
        self.rodando = True
        self.fonte = pg.font.match_font(const.FONTE) # Fonte padrao
        self.carregar_arquivos() # Carregar os arquivos de audio e imagem (só imagem)

    def novo_jogo(self):
        # Criar variaveis exenciais do jogo
        self.pontuacao = 0
        self.nivel = 1
        self.n_vidas = 5
        self.tempo = 0
        self.fantasmas_comidos = 0
        self.velocidade_fantasmas = const.VEL_FANTASMA
        self.frutas_pegas = pg.sprite.Group()
        self.adicionar_fruta = True
        # Loop responsável por rodar os levels
        self.rodando_levels = True
        while self.rodando_levels:
            self.criar_sprites()
            pg.mixer.Sound(const.GAME_START).play()
            self.rodar_level()
            self.proximo_level()

    def criar_sprites(self):
        # Criar grupos de sprites
        self.todas_sprites = pg.sprite.Group()
        self.paredes = pg.sprite.Group()
        self.pontos = pg.sprite.Group()
        self.vazios = pg.sprite.Group()
        self.personagens = pg.sprite.Group()
        self.fantasmas = pg.sprite.Group()
        self.vidas = pg.sprite.Group()
        self.fruta_atual = pg.sprite.Group()

        # Criar mapa
        for mapY, linha in enumerate(const.MAPA):
            for mapX, l in enumerate(linha):
                if l == 'M':
                    self.paredes.add(spr.Parede(mapX, mapY))
                elif l == '.':
                    self.pontos.add(spr.Pontos(mapX, mapY, 10))
                elif l == 'o':
                    self.pontos.add(spr.Pontos(mapX, mapY, 50))
                elif l == ' ':
                    self.vazios.add(spr.Vazio(mapX, mapY))
        # Criar Pacman
        self.pacman = spr.Pacman()
        self.personagens.add(self.pacman)
        # Criar fantasmas
        self.f_blinky = spr.Fantasma(0, (const.LARGURA//2 - 8, const.ALTURA//2 - 80), (0, 0), 0, self.velocidade_fantasmas)
        self.f_pinky = spr.Fantasma(1, (const.LARGURA//2 - 32, const.ALTURA//2 - 32), (const.LARGURA, 0), 30, self.velocidade_fantasmas)
        self.f_inky = spr.Fantasma(2, (const.LARGURA//2 - 16, const.ALTURA//2 - 32), (const.LARGURA, const.ALTURA), 60, self.velocidade_fantasmas)
        self.f_clyde = spr.Fantasma(3, (const.LARGURA//2, const.ALTURA//2 -32), (0, const.ALTURA), 90, self.velocidade_fantasmas)
        self.fantasmas.add(self.f_blinky, self.f_pinky, self.f_inky, self.f_clyde)
        # Criar vidas
        for v in range(self.n_vidas):
            self.vidas.add(spr.Vida(v))

        # Adicionar grupos ao grupo dos grupos
        self.todas_sprites.add(self.paredes, self.pontos, self.vazios, self.vidas, self.frutas_pegas, self.fantasmas, self.personagens)

    def rodar_level(self):
        # Loop do jogo
        self.jogando = True
        while self.jogando:
            pg.time.Clock().tick(const.FPS + self.nivel*2)
            self.tempo += 1/(const.FPS + self.nivel*2)
            self.eventos()
            self.atualizar_sprites()
            self.desenhar_sprites()
    
    def proximo_level(self):
        self.nivel += 1
        self.tempo = 0
        self.adicionar_fruta = True
        self.pacman.image = self.pacman.imagens_morte[0]
        self.velocidade_fantasmas += 0.4
        self.desenhar_sprites()
        const.CANAL_1.play(pg.mixer.Sound(const.LEVEL_COMPLETO))
        pg.time.delay(2000)

    def eventos(self):
        # Eventos do jogo
        for event in pg.event.get():
            # Fechar programa
            if event.type == QUIT:
                exit()

            # Movimentar jogador
            if event.type == KEYDOWN and event.key in const.TECLA_DIRECOES: # Precionou
                self.pacman.comeco = False
                self.pacman.nova_direcao = event.key

    def atualizar_sprites(self):
        self.todas_sprites.update()
        # Verificar linhas que colidiram com paredes PACMAN
        colididos = []
        for chave in const.TECLA_DIRECOES:
            linha = self.pacman.pegar_linha(chave)
            for parede in self.paredes:
                if parede.rect.colliderect(linha):
                    colididos.append(linha)
                    break
        self.pacman.colididos = colididos

        # Colisão com fantasmas PACMAN
        for fantasma in self.fantasmas:
            if self.pacman.rect_menor.colliderect(fantasma.rect_menor):
                # Comeu fantasma
                if fantasma.medo and not fantasma.morto:
                    const.CANAL_SIRENE.play(pg.mixer.Sound(const.EAT_GHOST))
                    self.fantasmas_comidos += 1
                    if self.fantasmas_comidos > 4: # Caso comer mais de 4 fantasmas
                        self.pacman.image = spr.Numero('fantasma', 4).image
                        self.pontuacao += 8200
                    else:
                        self.pacman.image = spr.Numero('fantasma', self.fantasmas_comidos-1).image
                        self.pontuacao += (2**self.fantasmas_comidos)*100
                    self.desenhar_sprites()
                    const.CANAL_3.pause()
                    pg.time.delay(500)
                    const.CANAL_3.unpause()
                    fantasma.medo = False
                    fantasma.morto = True
                # Game over / Fantasma te comeu 
                elif not fantasma.morto:
                    const.CANAL_3.play(pg.mixer.Sound(const.DEATH1))
                    
                    self.n_vidas -= 1
                    self.todas_sprites.remove(self.vidas)
                    ultima_vida = list(self.vidas)[-1]
                    self.vidas.remove(ultima_vida)
                    self.todas_sprites.add(self.vidas)

                    if self.n_vidas <= 0:
                        self.jogando = False
                        self.rodando_levels = False
                        self.nivel += -1
                    else:
                        self.game_over()
        # Pegar pontos
        for ponto in self.pontos:
            if self.pacman.rect_menor.colliderect(ponto.rect):
                self.pontuacao += ponto.pontuacao
                if ponto.pontuacao == 50: # Se pegar o ponto maior
                    for fantasma in self.fantasmas:
                        if not fantasma.morto:
                            fantasma.medo = True
                    const.CANAL_3.play(pg.mixer.Sound(const.POWER), 2)
                ponto.kill()
                if not const.CANAL_1.get_busy():
                    const.CANAL_1.play(pg.mixer.Sound(const.MUNCH1))
                    const.CANAL_1.queue(pg.mixer.Sound(const.MUNCH2))
                break
        # Adicionar fruta
        if len(self.pontos) <= 200 and self.adicionar_fruta:
            if self.nivel <= 8:
                self.fruta_atual.add(spr.Fruta(self.nivel-1))
            else:
                self.fruta_atual.add(spr.Fruta(random.randint(0, 7)))
            self.todas_sprites.add(self.fruta_atual)
            self.adicionar_fruta = False
        # Pegar fruta
        for fruta in self.fruta_atual:
            if self.pacman.rect_menor.colliderect(fruta.rect):
                # Coletar a fruta
                fruta.rect.topleft = (const.LARGURA -32 -32*len(self.frutas_pegas), const.ALTURA -32)
                self.frutas_pegas.add(fruta)
                self.fruta_atual.empty()
                # Mova todas as frutas pro lado se não haver mais espaço
                if len(self.frutas_pegas) > 8:
                    self.todas_sprites.remove(self.frutas_pegas)
                    self.frutas_pegas.remove(list(self.frutas_pegas)[0])
                    for fruta in self.frutas_pegas:
                        fruta.rect.x += 32
                    self.todas_sprites.add(self.frutas_pegas)
                # Mostrar pontos da fruta
                try:
                    ponto_fruta = spr.Numero('fruta', self.nivel-1)
                    self.pontuacao += const.PONTOS_FRUTA[self.nivel-1]
                except:
                    ponto_fruta = spr.Numero('fruta', 7)
                    self.pontuacao += 5000
                finally:
                    self.todas_sprites.add(ponto_fruta)
                    self.desenhar_sprites()
                    const.CANAL_1.play(pg.mixer.Sound(const.EAT_FRUTA))
                    pg.time.delay(500)
                    ponto_fruta.kill()
        
        # Inteligencia dos fantasmas
        for fantasma in self.fantasmas:
            # Mover fantasma para dentro da prisão quando morto
            if fantasma.rect_menor.collidepoint(fantasma.porta_prisao) and fantasma.morto:
                fantasma.morto = False
                fantasma.tempo_prisao = 60
                fantasma.rect_menor.center = (const.LARGURA//2, const.ALTURA//2 - 16)
                fantasma.rect.center = fantasma.rect_menor.center
            # Pegar direcoes em que o fantasma pode ir sem bater em paredes
            colididos = []
            nao_colididos = []
            for n in range(4):
                linha = fantasma.pegar_linha(n)
                for parede in self.paredes:
                    if parede.rect.colliderect(linha):
                        colididos.append(linha)
                        break
                if not linha in colididos:
                    nao_colididos.append(linha.center)
            
            # Mover fantasma de acordo com o frame / Sistema de velocidade
            if fantasma.frame >= fantasma.velocidade:
                fantasma.frame = 0
            else:
                fantasma.frame += 1
                # Escolhe para onde o fantasma vai ir
                fantasma.escolher_direcao(nao_colididos, fantasma.ponto_destino(self.pacman, self.f_blinky))
                # Movimentar fantasma
                fantasma.movimentar(fantasma.rect, fantasma.direcao)
                fantasma.movimentar(fantasma.rect_menor, fantasma.direcao)
            # Ativar e desativar tempo dispersão
            if 0 <= self.tempo < 5 or 15 <= self.tempo <= 18:
                fantasma.dispersao = True
            else:
                fantasma.dispersao = False
            
        # Sons
        if not const.CANAL_3.get_busy():
            for fantasma in self.fantasmas:
                fantasma.medo = False
                self.fantasmas_comidos = 0
        if not const.CANAL_SIRENE.get_busy() and len(self.pontos) > 2:
            s = (232 - len(self.pontos))//46 + 1
            const.CANAL_SIRENE.play(pg.mixer.Sound(os.path.join(const.DIRETORIO_AUDIOS, f'siren_{s}.wav')))

        # Terminar level
        if len(self.pontos) == 0:
            self.jogando = False

    def desenhar_sprites(self):
        self.tela.fill(const.FUNDO)
        self.todas_sprites.draw(self.tela)
        self.mostrar_texto(f'Pontuação: {self.pontuacao}', 32, const.BRANCO, const.LARGURA//4, 2)
        self.mostrar_texto(f'Nível: {self.nivel}', 32, const.BRANCO, const.LARGURA - const.LARGURA//4, 2)
        # Desenhos temporarios
        '''
        for rect in self.pacman.colididos:
            pg.draw.rect(self.tela, (0, 0, 255), rect)
        
        for fantasma in self.fantasmas:
            ponto = fantasma.ponto_destino(self.pacman, self.f_blinky)
            pg.draw.line(self.tela, (0, 255, 0), fantasma.rect.center, ponto)
        
        pg.draw.rect(self.tela, (255, 0, 0), self.pacman.rect_menor)
        for fantasma in self.fantasmas:
            pg.draw.rect(self.tela, (0, 255, 0), fantasma.rect_menor)
            pg.draw.rect(self.tela, (0, 0, 255), pg.Rect(fantasma.pegar_linha(fantasma.direcao)))
        
        for parede in self.paredes:
            pg.draw.rect(self.tela, (255, 0, 0), parede.rect, 1)'''

        pg.display.flip()

    def carregar_arquivos(self):
        # Carregar as imagens do jogo
        self.sprite_sheet = const.SPRITESHEET
        self.tela_inicial_logo = os.path.join(const.DIRETORIO_IMAGENS, const.TELA_INICIAL_LOGO)
        self.tela_inicial_logo = pg.image.load(self.tela_inicial_logo).convert()      

    def mostrar_imagem(self, imagem, x, y):
        imagem_rect = imagem.get_rect()
        imagem_rect.midtop = (x, y)
        self.tela.blit(imagem, imagem_rect)

    def mostrar_texto(self, mensagem, tamanho, cor, x, y):
        # Exibe um texto na tela do jogo
        fonte = pg.font.Font(self.fonte, tamanho)
        texto = fonte.render(mensagem, True, cor)
        texto_rect = texto.get_rect()
        texto_rect.midtop = (x, y)
        self.tela.blit(texto, texto_rect)

    def esperar_jogador(self):
        esperando = True
        while esperando:
            pg.time.Clock().tick(const.FPS)
            for event in pg.event.get():
                if event.type == QUIT:
                    esperando = False
                    self.rodando = False
                if event.type == KEYUP and event.key == K_KP_ENTER:
                    esperando = False
                    pg.mixer.music.stop()
                    pg.mixer.Sound(const.MUNCH1).play()
                    

    def tela_inicial(self):
        pg.mixer.music.load(os.path.join(const.DIRETORIO_AUDIOS, const.MUSICA_TELA_INICIAL))
        pg.mixer.music.play()

        self.mostrar_texto('Precione ENTER para jogar', 32, const.AMARELO, const.LARGURA//2, const.ALTURA//2 + 32)
        self.mostrar_texto('Desenvolvido por Michel Schauren', 20, const.BRANCO, const.LARGURA//2, const.LARGURA - 50)
        self.mostrar_imagem(self.tela_inicial_logo, const.LARGURA//2, 80)
        pg.display.flip()
        self.esperar_jogador()

    def game_over(self):
        self.morrendo = True
        while self.morrendo:
            pg.time.Clock().tick(const.FPS)
            self.pacman.morrer()
            self.desenhar_sprites()
            if not self.jogando:
                self.mostrar_texto('Game over', 32, (255, 0, 0), const.LARGURA//2, const.ALTURA//2 + 20)
                pg.display.flip()

            for event in pg.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == KEYDOWN and event.key == K_KP_ENTER:
                    const.CANAL_3.play(pg.mixer.Sound(const.DEATH2))
                    self.morrendo = False
        self.pacman.rect.topleft = (const.LARGURA//2 - 8, 180*2 + 32)
        self.pacman.rect_menor.center = self.pacman.rect.center
        self.pacman.comeco = True
        for pos, fantasma in enumerate(self.fantasmas):
            fantasma.rect.topleft = (const.LARGURA//2 - 8, const.ALTURA//2 - 32)
            fantasma.rect_menor.center = fantasma.rect.center
            fantasma.tempo_prisao = pos*30
            fantasma.morto = False

g = Game()
g.tela_inicial()

while g.rodando:
    g.novo_jogo()
    g.game_over()

# ATUALIZAÇÕES
# dispersão dos fantasmas *
# bug de sair do mapa *
# fantasmas indo para fora do mapa *
# bug de ir para o prox. level *
# bug lista de frutas * (falta testar)
# tempo de medo dos fantasmas *
# velocidade pacman/fantasmas *
# tranparencia das sprites *
# Aumentar a velocidade do fantasma quando morto *
# Ajustar velocidade dos fantasmas *

# CORREÇÂO DE BUGS
# pacman bugando na parede as vezes
# bugs com o teletransporte *
# bug na termino do level *
# bug com a velocidade dos fantasmas
