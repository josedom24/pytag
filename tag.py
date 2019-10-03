from os import scandir, getcwd
from os.path import abspath
import eyed3
import yaml
import os
import sys

def ls(ruta = getcwd()):
    return [abspath(arch.path) for arch in scandir(ruta) if arch.is_file() and arch.name.endswith("mp3")]

if len(sys.argv)!=3:
    print("Debes indicar la ruta donde se encuentran los ficheros y si quieres modificar nombre de ficheros:\npython3 tag.py '~/musica/disco' --change")
    sys.exit(1)

with open("configuration.yaml") as fichero:
    doc=yaml.load(fichero,Loader=yaml.FullLoader)


files = ls(sys.argv[1])

if len(files)!=len(doc["tracks"]):
    print("No coinciden el número de canciones")
else:
    canciones = []
    noencontradas = []
    for track in doc["tracks"]:
        for file in files:
            pos=len(track["titulo"])
            if track["titulo"][:pos].lower() in file.lower():
                canciones.append(file)
                break
    noencontradas=list(set(files) - set(canciones))
    if len(noencontradas)>0:
        print("No se han encontrado estas canciones:",noencontradas)
    else:
        for file,track in zip(canciones,doc["tracks"]):
            audiofile = eyed3.load(file)
            audiofile.tag.artist = doc["artista"]
            audiofile.tag.album = doc["album"]
            audiofile.tag.recording_date = doc["año"]
            audiofile.tag.track_num =(track["num"],doc["canciones"])
            audiofile.tag.title =track["titulo"]
            imagedata = open(doc["imagen"],"rb").read()

            audiofile.tag.images.set(3,imagedata,"image/jpeg","you can put a description here")
            audiofile.tag.save()
            if sys.argv[2]=="--change":
                path=file.split("/")
                nombre_nuevo="/".join(path[:-1])+"/"+track["titulo"]+".mp3"
                os.rename(file,nombre_nuevo)
                