# import-G-code
[![Gitter](https://badges.gitter.im/blender-for-science/community.svg)](https://gitter.im/blender-for-science/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

Imports G-code files into Blender 2.80+ as a collection of layers which can then be animated or exported.
![suzanne](suzanne.png)

## Installation
*   Download the latest release as a '.zip' file and head over to Blender 2.80+.  
*   Go to **Edit->Preferences->Add-on->Install** and point to the downloaded '.zip' file.
*   Make sure that the installed add-on is enabled. 
*   Once enabled, the add-on looks for Regex and Tqdm modules, it prompts for an installation if the required modules are missing. Kindly install them either via the prompt or manually.

## Usage
**Caution: It is a computationally expensive process.**
*Tested with Cura 4.6.2 and Blender 2.83.*

*   Run Blender 2.80+ from command line.
*   Specify **Layer height** and **Nozzle diameter** during file import.

![suzanne](suzanne.gif)

## References
*   [Cura](https://ultimaker.com/software/ultimaker-cura)
*   [G-code](https://reprap.org/wiki/G-code)