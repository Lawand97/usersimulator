# view
from tkinter import *
from tkinter.ttk import Progressbar
from xlutils.copy import copy
from xlrd import open_workbook
import time
import PyChromeDevTools
import psutil
import threading
import xlsxwriter

class View(Tk):
    def __init__(self):
        Tk.__init__(self)
        #self.callback = callback
        # Fenster
        self.title("User simulator tool")
        self.geometry('260x150+400+100')
        # Entries
        #self.eA = Entry(master=self)
        #self.eA.insert(0, '12.7')
        #self.eA.place(x=20, y=20, width=50)
        #self.eB = Entry(master=self)
        #self.eB.insert(0, '-18')
        #self.eB.place(x=80, y=20, width=50)
        # Button
        self.bRechne = Button(master=self, text="Run Script", command=self.run)
        self.bRechne.place(x=20, y=50, width=70)
        # Label
        self.lC = Label(master=self, text= " Your used bandwith is " + str(0)  + " mb")
        self.lC.place(x=20, y=80)
        self.time = Label(master=self, text=" Total loading time is " + str(0) +" seconds")
        self.time.place(x=20, y=100)
        self.createconnection()
        self.openfile()
        self.createpro()
        self.testnr = 0
        self.workbook = xlsxwriter.Workbook('Results.xls')
        self.worksheet = self.workbook.add_worksheet()
        self.workbook.close()
        #self.p = Progressbar(self, orient=HORIZONTAL, length=200, mode="determinate", takefocus=True, maximum=50)
        #self.p.pack()

    def reset(self):
        self.lC = Label(master=self, text=" Your used bandwith is " + str(0) + " mb")
        self.lC.place(x=20, y=80)
        self.time = Label(master=self, text=" Total loading time is " + str(0) + " seconds")
        self.time.place(x=20, y=100)


    def createpro(self):
        self.p = Progressbar(self, orient=HORIZONTAL, length=200, mode="determinate", takefocus=True, maximum=self.num_lines)
        self.p.pack()

    def runscript(self):
        for i in range(100):
            time.sleep(0.1)
            self.lC = Label(master=self, text= " Your used bandwith is " + str(i)  + "  mb")
            self.lC.place(x=20, y=80)
            self.p.step()
            self.update()

    def run(self):
        self.reset()
        self.download_thread = threading.Thread(target=self.calculateusage)
        self.download_thread.do_run = True
        self.download_thread.start()
        self.berechne1()

    def createconnection(self):
        self.chrome = PyChromeDevTools.ChromeInterface()
        self.chrome.Network.enable()
        self.chrome.Page.enable()

    def openfile(self):
        self.f = open("simulator.txt", "r")
        self.num_lines = sum(1 for line in self.f)
        self.f = open("simulator.txt", "r")
        print(self.num_lines)
        print("opened file")

    def berechne1(self):
        print("start opening pages")
        self.start_time = time.time()
        self.openfile()
        for x in self.f:
            print("for page in file")
            self.chrome.Page.navigate(url = x)
            self.chrome.wait_event("Page.loadEventFired", timeout=60)
            self.p.step()
            self.update()
        self.elapsed_time = self.format(time.time() - self.start_time)
        self.time = Label(master=self, text=" Total loading time is " + str(self.elapsed_time) + " seconds")
        self.time.place(x=20, y=100)
        self.download_thread.do_run = False
        print(self.elapsed_time)
        self.writetoexcel2()



    def format(self,value):
        self.formatted = round(value, 1)
        return self.formatted

    def writetoexcel(self):
        print("writing to excel")
        self.workbook = xlsxwriter.Workbook('Example2.xls')
        self.worksheet = self.workbook.add_worksheet()
        self.row = 0
        self.worksheet.write(self.row, 0, self.totalmb)
        self.worksheet.write(self.row, 1, self.elapsed_time)
        self.row += 1


    def writetoexcel2(self):
        self.book_ro = open_workbook('Results.xls')
        self.book = copy(self.book_ro)  # writable copy
        sheet1 = self.book.get_sheet(0)  # first sheet
        sheet1.write(self.testnr, 0, self.totalmb)
        sheet1.write(self.testnr, 1, self.elapsed_time)
        self.testnr += 1
        self.book.save('Results.xls')

    def calculateusage(self):
        print('yes1')
        self.old_value = 0
        self.once = True
        self.do_run = True
        while getattr(self.download_thread, "do_run", True):
            self.new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

            if self.once:
                self.once = False
                self.old_value = self.new_value

                time.sleep(1)


            else:

                self.send_stat(self.new_value - self.old_value)
                time.sleep(1)

    def convert_to_gbit(self,value):
        self.used = value/ 1024. / 1024.
        self.exact = round(self.used,2)
        self.lC = Label(master=self, text=" Your used bandwith is " + str(self.exact) + " mb")
        self.lC.place(x=20, y=80)
        self.totalmb = self.exact
        return (value / 1024. / 1024.)

    def send_stat(self,value):
        print("%0.3f" % self.convert_to_gbit(value))

    def saveresults(self):
        print("yes")
# controller
class Controller(object):
    def __init__(self):
        self.view = View()
        self.view.mainloop()

        print("yes")

    def berechne(self):
        self.chrome = PyChromeDevTools.ChromeInterface()
        self.chrome.Network.enable()
        self.chrome.Page.enable()
        self.f = open("simulator.txt", "r")
        self.start_time = time.time()
        self.num_lines = sum(1 for line in self.f)
        print(self.num_lines)
        self.view.createpro(self.num_lines)
        time.sleep(5)
        for x in self.f:
            self.chrome.Page.navigate(url=x)
            self.chrome.wait_event("Page.loadEventFired", timeout=60)
        self.elapsed_time = time.time() - self.start_time
        print(self.elapsed_time)
        return self.elapsed_time

    def calculateusage(self):
        print('yes1')
        self.old_value = 0

        self.once = True
        while self.run:
            self.new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

            if once:
                self.once = False
                self.old_value = self.new_value

                send_stat(self.old_value)
                time.sleep(1)


            else:

                send_stat(new_value - old_value)
                time.sleep(1)

    def convert_to_gbit(self,value):
        return (value / 1024. / 1024.)

    def send_stat(self,value):
        print("%0.3f" % convert_to_gbit(value))

# Hauptprogramm
c = Controller()

