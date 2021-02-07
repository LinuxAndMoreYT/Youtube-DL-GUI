#!/usr/bin/python3
import gi
import youtube_dl
import threading
import subprocess
import time

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
        gladeFile       = "youtube-dl-gui.glade"
        self.builder    = Gtk.Builder()
        self.builder.add_from_file(gladeFile)

        window          = self.builder.get_object("Main")
        window.connect("delete-event", Gtk.main_quit)
        window.show()

        container       = self.builder.get_object("GTKFixed")

        PlaylistChooser = self.builder.get_object("PlaylistChooser")
        PlaylistChooser.connect("toggled", self.on_checked)
        self.playlist   = "True"
        
        self.URLBar     = self.builder.get_object("URLBar")

        self.ArtChooser = self.builder.get_object("ArtChooser")

        self.Dir        = self.builder.get_object("FileChooser")

        self.label      = self.builder.get_object("label")

        Download        = self.builder.get_object("Download")
        Download.connect("clicked", self.do_clicked)

    def on_checked(self, widget, data = None):
        self.playlist   = "Flase"

    def do_clicked(self, button):

        URL             = self.URLBar.get_text()
        model           = self.ArtChooser.get_model()
        Vorlage         = self.ArtChooser.get_active()
        Dir             = self.Dir.get_filename()
        idel            = 1

        if Vorlage      == 0:
            Art         = "137+140"
            Sort        = ".mp4"
            audio       = "False"
        if Vorlage      == 1:
            Art         = "22+140"
            Sort        = ".mp4"
            audio       = "False"
        if Vorlage      == 2:
            Art         = "bestaudio/best"
            Sort        = ".mp3"
            audio       = "True"

        Out             = (Dir)+"/"+"%(title)s"+(Sort)

        def my_hook(d):
            if d['status']      == 'downloading':
                self.label.set_text("Fortschritt:"+d['_percent_str']+"Verbleibende Zeit:"+d['_eta_str'])
                
        ydl_opts = {
            'format': (Art),
            'outtmpl': (Out),
            'noplaylist': (self.playlist),
            'extract-audio': (audio),
            'progress_hooks': [my_hook],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([URL])

        Notify.init("YouTube DL GUI")
        notification = Notify.Notification.new("Download - Fertiggestellt")
        notification.show()
        Notify.uninit()
    
if __name__ == '__main__':
    main = Main()
    Gtk.main()

