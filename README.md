# SpaceScience-P1-EarthStateVectors
My first venture into programming for space science!

Project Goal: Find Earth's current state vectors

Source: "Space Science with Python — Setup and first steps
A starting guide to became a Citizen Space Scientist — Part 1", Thomas Albin, 21 April 2020
https://towardsdatascience.com/space-science-with-python-setup-and-first-steps-1-8551334118f6
Github Link of source: https://github.com/ThomasAlbin/SpaceScienceTutorial/tree/master/part1

Description:

In this project, we shall compute the Earth’s position and velocity vector 
(state vector) for today, midnight. Further, we shall compare the orbital speed 
of our home planet with the theoretical expectation.

We will be using a NASA toolkit SPICE (Spacecraft Planet Instrument C-matrix 
Events) in Python3 using the wrapper library spiceypy. SPICE is a huge toolkit 
that is being used by the Solar System science community to compute 
miscellaneous space mission-relevant information like:
    
1. Reference frames
2. Positions and velocities
3. Orientation/Pointing
4. Size/Shapes/Physical parameters
5. Time conversion

SPICE requires auxiliary data called kernels to work properly. They are stored 
at https://naif.jpl.nasa.gov/pub/naif/
These kernels are separated into different categories, like:
    
1. spk contain trajectory information of planetary bodies, spacecraft, etc.
2. pck contain physical parameters of bodies like the size or orientation
3. ik contain instrument-specific information that are e.g., mounted on a 
   spacecraft
4. ck contain information regarding the orientation of a spacecraft in space
5. fk contain reference frame information that is needed to calculate positions 
   in a less common reference system
6. lsk contain time information that is crucial to convert e.g., the UTC time into
   ephemeris time ET (a standard time format that is being used in space 
   science and astronomy)
    
For the current project, we have downloaded the relevant kernels and saved them
under data/external folder.