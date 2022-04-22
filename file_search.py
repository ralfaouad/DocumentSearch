import os
import pickle
import PySimpleGUI as sg
from typing import Dict
sg.ChangeLookAndFeel('Black')

class GUI:
    ''' Create a GUI object '''
    def __init__(self):
        self.layout: list = [
            [sg.Text('Search Query', size=(11,1)),
            sg.Input(size=(40,1), focus=True, key="QUERY"),
            sg.Button("Search", bind_return_key="True")], 
            [sg.Radio('Tag Based', size=(10,1), group_id='choice', key="TAGBASED", default=True), 
             sg.Radio('Path Based', size=(10,1), group_id='choice', key="PATHBASED"), 
             sg.Radio('--?--', size=(10,1), group_id='choice', key="")],
            # [#sg.Text('Root Path', size=(11,1)), 
            #  sg.Input('/..', size=(40,1), key="PATH"), 
            #  sg.FolderBrowse('Browse', size=(10,1)), 
            #  sg.Button('Re-Index', size=(10,1), key="_INDEX_"), 
            #  sg.Button('Search', size=(10,1), bind_return_key=True, key="_SEARCH_")],
            [sg.Output(size=(100,30))]]
        
        self.window: object = sg.Window('Search Engine', self.layout, element_justification='left')


def main():
    ''' The main loop for the program '''
    g = GUI()

    while True:
        event, values = g.window.read()
        if event in (sg.WIN_CLOSED, 'Exit', None):
            break
        if event == 'Search':
            q = values['QUERY']
            # print("The query is: ",q)
            if values["TAGBASED"]:
                print("query is: ",q," and tag-based approach")
            elif values["PATHBASED"]:
                print("query is: ",q," and path-based approach")
            else:
                print("--?-- chosen")
        if event == '_SEARCH_':
            break
           


if __name__ == '__main__':
    print('Starting Engine...')
    main()            