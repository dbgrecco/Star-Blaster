# Source Generated with Decompyle++
# File: Jogo_Nave3_1.pyc (Python 3.11)

import pygame
import sys
import random
import os
import math

def resource_path(relative_path):
    ''' Get absolute path to resource, works for dev and for PyInstaller '''
    
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)

LARGURA_TELA = 1250
ALTURA_TELA = 719
FPS = 60
CAMINHO_IMAGENS = resource_path('image')
CAMINHO_IMAGENS_NOVAS = os.path.join(CAMINHO_IMAGENS, 'Novas')
CAMINHO_SOM_EXPLOSAO = resource_path('explode.ogg')
CAMINHO_MUSICA_INTRO = resource_path(os.path.join('sounds', 'Alma Brasileira (Assads).mp3'))
CAMINHO_MUSICA_JOGO = resource_path(os.path.join('sounds', 'instrumental.mp3'))
CAMINHO_MUSICA_FASE2 = resource_path(os.path.join('sounds', 'bkg2fase.mp3'))
CAMINHO_MUSICA_FASE3 = resource_path(os.path.join('sounds', 'bkg3fase.mp3'))
CAMINHO_MUSICA_CHEFE = resource_path(os.path.join('sounds', 'boss.mp3'))
CAMINHO_SOM_TIRO_JOGADOR = resource_path(os.path.join('sounds', 'laser-gun-81720.mp3'))
CAMINHO_SOM_TIRO_INIMIGO = resource_path(os.path.join('sounds', 'laser-104.mp3'))
CAMINHO_SOM_POWERUP = resource_path(os.path.join('sounds', 'powerup.mp3'))
POWERUP_TIME = 10000
SUPER_SHOT_CHARGE_TIME = 3000
HIGH_SCORE_FILE = resource_path('highscore.txt')
COR_BRANCA = (255, 255, 255)
COR_AZUL = (100, 100, 255)
COR_VERDE = (100, 255, 100)
COR_VERMELHA = (255, 100, 100)
COR_AMARELA = (255, 255, 100)
COR_ROXA = (255, 100, 255)
COR_CINZA_CLARO = (200, 200, 200)
COR_LARANJA = (255, 165, 0)
ENEMY_DATA = {
    'corvette': {
        'img': 'ship_8.png',
        'escala': (70, 70),
        'vida': 100,
        'pontos': 100,
        'atira': True,
        'freq_tiro': (2500, 4500),
        'rotacao': 90,
        'cor': COR_AZUL },
    'frigate': {
        'img': 'ship_7.png',
        'escala': (80, 80),
        'vida': 200,
        'pontos': 250,
        'atira': True,
        'freq_tiro': (2000, 4000),
        'rotacao': 90,
        'cor': COR_VERDE },
    'gun_boat': {
        'img': 'ship_6.png',
        'escala': (60, 60),
        'vida': 50,
        'pontos': 150,
        'atira': True,
        'freq_tiro': (1500, 3000),
        'rotacao': 90,
        'cor': COR_AMARELA },
    'cruiser': {
        'img': 'ship_2.png',
        'escala': (120, 120),
        'vida': 500,
        'pontos': 800,
        'atira': True,
        'freq_tiro': (1200, 2500),
        'elite': True,
        'rotacao': 90,
        'cor': COR_ROXA },
    'destroyer': {
        'img': 'ship_3.png',
        'escala': (150, 150),
        'vida': 800,
        'pontos': 1200,
        'atira': True,
        'freq_tiro': (800, 1500),
        'elite': True,
        'rotacao': 90,
        'cor': COR_VERMELHA },
    'asteroid': {
        'img': random.choice([
            'asteroid.png',
            'meteorito.png',
            'meteorito2.png']),
        'escala': (60, 60),
        'vida': 100,
        'pontos': 50,
        'atira': False,
        'rotacao': 0,
        'cor': None } }
POWERUP_DATA = {
    'fast_shot': {
        'cor': COR_AMARELA },
    'shield': {
        'cor': COR_AZUL },
    'multi_shot': {
        'cor': COR_VERMELHA },
    'health_pack': {
        'cor': COR_CINZA_CLARO } }
BOSS_DATA = {
    1: {
        'img': 'ship_4.png',
        'escala': (250, 300),
        'vida': 3500,
        'pontos': 5000,
        'rotacao': 90,
        'cor': None,
        'ataque': 'leque',
        'freq_tiro': (1500, 2500),
        'tiros_leque': [
            -15,
            0,
            15] },
    2: {
        'img': 'ship_5.png',
        'escala': (280, 320),
        'vida': 7000,
        'pontos': 15000,
        'rotacao': 90,
        'cor': COR_LARANJA,
        'ataque': 'laser',
        'freq_tiro': (2000, 3000),
        'tiros_leque': [
            -10,
            10] } }
pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('Nave Espacial')
clock = pygame.time.Clock()

