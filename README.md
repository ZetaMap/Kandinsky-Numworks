# Kandinsky-Numworks

## Français

### Description
Un petit module permettant de faire la liaison du module kandinsky, de la Numworks, à une fenêtre Windows. Pratique si l'on veut tester son programme sans le mettre sur la calculette.

### Plus
[Ion module of Numworks](https://github.com/ZetaMap/Ion-numworks)

### Note
Faire en sorte que l'écran se rafrechisse automatiquement. (faire en sorte de ne pas dépendre de la fonction 'display()' pour affichier la fenetre)
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
* Description: Renplit un rectangle au pixel (x,y)

**display**
* Paramètres:
* Description: Affiche la fenetre contenant les dessins. (fonction bloquante)
