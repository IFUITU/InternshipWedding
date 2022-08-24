import os, random
from django.utils.deconstruct import deconstructible
from datetime import datetime

@deconstructible # when migrate return true however maybe false
class UploadTo:
    def __init__(self, folder):
        self.folder = folder
    
    def __call__(self, instance, filename): #how recieves atributes if we call class like function
        ext = os.path.splitext(filename)[1] #splitext-->returns tuple(filename[0], filename[1]) and that is why [1] 
        return "{}/{:%Y-%m}/{:%Y-%m-%d-%H-%M-%S}-{}{}".format(
            self.folder,
            datetime.now(),
            datetime.now(),
            random.randint(1000, 9999),
            ext
        )
