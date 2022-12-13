def InnerProfileMethod(y0,  U, nuRef, Karray, aArray, deltaYarray, UtauSave0, deltaUtau):

    import time
    import matplotlib.pyplot as plt
    import numpy as np
    from UtauEstimationInnerProfileMethod import UtauEstimationInnerProfileMethod
    #-------------------------------------------------
    UtauSave = 0; Ksave = 0; aSave = 0; deltaYsave = 0

    maxArrayLengthK = 50; maxArrayLengthA = 50; maxArrayLengthDeltaY = 0; 
    increseNumK = 5; increseNumA = 10; increseNumDeltaY = 20

    EK = 0; EA = 0

    maxIndexK = len(Karray)-1
    maxIndexA = len(aArray)-1
    maxIndexDeltaY = len(deltaYarray)-1

    Emin = 1000000
    E = Emin + 1
    M1 = 30; M2 = 2.85

    # enable interactive mode
    plt.ion()
    fig = plt.figure(200, figsize=[7.5, 5.5])

    #-----------------------------------------------
    indexK = 0; EKarray = []
    while indexK <= maxIndexK:  
        K = Karray[indexK]
        indexA = 0; EAarray = []

        while indexA <= maxIndexA:   
            a = aArray[indexA]
            indexDeltaY = 0;  EdeltaY = []

            while indexDeltaY <= maxIndexDeltaY:
                deltaY = deltaYarray[indexDeltaY]
                y = y0 + deltaY
        
                Utau, E = UtauEstimationInnerProfileMethod(y, U, K, a, nuRef, UtauSave0, deltaUtau, M1, M2)
    
                if E < Emin:            
                    Emin = E            
                    Ksave = K
                    aSave = a
                    deltaYsave = deltaY
                    UtauSave = Utau  
         
                print([indexK, indexA, indexDeltaY, Karray[0], aArray[0], deltaYarray[0]*1000])
                print([maxIndexK, maxIndexA, maxIndexDeltaY, Karray[maxIndexK-1], aArray[maxIndexA-1], deltaYarray[maxIndexDeltaY-1]*1000])
                print([UtauSave, Ksave, aSave,  deltaYsave*1000, Emin*100]) 
        
                EdeltaY = np.append(EdeltaY,E)

                if indexDeltaY == maxIndexDeltaY:
                    EA = min(EdeltaY)
                    EdeltaY = []                

                if (indexDeltaY == maxIndexDeltaY) & (maxIndexDeltaY > 1) & (maxArrayLengthDeltaY > 0):
                    maxArrayLength = maxArrayLengthDeltaY
                    increseNum = increseNumDeltaY
                    if deltaYsave == deltaYarray[maxIndexDeltaY]:
                        deltaDeltaY = deltaYarray[maxIndexDeltaY] - deltaYarray[maxIndexDeltaY-1]
                        addDeltaY = np.arange(deltaYarray[maxIndexDeltaY]+deltaDeltaY,deltaYarray[maxIndexDeltaY]+increseNum*deltaDeltaY,deltaDeltaY)                        
                        deltaYarray = np.append(deltaYarray,addDeltaY)
                        maxIndexDeltaY = maxIndexDeltaY + increseNum - 1
                        if maxIndexDeltaY > maxArrayLength:
                            deltaIndex = maxIndexDeltaY - maxArrayLength
                            deltaYarray = deltaYarray[deltaIndex+1:maxIndexDeltaY]
                            maxIndexDeltaY = maxIndexDeltaY - deltaIndex - 1
                            indexDeltaY = indexDeltaY -  deltaIndex
            
                    elif deltaYsave == deltaYarray[0]:
                        deltaDeltaY = deltaYarray[1] - deltaYarray[0]
                        addDeltaY = np.arange(deltaYarray[0]-increseNum*deltaDeltaY,deltaYarray[0]-deltaDeltaY,deltaDeltaY)
                        deltaYarray = np.append(addDeltaY,deltaYarray)
                        deltaYarray = np.flipud(deltaYarray)
                        maxIndexDeltaY = maxIndexDeltaY + increseNum - 1
                        if maxIndexDeltaY > maxArrayLength:
                            deltaIndex = maxIndexDeltaY - maxArrayLength
                            deltaYarray = deltaYarray[deltaIndex+1:maxIndexDeltaY]
                            maxIndexDeltaY = maxIndexDeltaY - deltaIndex - 1
                            indexDeltaY = indexDeltaY -  deltaIndex 

                indexDeltaY = indexDeltaY + 1 
            # end of the delatY loop
                        
            EAarray = np.append(EAarray,EA)

            if indexA == maxIndexA:
                EK = min(EAarray)
                EAarray = []    
    
            if (indexA == maxIndexA) & (maxIndexA > 1) & (maxArrayLengthA > 0):
                maxArrayLength = maxArrayLengthA
                increseNum = increseNumA
                if aSave == aArray[maxIndexA]:            
                    aDelta = aArray(maxIndexA) - aArray(maxIndexA-1)                    
                    addA = np.arange(aArray[maxIndexA]+aDelta,aArray[maxIndexA]+increseNum*aDelta,aDelta)
                    aArray = np.append(aArray,addA)                        
                    maxIndexA = maxIndexA + increseNum - 1
                    if maxIndexA > maxArrayLength:
                        deltaIndex = maxIndexA - maxArrayLength
                        aArray = aArray[deltaIndex+1:maxIndexA]
                        maxIndexA = maxIndexA - deltaIndex - 1
                        indexA = indexA -  deltaIndex          
                elif aSave == aArray[0]:
                    aDelta = aArray[1] - aArray[0]                    
                    addA = np.arange(aArray[0]-increseNum*aDelta,aArray[0]-aDelta,aDelta)
                    aArray = np.append(addA,aArray)  
                    aArray = np.flipud(aArray)
                    maxIndexA = maxIndexA + increseNum - 1
                    if maxIndexA > maxArrayLength:
                        deltaIndex = maxIndexA - maxArrayLength
                        aArray = aArray[deltaIndex+1:maxIndexA]
                        maxIndexA = maxIndexA - deltaIndex - 1
                        indexA = indexA -  deltaIndex

            indexA = indexA + 1
        # end of the a loop

        EKarray = np.append(EKarray,EK)
    
        if (indexK == maxIndexK) & (maxIndexK > 1) & (maxArrayLengthK > 0):        
            maxArrayLength = maxArrayLengthK
            increseNum = increseNumK
            if Ksave == Karray[maxIndexK]:            
                Kdelta = Karray[maxIndexK] - Karray[maxIndexK-1]   
                addK = np.arange(Karray[maxIndexK]+Kdelta,Karray[maxIndexK]+increseNum*Kdelta,Kdelta)
                Karray = np.append(Karray,addK)
                maxIndexK = maxIndexK + increseNum - 1
                if maxIndexK > maxArrayLength:
                    deltaIndex = maxIndexK - maxArrayLength
                    Karray = Karray[deltaIndex+1:maxIndexK]                
                    EKarray = EKarray[deltaIndex+1:maxIndexK]
                    maxIndexK = maxIndexK - deltaIndex - 1
                    indexK = indexK -  deltaIndex        
            elif Ksave == Karray[0]:
                Kdelta = Karray[1] - Karray[0] 
                addK = np.arange(Karray[0]-increseNum*Kdelta,Karray[0]-Kdelta,Kdelta)
                Karray = np.append(addK,Karray)
                Karray = np.flipud(Karray)
                EKarray = np.flipud(EKarray)
                maxIndexK = maxIndexK + increseNum - 1
                if maxIndexK > maxArrayLength:
                    deltaIndex = maxIndexK - maxArrayLength
                    Karray = Karray[deltaIndex+1:maxIndexK]
                    EKarray = EKarray[deltaIndex+1:maxIndexK]
                    maxIndexK = maxIndexK - deltaIndex - 1
                    indexK = indexK -  deltaIndex

        indexK = indexK + 1

        fontSize = 12; lineWidth = 1.2

        # enable interactive mode
        #plt.ion()

        #plt.figure(200, figsize=[7.5, 5.5])

        #plt.figure(200, figsize=[7.5, 5.5])
        plt.plot(Karray[0:indexK],EKarray*100,'b-+',linewidth = lineWidth)
        plt.grid(True)
        plt.xlabel('K', fontsize = fontSize); plt.xticks(fontsize = fontSize)
        plt.ylabel('$\u0394E_{fitting}$', fontsize = fontSize); plt.yticks(fontsize = fontSize)
                
        plt.title('Fitting error at ' +  
          'K = ' + str("{:.3f}".format(Karray[indexK-1])) + 
          ', optimal K = ' + str("{:.3f}".format(Ksave))
          )

        plt.show()  
        
        # drawing updated values
        fig.canvas.draw() 

        plt.pause(0.0001)
    # end of the K loop

    return UtauSave, Ksave, aSave, deltaYsave
    
    
