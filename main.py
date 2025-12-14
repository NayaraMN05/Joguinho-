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
porta = pygame.image.load("imagens/porta.png")
livro = pygame.image.load("imagens/livro.png")
estrela = pygame.image.load("imagens/estrela.png")
"""ADICIONAR:
BtnJogar = pygame.image.load("imagens/jogar.png")
BtnSair = pygame.image.load("imagens/sair.png")
BtnSoundOn = pygame.image.load("imagens/soundon.png")
BtnSoun = pygame.image.load("imagens/soundoff.png")
"""
# Velocidade e gravidade
velocidade = 5
gravidade = 1
forca_pulo = 20
nivel_atual = 0

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)
VERDE_CLARO = (0, 255, 0)
AZUL = (0, 0, 200)
AZUL_CLARO = (0, 0, 255)
VERMELHO = (200, 0, 0)
VERMELHO_CLARO = (255, 0, 0)

# Fonte
fonte = pygame.font.Font(None, 60)

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
        desenhar_texto("JOGAR", fonte, PRETO, janela, telaL//2 - 50, 210)

        # Opções
        if botao_opcoes.collidepoint(mouse_pos):
            pygame.draw.rect(janela, AZUL_CLARO, botao_opcoes)
            if mouse_click[0]:
                print("Botão OPÇÕES clicado!")
        else:
            pygame.draw.rect(janela, AZUL, botao_opcoes)
        desenhar_texto("OPÇÕES", fonte, PRETO, janela, telaL//2 - 60, 310)

        # Sair
        if botao_sair.collidepoint(mouse_pos):
            pygame.draw.rect(janela, VERMELHO_CLARO, botao_sair)
            if mouse_click[0]:
                pygame.quit()
                sys.exit()
        else:
            pygame.draw.rect(janela, VERMELHO, botao_sair)
        desenhar_texto("SAIR", fonte, PRETO, janela, telaL//2 - 40, 410)

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
        self.y = faseA - self.altura - 50
        self.vel_y = 0
        self.no_chao = False
        self.vidas = 3
        self.pontuacao = 0

    def andarEsquerda(self):
        self.x -= velocidade
        if self.x < 0:
            self.x = 0

    def andarDireita(self):
        self.x += velocidade
        if self.x + self.largura > faseL:
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

    def desenharPontuacao(self):
        texto_pontuacao = f"Pontuação: {self.pontuacao}"
        desenhar_texto(texto_pontuacao, fonte, PRETO, janela, 20, 80)

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

class Porta():
    def __init__(self, x, y):
        self.img = porta
        self.largura = self.img.get_width()
        self.altura = self.img.get_height()
        self.x = x
        self.y = y
        self.ativa = True

    def desenharPorta(self, cameraX):
        if self.ativa:
            janela.blit(self.img, (self.x - cameraX, self.y))

    def colisao(self, player):
        if (player.x + player.largura > self.x and player.x < self.x + self.largura and
            player.y + player.altura > self.y and player.y < self.y + self.altura):
            return True
        return False

class Bolhas():
    def __init__(self, x, y):
        self.img = bolha
        self.largura = self.img.get_width()
        self.altura = self.img.get_height()
        self.x = x
        self.y = y

    def desenharBolhas(self, cameraX):
        janela.blit(self.img, (self.x - cameraX, self.y))

fases = [
    {
        "plataformas": [
            Plataforma(310, 464), Plataforma(648, 428), Plataforma(810, 428),
            Plataforma(992, 345), Plataforma(1190, 280), Plataforma(1350, 280),
            Plataforma(1540, 235), Plataforma(1700, 235), Plataforma(1420, 487),
            Plataforma(1870, 465), Plataforma(2043, 550), Plataforma(2221, 470),
            Plataforma(2400, 380), Plataforma(2600, 300), Plataforma(2780, 235),
            Plataforma(2950, 235), Plataforma(3135, 308),
        ],
        "inimigos": [(300, 600), (600, 600), (950, 600)],
        "bolhas": [(300, 400), (600, 400), (950, 400)],
        "porta": (3170, 200),
        "faseL": 3360,
        "vidasIniciais": 3
    },
    {
        "plataformas": [
            Plataforma(334, 521), Plataforma(523, 463), Plataforma(688, 463),
            Plataforma(839, 525), Plataforma(1004, 525), Plataforma(1183, 468),
            Plataforma(1348, 468), Plataforma(1512, 392), Plataforma(1678, 392),
            Plataforma(2042, 420), Plataforma(2230, 348), Plataforma(2464, 490),
            Plataforma(2645, 457), Plataforma(2820, 396), Plataforma(2969, 464)
        ],
        "inimigos": [(724, 388), (946, 554), (1927, 554)],
        "bolhas": [(1308, 581), (1744, 324), (2848, 294)],
        "porta": (3200, 500),
        "faseL": 3360,
        "vidasIniciais": 3
    },
    {
        "plataformas": [
            Plataforma(284, 473), Plataforma(446, 473), Plataforma(634, 473),
            Plataforma(799, 307), Plataforma(973, 471), Plataforma(1116, 276),
            Plataforma(1304, 396), Plataforma(1487, 342), Plataforma(1649, 342),
            Plataforma(1916, 220), Plataforma(1916, 475), Plataforma(2223, 366),
            Plataforma(2404, 313), Plataforma(2564, 252), Plataforma(2868, 410),
            Plataforma(3145, 221)
        ],
        "inimigos": [(1026, 554), (1340, 322), (2970, 554)],
        "bolhas": [(1350, 51), (1951, 53), (3189, 46)],
        "porta": (3200, 500),
        "faseL": 3360,
        "vidasIniciais": 3
    }
]

def carregarFase(nivel):
    global plataformas, bolhas, porta_checkpoint, faseL, totalEstrelas, inimigos
    fase = fases[nivel]
    plataformas = fase["plataformas"]
    bolhas = [Bolhas(x, y) for x, y in fase["bolhas"]]
    inimigos = [Inimigo(x, y) for x, y in fase["inimigos"]]
    porta_checkpoint = Porta(*fase["porta"])
    faseL = fase["faseL"]
    totalEstrelas = len(fase["bolhas"])

    # Resetar player sem alterar vidas
    player.x = 100
    player.y = faseA - player.altura - 50

def reiniciar_jogo():
    global nivel_atual, player
    nivel_atual = 0
    player = Player()  # Recria player e reseta vidas/pontuação

    # Recria a fase e os inimigos/bolhas do nível inicial
    carregarFase(nivel_atual)

def tela_pontuacao():
    mostrando = True
    while mostrando:
        janela.fill(BRANCO)

        # Mostrar estrelas
        if totalEstrelas > 0:
            bolhasColetadas = totalEstrelas - len(bolhas) # número de bolhas coletadas
            estrelasFinais = int(round((bolhasColetadas / totalEstrelas *3))) 
            for i in range(estrelasFinais):
                janela.blit(estrela, (400 + i * (estrela.get_width() + 10), 300))

        desenhar_texto(f"Atributos: {player.pontuacao}", fonte, PRETO, janela, 400, 200)
        
        # Botão continuar
        botao_continuar = pygame.Rect(telaL//2 - 100, 400, 200, 60)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if botao_continuar.collidepoint(mouse_pos):
            pygame.draw.rect(janela, VERDE_CLARO, botao_continuar)
            if mouse_click[0]:
                mostrando = False
        else:
            pygame.draw.rect(janela, VERDE, botao_continuar)

        desenhar_texto("CONTINUAR", fonte, PRETO, janela, telaL//2 - 80, 410)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()
        clock.tick(60)

def tela_game_over():
    rodando_game_over = True
    while rodando_game_over:
        janela.fill(PRETO)
        desenhar_texto("GAME OVER", fonte, VERMELHO_CLARO, janela, telaL//2 - 150, 200)

        # Botão Reiniciar
        botao_reiniciar = pygame.Rect(telaL//2 - 100, 300, 200, 60)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if botao_reiniciar.collidepoint(mouse_pos):
            pygame.draw.rect(janela, VERDE_CLARO, botao_reiniciar)
            if mouse_click[0]:
                rodando_game_over = False
                reiniciar_jogo()  # Reinicia o jogo
        else:
            pygame.draw.rect(janela, VERDE, botao_reiniciar)
        desenhar_texto("REINICIAR", fonte, PRETO, janela, telaL//2 - 80, 310)

        # Botão Sair
        botao_sair = pygame.Rect(telaL//2 - 100, 400, 200, 60)
        if botao_sair.collidepoint(mouse_pos):
            pygame.draw.rect(janela, VERMELHO_CLARO, botao_sair)
            if mouse_click[0]:
                pygame.quit()
                sys.exit()
        else:
            pygame.draw.rect(janela, VERMELHO, botao_sair)
        desenhar_texto("SAIR", fonte, PRETO, janela, telaL//2 - 40, 410)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

# Criar player
player = Player()
carregarFase(nivel_atual)

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

    cameraX = player.x - telaL // 2
    cameraX = max(0, min(cameraX, faseL - telaL))

    if player.vidas <= 0:
        tela_game_over()
        continue

    # Fundo
    janela.fill((255, 247, 231))

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
            player.pontuacao += 10
            print("Bolha coletada! Pontuação:", player.pontuacao)
        else:
            b.desenharBolhas(cameraX)

    # Porta
    porta_checkpoint.desenharPorta(cameraX)
    if porta_checkpoint.colisao(player):
        print("Checkpoint atingido! Mostrando pontuação...")
        tela_pontuacao()  # mostra tela de pontuação
        nivel_atual += 1
        if nivel_atual < len(fases):
            carregarFase(nivel_atual)
            # Resetar posição do player sem alterar vidas
            player.x = 100
            player.y = faseA - player.altura - 50
        else:
            print("Parabéns! Você terminou o jogo!")
            pygame.quit()
            sys.exit()

    # Vidas
    player.desenharVidas()

    pygame.display.update()

pygame.quit()
