import pygame
import sys
import random
import os
import math
import asyncio

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
CAMINHO_SOM_EXPLOSAO = resource_path('explode.wav')
CAMINHO_MUSICA_INTRO = resource_path(os.path.join('sounds', 'intro.wav'))
CAMINHO_MUSICA_JOGO = resource_path(os.path.join('sounds', 'game.wav'))
CAMINHO_MUSICA_FASE2 = resource_path(os.path.join('sounds', 'phase2.wav'))
CAMINHO_MUSICA_FASE3 = resource_path(os.path.join('sounds', 'phase3.wav'))
CAMINHO_MUSICA_CHEFE = resource_path(os.path.join('sounds', 'boss.wav'))
CAMINHO_SOM_TIRO_JOGADOR = resource_path(os.path.join('sounds', 'laser_player.wav'))
CAMINHO_SOM_TIRO_INIMIGO = resource_path(os.path.join('sounds', 'laser_enemy.wav'))
CAMINHO_SOM_POWERUP = resource_path(os.path.join('sounds', 'powerup.wav'))
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
        'cor': COR_AZUL
    },
    'frigate': {
        'img': 'ship_7.png',
        'escala': (80, 80),
        'vida': 200,
        'pontos': 250,
        'atira': True,
        'freq_tiro': (2000, 4000),
        'rotacao': 90,
        'cor': COR_VERDE
    },
    'gun_boat': {
        'img': 'ship_6.png',
        'escala': (60, 60),
        'vida': 50,
        'pontos': 150,
        'atira': True,
        'freq_tiro': (1500, 3000),
        'rotacao': 90,
        'cor': COR_AMARELA
    },
    'cruiser': {
        'img': 'ship_2.png',
        'escala': (120, 120),
        'vida': 500,
        'pontos': 800,
        'atira': True,
        'freq_tiro': (1200, 2500),
        'elite': True,
        'rotacao': 90,
        'cor': COR_ROXA
    },
    'destroyer': {
        'img': 'ship_3.png',
        'escala': (150, 150),
        'vida': 800,
        'pontos': 1200,
        'atira': True,
        'freq_tiro': (800, 1500),
        'elite': True,
        'rotacao': 90,
        'cor': COR_VERMELHA
    },
    'asteroid': {
        'img': 'asteroid.png', # Placeholder key, randomly select below
        'escala': (60, 60),
        'vida': 100,
        'pontos': 50,
        'atira': False,
        'rotacao': 0,
        'cor': None
    }
}

POWERUP_DATA = {
    'fast_shot': {
        'cor': COR_AMARELA
    },
    'shield': {
        'cor': COR_AZUL
    },
    'multi_shot': {
        'cor': COR_VERMELHA
    },
    'health_pack': {
        'cor': COR_CINZA_CLARO
    }
}

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
        'tiros_leque': [-15, 0, 15]
    },
    2: {
        'img': 'ship_5.png',
        'escala': (280, 320),
        'vida': 7000,
        'pontos': 15000,
        'rotacao': 90,
        'cor': COR_LARANJA,
        'ataque': 'laser',
        'freq_tiro': (2000, 3000),
        'tiros_leque': [-10, 10]
    }
}

pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('Nave Espacial')
clock = pygame.time.Clock()

def carregar_imagem(nome_arquivo, caminho_base=CAMINHO_IMAGENS, escalar=None, flip=False, escurecer=0, rotacao=0, cor_tint=None):
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
            imagem.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        if flip:
            imagem = pygame.transform.flip(imagem, True, False)
        if escurecer > 0:
            darken_surface = pygame.Surface(imagem.get_size()).convert_alpha()
            darken_surface.fill((0, 0, 0, escurecer))
            imagem.blit(darken_surface, (0, 0))
        return imagem
    except pygame.error as e:
        print(f"Erro ao carregar a imagem: {caminho_completo}")
        raise SystemExit(e)

def carregar_som(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        print(f"Aviso: Arquivo de som não encontrado: {nome_arquivo}")
        return None
    try:
        return pygame.mixer.Sound(nome_arquivo)
    except pygame.error:
        print(f"Erro ao carregar o som: {nome_arquivo}")
        return None

def tocar_musica(nome_arquivo, loops=-1):
    if not os.path.exists(nome_arquivo):
        print(f"Aviso: Arquivo de música não encontrado: {nome_arquivo}")
        return None
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(nome_arquivo)
        pygame.time.wait(100)
        pygame.mixer.music.play(loops)
        return None
    except pygame.error:
        print(f"Erro ao carregar ou tocar a música: {nome_arquivo}")
        return None

def carregar_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                return int(f.read().strip())
        except (ValueError, TypeError):
            return 0
    return 0

def salvar_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(score))
    except Exception:
        pass

