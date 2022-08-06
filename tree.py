import cv2
import numpy as np
import math
import time

class fractal_tree():
    def __init__(self, canvas, left_angle_delta = 30,right_angle_delta = -1, left_length_factor = 0.5,right_length_factor = -1,thickness_factor=0.1):
        self.canvas = canvas
        self.left_angle_delta = left_angle_delta
        self.right_angle_delta = right_angle_delta if (right_angle_delta != -1) else left_angle_delta
        self.left_length_factor = left_length_factor
        self.right_length_factor = right_length_factor if (right_length_factor != -1) else left_length_factor
        self.thickness_factor=thickness_factor
        self.leaves=[]
        print('TREE CREATED')
        print ('left_length_factor: ',self.left_length_factor,'  right_length_factor: ',self.right_length_factor)
        print ('left_angle_delta: ',self.left_angle_delta,'  right_angle_delta: ',self.right_angle_delta)

    def plant(self,length,angle=90,start_position = (-1,-1)):
        start_position = start_position if (start_position != (-1,-1)) else (int(self.canvas.shape[0]/2),int(self.canvas.shape[1]))
        self.root=branch(self,length,angle,start_position)
        self.leaves.append(self.root)
    
    def draw_leaves(self,step=100):
        for percent in range(0,101,step):
            for leaf in self.leaves:
                leaf.draw(percent)
            self.refresh_canvas()

    def draw_tree(self):
        self.canvas[::]=0
        self.draw_tree_recursion()
        self.refresh_canvas()

    def draw_tree_recursion(self,root=-1):
        if (root == -1):
            root = self.root
        root.draw()
        if(not root.is_leaf):
            self.draw_tree_recursion(root.left)
            self.draw_tree_recursion(root.right)

    def propagate_leaves(self,minimum_leaf_length = -1, growing_rate=100):
        new_leaves=[]
        leaves_propagated = 0
        for leaf in self.leaves:
            if ((minimum_leaf_length != -1 and leaf.length > minimum_leaf_length) or minimum_leaf_length == -1):
                leaves_propagated += 1
                left_sprout,right_sprout=leaf.propagate()
                new_leaves.append(left_sprout)
                new_leaves.append(right_sprout)
        self.leaves=new_leaves
        self.draw_leaves(growing_rate)
        return leaves_propagated
    
    def grow(self, minimum_leaf_length=1,growing_rate=5):
        leaves_propagated=1
        while (leaves_propagated>0):
            leaves_propagated=self.propagate_leaves(minimum_leaf_length,growing_rate)


    def refresh_canvas(self):
        cv2.imshow('image',self.canvas)
        cv2.waitKey(1)
    


class branch():
    def __init__(self, tree, length, angle, start_position = (-1,-1)):
        self.tree = tree
        self.length = length
        self.angle = angle
        self.start_position = start_position if (start_position != (-1,-1)) else (int(canvas.shape[0]/2),int(canvas.shape[1]))
        self.end_position = self.get_end_position()
        self.thickness=1
        self.thickness=self.get_thickness()
        self.is_leaf = True

    def propagate(self):
            left_length_factor = self.tree.left_length_factor
            right_length_factor = self.tree.right_length_factor
            left_angle_delta = self.tree.left_angle_delta
            right_angle_delta = -self.tree.right_angle_delta
            self.is_leaf = False
            self.right = branch(self.tree,self.length * right_length_factor, self.angle+right_angle_delta,self.end_position)
            self.left = branch(self.tree,self.length * left_length_factor, self.angle+left_angle_delta,self.end_position)
            return(self.left,self.right)

    def get_thickness(self,length=-1):
        length = length if (length != 1) else self.length
        thickness_factor=self.tree.thickness_factor
        return 1+int(self.length*thickness_factor)

    def get_end_position(self,length=-1):
        if (length == -1):
            length = self.length
        x = self.start_position[0] + length * math.cos(math.radians(self.angle))        
        y = self.start_position[1] - length * math.sin(math.radians(self.angle))
        return(int(x),int(y))

    def draw(self,percent=100):
        percent = percent/100
        leaf_length = self.length * percent
        end_position = self.get_end_position(leaf_length)
        thickness = self.get_thickness(leaf_length)
        cv2.line(self.tree.canvas,self.start_position,end_position,(255,255,255),thickness,lineType=16)
        #self.tree.refresh_canvas()



CANVAS_SIZE=(1080,1080,3)
def main():
    canvas = np.zeros(CANVAS_SIZE,dtype=np.uint8)
    tree = fractal_tree(canvas,left_angle_delta=25,left_length_factor=0.7,thickness_factor=0.1)
    tree.plant(200)
    tree.draw_leaves()
    tree.grow(5)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()    