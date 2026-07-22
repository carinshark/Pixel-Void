import numpy as np


"""
limits value within a range

@param value: the value to limit
@param min: minimum range for value
@param max: maximum range for value

@return: min if value<min or max if value>max or value on all other cases
"""
def limit(value,min,max):
    if type(value)==tuple:
        temp=[]
        for item in value:
            temp.append(limit(item,min,max))

        return tuple(temp)

    else:
        if value<min:
            return min
        elif value>max:
            return max
        return value

#combine colors
def mix_colors(color1:np.ndarray,color2:np.ndarray):
    return np.average(np.array((color1,color2)),0).astype("uint8")


#check if item is within startpos and startpos+size
def in_range(item:tuple,startPos:tuple,size:tuple):
    if item[0]<startPos[0] or item[0] > startPos[0]+size[0]:
        return False
    elif item[1]<startPos[1] or item[1] > startPos[1]+size[1]:
        return False
    else:
        return True


def subtract(item:tuple,item2:tuple):
    return (item[0]-item2[0],item[1]-item2[1])
