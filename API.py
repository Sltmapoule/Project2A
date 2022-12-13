import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
import matplotlib.figure as fig

matplotlib.use('TkAgg')

input_sig = fig.Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
input_sig.add_subplot().plot(t, 2 * np.sin(2 * np.pi * t))  # Ajouter les graphs ici
input_spectre = fig.Figure(figsize=(5, 4), dpi=100)
input_spectre.add_subplot().plot(t, 4 * np.cos(2 * np.pi * t))

output_sig = fig.Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
output_sig.add_subplot().plot(t, 2 * np.sin(2 * np.pi * t))  # Ajouter les graphs ici
output_spectre = fig.Figure(figsize=(5, 4), dpi=100)
output_spectre.add_subplot().plot(t, 4 * np.cos(2 * np.pi * t))


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
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
        [sg.Text('Input Signal'), sg.Text('Input spectre', justification='center', expand_x=True)],
        [sg.Canvas(key='-INSIG-'), sg.Canvas(key='-INSP-')]
    ]

    output_layout = [
        [sg.Text('Output Signal'), sg.Text('Output Spectre', justification='center', expand_x=True)],
        [sg.Canvas(key='-OUTSIG-'), sg.Canvas(key='-OUTSP-')]
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
    draw_figure(window['-OUTSIG-'].TKCanvas, output_sig)
    draw_figure(window['-OUTSP-'].TKCanvas, output_spectre)

    while True:
        fg = draw_figure(window['-INSIG-'].TKCanvas, input_sig)
        fg2 = draw_figure(window['-INSP-'].TKCanvas, input_spectre)

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
            sg.popup('Project 2A ENSEA',
                     'Trombone modifying sound API ',
                     keep_on_top=True)
        elif event == 'Edit Me':
            sg.execute_editor(__file__)
        elif event == 'Versions':
            sg.popup_scrolled(__file__, sg.get_versions(), keep_on_top=True, non_blocking=True)
        fg.get_tk_widget().pack_forget()
        fg2.get_tk_widget().pack_forget()
    window.close()
    exit(0)


if __name__ == '__main__':
    sg.theme('black')
    main()