# ----------------------------------------------------
# PREMIUM PARTICLE SYSTEM
# ----------------------------------------------------
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.size = random.randint(3, 7)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.color = color
        self.alpha = 255
        self.image.fill((*self.color, self.alpha))
        self.rect = self.image.get_rect(center=(x, y))
        # Random explosion direction and velocity
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.velocity = pygame.math.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        self.lifespan = random.randint(20, 40)
        self.age = 0

    def update(self, *args):
        self.age += 1
        if self.age >= self.lifespan:
            self.kill()
            return
            
        # Spacy physics: decelerate and float
        self.rect.x += int(self.velocity.x)
        self.rect.y += int(self.velocity.y)
        self.velocity *= 0.95
        
        # Shrink and fade
        self.alpha = int((1 - self.age / self.lifespan) * 255)
        current_size = max(1, int(self.size * (1 - self.age / self.lifespan)))
        self.image = pygame.Surface((current_size, current_size), pygame.SRCALPHA)
        self.image.fill((*self.color, self.alpha))
        # Keep centered
        cx, cy = self.rect.center
        self.rect = self.image.get_rect(center=(cx, cy))

def criar_explosao(x, y, color, all_sprites):
    # Default color to orange/fire if none
    if not color:
        colors = [(255, 100, 0), (255, 200, 0), (255, 50, 0)]
    else:
        colors = [color, (min(255, color[0]+50), min(255, color[1]+50), min(255, color[2]+50)), (255, 255, 255)]
        
    for _ in range(25):
        c = random.choice(colors)
        p = Particle(x, y, c)
        all_sprites.add(p)

# ----------------------------------------------------
# GAME ENTITIES
# ----------------------------------------------------
class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Premium: Parallax Scrolling Layers
        self.layer = random.choice([1, 2, 3])
        if self.layer == 1:
            self.size = 1
            self.velocidade = random.uniform(0.1, 0.4)
            color = random.choice([(100, 100, 120), (120, 120, 140)])
        elif self.layer == 2:
            self.size = 2
            self.velocidade = random.uniform(0.5, 0.9)
            color = random.choice([(150, 150, 180), (180, 180, 200)])
        else:
            self.size = 3
            self.velocidade = random.uniform(1.0, 1.8)
            color = random.choice([(200, 200, 255), (255, 255, 255)])
            
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(random.randrange(LARGURA_TELA), random.randrange(ALTURA_TELA)))
        
    def update(self, *args):
        self.rect.x -= self.velocidade
        if self.rect.right < 0:
            self.rect.left = LARGURA_TELA
            self.rect.y = random.randrange(ALTURA_TELA)

class Thruster(pygame.sprite.Sprite):
    def __init__(self, parent, is_player=True):
        super().__init__()
        self.parent = parent
        self.is_player = is_player
        self.images = [
            pygame.Surface((random.randint(15, 25), random.randint(8, 12)), pygame.SRCALPHA)
            for _ in range(3)
        ]
        for surf in self.images:
            color = random.choice([(255, 220, 0), (255, 165, 0), (255, 140, 0)])
            pygame.draw.ellipse(surf, color, surf.get_rect())
            
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.animation_speed = 60 # Faster animation
        self.last_update = pygame.time.get_ticks()
        
    def update(self, *args):
        if not self.parent.alive():
            self.kill()
            return
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
            
        if self.is_player:
            self.rect.midright = self.parent.rect.midleft
        else:
            self.rect.midleft = self.parent.rect.midright

