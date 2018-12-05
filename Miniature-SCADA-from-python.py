##BERES 100%
from tkinter import *
import time
import sqlite3
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
style.use('fivethirtyeight')


class StopWatch(Frame):  
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()               
        self.makeWidgets()
        self.penampilan()

    def makeWidgets(self):                         
        """ Make the time label. """
        l = Label(self, textvariable=self.timestr) #membuat tabel untuk memperlihatkan waktu
        self._setTime(self._elapsedtime)
##        l.pack(fill=X, expand=NO, pady=2, padx=2)
        l.grid(row = 0,column = 9)
    
    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    
    def _setTime(self, elap):
        """ Set the time string to Jam:Minutes:Seconds:Hundreths """
        hours = int(elap/3600)
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d:%02d' % (hours,minutes, seconds, hseconds))
        
    def Start(self):
##      Tempat Untuk Mengontrol LED
        GPIO.setmode(GPIO.BCM)
        pin1 = 5
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.output(5,GPIO.HIGH)
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
    
    def Stop(self):                                    
##      Tempat untuk mengontrol LED
        GPIO.setmode(GPIO.BCM)
        pin1 = 5
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.output(5,GPIO.LOW)
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
##Mengambil data waktu dari label
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
            
##Manipulasi string menjadi data detik atau menit
            
            menit = int(self._elapsedtime/60)
            detik = int(self._elapsedtime - menit*60.0)
            data_detik = menit * 60 + detik
            a = "%02i:%02i"%(menit,detik)
            b = date.today()
            x = str(b)
            print(a)
            print(b)
            self._elapsedtime = 0.0
            conn = sqlite3.connect('percobaan-database-pkm.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS Database1(tanggal TEXT, lama TEXT,detik INTEGER)')
            c.execute("INSERT INTO Database1(tanggal,lama,detik)VALUES(?,?,?)",(b,a,data_detik))
            
##Membuat Tabel baru khusus untuk Grafik
            c.execute('CREATE TABLE IF NOT EXISTS Grafik1(Tanggal_grafik TEXT, lama_detik INTEGER)')
            
##Mengambil data dari tabel khusus grafik
            c.execute("SELECT max(Tanggal_grafik) from Grafik1")
            for baris_terakhir in c.fetchone() :
                print(baris_terakhir)
            print(' ')   
            tanggal_terakhir = baris_terakhir
            print('x = ', x)
            print(tanggal_terakhir)
            if (tanggal_terakhir == x) :
                c.execute("SELECT * FROM Grafik1 order by Tanggal_grafik DESC LIMIT 1")
                baris_terakhir_grafik = c.fetchone()
                detik_terakhir = baris_terakhir_grafik[1]
                print(' ')
                print(detik_terakhir)
                
                detik_total_baru = data_detik + detik_terakhir

                print(' ')
                print(detik_total_baru)
                c.execute("UPDATE Grafik1 SET lama_detik=(?) WHERE lama_detik=(?)",[detik_total_baru, detik_terakhir])
                conn.commit()

            else :
                c.execute("INSERT INTO Grafik1 VALUES(?,?)",[b , data_detik])
                conn.commit()
                
            conn.commit()
            c.close()
            conn.close()
            
            
    def Reset(self):                                
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)

##membuat graphic dengan data dari Database 1
    def graphic1(self):
        conn = sqlite3.connect('percobaan-database-pkm.db')
        c = conn.cursor()
        c.execute('SELECT Tanggal_grafik,lama_detik FROM Grafik1')
        Tanggal_grafik = []
        lama_detik = []
        for row in c.fetchall() :
##            print(row[0])
##            print(datetome
            Tanggal_grafik.append(row[0])
            lama_detik.append(row[1])
        plt.plot_date(Tanggal_grafik, lama_detik, "-")
        plt.show()
        conn.commit()
        c.close()
        conn.close()
