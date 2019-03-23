This file includes a demonstration of example code for detecting and tracking the location of the marker provided
the script is written in python.
there is a video example of me using this program to track the object in the file.

To Start:
Simply open tracker.py and run it.

All imported libraries are imported using pycharm and I am usure if the computer can interpret the project properly otherwise.
libraries necessary include opencv-python, opencv-contrib-pyton, numpy

The script uses color detection to detect the marker. The image captured is first converted into hsv format and then thresholded for only specific red and blue values.
The thresholded values are saved into a mask and the function morphologyEx is applied to clean up noise and solidify forground objects
the a contour is then defined for the resulting image and only the largest contour about a certain size threshold is returned.
(to see this process more clearly, run MarkerDetect.py. All the layers of processing are shown)

In order to start tracking, the find marker functuion must return 100 consecutive bounding box spcecifications within tolerance.
a CSRT tracker is then applied to track the marker and the detection script pauses

the detection script is reactivated when the tracking fails.


Current pros:
handles motion blur
handles obstruction
handles false positives when detecting the marker to some degree
accurate report of tracking failure
images can be scaled down to be more computationally efficient and increase frame rate

Current issues:
detection not accurate under low lighting
possibility of false positive
detector currently only processes color instead shape
tracker cannot track multiple objects


possible imporvements:
adding shape recognizer to the detection process(ability to detect circles)
more accurate tuning of color thresholds
enable multi object tracking


Final comments:
the weakness of this solution is mainly due to the accuracy and oversimplicity of the object detector. Currently the detector is only capable of detecting colors
and grouping them together
with a better detector,(one that can also detect shapes and color patterns) the detection process would be come more efficient and more accurate and tracking
multiple objects would be much easier to do.