import flet as ft
import random

#TODO 1: Finish core gameplay [DONE]
#TODO 2: Add animations for played spaces
#TODO 3: Finish play again mechanic [DONE]
#TODO 4: Add winning conditions 
#TODO 5: Check empty spaces to finish game [DONE]
#TODO 6: ??? -> Profit
#TODO 7: Add option to change background
#TODO 8: Add capture mechanic [DONE]

#! There is a bug regarding the p1buttons, p2buttons lists and the turn logic, i'll fix it later
#! Bug Fixed

#! There is a bug with capture mechanic, playing a 2 spaces before the score space is skipping and adding the points
#! Bug Fixed

def main(page: ft.Page):
    #variables
    turn = random.randint(0,1)

    #functions

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
        
        print(f"---{turn+1}---")
        
        checkCapture(position, turn)
        checkTurn(position)
        checkEmptyBoard()

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
        pass

    #debug

    def printPosition(e):
        print(e.control.data[0])

    #page setup
    page.title = "Mancala"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    #controls

    p1Buttons = [ft.Button(width=100, 
                           height=100, 
                           content=ft.Text(value="1", 
                                           size=20), 
                            data = [i,1], 
                            color=ft.Colors.BLUE,
                            on_click=transferPoints)
                            for i in range(12,6,-1)]
    
    p2Buttons = [ft.Button(width=100, 
                           height=100, 
                           content=ft.Text(value="1", 
                                           size=20), 
                            data = [i,1], 
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

    p1Buttons = sorted(p1Buttons, key=lambda e: e.data[0])
    orderList = p2Buttons + [p2Space] + p1Buttons + [p1Space]

    for i in orderList:
        print(i.data)

    playerColumn = ft.Column(controls=[p1Row, p2Row])
    finalRow = ft.Row(controls=[p1Space, playerColumn, p2Space], alignment=ft.MainAxisAlignment.CENTER)
    turnText = ft.Text(value=f"Turn: Player {turn+1}")
    changeTurn(turn)
    page.add(turnText, finalRow)

ft.run(main=main, assets_dir="assets")