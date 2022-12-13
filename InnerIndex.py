def InnerIndex(Ue,y,U,Utau,nu):
    
    import math
    from TBLthickness import TBLthickness
    from IndexFind import IndexFind

    delta, indexDelta = TBLthickness(y,U,Ue)
    ReTau = delta*Utau/nu
    yPlusInner = 2.6*math.sqrt(ReTau)
    yPlus = y*Utau/nu
    indexInner = IndexFind(yPlus,yPlusInner)

    return indexInner