#This stands for pythontexttospeech

import pyttsx3 as speech_convertor
import tkinter as gui
from tkinter import filedialog, messagebox
import gtts as g_translate
from playsound import playsound
import os
import PyPDF2
from PIL import ImageTk, Image

if __name__ == '__main__':

    #Defining the main function that is text to speech function
    def workingpart(files):

        for file in files:

            for keys in apps_dict:
                if file in apps_dict[keys]:
                    if keys == 'Tamil':
                        flag = 1
                    else:
                        flag = 0

            if '.pdf' in file:
                pdf = 1
            else:
                pdf = 0

            if flag == 0 and pdf == 0:
                with open(file, 'r') as f:
                    Content = f.read()
            elif pdf == 0:
                with open(file, 'r', encoding="utf-8") as f:
                    Content = f.read()


            #We are reading the text file which contains content in Tamil
            #with open('Tamil_Sample.txt','r', encoding="utf-8") as f:
                #Tamil_content = f.read()

            #We are reading the text file which contains content in English
            #with open('sample.txt','r') as f:
                #English_content = f.read()
            #print(content)


            if pdf == 1:
                #The below set of code is for reading PDF file
    
                pdf_content = open(file,'rb')

                #creating a pdf reader object
                pdfReader = PyPDF2.PdfFileReader(pdf_content)

                #printing number of pages in pdf file
                print(pdfReader.numPages)

                #creating a page object
                for i in range(0,pdfReader.numPages):

                    pageObj = pdfReader.getPage(i)
                #extracting text from page
                    if i == 0:
                        ext_pdf = pageObj.extractText()
                    else:
                        ext_pdf = ext_pdf+pageObj.extractText()
                print(ext_pdf)
                Content = ext_pdf



            #Here we are calling the main function from pyttsx3 module
            main_speech_func = speech_convertor.init()

            #This is just for ref, we are reading the voices in this module
            assit_voice = main_speech_func.getProperty('voices')

            #for voice in assit_voice:
            #    print(voice)

            #print(assit_voice[0].id)
            #print(assit_voice[1].id)
            #print(assit_voice[2].id)
            #print(assit_voice[3].id)


            #Choosing voice type
            main_speech_func.setProperty('voice',assit_voice[1].id)

            #defining voice rate. By default its value is 200
            assit_rate = main_speech_func.getProperty('rate')
            #print(assit_rate)
            main_speech_func.setProperty('rate',170)

            if flag == 0:
                #Finally reading our content
                main_speech_func.say("Hello Reader...I'm Alice...lets get into our content")
                main_speech_func.say(Content)
                main_speech_func.runAndWait()

            else:
                #This section is defined for reading tamil content using Google translator API

                tts = g_translate.gTTS(Content, lang='ta')
                tts.save('Tamil_Sample.mp3')
                playsound('Tamil_Sample.mp3')
                os.remove('Tamil_Sample.mp3')

                #main_speech_func.say(content)
                #main_speech_func.runAndWait()

    apps_dict = {'Tamil':[],'English':[]}
    apps = []

    def popup():
        answer = messagebox.askquestion("Confirm","Whether the content is in Tamil?")
        print(answer)
        return answer



    #defining functionality of select button
    def Pick_file():

        for widget in frame.winfo_children():
            widget.destroy()

        FileName = filedialog.askopenfilename(initialdir='/', title='Select File', filetypes=(('text','.txt'),
                                                                                         ('document','.docx'),
                                                                                              ('PDF','.pdf')))
        if FileName:
            choice = popup()
            apps.append(FileName)
            if choice == 'yes':
                apps_dict['Tamil'].append(FileName)
            else:
                apps_dict['English'].append(FileName)
            print(apps)

        for app in apps:
            entry = gui.Label(frame, text=app, anchor="center", fg='black')
            entry.pack()


    #defining functionality for the render button
    def converttospeech():

        workingpart(apps)
        print("Completed")


    #defining functionality of clear button
    def clrhistory():

        apps.clear()

        for keys in apps_dict:
            apps_dict[keys].clear()

        for widget in frame.winfo_children():
            widget.destroy()

        #Header = gui.Label(frame, text="Files to be converted", fg="black")
        #Header.pack()


    print("GUI---part")
    root = gui.Tk()
    root.geometry("500x550")

    #Main window ie base layer
    gui_window = gui.Canvas(root, height=500, width=550)
    gui_window.pack(fill="both", expand=True)

    #Blending Image to the bg of application
    BackGroundImage = ImageTk.PhotoImage(file='BackGround.jpeg')
    gui_window.create_image(0, 0, image=BackGroundImage, anchor='nw')

    #This function is to dynamaically resize the bg according to the window size
    def resize_image(e):
        global bg, resized_bg, final_bg
        new_width = e.width
        new_height = e.height
        bg = Image.open('BackGround.jpeg')
        resized_bg = bg.resize((new_width, new_height), Image.ANTIALIAS)
        final_bg = ImageTk.PhotoImage(resized_bg)
        gui_window.create_image(0, 0, image=final_bg, anchor='nw')


    #functional frame for the application
    frame = gui.Frame(root, bg='white')
    frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
    #frame.pack()

    Header = gui.Frame(root)
    Header.place(relx=0.5, rely=0.05, relwidth=0.8, relheight=0.05, anchor='n')

    HeaderLabel = gui.Label(Header, text='List of Files to be converted')
    HeaderLabel.pack()



    #Defining Several buttons for the application
    Select_File = gui.Button(root, text="Select", fg="blue", bg="white", command=Pick_file)
    Select_File.pack(side = gui.LEFT)

    Convertor = gui.Button(root, text="Render", fg="green", bg="white", command=converttospeech)
    Convertor.pack(side = gui.RIGHT)

    Refresh = gui.Button(root, text="Clear", fg="red", bg="white", cursor='exchange', command=clrhistory)
    Refresh.pack()

    #This method will pass the altered size of windows to resize_image function
    root.bind('<Configure>', resize_image)
    #Executing the main program
    root.mainloop()

