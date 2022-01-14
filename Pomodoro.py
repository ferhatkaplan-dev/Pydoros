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

        self.anaPencere()

        self.pencere.mainloop()

    def anaPencere(self):
        self.kontrol = False
        self.say = 2400
        self.pencere = tk.Tk()
        self.pencere.title('Pomodoro')
        self.pencere.resizable(width=False, height=False)
        self.pencere.geometry('412x510')

        self.c = tk.Canvas(bg='white', width=512, height=512)
        self.c.place(x=0, y=0)

        self.dosya = tk.PhotoImage(file='./images/ss2.png')
        self.imaj = self.c.create_image(210, 256, image=self.dosya)

        # ana objeler
        self.mesajOlustur()
        self.istatistik()
        self.sureOlustur()
        self.baslaButtonOlustur()

    def mesajOlustur(self):
        self.yazı = tk.Label(text='Hazır',
                             bg='white',
                             fg='black',
                             font='Verdana 16 bold')
        self.yazı.place(x=175, y=40)

    def sureOlustur(self):
        self.labelSaniye = tk.Label(text='00',
                                    bg='#c31c28',
                                    fg='white',
                                    font='Verdana 22 bold')
        self.labelSaniye.place(x=240, y=233)

        self.labelDakika = tk.Label(text=str(int(self.say / 60)),
                                    bg='#c31c28',
                                    fg='white',
                                    font='Verdana 22 bold')
        self.labelDakika.place(x=132, y=235)

    def baslaButtonOlustur(self):
        self.icon2 = tk.PhotoImage(file='./images/icon2.png')
        self.baslaButton = tk.Button(text='başla',
                                     bg='yellow',
                                     image=self.icon2,
                                     command=self.komut)
        self.baslaButton.place(x=190, y=450)

    def durdurButtonOlustur(self):
        self.icon = tk.PhotoImage(file='./images/icon.png')
        self.b2 = tk.Button(text='başla',
                            bg='yellow',
                            image=self.icon,
                            command=self.durdur)
        self.b2.place(x=190, y=450)

    def istatistik(self):
        self.b2 = tk.Button(text='İstatistik',
                            bg='yellow',
                            command=self.ToplamGorunum)
        self.b2.place(x=0, y=485)

    def durdur(self):
        self.b2.destroy()
        self.labelSaniye.destroy()
        self.labelDakika.destroy()

        self.sureOlustur()
        self.kontrol = True
        self.baslaButtonOlustur()
        self.dosya = tk.PhotoImage(file='./images/ss1.png')
        self.imaj = self.c.create_image(210, 256, image=self.dosya)
        self.yazı['text'] = 'Hazır'
        self.yazı['bg'] = '#515151'
        self.yazı['fg'] = 'white'

        self.Oku((self.say - self.k) / 60)

    def calısEkran(self):
        self.dosya['file'] = './images/ss.png'
        self.yazı['text'] = 'Çalış'
        self.yazı['bg'] = '#ff8500'
        self.yazı['fg'] = 'white'

        self.baslaButton.destroy()
        media1.play()
        time.sleep(3)
        media1.stop()
        self.durdurButtonOlustur()

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

    def ToplamGorunum(self):
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
        self.kontrol = False
        self.calısEkran()

        yield self.pencere
        for self.k in range(self.say, -1, -1):
            if self.kontrol:
                break
            self.labelSaniye["text"] = str(self.k % 60).zfill(2)
            self.labelDakika['text'] = str(self.k // 60).zfill(2)
            if self.k == 0:
                self.Oku(int(self.say / 60))
                self.b2.destroy()
                self.baslaButtonOlustur()
                self.dosya = tk.PhotoImage(file='./images/ss1.png')
                self.imaj = self.c.create_image(210, 256, image=self.dosya)
                media2.play()
                time.sleep(2)
                media2.stop()
                self.yazı['text'] = 'Bitti'
                self.yazı['bg'] = '#515151'
                self.yazı['fg'] = 'white'

            yield 1


Pomodoro()