def carregar_imagem(nome_arquivo, caminho_base, escalar, flip, escurecer, rotacao, cor_tint = (CAMINHO_IMAGENS, None, False, 0, 0, None)):
    caminho_completo = os.path.join(caminho_base, nome_arquivo)
    
    try:
        imagem = pygame.image.load(caminho_completo).convert_alpha()
        if escalar:
            imagem = pygame.transform.scale(imagem, escalar)
        if rotacao != 0:
            imagem = pygame.transform.rotate(imagem, rotacao)
        if cor_tint:
            tint_surface = pygame.Surface(imagem.get_size()).convert_alpha()
            tint_surface.fill(cor_tint)
            imagem.blit(tint_surface, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
        if flip:
            imagem = pygame.transform.flip(imagem, True, False)
        if escurecer > 0:
            darken_surface = pygame.Surface(imagem.get_size()).convert_alpha()
            darken_surface.fill((0, 0, 0, escurecer))
            imagem.blit(darken_surface, (0, 0))
        return imagem
    except pygame.error:
        e = None
        print(f'''Erro ao carregar a imagem: {caminho_completo}''')
        raise SystemExit(e)
        e = None
        del e



def carregar_som(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        print(f'''Aviso: Arquivo de som n├úo encontrado: {nome_arquivo}''')
        return None
    
    try:
        return pygame.mixer.Sound(nome_arquivo)
    except pygame.error:
        e = None
        print(f'''Erro ao carregar o som: {nome_arquivo}''')
        e = None
        del e
        return None
        e = None
        del e



def tocar_musica(nome_arquivo, loops = (-1,)):
    if not os.path.exists(nome_arquivo):
        print(f'''Aviso: Arquivo de m├║sica n├úo encontrado: {nome_arquivo}''')
        return None
    
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(nome_arquivo)
        pygame.time.wait(100)
        pygame.mixer.music.play(loops)
        return None
    except pygame.error:
        e = None
        print(f'''Erro ao carregar ou tocar a m├║sica: {nome_arquivo}''')
        e = None
        del e
        return None
        e = None
        del e



def carregar_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        f = open(HIGH_SCORE_FILE, 'r')
        None(None, None)
        return 
    except (ValueError, TypeError):
        None(None, None)
        return 0
    with None:
        if not None:
            pass
    return 0


def salvar_high_score(score):
    f = open(HIGH_SCORE_FILE, 'w')
    f.write(str(score))
    None(None, None)
    return None
    with None:
        if not None:
            pass


class Star(pygame.sprite.Sprite):
    pass
# WARNING: Decompyle incomplete


class Thruster(pygame.sprite.Sprite):
    pass
# WARNING: Decompyle incomplete


class Player(pygame.sprite.Sprite):
    pass
# WARNING: Decompyle incomplete


class Enemy(pygame.sprite.Sprite):
    pass
# WARNING: Decompyle incomplete


class Boss(pygame.sprite.Sprite):
    pass
# WARNING: Decompyle incomplete


class LaserBeam(pygame.sprite.Sprite):
    pass
# WARNING: Decompyle incomplete


class PlayerBullet(pygame.sprite.Sprite):
    pass
# WARNING: Decompyle incomplete


class SuperBullet(pygame.sprite.Sprite):
    pass
# WARNING: Decompyle incomplete


class EnemyBullet(pygame.sprite.Sprite):
    pass
# WARNING: Decompyle incomplete


class PowerUp(pygame.sprite.Sprite):
    pass
# WARNING: Decompyle incomplete


def mostrar_texto(superficie, texto, tamanho, x, y, cor = ((255, 255, 255),)):
    fonte = pygame.font.Font(pygame.font.match_font('arial'), tamanho)
    texto_surface = fonte.render(texto, True, cor)
    texto_rect = texto_surface.get_rect(midtop = (x, y))
    superficie.blit(texto_surface, texto_rect)


def draw_health_bar(surf, x, y, pct, max_val, length, height = (150, 20)):
    if pct < 0:
        pct = 0
    fill = (pct / max_val) * length
    outline_rect = pygame.Rect(x, y, length, height)
    fill_rect = pygame.Rect(x, y, fill, height)
    if pct / max_val > 0.6:
        pass
    elif pct / max_val > 0.3:
        pass
    
    cor = (255, 0, 0)
    pygame.draw.rect(surf, cor, fill_rect)
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)


def draw_charge_bar(surf, x, y, pct):
    if pct <= 0:
        return None
    BAR_LENGTH = None
    BAR_HEIGHT = 10
    fill = pct * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (0, 128, 255), fill_rect)
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)


