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
plataformaImg = pygame.image.load("imagens/plataforma1.png")
coracaoImg = pygame.image.load("imagens/vida.png")
inimigo1 = pygame.image.load("imagens/inimigo1.png")
bolha = pygame.image.load("imagens/bolhas1.png")
porta = pygame.image.load("imagens/porta.png")
livro = pygame.image.load("imagens/livro.png")
estrela = pygame.image.load("imagens/estrela.png")
charwalk1 = pygame.image.load("imagens/charwalk1.png")
charwalk1 = pygame.transform.scale(charwalk1, (80, 40))
charwalk2 = pygame.image.load("imagens/charwalk2.png")
charwalk2 = pygame.transform.scale(charwalk2, (80, 40))

# Botões
BtnJogar = pygame.image.load("imagens/Btnjogar.png")
BtnSair = pygame.image.load("imagens/Btnsair.png")
BtnSoundOn = pygame.image.load("imagens/BtnsoundOn.png")
BtnSoundOff = pygame.image.load("imagens/BtnsoundOff.png")
logo = pygame.image.load("imagens/Btnlogostudio.png")

# Músicas de Fases
musicas_fases = [
    "sound/fase1.wav",
    "sound/fase2.wav",
    "sound/fase3.wav"
]
# Som
somBolhas = pygame.mixer.Sound("sound/Bolhas.wav")
somgameover = pygame.mixer.Sound("sound/GameOver.wav")
somlixo = pygame.mixer.Sound("sound/Lixo.wav")
somMenu = "sound/menu.wav"
somwin = pygame.mixer.Sound("sound/win.wav")

# Velocidade e gravidade
velocidade = 5
gravidade = 1
forca_pulo = 20
nivel_atual = 0
bolhasTotal = 0
som_ativo = True

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

# Fases
fases = [
    {
        "plataformas": [
            (310, 464), (648, 428), (810, 428),
            (992, 345), (1190, 280), (1350, 280),
            (1540, 235), (1700, 235), (1420, 487),
            (1870, 465), (2043, 550), (2221, 470),
            (2400, 380), (2600, 300), (2780, 235),
            (2950, 235), (3135, 308),
        ],
        "inimigos": [(300, 600), (600, 600), (950, 600)],
        "bolhas": [(300, 400), (600, 400), (950, 400)],
        "porta": (3170, 200),
        "faseL": 3360,
        "vidasIniciais": 3
    },
    {
        "plataformas": [
            (334, 521), (523, 463), (688, 463),
            (839, 525), (1004, 525), (1183, 468),
            (1348, 468), (1512, 392), (1678, 392),
            (2042, 420), (2230, 348), (2464, 490),
            (2645, 457), (2820, 396), (2969, 464)
        ],
        "inimigos": [(724, 388), (946, 554), (1927, 554)],
        "bolhas": [(1308, 581), (1744, 324), (2848, 294)],
        "porta": (3200, 500),
        "faseL": 3360,
        "vidasIniciais": 3
    },
    {
        "plataformas": [
            (284, 473), (446, 473), (634, 473),
            (799, 307), (973, 471), (1116, 276),
            (1304, 396), (1487, 342), (1649, 342),
            (1916, 220), (1916, 475), (2223, 366),
            (2404, 313), (2564, 252), (2868, 410),
            (3145, 221)
        ],
        "inimigos": [(1026, 554), (1340, 322), (2970, 554)],
        "bolhas": [(1350, 51), (1951, 53), (3189, 46)],
        "porta": (3200, 500),
        "faseL": 3360,
        "vidasIniciais": 3
    }
]

def musicas(nivel):
    if som_ativo:
        pygame.mixer.music.load(musicas_fases[nivel])
        pygame.mixer.music.play(-1)  # loop infinito

def tocar_musica(caminho):
    if som_ativo:
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.play(-1)

def parar_musica():
    pygame.mixer.music.stop()

def desenhar_texto(texto, fonte, cor, surface, x, y):
    texto_obj = fonte.render(texto, True, cor)
    surface.blit(texto_obj, (x, y))

