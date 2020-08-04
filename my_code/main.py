import os
import sys
import algorithm
import image_processing

sys.path.append("../auto_grader/")
from auto_grader import auto_grader
ag = auto_grader()

image_processing.image_processing.set_squares()  # Analyze all squares, determine color and number, save gray images to image folder
os.system('pause')
