import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
import math
matplotlib.use('TkAgg')


fig, (ax1, ax2) = plt.subplots(1, 2, sharey="row")


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
        [sg.Graph(canvas_size=(1000, 480), graph_bottom_left=(0, 0), graph_top_right=(1000, 480),
                  background_color='white', enable_events=True, key='-IN-')]
    ]

    output_layout = [
        [sg.Graph(canvas_size=(1000, 480), graph_bottom_left=(0, 0), graph_top_right=(1000, 480),
                  background_color='white', enable_events=True, key='-OUT-')]
    ]

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
    canvas = FigureCanvasTkAgg(fig, window['-IN-'].Widget)
    canvas = FigureCanvasTkAgg(fig, window['-OUT-'].Widget)
    plot_widget = canvas.get_tk_widget()
    plot_widget.grid(row=0, column=0)
    theta = 0  # offset angle for each sine curve

    while True:
        event, values = window.read(timeout=100)
        if values['-TAB GROUP-'] == "Input":
            # Generate points for sine curve.
            x = [degree for degree in range(1080)]
            y = [math.sin((degree + theta) / 180 * math.pi) for degree in range(1080)]
            x2 = [degree for degree in range(1080)]
            y2 = [math.cos((degree + theta) / 180 * math.pi) for degree in range(1080)]

            # Reset ax
            ax1.cla()
            ax1.set_title("Input signal")
            ax1.set_xlabel("t")
            ax1.set_ylabel("A(V)")
            ax1.grid()
            ax1.plot(x, y)  # Plot new curve
            fig.canvas.draw()

            ax2.cla()
            ax2.set_title("Input signal spectrum")
            ax2.set_xlabel("f(Hz)")
            ax2.set_xscale('log')
            ax2.grid()
            ax2.plot(x2, y2)
            fig.canvas.draw()

        elif values['-TAB GROUP-'] == "Output":
            x = [degree for degree in range(1080)]
            y = [3*math.sin((degree + theta) / 180 * math.pi) for degree in range(1080)]
            x2 = [degree for degree in range(1080)]
            y2 = [0.5*math.cos((degree + theta) / 180 * math.pi) for degree in range(1080)]

            # Reset ax
            ax1.cla()
            ax1.set_title("Output signal")
            ax1.set_xlabel("t")
            ax1.set_ylabel("A(V)")
            ax1.grid()
            ax1.plot(x, y)  # Plot new curve
            fig.canvas.draw()

            ax2.cla()
            ax2.set_title("Output signal spectrum")
            ax2.set_xlabel("f(Hz)")
            ax2.set_xscale('log')
            ax2.grid()
            ax2.plot(x2, y2)
            fig.canvas.draw()

        theta = (theta + 10) % 360  # change offset angle for curve shift on Graph

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
            sg.popup('Project 2A ENSEA',
                     'Trombone modifying sound API ',
                     keep_on_top=True)
        elif event == 'Edit Me':
            sg.execute_editor(__file__)
        elif event == 'Versions':
            sg.popup_scrolled(__file__, sg.get_versions(), keep_on_top=True, non_blocking=True)
    window.close()
    exit(0)


if __name__ == '__main__':
    sg.theme('black')
    main()
