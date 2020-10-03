import load

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import norm
from scipy.optimize import minimize
from resource import mov_avg

"""__________________________
Observed variables:
pilong_delta    --> change in long term inflation expectation  
pishort_t       --> short term inflation expectation
pistar_t        --> inflation target
pi              --> inflation rate                        
_____________________________
"""

plt.style.use('classic')


pilong_delta = load.next5yearsmsc_delta
pilong       = load.next5yearsmsc
dat = load.datesmsc[1:]
#Skipping the first value because there is no value for pilong_delta
#this is due to the fact that pilong_delta is a first difference varaible
pishort = load.nextyearmsc[1:]
#Skipping the first value for the same reasons as for pilong_delta
pistar = [2 for t in range(len(pilong))]

pi = load.inflation_oecd
#Skipping the first value for the same

"""__________________________
Estimated Variables:
Through MLE:
alpha_0
alpha_1
sigma_eps_1
sigma_eps_2
sigma_v

Through the Kalman Filter:
theta_1
theta_2
u_t
_____________________________
"""



"""__________________________
system of equations:
pilong_delta_t = c_t + Z_t * theta_t      --> signal / observation
theta_t = d + T * theta_(t-1) + V_t       --> state  / transition
_____________________________
"""

timerange = range(len(pilong_delta))

#observation matrices
c = [(pistar[t+1] - pilong[t]) for t in timerange]
Z = np.array([    np.array([[pi[t] - pistar[t+1]],[pishort[t]-pistar[t+1]],[1]]).T   for t in timerange])

"""
Main Kalman Filter
The Main funtion for estimating the $\theta$ coefficients.
This funtion is iterated many times as the gaussian likelihood is maximized.
"""
def Kalman_Estimation(estim):
    """
    Kalman Estimation Function
    ____
    Input:
    observations
    estimations for alpha_0 alpha_1 and Sum
    ____
    Returns:
    Theta estimations    
    """
   
    mle_alpha_0,mle_alpha_1,mle_sigma_eps_1,mle_sigma_eps_2,mle_sigma_v = estim
    mle_sigma_eps_1 = np.exp(mle_sigma_eps_1)
    mle_sigma_eps_2 = np.exp(mle_sigma_eps_2)
    mle_sigma_v     = np.exp(mle_sigma_v)
    # exponential form to assure the variance being positive
        
    d   = np.array([0,0,mle_alpha_0])
    T   = np.diag ([1,1,mle_alpha_1])
    Sum = np.diag([mle_sigma_eps_1,mle_sigma_eps_2,mle_sigma_v]) 
    
    F =     [None for t in timerange]   #k x k
    e =     np.zeros(len(pilong_delta)) #1 x 1
    P =     [None for t in timerange]   #k x k
    K =     [None for t in timerange]   #k x 1
    S =     [None for t in timerange]   #k x k
    Theta = [None for t in timerange]   #k x 1
    pilong_delta_exp = [None for t in timerange] 
                                        #1 x 1
    pov =   [None for t in timerange]   #1 x 1
    
    

    #__________________________
    #initial states
    F[0] = None     #k x k
    e[0] = None     #single values
    P[0] = np.diag([0,0,0]) #k x k intitial error
    #Zeros seemed sensible
    K[0] = None     #k x 1
    S[0] = None     #k x k
    Theta[0] = np.array([0,0,0]) #k x 1
    #completely arbitrary choice for initial values of [theta_1,theta_2,u]
    
    
    
    #__________________________
    

    for t in range(1,len(pilong_delta)):
        #note: its easy to confuse " [variable].T " and " [variable]*T "
        #.T is the numpy transpose method and T is the state matrix as defined above
        
        #__________________________
        #Prediction Step
        
        S[t] = np.linalg.multi_dot([T,P[t-1],T]) + Sum
        #predicted state covariance

        predicted_observation_covariance = np.dot(Z[t],np.dot(S[t],Z[t].T))   
        pov[t] = predicted_observation_covariance
        
        #predicted_observation_covariance
        #returns a scalar
        
        pilong_delta_exp[t] = c[t] + np.dot(Z[t],(d + np.dot(T,Theta[t-1])))
        #predicted observation mean
        #theta[t] not knowiing pilong_delta[t]
        
        #__________________________
        #Estimation Step
        
        
        K[t] = np.dot(S[t],np.dot(Z[t].T, np.linalg.pinv(predicted_observation_covariance)))
        #kalman gains
        
        P[t] = S[t] - np.dot(K[t],np.dot(Z[t],S[t]))
        #corrected state covariance

        Theta[t] = d + np.dot(T,Theta[t-1]) + np.dot(K[t], (pilong_delta[t] -(c[t] + np.dot( Z[t] ,(d + np.dot(T,Theta[t-1])))))) #theta[t] knowing pilong_delta[t]
        #corrected_state_mean
        
        #__________________________
        #Variables for Gaussian Likelihood
        
        e[t] = pilong_delta[t] - pilong_delta_exp[t]
        #Forecast Error
        
        F[t] = (np.linalg.multi_dot([Z[t],S[t],Z[t].T]))
        #Variance of Forecast Error is the predicted_observation_covariance


    
    return [Theta,F,e,P,S,d,T,Sum,pilong_delta_exp,pov]



