'''
Subjest:   Estimation of friciton velocities
Author: Van Thuan Hoang
Time:   Dec 2022
Reference: 
Instruction: 
'''

import os
import time
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from InnerProfileMethod import InnerProfileMethod
from InnerIndex import InnerIndex
from InnerProfile import InnerProfile
from TBLthickness import TBLthickness


os.system("cls")
print('-------------------------------------------------------------------')

fontSize = 12; lineWidth = 1.2
# --------------------------------------------------------------------------

fileName ='Input_Data.mat'

varData = scipy.io.loadmat(fileName, variable_names = 'y'); y = varData['y']; numY = len(y); y = y[0:numY,0]    #print(y)
varData = scipy.io.loadmat(fileName, variable_names = 'U'); U = varData['U']; U = U[0]                          #print(U)
varData = scipy.io.loadmat(fileName, variable_names = 'nu'); nu = varData['nu']; nu = nu[0,0]                   #print(nu)

#Kstr = '_Kfixed'; aStr = '_aFixed'; deltaYstr = ''
#Kstr = ''; aStr = ''; deltaYstr = '_deltaYfixed'
Kstr = ''; aStr = '_aFixed'; deltaYstr = '_deltaYfixed'

# Estimate friction velocity for smooth surface cases

# Optimize von Karman contant
minK = 0.375; maxK = 0.385; deltaK = 0.001
    
# Optimize aditive coefficient, a
minA = -10.5; maxA = -10; deltaA =   0.01 
    
# Optimize deltaY: Accuracy of the closest measured location to the surface
deltaYmin = -0.05e-3; deltaYmax = 0.15e-3; deltaYdelta = 0.01e-3
#deltaYmin = -0.05e-3; deltaYmax = 0.2e-3; deltaYdelta = 0.15e-3

Utau = 1.77; deltaUtau = 1e-5
      
Karray = np.arange(minK,maxK,deltaK)                          # print(Karray)
aArray = np.arange(minA,maxA,deltaA)
deltaYarray = np.arange(deltaYmin,deltaYmax,deltaYdelta)
 
if Kstr == '_Kfixed': Karray = np.array([0.384])    
if aStr == '_aFixed': aArray = np.array([-10.3061])
if deltaYstr == '_deltaYfixed':  deltaYarray = np.array([0])

Utau, Ksave, aSave, deltaYsave = InnerProfileMethod(y,U,nu,Karray,aArray,deltaYarray,Utau,deltaUtau)

#time.sleep(5)
# --------------------------------------------------------------------------
M1 = 30; M2 = 2.85

y = y + deltaYsave

yPlusExperiment = y * Utau/nu       # y in wall units        
UplusExperiment = (U / Utau)        # mean velocity in wall unit 

Ue = 0.99*max(U)
delta, indexDelta = TBLthickness(y,U,Ue)
indexInner = InnerIndex(Ue,y,U,Utau,nu)
indexComparison = np.arange(0,indexInner+1) 
Uplus, Bsave = InnerProfile(yPlusExperiment[indexComparison],Ksave,aSave,M1,M2)
nComparison = len(indexComparison);            
Emin_whole = 1/nComparison *sum( abs(Uplus - UplusExperiment[indexComparison])/abs(Uplus) )*100

maxX = 15; linearX = np.arange(1,maxX) 
logX = np.arange(5,yPlusExperiment[indexDelta],5)  
logY = 1/Ksave*np.log(logX)+Bsave

Cf = 2*(Utau/Ue)**2

# Plot the result of the fitting method
plt.figure(1, figsize=[7.5, 5.5])
plt.semilogx(yPlusExperiment, UplusExperiment,'ko',linewidth = lineWidth)
plt.semilogx(yPlusExperiment[indexComparison], Uplus,'m-+',linewidth = lineWidth)
plt.semilogx(linearX,linearX,'k--',linewidth = lineWidth)
plt.semilogx(logX,logY,'b--',linewidth = lineWidth)

# Get current axis
ax = plt.gcf().gca()
txtStr = '$U_{\u03C4}$ = ' + str("{:.4f}".format(Utau)) + ' m/s'
ax.annotate(txtStr,
            xy=(yPlusExperiment[7], UplusExperiment[7]),
            xytext=(yPlusExperiment[7]+5000, UplusExperiment[7]),
            va='center', ha='right',
            arrowprops={'arrowstyle':'-|>', 'lw': 1}, fontsize = fontSize)

plt.xlim([1, 1e5])

plt.grid(True)
plt.xlabel(r'$\bf{y^+}$', fontsize = fontSize); plt.xticks(fontsize = fontSize)
plt.ylabel(r'$\bf{U^+}$', fontsize = fontSize); plt.yticks(fontsize = fontSize)
plt.legend([ 'Experimental data by Osterlund (1999)', 'Proposed profile','Linear profile','Log-law profile'], fontsize = fontSize, loc='lower right')
plt.title('Velocity profile' +  
          ', K = ' + str("{:.3f}".format(Ksave)) + 
          ', a = ' + str("{:.3f}".format(aSave)) +
          ', B = ' + str("{:.3f}".format(Bsave)) +
          '\n$\u0394E_{fitting}$ = ' + str("{:.2f}".format(Emin_whole)) + ' %' +
          ', $C_f$ = ' + str("{:.6f}".format(Cf)) +
          ', \u0394y = ' + str("{:.2f}".format(deltaYsave*1e3)) + ' mm'
          )

plt.show(block=True)



