import numpy as np
from PIL import ImageTk, Image

def MatrixDifferenceNumpy (A, B):
    #result = np.sum( np.absolute(np.array(A) - np.array(B)) )
    result = np.average(np.absolute((np.array( np.mean(list(A.getdata()), axis=1) ) - np.array( np.mean(list(B.getdata()), axis=1) ))))
    return result