"""__________________________
Log Likelihood Function
This method calculates the gaussian likelihood for a Kalman filter output, if the filter recieves a set of estimates for the $\gamma$ variables.
The function has its maximum at the most probable estimates for the $\gamma$ variables.
Therefore the most likely estimates for $\gamma$ can be found out by maximizing the function.
_____________________________
"""

def loglikfun(estim):#the likelihood of the given parameters
    """
    Loglikelihood estimation
    ____
    Input:
    values for the unknown parameters alpha_0,alpha_1,sigma_eps_1,sigma_eps_2,sigma_v
    in a list named "estim"
    ____
    Returns:
    the loglikelihood that the given values for the parameters are true
    
    ____
    most of the variables are redefined when the values for the estimated parameters is changed
    the temporary variables are marked with an underscore --> variable_
    all other variables are observations or constants
    """
    

    Kalman_returns = Kalman_Estimation(estim)
    Theta_,F_,e_,P_,S_,d_,T_,Sum_,pilong_delta_exp,pov = Kalman_returns
    
    term_1 = - len(pilong_delta) * 0.5 * np.log(2*np.pi)
    term_2 = - 0.5 * sum([np.log(np.absolute(F_[t])) for t in timerange[1:]])
    term_3 = - 0.5 * sum([np.dot(e_[t],e_[t])/F_[t] for t in timerange[1:]])
    
    loglik = sum([term_1,term_2,term_3])
    #calculation of likelihood
    
    #print( loglik )
    return -loglik 
    #return a negative value because the optimization algorithm minimizes



"""__________________________
Maximizing the Likelihood Function}
To maximize the LogLikelihood function, an iterative optimization Algorithm is applied to it.
Standard Scipy librarys provide only minimizing algorithms. It is allthough possible to find the optimal estimates by simply having the likelihood function return negatives of the likelihood.
The algorithm then finds the most likely estimates by minimizing it.
The Maximization function applies the minimizing algorithm to the likelihood function.
_____________________________
"""
def MaxLikEstim(init_est):
    """
    Maximum Likihood Estimation Function
    ____
    Input:
    initial values for the estimated variables
    ____
    Returns:
    maximum likihood estimates for the estimated variables
    """
    
    print("Optimizing likelihood for Gamma Variables...\n")
    estim = minimize(loglikfun,init_est,method='L-BFGS-B',options = {'gtol':1e-6, 'maxfun' : 5000})    
    print("Calculating Thetas...\n")
    return(estim.x)



"""__________________________
Confidence Bands
Confidence Bands are calculated by standard procedures as described in the empirical model section.
_____________________________
"""
def confidence_band (series_mean,series_var,alpha):
    """
    ____
    Input:
    Time series of a Theta estimates (series_mean)   
    Alpha Value
    ____
    Return:
    two time series that form a confidence band around the input time series
    the confidence level is given by the quantiles
    alpha = lower quantile + ( 1 - upper quantile )
    """      
    confidence_band_upper = [(series_mean[t]) + (norm.ppf(1-alpha/2) * (np.sqrt(series_var[t])))
                       for t in range(len(series_mean))]    
    confidence_band_lower = [(series_mean[t]) - (norm.ppf(1-alpha/2) * (np.sqrt(series_var[t])))
                       for t in range(len(series_mean))]

    return confidence_band_upper,confidence_band_lower

init_est = np.array([0,0,0,0,0])
#alpha_0,alpha_1,sigma_eps_1,sigma_eps_2,sigma_v
#take the results from nautz paper as starting points in the optimization


optim_est = MaxLikEstim(init_est)
Kalman_return = Kalman_Estimation(optim_est)
#Kalman_return = [Theta,F,e,P,S,d,T,Sum,pilong_delta_exp,pov]