##Membuat fungsi untuk memperlihatkan data yang ada pada sebuah tabel secara khusus
    def lihat_data(self):
        print('*'*25,"Data Pada mesin 1",25*'*')
        conn = sqlite3.connect('percobaan-database-pkm.db')
        c = conn.cursor()
        c.execute('SELECT tanggal,lama FROM Database1')
        [print(row) for row in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()

##Mencoba untuk merapihkan penampilan dari gui
    def penampilan(self):
        Button( text='Nyalakan', command=self.Start,bg='green').grid(row=0, column=1)
        Button( text='Matikan', command=self.Stop, bg ='red').grid(row=0, column=2)
        Button( text='Reset', command=self.Reset,bg ='blue').grid(row=0, column=3)
        Button( text='grafis', command=self.graphic1).grid(row=0, column=4)
        Button( text='History', command=self.lihat_data).grid(row=0, column=5)
        Button( text='Quit', command=quit).grid(row=0, column=6)




















        
        
class StopWatch2(Frame):  
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()               
        self.makeWidgets()
        self.penampilan()
        
        
    def makeWidgets(self):                         
        """ Make the time label. """
        l = Label(self, textvariable=self.timestr) #membuat tabel untuk memperlihatkan waktu
        self._setTime(self._elapsedtime)
##        l.pack(fill=X, expand=NO, pady=2, padx=2)
        l.grid(row=1 ,column =8)
        
    
    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    
    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        hours = int(elap/3600)
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d:%02d' % (hours,minutes, seconds, hseconds))
        
    def Start(self):
        GPIO.setmode(GPIO.BCM)
        pin1 = 6
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.output(6,GPIO.HIGH)
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
    
    def Stop(self):
        GPIO.setmode(GPIO.BCM)
        pin1 = 6
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.output(6,GPIO.LOW)
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
##Mengambil data waktu dari label
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
            
##Manipulasi string menjadi data detik atau menit
            
            menit = int(self._elapsedtime/60)
            detik = int(self._elapsedtime - menit*60.0)
            data_detik = menit * 60 + detik
            a = "%02i:%02i"%(menit,detik)
            b = date.today()
##Mengubah date type menjadi string
            x = str(b)
            print(a)
            print(b)
            self._elapsedtime = 0.0
            conn = sqlite3.connect('percobaan-database-pkm.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS Database2(tanggal TEXT, lama TEXT,detik INTEGER)')
            c.execute("INSERT INTO Database2(tanggal,lama,detik)VALUES(?,?,?)",(b,a,data_detik))
            
##Membuat Tabel baru khusus untuk Grafik
            c.execute('CREATE TABLE IF NOT EXISTS Grafik2(Tanggal_grafik TEXT, lama_detik INTEGER)')
            
##Mengambil data dari tabel khusus grafik
            c.execute("SELECT max(Tanggal_grafik) from Grafik2")
            for baris_terakhir in c.fetchone() :
                print(baris_terakhir)
            print(' ')   
            tanggal_terakhir = baris_terakhir
            print('x = ', x)
            print(tanggal_terakhir)
            if (tanggal_terakhir == x) :
                c.execute("SELECT * FROM Grafik2 order by Tanggal_grafik DESC LIMIT 1")
                baris_terakhir_grafik = c.fetchone()
                detik_terakhir = baris_terakhir_grafik[1]
                print(' ')
                print(detik_terakhir)
                
                detik_total_baru = data_detik + detik_terakhir

                print(' ')
                print(detik_total_baru)
                c.execute("UPDATE Grafik2 SET lama_detik=(?) WHERE lama_detik=(?)",[detik_total_baru, detik_terakhir])
                conn.commit()

            else :
                c.execute("INSERT INTO Grafik2 VALUES(?,?)",[b , data_detik])
                conn.commit()
                
            conn.commit()
            c.close()
            conn.close()
            
            
    def Reset(self):                                
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)
        
    def graphic2(self):
        conn = sqlite3.connect('percobaan-database-pkm.db')
        c = conn.cursor()
        c.execute('SELECT Tanggal_grafik,lama_detik FROM Grafik2')
        Tanggal_grafik = []
        lama_detik = []
        for row in c.fetchall() :
