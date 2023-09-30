import pygame,random,time,sys,inspect

class Sorter:
    def __init__(self,WINDOW_SIZE):

        self.WINDOW_SIZE = WINDOW_SIZE
        self.RECT_WIDTH = 10
        self.OFFSET = 2
        
        self.TIMSORT_RUN = 16
        self.BUBBLE_SORT_INTERVAL = 0.02
        self.INSERTION_SORT_INTERVAL = 0.05
        self.SELECTION_SORT_INTERVAL = 0.02
        self.QUICK_SORT_INTERVAL = 0.1
        self.MERGE_SORT_INTERVAL = 0.05

        self.SCALE_Y = (0.75 * WINDOW_SIZE[1]) // 100
        self.BOTTOM_OFFSET = 5

        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.GREEN = (0,255,0)
        self.ROYALBLUE = (65, 105, 225)
        
        self.window = self.initialize()

        self.avaliableSorts = ["bubbleSort","insertionSort","selectionSort","quickSort","mergeSort","timSort"]
        self.choicer = self.getChoicer()
        self.unsortedList = []

        self.sorted = False
        self.showReset = False
        self.showMenu = True

        self.font = pygame.font.SysFont("Courier",25)
        self.buttons = self.generateButtons()
        self.resetButton = self.getResetButton()
    
    
    def getChoicer(self):
        res = {}
        members = inspect.getmembers(self)
        for member in members:
            if member[0] in self.avaliableSorts:
                res[member[0]] = member[1]
        
        return res
            

    def initialize(self):
        pygame.init()
        pygame.display.set_caption('Sorting Visualizer')
        window = pygame.display.set_mode(self.WINDOW_SIZE,0,0)
        return window
                    

    def checkForEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.showReset and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.resetButton[1].collidepoint(pygame.mouse.get_pos()):
                        self.handleReset()

            if self.showMenu and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        if button['rectangle'].collidepoint(pygame.mouse.get_pos()):
                            self.handleChoice(button['button_name'])


    def displayButtons(self):
        for button in self.buttons:
            self.window.blit(button['text'],button['rectangle'])


    def generateButtons(self):
        res = []
        index = 1

        for sort in self.avaliableSorts:
            txt = self.font.render(f"{index}. {sort}",True,self.WHITE)
            txtRect = txt.get_rect(topleft=(50,50 + index * 50))
            res.append({'text':txt,'rectangle':txtRect,'button_name':sort})
            index += 1
        return res


    def showResetButton(self):
        self.window.blit(self.resetButton[0],self.resetButton[1])


    def getResetButton(self):
        txt = self.font.render("Reset",True,self.WHITE)
        txtRect = txt.get_rect(topleft=(50,50))
        return [txt,txtRect]
    

    def menu(self):
        self.displayButtons()


    def updateDisplay(self):
        pygame.display.update()


    def resetDisplay(self):
        self.window.fill(self.BLACK)


    def checkValidList(self):
        return len(self.unsortedList) >= 2;


    def generateList(self):
        n =  self.WINDOW_SIZE[0] // (self.RECT_WIDTH + self.OFFSET)
        for i in range(n):
            self.unsortedList.append(random.randint(1,100))


    def drawPygameRect(self,color,left,height):
        '''
        needs the color,left and height for pygame.Rect\n
        top is calculated using height. Width is a constant
        ''' 

        top = self.WINDOW_SIZE[1] - self.BOTTOM_OFFSET - int(height)        
        pygame.draw.rect(self.window,
                         color,
                         pygame.Rect(left,top,self.RECT_WIDTH,height)
                         )
        

    def displayList(self,targetIndex = None,currentSortedIndex = None):
        # print(targetIndex,currentSortedIndex)
        self.checkForEvents()
        for i in range(len(self.unsortedList)):
            if targetIndex and i == targetIndex:
                self.drawPygameRect(
                        self.GREEN,
                        self.OFFSET + (i * (self.RECT_WIDTH + self.OFFSET)),
                        self.unsortedList[i] + (self.unsortedList[i] * self.SCALE_Y)
                    )
            elif currentSortedIndex and i == currentSortedIndex:
                self.drawPygameRect(
                        self.ROYALBLUE,
                        self.OFFSET + (i * (self.RECT_WIDTH + self.OFFSET)),
                        self.unsortedList[i] + (self.unsortedList[i] * self.SCALE_Y)
                    )
            else:
                self.drawPygameRect(
                        self.WHITE,
                        self.OFFSET + (i * (self.RECT_WIDTH + self.OFFSET)),
                        self.unsortedList[i] + (self.unsortedList[i] * self.SCALE_Y)
                    ) 
           

    def finalSortedDisplay(self):
        for i in range(len(self.unsortedList)):
            for j in range(len(self.unsortedList)):
                if j <= i:
                    self.drawPygameRect(
                                self.GREEN,
                                self.OFFSET + (j * (self.RECT_WIDTH + self.OFFSET)),
                                self.unsortedList[j] + (self.unsortedList[j] * self.SCALE_Y)
                            ) 
                else:
                    self.drawPygameRect(
                                self.WHITE,
                                self.OFFSET + (j * (self.RECT_WIDTH + self.OFFSET)),
                                self.unsortedList[j] + (self.unsortedList[j] * self.SCALE_Y)
                            ) 
            self.checkForEvents()
            self.updateDisplay()
            time.sleep(0.02)
            self.resetDisplay()


    def handleReset(self):
        self.showReset = False
        self.sorted = False
        self.showMenu = True
        self.unsortedList.clear()
        self.generateList()


    def handleChoice(self,choice):
        self.resetDisplay()
        self.showMenu = False
        func = self.choicer[choice]
        # self.buttons.clear()
        time.sleep(0.3)
        func()
            

    def bubbleSort(self):
        
        if not self.checkValidList() :
            return;
        
        self.sorted = True
        for i in range(len(self.unsortedList) - 1):

            for j in range(len(self.unsortedList) - i - 1):
                
                if self.unsortedList[j + 1] < self.unsortedList[j]:
                    temp = self.unsortedList[j + 1]
                    self.unsortedList[j + 1] = self.unsortedList[j]
                    self.unsortedList[j] = temp
                
                self.displayList(j + 1,len(self.unsortedList) - i)
                time.sleep(self.BUBBLE_SORT_INTERVAL)
                self.updateDisplay()
                self.resetDisplay()


    def insertionSort(self):
        if not self.checkValidList() :
            return;
        
        self.sorted = True

        for i in range(len(self.unsortedList)):
            key = self.unsortedList[i]
            j = i - 1
            while j > -1 and self.unsortedList[j] > key:
                self.unsortedList[j + 1] = self.unsortedList[j]
                j -= 1
                self.displayList(j,i)
                time.sleep(self.INSERTION_SORT_INTERVAL)
                self.updateDisplay()
            self.unsortedList[j + 1] = key
            self.resetDisplay()


    def selectionSort(self):
        
        if not self.checkValidList() :
            return;
    
        self.sorted = True

        for i in range(len(self.unsortedList) - 1):

            minIndex = i
            
            for j in range(i + 1,len(self.unsortedList)):
                
                if self.unsortedList[j] < self.unsortedList[minIndex]:
                    minIndex = j

                self.displayList(j, i - 1)
                time.sleep(self.SELECTION_SORT_INTERVAL)
                self.updateDisplay()
            
            if minIndex != i:
                temp = self.unsortedList[i]
                self.unsortedList[i] = self.unsortedList[minIndex]
                self.unsortedList[minIndex] = temp
            
            self.resetDisplay()
                    

    def quickSortHelper(self,lowerBound,upperBound):
        if lowerBound < upperBound:    
            low = lowerBound
            high = upperBound               
            pivot = lowerBound
        
            while low < high:

                while self.unsortedList[low] <= self.unsortedList[pivot] and low < high:
                    low += 1
                    
                while self.unsortedList[high] > self.unsortedList[pivot]: 
                    high -= 1
                
                self.displayList(low,high)
                self.updateDisplay()
                time.sleep(self.QUICK_SORT_INTERVAL)
                self.resetDisplay()

                if low < high:
                    temp = self.unsortedList[low]
                    self.unsortedList[low] = self.unsortedList[high]
                    self.unsortedList[high] = temp
                
            
            temp = self.unsortedList[pivot]
            self.unsortedList[pivot] = self.unsortedList[high]
            self.unsortedList[high] = temp
            

            self.quickSortHelper(lowerBound,high - 1)
            self.quickSortHelper(high + 1,upperBound)


    def quickSort(self):
        if not self.checkValidList() :
            return;
    
        self.sorted = True  
        self.quickSortHelper(0,len(self.unsortedList) - 1)


    def mergeSortHelper(self,low,mid,high):
        i = low
        j = mid + 1
        k = low

        arr = [0]*len(self.unsortedList)

        while i <= mid and j <= high:
            if self.unsortedList[i] >= self.unsortedList[j]:
                arr[k] = self.unsortedList[j]
                k += 1
                j += 1
            else:
                arr[k] = self.unsortedList[i]
                k += 1
                i += 1
                
            self.displayList(i,j)
            self.updateDisplay()
            time.sleep(self.MERGE_SORT_INTERVAL)

        
        while i <= mid:
            arr[k] = self.unsortedList[i]
            k += 1
            i += 1            

        while j <= high:
            arr[k] = self.unsortedList[j]
            k += 1
            j += 1   

        for z in range(low,high + 1):
            self.unsortedList[z] = arr[z]

            self.displayList(z,z - 1)
            time.sleep(0.02)
            self.updateDisplay()
            self.resetDisplay()         


    def divide(self,lb,ub):
        if lb != ub:
            mid = (lb + ub) // 2
            self.divide(lb,mid)
            self.divide(mid + 1,ub)
            self.mergeSortHelper(lb,mid,ub)


    def mergeSort(self):
        if not self.checkValidList():
            return
        
        self.sorted = True 
        self.divide(0,len(self.unsortedList) - 1)
        

    def timInsertionSort(self,start:int,end:int):
        for i in range(start + 1,end + 1):
            
            temp = self.unsortedList[i]
            j = i - 1
            
            while j >= start and self.unsortedList[j] > temp:
                self.unsortedList[j + 1] = self.unsortedList[j]
                j -= 1

                self.displayList(j,i)
                time.sleep(self.INSERTION_SORT_INTERVAL)
                self.updateDisplay()
            
            self.unsortedList[j + 1] = temp
            self.resetDisplay()
    

    def timSort(self):
        if not self.checkValidList():
            return
        
        self.sorted = True

        for i in range(0,len(self.unsortedList),self.TIMSORT_RUN):
            self.timInsertionSort(i,min(i + self.TIMSORT_RUN - 1, len(self.unsortedList) - 1))


        i = self.TIMSORT_RUN
        while i < len(self.unsortedList):
            for j in range(0,len(self.unsortedList),2 * i):
                
                mid = j + i - 1
                end = min(j + (2 * i) - 1,len(self.unsortedList) - 1)

                if mid < end:
                    self.mergeSortHelper(j, mid, end)

            i = 2 * i

            