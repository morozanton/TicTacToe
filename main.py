from game import MultiplayerGame, AiGame

logo = """
                 ______                 
 ``..      ..''.~      ~.``..      ..'' 
     ``..''   |          |   ``..''     
     ..'`..   |          |   ..'`..     
 ..''      ``..`.______.'..''      ``.. 
   ______                  ______       
 .~      ~.``..      ..''.~      ~.     
|          |   ``..''   |          |    
|          |   ..'`..   |          |    
 `.______.'..''      ``..`.______.'     
                 ______                 
 ``..      ..''.~      ~.``..      ..'' 
     ``..''   |          |   ``..''     
     ..'`..   |          |   ..'`..     
 ..''      ``..`.______.'..''      ``.. 
\t\t\tTic Tac Toe                                  
\t\t©Anton Moroz, 2023             
"""

print(logo)
game_mode = int(input('Select game mode\n1 - Single player, 2 - Multiplayer: '))
if game_mode == 1:
    game = AiGame()
elif game_mode == 2:
    game = MultiplayerGame()
else:
    raise Exception('Incorrect game mode')
game.game_loop()