##            print(row[0])
##            print(datetome
            Tanggal_grafik.append(row[0])
            lama_detik.append(row[1])
        plt.plot_date(Tanggal_grafik, lama_detik, "-")
        plt.show()
        conn.commit()
        c.close()
        conn.close()

    def lihat_data(self):
        print('*'*25,"Data Pada mesin 2",25*'*')
        conn = sqlite3.connect('percobaan-database-pkm.db')
        c = conn.cursor()
        c.execute('SELECT tanggal,lama FROM Database2')
        [print(row) for row in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        
    def penampilan(self):
        Button( text='Nyalakan', command=self.Start,bg='green').grid(row=1, column=1)
        Button( text='Matikan', command=self.Stop, bg ='red').grid(row=1, column=2)
        Button( text='Reset', command=self.Reset,bg ='blue').grid(row=1, column=3)
        Button( text='grafis', command=self.graphic2).grid(row=1, column=4)
        Button( text='History', command=self.lihat_data).grid(row=1, column=5)
##        Button( text='grafis', command=self.graphic).grid(row=1, column=3)
##        Button( text='lihat data', command=self.lihat_data).grid(row=1, column=4)
##        Button( text='Quit', command=quit).grid(row=0, column=5)






















        

class StopWatch3(Frame):  
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()               
        self.makeWidgets()
        self.penampilan()

    def makeWidgets(self):                         
        """ Make the time label. """
        l = Label(self, textvariable=self.timestr) #membuat tabel untuk memperlihatkan waktu
        self._setTime(self._elapsedtime)
##        l.pack(fill=X, expand=NO, pady=2, padx=2)
        l.grid(row=2 ,column =6)
    
    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    
    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        hours = int(elap/3600)
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d:%02d' % (hours,minutes, seconds, hseconds))
        
    def Start(self):
        GPIO.setmode(GPIO.BCM)
        pin1 = 13
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.output(13,GPIO.HIGH)
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
    
    def Stop(self):
        GPIO.setmode(GPIO.BCM)
        pin1 = 13
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.output(13,GPIO.LOW)
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
##Mengambil data waktu dari label
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
            
##Manipulasi string menjadi data detik atau menit
            
            menit = int(self._elapsedtime/60)
            detik = int(self._elapsedtime - menit*60.0)
            data_detik = menit * 60 + detik
            a = "%02i:%02i"%(menit,detik)
            b = date.today()
            x = str(b)
            print(a)
            print(b)
            self._elapsedtime = 0.0
            conn = sqlite3.connect('percobaan-database-pkm.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS Database3(tanggal TEXT, lama TEXT,detik INTEGER)')
            c.execute("INSERT INTO Database3(tanggal,lama,detik)VALUES(?,?,?)",(b,a,data_detik))
            
##Membuat Tabel baru khusus untuk Grafik
            c.execute('CREATE TABLE IF NOT EXISTS Grafik3(Tanggal_grafik TEXT, lama_detik INTEGER)')
            
##Mengambil data dari tabel khusus grafik
            c.execute("SELECT max(Tanggal_grafik) from Grafik3")
            for baris_terakhir in c.fetchone() :
                print(baris_terakhir)
            print(' ')   
            tanggal_terakhir = baris_terakhir
            print('x = ', x)
            print(tanggal_terakhir)
            if (tanggal_terakhir == x) :
                c.execute("SELECT * FROM Grafik3 order by Tanggal_grafik DESC LIMIT 1")
                baris_terakhir_grafik = c.fetchone()
                detik_terakhir = baris_terakhir_grafik[1]
                print(' ')
                print(detik_terakhir)
                
                detik_total_baru = data_detik + detik_terakhir

                print(' ')
                print(detik_total_baru)
                c.execute("UPDATE Grafik3 SET lama_detik=(?) WHERE lama_detik=(?)",[detik_total_baru, detik_terakhir])
                conn.commit()

            else :
                c.execute("INSERT INTO Grafik3 VALUES(?,?)",[b , data_detik])
                conn.commit()
                
            conn.commit()
            c.close()
            conn.close()
            
            
    def Reset(self):                                
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)

    def graphic3(self):
        conn = sqlite3.connect('percobaan-database-pkm.db')
        c = conn.cursor()
        c.execute('SELECT Tanggal_grafik,lama_detik FROM Grafik3')
        Tanggal_grafik = []
        lama_detik = []
        for row in c.fetchall() :
