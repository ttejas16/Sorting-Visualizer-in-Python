from sorter import Sorter

# set window size according to preference 1000 x 600 works great
sorter = Sorter((1000,600))
sorter.generateList()


while True:
    sorter.resetDisplay()

    if sorter.showMenu:
        sorter.menu()
    
    if not sorter.showMenu:
        if sorter.showReset:
            sorter.showResetButton()

        sorter.displayList()
        sorter.updateDisplay()

        if sorter.sorted:
            sorter.sorted = False
            sorter.showReset = True
            sorter.finalSortedDisplay()
            sorter.updateDisplay()

    sorter.checkForEvents()
    sorter.updateDisplay()

