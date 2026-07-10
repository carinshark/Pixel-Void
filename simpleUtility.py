import numpy as np

class SimpleUtility:

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
                temp.append(SimpleUtility.limit(item,min,max))

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
    


