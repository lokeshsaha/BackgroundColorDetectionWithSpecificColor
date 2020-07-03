import sys
import cv2
import numpy as np
from collections import Counter


class BackgroundColorDetector():
    def __init__(self, imageLoc):
        self.img = cv2.imread(imageLoc, 1)
        self.manual_count = {}
        self.w, self.h, self.channels = self.img.shape
        self.total_pixels = self.w*self.h

    def count(self):
        for y in range(0, self.h):
            for x in range(0, self.w):
                RGB = (self.img[x//2, y//2, 2], self.img[x//2, y//2, 1], self.img[x//2, y//2, 0])
                if RGB in self.manual_count:
                    self.manual_count[RGB] += 1
                else:
                    self.manual_count[RGB] = 1

    def average_colour(self):
        red = 0
        green = 0
        blue = 0
        sample = 10
        for top in range(0, sample):
            red += self.number_counter[top][0][0]
            green += self.number_counter[top][0][1]
            blue += self.number_counter[top][0][2]

        average_red = red / sample
        average_green = green / sample
        average_blue = blue / sample
        print("Average RGB for top ten is: (", average_red,
              ", ", average_green, ", ", average_blue, ")")
        return (average_red, average_green, average_blue)

    def twenty_most_common(self):
        self.count()
        self.number_counter = Counter(self.manual_count).most_common(20)
        for rgb, value in self.number_counter:
            print(rgb, value, ((float(value)/self.total_pixels)*100))

    def detect(self):
        self.twenty_most_common()
        self.percentage_of_first = (
            float(self.number_counter[0][1])/self.total_pixels)
        print(self.percentage_of_first)
        if self.percentage_of_first > 0.5:
            print("Background color is ", self.number_counter[0][0])
            return self.number_counter[0][0]
        else:
            return self.average_colour()


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        pass                        # Checks if image was given as cli argument
      #print("error: syntax is 'python bg.py \location of image")
    else:
        BackgroundColor = BackgroundColorDetector(sys.argv[1])
        average_color = BackgroundColor.detect()
        print(average_color)
        (r, g, b) = average_color
        if(175 <= r and r <= 255) and (180 <= g and g <= 255) and (173 <= b and b <= 255):
            print("This image has a absolute white background color")
            sys.exit(0)
        print("This image does not match with most instances of white background color")
        #img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
        #laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
        #print("laplacian threshold of blur",laplacian_var)
        #if laplacian_var < 100:
         #  print("Image is blurry")
        #else:
         #   print("Image is not blurred")

        #r_min = 161 #175
        #r_max = 255
        #g_min = 180
        #g_max = 255
        #b_min = 173
        #b_max = 255

        #if r_min <= average_color[0] <= r_max and g_min <= average_color[1] <= g_max and b_min <= average_color[2] <= b_max:
         #   print("This image has a absolute white background color")
          #  sys.exit(0)
        #print("This image does not match with most instances of white background color")


