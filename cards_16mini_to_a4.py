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
#Put several card images on an A4-sheet for printing proxie-cards
#C.Roters 9/2025   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Open alls cards images as layers in Gimp
# These layers lay on an image, that is automatically created by Gimp.    

    
    
import sys

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
from gi.repository import Gio
from gi.repository import GLib

class MyPlugin (Gimp.PlugIn):
    def do_query_procedures(self):
        return [ "cards-to-a4-Plugin" ]

    def do_set_i18n (self, name):
        return False

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)

        procedure.set_image_types("*")

        procedure.set_menu_label("cards to a4 Plugin")
        procedure.add_menu_path('<Image>/Filters/Tutorial')

        procedure.set_documentation("cards_to a4_Plugin tryout",
                                    "cards to a4 Plugin plug-in for GIMP 3.0",
                                    name)
        procedure.set_attribution("Christoph", "Lamaflieger", "2025")

        return procedure

    def run(self, procedure, run_mode, img, drawables, config, run_data):
        
        # Open alls cards images as layers in Gimp
        # These layers lay on an image, that is automatically created by Gimp.
        # this image is referenced in "img" . see definition in "def run" procedure
        ausgabename_fotos = "frontside"      #basename of the A4 pages that will written to the drive
    
        #Anzahl der Kartenbilder, die auf A4 fotos gebracht werden. Jedes Kartenbild liegt auf einem eigenen Layer. 
        anzahl_karten = 16     #Die Zahl sollte durch xxx teilbar sein, da jeweils xxx Karten auf ein A4 Foto kommen
    
     
    
        dpi = 300
    
        save_to_disk = 1           #default = 1:save fotos to disk   0:no save to disk 
    

        karten_breite_px = 520  #minikarte 44mm =  520px
        karten_hoehe_px  = 791    #minkarte 67mm =  791px
         
    
        foto_breite_px  = 2480      #A4 breite in px bei 300dpi
        foto_hoehe_px   = 3508      #A4 hoehe  in px bei 300dpi
    
        layer_basename = "ds_"      #default = ""
        layer_number_offset = 0   #default = 0
    
        #bild = img    #first image in gimp will be saved in "bild"
        img.scale(karten_breite_px, karten_hoehe_px)
        
        layers = img.get_selected_layers()
        for layer in layers:
            layer.scale(karten_breite_px,karten_hoehe_px,0)
        
        #Gimp.Display.new(img)
        Gimp.displays_flush()
        
        karten_pro_seite = 16    

        zaehler = 0
        zaehler_karten = 0
        if save_to_disk == 1:
            for karten in range(0,anzahl_karten,karten_pro_seite):   #jeweils 16 Karten auf ein A4 - Foto
                layer = []
                layername = []
                # new Image "image_foto"  
                #image_foto = pdb.gimp_image_new(foto_breite_px, foto_hoehe_px, 0)  # 0 = type RGB
                #pdb.gimp_image_set_filename(image_foto, "image_foto")   
                
                image_foto = Gimp.Image.new(foto_breite_px, foto_hoehe_px, Gimp.ImageBaseType.RGB)
                layer0 = Gimp.Layer.new(image_foto, "base", foto_breite_px, foto_hoehe_px, image_foto.get_base_type(), 100, Gimp.LayerMode.NORMAL)
                image_foto.insert_layer(layer0, None, 0)
                Gimp.Drawable.fill(layer0, 3)   #    0:background  1:foreground 3:white
                

                
                midpoint_a4_x = int(foto_breite_px / 2)
                midpoint_a4_y = int(foto_hoehe_px / 2)
                for reihe in range(0,4):        #n-te Reihe karten
                    for lauf in range(0,4):     #eine reihe besteht aus 4 Karten   
                        ind = lauf + reihe*4
                        #Gimp.message("ind:"+str(ind))
                        
                        
                        #img.select_rectangle(2,0 ,0,img.get_width() ,img.get_height())
                        Gimp.edit_copy([img.get_layers()[ind]])
                        

                        
                        layer0 = Gimp.Layer.new(image_foto, str(ind), karten_breite_px, karten_hoehe_px, image_foto.get_base_type(), 100, Gimp.LayerMode.NORMAL)
                        image_foto.insert_layer(layer0, None, 0)
                        #layer0.add_alpha()
                        
                
                        #selection auf layer pasten
                        sel = Gimp.edit_paste(layer0, True)
                        for sl in sel:
                            Gimp.floating_sel_attach(sl, layer0)
                            Gimp.floating_sel_remove(sl)
                                                
                        left_margin = midpoint_a4_x - (2* karten_breite_px) + lauf * karten_breite_px
                        top_margin = midpoint_a4_y - 2* karten_hoehe_px + reihe * karten_hoehe_px
                        
                        layer0.set_offsets(left_margin, top_margin)
                
                
                
                image_foto.flatten()
                Gimp.Display.new(image_foto)
                Gimp.displays_flush()
                       
                # save image to disk
                #filename = ausgabename_fotos + "_A4_300dpi_"+ str(zaehler) + ".png"                
                #pdb.file_png_save_defaults(image_foto, image_foto.layers[0], filename, '?')
                
                #image save to disk
                filename = ausgabename_fotos + "_A4_300dpi_" + str(zaehler) + ".png" 
                Gimp.message(filename)
                outputfile = Gio.File.new_for_path(filename)
                Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, image_foto, outputfile, None)
                
                zaehler  =  zaehler + 1
            
            
        
        
        
        
        
        
        Gimp.message("fertig")
        
        # do what you want to do, then, in case of success, return:
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

Gimp.main(MyPlugin.__gtype__, sys.argv)