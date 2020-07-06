from det2Clo.visIm import visIm
from det2Clo.jSona import jSona
from cv2 import cv2
import numpy as np
from tqdm import tqdm
from pprint import pprint as pp
from math import cos, sin, pi

class colorCls :
    def __init__(self, color_labels, model='hsv') :
        self.labels = jSona().loadJson(color_labels) if type(color_labels) == type("") else color_labels
        self.model  = model
        if   self.model=='rgb' :
            self.color_dict = {color['id']:(color['r'], color['g'], color['b']) for color in self.labels}
            self.matC   = np.array([[color['r'], color['g'], color['b']] for color in self.labels])
            self.matI   = np.full(shape=(3,), fill_value=(1))
            
        elif self.model=='hsv' :
            self.color_dict = {color['id']:(color['h'], color['s'], color['v']) for color in self.labels}
            self.matC       = np.array([self.convertHSV2XYZ(color['h'], color['s'], color['v']) for color in self.labels])
            self.matI       = np.full(shape=(3,), fill_value=(1))

    def convertHSV2XYZ(self, h, s, v) :
        return np.array([
            s*cos(h*pi/127.5)*v/255, 
            s*sin(h*pi/127.5)*v/255, 
            v])

    def rgb4LABEL(self, label) :
        return self.color_dict[label]

    def rgb2LABEL(self, rgb) :
        distances = list(np.inner((self.matC-rgb)**2, self.matI))
        dinx = distances.index(min(distances))
        return self.labels[dinx]['id']
    
    def rgb_to_hsv(self, r, g, b) :
        r, g, b = r/255.0, g/255.0, b/255.0
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        diff = cmax - cmin
        h, s, v  = 0, 0, 0
        if   cmax == cmin : h = 0
        elif cmax == r    : h = (60 * ((g - b) / diff) + 360) % 360
        elif cmax == g    : h = (60 * ((b - r) / diff) + 120) % 360
        elif cmax == b    : h = (60 * ((r - g) / diff) + 240) % 360

        if cmax == 0 : s = 0
        else         : s = (diff / cmax) * 100

        v = cmax * 100
        return int(h*255/359), int(s*255/100), int(v*255/100)
        
    def percentage(self, img, resize=True, top=0, cform='rgb', cry=True) :
        if type(img) == type('') : img = cv2.imread(img)
        if resize : img = cv2.resize(img, dsize=(0, 0), fx=100/img.shape[0], fy=100/img.shape[0], interpolation=cv2.INTER_AREA)
        
        total = 0
        pcount = dict()
        if cry : pbar = tqdm(total=img.shape[1]*img.shape[0])
        if self.model=='rgb' :
            if cform == 'bgr' : img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            for j in range(img.shape[1]) :
                for i in range(img.shape[0]) :
                    if cry : pbar.update(1)
                    if np.sum(np.abs(np.array([0, 0, 0])-img[i, j, :])) == 0 : continue

                    distances = list(np.inner((self.matC-img[i, j, :])**2, self.matI))
                    dinx = distances.index(min(distances))
                    label = self.labels[dinx]['id']
                    if label in pcount : pcount[label] += 1
                    else               : pcount[label]  = 1
                    total += 1

        elif self.model=='hsv' :
            if cform == 'bgr' : img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
            else              : img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV_FULL)
            hsv_count = {}
            for j in range(img.shape[1]) :
                for i in range(img.shape[0]) :
                    label = '{} {} {}'.format(*img[i, j, :])
                    if label not in hsv_count : hsv_count[label]  = 1
                    else                      : hsv_count[label] += 1      
                    if cry : pbar.update()      
            # print(sorted(list(hsv_count.items()), key=lambda e:e[1], reverse=True))
            for hsv_key in hsv_count :
                hsv = np.array(hsv_key.split()).astype(np.int)
                if np.sum(hsv) == 0 : continue
                hsv = self.convertHSV2XYZ(*hsv)
                distances = list(np.inner((self.matC - hsv)**2, self.matI))
                dinx = distances.index(min(distances))
                label = self.labels[dinx]['id']
                if label in pcount : pcount[label] += hsv_count[hsv_key]
                else               : pcount[label]  = hsv_count[hsv_key]
                total += hsv_count[hsv_key]

        pcount = sorted(list(pcount.items()), key=lambda e:e[1], reverse=True)         
        # print(pcount)  
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


        # hsv
        # elif self.model=='hsv' :
        #     if cform == 'bgr' : img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
        #     else              : img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        #     for j in range(img.shape[1]) :
        #         for i in range(img.shape[0]) :
        #             if cry : pbar.update(1)
        #             if np.sum(np.array([0, 0, 255])-img[i, j, :]) == 0 : continue

        #             h, sv = img[i, j, 0], img[i, j, 1:3] 
        #             hdistances = list(np.abs(self.h_indices - h))
        #             dinx = hdistances.index(min(hdistances))

        #             _sv = self.color_dict[self.h_indices[dinx]][0]
        #             svdistances = list((np.inner((_sv - np.ones((_sv.shape[0], 1))*sv)**2, np.full((1, 2), fill_value=(1)))))
        #             svinx = svdistances.index(min(svdistances))

        #             label = self.color_dict[self.h_indices[dinx]][1][svinx]
        #             if label in pcount : pcount[label] += 1
        #             else               : pcount[label]  = 1
        #             total += 1

        # pcount = sorted(list(pcount.items()), key=lambda e:e[1], reverse=True)           
        # if cry : pbar.close()
        # if top > 0 :
        #     pcount = pcount[:top]
        #     total = sum([pitem[1] for pitem in pcount])
        # prate = [(pitem[0], pitem[1]/total) for pitem in pcount]
        # return prate, pcount