class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, player_bullets, super_bullets, som_tiro):
        super().__init__()
        self.original_image = carregar_imagem('ship_1.png', CAMINHO_IMAGENS_NOVAS, escalar=(80, 100), rotacao=-90)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(100, ALTURA_TELA // 2))
        self.velocidade = 8
        self.all_sprites = all_sprites
        self.player_bullets = player_bullets
        self.super_bullets = super_bullets
        self.som_tiro = som_tiro
        self.powerups = {}
        self.health = 100
        self.max_health = 100
        self.is_charging = False
        self.charge_start_time = 0
        self.thruster = Thruster(self, is_player=True)
        self.all_sprites.add(self.thruster)
        self.flash_duration = 200
        self.last_flash = 0
        self.base_shoot_delay = 250
        self.shoot_delay = self.base_shoot_delay
        
    def update(self, *args):
        self.check_powerups()
        self.handle_flash()
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidade
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
            
        self.rect.clamp_ip(tela.get_rect())
        
        if self.is_charging:
            draw_charge_bar(tela, self.rect.x, self.rect.top - 15, self.get_charge_percentage())

    def start_charging(self):
        self.is_charging = True
        self.charge_start_time = pygame.time.get_ticks()

    def get_charge_percentage(self):
        if not self.is_charging:
            return 0
        charge_duration = pygame.time.get_ticks() - self.charge_start_time
        return min(charge_duration / SUPER_SHOT_CHARGE_TIME, 1.0)

    def fire(self):
        charge_duration = pygame.time.get_ticks() - self.charge_start_time
        if self.is_charging and charge_duration >= SUPER_SHOT_CHARGE_TIME:
            self.fire_super_shot()
        else:
            self.fire_normal_shot()
        self.is_charging = False

    def fire_normal_shot(self):
        now = pygame.time.get_ticks()
        if now > self.powerups.get('last_shot', 0):
            self.powerups['last_shot'] = now + self.shoot_delay
            if 'multi_shot' in self.powerups:
                for angle in (-20, 0, 20):
                    bullet = PlayerBullet(self.rect.right, self.rect.centery, angle)
                    self.all_sprites.add(bullet)
                    self.player_bullets.add(bullet)
            else:
                bullet = PlayerBullet(self.rect.right, self.rect.centery, 0)
                self.all_sprites.add(bullet)
                self.player_bullets.add(bullet)
                
            if self.som_tiro:
                self.som_tiro.play()

    def fire_super_shot(self):
        super_bullet = SuperBullet(self.rect.right, self.rect.centery)
        self.all_sprites.add(super_bullet)
        self.super_bullets.add(super_bullet)
        som_explosao = carregar_som(CAMINHO_SOM_EXPLOSAO)
        if som_explosao:
            som_explosao.play()
        trigger_screen_shake(20)

    def take_damage(self, amount):
        if 'shield' in self.powerups:
            return
        self.health -= amount
        self.last_flash = pygame.time.get_ticks()
        # Premium: spawn sparks on damage
        criar_explosao(self.rect.centerx, self.rect.centery, (100, 100, 255), self.all_sprites)
        trigger_screen_shake(8)
        if self.health <= 0:
            self.health = 0
            self.kill()

    def handle_flash(self):
        if self.last_flash and pygame.time.get_ticks() - self.last_flash < self.flash_duration:
            self.image.fill(COR_BRANCA, special_flags=pygame.BLEND_RGB_ADD)
        else:
            self.image = self.original_image.copy()

    def kill(self):
        # Spawns massive player explosion
        criar_explosao(self.rect.centerx, self.rect.centery, (255, 100, 0), self.all_sprites)
        criar_explosao(self.rect.centerx, self.rect.centery, (255, 200, 0), self.all_sprites)
        self.thruster.kill()
        super().kill()

    def activate_powerup(self, p_type):
        now = pygame.time.get_ticks()
        if p_type == 'health_pack':
            self.health += 25
            if self.health > self.max_health:
                self.health = self.max_health
            return
            
        if p_type in self.powerups:
            self.powerups[p_type] += POWERUP_TIME
        else:
            self.powerups[p_type] = now + POWERUP_TIME
            
        if p_type == 'fast_shot':
            self.shoot_delay = 100

    def check_powerups(self):
        now = pygame.time.get_ticks()
        for p_type, expiration_time in list(self.powerups.items()):
            if p_type == 'last_shot':
                continue
            if now > expiration_time:
                del self.powerups[p_type]
                if p_type == 'fast_shot':
                    self.shoot_delay = self.base_shoot_delay

    def draw_shield(self, surface):
        if 'shield' in self.powerups:
            remaining_time = self.powerups['shield'] - pygame.time.get_ticks()
            alpha = (remaining_time / POWERUP_TIME) * 128
            if alpha < 0:
                alpha = 0
            shield_radius = max(self.rect.width, self.rect.height) // 2 + 15
            shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (100, 100, 255, int(alpha)), (shield_radius, shield_radius), shield_radius)
            pygame.draw.circle(shield_surface, (180, 180, 255, int(alpha * 1.5)), (shield_radius, shield_radius), shield_radius, 2)
            surface.blit(shield_surface, (self.rect.centerx - shield_radius, self.rect.centery - shield_radius))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, all_sprites, enemy_bullets, som_tiro_inimigo, player, rank='comum'):
        super().__init__()
        self.all_sprites = all_sprites
        self.enemy_bullets = enemy_bullets
        self.som_tiro_inimigo = som_tiro_inimigo
        self.player = player
        self.rank = rank
        
        if rank == 'elite':
            self.enemy_type = random.choice([k for k, v in ENEMY_DATA.items() if v.get('elite')])
        else:
            # Procedural choice excluding asteroid here since we handle it below
            self.enemy_type = random.choice([k for k, v in ENEMY_DATA.items() if not v.get('elite') and k != 'asteroid'])
            
        # 10% chance to be an asteroid for non-elite
        if rank != 'elite' and random.random() < 0.15:
            self.enemy_type = 'asteroid'
            
        data = ENEMY_DATA[self.enemy_type]
        self.color = data['cor']
        
        if self.enemy_type == 'asteroid':
            # Dynamically select an asteroid image
            img_name = random.choice(['asteroid.png', 'meteorito.png', 'meteorito2.png'])
            caminho_base = CAMINHO_IMAGENS
        else:
            img_name = data['img']
            caminho_base = CAMINHO_IMAGENS_NOVAS
            
        self.original_image = carregar_imagem(img_name, caminho_base, escalar=data['escala'], rotacao=data['rotacao'], cor_tint=data['cor'])
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.health = data['vida']
        self.score_value = data['pontos']
        self.can_shoot = data['atira']
        
        self.last_flash = 0
        self.flash_duration = 150
        
        if self.can_shoot:
            self.base_freq_tiro = data['freq_tiro']
            self.shoot_delay = random.randint(*self.base_freq_tiro)
            self.last_shot = pygame.time.get_ticks()
            self.thruster = Thruster(self, is_player=False)
            self.all_sprites.add(self.thruster)
        else:
            self.thruster = None
            
        self.resetar()

    def resetar(self):
        self.rect.x = random.randrange(LARGURA_TELA + 50, LARGURA_TELA + 400)
        self.rect.y = random.randrange(0, ALTURA_TELA - self.rect.height)
        self.velocidade = random.uniform(1.5, 4.5)
        # Reset health
        data = ENEMY_DATA[self.enemy_type]
        self.health = data['vida']

    def update(self, difficulty_multiplier=1):
        self.rect.x -= self.velocidade
        if self.rect.right < 0:
            self.resetar()
        if self.can_shoot:
            self.shoot(difficulty_multiplier)
        self.handle_flash()

    def shoot(self, difficulty_multiplier):
        now = pygame.time.get_ticks()
        current_delay = self.shoot_delay * difficulty_multiplier
        if now - self.last_shot > current_delay:
            self.last_shot = now
            min_delay, max_delay = self.base_freq_tiro
            self.shoot_delay = random.randint(int(min_delay * difficulty_multiplier), int(max_delay * difficulty_multiplier))
            bullet = EnemyBullet(self.rect.center, self.player.rect.center)
            self.all_sprites.add(bullet)
            self.enemy_bullets.add(bullet)
            if self.som_tiro_inimigo:
                self.som_tiro_inimigo.play()

    def take_damage(self, amount):
        self.health -= amount
        self.last_flash = pygame.time.get_ticks()
        # Spawn small hit sparks
        criar_explosao(self.rect.centerx, self.rect.centery, self.color, self.all_sprites)
        if self.health <= 0:
            self.kill()
            return self.score_value
        return 0

    def handle_flash(self):
        if self.last_flash and pygame.time.get_ticks() - self.last_flash < self.flash_duration:
            # Red/White flash tint
            tint = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            tint.fill((255, 255, 255, 120))
            self.image = self.original_image.copy()
            self.image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        else:
            self.image = self.original_image.copy()

    def kill(self):
        # Spawn explosion particles
        criar_explosao(self.rect.centerx, self.rect.centery, self.color, self.all_sprites)
        if self.thruster:
            self.thruster.kill()
        super().kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self, all_sprites, enemy_bullets, som_tiro_inimigo, player, level=1):
        super().__init__()
        self.all_sprites = all_sprites
        self.enemy_bullets = enemy_bullets
        self.som_tiro_inimigo = som_tiro_inimigo
        self.player = player
        self.level = level
        
        data = BOSS_DATA[self.level]
        self.color = data['cor']
        self.original_image = carregar_imagem(data['img'], CAMINHO_IMAGENS_NOVAS, escalar=data['escala'], rotacao=data['rotacao'], cor_tint=data['cor'])
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(centerx=LARGURA_TELA + 200, centery=ALTURA_TELA // 2)
        self.health = data['vida']
        self.max_health = data['vida']
        self.score_value = data['pontos']
        self.attack_type = data['ataque']
        self.base_freq_tiro = data['freq_tiro']
        self.tiros_leque = data['tiros_leque']
        self.entry_speed = 2
        self.speed_y = 2
        self.is_on_screen = False
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = random.randint(*self.base_freq_tiro)
        self.laser_charge_time = 2000
        self.laser_duration = 1000
        self.is_charging_laser = False
        self.laser_charge_start = 0
        
        self.last_flash = 0
        self.flash_duration = 150

    def update(self, difficulty_multiplier=1):
        if not self.is_on_screen:
            self.rect.x -= self.entry_speed
            if self.rect.right < LARGURA_TELA - 50:
                self.is_on_screen = True
            return
            
        self.rect.y += self.speed_y
        if self.rect.top < 0 or self.rect.bottom > ALTURA_TELA:
            self.speed_y *= -1
            
        self.shoot(difficulty_multiplier)
        self.handle_flash()

    def shoot(self, difficulty_multiplier):
        now = pygame.time.get_ticks()
        current_delay = self.shoot_delay * difficulty_multiplier
        if self.attack_type == 'laser' and self.is_charging_laser:
            charge_elapsed = now - self.laser_charge_start
            if charge_elapsed > self.laser_charge_time:
                self.is_charging_laser = False
                laser = LaserBeam(self.rect.midleft, self.laser_duration)
                self.all_sprites.add(laser)
                self.enemy_bullets.add(laser)
            else:
                # Warning line
                start_pos = self.rect.midleft
                end_pos = (0, start_pos[1])
                pygame.draw.line(tela, COR_LARANJA, start_pos, end_pos, 4) # Thicker warning line
            return
            
        if now - self.last_shot > current_delay:
            self.last_shot = now
            min_delay, max_delay = self.base_freq_tiro
            self.shoot_delay = random.randint(int(min_delay * difficulty_multiplier), int(max_delay * difficulty_multiplier))
            
            if self.attack_type == 'leque':
                self.shoot_fan(angles=self.tiros_leque)
            elif self.attack_type == 'laser':
                if random.random() < 0.4:  # Slightly higher chance for laser
                    self.is_charging_laser = True
                    self.laser_charge_start = now
                else:
                    self.shoot_fan(angles=self.tiros_leque)

    def shoot_fan(self, angles=[-15, 0, 15]):
        start_pos = self.rect.midleft
        target_pos = self.player.rect.center
        try:
            direction = (pygame.math.Vector2(target_pos) - start_pos).normalize()
        except ValueError:
            direction = pygame.math.Vector2(-1, 0)
            
        for angle in angles:
            rotated_dir = direction.rotate(angle)
            bullet = EnemyBullet(start_pos, start_pos + rotated_dir * 100)
            self.all_sprites.add(bullet)
            self.enemy_bullets.add(bullet)
            
        if self.som_tiro_inimigo:
            self.som_tiro_inimigo.play()

    def take_damage(self, amount):
        self.health -= amount
        self.last_flash = pygame.time.get_ticks()
        criar_explosao(self.rect.centerx - 50, self.rect.centery + random.randint(-50, 50), self.color, self.all_sprites)
        trigger_screen_shake(10)
        if self.health <= 0:
            self.kill()
            trigger_screen_shake(40)
            return self.score_value
        return 0

    def handle_flash(self):
        if self.last_flash and pygame.time.get_ticks() - self.last_flash < self.flash_duration:
            tint = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            tint.fill((255, 255, 255, 120))
            self.image = self.original_image.copy()
            self.image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        else:
            self.image = self.original_image.copy()

    def kill(self):
        # Massive explosion bursts
        for _ in range(5):
            ex_x = self.rect.centerx + random.randint(-50, 50)
            ex_y = self.rect.centery + random.randint(-50, 50)
            criar_explosao(ex_x, ex_y, self.color, self.all_sprites)
        super().kill()

class LaserBeam(pygame.sprite.Sprite):
    def __init__(self, start_pos, duration):
        super().__init__()
        self.image = pygame.Surface((LARGURA_TELA, 30)) # Thicker laser beam
        self.image.fill(COR_LARANJA)
        # Add yellow laser core inside the orange laser beam
        pygame.draw.rect(self.image, (255, 255, 200), (0, 7, LARGURA_TELA, 16))
        self.rect = self.image.get_rect(midleft=start_pos)
        self.spawn_time = pygame.time.get_ticks()
        self.duration = duration
        
    def update(self, *args):
        if pygame.time.get_ticks() - self.spawn_time > self.duration:
            self.kill()

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0):
        super().__init__()
        self.image = carregar_imagem('bola_fogo.png', CAMINHO_IMAGENS_NOVAS, escalar=(30, 30))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 16
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(self.speed, 0).rotate(angle)
        
    def update(self, *args):
        self.pos += self.velocity
        self.rect.center = self.pos
        if self.rect.left > LARGURA_TELA:
            self.kill()

class SuperBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = carregar_imagem('bola_fogo.png', CAMINHO_IMAGENS_NOVAS, escalar=(90, 90))
        self.rect = self.image.get_rect(centery=y, left=x)
        self.velocidade = 22
        
    def update(self, *args):
        self.rect.x += self.velocidade
        if self.rect.left > LARGURA_TELA:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()
        self.image = carregar_imagem('bola_fogo.png', CAMINHO_IMAGENS_NOVAS, escalar=(20, 20))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = 8
        self.pos = pygame.math.Vector2(start_pos)
        try:
            self.velocity = (pygame.math.Vector2(target_pos) - start_pos).normalize() * self.speed
        except ValueError:
            self.velocity = pygame.math.Vector2(-self.speed, 0)
            
    def update(self, *args):
        self.pos += self.velocity
        self.rect.center = self.pos
        if not tela.get_rect().colliderect(self.rect):
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(list(POWERUP_DATA.keys()))
        data = POWERUP_DATA[self.type]
        self.image = carregar_imagem('saturno.png', CAMINHO_IMAGENS, escalar=(60, 60), cor_tint=data['cor'])
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(LARGURA_TELA + 100, LARGURA_TELA + 500)
        self.rect.y = random.randrange(50, ALTURA_TELA - 50)
        self.velocidade = 3
        
    def update(self, *args):
        self.rect.x -= self.velocidade
        if self.rect.right < 0:
            self.kill()

