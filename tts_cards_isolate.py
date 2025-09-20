#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   GIMP - The GNU Image Manipulation Program
#   Copyright (C) 1995 Spencer Kimball and Peter Mattis
#
#   gimp-tutorial-plug-in.py
#   sample plug-in to illustrate the Python plug-in writing tutorial
#   Copyright (C) 2023 Jacob Boerema
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Das Bild aus TTS-Simulator so skalieren, dass beim Teilen durch die anzahl der bilder eine glatte zahl herauskommt
#C.Roters 9/2025   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    

    
    
import sys

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
from gi.repository import Gio
from gi.repository import GLib

class MyFirstPlugin (Gimp.PlugIn):
    def do_query_procedures(self):
        return [ "jb-plug-in-first-try" ]

    def do_set_i18n (self, name):
        return False

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)

        procedure.set_image_types("*")

        procedure.set_menu_label("My first Python plug-in")
        procedure.add_menu_path('<Image>/Filters/Tutorial')

        procedure.set_documentation("My first Python plug-in tryout",
                                    "My first Python 3 plug-in for GIMP 3.0",
                                    name)
        procedure.set_attribution("Your name", "Your name", "2023")

        return procedure

    def run(self, procedure, run_mode, img, drawables, config, run_data):
        #Gimp.message("Start")
        
        
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #Das Bild aus TTS-Simulator so skalieren, dass beim Teilen durch die anzahl der bilder eine glatte zahl herauskommt
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
        #Hier die anzahl der kartenbilder angeben die auf dem TTS-Simulator-Bild zu Platz finden.
    
   
        anzahl_bilder_in_x = 3     #how much cards are lying on the tts-image in x-direction?
        anzahl_bilder_in_y = 3      #how much cards are lying on the tts-image in y-direction?
   
        ausgabename_fotos = "warfront"      #basename of the 13x8 photos on the drive
    
    
        anzahl_karten_auslesen_x = anzahl_bilder_in_x            #default =   anzahl_bilder_in_x         
        anzahl_karten_auslesen_y = anzahl_bilder_in_y            #default an even number , so that x*y can divide by 4
    
        
        save_to_disk = 1           #default = 1:save fotos to disk   0:no save to disk 
    
        layer_basename = ausgabename_fotos     
        layer_number_offset = 0    #default = 0
    
     

        breite = img.get_width()
        hoehe  = img.get_height()
    
        #scale the image, so that the resolution can be divided by anzahl_bilder_in_x and anzahl_bilder_in_x without rest
        dx = int(breite/anzahl_bilder_in_x)
        dy = int(hoehe/anzahl_bilder_in_y)
        img.scale(dx*anzahl_bilder_in_x, dy*anzahl_bilder_in_y)
        
        breite = img.get_width()
        hoehe  = img.get_height()
           
        #Einzelbilder mit rand, dann randbreite hier eingeben in pixel
        crop_left   =  0.0    #default=0 : kein Rand
        crop_right  =  0.0    #default=0 : kein Rand
        crop_top    =  0.0    #default=0 : kein Rand
        crop_bottom =  0.0    #default=0 : kein Rand
       
        karten_hoehe = 791      
        karten_breite = 520     
        
        #fuer 44mmx67mm bei 300dpi (gilded realms minikarten)
        #karten_hoehe = 791 
        #karten_breite = 520
        
        #liste_layer = img.get_layers()
        #layer1 = drawables[0]
        zaehler = 0
        img1 = []
        layer1 = []
        for ver in range(anzahl_karten_auslesen_y):
            for hor in range(anzahl_karten_auslesen_x):
            
                layername = layer_basename  + str(zaehler)           
                x_anf = dx*hor 
                #pdb.gimp_message("x_anf: "+str(x_anf))
                y_anf = dy*ver 
                rect_anfang_x = x_anf + crop_left
                rect_anfang_y = y_anf + crop_top
                rect_dx = dx-crop_left-crop_right
                rect_dy = dy-crop_top-crop_bottom
            
                #aus "bild" ein rechteck ausschneiden: entspricht einer Spielkarte
                img.select_rectangle(2,rect_anfang_x ,rect_anfang_y,rect_dx , rect_dy)
                Gimp.message("hor:"+str(hor+1)+" / ver: "+str(ver+1))
                
                Gimp.edit_copy([img.get_layers()[0]])
                
                                
                img0 = Gimp.Image.new(karten_breite, karten_hoehe, Gimp.ImageBaseType.RGB)
                #img1.append(img0)
                #img0 = img1[zaehler]
                #Gimp.message(str(len(img1)))
                
                layer0 = Gimp.Layer.new(img0, "test", rect_dx, rect_dy, img0.get_base_type(), 100, Gimp.LayerMode.NORMAL)
                #layer1.append(layer0)
                
                layer0.add_alpha()
                img0.insert_layer(layer0, None, 0)
                
                #selection auf layer pasten
                sel = Gimp.edit_paste(layer0, True)
                #for sl in sel:
                #    Gimp.floating_sel_attach(sl, layer0)
                #    Gimp.floating_sel_remove(sl)
                
                #Kartenbilder auf Kartenbreite skalieren
                layer0.scale(karten_breite, karten_hoehe, 0)
                
                img0.flatten()
                Gimp.Display.new(img0)
                Gimp.displays_flush()
                
                #image save to disk
                filename = ausgabename_fotos + str(zaehler) + ".png" 
                outputfile = Gio.File.new_for_path(filename)
                Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, img0, outputfile, None)
                
                
                zaehler = zaehler +1

      
        
        #Gimp.displays_flush()
        Gimp.message("fertig")
        
        # do what you want to do, then, in case of success, return:
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(MyFirstPlugin.__gtype__, sys.argv)