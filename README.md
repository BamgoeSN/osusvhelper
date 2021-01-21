# osu!taiko Timeline Helper
osu!taiko SV/Volume helper is a program aiming for helping you to apply gradual SV/volume changes easily to an osu!taiko beatmap.  
This program is built for learning GUIs with PyQt5 (and general programming), so any feedbacks and helps are appreciated.

I'm not sure if anyone will care this or if I can even achieve the most basic goal but I hope this'll go well lol

-------------

## Plans
### Functions
A user can initially set an interval of time to manage timelines from an .osu file. Then, they can add multiple non-overlapping intervals of timelines with gradual SV/volume changes. Standalone timelines will also be supported.  
Currently there is a plan for supporting BPM changes as well, but yet there's nothing decided of how to support those.

After the user finished inserting timeline intervals, the program will convert those into text of timelines which can be inserted into .osu file.  
This might be done by simply exporting a text file with timeline data so that the user can manually paste it into .osu's file, or insert it into .osu file automatically. Either of the options seem to be easy to implement.

There is an unrealistic (with my current level) plan of searching .osu files, supporting previews of SVs or more. These might be implemented if I be able to do so.

### Current status and the nearest goal
Currently backends are being built.  
After the basic is done, a simple console interactive application will be made for test.