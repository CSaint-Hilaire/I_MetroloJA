<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/MetroloJA_logo_black.png">
 <img alt="light-logo" src="https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/MetroloJA_logo_white.png">
</picture>

A guide for time-tracking metrology analyses of light microscopes, after using the ImageJ MetroloJ_QC plugin. :tada:

## MetroloJ_QC plugin
MetroloJ_QC is a plugin whose goal is to enable automation of quality control tests regularly implemented within a light microscopy facility. This plugin, used from the image analysis software **ImageJ**, was developed by Fabrice Cordelières and Cedrick Matthews ([GitHub Pages](https://github.com/MontpellierRessourcesImagerie/MetroloJ_QC)). After running MetroloJ_QC, an output folder is created, named **Processed**. &#x1F4D7; 

## MetroloJA description
MetroloJA is a Jupyter notebook that allows a follow-up over time of these quality control tests of light microscopes of a facility by proceeding as follows: 
 > - [x] Extract analysis data from the **Processed** folder :+1:
 > - [x] Represent this data as a **boxplot** with statistical tests, for follow-up over time with dates :tada:

## Getting Started
### Installation
The only thing to do is to click on this [link](https://mybinder.org/v2/gh/CSaint-Hilaire/MetroloJA_Binder/HEAD?urlpath=tree%2Fmetroloj_analyze.ipynb). 
The notebook opens in an executable environment from [Binder](https://mybinder.readthedocs.io/en/latest/), and it is converted into a standalone application using [Voilà](https://voila.readthedocs.io/en/stable/using.html). The process can take few minutes, be patient ! :laughing:


### Usage
After loading, this Jupyter notebook appears :

![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_1.png) 

To access the space where all folders and files are located, go to the "File" tab and click on "Open..." :
![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_2.png) ![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_3.png) ![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_3bis.png)

And this new tab opens :
![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_4.png)

You will be able to upload your analysis folder from MetroloJ_QC :
 * Click on the "Upload" button and select the folder that must first be compressed in .zip format :
 
 ![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_5.png)
 
 * Your zip file appears in your environment. Click on the blue "Upload" button :
 
 ![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_6.png)
 
Here, your analysis data is available. You can then go back to the Jupyter notebook and run the code for analysis, or open an HTML page so that only the code outputs are visible and not the code itself.

To do this, always in the Jupyter notebook, press the "voilà" button : 
![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_7.png)

A new tab opens. This is an HTML page with only the code outputs :
![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_8.png)

Click on the green button and make following selections : 
1. Select the type of analyze

![Voilà Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_2.png) ![Voilà Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_2bis.png)

2. Select the input folder which contains MetroloJ_QC's **Processed** folder for each acquisition date

![Voilà Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_3.png)

3. Select all desired measurement types

In this example, the resolution (FWHM), the fitting between raw data and a Gaussian (R2) and the signal to background ratio (SBR) are selected  

![Voilà Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_4.png) ![Voilà Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_5.png)

4. Indicate if you want to save your boxplot

![Voilà Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_6.png)

5. If **yes**, select your output folder 

![Voilà Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_7.png)

At the end, all boxplot are displayed on the web page, save or not according to your selection.

![Voilà Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_8.png)
