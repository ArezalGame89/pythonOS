import os
import subprocess
import colorama
import json
import time

from datetime import datetime
from colorama import Fore, Back, Style
from pathlib import Path
from platform import system as usersOS

colorama.init(autoreset=True)


def getOption(option):
    os.chdir("data")
    with open("settings.json", "r") as f:
        data = json.load(f)
        os.chdir("..")
        return data.get(option)


subprocess.run("clear" if os.name == "posix" else "cls")
print("ChungOS Rewrite")
print("v0.0.1")
print(Fore.YELLOW + "Loading...")


def setOption(optionName, option):
    weirdPath = Path("data")
    with open(weirdPath / "settings.json", "r") as f:
        data = json.load(f)
        data[optionName] = option
    with open(weirdPath / "settings.json", "w") as f:
        json.dump(data, f, indent=4)


time.sleep(0.5)

subprocess.run("clear" if os.name != "nt" else "cls")
while True is not False:
    try:
        match getOption("input-color"):
            case "white":

                msg = input(Fore.WHITE + os.getcwd() + " >>> ").lower()
            case "red":
                msg = input(Fore.RED + os.getcwd() + " >>> ").lower()
            case _:
                msg = input(os.getcwd() + " >>> ")
        if msg == "time":
            print(datetime.now())
        elif msg.startswith("change"):
            if "--help" in msg.split(" "):
                print(
                    "colors - This affects if you want colored text or not, recommended to turn off incase this causes eyestrains or if your colorblind."
                )
            else:
                newoption = None
                if (
                    msg.split(" ")[2].lower() == "false"
                    or msg.split(" ")[2].lower() == "on"
                ):
                    newoption = False
                elif (
                    msg.split(" ")[2].lower() == "true"
                    or msg.split(" ")[2].lower() == "off"
                ):
                    newoption = True
                if getOption(msg.split(" ")[1].lower()) is not None:
                    if msg.split(" ")[1].lower() != "input-color":
                        setOption(msg.split(" ")[1].lower(), newoption)
                        print("Changed option.")
                    else:
                        setOption(msg.split(" ")[1].lower(), msg.split(" ")[2].lower())
                else:
                    print("That is not a valid option.")
                    match msg.split(" ")[1].lower():
                        case "input-color":
                            setOption("input-color", "white")
                        case "colors":
                            setOption("colors", True)
                        case _:
                            pass
        elif msg == "update":
            if getOption("colors"):
                print(Fore.RED + "This action requires Git, do you have it installed?")
            else:
                print("This action requires Git, do you have it installed?")
            confirm = input().lower()
            if confirm == "y":
                os.system("git pull origin main")
                match usersOS():
                    case 'Darwin': 
                        os.system("python3 main.py")
                    case 'Windows':
                        os.system("py main.py")
                    case 'Linux':
                        os.system("python main.py")
            elif confirm == "n" and not getOption("security"):
                from webbrowser import open_new_tab
                open_new_tab('https://git-scm.com/downloads')
        elif msg == "exit":
            exit()
        elif msg == "memory":
            from psutil import Process

            curMemory = Process(os.getpid())
            print("Memory in kilobytes: " + str(curMemory.memory_info().rss / 1000))
        elif msg == "browser":
            import sys
            from PyQt5.QtWidgets import *
            from PyQt5.QtWebEngineWidgets import *
            from PyQt5.QtCore import *
            from PyQt5.QtGui import QIcon, QKeySequence

            class MainWindow(QMainWindow):
                def __init__(self):

                    super(MainWindow, self).__init__()
                    self.setWindowTitle("Revrit")
                    self.browser = QWebEngineView()
                    self.browser.setUrl(QUrl("https://google.com"))
                    self.setCentralWidget(self.browser)
                    self.showMaximized()

                    navbar = QToolBar()
                    self.addToolBar(navbar)

                    back_btn = QAction("Back", self)
                    back_btn.triggered.connect(self.browser.back)
                    navbar.addAction(back_btn)

                    forward_btn = QAction("Foward", self)
                    forward_btn.triggered.connect(self.browser.forward)
                    navbar.addAction(forward_btn)

                    reload_btn = QAction("Reload", self)
                    reload_btn.triggered.connect(self.browser.reload)
                    navbar.addAction(reload_btn)

                    home_btn = QAction("Home", self)
                    home_btn.triggered.connect(self.navigate_home)
                    navbar.addAction(home_btn)

                    quit_btn = QAction("Quit", self)
                    quit_btn.triggered.connect(self.close)
                    navbar.addAction(quit_btn)

                    self.url_bar = QLineEdit()
                    self.url_bar.returnPressed.connect(self.nav_url)
                    navbar.addWidget(self.url_bar)


                def navigate_home(self):
                    self.browser.setUrl(QUrl("https://google.com"))

                def nav_url(self):
                    url = self.url_bar.text()
                    if url[0:7] != "https://":
                        self.browser.setUrl(QUrl("https://" + url))
                    else:
                        self.browser.setUrl(QUrl(url))
                        for i in range(2):
                            print(url)

            app = QApplication(sys.argv)
            QApplication.setApplicationName("Revrit")
            window = MainWindow()
            app.setWindowIcon(QIcon("chungos_icon.png"))
            app.exec_()
        elif bool(msg) is not False:
            print(msg + " is not a command.")
        elif msg == "run-lua":
            from lupa import LuaRuntime
            lua = LuaRuntime()
            os.chdir("scripts")
            for luathing in os.listdir():
                with open(luathing, "r") as f:
                    lua.eval(f.read())
            os.chdir("..")
        elif msg.startswith("run-luafile"):
            from lupa import LuaRuntime
            lua = LuaRuntime()
            os.chdir("scripts")
            for luathing in os.listdir():
                if msg.split(" ")[1] == luathing:
                    with open(msg.split(" ")[1], "r") as f:
                        lua.eval(f.read())
            os.chdir("..")
    except Exception as e:
        if getOption("colors"):
            print(Fore.RED + "Error: " + Fore.WHITE + str(e))
        else:
            print("Error: " + str(e))
