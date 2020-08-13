import os

from image_processing import image_processing
import scoring

image_processing.start_recognition_simple()
scoring.start_scoring()
os.system('pause')
