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