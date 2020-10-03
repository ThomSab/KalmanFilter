<img src="https://user-images.githubusercontent.com/64082072/94999923-0c678200-05bd-11eb-90ad-8a73a6f6aa25.jpeg" width="287" height="446" alt="Rudolf Emil Kálmán">


## KalmanFilter
Custom implementation of the Kalman-Bucy-Filter as a part of my Bachelor Thesis
Description are passages taken directly from the thesis:

## Thesis

The Title of the thesis was "Using Consumer Data to determine the Time-Varying Degree of Inflation Expectation Anchoring".
I summary, the point of the thesis was to investigate US consumer data between 2004 and 2014 for periods of de-anchoring from the inflation target given by the central bank.
This repo is although only here for displaying the code itself.

## Data 

The data used for the model is based on a monthly consumer survey conducted
through telephone by the University of Michigan. Started in 1946 on a three
times per year basis, the University has since then increased size and frequency
of the surveys. 
The inflation rates data that this filter was written for was taken directly from the OECD.
Beyond the consumer inflation expectations and inflation rates, a dataset for the central bank’s
inflation target is required. The US central bank’s exact inflation target has
not been announced up until 2012, when it was announced to be 2%. The
target is therefore assumed to be constant at that level over the entire considered timespan.

## Model
The model for which I implemented the filter in short is:

∆π<sup>e</sup><sub>l,t</sub> = (1 − θ<sub>1</sub> − θ<sub>2</sub>)(π<sup>*</sup> − π<sup>e</sup><sub>l,t</sub>) + θ<sub>1</sub>(π<sub>t-1</sub> − π<sup>e</sup>
<sub>l,t</sub>) + θ<sub>2</sub>(π<sup>e</sup><sub>s,t−1</sub> − π
<sup>e</sup>
<sub>l,t</sub>) + u

With π<sup>e</sup><sub>l,t</sub> being the long-term inflation expectation at the time t, π<sup>e</sup><sub>s,t−1</sub> the short-term inflation expectations,
π<sup>∗</sup> the central banks inflation
target, π<sub>t−1</sub> the actual inflation rate at time t − 1, and u the error term.

θ<sub>1</sub> and θ<sub>2</sub> are estimated by the filter.
For more details on the  estimation itself see Hamilton (1994).
