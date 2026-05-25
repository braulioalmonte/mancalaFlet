import flet as ft
import random

#TODO 1: Finish core gameplay [DONE]
#TODO 2: Add animations for played spaces
#TODO 3: Finish play again mechanic [DONE]
#TODO 4: Add winning conditions [DONE]
#TODO 5: Check empty spaces to finish game [DONE]
#TODO 6: ??? -> Profit
#TODO 7: Add option to change background [Halfly Done]
#TODO 8: Add capture mechanic [DONE]
#TODO 9: Add an option to disable zero buttons
#TODO 10: Add reset button and reset game function [DONE]
#TODO 11: Add a settings view for TODO 9 and TODO 7

def main(page: ft.Page):
    #variables
    turn = random.randint(0,1)

    #functions

    def changeBackground(e:ft.Event[ft.Dropdown]):
        if e.control.value != "None":
            page.decoration = ft.BoxDecoration(image=ft.DecorationImage(src=e.control.value, fit=ft.BoxFit.FILL))
            page.bgcolor = ft.Colors.TRANSPARENT #<- Gotta make bgcolor transparent for background images to work
        else:
            page.bgcolor = ft.Colors.WHITE

    def animateButton(button):
        pass

    def transferPoints(e: ft.Event[ft.Button]):
        nonlocal turn
        position = e.control.data[0]
        beads = e.control.data[1]
        e.control.data[1] = 0
        e.control.content.value = f"{0}"

        for i in range(beads):
            position = (position + 1) % 14 # <- Sneaky Idiot, was 13 and was giving me a looping logic mistake
            if (position == 6 and turn == 0):
                position = 7
            elif (position == 13 and turn == 1):
                position = 0

            print(position)
            orderList[position].data[1] += 1
            orderList[position].content.value = f"{orderList[position].data[1]}"
        
        checkCapture(position, turn)
        checkTurn(position)
        checkEmptyBoard()
        disableZeroes(turn)

    def checkCapture(position, turn):

        if orderList[12-position].data[1] != 0:
            if turn == 0:
                if  12 >= position >= 7:
                    if orderList[position].data[1] == 1:
                        print(f"Capture: {12-position}")
                        #add captured beads and display new amount
                        p1Space.data[1] += orderList[12-position].data[1] + 1
                        p1Space.content.value = f"{p1Space.data[1]}"

                        #reset the capturing and captured space
                        orderList[12-position].data[1] = 0
                        orderList[12-position].content.value = f"{0}"

                        orderList[position].data[1] = 0
                        orderList[position].content.value = f"{0}"

                        stateText.visible = True
            elif turn == 1:
                if  5 >= position >= 0:
                    if orderList[position].data[1] == 1:
                        print(f"Capture: {12-position}")
                        #add captured beads and display new amount
                        p2Space.data[1] += orderList[12-position].data[1] + 1
                        p2Space.content.value = f"{p2Space.data[1]}"

                        #reset the capturing and captured space
                        orderList[12-position].data[1] = 0
                        orderList[12-position].content.value = f"{0}"

                        orderList[position].data[1] = 0
                        orderList[position].content.value = f"{0}"

                        stateText.visible = True
        else:
            stateText.visible = False

    def checkTurn(position):
        nonlocal turn
        #play again or not
        if position == 13 and turn == 0:
            turn = 0
        elif position == 6 and turn == 1:
            turn = 1
        else:
            turn = (turn+1) % 2

        turnText.value = f"Turn: Player {turn+1}"

        changeTurn(turn)

    def changeTurn(turn):
        if turn == 0:
            #disable p2 buttons
            for button in p2Buttons:
                button.disabled = True
            #enable p1 buttons
            for button in p1Buttons:
                button.disabled = False

        elif turn == 1:
            #disable p1 buttons
            for button in p1Buttons:
                button.disabled = True
            #enable p2 buttons
            for button in p2Buttons:
                button.disabled = False

    def checkEmptyBoard():
        checkp1 = all(b.data[1] == 0 for b in p1Buttons)
        checkp2 = all(b.data[1] == 0 for b in p2Buttons)
        
        if checkp1:
            p2Space.data[1]+=sum(b.data[1] for b in p2Buttons)
            p2Space.content.value = f"{p2Space.data[1]}"
            for b in p2Buttons:
                b.data[1] = 0
                b.content.value = f"{b.data[1]}"
            finishGame()
        elif checkp2:
            p1Space.data[1]+=sum(b.data[1] for b in p1Buttons)
            p1Space.content.value = f"{p1Space.data[1]}"
            for b in p1Buttons:
                b.data[1] = 0
                b.content.value = f"{b.data[1]}"
            finishGame()

    def finishGame():
        for b in orderList:
            b.disabled = True
        checkWin()

    def checkWin():
        if p1Space.data[1] > p2Space.data[1]:
            stateText.value = "Player 1 Wins"
        elif p2Space.data[1] > p1Space.data[1]:
            stateText.value = "Player 2 Wins"
        else:
            stateText.value = "Tie"
        stateText.visible = True

    def resetGame(e):
        nonlocal turn
        for b in orderList:
            if b.data[0] not in [6,13]:
                b.data[1] = 4
            else:
                b.data[1] = 0
            
            b.content.value = f"{b.data[1]}"
        changeTurn(turn)

    def disableZeroes(turn):
        lower = upper = 0
        if turn == 0:
            lower,upper = 7,13
        elif turn == 1:
            lower,upper = 0,6
        
        for b in orderList[lower:upper]:
            if b.data[1] == 0:
                b.disabled = True
            else:
                b.disabled = False

    #page setup
    page.title = "Mancala"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.WHITE

    #controls

    p1Buttons = [ft.Button(width=100, 
                           height=100, 
                           content=ft.Text(value="4", 
                                           size=20), 
                            data = [i,4], 
                            color=ft.Colors.BLUE,
                            on_click=transferPoints)
                            for i in range(12,6,-1)]
    
    p2Buttons = [ft.Button(width=100, 
                           height=100, 
                           content=ft.Text(value="4", 
                                           size=20), 
                            data = [i,4], 
                            color=ft.Colors.RED,
                            on_click=transferPoints) 
                            for i in range(0,6)]

    p1Row = ft.Row(controls=p1Buttons)
    p2Row = ft.Row(controls=p2Buttons)

    p1Space = ft.Button(bgcolor=ft.Colors.BLUE, 
                        color=ft.Colors.BLACK, 
                        content=ft.Text("0"), 
                        data=[13,0], width=100, 
                        height=200, 
                        disabled=True)
    
    p2Space = ft.Button(bgcolor=ft.Colors.RED, 
                        color=ft.Colors.BLACK, 
                        content=ft.Text("0"), 
                        data=[6,0],
                        width=100, 
                        height=200, 
                        disabled=True)
    
    backgroundDropdown = ft.Dropdown(options=[ft.DropdownOption(key="None", text="No BG"),
                                              ft.DropdownOption(key="images/bg1.jpg", text="Background 1"),
                                              ft.DropdownOption(key="images/bg2.jpg", text="Background 2")
                                              ],
                                    on_select=changeBackground,
                                    bgcolor=ft.Colors.WHITE,
                                    fill_color=ft.Colors.WHITE,
                                    text="Change Background",
                                    width=250)

    p1Buttons = sorted(p1Buttons, key=lambda e: e.data[0])
    orderList = p2Buttons + [p2Space] + p1Buttons + [p1Space]

    for i in orderList:
        print(i.data)

    playerColumn = ft.Column(controls=[p1Row, p2Row])
    finalRow = ft.Row(controls=[p1Space, playerColumn, p2Space], alignment=ft.MainAxisAlignment.CENTER)
    turnText = ft.Text(value=f"Turn: Player {turn+1}")
    stateText = ft.Text("Capture!", visible=False) #<- Display capture message using the result in checkCapture()
    resetButton = ft.Button("Reset", on_click=resetGame)
    mainColumn = ft.Column(controls=[stateText, 
                                     turnText, 
                                     resetButton, 
                                     finalRow], 
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    mainArea = ft.SafeArea(expand=True, content=mainColumn)
    changeTurn(turn)
    page.add(backgroundDropdown, mainArea)

ft.run(main=main, assets_dir="assets")