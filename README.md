# MoxCardProcessor
Python class (with .exe version) which has several useful MTG card parsing and processing functions, helpful for making a proxied cube. It accepts card information in the format of "Moxfield Bulk Edit."

# Requirements
There are no requirements for just the .exe, it should just work, however if you want to run the program through the .py file in a python3 interpreter, you'll need install the <a href="https://github.com/psf/requests">requests</a> and <a href="https://github.com/NandaScott/Scrython">scrython</a> libraries.

# Formatting
Card information is accepted in the format of: "[\Quantity] [Card Name] ([Set Code]) [Collector Number]" each seperated by a return.

EX:  
    1 Academy Rector (UDS) 1  
    2 Adarkar Wastes (BLC) 291  
    5 Aftershock (PLST) TMP-160  

# Notes
When running the program, if you are pasting your list of cards into the console off moxfield bulk edit, your console may give you a warning, saying you are about to paste a lot of lines into the console, this is normal and just something your computer does to make sure you don't accidentally paste something crazy you didn't mean to into the console. If the little preview it shows you looks normal, just hit enter and it'll continue as normal.

# Common Issues
Make sure to be on a new line and then type -1 to finish inputting your card list. Easy step to forget.

# LICENSE
Everything in this repo (that isn't or isn't a part of any third party libraries) is free to use for non-commercial purposes. Commercial use requires a separate license and compensation. See the LICENSE file for more details
