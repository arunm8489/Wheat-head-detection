import pandas as pd
import numpy as np
import os
import xml.etree.ElementTree as ET



def process_coords(coords,out):
    """
    will take xmlfile as input and returns [[class_id,centerx,centrey,w,h],[class_id....]....]
    """
    final = []
    for c in coords:
        c = [int(i) for i in c]
        xmin,ymin,xmax,ymax,h,w = c[0],c[1],c[2],c[3],int(out['height']),int(out['width'])
        xmin,ymin,xmax,ymax = xmin/w,ymin/h,xmax/h,ymax/h
        h,w = ymax - ymin, xmax - xmin

        c_x,c_y = xmin + w/2, ymin + h/2 
        cc = [str(0),str(c_x),str(c_y),str(w),str(h)]
        final.append(cc)
    return final



def parse_xml(xmlfile):

    tree = ET.parse(xmlfile)
    root = tree.getroot()

    out = {}
    for elem in root.findall('size'):
        out['width'] = elem.find('width').text
        out['height'] = elem.find('height').text

    coords = []
    for i,elem in enumerate(root.findall('object')):
        coord = []
        bnd = elem.find('bndbox')
        for elem in bnd:
            coord.append(elem.text)
        coords.append(coord)

    final = process_coords(coords,out)

    return final


######code#######

# present annotation and image paths
annot_folder = 'number_plates/annots'
image_folder = 'number_plates/images'

# new basepath and annotation path
# data -> custom -> labels,train.txt,val.txt
base_path = 'data/custom/'
label_path = 'data/custom/labels'
train_txt = 'data/custom/train.txt'
val_txt = 'data/custom/valid.txt'

# creating folders if not present
if not os.path.exists(label_path):
  os.makedirs(label_path)

trainF = open(train_txt, "w")
valF = open(val_txt,"w")


imageidx = [i.split('.')[0] for i in os.listdir(annot_folder)]
idx = int(len(os.listdir(annot_folder))*0.8)
train_ids = imageidx[0:idx]
val_ids = imageidx[idx:]

count = 0
for img_id in imageidx:
    mode = 'train' if img_id in train_ids else 'val'
    image_path = base_path + f'images/{str(img_id)}.jpg'
    annotation_path = base_path + f'labels/{str(img_id)}.txt'


    if mode == 'train':
        trainF.write(image_path)
        trainF.write('\n')
        count += 1
    else:
        valF.write(image_path)
        valF.write('\n')
        count += 1

    # annotation contents writing
    xmlfile = os.path.join(annot_folder,str(img_id)+'.xml')
    outxml = parse_xml(xmlfile)
    outF = open(annotation_path, "w")
    for lst in outxml:
      line = ' '.join(lst)
      outF.write(line)      
      outF.write("\n")
    outF.close()
    print(f'written {mode} : {annotation_path}')
   
print(f'Totaly {count} files written')
trainF.close()
valF.close()

















