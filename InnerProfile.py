def InnerProfile(yPlus,K,a,M1,M2):
    Uplus0, yPlus0, B = MuskerProfile(yPlus,K,a)
    Uplus = Uplus0 + BumpUplus(yPlus0,M1,M2)

    return Uplus, B

def MuskerProfile(yPlus,K,a):
    import numpy as np
    
    alpha = (-1/K - a)/2
    beta = np.sqrt(-2*a*alpha - alpha*alpha)
    R = np.sqrt(alpha*alpha + beta*beta)

    indexB = 0
    maxIndex = len(yPlus)
    yPlusB = 100
    while (indexB <= maxIndex) & (yPlus[indexB] < yPlusB):
        indexB += 1
    if indexB > maxIndex:
        yPlus.append(yPlusB)
        maxIndex += 1

    muskerUplus = 1/K*np.log((yPlus - a)/(-1*a))\
                  + R**2/a/(4*alpha - a)\
                  *(\
                  (4*alpha + a) * np.log( -a/R*( (yPlus-alpha)**2+beta**2 )**0.5 / (yPlus-a) )\
                  + alpha/beta * (4*alpha + 5*a) * ( np.arctan( (yPlus-alpha)/beta ) + np.arctan(alpha/beta) )\
                  )
    MuskerUplus = muskerUplus[0:maxIndex]
    B = muskerUplus[indexB] - 1/K*np.log(yPlus[indexB])

    return MuskerUplus, yPlus, B

def BumpUplus(yPlus,M1,M2):
    import numpy as np
    
    return np.exp( -1*np.log(yPlus/M1)**2 )/M2
