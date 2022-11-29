import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
import matplotlib.figure as fig
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')


fig1 = fig.Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
fig1.add_subplot().plot(t, 2 * np.sin(2 * np.pi * t)) # Ajouter les graphs ici
fig2 = fig.Figure(figsize=(5, 4), dpi=100)

fig2.add_subplot().plot(t, 2 * np.sin(2 * np.pi * t))

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def make_window(theme):
    sg.theme(theme)
    menu_def = [['Application', ['Exit']],
                ['Help', ['About']]]
    right_click_menu_def = [[], ['Edit Me', 'Versions', 'Exit']]

    paramètres_layout = [
        [sg.Checkbox('Allumer/Eteindre', default=False, k='-Etat-')],
        [sg.Radio('Ordre 1', "RadioDemo", default=False, size=(10, 1), k='-R1-'),
         sg.Radio('Ordre > 1', "RadioDemo", default=False, size=(10, 1), k='-R2-')],

    ]

    input_layout = [
        [sg.Text('Plot test')],
        [sg.Canvas(key='-CANVAS-')],
        [sg.Button('Ok', k='okbtn')]
        ]



    output_layout = [[sg.Text("Popup Testing")],
                     [sg.Button("Open Folder")],
                     [sg.Button("Open File")]]

    filtre_layout = [[sg.Text("See how elements look under different themes by choosing a different theme here!")],
                     [sg.Listbox(values=sg.theme_list(),
                                 size=(20, 12),
                                 key='-THEME LISTBOX-',
                                 enable_events=True)],
                     [sg.Button("Set Theme")]]

    logging_layout = [[sg.Text("Anything printed will display here!")],
                      [sg.Multiline(size=(60, 15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                                    reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True,
                                    auto_refresh=True)]
                      ]

    layout = [[sg.MenubarCustom(menu_def, font='Courier 10', tearoff=False)]]  # , #font : Police et taille.
    # [sg.Text('Projet2A API', size=(38, 1), justification='center', font=("Helvetica", 16),
    #        relief=sg.RELIEF_RIDGE, enable_events=False)]]# relief => cadre(ici)
    layout += [[sg.TabGroup([[sg.Tab('Paramètres', paramètres_layout),
                              sg.Tab('Input', input_layout),
                              sg.Tab('Output', output_layout),
                              sg.Tab('Filtre', filtre_layout),
                              sg.Tab('Control', logging_layout)]], key='-TAB GROUP-', expand_x=True, expand_y=True),

                ]]
    layout[-1].append(sg.Sizegrip())
    window = sg.Window('Projet2A API', layout, right_click_menu=right_click_menu_def,
                       right_click_menu_tearoff=False, grab_anywhere=False, resizable=True, margins=(0, 0),
                       use_custom_titlebar=False, finalize=True, keep_on_top=False)
    window.set_min_size(window.size)
    #  window.maximize()
    return window

def main():
    window = make_window(sg.theme())
    while True:
        draw_figure(window['-CANVAS-'].TKCanvas, fig2)
        event, values = window.read(timeout=100)
        # keep an animation running so show things are happening
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ', values[key])
        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            break
        elif event == 'About':
            print("[LOG] Clicked About!")
            sg.popup('PySimpleGUI Demo All Elements',
                     'Right click anywhere to see right click menu',
                     'Visit each of the tabs to see available elements',
                     'Output of event and values can be see in Output tab',
                     'The event and values dictionary is printed after every event', keep_on_top=True)
        elif event == 'Popup':
            print("[LOG] Clicked Popup Button!")
            sg.popup("You pressed a button!", keep_on_top=True)
            print("[LOG] Dismissing Popup!")
        elif event == 'Test Progress bar':
            print("[LOG] Clicked Test Progress Bar!")
            progress_bar = window['-PROGRESS BAR-']
            for i in range(100):
                print("[LOG] Updating progress bar by 1 step (" + str(i) + ")")
                progress_bar.update(current_count=i + 1)
            print("[LOG] Progress bar complete!")
        elif event == "-GRAPH-":
            graph = window['-GRAPH-']  # type: sg.Graph
            graph.draw_circle(values['-GRAPH-'], fill_color='yellow', radius=20)
            print("[LOG] Circle drawn at: " + str(values['-GRAPH-']))
        elif event == "Open Folder":
            print("[LOG] Clicked Open Folder!")
            folder_or_file = sg.popup_get_folder('Choose your folder', keep_on_top=True)
            sg.popup("You chose: " + str(folder_or_file), keep_on_top=True)
            print("[LOG] User chose folder: " + str(folder_or_file))
        elif event == "Open File":
            print("[LOG] Clicked Open File!")
            folder_or_file = sg.popup_get_file('Choose your file', keep_on_top=True)
            sg.popup("You chose: " + str(folder_or_file), keep_on_top=True)
            print("[LOG] User chose file: " + str(folder_or_file))
        elif event == "Set Theme":
            print("[LOG] Clicked Set Theme!")
            theme_chosen = values['-THEME LISTBOX-'][0]
            print("[LOG] User Chose Theme: " + str(theme_chosen))
            window.close()
            window = make_window(theme_chosen)
        elif event == 'Edit Me':
            sg.execute_editor(__file__)
        elif event == 'Versions':
            sg.popup_scrolled(__file__, sg.get_versions(), keep_on_top=True, non_blocking=True)
    window.close()
    exit(0)



if __name__ == '__main__':
    sg.theme('black')
    main()