# ----------------------------------------------------
# UI RENDERING FUNCTIONS
# ----------------------------------------------------
def mostrar_texto(superficie, texto, tamanho, x, y, cor=COR_BRANCA):
    fonte = pygame.font.Font(pygame.font.match_font('arial'), tamanho)
    texto_surface = fonte.render(texto, True, cor)
    texto_rect = texto_surface.get_rect(midtop=(x, y))
    superficie.blit(texto_surface, texto_rect)

def draw_health_bar(surf, x, y, pct, max_val, length, height=20):
    if pct < 0:
        pct = 0
    fill = (pct / max_val) * length
    outline_rect = pygame.Rect(x, y, length, height)
    fill_rect = pygame.Rect(x, y, fill, height)
    
    ratio = pct / max_val
    if ratio > 0.6:
        cor = (0, 255, 100)  # Sleek neon green
    elif ratio > 0.3:
        cor = (255, 200, 0)  # Warm orange-yellow
    else:
        cor = (255, 50, 50)  # Bright neon red
        
    # Draw dark background bar
    pygame.draw.rect(surf, (40, 40, 40), outline_rect)
    # Draw filled health
    pygame.draw.rect(surf, cor, fill_rect)
    # Draw white highlight outline
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)

def draw_charge_bar(surf, x, y, pct):
    if pct <= 0:
        return
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = pct * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    
    # Glow effect
    pygame.draw.rect(surf, (30, 30, 30), outline_rect)
    pygame.draw.rect(surf, (0, 160, 255), fill_rect)
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)

