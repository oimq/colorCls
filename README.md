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

ccls = colorCls(<color_dict_path>)
print(ccls.rgb4LABEL((255,255,255)))
print(ccls.rgb2LABEL('white'))
print(ccls.percentage(<img>))
```

* Output
```code
white
(255, 255, 255)
{'white':0.79322, 'gray':'0.23521', ...}
```

***

### Notices

###### Unauthorized distribution and commercial use is strictly prohibited without the permission of the original author and the related module.