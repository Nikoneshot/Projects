#!/usr/bin/env python
# coding: utf-8

# # Example Code for Lab 01
# Note: The data used in this example is made up, just for the purposes of illustrating the techniques. You should use the real data you collected in lab. Cells [6],[7] and [8] have the details on doing the fit

# In[ ]:


import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize 


# Read in the you data file 

# In[ ]:


data_file = np.loadtxt("Lab1_Data.csv", delimiter=',',skiprows=2)
v = data_file[:,0]
dv = data_file[:,1]
i = 0.001*data_file[:,2] #convert mA to Amp
di = 0.001*data_file[:,3]


# A function to calculate resistance 

# In[ ]:


def get_resistance_and_error(v,dv,i,di):
    #just Ohm's law
    resistance = v/i 
    #Use chain rule from calculus to calculate error
    error = np.sqrt(pow(dv/i,2) + pow(v*di/(i*i),2))
    return resistance, error


# Some code to loop over the data and calculated the resistance with error

# In[ ]:


#len(v) just gives the l
r =np.empty(len(v))

#initialise empty array to hold resistance uncertainty values
dr = np.empty(len(v))
for j in range(0, len(v)):
    r[j],dr[j]= get_resistance_and_error(v[j],dv[j],i[j],di[j])
    


# To combine the measurements, take the error weighted-mean and standard error

# In[ ]:


error_weighted_sum =0;
error_weights=0    

#Do the sums
for j in range(0, len(v)):
    error_weighted_sum += r[j]/pow(dr[j],2)    
    error_weights += 1/pow(dr[j],2)
    
#Next calculate finalize the average weighting     
mean_resistance = error_weighted_sum/error_weights
mean_resistance_error = 1/math.sqrt(error_weights)
print("Weighted mean resistance = %.1f Ohm"%mean_resistance)
print("Standard error  = %.1f Ohm" %mean_resistance_error)


# To fit Ohm's law to the data, we need to implement a function that we can pass to the fitting routine 

# In[ ]:


#Implement Ohm's law function 
def ohms_law(v_input,r_parameter):
    expected_current  =v_input/r_parameter
    return expected_current


# Next we use the "curve_fit" utility of the scipy otimize library to fit a function to the data.
# It returns the best-fit value of the parameters together with something called the covariance matrix. 
# We will discuss what all that means lecture but for now, you can assume the diagonal terms encode 
# the error estimate of the parameters squared. Meaning, if you want the error estimated by the fit on parameter 0, 
# you should take the square-root of the [0][0] element of the covariance matrix. 
# 
# The curve fit function takes the following parameters:
# 
# 1: The model function you want to fit to the data, for us this will be Ohm's law which we defined above
# 
# 2: The xdata, for us this is the voltage data (we are treating the voltage as the independent 
#    variable, i.e., the variable we control)
# 
# 3: The ydata, for us this is the current data ( so we are taking the measured current as the dependent variable)
# 
# 4: The "sigma" on the ydata, for us this is the current uncertainty 
# 
# 5: The parameter "absolute_sigma" can be set =1 or =0.  If it is =1 that means the errors we just passed are absolute    errors, if it is =0 that means the errors just passed are relative errors
# 
# 6: Note this optimization function does not allow for error on the xdata, it is assumed they are known perfectly. For    now we accept this as a compromise. Time permitting we can come back to this later in the course.  

# In[ ]:


params, params_covariance = optimize.curve_fit(
        f=ohms_law,xdata=v,ydata=i,sigma=di,absolute_sigma=1)
print("The resistance is ", params[0], " Ohm.\nThe uncertainty is", 
      math.sqrt(params_covariance[0][0]), "Ohm")


# It would be lunacy to report all the digits above! Next plot the data with the best-fit function

# In[ ]:


#You can see above the error bars are too small to see but they are there
plt.errorbar(x=v,y=i,xerr=dv,yerr=di,fmt='o',label='Data')
plt.plot(v,ohms_law(v,params[0]),label='Fitted function')
plt.legend(loc='best')
plt.xlabel('Applied Voltage (V)')
plt.ylabel('Measured Current (A)')
plt.title("Measured Current vs. Applied Voltage")
plt.savefig("My-beautiful-data.pdf")


# The material below is not needed for the report, but is included for your information 
# 
# You might notice the uncertainty returned by the fitting method (2.6 Ohm) is smaller than the uncertainty we get doing the error-weighted mean (4.5 Ohm).  Why is this when both methods use the exact same data ?  
# The reason is the fitting rountine used above does not account for error on the voltage (the xdata) and so the overall uncertainty being considered in the analysis is smaller. 
# To confirm this, below we set the voltage uncertainty to 0 V and redo the resistance calculations and error-weighted mean calculation

# In[ ]:


dv = 0*data_file[:,1] # set the voltage errors to zero

#redo the resistance calculation
for j in range(0, len(v)):
    r[j],dr[j]= get_resistance_and_error(v[j],dv[j],i[j],di[j])
    
    
#Redo the error weighted mean calculation
error_weighted_sum =0;
error_weights=0    
#Do the sums
for j in range(0, len(v)):
    error_weighted_sum += r[j]/pow(dr[j],2)    
    error_weights += 1/pow(dr[j],2)
         
mean_resistance = error_weighted_sum/error_weights
mean_resistance_error = 1/math.sqrt(error_weights)
print("Weighted mean resistance = %.1f Ohm"%mean_resistance)
print("Standard error  = %.1f Ohm" %mean_resistance_error)


# Now you see the error returned by both method is 2.6 Ohm.  We will use the error of 4.5 Ohm value as accounts for both the uncertainty in voltage and current.  We will introduce other fitting routines later in the course that accounts for the error on both V and I later in the course. 
# To report this value it doesn't make sense to keep all the digits returned by the computer. To 1 significant figure the uncertainty is 10 Ohm so we have 
# 
# R = 221 +/- 5 Ohms

# Finally, here is some perhaps useful code for printing out the data in LaTeX table format. You could use something like this to easily generate tables in your lab reports.
# 

# In[ ]:


dv = 1*data_file[:,1] # set the voltage errors back to the input values from the csv file
print("V(V) & dV(V) & I(mA) & dI(mA)  & R($\Omega$) & dR($\Omega$)\\\\")
print("[0.5ex]")
print("\\hline")

#Notice above I put mA for the units of current and dI, so below I multiply 
#by 1000 to convert A to mA for the current and dI parameters

for j in range(0, len(v)):
    print("%.2f&%.2f&%.2f&%.2f&%1.0f&%1.0f\\\\" 
          %(v[j],dv[j],1000*i[j],1000*di[j],r[j],dr[j]))
    print("[0.5ex]")
    print("\\hline")


# In[ ]:





#%%