##            print(row[0])
##            print(datetome
            Tanggal_grafik.append(row[0])
            lama_detik.append(row[1])
        plt.plot_date(Tanggal_grafik, lama_detik, "-")
        plt.show()
        conn.commit()
        c.close()
        conn.close()

    def lihat_data(self):
        print('*'*25,"Data Pada mesin 3",25*'*')
        conn = sqlite3.connect('percobaan-database-pkm.db')
        c = conn.cursor()
        c.execute('SELECT tanggal,lama FROM Database3')
        [print(row) for row in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()
        
    def penampilan(self):
        Button( text='Nyalakan', command=self.Start,bg='green').grid(row=2, column=1)
        Button( text='Matikan', command=self.Stop, bg ='red').grid(row=2, column=2)
        Button( text='Reset', command=self.Reset,bg ='blue').grid(row=2, column=3)
        Button( text='grafis', command=self.graphic3).grid(row=2, column=4)
        Button( text='History', command=self.lihat_data).grid(row=2, column=5)
##        Button( text='grafis', command=self.graphic).grid(row=1, column=3)
##        Button( text='lihat data', command=self.lihat_data).grid(row=1, column=4)
##        Button( text='Quit', command=quit).grid(row=0, column=5)

















class StopWatch4(Frame):  
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()               
        self.makeWidgets()
        self.penampilan()

    def makeWidgets(self):                         
        """ Make the time label. """
        l = Label(self, textvariable=self.timestr) #membuat tabel untuk memperlihatkan waktu
        self._setTime(self._elapsedtime)
##        l.pack(fill=X, expand=NO, pady=2, padx=2)
        l.grid(row = 3,column = 8)
    
    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    
    def _setTime(self, elap):
        """ Set the time string to Jam:Minutes:Seconds:Hundreths """
        hours = int(elap/3600)
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d:%02d' % (hours,minutes, seconds, hseconds))
        
    def Start(self):
##      Tempat Untuk Mengontrol LED
        GPIO.setmode(GPIO.BCM)
        pin1 = 19
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.output(19,GPIO.HIGH)
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
    
    def Stop(self):                                    
##      Tempat untuk mengontrol LED
        GPIO.setmode(GPIO.BCM)
        pin1 = 19
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.output(19,GPIO.LOW)
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
##Mengambil data waktu dari label
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
            
##Manipulasi string menjadi data detik atau menit
            
            menit = int(self._elapsedtime/60)
            detik = int(self._elapsedtime - menit*60.0)
            data_detik = menit * 60 + detik
            a = "%02i:%02i"%(menit,detik)
            b = date.today()
            x = str(b)
            print(a)
            print(b)
            self._elapsedtime = 0.0
            conn = sqlite3.connect('percobaan-database-pkm.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS Database4(tanggal TEXT, lama TEXT,detik INTEGER)')
            c.execute("INSERT INTO Database4(tanggal,lama,detik)VALUES(?,?,?)",(b,a,data_detik))
            
##Membuat Tabel baru khusus untuk Grafik
            c.execute('CREATE TABLE IF NOT EXISTS Grafik4(Tanggal_grafik TEXT, lama_detik INTEGER)')
            
##Mengambil data dari tabel khusus grafik
            c.execute("SELECT max(Tanggal_grafik) from Grafik4")
            for baris_terakhir in c.fetchone() :
                print(baris_terakhir)
            print(' ')   
            tanggal_terakhir = baris_terakhir
            print('x = ', x)
            print(tanggal_terakhir)
            if (tanggal_terakhir == x) :
                c.execute("SELECT * FROM Grafik4 order by Tanggal_grafik DESC LIMIT 1")
                baris_terakhir_grafik = c.fetchone()
                detik_terakhir = baris_terakhir_grafik[1]
                print(' ')
                print(detik_terakhir)
                
                detik_total_baru = data_detik + detik_terakhir

                print(' ')
                print(detik_total_baru)
                c.execute("UPDATE Grafik4 SET lama_detik=(?) WHERE lama_detik=(?)",[detik_total_baru, detik_terakhir])
                conn.commit()

            else :
                c.execute("INSERT INTO Grafik4 VALUES(?,?)",[b , data_detik])
                conn.commit()
                
            conn.commit()
            c.close()
            conn.close()
            
            
    def Reset(self):                                
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)

