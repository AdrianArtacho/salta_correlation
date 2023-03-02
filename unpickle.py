import pickle
# import easygui
# import PySimpleGUI as sg


# layout = [[sg.Text("Choose a file: "), sg.FileBrowse()]]
# sg.theme("DarkTeal2")
# layout = [[sg.T("")], [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse()]]

# ###Building Window
# window = sg.Window('My File Browser', layout, size=(600,150))

# file_to_unpickle = easygui.fileopenbox()
# print("file_to_unpickle", file_to_unpickle)

# athletes_file = open("pickled_annotations.pkl", "rb")
athletes_file = open("person_data.pkl", "rb")
athletes = pickle.load(athletes_file)
athletes_file.close()
print(athletes)