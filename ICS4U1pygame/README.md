#=========================================== ADDITIONAL FEATURES: ===========================================#
            (1) Scoring System: Implement a real-time score display that increases as the player avoids obstacles.
            (2) Restart Feature: Allow players to restart the game after a game-over without restarting the program.
            (3) Level Progression: Increase game difficulty over time by speeding up enemies.
            (4) Custom Game Mechanics: Introduce new gameplay elements, such as different enemy types or player abilities. 
            (5) Physics Movement: Acceleration and Decelleration
            (6) Soundtrack Integration: Add background music that plays during gameplay and changes based on game events.
            (7) High Score Tracking: Save and display the highest score achieved across game sessions.

#=========================================== INSTRUCTIONS: ===========================================#
    (1) Ensure that pygame is installed on computer. If not, enter in your terminal "pip install pygame"

    (2) Open Folder in IDE (This program was made in Visual Studio Code)

    (3) Ensure the zip file downloaded comes with these files:
        # FILES
        - ICS4U1 - U13_14.py
        - README.md

        # AUDIO FILES
        - background_music.mp3
        - Backward.mp3
        - Collision.mp3
        - Falling_putter.mp3
        - Forward.mp3
        - Jet_EngineStartUp.mp3
        - Rising_putter.mp3
        - highscore.txt

        # IMAGE FILES
        - cloud.png
        - jet.png
        - missile.png
        - Moodcake.ttf
    
    (4) Run the ICS4U1pygame.py file and play the game!

    (5) When the jet collides, you are given the option to restart or exit
        a. To Restart, Click Enter
        b. To Exit Click ESC

CHALLENGES:
A challenge I faced was making sure that the audio of the jet flying up and down has different audios and don't overlap. I fixed this by stopping the audio whenever the player dies. Adding on, a scoring system was implemented and I made sure that high score kept track of and was properly read from the file and written to. Additionally, increasing the difficulty and ensuring it was balanced and playable (as in not too hard and not too easy) was something I needed to ensure was done properly. Doing this, it made the game more fun for the player Furthermore, I delt with an issue of the game program automatically exiting after collision, which was easily fixed by ensuring that the game state transitioned correctly to "game_over" instead of "exit". By managing the game_state variable more carefully, I was able to stop the game from closing and instead display the game over screen with the option to restart or quit. Another minor but tricky challenge was resetting all game elements, like score and level properly when restarting the game. If not handled correctly, leftover sprites or incorrect values could carry over into the next run and break the program.