##membuat graphic dengan data dari Database4

    def graphic4(self):
        conn = sqlite3.connect('percobaan-database-pkm.db')
        c = conn.cursor()
        c.execute('SELECT Tanggal_grafik,lama_detik FROM Grafik4')
        Tanggal_grafik = []
        lama_detik = []
        for row in c.fetchall() :
##            print(row[0])
##            print(datetome
            Tanggal_grafik.append(row[0])
            lama_detik.append(row[1])
        plt.plot_date(Tanggal_grafik, lama_detik, "-")
        plt.show()
        conn.commit()
        c.close()
        conn.close()
##Membuat fungsi untuk memperlihatkan data yang ada pada sebuah tabel secara khusus
    def lihat_data(self):
        print('*'*25,"Data Pada mesin 4",25*'*')
        conn = sqlite3.connect('percobaan-database-pkm.db')
        c = conn.cursor()
        c.execute('SELECT tanggal,lama FROM Database4')
        [print(row) for row in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()

##Mencoba untuk merapihkan penampilan dari gui
    def penampilan(self):
        Button( text='Nyalakan', command=self.Start,bg='green').grid(row=3, column=1)
        Button( text='Matikan', command=self.Stop, bg ='red').grid(row=3, column=2)
        Button( text='Reset', command=self.Reset,bg ='blue').grid(row=3, column=3)
        Button( text='grafis', command=self.graphic4).grid(row=3, column=4)
        Button( text='History', command=self.lihat_data).grid(row=3, column=5)
##        Button( text='Quit', command=quit).grid(row=3, column=5)





















class StopWatch5(Frame):  
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()               
        self.makeWidgets()
        self.penampilan()

    def makeWidgets(self):                         
        """ Make the time label. """
        l = Label(self, textvariable=self.timestr) #membuat tabel untuk memperlihatkan waktu
        self._setTime(self._elapsedtime)
##        l.pack(fill=X, expand=NO, pady=2, padx=2)
        l.grid(row = 4,column = 8)
    
    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    
    def _setTime(self, elap):
        """ Set the time string to Jam:Minutes:Seconds:Hundreths """
        hours = int(elap/3600)
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d:%02d' % (hours,minutes, seconds, hseconds))
        
    def Start(self):
##      Tempat Untuk Mengontrol LED
        GPIO.setmode(GPIO.BCM)
        pin1 = 23
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.output(23,GPIO.HIGH)
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
    
    def Stop(self):                                    
##      Tempat untuk mengontrol LED
        GPIO.setmode(GPIO.BCM)
        pin1 = 23
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.output(23,GPIO.LOW)
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
##Mengambil data waktu dari label
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
            
##Manipulasi string menjadi data detik atau menit
            
            menit = int(self._elapsedtime/60)
            detik = int(self._elapsedtime - menit*60.0)
            data_detik = menit * 60 + detik
            a = "%02i:%02i"%(menit,detik)
            b = date.today()
            x = str(b)
            print(a)
            print(b)
            self._elapsedtime = 0.0
            conn = sqlite3.connect('percobaan-database-pkm.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS Database5(tanggal TEXT, lama TEXT,detik INTEGER)')
            c.execute("INSERT INTO Database5(tanggal,lama,detik)VALUES(?,?,?)",(b,a,data_detik))
            
##Membuat Tabel baru khusus untuk Grafik
            c.execute('CREATE TABLE IF NOT EXISTS Grafik5(Tanggal_grafik TEXT, lama_detik INTEGER)')
            
##Mengambil data dari tabel khusus grafik
            c.execute("SELECT max(Tanggal_grafik) from Grafik5")
            for baris_terakhir in c.fetchone() :
                print(baris_terakhir)
            print(' ')   
            tanggal_terakhir = baris_terakhir
            print('x = ', x)
            print(tanggal_terakhir)
            if (tanggal_terakhir == x) :
                c.execute("SELECT * FROM Grafik5 order by Tanggal_grafik DESC LIMIT 1")
                baris_terakhir_grafik = c.fetchone()
                detik_terakhir = baris_terakhir_grafik[1]
                print(' ')
                print(detik_terakhir)
                
                detik_total_baru = data_detik + detik_terakhir

                print(' ')
                print(detik_total_baru)
                c.execute("UPDATE Grafik5 SET lama_detik=(?) WHERE lama_detik=(?)",[detik_total_baru, detik_terakhir])
                conn.commit()

            else :
                c.execute("INSERT INTO Grafik5 VALUES(?,?)",[b , data_detik])
                conn.commit()
                
            conn.commit()
            c.close()
            conn.close()
            
            
    def Reset(self):                                
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)

