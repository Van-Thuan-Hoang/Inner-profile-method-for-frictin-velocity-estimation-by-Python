def UtauEstimationInnerProfileMethod(y, U, K, a, nu, Utau0, deltaUtau, M1, M2):
    import numpy as np
    import math
    from InnerIndex import InnerIndex
    from InnerProfile import InnerProfile

    Ue = 0.99*max(U)
    nComparison = InnerIndex(Ue,y,U,Utau0,nu)
    indexInner = np.arange(0,nComparison+1) 
    Utau = Utau0;                       # inital guessed value of the friction velocit            
    yPlusExperiment = y * Utau/nu       # y in wall units        
    UplusExperiment = (U / Utau)        # mean velocity in wall unit
            
    Uplus0, B = InnerProfile(yPlusExperiment[indexInner],K,a,M1,M2)  
    residual1 = 1/nComparison *sum( abs(Uplus0 - UplusExperiment[indexInner])/abs(Uplus0) )
                        
    index = 1;           
    Utau = Utau - deltaUtau;   
    nComparison = InnerIndex(Ue,y,U,Utau,nu)
    indexInner = np.arange(0,nComparison+1) 
    yPlusExperiment = y * Utau/nu          # y in wall units
    UplusExperiment = (U / Utau)
            
    Uplus0, B = InnerProfile(yPlusExperiment[indexInner],K,a,M1,M2)              
    residual = 1/nComparison *sum( abs(Uplus0 - UplusExperiment[indexInner])/abs(Uplus0) )
    
    # The sign of delta uTau
    signDeltaUtau = -1
    if (residual > residual1):
        signDeltaUtau = 1        
            
    residual0 = 1000000
    residual = residual0 - 0.1; 
    indexMax = math.floor(Utau0/deltaUtau) + 1
         
    while (Utau >0) & (index<indexMax) & (residual < residual0):  
        Utau = Utau + signDeltaUtau * deltaUtau
        nComparison = InnerIndex(Ue,y,U,Utau,nu)
        indexInner = np.arange(0,nComparison+1)
        yPlusExperiment = y * Utau/nu;     # y in wall units        
        UplusExperiment = (U / Utau)       # mean velocity in wall unit
                
        Uplus0, B = InnerProfile(yPlusExperiment[indexInner],K,a,M1,M2)                         
        residual0 = residual
        residual = 1/nComparison *sum( abs(Uplus0 - UplusExperiment[indexInner])/abs(Uplus0) )
 
        index = index + 1                
            
    Utau = Utau - signDeltaUtau * deltaUtau; 
    residual = residual0
            
    frictionVelocity = Utau
    E1 = abs(residual)

    return frictionVelocity, E1

    