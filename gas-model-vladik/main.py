from visual import sleep

import config
import interface
import model

interface.MenuInterface()

while True:
    if config.menu_switch == 1:
        interface.ModelInterface()
        while config.menu_switch:
            if config.start:
                model.Simulation()
            sleep(0.1)
        interface.MenuInterface()
    
    if config.menu_switch == 2:
        interface.AuthorsInterface()
        while config.menu_switch:
            sleep(0.1)
        interface.MenuInterface()

    if config.menu_switch == 3:
        interface.TheoryInterface()
        while config.menu_switch:
            sleep(0.1)
        interface.MenuInterface()

    sleep(0.1)