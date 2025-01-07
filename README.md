




## KalmanFilter
Custom implementation of the Kalman-Bucy-Filter as a part of my Bachelor Thesis at Freie Universität Berlin.
The thesis and implementation are briefly summarized below:

## Thesis

The Title of the thesis is "Using Consumer Data to determine the Time-Varying Degree of Inflation Expectation Anchoring" commited to the chair of Econometrics of the Freie Universität Berlin.
In summary, the research goal of the thesis was to investigate US consumer data between 2004 and 2014 for periods of de-anchoring from the inflation target given by the central bank.
Because there were a number of issues concerning the consumer data on inflation expectations, results of the thesis were not conclusive. The implemented methods did however function as intended.

## Data 

A number of different datasets were employed in this thesis, namely consumer survey data, inflation data and data on the central bank's inflation target.
The data used for the model is based on a monthly consumer survey conducted through telephone by the University of Michigan. Started in 1946 on a three times per year basis, the University has since then increased size and frequency of the surveys. 
Tnflation rates data that the Kalman-Bucy filter was applied to were retrieced directly from the OECD website.
Beyond the consumer inflation expectations and inflation rates, a dataset for the central bank’s inflation target was retrieved.
The US central bank's exact inflation target has not been announced up until 2012, when it was announced to be 2%. The target was therefore assumed to be constant at that level over the entire considered timespan.

## Model
The state-space model for which the filter was implemented is defined as follows:

∆π<sup>e</sup><sub>l,t</sub> = (1 − θ<sub>1</sub> − θ<sub>2</sub>)(π<sup>*</sup> − π<sup>e</sup><sub>l,t</sub>) + θ<sub>1</sub>(π<sub>t-1</sub> − π<sup>e</sup>
<sub>l,t</sub>) + θ<sub>2</sub>(π<sup>e</sup><sub>s,t−1</sub> − π
<sup>e</sup>
<sub>l,t</sub>) + u

With π<sup>e</sup><sub>l,t</sub> being the long-term inflation expectation at the time t, π<sup>e</sup><sub>s,t−1</sub> the short-term inflation expectations,
π<sup>∗</sup> the central banks inflation
target, π<sub>t−1</sub> the actual inflation rate at time t − 1, and u the error term.

θ<sub>1</sub> and θ<sub>2</sub> are estimated by the filter.
For more details on the  estimation itself see Hamilton (1994).

## Results

As mentioned, results on whether there was a significant period of de-anchoring of inflation expectation from the central bank's inflation target during the investigated period were inconclusive.
Fortunately the lack of clear results cannot be attributed to the algorithm or model, both of which functioned as intended.
The figure below shows the estimated level of inflation expectation compared to the inflation target in the time between 2004 and 2014.

<img src="https://private-user-images.githubusercontent.com/64082072/400851416-2a5230bf-f2b5-4347-84e6-05ed288f4a66.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzYyNjkwMTMsIm5iZiI6MTczNjI2ODcxMywicGF0aCI6Ii82NDA4MjA3Mi80MDA4NTE0MTYtMmE1MjMwYmYtZjJiNS00MzQ3LTg0ZTYtMDVlZDI4OGY0YTY2LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAxMDclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMTA3VDE2NTE1M1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWQ1ZDQ1MDg4ZGM0NDA1NWZkMGZlZThjZjJiMDE4MTJkMmQwMTJmZTdhNzdjZWQ5NTVkYzM2OWYzMTU3MTliNGMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.RAjRgEi3aQZFl7KmMAgvxiPSPxsPMLabeOyHRBLD9wU" width="800" >


## Kálmán Portrait

I like to draw in my free time so I sketched Kálmán during the time of writing the thesis.

<figure class="image"> 
  <img src="https://user-images.githubusercontent.com/64082072/94999923-0c678200-05bd-11eb-90ad-8a73a6f6aa25.jpeg" width="287" height="446" alt="Rudolf Emil Kálmán" description="Rudolf Emil Kálmán">
  <figcaption>Rudolf Emil Kálmán</figcaption>
</figure>