##membuat graphic dengan data dari Database5
    def graphic5(self):
        conn = sqlite3.connect('percobaan-database-pkm.db')
        c = conn.cursor()
        c.execute('SELECT Tanggal_grafik,lama_detik FROM Grafik5')
        Tanggal_grafik = []
        lama_detik = []
        for row in c.fetchall() :
##            print(row[0])
##            print(datetome
            Tanggal_grafik.append(row[0])
            lama_detik.append(row[1])
        plt.plot_date(Tanggal_grafik, lama_detik, "-")
        plt.show()
        conn.commit()
        c.close()
        conn.close()
        
##Membuat fungsi untuk memperlihatkan data yang ada pada sebuah tabel secara khusus
    def lihat_data(self):
        print('*'*25,"Data Pada mesin 5",25*'*')
        conn = sqlite3.connect('percobaan-database-pkm.db')
        c = conn.cursor()
        c.execute('SELECT tanggal,lama FROM Database5')
        [print(row) for row in c.fetchall()]
        conn.commit()
        c.close()
        conn.close()

##Mencoba untuk merapihkan penampilan dari gui
    def penampilan(self):
        Button( text='Nyalakan', command=self.Start,bg='green').grid(row=4, column=1)
        Button( text='Matikan', command=self.Stop, bg ='red').grid(row=4, column=2)
        Button( text='Reset', command=self.Reset,bg ='blue').grid(row=4, column=3)
        Button( text='grafis', command=self.graphic5).grid(row=4, column=4)
        Button( text='History', command=self.lihat_data).grid(row=4, column=5)
##        Button( text='Quit', command=quit).grid(row=3, column=5)




        
        


        
def main():
    root = Tk()
    
    label0=Label(root ,padx=18,pady = 18,text='CONTROL DAN MONITORING',font=72,fg='Black', relief=RAISED)
    label0.grid(row = 5, column = 10)

    label17=Label(root ,text='PKM KARSA CIPTA',font=15,fg='Black', relief=RAISED)
    label17.grid(row = 0, column = 11)
    
    label17=Label(root ,text='created by Amar',font=0.2,fg='Black', relief=RAISED)
    label17.grid(row = 6, column = 11)
    
    label1=Label(root ,padx=18,pady = 18,text='Control Dan Monitor Mesin 1',font=72,fg='Black', relief=RAISED).grid(row=0, column=0)
    sw = StopWatch(root)
    sw.grid(row = 0,column= 9)

    label2=Label(root ,padx=18,pady = 18,text='Control Dan Monitor Mesin 2',font=72,fg='Black', relief=RAISED).grid(row=1, column=0)
    sw2 = StopWatch2(root)
    sw2.grid(row = 1,column= 9)

    label3=Label(root ,padx=18,pady = 18,text='Control Dan Monitor Mesin 3',font=72,fg='Black', relief=RAISED).grid(row=2, column=0)
    sw3 = StopWatch3(root)
    sw3.grid(row = 2,column= 9)
    

    label4=Label(root ,padx=18,pady = 18,text='Control Dan Monitor Mesin 4',font=72,fg='Black', relief=RAISED).grid(row=3, column=0)
    sw4 = StopWatch4(root)
    sw4.grid(row = 3,column= 9)


    label5=Label(root ,padx=18,pady = 18,text='Control Dan Monitor Mesin 5',font=72,fg='Black', relief=RAISED).grid(row=4, column=0)
    sw5 = StopWatch5(root)
    sw5.grid(row = 4,column= 9)
    
    root.mainloop()

if __name__ == '__main__':
    main()