def cutscene_texto(cena):
    """
    cena: "inicio", "vencer", "gameover"
    """
    if cena == "inicio":
        linhas = [
            "Minha nova missão: encontrar uma companhia para minha jornada.",
            "Todos os anos eu e meus colegas Uças vamos a procura de construir um legado.",
            "Encontrar um parceiro para dar vida às novas gerações é a nossa nova missão de vida.",
            "Mas nem tudo é tão fácil, precisamos conquistar nossos pretendentes.",
            "Vou colecionar Atributos para impressionar alguém!"
        ]
    elif cena == "vencer":
        linhas = [
            "Ufa! Finalmente chegamos ao final da jornada.",
            "Será que consegui conquistar alguém?",
            "Uau, você tem uma bela coleção!",
            "Parabéns! Você venceu!"
        ]
    elif cena == "gameover":
        linhas = [
            "Oh não! Você perdeu todas as vidas.",
            "A missão falhou...",
            "Mas não desista, tente novamente!"
        ]
    else:
        return  # cena inválida

    indice = 0
    esperando = True
    while esperando:
        janela.fill(BRANCO if cena != "gameover" else PRETO)

        # Mostrar a linha atual
        desenhar_texto(linhas[indice], fonte, PRETO if cena != "gameover" else VERMELHO_CLARO, janela, 100, telaA//2 - 30)
        desenhar_texto("Pressione ESPAÇO para continuar", pygame.font.Font(None, 40),
                       PRETO if cena != "gameover" else VERMELHO_CLARO, janela, 100, telaA//2 + 40)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    indice += 1
                    if indice >= len(linhas):
                        esperando = False

        pygame.display.update()
        clock.tick(60)

def menu_inicial():
    global som_ativo
    tocar_musica(somMenu)

    BtnL = 300
    BtnA = 150

    # Redimensionando Botões
    BtnJogarImg =  pygame.transform.scale(BtnJogar, (BtnL, BtnA))
    BtnsounOnImg = pygame.transform.scale(BtnSoundOn, (BtnL, BtnA))
    BtnsounOffImg = pygame.transform.scale(BtnSoundOff, (BtnL, BtnA))
    BtnSairImg =  pygame.transform.scale(BtnSair, (380, 200))
    logoImg = pygame.transform.scale(logo, (150, 150))

    # Posição dos botões
    posLogo = (telaL//2 - logoImg.get_width()//0.35, 100)
    posJogar = (telaL//2 - BtnJogarImg.get_width()//0.585, 255)
    posSair = (telaL//2 - BtnSairImg.get_width()//0.7, 275)
    posSomOn = (telaL//2 - BtnsounOnImg.get_width()//0.55, 345)
    posSomOff = (telaL//2 - BtnsounOffImg.get_width()//0.55, 345)
    
    # Máscaras para clique pixel-perfect
    BtnJogarMask = pygame.mask.from_surface(BtnJogarImg)
    BtnSairMask = pygame.mask.from_surface(BtnSairImg)
    BtnsoundOnMask = pygame.mask.from_surface(BtnsounOnImg)
    BtnsoundOffMask = pygame.mask.from_surface(BtnsounOffImg)
    
    mouse_pos = None
    rodando_menu = True

    # Função auxiliar para checar clique na máscara
    def clicou_em_mask(mask, pos_elemento,  clique_pos):
        if clique_pos is None:
            return 0

        x = clique_pos[0] - pos_elemento[0]
        y = clique_pos[1] - pos_elemento[1]

        if 0 <= x < mask.get_size()[0] and 0 <= y < mask.get_size()[1]:
            return mask.get_at((x, y))
        return 0

    while rodando_menu:
        janela.fill(BRANCO)
        janela.blit(logoImg, posLogo)
        janela.blit(BtnJogarImg, posJogar)
        janela.blit(BtnSairImg, posSair)

        # Desenha botão de som conforme estado
        if som_ativo:
            janela.blit(BtnsounOnImg, posSomOn)
        else:
            janela.blit(BtnsounOffImg, posSomOff)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_pos = evento.pos  # guarda posição do clique

                # BOTÃO JOGAR
                if clicou_em_mask(BtnJogarMask, posJogar, mouse_pos):
                    parar_musica()
                    cutscene_texto("inicio")
                    rodando_menu = False

                # BOTÃO SAIR
                elif clicou_em_mask(BtnSairMask, posSair, mouse_pos):
                    pygame.quit()
                    sys.exit()

                # BOTÃO SOM
                elif som_ativo and clicou_em_mask(BtnsoundOnMask, posSomOn, mouse_pos):
                    som_ativo = False
                    parar_musica()
                    pygame.mixer.stop()

                elif not som_ativo and clicou_em_mask(BtnsoundOffMask, posSomOff, mouse_pos):
                    som_ativo = True
                    tocar_musica(somMenu)

            elif som_ativo and clicou_em_mask(BtnsoundOnMask, posSomOn, mouse_pos):
                som_ativo = False
                parar_musica()
                pygame.mixer.stop()

            elif not som_ativo and clicou_em_mask(BtnsoundOffMask, posSomOff, mouse_pos):
                som_ativo = True
                tocar_musica(somMenu)
            mouse_pos = None   

        pygame.display.update()
        clock.tick(60)

# Chama o menu antes do jogo
menu_inicial()

class Player():
    def __init__(self):
        self.img1 = charwalk1
        self.img2 = charwalk2
        self.img = self.img1 # A imagem inicial é a charwalk1
        self.largura = self.img.get_width()
        self.altura = self.img.get_height()
        self.x = 100
        self.y = faseA - self.altura - 50
        self.vel_y = 0
        self.no_chao = False
        self.vidas = 3
        self.pontuacao = 0
        self.animacao_anda = 0

    def andarEsquerda(self):
        self.x -= velocidade
        if self.x < 0:
            self.x = 0
        
        # Alterna entre as imagens de animação ao andar para a esquerda
        self.animacao_anda += 1
        if self.animacao_anda % 10 == 0:  # Troca a cada 10 frames
            self.img = self.img2 if self.img == self.img1 else self.img1

    def andarDireita(self):
        self.x += velocidade
        if self.x + self.largura > faseL:
            self.x = faseL - self.largura

        # Alterna entre as imagens de animação ao andar para a direita
        self.animacao_anda += 1
        if self.animacao_anda % 10 == 0:  # Troca a cada 10 frames
            self.img = self.img2 if self.img == self.img1 else self.img1

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
        for inimigo in inimigos[:]:
            if (self.x + self.largura > inimigo.x and self.x < inimigo.x + inimigo.largura and
                self.y + self.altura > inimigo.y and self.y < inimigo.y + inimigo.altura):
                self.vidas -= 1

                if som_ativo:
                    somlixo.play()
                    somlixo.set_volume(0.6)
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

# ------------------- Funções de fase e jogo -------------------

def carregarFase(nivel):
    global plataformas, bolhas, porta_checkpoint, faseL, totalEstrelas, inimigos
    fase = fases[nivel]
    plataformas = [Plataforma(x, y) for x, y in fase["plataformas"]]
    bolhas = [Bolhas(x, y) for x, y in fase["bolhas"]]
    inimigos = [Inimigo(x, y) for x, y in fase["inimigos"]]
    porta_checkpoint = Porta(*fase["porta"])
    faseL = fase["faseL"]
    totalEstrelas = len(fase["bolhas"])

    # Resetar player sem alterar vidas
    player.x = 100
    player.y = faseA - player.altura - 50

    pygame.mixer.music.stop() # Para música anterior
    musicas(nivel)
    
    
def reiniciar_jogo():
    global nivel_atual, player
    nivel_atual = 0
    player = Player()  # Recria player e reseta vidas/pontuação
    carregarFase(nivel_atual)

def tela_pontuacao():
    mostrando = True
    while mostrando:
        janela.fill(BRANCO)

        # Mostrar estrelas
        if totalEstrelas > 0:
            bolhasColetadas = totalEstrelas - len(bolhas)
            estrelasFinais = int(round((bolhasColetadas / totalEstrelas *3))) 
            for i in range(estrelasFinais):
                janela.blit(estrela, (400 + i * (estrela.get_width() + 10), 300))

        desenhar_texto(f"Atributos: {player.pontuacao}", fonte, PRETO, janela, 400, 200)

        # Botão continuar
        botao_continuar = pygame.Rect(telaL//2 - 100, 400, 200, 60)
        mouse_pos = pygame.mouse.get_pos()
        if botao_continuar.collidepoint(mouse_pos):
            pygame.draw.rect(janela, VERDE_CLARO, botao_continuar)
        else:
            pygame.draw.rect(janela, VERDE, botao_continuar)
        desenhar_texto("CONTINUAR", fonte, PRETO, janela, telaL//2 - 80, 410)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_continuar.collidepoint(evento.pos):
                    mostrando = False

        pygame.display.update()
        clock.tick(60)

def tela_game_over():
    # Parar música ao perder todas as vidas 
    pygame.mixer.music.stop()

    if som_ativo:
        somgameover.play()

    # CUTSCENE roda uma única vez
    cutscene_texto("gameover")

    rodando_game_over = True
    while rodando_game_over:
        janela.fill(PRETO)
        desenhar_texto("GAME OVER", fonte, VERMELHO_CLARO, janela, telaL//2 - 150, 200)

        # Botão Reiniciar
        botao_reiniciar = pygame.Rect(telaL//2 - 100, 300, 200, 60)
       
       # Botão Sair
        botao_sair = pygame.Rect(telaL//2 - 100, 400, 200, 60)

        mouse_pos = pygame.mouse.get_pos()

        # Botão Reiniciar
        if botao_reiniciar.collidepoint(mouse_pos):
            pygame.draw.rect(janela, VERDE_CLARO, botao_reiniciar)
        else:
            pygame.draw.rect(janela, VERDE, botao_reiniciar)
        
        desenhar_texto("REINICIAR", fonte, PRETO, janela, telaL//2 - 80, 310)
        
        # Botão Sair
        if botao_sair.collidepoint(mouse_pos):
            pygame.draw.rect(janela, VERMELHO_CLARO, botao_sair)
        else:
            pygame.draw.rect(janela, VERMELHO, botao_sair)
        
        desenhar_texto("SAIR", fonte, PRETO, janela, telaL//2 - 40, 410)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_reiniciar.collidepoint(evento.pos):
                    rodando_game_over = False
                    reiniciar_jogo()
                elif botao_sair.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)

# ------------------- Inicialização do jogo -------------------

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
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        player.andarEsquerda()
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        player.andarDireita()
    if teclas[pygame.K_UP] or teclas[pygame.K_SPACE] or teclas[pygame.K_w]:
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
            bolhasTotal += 1

            if som_ativo:
                somBolhas.play()
                somBolhas.set_volume(0.5)

            print("Bolha coletada! Pontuação:", player.pontuacao)
        else:
            b.desenharBolhas(cameraX)

    # Porta
    porta_checkpoint.desenharPorta(cameraX)
    if porta_checkpoint.colisao(player):
        print("Checkpoint atingido! Mostrando pontuação...")
        tela_pontuacao()
        nivel_atual += 1
        if nivel_atual < len(fases):
            # carrega próxima fase normalmente
            carregarFase(nivel_atual)
            player.x = 100
            player.y = faseA - player.altura - 50
        else:
            # Última fase concluída
            if bolhasTotal >= 6:
                cutscene_texto("vencer")  # chama cutscene de vitória
            else:
                cutscene_texto("gameover")  # mostra cutscene de game over
                print("Fim do jogo. Você não coletou bolhas suficientes para a cutscene de vitória!")
            pygame.quit()
            sys.exit()

    # Vidas
    player.desenharVidas()

    pygame.display.update()

pygame.quit()
