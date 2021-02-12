import rasterio

import rasterio._shim
import rasterio.crs
import rasterio.control
import rasterio.sample
import rasterio.vrt
import rasterio._features
from rasterio import plot

import os
import tkinter as tk
import cv2
import numpy as np

import matplotlib.pyplot as plt
import re
import glob

from matplotlib import colors
from matplotlib.colors import TwoSlopeNorm
from tkinter import filedialog


def NDVI():

    data_path = file_path
    bands_grep = re.compile(".*_(B4|B5)\.(tif|TIF)")

    file_list = glob.glob(data_path + '\*.TIF')
    print(file_list)

    # Filter and keep only useful files (bands 4 and 5 to compute NDVI)
    bands = filter(lambda x: bands_grep.search(x), file_list)
    bands = [s for s in bands]

    #Open and read files
    with rasterio.open(bands[0]) as src:
        b4 = src.read(1).astype('float64')

    with rasterio.open(bands[1]) as src:
        b5 = src.read(1).astype('float64')


    # Allow division by zero
    np.seterr(divide='ignore', invalid='ignore')

    # Calculate NDVI
    ndvi = (b5.astype(float) - b4.astype(float)) / (b4 + b5)

    #No data values
    ndvi = np.where(
        (b5.astype(float) - b4.astype(float)) / (b4 + b5) == 0,
        0,
        (b5.astype(float) - b4.astype(float)) / (b4 + b5))

    # Define spatial characteristics of output object (basically they are analog to the input)
    kwargs = src.meta

    # Update kwargs (change in data type)
    kwargs.update(
        dtype=rasterio.float64,
        count=1)

    with rasterio.open(output_path + '/NDVI.tif', 'w', **kwargs) as dst:
        dst.write_band(1, ndvi.astype(rasterio.float64))

    src = rasterio.open(output_path + '/NDVI.tif')

    # Render with colormap and colorbar
    z = np.linspace(-1, 1, 50 * 50)

    norm = TwoSlopeNorm(vmin=z.min(), vcenter=0, vmax=z.max())
    pc = plt.imshow(src.read(1).astype('float64'), norm=norm, cmap='RdBu_r')
    plt.colorbar(pc)

    plt.show()

    # geotiff kaydetme
    naip_data_path = output_path + '/NDVI.tif'

    with rasterio.open(naip_data_path) as src:
        naip_data = src.read()
        naip_meta = src.profile

    naip_transform = naip_meta["transform"]
    naip_crs = naip_meta["crs"]

    w, h = ndvi.shape

    customized_cmap = {}
    a = float(255 / 2)

    print(a)
    print(customized_cmap)

    for s in range(-1, 2):
        s = s * (255 / 2)
        print(s)

    a = 0
    b = 255
    for s in range(0, 256):
        s_color = (a, 0, b, 0)
        customized_cmap[s] = s_color
        a += 1
        b -= 1

    print(customized_cmap)

    ndvi = cv2.normalize(ndvi, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    with rasterio.open(
            (output_path + '/NDVI.tif'), 'w',
            driver='GTiff', width=w, height=h, count=1,
            dtype=rasterio.uint8, crs=naip_crs, transform=naip_transform) as dst:
        dst.write(ndvi.astype(rasterio.uint8), indexes=1)
        dst.write_colormap(1, customized_cmap)


def MSI():

    data_path = file_path
    bands_grep = re.compile(".*_(B5|B6)\.(tif|TIF)")

    file_list = glob.glob(data_path + '\*.TIF')

    # Filter and keep only useful files (bands 4 and 5 to compute NDVI)
    bands = filter(lambda x: bands_grep.search(x), file_list)
    bands = [s for s in bands]

    with rasterio.open(bands[0]) as src:
        b5 = src.read(1).astype('float64')

    with rasterio.open(bands[1]) as src:
        b6 = src.read(1).astype('float64')

    # Allow division by zero
    np.seterr(divide='ignore', invalid='ignore')

    msi_temp = np.where(
        b5 == 0,
        0,
        b6 / b5)

    max = msi_temp.astype(float).max()

    msi = np.where(
        b6 / b5 >= max,
        max,
        b6 / b5)

    # Define spatial characteristics of output object (basically they are analog to the input)
    kwargs = src.meta

    # Update kwargs (change in data type)
    kwargs.update(
        dtype=rasterio.float64,
        count=1)

    with rasterio.open(output_path + '/MSI.tif', 'w', **kwargs) as dst:
        dst.write_band(1, msi.astype(rasterio.float64))

    src = rasterio.open(output_path + '/MSI.tif')

    # matplotlib ile görsel ve colorbar ayrı ayrı
    z = np.linspace(0, max, 50 * 50)

    norm = TwoSlopeNorm(vmin=z.min(), vcenter=max / 2, vmax=z.max())
    pc = plt.imshow(src.read(1).astype('float64'), norm=norm, cmap='RdBu_r')
    plt.colorbar(pc)

    plt.show()

    # geotiff kaydetme
    naip_data_path = output_path + '/MSI.tif'

    with rasterio.open(naip_data_path) as src:
        naip_data = src.read()
        naip_meta = src.profile

    naip_transform = naip_meta["transform"]
    naip_crs = naip_meta["crs"]

    w, h = msi.shape

    customized_cmap = {}
    a = float(255 / (max + 2))

    for s in range(0, int(max + 2)):
        s_color = (0 + a, 0, 255 - a, 0)
        customized_cmap[s] = s_color
        s += 1
        a += float(255 / (max + 2))

    with rasterio.open(
            output_path + '/MSI.tif', 'w',
            driver='GTiff', width=w, height=h, count=1,
            dtype=rasterio.uint8, crs=naip_crs, transform=naip_transform) as dst:
        dst.write(msi.astype(rasterio.uint8), indexes=1)
        dst.write_colormap(1, customized_cmap)


top = tk.Tk()
top.configure(bg='Plum')
top.geometry("600x600")

greeting = tk.Label(text="WELCOME!",
                    fg="black",
                    bg="Plum",
                    font=("Courier", 30),
                    width=100,
                    height=30)

greeting.pack(side='top')
greeting.place(relx=0.5,
               rely=0.1,
               anchor='center')



headline = tk.Label(text="Estimate NDVI \n (Normalized Difference Vegetation Index) \n and \n MSI (Moisture Stress Index) of Land Cover \n by Using Landsat-8 Images",
                        fg="black",
                        bg="Plum",
                        font=("Courier", 15),
                        width=100,
                        height=5)

headline.pack(side='top')
headline.place(relx=0.5,
                   rely=0.4,
                   anchor='center')


path_warning = tk.Label(text="Colored version of estimated .tiff file\n" + " will be saved after Matplotlib window is closed.",
                        fg="black",
                        bg="Plum",
                        font=("Courier", 12),
                        width=100,
                        height=5)

path_warning.pack(side='top')
path_warning.place(relx=0.5,
                   rely=0.8,
                   anchor='center')



#path_button = tk.Button(top, text="Choose Directory", font="Courier", bg='MediumOrchid', command=get_directory)

ndvi_button = tk.Button(top, text="Estimate NDVI", font="Courier", bg='MediumOrchid', command=NDVI)
msi_button = tk.Button(top, text="Estimate MSI", font="Courier", bg='MediumOrchid', command=MSI)

#path_button.pack(side='top')
#path_button.place(relx=0.5, rely=0.4, anchor='center')

ndvi_button.pack(side='top')
ndvi_button.place(x=100, y=400)

msi_button.pack(side='bottom')
msi_button.place(x=350, y=400)


file_path = filedialog.askdirectory()
print(file_path)

output_path = file_path + '/Output'

try:
    os.mkdir(output_path)
except FileExistsError:
    pass


top.mainloop()