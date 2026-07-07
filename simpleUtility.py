class SimpleUtility:

    """
    limits value within a range

    @param value: the value to limit
    @param min: minimum range for value
    @param max: maximum range for value

    @return: min if value<min or max if value>max or value on all other cases
    """
    def limit(value,min,max):
        if value<min:
            return min
        elif value>max:
            return max
        return value