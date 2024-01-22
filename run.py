from birdy import BirdyGame

game = BirdyGame()

while True:
    game.handle_events()
    game.update_game_state()
    game.draw_elements()