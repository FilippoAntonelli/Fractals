import cv2
import numpy as np
import math
import time



class branch():
    def __init__(self, canvas, length, angle, start_position = (-1,-1), angle_delta = 0.9, length_factor = 0.5,thickness_factor=0.1):
        self.canvas = canvas
        self.length = length
        self.angle = angle
        self.angle_delta = angle_delta
        self.length_factor = length_factor
        self.thickness=1+int(self.length*thickness_factor)
        pixel_color=np.zeros((1,1,3))
        pixel_color=(255,255,255)
        #self.color=cv2.cvtColor(pixel_color,cv2.COLOR_HSV2BGR)
        color_component=int(self.length*self.thickness%255)
        self.color=(color_component,255-color_component,color_component)
        self.start_position = start_position if (start_position != (-1,-1)) else (int(canvas.shape[0]/2),int(canvas.shape[1]))
        self.end_position = self.get_end_position()
        #print('ANGLE: ',self.angle, '    SIN: ',math.sin(math.radians(self.angle)), '    COS: ',math.cos(math.radians(self.angle)))
        #print('STARTPOS',self.start_position)
        #print('ENDPOS',self.end_position)

    def get_end_position(self):
        x = self.start_position[0] + self.length * math.cos(math.radians(self.angle))        
        y = self.start_position[1] - self.length * math.sin(math.radians(self.angle))
        return(int(x),int(y))

    def draw(self):
        if(self.length>20):
            cv2.line(self.canvas,self.start_position,self.end_position,self.color,self.thickness)
            self.right = branch(self.canvas,self.length*self.length_factor, self.angle+self.angle_delta,self.end_position,self.angle_delta, self.length_factor)
            self.left = branch(self.canvas,self.length*self.length_factor, self.angle-self.angle_delta,self.end_position,self.angle_delta, self.length_factor)
            self.refresh_canvas()
            cv2.waitKey(1)
            #time.sleep(0.2)
            self.right.draw()
            self.left.draw()

    def refresh_canvas(self):
        cv2.imshow('image',self.canvas)   

CANVAS_SIZE=(1080,1080,3)
def main():
    canvas = np.zeros(CANVAS_SIZE,dtype=np.uint8)
    tree = branch(canvas,length = 200,angle=90,angle_delta=20,length_factor=0.8)
    tree.draw()
    cv2.waitKey(0) 
"""
for x in range(0,360,15):
    print('ANGLE: ',x, '    SIN: ',math.sin(math.radians(x)), '    COS: ',math.cos(math.radians(x)))
"""


if __name__ == "__main__":
    main()    