<h1>Morse Code Blink Detector</h1>

The Morse Code Blink Detector reads the video feed from your webcam and translates your blinks into Morse Code. The interpreter determines the length of your blink, and accordingly parses it into either a '.' (dit) or a '-' (dah). The string of dits and dahs is then ran through the Morse Code alphabet, and the interpretation is displayed on your screen.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<h3>Description</h3>

> This project is built upon OpenCV, the world-renowned and widely utilzied computer vision library and the <i>Python</i> programming language. The program begins by identifying the marking the face in the video feed, and proceeeds to calculate the <i><b>Eye Aspect Ratio (EAR)</b></i> to determine whether either eye is closed or not at any given moment. If a closed pair of eyes is detected, the program times the duration of the blink, and parses the corresponding Morse Code value.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<i>Developed by Farzan Mirshekari</i>
