import pygame, sys
pygame.init()

# Tela
telaL = 1120
telaA = 630
janela = pygame.display.set_mode((telaL, telaA))
pygame.display.set_caption("Joguinho!")
clock = pygame.time.Clock()

# Fase
faseL  = 3360
faseA = 630

# Imagens
playerImg = pygame.image.load("imagens/player.png")
plataformaImg = pygame.image.load("imagens/plataforma1.png")
coracaoImg = pygame.image.load("imagens/vida.png")
inimigo1 = pygame.image.load("imagens/inimigo1.png")
bolha = pygame.image.load("imagens/bolhas1.png")

# Velocidade e gravidade
velocidade = 5
gravidade = 1
forca_pulo = 20
vidasIniciais = 3
pontuacao = 0

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)
VERDE_CLARO = (0, 255, 0)
AZUL = (0, 0, 200)
AZUL_CLARO = (0, 0, 255)
VERMELHO = (200, 0, 0)
VERMELHO_CLARO = (255, 0, 0)

# Fonte
font = pygame.font.Font(None, 60)

def desenhar_texto(texto, fonte, cor, surface, x, y):
    texto_obj = fonte.render(texto, True, cor)
    surface.blit(texto_obj, (x, y))

def menu_inicial():
    rodando_menu = True
    while rodando_menu:
        janela.fill(BRANCO)

        # Botões
        botao_jogar = pygame.Rect(telaL//2 - 100, 200, 200, 60)
        botao_opcoes = pygame.Rect(telaL//2 - 100, 300, 200, 60)
        botao_sair = pygame.Rect(telaL//2 - 100, 400, 200, 60)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Jogar
        if botao_jogar.collidepoint(mouse_pos):
            pygame.draw.rect(janela, VERDE_CLARO, botao_jogar)
            if mouse_click[0]:
                rodando_menu = False
        else:
            pygame.draw.rect(janela, VERDE, botao_jogar)
        desenhar_texto("JOGAR", font, PRETO, janela, telaL//2 - 50, 210)

        # Opções
        if botao_opcoes.collidepoint(mouse_pos):
            pygame.draw.rect(janela, AZUL_CLARO, botao_opcoes)
            if mouse_click[0]:
                print("Botão OPÇÕES clicado!")
        else:
            pygame.draw.rect(janela, AZUL, botao_opcoes)
        desenhar_texto("OPÇÕES", font, PRETO, janela, telaL//2 - 60, 310)

        # Sair
        if botao_sair.collidepoint(mouse_pos):
            pygame.draw.rect(janela, VERMELHO_CLARO, botao_sair)
            if mouse_click[0]:
                pygame.quit()
                sys.exit()
        else:
            pygame.draw.rect(janela, VERMELHO, botao_sair)
        desenhar_texto("SAIR", font, PRETO, janela, telaL//2 - 40, 410)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

# Chama o menu antes do jogo
menu_inicial()


class Player():
    def __init__(self):
        self.img = playerImg
        self.largura = self.img.get_width()
        self.altura = self.img.get_height()
        self.x = 100
        self.y = faseA - self.altura - 50  # perto do chão
        self.vel_y = 0
        self.no_chao = False
        self.vidas = vidasIniciais

    def andarEsquerda(self):
        self.x -= velocidade
        if self.x < 0:
            self.x = 0

    def andarDireita(self):
        self.x += velocidade
        if self.x + self.largura > faseL:  # usar tamanho da fase
            self.x = faseL - self.largura

    def pula(self):
        if self.no_chao:
            self.vel_y = -forca_pulo
            self.no_chao = False

    def aplicarGravidade(self, plataformas):
        self.vel_y += gravidade
        self.y += self.vel_y
        self.no_chao = False

        for plat in plataformas:
            if self.x + self.largura > plat.x and self.x < plat.x + plat.largura:
                if self.y + self.altura >= plat.y and self.y + self.altura - self.vel_y <= plat.y:
                    self.y = plat.y - self.altura
                    self.vel_y = 0
                    self.no_chao = True

        if self.y + self.altura >= faseA:
            self.y = faseA - self.altura
            self.vel_y = 0
            self.no_chao = True

    def colisaoInimigo(self, inimigos):
        for inimigo in inimigos:
            if (self.x + self.largura > inimigo.x and self.x < inimigo.x + inimigo.largura and
                self.y + self.altura > inimigo.y and self.y < inimigo.y + inimigo.altura):
                self.vidas -= 1
                print(f"Vida perdida! Vidas restantes: {self.vidas}")
                inimigos.remove(inimigo)
                if self.vidas <= 0:
                    print("Game Over!")

    def desenharPlayer(self, cameraX):
        janela.blit(self.img, (self.x - cameraX, self.y))

    def desenharVidas(self):
        for i in range(self.vidas):
            janela.blit(coracaoImg, (20 + i * (coracaoImg.get_width() + 5), 20))


class Plataforma():
    def __init__(self, x, y):
        self.img = plataformaImg
        self.largura = self.img.get_width()
        self.altura = self.img.get_height()
        self.x = x
        self.y = y

    def desenharPlat(self, cameraX):
        janela.blit(self.img, (self.x - cameraX, self.y))


class Inimigo():
    def __init__(self, x, y):
        self.img = inimigo1
        self.largura = self.img.get_width()
        self.altura = self.img.get_height()
        self.x = x
        self.y = y

    def desenharInimigo(self, cameraX):
        janela.blit(self.img, (self.x - cameraX, self.y))


class Bolhas():
    def __init__(self, x, y):
        self.img = bolha
        self.largura = self.img.get_width()
        self.altura = self.img.get_height()
        self.x = x
        self.y = y

    def desenharBolhas(self, cameraX):
        janela.blit(self.img, (self.x - cameraX, self.y))


# Criar player
player = Player()

# Criar múltiplas plataformas
plataformas = [
    Plataforma(310, 464),
    Plataforma(648, 428),
    Plataforma(810, 428),
    Plataforma(992, 345),
    Plataforma(1190, 280),
    Plataforma(1350, 280),
    Plataforma(1540, 235),
    Plataforma(1700, 235),
    Plataforma(1420, 487),
    Plataforma(1870, 465),
    Plataforma(2043, 550),
    Plataforma(2221, 470),
    Plataforma(2400, 380),
    Plataforma(2600, 300),
    Plataforma(2780, 235),
    Plataforma(2950, 235),
    Plataforma(3135, 308),

]

inimigos = [
    Inimigo(300, 600),
    Inimigo(600, 600),
    Inimigo(950, 600)
]

bolhas = [
    Bolhas(300, 400),
    Bolhas(600, 400),
    Bolhas(950, 400)
]

rodando = True
while rodando:
    clock.tick(60)
    eventos = pygame.event.get()

    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        player.andarEsquerda()
    if teclas[pygame.K_RIGHT]:
        player.andarDireita()
    if teclas[pygame.K_UP]:
        player.pula()

    player.aplicarGravidade(plataformas)
    player.colisaoInimigo(inimigos)

    # Câmera para seguir o player
    cameraX = player.x - telaL // 2
    cameraX = max(0, min(cameraX, faseL - telaL))

    # Fundo
    janela.fill((255,247,231))


    # Plataformas
    for plat in plataformas:
        plat.desenharPlat(cameraX)

    # Player
    player.desenharPlayer(cameraX)

    # Inimigos
    for inimigo in inimigos:
        inimigo.desenharInimigo(cameraX)

    # Bolhas
    for b in bolhas[:]:
        if (player.x + player.largura > b.x and player.x < b.x + b.largura and
            player.y + player.altura > b.y and player.y < b.y + b.altura):
            bolhas.remove(b)
            print("Bolha coletada!")
        else:
            b.desenharBolhas(cameraX)

    # Vidas
    player.desenharVidas()

    pygame.display.update()

pygame.quit()