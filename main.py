import pygame, sys

pygame.init()
janela = pygame.display.set_mode((1120, 630))
pygame.display.set_caption("Joguinho!")

clock = pygame.time.Clock() #controla os frames
 

rodando = True
while rodando:
    #rodando o loop em 60 fps
    clock.tick(60)
    eventos = pygame.event.get()

    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False


    janela.fill((255,247,231))




    #Atualizar a imagem da tela
    pygame.display.update()
    

pygame.quit()