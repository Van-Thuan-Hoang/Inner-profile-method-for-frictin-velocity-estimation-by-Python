def IndexFind(y, y0):
    maxIndex = len(y)
    index = 0
    while (index < maxIndex) & (y[index] < y0):
        index += 1
    
    return index
