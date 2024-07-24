# RetroTINK4K Profile Update Detection
A python script for comparing the profile folders of two RetroTINK4K update zip archives from [this page](https://retrotink-llc.github.io/firmware/4k-sdcards.html)

It uses `git` and `GitPython` in order to compare the two archives, so in order to run this script you are required to have the following:
- Python installed (developed on v3.11.2) [available here](https://www.python.org/downloads/)
- git installed [available here](https://git-scm.com/downloads)
- GitPython installed (run the command `pip install GitPython`, more info [here](https://gitpython.readthedocs.io/en/stable/))

Once these requirements are met, you can compare two archives by placing them in a folder with the script, opening a terminal in that folder and running the following command:

`python rt4k_profile_diff.py file1.zip file2.zip`

The script lazily assumed that the archives use the naming convention of `Rt4k_xxx_sdcard.zip`, where `xxx` is the version number. So for it to work properly, ensure the files are named in this way (at least the `Rt4k_xxx part!). So for example, comparing the 1.4.2 zip with 1.5.4 would look like this:

`python rt4k_profile_diff.py Rt4k_142_sdcard.zip  Rt4k_154_sdcardd.zip`

The results are currently displayed in a newly created file called `results.txt`