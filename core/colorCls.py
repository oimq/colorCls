from jSona import jSona
from cv2 import cv2
import numpy as np
from tqdm import tqdm
import pprint
pp = pprint.pprint

class colorCls :
    def __init__(self, color_labels) :
        if type(color_labels) == type("") :
            self.labels = jSona().loadJson(color_labels)
        else :
            self.labels = color_labels
        self.color_dict = {color['id']:(color['r'], color['g'], color['b']) for color in self.labels}
        self.matC   = np.array([[color['r'], color['g'], color['b']] for color in self.labels])
        self.matI   = np.full(shape=(3,), fill_value=(1))

    def rgb4LABEL(self, label) :
        return self.color_dict[label]

    def rgb2LABEL(self, rgb) :
        distances = list(np.inner((self.matC-rgb)**2, self.matI))
        dinx = distances.index(min(distances))
        return self.labels[dinx]['id']
        
    def percentage(self, img, resize=True, top=0, format='rgb', cry=True) :
        if type(img) == type('') : img = cv2.imread(img)
        if resize : img = cv2.resize(img, dsize=(0, 0), fx=100/img.shape[0], fy=100/img.shape[0], interpolation=cv2.INTER_AREA)
        if format == 'bgr' : img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        total = img.shape[0]*img.shape[1]
        pcount = dict()

        if cry : pbar = tqdm(total=total)
        for j in range(img.shape[1]) :
            for i in range(img.shape[0]) :
                if np.sum(np.array([255, 255, 255])-img[i, j, :]) == 0 : 
                    continue
                else :
                    distances = list(np.inner((self.matC-img[i, j, :])**2, self.matI))
                    dinx = distances.index(min(distances))
                    label = self.labels[dinx]['id']
                    if label in pcount : pcount[label] += 1
                    else               : pcount[label]  = 1
                if cry : pbar.update(1)
        pcount = sorted(list(pcount.items()), key=lambda e:e[1], reverse=True)
        if cry : pbar.close()
        
        if top > 0 :
            pcount = pcount[:top]
            total = sum([pitem[1] for pitem in pcount])
        prate = [(pitem[0], pitem[1]/total) for pitem in pcount]
        return prate, pcount

# ---------------

        # threading
        # print([(i*CHUNK_SIZE, (i+1)*CHUNK_SIZE) if i != NUM_CPU-1 else (i*CHUNK_SIZE, ) for i in range(NUM_CPU)])
        # CHUNK_SIZE = int(img.shape[0]/NUM_CPU)
        # CHUNKS = [img[i*CHUNK_SIZE:(i+1)*CHUNK_SIZE,:,:] if i != NUM_CPU-1 else img[i*CHUNK_SIZE:,:,:] for i in range(NUM_CPU)]
        # THREADS = [threading.Thread(target=self.ptask, args=(CHUNKS[i], None)) for i in range(NUM_CPU)]
        # for th in THREADS : th.start()
        # for th in THREADS : th.join()