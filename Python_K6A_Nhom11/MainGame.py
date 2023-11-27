from sys import argv
import pygame
import PyMaze
import UI
import AchievementUI

if __name__ == '__main__':
    Run = True
    while Run:
        pygame.init()
        args = argv[1:]
        diff = 0
        dim = '20x30'
        path = 1
        for arg in args:
            if '--diff' in arg:
                diff = int(arg.split('=')[-1])
            elif '--dim' in arg:
                dim = arg.split('=')[-1]
            elif '--path' in arg:
                path = int(arg.split('=')[-1])
        ui = UI.UI()
        # Khối điều khiển sự kiện

        if ui.run() == "run":
            g = PyMaze.Game(diff, dim, path)
            g.start()
        else:
            scoreboard = AchievementUI.Scoreboard()
            scoreboard.main()
