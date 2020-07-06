# colorCls

##### Labeling, Aggragation and Categorizing about color RGB

for installing and visualizing, requires are below : 

* tqdm : https://github.com/tqdm/tqdm

* opencv-python : https://github.com/skvark/opencv-python

***

### Projects

colorCls have three major functions

* rgb4LABEL : Label is converted to RGB color.

* rgb2LABEL : RGB color is converted to label.

* percentage : Shows percent of RGB color compositions.

***

### Datasets

Some metadata is required to use the module.

##### color_dict.json

Those data available only permitted person, please contact to taep0q@gmail.com

***

### Example

* Script
```code
from colorCls import colorCls

if __name__=='__main__' :
    CLR_PATH = './color_hsv_upper.json'
    IMG_PATH = './sample.jpg'

    clr = colorCls(CLR_PATH, model='hsv')
    print("* Label of RGB 255, 255, 255 : {}".format(clr.rgb4LABEL('white')))
    print("* RGB Value of white : {}".format(clr.rgb2LABEL((255,255,255))))

    # Newly add : HSV Aggregation Algorithms
    print("- Color RGB 255, 0, 4 to HSV : {}".format(clr.rgb_to_hsv(255, 0, 4)))
    print("- Getting Percentage of a sample image\n{}".format(
        clr.percentage(IMG_PATH, resize=True, cform='bgr')))
```

* Output
```code
* Label of RGB 255, 255, 255 : (0, 0, 240)
* RGB Value of white : yellow
- Color RGB 255, 0, 4 to HSV : (255, 255, 255)
100%|██████████████████████████████████| 6700/6700 [00:00<00:00, 36725.79it/s]
- Getting Percentage of a sample image
([('yellowgray', 0.32402985074626867), ('white', 0.17477611940298507), ... )])
```

***

### Notices

###### Unauthorized distribution and commercial use are strictly prohibited without the permission of the original author and the related module.