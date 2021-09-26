# Kandinsky-Numworks

## Français

### Description
Un petit module permettant de faire la liaison du module kandinsky, de la Numworks, à une fenêtre Windows. 
Pratique si l'on veut tester son programme sans le mettre sur la calculette.

### Plus
[Ion module of Numworks](https://github.com/ZetaMap/Ion-numworks)

### Note
Faire en sorte que l'écran se rafrechisse automatiquement. (faire en sorte de ne pas dépendre de la fonction 'display()' pour affichier la fenetre)<br>
La fonction 'get_pixel()' ne fonctionne pas.

### Contenu utilisable
**get_pixel**:
* Paramètres: **x**, **y**
* Description: Retourne la couleur du pixel (x,y)

**set_pixel**
* Paramètres: **x**, **y**, **color**
* Description: Colore le pixel (x,y)

**color**
* Paramètres: **r**, **g**, **b**
* Description: Définit une couleur rgb

**draw_string**
* Paramètres: **text**, **x**, **y**, **color (optionnel)[par défaut : (0,0,0)]**, **background (optionnel)[par défaut : (255,255,255)]**
* Description: Affiche un texte au pixel (x,y)

**fill_rect**
* Paramètres: **x**, **y**, **width**, **height**, **color**
* Description: Remplit un rectangle au pixel (x,y)

**display**
* Paramètres:
* Description: Affiche la fenêtre contenant les dessins. (fonction bloquante)


## English (translated)

### Description
A small module allowing to link the kandinsky module, from the Numworks, to a Windows window. 
Useful if you want to test your program without putting it on the calculator.

### More
[Ion module of Numworks](https://github.com/ZetaMap/Ion-numworks)

### Usable content
**get_pixel**:
* Parameters: **x**, **y**
* Description: Return pixel (x, y) color

**set_pixel**
* Parameters: **x**, **y**, **color**
* Description: Color pixel (x, y)

**color**
* Parameters: **r**, **g**, **b**
* Description: Define a rgb color

**draw_string**
* Parameters: **text**, **x**, **y**, **color (optionnel)[par défaut : (0,0,0)]**, **background (optionnel)[par défaut : (255,255,255)]**
* Description: Display a text from pixel (x, y)

**fill_rect**
* Parameters: **x**, **y**, **width**, **height**, **color**
* Description: Fill a rectangle at pixel (x, y)

**display**
* Parameters:
* Description: Displays the window containing the drawings. (blocking function) 
