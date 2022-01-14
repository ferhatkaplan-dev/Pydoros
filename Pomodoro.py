import tkinter as tk
import vlc
import time
import datetime
import json
import matplotlib.pyplot as plt

media1 = vlc.MediaPlayer(r"./sounds/Basla.mp3")
media2 = vlc.MediaPlayer(r"./sounds/tuturu_1.mp3")


class Pomodoro:

    def __init__(self):

        self.mainWindow()

        self.window.mainloop()

    def mainWindow(self):
        self.check = False
        self.count = 2400
        self.window = tk.Tk()
        self.window.title('Pomodoro')
        self.window.resizable(width=False, height=False)
        self.window.geometry('412x510')

        self.c = tk.Canvas(bg='white', width=512, height=512)
        self.c.place(x=0, y=0)

        self.imageFile = tk.PhotoImage(file='./images/ss2.png')
        self.imaj = self.c.create_image(210, 256, image=self.imageFile)

        # Main objects/
        self.messageText()
        self.statistics()
        self.timeCreate()
        self.startButtonCreate()

    def messageText(self):
        self.text = tk.Label(text='Hazır',
                             bg='white',
                             fg='black',
                             font='Verdana 16 bold')
        self.text.place(x=175, y=40)

    def timeCreate(self):
        self.labelSecond = tk.Label(text='00',
                                    bg='#c31c28',
                                    fg='white',
                                    font='Verdana 22 bold')
        self.labelSecond.place(x=240, y=233)

        self.labelMinute = tk.Label(text=str(int(self.count / 60)),
                                    bg='#c31c28',
                                    fg='white',
                                    font='Verdana 22 bold')
        self.labelMinute.place(x=132, y=235)

    def startButtonCreate(self):
        self.icon2 = tk.PhotoImage(file='./images/icon2.png')
        self.startButton = tk.Button(text='başla',
                                     bg='yellow',
                                     image=self.icon2,
                                     command=self.komut)
        self.startButton.place(x=190, y=450)

    def stopButtonCreate(self):
        self.icon = tk.PhotoImage(file='./images/icon.png')
        self.b2 = tk.Button(text='başla',
                            bg='yellow',
                            image=self.icon,
                            command=self.stop)
        self.b2.place(x=190, y=450)

    def statistics(self):
        self.b2 = tk.Button(text='İstatistik',
                            bg='yellow',
                            command=self.statisticsView)
        self.b2.place(x=0, y=485)

    def stop(self):
        self.b2.destroy()
        self.labelSecond.destroy()
        self.labelMinute.destroy()

        self.timeCreate()
        self.check = True
        self.startButtonCreate()
        self.imageFile = tk.PhotoImage(file='./images/ss1.png')
        self.imaj = self.c.create_image(210, 256, image=self.imageFile)
        self.text['text'] = 'Hazır'
        self.text['bg'] = '#515151'
        self.text['fg'] = 'white'

        self.Oku((self.count - self.k) / 60)

    def calısEkran(self):
        self.imageFile['file'] = './images/ss.png'
        self.text['text'] = 'Çalış'
        self.text['bg'] = '#ff8500'
        self.text['fg'] = 'white'

        self.startButton.destroy()
        media1.play()
        time.sleep(3)
        media1.stop()
        self.stopButtonCreate()

    def wait(f):

        def start(*args, **kwargs):
            g = f(*args, **kwargs)
            widget = next(g)

            def repeater():
                try:

                    widget.after(next(g) * 1000, repeater)
                except StopIteration:
                    pass

            repeater()

        return start

    def Oku(self, süre):
        tarih = {
            datetime.datetime.strftime(datetime.datetime.now(), '%x'): {
                "yil": datetime.datetime.strftime(datetime.datetime.now(),
                                                  '%Y'),
                "ay": datetime.datetime.strftime(datetime.datetime.now(),
                                                 '%m'),
                "gun": datetime.datetime.strftime(datetime.datetime.now(),
                                                  '%d'),
                "calisma": 0
            }
        }

        try:
            with open('veri.json', 'r') as f:
                veri = json.load(f)
        except FileNotFoundError:
            with open('veri.json', 'w') as f:
                veri = {}
                veri.update(tarih)
                json.dump(veri, f)

        if not datetime.datetime.strftime(datetime.datetime.now(),
                                          '%x') in veri:
            veri.update(tarih)
            with open('veri.json', 'w') as json_dosya:
                json.dump(veri, json_dosya)
        else:
            veri[datetime.datetime.strftime(datetime.datetime.now(),
                                            '%x')]["calisma"] += süre
            with open('veri.json', 'w') as json_dosya:
                json.dump(veri, json_dosya)

    def statisticsView(self):
        with open('veri.json') as f:
            veri = json.load(f)

        listeX = []
        listeXX = []

        listeY = []
        listeYY = []

        for i in veri:
            listeX.append(veri[i]["gun"])
            listeY.append(veri[i]["calisma"])

        if len(listeX) > 30:
            for i in range(len(listeX) - 30, len(listeX)):
                listeXX.append(listeX[i])
                listeYY.append(listeY[i])

        def medyanBul(vektor):
            vektor = sorted(vektor)
            veriAdedi = len(vektor)
            if veriAdedi % 2 == 1:
                return vektor[veriAdedi // 2]
            else:
                i = veriAdedi // 2
                return (vektor[i - 1] + vektor[i]) / 2

        def ortalamaBul(vektor):
            veriAdedi = len(vektor)
            if veriAdedi <= 1:
                return vektor[0]
            else:
                return sum(vektor) / veriAdedi

    # grafik

        plt.bar(listeXX, listeYY, color="orange")

        # başlık
        plt.title('POMODORO')

        # ortalama list oluştur.
        ortalamaLis = []
        medyaLis = []

        for i in listeX:
            ortalamaLis.append(ortalamaBul(listeY))
            medyaLis.append(medyanBul(listeY))

        # ortalama
        plt.plot(listeX,
                 ortalamaLis,
                 label=f"Ortalama : {int(ortalamaBul(listeY))}",
                 color="red")
        plt.plot(listeX,
                 medyaLis,
                 label=f"Medyan : {int(medyanBul(listeY))}",
                 color="green")

        plt.legend()
        plt.show()

    @wait
    def komut(self):
        self.check = False
        self.calısEkran()

        yield self.window
        for self.k in range(self.count, -1, -1):
            if self.check:
                break
            self.labelSecond["text"] = str(self.k % 60).zfill(2)
            self.labelMinute['text'] = str(self.k // 60).zfill(2)
            if self.k == 0:
                self.Oku(int(self.count / 60))
                self.b2.destroy()
                self.startButtonCreate()
                self.imageFile = tk.PhotoImage(file='./images/ss1.png')
                self.imaj = self.c.create_image(210, 256, image=self.imageFile)
                media2.play()
                time.sleep(2)
                media2.stop()
                self.text['text'] = 'Bitti'
                self.text['bg'] = '#515151'
                self.text['fg'] = 'white'

            yield 1


Pomodoro()
