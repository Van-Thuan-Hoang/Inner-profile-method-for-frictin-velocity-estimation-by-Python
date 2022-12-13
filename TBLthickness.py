def TBLthickness(y,U,Ue):
    
    maxIndex = len(U)
    index = 1
    while (index <= maxIndex) & (U[index] < Ue):
        index += 1
    
    delta = y[index - 1] + (Ue - U[index - 1])*(y[index ] - y[index - 1])/(U[index ] - U[index - 1])
    indexDelta = index - 1

    return delta, indexDelta