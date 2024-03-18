# Background

This integrates much of the logic in my wordle_cli program and was done specifically to learn a GUI library.


# Description 

GUI implementation of the Wordle game using the PySimpleGUI library

  
# Game introduction

Wordle is a word guessing game.  Words are restricted to five letters and players get six guesses.  If a letter is in the correct spot in the answer, it will turn green.  If it is in the answer, but in the wrong spot it will turn yellow.  If it is not in the answer it will turn gray.  Multiples of the same letter (such as the o's in color) will be colored green or yellow as appropriate if the answer also contains multiple instances of the letter, otherwise the duplicates will be gray.  

Additional information can be found here: https://en.wikipedia.org/wiki/Wordle

![image](https://user-images.githubusercontent.com/106843224/186750537-2a1764eb-61ce-4b28-8811-04f6cbf3a544.png)


# Dependencies

- Python3 
- python-tk.  Installation depends on your system.  https://tkdocs.com/tutorial/install.html
- Install the required libraries via 'pip install -r requirements.txt'


# Help
  
Help can be obtained by including the [-h] option to the program: './wordle_gui.py -h'


# Author

Dennis Byington - dennisbyington@mac.com


# Version history & release notes

0.1 - Initial release


# Bugs

- Deleting one letter deletes the entire word.  I am still thinking through the process of deleting one letter at a time.  

- I am also seeking inputs and constructive criticism on areas I can improve. 


# Future features

None


# License

This software is licensed under the MIT License.  See license.txt for details.



# Acknowledgments

This is my software recreation the web-based Wordle game.  Wordle was originally created by Josh Wardle and is now owned and published by the New York Times.  
