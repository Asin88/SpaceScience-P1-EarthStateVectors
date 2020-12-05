# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 01:56:09 2020

@author: AAKRITI
"""

# === Space Science Project 1 ===

# === Goal: Find Earth's current state vectors ===
"""
Description:
In this project, we shall compute the Earth’s position and velocity vector 
(so-called state vector) for today, midnight. Further, we compare the orbital 
speed of our home planet with the theoretical expectation.

We will be using a NASA toolkit SPICE (Spacecraft Planet Instrument C-matrix 
Events) in Python3 using the wrapper library spiceypy. SPICE is a huge toolkit 
that is being used by the Solar System science community to compute 
miscellaneous space mission-relevant information like:
-> Reference frames
-> Positions and velocities
-> Orientation/Pointing
-> Size/Shapes/Physical parameters
-> Time conversion

SPICE requires auxiliary data called kernels to work properly. They are stored 
at https://naif.jpl.nasa.gov/pub/naif/
These kernels are separated into different categories, like:
-> spk contain trajectory information of planetary bodies, spacecraft, etc.
-> pck contain physical parameters of bodies like the size or orientation
-> ik contain instrument-specific information that are e.g., mounted on a 
   spacecraft
-> ck contain information regarding the orientation of a spacecraft in space
-> fk contain reference frame information that is needed to calculate positions 
   in a less common reference system
-> lsk contain time information that is crucial to convert e.g., the UTC time into
   ephemeris time ET (a standard time format that is being used in space 
   science and astronomy)
    
For the current project, we have downloaded the relevant kernels and saved them
under data/external folder.
"""

# === We begin by first importing the spiceypy module. ===
#Import modules
import spiceypy
import datetime as dt
import math

# === Main Function ===
"""
We use the spkgeo function in SPICE to determine the state vector and the light 
time (travel time of the light between the Sun and our home planet). Positions 
are always given in km, velocities in km/s and times in seconds.

Abstract:
    Compute the geometric state (position and velocity) of a target body 
    relative to an observing body.

Inputs:
    targ: NAIF ID of Object that shall be pointed at
    et: The ET of the computation
    ref: The reference frame. Here, it is ECLIPJ2000 
    obs:  NAIF ID of the observer respectively the center of our state vector 
        computation

The target object is Earth (NAIF ID = 399) and the observer is the Sun 
(NAIF ID = 10). NAIF IDs are referenced from 
https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/naif_ids.html
The reference frame is the standard “Ecliptic Plane” of our planet set in the 
year 2000. 

Outputs:
    state: State of target. It contains the geometric position and velocity of 
           the target body, relative to the observing body, at epoch
           'et'. 'state' has six elements: the first three contain
           the target's position; the last three contain the
           target's velocity. These vectors are transformed into
           the specified reference frame.
 
   lt      Light Time. It is the one-way light time from the observing body 
           to the geometric position of the target body
           in seconds at the specified epoch. 
    
We shall first calculate the ET (ephemeric time).   
"""
def main():

# === Convert today's time at midnight from UTC to ephemeric time ET
    date_today_utc = dt.datetime.today()
    #Convert datetime to string, replacing time with midnight
    date_today_utc = date_today_utc.strftime('%Y-%m-%dT00:00:00')
    
    #Get time conversion information from a lsk kernel 'naif0012.tls'
    spiceypy.furnsh('E:\Data Science Projects\Space Science\SpaceScience-P1-EarthStateVectors\data\external\_kernels\lsk/naif0012.tls')
    #Convert UTC to ET using SPICE function 'utc2et'
    et_today = spiceypy.utc2et(date_today_utc)
    
# === Compute the position and velocity of the Earth with respect to the Sun ===

    #First load a spk kernel 'de432s.bsp' for positional information of planets. 
    """
    How to find the relevant kernel?
    At https://naif.jpl.nasa.gov/pub/naif/ we navigate to generic_kernels/spk/
    planets, since we are trying to find the trajectory of our planet. We 
    browse the aa_summaries.txt file. The last line of each summary shows the 
    time range covered in each kernel. The time period of de432s is suitable.
    """
    spiceypy.furnsh('E:\Data Science Projects\Space Science\SpaceScience-P1-EarthStateVectors\data\external/_kernels/spk/de432s.bsp')
    
    #Use spkgeo function to compute Earth state vectors   
    earth_state_wrt_sun, earth_sun_lt = spiceypy.spkgeo(targ=399, \
                                                        et=et_today, \
                                                        ref='ECLIPJ2000', \
                                                        obs=10)
    
    #Report position vector of Earth
    print(f"Position of Earth wrt Sun on {date_today_utc} is: \n \
          {earth_state_wrt_sun}", file=outfile)
    
    #Check whether computation is correct
    """
    We check the veracity of the computed position vectors by using the result 
    to compute the distance between Earth and Sun. If it is around 1 AU, then 
    the computation is satisfactory. ("around" 1AU because Earth's orbit is 
    elliptical, ot perfectly circular)
    """
    #Compute distance between Earth and Sun in km
    earth_sun_distance = math.sqrt(earth_state_wrt_sun[0]**2.0 \
                                 + earth_state_wrt_sun[1]**2.0 \
                                 + earth_state_wrt_sun[2]**2.0)
    #Convert km to AU
    earth_sun_distance_AU = spiceypy.convrt(earth_sun_distance, 'km', 'AU')
    #Report value
    print(f"Current distance between the Earth and the Sun in AU: \
          {earth_sun_distance_AU}", file=outfile)
    
    # === Orbital Speed of Earth ===
    #First we compute actual current orbital speed of Earth around Sun
    earth_orb_speed_wrt_sun = math.sqrt(earth_state_wrt_sun[3]**2.0 \
                                  + earth_state_wrt_sun[4]**2.0 \
                                  + earth_state_wrt_sun[5]**2.0)
    #Report current orbital speed of Earth
    print(f"Current orbital speed of the Earth around the Sun in km/s: \
      {earth_orb_speed_wrt_sun}", file=outfile)
    
    #Now we compute theoretical orbital speed of Earth around Sun
    """
    For this, we need the equation to determine the orbital speed. We assume
    that the Sun's mass is greater than the mass of the Earth and we assume 
    that our planet is moving on an almost circular orbit. The orbit velocity 
    $v_{\text{orb}}$ can be approximated with, where $G$ is the gravitational
    constant, $M$ is the mass of the Sun and $r$ is the distance between the 
    Earth and the Sun:
    \begin{align}
        v_{\text{orb}}\approx\sqrt{\frac{GM}{r}}
    \end{align}
    
    The G*M values for different objects are found in a pck file 'gm_de431.tpc'
    """
    #Load pck kernel for G*M value
    spiceypy.furnsh('E:\Data Science Projects\Space Science\SpaceScience-P1-EarthStateVectors\data\external/_kernels/pck/gm_de431.tpc')
    _, GM_SUN = spiceypy.bodvcd(bodyid=10, item='GM', maxn=1)
    #COmpute theoretical orbital speed
    v_orb_func = lambda gm, r: math.sqrt(gm/r)
    earth_orb_speed_wrt_sun_theory = v_orb_func(GM_SUN[0], earth_sun_distance)
    #Report theoretical value
    print(f"Theoretical orbital speed of the Earth around the Sun in km/s: \
      {earth_orb_speed_wrt_sun_theory}", file=outfile)
    
# === Run the script ===
if __name__ == "__main__":
    #Output file
    outfile = open(r"E:\Data Science Projects\Space Science\SpaceScience-P1-EarthStateVectors\reports\outfile.txt","a+")
    main()
    outfile.close()