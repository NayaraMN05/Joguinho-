import pygame, asyncio, platform


som_ativo = True
async def game_loop():
    pygame.init()
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    

    # Tela do Jogo
    telaL = 1120
    telaA = 630
    janela = pygame.display.set_mode((telaL, telaA))
    pygame.display.set_caption("O Legado de Cid")

    # Tamanho da Tela da Fase
    faseL  = 3360
    faseA = 630

    # -------------- Imagens --------------
    plataformaImg = pygame.image.load("imagens/plataforma1.png")
    pats = pygame.image.load("imagens/pats.png")

    bgImg = pygame.image.load("imagens/BG.png")
    bgImg = pygame.transform.scale(bgImg, (telaL, telaA))

    coracaoImg = pygame.image.load("imagens/corazon.png")
    coracaoImg = pygame.transform.scale(coracaoImg, (70, 50))

    inimigo1 = pygame.image.load("imagens/pets.png")
    inimigo1 = pygame.transform.scale(inimigo1, (100, 52))

    bolha = pygame.image.load("imagens/bolha1.png")
    bolha = pygame.transform.scale(bolha,(60,60))

    porta = pygame.image.load("imagens/shell.png")
    porta = pygame.transform.scale(porta, (150, 150))

    charwalk1 = pygame.image.load("imagens/walk1.png")
    charwalk1 = pygame.transform.scale(charwalk1, (80, 40))

    charwalk2 = pygame.image.load("imagens/walk2.png")
    charwalk2 = pygame.transform.scale(charwalk2, (80, 40))

    async def menu_inicial():
        global som_ativo, rodando
        tocar_musica(somMenu)

        BtnL = 300
        BtnA = 150

        # Redimensionando Botões
        logoImg = pygame.transform.scale(logo, (150, 150))
        BtnJogarImg =  pygame.transform.scale(BtnJogar, (BtnL, BtnA))
        BtnSairImg =  pygame.transform.scale(BtnSair, (380, 200))
        BtnsounOnImg = pygame.transform.scale(BtnSoundOn, (BtnL, BtnA))
        BtnsounOffImg = pygame.transform.scale(BtnSoundOff, (BtnL, BtnA))
        patsImg = pygame.transform.scale(pats, (telaL, 80))
        charImg = pygame.transform.scale(logo2, (200, 200)) # TROCAR DEPOIS

        # Posição dos botões
        posLogo = (telaL//2 - logoImg.get_width()//0.35, 100)
        posJogar = (telaL//2 - BtnJogarImg.get_width()//0.585, 255)
        posSair = (telaL//2 - BtnSairImg.get_width()//0.7, 275)
        posSom = (telaL//2 - BtnsounOnImg.get_width()//0.55, 345)
        posPats = (telaL//2 - patsImg.get_width()//2, 550)
        posChar = (telaL//2 - logo2.get_width()//50, 150)
        
        # Rect para colisão e reconhecimento de cliques
        BtnJogarRect = pygame.Rect(
            posJogar[0] + 100, # posição x da colisão do botão
            posJogar[1] + 40, # posição y da posição do botão
            BtnJogarImg.get_width() - 190,
            BtnJogarImg.get_height() - 110,
        )

        BtnSairRect = pygame.Rect(
            posSair[0] + 150,
            posSair[1] + 90,
            BtnSairImg.get_width() - 300,
            BtnSairImg.get_height() - 160,
        )

        BtnsoundRect = pygame.Rect(
            posSom[0] + 160,
            posSom[1] + 90, 
            BtnsounOnImg.get_width() - 250,
            BtnsounOnImg.get_height() - 110,
        )
    
        rodando_menu = True

        while rodando_menu:
            await asyncio.sleep(0)

            # Desenhando os botões na tela do Menu Iniciar
            janela.fill(BRANCO)
            janela.blit(logoImg, posLogo)
            janela.blit(BtnJogarImg, posJogar)
            janela.blit(BtnSairImg, posSair)
            janela.blit(patsImg, posPats)
            janela.blit(charImg, posChar)
            if som_ativo:
                janela.blit(BtnsounOnImg, (posSom))
            else:
                janela.blit(BtnsounOffImg, (16, 383))

            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    # BOTÃO JOGAR
                    if BtnJogarRect.collidepoint(evento.pos):
                        await cutscene_texto("inicio")
                        rodando_menu = False

                    # BOTÃO SAIR
                    elif BtnSairRect.collidepoint(evento.pos):
                        sairWeb()
                        pygame.quit()

                    # BOTÃO SOM
                    elif som_ativo and BtnsoundRect.collidepoint(evento.pos):
                        som_ativo = False
                        parar_musica()
                        pygame.mixer.stop()

                    elif not som_ativo and BtnsoundRect.collidepoint(evento.pos):
                        som_ativo = True
                        tocar_musica(somMenu)

                    elif som_ativo and BtnsoundRect.collidepoint(evento.pos):
                        som_ativo = False
                        parar_musica()
                        pygame.mixer.stop()

                    elif not som_ativo and BtnsoundRect.collidepoint(evento.pos):
                        som_ativo = True
                        tocar_musica(somMenu)
            """
            # DEBUG - botão jogar
            pygame.draw.rect(janela, (255, 0, 0), BtnJogarRect, 2)
            # DEBUG - botão sair
            pygame.draw.rect(janela, (255, 0, 0), BtnSairRect, 2)
            # DEBUG - botão som
            pygame.draw.rect(janela, (255, 0, 0), BtnsoundRect, 2)
            """


            pygame.display.update()
            await asyncio.sleep(0.016) # 60 FPS


    # Botões
    BtnJogar = pygame.image.load("imagens/Btnjogar.png")
    BtnSair = pygame.image.load("imagens/Btnsair.png")
    BtnSoundOn = pygame.image.load("imagens/BtnsoundOn.png")
    BtnSoundOff = pygame.image.load("imagens/BtnsoundOff.png")
    logo = pygame.image.load("imagens/Btnlogostudio.png")
    logo2 = pygame.image.load("imagens/logo2.png")


     # -------------- Som --------------
    # Músicas das Fases
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
    # somwin = pygame.mixer.Sound("sound/win.wav") COLOCAR DEPOIS

    # Velocidade e gravidade
    velocidade = 5
    gravidade = 1
    forca_pulo = 20
    nivel_atual = 0
    bolhasTotal = 0
    distanciaChao = 20
    rodando = True
    acabouJogo = False

    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    VERDE = (0, 200, 0)
    VERDE_CLARO = (0, 255, 0)
    VERMELHO = (200, 0, 0)
    VERMELHO_CLARO = (255, 0, 0)

    # Fonte
    fonte = pygame.font.Font(None, 60)

    # Fases
    fases = [

            #1
        {
            "plataformas": [
                (685, 470),
                (900, 280),
                (1100, 100),
                (1512, 480),
                (1678, 480),
                (2042, 420),
                (2230, 348),
                (2464, 490),
                (2820, 396),
                (2969, 464),
            ],
            "inimigos": [(930, 554), (1030,554), (1130,554), (1927, 554), (2030,554),(2150,554)],
            "bolhas": [(1150, 40), (1744, 324), (2860, 290)],
            "porta": (3200, 500),
            "faseL": 3360,
            "vidasIniciais": 3
        },

        #2
        {
            "plataformas": [
                (310, 450),
                (610, 270),
                (810, 428),
                (992, 270),
                (1350, 200),
                (1700, 235),
                (1420, 487),
                (2043, 550),
                (2400, 550),
                (2400, 380),
                (2400, 200),
                (2600, 100),
                (2900, 200),
                (3135, 308),
            ],
            "inimigos": [(518,554), (620,554), (720,554),(820,554),(950, 554),(867, 340),(1442, 554),(1900,554 ),(1765, 160)],
            "bolhas": [(830, 100),(1722, 200),(2650, 35)],
            "porta": (3170, 200),
            "faseL": 3360,
            "vidasIniciais": 3
        },

        #3
        {
            "plataformas": [
                (284, 473),
                (470, 473),
                (799, 307),
                (1116, 276),
                (1487, 342),
                (1649, 342),
                (1916, 220),
                (1916, 475),
                (2223, 366),
                (2564, 470),
                (2868, 410),
                (2870, 190),
                (3145, 321),
            ],
            "inimigos": [(500,565),(600,565),(700,565),(800,565),(900,565),(1026, 565),(1200,565), (1340, 322),(1500,565),(1600,565),(1700,565),(1850,565),(2000,565),(2100,565),(2200,565),(2300,565),(2400,565),(2700,565), (2970, 565)],
            "bolhas": [(1350, 51), (1951, 53), (2575,565)],
            "porta": (2870, 40),
            "faseL": 3360,
            "vidasIniciais": 3
        }
    ]

    def sairWeb():
        if platform.system() == "Emscripten":
            import js
            js.window.location.href = "https://corallium-studio.itch.io/o-legado-de-cid"
        else:
            pygame.quit()

    def musicas(nivel):
        global som_ativo
        if som_ativo:
            pygame.mixer.music.load(musicas_fases[nivel])
            pygame.mixer.music.play(-1)  # loop infinito

    def tocar_musica(caminho):
        global som_ativo
        if som_ativo:
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.play(-1)

    def parar_musica():
        pygame.mixer.music.stop()

    def desenhar_texto(texto, fonte, cor, surface, x, y):
        texto_obj = fonte.render(texto, True, cor)
        surface.blit(texto_obj, (x, y))

    async def cutscene_texto(cena):
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
                                    
        # Tamanho da caixa
        caixa_largura = 900
        caixa_altura = 500

        caixa_x = (telaL - caixa_largura) // 2
        caixa_y = telaA - caixa_altura - 60
        caixa_rect = pygame.Rect(caixa_x, caixa_y, caixa_largura, caixa_altura)

        while esperando:
            janela.fill(BRANCO if cena != "gameover" else PRETO)

            # Fundo da caixa
            pygame.draw.rect(janela, BRANCO, caixa_rect, border_radius=12)
            pygame.draw.rect(janela, PRETO, caixa_rect, 3, border_radius=12)

            # Texto dentro da caixa
            desenhar_texto_em_caixa(
                janela,
                linhas[indice],
                pygame.font.Font(None, 40),
                PRETO if cena != "gameover" else VERMELHO_CLARO,
                caixa_rect
            )

            # Texto de instrução
            desenhar_texto(
                "Pressione ESPAÇO para continuar",
                pygame.font.Font(None, 30),
                PRETO if cena != "gameover" else VERMELHO_CLARO,
                janela,
                caixa_x + 20,
                caixa_y + caixa_altura - 35
            ) 

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()

                # passar cutscene com botão do mouse
                if evento.type == pygame.MOUSEBUTTONDOWN:
                        indice += 1
                        if indice >= len(linhas):
                            esperando = False

                # passar cutscene com espaço            
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        indice += 1
                        if indice >= len(linhas):
                            esperando = False
                            
            pygame.display.update()
            await asyncio.sleep(0)

    # Organizaão da Cut Scene
    def desenhar_texto_em_caixa(surface, texto, fonte, cor, rect, espacamento=5):
        palavras = texto.split(" ")
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            teste_linha = linha_atual + palavra + " "
            if fonte.size(teste_linha)[0] <= rect.width - 20:
                linha_atual = teste_linha
            else:
                linhas.append(linha_atual)
                linha_atual = palavra + " "

        linhas.append(linha_atual)

        # Calcula altura total do texto
        altura_texto = len(linhas) * (fonte.get_height() + espacamento)

        # Centraliza verticalmente dentro da caixa, altura da caixa
        altura_extra = (rect.height - altura_texto) // 5

        # Centraliza verticalmente o texto na caixa
        y_offset = rect.y + altura_extra


        # Preenche a caixa com o fundo (ajustando o fundo se necessário)
        pygame.draw.rect(surface, BRANCO, rect)  # fundo da caixa
        pygame.draw.rect(surface, PRETO, rect, 3, border_radius=12)  # borda da caixa

        # Desenha cada linha do texto dentro da caixa
        for linha in linhas:
            texto_render = fonte.render(linha, True, cor)
            surface.blit(texto_render, (rect.x + 10, y_offset))
            y_offset += texto_render.get_height() + espacamento

    # Chama o menu antes do jogo
    await menu_inicial()

    class Player():
        def __init__(self):
            self.img1 = charwalk1
            self.img2 = charwalk2
            self.img = self.img1 # A imagem inicial é a charwalk1
            self.largura = self.img.get_width()
            self.altura = self.img.get_height()
            self.x = 100
            self.y = faseA - self.altura - distanciaChao
            self.vel_y = 0
            self.chao_y = faseA - distanciaChao
            self.no_chao = True
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

            if self.y + self.altura >= faseA - distanciaChao:
                self.y = faseA - distanciaChao - self.altura
                self.vel_y = 1
                self.no_chao = True

        def colisaoInimigo(self, inimigos):
            for inimigo in inimigos[:]:
                if (self.x + self.largura > inimigo.x and self.x < inimigo.x + inimigo.largura and
                    self.y + self.altura > inimigo.y and self.y < inimigo.y + inimigo.altura):
                    self.vidas -= 1

                    if som_ativo:
                        somlixo.play()
                        somlixo.set_volume(0.6)
                        # COLOCAR NA TELA DEPOIS
                    print(f"Vida perdida! Vidas restantes: {self.vidas}")
                    inimigos.remove(inimigo)
                    if self.vidas <= 0:
                        # COLOCAR NA TELA DEPOIS
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
        player.y = faseA - player.altura - distanciaChao
        player.vel_y = 1
        player.no_chao = False

        pygame.mixer.music.stop() # Para música anterior
        musicas(nivel)
        
        
    def reiniciar_jogo():
        global nivel_atual, acabouJogo
        nivel_atual = 0
        acabouJogo = False

        # Refazendo as infos do Player quando reiniciar o jogo
        player.vidas = 3
        player.pontuacao = 0
        player.x = 100
        player.y = faseA - player.altura - distanciaChao
        player.vel_y = 1
        player.no_chao = False



        carregarFase(nivel_atual)
        

    async def tela_pontuacao():
        mostrando = True
        while mostrando:
            await asyncio.sleep(0)
            janela.fill(BRANCO)

            # Mostrar estrelas
            if totalEstrelas > 0:
                bolhasColetadas = totalEstrelas - len(bolhas)
                estrelasFinais = int(round((bolhasColetadas / totalEstrelas *3))) 
                for i in range(estrelasFinais):
                    janela.blit(bolha, (400 + i * (bolha.get_width() + 10), 300))

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

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if botao_continuar.collidepoint(evento.pos):
                        mostrando = False

            pygame.display.update()

    async def tela_game_over():
        global som_ativo
        await asyncio.sleep(0)
        # Parar música ao perder todas as vidas 
        pygame.mixer.music.stop()

        if som_ativo:
            somgameover.play()

        # CUTSCENE roda uma única vez
        await cutscene_texto("gameover")

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
                    
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if botao_reiniciar.collidepoint(evento.pos):
                        reiniciar_jogo()
                        return
                    elif botao_sair.collidepoint(evento.pos):
                        sairWeb()

            pygame.display.update()
            await asyncio.sleep(0)



    player = Player()
    carregarFase(nivel_atual)

    # Colocando o jogo para rodar, na web :)
    while rodando:
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

        if player.vidas <= 0 and not acabouJogo:
            acabouJogo = True
            await tela_game_over()
            acabouJogo = False
            continue

        # Fundo
        janela.blit(bgImg, (0, 0))

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
            else:
                b.desenharBolhas(cameraX)

        # Porta
        porta_checkpoint.desenharPorta(cameraX)
        if porta_checkpoint.colisao(player):
            await tela_pontuacao()
            nivel_atual += 1
            if nivel_atual < len(fases):
                # carrega próxima fase normalmente
                carregarFase(nivel_atual)
                player.x = 100
                player.y = faseA - player.altura - distanciaChao
                player.vel_y = 1
                player.no_chao = False
            else:
                # Última fase concluída
                if bolhasTotal >= 6:
                    await cutscene_texto("vencer")  # chama cutscene de vitória
                else:
                    await cutscene_texto("gameover")  # mostra cutscene de game over
                pygame.quit()

        # Vidas
        player.desenharVidas()

        pygame.display.update()
        await asyncio.sleep(0)

    
    pygame.quit()

asyncio.run(game_loop())
