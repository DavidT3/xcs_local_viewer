# xcs_local_viewer
Simple viewer that uses the FCtrlA module to locally view XCS images.

## Requirements
* Python 3.5+
* RustyRegions from FCtrlA (email david.turner@sussex.ac.uk for this code)
* A user account on Apollo
* You must have exchanged RSA keys with Apollo (otherwise you're going to get a LOT of password requests).

## Installation
* Pull this repo
* Place RustyRegions.py inside the same folder

## Starting the viewer
* DON'T RUN THIS WITH LOTS OF SSH CONNECTIONS TO APOLLO OPEN, it probably won't work.
* Make a .csv with a list of all relevant ObsIDs in it (see obs_ids.csv for an example).
* Pass the name of the .csv as a command line argument to viewer.py, also pass a True or False argument to specify if you want the downloaded image/supporting files to be deleted after use.
* For instance:
```python
python viewer.py obs_ids.csv True
```
This will call the viewer and delete all downloaded files after viewer.py finishes.

## Using the viewer
* Click on a region to select it, the line should get thicker to indicate current selection.
* Click and drag to move the selected region; if you are unhappy with your new placement, press ctrl+z to undo.
* To resize the selected region, use the wasd keys, q and e change the angle.
* To make a new region, click the place on the screen you want it to appear, then press one of the buttons on the left side of the screen.
* Click save to create modified files (these will be saved to a local directory called {obs}_modded, in the obs_viewer_files directory.
* Close the viewer window to trigger the next observation (if you do this within ~10 seconds of opening the last one then you might have a crash, as the files may not have downloaded).

## Notes
* It isn't really necessary to delete all the downloaded files to save storage space, they aren't normally very large.
* Expect a several second delay before the first image appears, the script has to wait until the first two sets of images are downloaded.
* If the scaling on the images isn't to your taste, modify the stretch parameter in ```obs_obj.setup_image()```.
* When creating a new region, if you haven't clicked the place you want it to appear then it will be created in the middle of the image.

# PLEASE GIVE THOUGHTS AND REQUEST FEATURES/CHANGES, PREFERABLY USING GITHUB ISSUES.