# ----------------------------------------------------
# SCREEN MENUS
# ----------------------------------------------------
async def tela_de_inicio(superficie, fundo, high_score):
    tocar_musica(CAMINHO_MUSICA_INTRO)
    superficie.blit(fundo, (0, 0))
    
    # Elegant title glow
    mostrar_texto(superficie, 'STAR BLASTER', 72, LARGURA_TELA / 2, ALTURA_TELA / 4, COR_AZUL)
    mostrar_texto(superficie, 'STAR BLASTER', 70, LARGURA_TELA / 2 - 2, ALTURA_TELA / 4 + 2, COR_BRANCA)
    
    mostrar_texto(superficie, 'Use as setas para mover | Segure ESPAÇO para carregar o Super Tiro', 22, LARGURA_TELA / 2, ALTURA_TELA / 2)
    mostrar_texto(superficie, f'Recorde: {high_score}', 28, LARGURA_TELA / 2, ALTURA_TELA * 3 / 4 - 45, COR_AMARELA)
    mostrar_texto(superficie, 'Pressione qualquer tecla para começar', 18, LARGURA_TELA / 2, ALTURA_TELA * 3 / 4)
    pygame.display.flip()
    
    aguardando = True
    while aguardando:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYUP:
                aguardando = False
        await asyncio.sleep(0)
                
    pygame.mixer.music.fadeout(500)
    return True

async def tela_final(superficie, fundo, pontuacao, high_score):
    tocar_musica(CAMINHO_MUSICA_INTRO)
    superficie.blit(fundo, (0, 0))
    
    mostrar_texto(superficie, 'Fim de Jogo!', 72, LARGURA_TELA / 2, ALTURA_TELA / 4, COR_VERMELHA)
    
    if pontuacao > high_score:
        mostrar_texto(superficie, 'NOVO RECORDE!', 35, LARGURA_TELA / 2, ALTURA_TELA / 2 - 50, COR_AMARELA)
        mostrar_texto(superficie, f'Sua Pontuação: {pontuacao}', 35, LARGURA_TELA / 2, ALTURA_TELA / 2)
    else:
        mostrar_texto(superficie, f'Sua Pontuação: {pontuacao}', 35, LARGURA_TELA / 2, ALTURA_TELA / 2 - 20)
        mostrar_texto(superficie, f'Recorde: {high_score}', 25, LARGURA_TELA / 2, ALTURA_TELA / 2 + 30, COR_CINZA_CLARO)
        
    mostrar_texto(superficie, 'Pressione qualquer tecla para fechar', 22, LARGURA_TELA / 2, ALTURA_TELA * 3 / 4)
    pygame.display.flip()
    
    aguardando = True
    while aguardando:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or evento.type == pygame.KEYUP:
                aguardando = False
        await asyncio.sleep(0)
                
    pygame.mixer.music.fadeout(500)

screen_shake = 0

def trigger_screen_shake(magnitude):
    global screen_shake
    screen_shake = magnitude

