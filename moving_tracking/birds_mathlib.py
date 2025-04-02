import math

# Constants
PI = 3.141592653589793
E = 2.718281828459045

    # Basic Operations for tracking algo    
    
# X, Y = [x,y] coordinates
def distEuclides(X, Y):
    return math.sqrt((X[0]-Y[0])**2 + (X[1]-Y[1])**2)
    
# calculate centre of masses for box object    
# bounding_box: [x, y, w, h]
def massCentre(bounding_box):
    return [(bounding_box[0] + bounding_box[2])/2, (bounding_box[1] + bounding_box[3])/2]

# bounding_box: [x, y, w, h]
def Square(bounding_box):
    return bounding_box[2] * bounding_box[3]