for ind in range(3):
    print(["\nd matrix: \n","\nT matrix: \n","\nSUM matrix: \n"][ind])
    print(Kalman_return[ind+5],'\n')



#_____________________________
#generating the variables from the kalman results
thetas   = Kalman_return[0][1:]
#skip the first value bc the variance is unknown for the first value
thetaone = [(theta[0]) for theta in thetas]           
thetatwo = [(theta[1]) for theta in thetas]             
thetau   = [(theta[2]) for theta in thetas]             
thetas = [thetaone,thetatwo,thetau]

Ps       = Kalman_return[3][1:]
#skip the first value bc the variance is unknown for the first value
Pone = [(P[0][0]) for P in Ps]
Ptwo = [(P[1][1]) for P in Ps]
Pu   = [(P[2][2]) for P in Ps]
thetas_var   = [Pone,Ptwo,Pu]

anchoring = [[1-thetaone[idx]-thetatwo[idx] for idx in range(len(thetaone))]]
anchoring_var = [[Pone[idx] + Ptwo[idx] for idx in range(len(Pone))]]
#adding variances bc the thetas are assumed to be independend of each other
#_____________________________


alpha = 0.05
confidence_bands_bool = True
smoothed_bool         = False


if confidence_bands_bool:
    #_____________________________
    #calculating the confidence bands
    print("Alpha level is at {} percent.".format(alpha *100))    
    thetas_confidence_bands = [confidence_band(thetas[series_idx],thetas_var[series_idx],alpha) for series_idx in range(len(thetas))]
    anchoring_confidence_bands = [confidence_band(anchoring[series_idx],anchoring_var[series_idx],alpha) for series_idx in range(len(anchoring))]
        
    names = ['Theta 1', 'Theta 2']
    for idx in range(len(names)):
        plt.title( names[idx] , fontsize = 28)
        plt.plot(dat[1:][308:450],thetas[idx][308:450],label = 'Mean Estimate',color='r')
        plt.plot(dat[1:][308:450],thetas_confidence_bands[idx][0][308:450],label = 'Confidence Bands',color='b',alpha = 0.7)
        plt.plot(dat[1:][308:450],thetas_confidence_bands[idx][1][308:450],color='b',alpha = 0.7)
        plt.plot(dat[308:450],[0 for _ in dat[1:][308:450]])
        plt.legend(fontsize = 20)
        plt.show()
    
    if not smoothed_bool:
        plt.title('Anchoring', fontsize = 24)
        plt.plot(dat[1:][308:450],anchoring[0][308:450],label = 'Mean Estimate',color='r')
        plt.plot(dat[1:][308:450],anchoring_confidence_bands[0][0][308:450],label = 'Confidence Bands',color='b',alpha = 0.7)
        plt.plot(dat[1:][308:450],anchoring_confidence_bands[0][1][308:450],color='b',alpha = 0.7)
        plt.plot(dat[1:][308:450],[1 for _ in dat[1:][308:450]])
        plt.legend(fontsize = 20)
        plt.show()
        
    else:   
        plt.plot(dat[1:][308:450],anchoring[0][308:450],label = 'Mean Estimate', color='k')
        plt.plot(dat[1:][308:450],anchoring_confidence_bands[0][0][308:450],label = 'Confidence Bands',color='k',alpha = 0.7)
        plt.plot(dat[1:][308:450],anchoring_confidence_bands[0][1][308:450],color='k',alpha = 0.7)
        plt.plot(dat[308:450],[1 for _ in dat[1:][308:450]])
        plt.legend(fontsize = 20)
        plt.show()
    #_____________________________


plt.title('Corrected State Covariance',fontsize = 38)
plt.plot(dat[1:][308:450],[1/(P[0][0]) for P in Kalman_return[3][1:][308:450]],label = 'Theta 1',color = 'b')
plt.plot(dat[1:][308:450],[1/(P[1][1]) for P in Kalman_return[3][1:][308:450]],label = 'Theta 2',color = 'k')
plt.plot(dat[1:][308:450],[1/(P[2][2]) for P in Kalman_return[3][1:][308:450]],label = 'u',color = 'r')
plt.legend(fontsize = 20)
plt.show()

plt.title('Kalman Prediction', fontsize = 24)
plt.plot(dat[308:450],pilong_delta[308:450],label = 'Change in Long-Term Inflation Expectations',color='b',alpha = 0.5)
plt.plot(dat[308:450],Kalman_return[-2][308:450],label = 'Kalman Filter Prediction',color = 'r')
plt.plot(dat[308:450],[0 for _ in dat][308:450],color = 'k')
plt.legend()
plt.show()
