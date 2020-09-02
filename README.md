# import-G-code
[![Blender](https://img.shields.io/badge/Blender-2.80%2B-orange)](https://www.blender.org/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b11bd990376a4995a9f9e5d830d20e24)](https://app.codacy.com/gh/blender-for-science/import-G-code?utm_source=github.com&utm_medium=referral&utm_content=blender-for-science/import-G-code&utm_campaign=Badge_Grade_Dashboard)
[![Release](https://img.shields.io/github/v/release/blender-for-science/import-G-code)](https://github.com/blender-for-science/import-G-code/releases)
[![License](https://img.shields.io/github/license/blender-for-science/import-G-code)](https://github.com/blender-for-science/import-G-code/blob/master/LICENSE.md)
[![Discord](https://img.shields.io/discord/750488363571740747?color=738ADB&label=Discord&style=flat-square)](https://discord.gg/K4jwkG)

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
