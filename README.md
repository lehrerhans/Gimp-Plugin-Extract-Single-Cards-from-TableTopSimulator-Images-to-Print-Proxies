# Gimp3 Plugin for Extracting Single-Cards from TableTopSimulator Images
Most TableTop Simulator Mods have Images with many cards of the game on it. <br>
if you want to print these cards as proxies , for examples for games out of print or not yet in print, <br>
it is convenient to have a plugin that extract each card from the Image.<br>


<b>
1) Isolate Cards </b> <br>
The python-plugin "tts-cards-isolate.py" file has to be put in a folder of the same name as the file (without-py-extension). this folder has to be in the plugin-folder of Gimp3.<br>
You load an image that has several cards in it. <br>
Then you change in the pythonfile "TTS-cards_isolate.py" the number of cards and the size the single cards should have.<br>

anzahl_bilder_in_x = 3     #how much cards are lying on the tts-image in x-direction? <br>
anzahl_bilder_in_y = 3      #how much cards are lying on the tts-image in y-direction?<br>
....<br>
.....<br>
karten_hoehe = 791      #cards height in pixel<br>
karten_breite = 520     # cards width in pixel<br>
....<br>
.....<br>       
#for 44mmx67mm at 300dpi (gilded realms minikarten)<br>
<br>
<br>

        
Then save the the changes.<br>
You start the plugin under Filter/Tutorial/<br>
You find the single cards as pngs in the output-directory is C:\users\your_username\ <br>


<b>2.Putting several cards on one A4-Sheet for printing out the Porxies   </b><br>
use the plugin "cards_16minis_to_a4".py<br>
<br>
<br>
<b>Remarks:</b><br>
Keep in mind, that a syntax-error in the plugin can force gimp not showing up the plugin. for example a missing bracket can force this.<br>
when using the Development version of Gimp , you have a console-window where you can see possible problems or errors.<br>



Actual tested with Gimp3.1.4 <br>
The output format is *.png 

Actual tested with Gimp3.1.4 <br>
Should work with Current Stable release of Gimp3





