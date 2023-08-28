from sorter import Sorter

sorter = Sorter((800,600))
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

    sorter.checkForEvents()
    sorter.updateDisplay()