def tela_de_inicio(superficie, fundo, high_score):
    tocar_musica(CAMINHO_MUSICA_INTRO)
    superficie.blit(fundo, (0, 0))
    mostrar_texto(superficie, 'Nave Espacial', 64, LARGURA_TELA / 2, ALTURA_TELA / 4)
    mostrar_texto(superficie, 'Use as setas para mover e segure ESPA├çO para um super tiro', 22, LARGURA_TELA / 2, ALTURA_TELA / 2)
    mostrar_texto(superficie, f'''Recorde: {high_score}''', 28, LARGURA_TELA / 2, ALTURA_TELA * 3 / 4 - 40)
    mostrar_texto(superficie, 'Pressione qualquer tecla para come├ºar', 18, LARGURA_TELA / 2, ALTURA_TELA * 3 / 4)
    pygame.display.flip()
    aguardando = True
# WARNING: Decompyle incomplete


def tela_final(superficie, fundo, pontuacao, high_score):
    tocar_musica(CAMINHO_MUSICA_INTRO)
    superficie.blit(fundo, (0, 0))
    mostrar_texto(superficie, 'Fim de Jogo!', 64, LARGURA_TELA / 2, ALTURA_TELA / 4)
    if pontuacao > high_score:
        mostrar_texto(superficie, 'Novo Recorde!', 30, LARGURA_TELA / 2, ALTURA_TELA / 2 - 40)
        mostrar_texto(superficie, f'''Sua Pontua├º├úo: {pontuacao}''', 35, LARGURA_TELA / 2, ALTURA_TELA / 2)
    else:
        mostrar_texto(superficie, f'''Sua Pontua├º├úo: {pontuacao}''', 35, LARGURA_TELA / 2, ALTURA_TELA / 2 - 20)
        mostrar_texto(superficie, f'''Recorde: {high_score}''', 25, LARGURA_TELA / 2, ALTURA_TELA / 2 + 20)
    mostrar_texto(superficie, 'Pressione qualquer tecla para fechar', 22, LARGURA_TELA / 2, ALTURA_TELA * 3 / 4)
    pygame.display.flip()
    aguardando = True
# WARNING: Decompyle incomplete

screen_shake = 0

def trigger_screen_shake(magnitude):
    global screen_shake
    screen_shake = magnitude


def game_loop(fundo_jogo, som_explosao, som_tiro_jogador, som_tiro_inimigo, som_powerup, current_boss_level, boss_spawn_score_trigger):
    global screen_shake
    trigger_screen_shake(0)
    if current_boss_level == 1:
        tocar_musica(CAMINHO_MUSICA_JOGO)
    elif current_boss_level == 2:
        tocar_musica(CAMINHO_MUSICA_FASE2)
    elif current_boss_level == 3:
        tocar_musica(CAMINHO_MUSICA_FASE3)
    else:
        music_cycle = [
            CAMINHO_MUSICA_JOGO,
            CAMINHO_MUSICA_FASE2,
            CAMINHO_MUSICA_FASE3]
        tocar_musica(music_cycle[(current_boss_level - 1) % len(music_cycle)])
    todos_sprites = pygame.sprite.Group()
    estrelas = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    super_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    boss_group = pygame.sprite.GroupSingle()
# WARNING: Decompyle incomplete


def main():
    fundo_intro = carregar_imagem('space.jpg', escalar = (LARGURA_TELA, ALTURA_TELA))
    fundos_jogo = [
        carregar_imagem('bkg1.png', escalar = (LARGURA_TELA, ALTURA_TELA), escurecer = 100),
        carregar_imagem('bkg2.png', escalar = (LARGURA_TELA, ALTURA_TELA), escurecer = 100),
        carregar_imagem('bkg3.png', escalar = (LARGURA_TELA, ALTURA_TELA), escurecer = 100)]
    som_explosao = carregar_som(CAMINHO_SOM_EXPLOSAO)
    som_tiro_jogador = carregar_som(CAMINHO_SOM_TIRO_JOGADOR)
    som_tiro_inimigo = carregar_som(CAMINHO_SOM_TIRO_INIMIGO)
    som_powerup = carregar_som(CAMINHO_SOM_POWERUP)
    high_score = carregar_high_score()
    current_phase_index = 0
    current_boss_level_id = 1
    boss_spawn_score_trigger = 5000
    fundo_jogo_atual = fundos_jogo[current_phase_index]
    if not tela_de_inicio(tela, fundo_intro, high_score):
        pass
    else:
        (pontuacao_atual, game_status, current_boss_level_id, boss_spawn_score_trigger) = game_loop(fundo_jogo_atual, som_explosao, som_tiro_jogador, som_tiro_inimigo, som_powerup, current_boss_level_id, boss_spawn_score_trigger)
        if game_status == 'quit':
            pass
        elif pontuacao_atual > high_score:
            high_score = pontuacao_atual
            salvar_high_score(high_score)
        if game_status == 'boss_defeated':
            current_phase_index = (current_phase_index + 1) % len(fundos_jogo)
        else:
            tela_final(tela, fundo_intro, pontuacao_atual, high_score)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
    return None
