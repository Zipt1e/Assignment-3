# ... (previous code)

# Create Fighter instances using the loaded images
knight = Fighter(100, 260, 'Knight', 30, 10, 3, 3, knight_image)
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1, 1, bandit_image)

# Main game loop
run = True
while run:
    clock.tick(fps)

    # Draw background
    draw_bg()

    # Draw panel
    draw_panel()

    # Draw fighters
    knight.draw()
    for bandit in bandit_list:
        bandit.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Draw the flipped bandit image
    flipped_bandit_image = pygame.transform.flip(bandit1.image, True, False)
    screen.blit(flipped_bandit_image, bandit1.rect)

    pygame.display.update()

pygame.quit()
sys.exit()
