import subprocess
import configparser
import tkinter as tk

TYPE_NOTE=True
DEFAULT_NOTEBOOK=""
BACKGROUND_COLOR_SELECTED=""
FONT_COLOR_SELECTED="#ffffff"

def config():
    global TYPE_NOTE
    global DEFAULT_NOTEBOOK
    global BACKGROUND_COLOR_SELECTED
    global FONT_COLOR_SELECTED
    global FONT_COLOR
    global BACKGROUND_COLOR
    global BACKGROUND_COLOR_WINDOW
    global BACKGROUND_COLOR_BUTTON
    global FONT_COLOR_BUTTON
    global BACKGROUND_COLOR_INPUT
    global FONT_COLOR_INPUT
    global BACKGROUND_COLOR_LABEL
    global FONT_COLOR_LABEL

    try:
        config = configparser.ConfigParser()
#        config.read('config.ini')
        config.read('/home/lucolombo/Documentos/proyectos/polybar-joplin/config.ini')
        try:
            TYPE_NOTE = config.getboolean('module/joplin','TYPE_NOTE')
        except KeyError:
            TYPE_NOTE=True
            print("KeyError - TYPE_NOTE: Defaulting to 'note'")
        try:
            DEFAULT_NOTEBOOK = config.get('module/joplin','DEFAULT_NOTEBOOK')
            print(DEFAULT_NOTEBOOK)
        except KeyError: 
            DEFAULT_NOTEBOOK = ''
            print("KeyError - DEFAULT_NOTEBOOK: Defaulting to 'None'")
        BACKGROUND_COLOR_SELECTED = "#"+config.get('module/joplin','BACKGROUND_COLOR_SELECTED')
        FONT_COLOR_SELECTED = "#"+config.get('module/joplin','FONT_COLOR_SELECTED')
        FONT_COLOR = "#"+config.get('module/joplin','FONT_COLOR')
        BACKGROUND_COLOR = "#"+config.get('module/joplin','BACKGROUND_COLOR')
        BACKGROUND_COLOR_WINDOW = "#"+config.get('module/joplin','BACKGROUND_COLOR_WINDOW')
        BACKGROUND_COLOR_BUTTON = "#"+config.get('module/joplin','BACKGROUND_COLOR_BUTTON')
        FONT_COLOR_BUTTON = "#"+config.get('module/joplin','FONT_COLOR_BUTTON')
        BACKGROUND_COLOR_INPUT = "#"+config.get('module/joplin','BACKGROUND_COLOR_INPUT')
        FONT_COLOR_INPUT = "#"+config.get('module/joplin','FONT_COLOR_INPUT')
        BACKGROUND_COLOR_LABEL = "#"+config.get('module/joplin','BACKGROUND_COLOR_LABEL')
        FONT_COLOR_LABEL = "#"+config.get('module/joplin','FONT_COLOR_LABEL')


    except Exception as e:
        print(str(e))
        print("config.ini file not found. Values set to default.")
        

def clean(item):
    return str(item)[2:-1].strip()

def get_notebook_list():
    notebooks = subprocess.check_output(['joplin', 'ls', '/']).splitlines()
    notebooks = list(map(clean, notebooks))
    return notebooks

def set_current_notebook(notebook):
    return subprocess.check_output(['joplin','use',notebook])

def create_note(content):
    print(content)
    subprocess.check_output(['joplin','mknote',content])

def create_todo(content):
    subprocess.check_output(['joplin','mktodo',content])

def create_note_in_notebook(note,notebook):
    global TYPE_NOTE
    try:
        set_current_notebook(notebook)
        if TYPE_NOTE:
            create_note(note)
        else:
            print("Estoy aqui")
            create_todo(note)
    except Exception as e:
        print("Error" + str(e))

def btn_status(listbox):
    print(listbox.get_selected())
    return "disabled"

def main():
    global DEFAULT_NOTEBOOK
    global BACKGROUND_COLOR_SELECTED
    global FONT_COLOR_SELECTED
    global FONT_COLOR
    global BACKGROUND_COLOR
    global BACKGROUND_COLOR_WINDOW
    global BACKGROUND_COLOR_BUTTON
    global FONT_COLOR_BUTTON
    global BACKGROUND_COLOR_INPUT
    global FONT_COLOR_INPUT
    global BACKGROUND_COLOR_LABEL
    global FONT_COLOR_LABEL

    try:
        window = tk.Tk()
        window.attributes('-type', 'dialog')
        window.title('polybar-joplin')
        window.configure(bg=BACKGROUND_COLOR_WINDOW)
        #window.geometry("300x200+10+20")
        
        tk.Label(window, text="Note:", background=BACKGROUND_COLOR_LABEL, foreground=FONT_COLOR_LABEL).pack(anchor="center")
        entry = tk.Text(window, width=22, height=5, bd=0, relief="flat", highlightthickness=0, background=BACKGROUND_COLOR_INPUT, foreground=FONT_COLOR_INPUT, cursor="xterm")
        entry.pack()
        print(DEFAULT_NOTEBOOK)
        print(len(DEFAULT_NOTEBOOK))

        if not DEFAULT_NOTEBOOK.strip():
            print("no default notebook")
            tk.Label(window, text="Notebook:", background=BACKGROUND_COLOR_LABEL, foreground=FONT_COLOR_LABEL).pack(anchor="center")
            listbox = tk.Listbox(window, bd=0, width=20, relief="ridge",highlightthickness=0,background=BACKGROUND_COLOR,foreground=FONT_COLOR,selectforeground=FONT_COLOR_SELECTED, selectbackground=BACKGROUND_COLOR_SELECTED)
            listbox.pack()

            notebooks = get_notebook_list()

            if len(notebooks) == 0:
                print("No notebook found")
            
            for item in notebooks:
                listbox.insert(tk.END, item)

            btn = tk.Button(window, bd=0, width=20, relief="flat", background=BACKGROUND_COLOR_BUTTON, foreground=FONT_COLOR_BUTTON, text="OK", command=lambda lb=listbox, e=entry: create_note_in_notebook(e.get("1.0",'end-1c'),lb.selection_get()))
        else:
            btn = tk.Button(window, bd=0, width=20, relief="flat", background=BACKGROUND_COLOR_BUTTON, foreground=FONT_COLOR_BUTTON, text="OK", command=lambda e=entry: create_note_in_notebook(e.get(),DEFAULT_NOTEBOOK))

        btn.pack()

        window.mainloop()
    except Exception as e:
        print(str(e))

config()       
main()
