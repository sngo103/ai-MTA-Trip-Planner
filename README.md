# ai-MTA-Trip-Planner
### By Team Wish Upon A*
### Anton Goretsky, Samantha Ngo, Daniel Rozenzaft

For our current plans, issues, and features, please see notes.txt

Note: All three of us have been working together via Microsoft LiveShare.
We often host on Daniel's PC, so most commits are in his name.

NEXT FIXES:
-(Manually) fill in unlisted latitude and longitude values in stop_directory.csv
-General code cleanup in subway_system.py and basic_search.py
-Apply current_state structure?
-Route is sometimes not picking the shortest path
    -Needs confirmation

ISSUE:
-Import loops resulting from current_state structure
    -current_state is not being utilized at the moment

NEXT STEPS:
- Have algorithm better detect which train to start/end with if the user inputs stops with many available trains
    -Currently randomized
- ensure that the user does not need to enter the exact name of desired stops
    -there is presently no way to distinguish between stops with the same station name
        -ex: "7th Av" is a stop in Brooklyn on the F/G, a different Brooklyn stop on the B/Q, and a Manhattan stop on the B/D/E
        -the current method of relating user-inputted station names to stopIDs (mta.findStop) cannot distinguish between these different stations
    -current solution: allowing keywords (algorithm accepts substrings of station names)
    -potential improvement: use a drop-down GUI?


Things Completed:

-Much improved A* search, supporting transfers and routes in both directions
-Heuristic that takes into account latitude/longitude-based distance to the end stop, number of transfers made, and distance to the end stop (now including transfers!)
-Four-borough data set (though a few latitude and longitude values need to be inputted)
-Standardized station names in stop_directory (same types of dashes are used; "th," "rd" or "nd" are inputted for all numbered station names)
-Continuing to fix issues related to null pointers in data files
-Resolved issue in Stop class __eq__ method
-Smarter, heuristic-based train selection for starting stations with multiple line options
-Heuristic takes into account total stops to destination, including transfers
-Randomly chosen starting and ending stations when there are multiple options that match user inputs

Samantha Ngo | 23765404
CSCI 350
Assignment 3
2020-05-01

Dependencies:
- Python version: >3.6.0
- Outside Modules Used:
-- Perceptrons[numpy, pandas, matplotlib, sys, csv]
-- LinReg[numpy, pandas, sys, math]
-- K-Means Clustering[numpy, sys, sklearn, cv2, matplotlib]

My Environment Specifics(conditions under which I wrote and ran my code):
- Python Version: 3.7.4
- Operating System: Windows 10
- IDE: Atom

Usage Instructions:
- Perceptrons: python problem1.py input1.csv output1.csv
- Linear Regression: python problem2.py input2.csv output2.csv
- K-Means Clustering: python problem3.py

Limitations:
- Perceptron: N/A
- LinReg: Not sure if it is optimal.
- K-Means Clustering: N/A

Important Notes:
- Perceptron: N/A
- LinReg: N/A
- K-Means Clustering: Program displays 3 cluster variations using matplotlib. If you
are going to run the file and don't want the images to display, comment out the display
function calls at the bottom of problem3.py; Screenshots from testing can be found
in the KMeans Screenshots folder and are referenced by file name in my
explanation below; problem3.py DOES NOT read in the pixel array from input3.csv--
it creates a pixel array from 'trees.png' in the directory. This wasn't specified
in the instructions and I already wrote the code, so I didn't change it.

Tasks:
- Perceptrons - completed
- Linear Regression with Gradient Descent - completed, but may not be optimal, I'm also not
sure if it's completely correct.
- K-Means Clustering - completed

Perceptrons: N/A

Linear Regression: I chose the learning rate 1.0 and the loop count 98
because I observed it to have the lowest risk(cost) out of all the rates.
Based on my observations, from learning rate 0.001 to 1.0, the risk
decreased from 0.20 to 0.10. After a learning rate of 1.0, the risk
dramatically increased to 9.06 at a learning rate of 10.0. I decided to
focus in on learning rates around near 1.0 and varying loop counts to
try and lower the risk, but the lowest I was able to achieve was a risk
of 0.10837766541850194 at learning rate 1.0 and loop count 98, down 1e-17
from 0.10837766541850195 at learning rate 1.0 and loop count 100. It may
have decreased further passed that decimal as I tested, but I was unable
notice any further differences due to python's float size. However, if
there was any further differences past the last decimal, they are likely
negligible.

K-Means Clustering: The three representative k-values I chose are 2, 5, and 50.
Using these three k-values, I tested segemented images using KMeans first with
kmeans++ for choosing the initial cluster centers and then choosing them randomly.
I observed that the greater the k-value, the more similar the picture is to the
original, the clearer the image is, the more colorful the image is, and the longer
it takes to process. With image segmentation, the clusters sort the pixels by color,
so the greater k is, the greater number of colors. The init algorithm kmeans++
chooses initial cluster centers that are optimal in producing the best image.
However, when compared with randomly choosing initial cluster centers, it didn't
seem to make that big a difference in the outcome of the image. The comparisons
are shown in '2 clusters labeled.png', '5 clusters labeled.png', and
'50 clusters labeled.png'. The only things that seemed different were a couple of
the color choices and how defined some of the features were. Overall, though, it
was interesting to see how K-Means CLustering works visually.
