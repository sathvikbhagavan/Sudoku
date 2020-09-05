# Sudoku OCR and Play

Project Description: Input - Image of Sudoku puzzle, Output - Sudoku displayed in pygame where it can be played or solution can be visualized by backtracking

OCR part uses OpenCV and an ensemble of mnist handwritten digits classifier

Game part uses pygame and numpy

You can play by clicking on a square and typing any number on it. You can delete by pressing 0. You can also check whether the solution is wrong, correct but incomplete, and completely correct by clicking CHECK
You can click SOLVE to visualize the solution.

To run this, run sudoku.py with following command line arguements: 

  --model_directory = models/
  
  --image = Your sample image path
  
  --number = 3 
  
So an example run will be : python sudoku.py --model_directory models/ --number 3 --image images/sudoku.jpg
