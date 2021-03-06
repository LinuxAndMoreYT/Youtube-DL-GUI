#!/usr/bin/python3

import os
os.chdir("/opt/youtube-dl-gui/")

import gi
import youtube_dl
import time
import threading
import math
import re

gi.require_version("Gtk", "3.0")
gi.require_version('Notify', '0.7')

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gdk
from gi.repository import Notify

APP_NAME = 'YouTube DL GUI'

class Main:
    def __init__(self):
        gladeFile               = "/opt/youtube-dl-gui/youtube-dl-gui.glade"
        self.builder            = Gtk.Builder()
        self.builder.add_from_file(gladeFile)

        window                  = self.builder.get_object("Main")
        window.connect("delete-event", Gtk.main_quit)
        window.show()

        container               = self.builder.get_object("GTKFixed")

        self.PlaylistChooser    = self.builder.get_object("PlaylistChooser")
        self.PlaylistChooser.connect("toggled", self.playlist_on_checked)
        self.playlist           = "True"
        
        self.URLBar             = self.builder.get_object("URLBar")

        self.ArtChooser         = self.builder.get_object("ArtChooser")

        self.Dir                = self.builder.get_object("FileChooser")

        self.label              = self.builder.get_object("label")
        self.label.set_text("Keine Aufträge")

        self.progress           = self.builder.get_object("progress")

        self.Download           = self.builder.get_object("Download")
        self.Download.connect("clicked", self.do_clicked)

    def playlist_on_checked(self, widget, data = None):
        if self.playlist == "False":
            self.playlist   = "True"
        else:
            self.playlist   = "False"

    def do_clicked(self, button):

        self.label.set_text("Vorbereiten - Bitte warten")
        URL             = self.URLBar.get_text()
        model           = self.ArtChooser.get_model()
        Vorlage         = self.ArtChooser.get_active()
        Dir             = self.Dir.get_filename()
        idel            = 1

        if URL == "":
            self.label.set_text("Fehler - Eingaben Überprüfen")

        if Vorlage      == 0:
            Art         = "401+140"
            Sort        = ".mp4"
            audio       = "False"
        if Vorlage      == 1:
            Art         = "400+140"
            Sort        = ".mp4"
            audio       = "False"
        if Vorlage      == 2:
            Art         = "137+140"
            Sort        = ".mp4"
            audio       = "False"
        if Vorlage      == 3:
            Art         = "22+140"
            Sort        = ".mp4"
            audio       = "False"
        if Vorlage      == 4:
            Art         = "18+140"
            Sort        = ".mp4"
            audio       = "False"
        if Vorlage      == 5:
            Art         = "bestaudio/best"
            Sort        = ".mp3"
            audio       = "True"

        Out             = (Dir)+"/"+"%(title)s"+(Sort)

        def my_hook(d):
            if d['status']      == 'downloading':
                self.label.set_text("Fortschritt: "+d['_percent_str']+"     Verbleibende Zeit: "+d['_eta_str']+"     Geschwindigkeit: "+d['_speed_str'])
                p = d['_percent_str']
                p = p.replace('%','')
                p = float(p) / 100
                self.progress.set_fraction(float(p))
                time.sleep(0.1)

        ydl_opts = {
            'format': (Art),
            'outtmpl': (Out),
            'noplaylist': (self.playlist),
            'extract-audio': (audio),
            'addmetadata': True,
            'progress_hooks': [my_hook],
        }
        
        def clear():
            self.label.set_text("Keine Aufträge")
            self.URLBar.set_text("")
            self.progress.set_fraction(0.0)

        def get():
            try:
                status = True
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([URL])
            except:
                self.label.set_text("Fehler - Videoformat, Internetverbindung und Speicherort überprüfen.")
                status = False

            if status == True:
                Notify.init("YouTube DL GUI")
                notification = Notify.Notification.new("Download - Fertiggestellt")
                notification.show()
                Notify.uninit()
                clear()

        thread = threading.Thread(target=get)
        thread.start()

if __name__ == '__main__':
    main = Main()
    Gtk.main()

