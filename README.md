# Remote-Sensing-NDVI-MSI-Estimation

This Remote Sensing application aims to analyze NDVI and MSI vegetation indexes of selected Landsat 8 images. NDVI shows the vitality of the plants, and the MSI shows the water content of the plants. By coloring these indexes, vegetation health analyses can be clearly observed. Output NDVI and MSI files are saved as geotiff files with coordinates hence, when used with a map layer (like OSM or GoogleEarth) it fits its real location on earth. 

## Technologies Used

- Rasterio Library
- PyCharm
- Python
- Matplotlib
- Numpy
- Tkinter

## Launch and Run

Source code of this program and can be compiled at any Python development environment. When its run, a Windows Application will be opened and ask for a directory. In this step you should select a directory that contains Landsat 8 imagery as Bands 4, 5 and 6 specifically. After the directory selected, you can select one of the two buttons in the main page as shown below.

![alt text](https://github.com/isilsukorkmaz/Remote-Sensing-NDVI-MSI-Estimation/blob/main/Application%20Window.png)

These buttons are programmed to calculate NDVI and MSI indexes and when either of buttons clicked, related index image will be appear in colored form with a colorbar. The output of NDVI button can be seen as below. Calculated NDVI values and coordinates can be seen at the upper right-hand-side of the window.


![alt text](https://github.com/isilsukorkmaz/Remote-Sensing-NDVI-MSI-Estimation/blob/main/NDVI%20Estimation%20Window.png)

After closing this window, the colored of calculated index will be saved under the selected directory under the created "output" directory with names NDVI.tif and MSI.tif.