# ----------------------------------------------------
# MAIN GAME LOOP
# ----------------------------------------------------
async def game_loop(fundo_jogo, som_explosao, som_tiro_jogador, som_tiro_inimigo, som_powerup, current_boss_level, boss_spawn_score_trigger):
    global screen_shake
    trigger_screen_shake(0)
    
    if current_boss_level == 1:
        tocar_musica(CAMINHO_MUSICA_JOGO)
    elif current_boss_level == 2:
        tocar_musica(CAMINHO_MUSICA_FASE2)
    elif current_boss_level == 3:
        tocar_musica(CAMINHO_MUSICA_FASE3)
    else:
        music_cycle = [CAMINHO_MUSICA_JOGO, CAMINHO_MUSICA_FASE2, CAMINHO_MUSICA_FASE3]
        tocar_musica(music_cycle[(current_boss_level - 1) % len(music_cycle)])
        
    todos_sprites = pygame.sprite.Group()
    estrelas = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    super_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    boss_group = pygame.sprite.GroupSingle()
    
    for _ in range(200):
        estrela = Star()
        todos_sprites.add(estrela)
        estrelas.add(estrela)
        
    player = Player(todos_sprites, player_bullets, super_bullets, som_tiro_jogador)
    todos_sprites.add(player)
    
    for _ in range(8):
        enemy = Enemy(todos_sprites, enemy_bullets, som_tiro_inimigo, player)
        todos_sprites.add(enemy)
        enemies.add(enemy)
        
    pontuacao = 0
    combo_count = 1
    last_kill_time = 0
    
    powerup_spawn_timer = pygame.time.get_ticks()
    elite_spawn_timer = pygame.time.get_ticks()
    boss_active = False
    boss_warning_active = False
    boss_warning_start = 0
    
    rodando = True
    
    while rodando:
        clock.tick(FPS)
        now = pygame.time.get_ticks()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return pontuacao, 'quit', current_boss_level, boss_spawn_score_trigger
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    player.start_charging()
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_SPACE:
                    player.fire()
                    
        # Calculate difficulty scaling
        difficulty_multiplier = max(0.3, 1.0 - (pontuacao / 20000.0))
        
        # Spawners
        if not boss_active and not boss_warning_active:
            # PowerUps
            if now - powerup_spawn_timer > random.randint(8000, 15000):
                powerup_spawn_timer = now
                powerup = PowerUp()
                todos_sprites.add(powerup)
                powerups.add(powerup)
                
            # Elite enemies
            if now - elite_spawn_timer > random.randint(12000, 22000):
                elite_spawn_timer = now
                elite = Enemy(todos_sprites, enemy_bullets, som_tiro_inimigo, player, rank='elite')
                todos_sprites.add(elite)
                enemies.add(elite)
                
            # Boss warning trigger
            if pontuacao >= boss_spawn_score_trigger:
                boss_warning_active = True
                boss_warning_start = now
                pygame.mixer.music.fadeout(500)
                
        # Handle boss warning phase (dramatic freeze + flashing banner)
        if boss_warning_active:
            if now - boss_warning_start > 3000:  # 3 seconds warning
                boss_warning_active = False
                boss_active = True
                # Clean screen
                for enemy in list(enemies):
                    enemy.kill()
                # Spawn Boss
                boss = Boss(todos_sprites, enemy_bullets, som_tiro_inimigo, player, level=current_boss_level)
                todos_sprites.add(boss)
                boss_group.add(boss)
                tocar_musica(CAMINHO_MUSICA_CHEFE)
            else:
                # Update only stars to keep space moving
                estrelas.update()
                
                # Render screen shake
                render_offset = [0, 0]
                if (now // 100) % 2 == 0:  # Shake screen during warning!
                    render_offset[0] = random.randint(-3, 3)
                    render_offset[1] = random.randint(-3, 3)
                    
                tela.blit(fundo_jogo, render_offset)
                estrelas.draw(tela)
                
                # Draw player and thrusters static but animated
                for sprite in todos_sprites:
                    if isinstance(sprite, Player) or isinstance(sprite, Thruster):
                        tela.blit(sprite.image, (sprite.rect.x + render_offset[0], sprite.rect.y + render_offset[1]))
                        
                # Warning banner
                if (now // 250) % 2 == 0:
                    mostrar_texto(tela, "WARNING: BOSS DETECTED!", 48, LARGURA_TELA / 2, ALTURA_TELA / 2 - 50, COR_VERMELHA)
                    mostrar_texto(tela, "PREPARE TO FIGHT!", 24, LARGURA_TELA / 2, ALTURA_TELA / 2 + 10, COR_LARANJA)
                    
                pygame.display.flip()
                continue
                
        # Main updates
        todos_sprites.update(difficulty_multiplier)
        
        # --- COLLISIONS ---
        if not boss_active:
            # Player hits normal enemies
            hits_obstaculos = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask)
            for hit in hits_obstaculos:
                player.take_damage(25)
                # Respawn replacement enemy
                enemy = Enemy(todos_sprites, enemy_bullets, som_tiro_inimigo, player)
                todos_sprites.add(enemy)
                enemies.add(enemy)
                
        # Player hits enemy bullets
        hits_tiros = pygame.sprite.spritecollide(player, enemy_bullets, True, pygame.sprite.collide_mask)
        for hit in hits_tiros:
            player.take_damage(10)
            
        if not player.alive():
            if som_explosao:
                som_explosao.play()
            pygame.mixer.music.stop()
            return pontuacao, 'died', current_boss_level, boss_spawn_score_trigger
            
        # Player bullets hit enemies
        hits = pygame.sprite.groupcollide(enemies, player_bullets, False, True)
        for enemy_hit in hits:
            gained = enemy_hit.take_damage(100)
            if gained > 0:
                # Combo tracking
                if now - last_kill_time < 2000:
                    combo_count += 1
                else:
                    combo_count = 1
                last_kill_time = now
                pontuacao += gained * combo_count
                
        # Super bullets hit enemies (Super bullet survives)
        hits = pygame.sprite.groupcollide(enemies, super_bullets, False, False)
        for enemy_hit in hits:
            gained = enemy_hit.take_damage(200)
            if gained > 0:
                if now - last_kill_time < 2000:
                    combo_count += 1
                else:
                    combo_count = 1
                last_kill_time = now
                pontuacao += gained * combo_count
                
        # Boss collisions
        if boss_active and boss_group.sprite:
            boss = boss_group.sprite
            # Player hits Boss
            if pygame.sprite.spritecollide(player, boss_group, False, pygame.sprite.collide_mask):
                player.take_damage(50)
                
            # Player bullets hit Boss
            if pygame.sprite.groupcollide(boss_group, player_bullets, False, True):
                gained = boss.take_damage(100)
                if gained > 0:
                    pontuacao += gained
                    
            # Super bullets hit Boss
            if pygame.sprite.groupcollide(boss_group, super_bullets, False, False):
                gained = boss.take_damage(200)
                if gained > 0:
                    pontuacao += gained
                    
            if not boss.alive():
                boss_active = False
                current_boss_level += 1
                boss_spawn_score_trigger += 7500
                pygame.mixer.music.fadeout(500)
                return pontuacao, 'boss_defeated', current_boss_level, boss_spawn_score_trigger
                
        # Player collects powerups
        colisoes_powerup = pygame.sprite.spritecollide(player, powerups, True)
        for powerup in colisoes_powerup:
            player.activate_powerup(powerup.type)
            if som_powerup:
                som_powerup.play()
                
        # --- SCREEN SHAKE OFFSET ---
        render_offset = [0, 0]
        if screen_shake > 0:
            screen_shake -= 1
            render_offset[0] = random.randint(-4, 4)
            render_offset[1] = random.randint(-4, 4)
            
        # --- RENDERING ---
        tela.blit(fundo_jogo, render_offset)
        estrelas.draw(tela)
        
        # Draw all sprites EXCEPT stars (so stars stay in parallax background)
        for sprite in todos_sprites:
            if not isinstance(sprite, Star) and not isinstance(sprite, Particle):
                tela.blit(sprite.image, (sprite.rect.x + render_offset[0], sprite.rect.y + render_offset[1]))
                
        # Update and draw particles separately to handle transparency
        for sprite in todos_sprites:
            if isinstance(sprite, Particle):
                tela.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
                
        player.draw_shield(tela)
        
        # HUD Text & Bars
        mostrar_texto(tela, f'Pontuação: {pontuacao}', 22, LARGURA_TELA / 2, 10)
        draw_health_bar(tela, 10, 10, player.health, player.max_health, 150)
        
        # Display Combo
        if combo_count > 1 and now - last_kill_time < 2000:
            # Pulsing color scale
            pulse = int((math.sin(now / 100) + 1) * 30)
            combo_color = (255, 150 + pulse, 50)
            mostrar_texto(tela, f'COMBO x{combo_count}!', 26, 180, 10, combo_color)
            
        # Boss Health Bar
        if boss_active and boss_group.sprite:
            boss = boss_group.sprite
            mostrar_texto(tela, "CHEFE", 18, LARGURA_TELA / 2, 40, COR_VERMELHA)
            draw_health_bar(tela, LARGURA_TELA / 2 - 150, 65, boss.health, boss.max_health, length=300)
            
        pygame.display.flip()
        await asyncio.sleep(0)

# ----------------------------------------------------
# MAIN INITIALIZATION ENTRYPOINT
# ----------------------------------------------------
async def main():
    fundo_intro = carregar_imagem('space.jpg', CAMINHO_IMAGENS, escalar=(LARGURA_TELA, ALTURA_TELA))
    fundos_jogo = [
        carregar_imagem('bkg1.png', CAMINHO_IMAGENS, escalar=(LARGURA_TELA, ALTURA_TELA), escurecer=100),
        carregar_imagem('bkg2.png', CAMINHO_IMAGENS, escalar=(LARGURA_TELA, ALTURA_TELA), escurecer=100),
        carregar_imagem('bkg3.png', CAMINHO_IMAGENS, escalar=(LARGURA_TELA, ALTURA_TELA), escurecer=100)
    ]
    som_explosao = carregar_som(CAMINHO_SOM_EXPLOSAO)
    som_tiro_jogador = carregar_som(CAMINHO_SOM_TIRO_JOGADOR)
    som_tiro_inimigo = carregar_som(CAMINHO_SOM_TIRO_INIMIGO)
    som_powerup = carregar_som(CAMINHO_SOM_POWERUP)
    
    high_score = carregar_high_score()
    current_phase_index = 0
    current_boss_level_id = 1
    boss_spawn_score_trigger = 5000
    
    while True:
        fundo_jogo_atual = fundos_jogo[current_phase_index]
        if not await tela_de_inicio(tela, fundo_intro, high_score):
            break
            
        pontuacao_atual, game_status, current_boss_level_id, boss_spawn_score_trigger = await game_loop(
            fundo_jogo_atual, som_explosao, som_tiro_jogador, som_tiro_inimigo, som_powerup,
            current_boss_level_id, boss_spawn_score_trigger
        )
        
        if game_status == 'quit':
            break
            
        if pontuacao_atual > high_score:
            high_score = pontuacao_atual
            salvar_high_score(high_score)
            
        if game_status == 'boss_defeated':
            current_phase_index = (current_phase_index + 1) % len(fundos_jogo)
        else:
            await tela_final(tela, fundo_intro, pontuacao_atual, high_score)
            
        await asyncio.sleep(0)
            
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    asyncio.run(main())
