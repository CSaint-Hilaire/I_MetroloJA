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

Now, whether on the Jupyter notebook or on the HTML page, process the analysis data according to the following instructions : 
1. Select your input file. This is the zip file you imported :

![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_9.png) ![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_9bis.png)

2. Then press the big green button after selecting your zip file :

![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_10.png)

3. Select the type of analysis performed. Then press "OK!" :

![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_11.png) ![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_11bis.png)

4. Select all desired measurement types :

In this example, the resolution (FWHM), the ratio between measured and theoretical data and the signal to background ratio (SBR) are selected  

![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_12.png) ![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_12bis.png)

  a. First click on "Get Selected!"
  
  ![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_13.png)
  
  b. Then click on "Send!"
  
  ![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_13bis.png)
  
  c. Finally click on "Run!"

4. Indicate if you want to save your boxplot :

![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_14.png)

5. To complete, press on the orange "Show Boxplot!" button :

![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_15.png)

All boxplot are displayed on the HTML page or on the Jupyter notebook output, save (The folder and PDF file name is displayed At the very bottom of the HTML page or boxplots in the case of the Jupyter notebook) or not according to your selection.

![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_16.png)

If you have chosen to save the plots in PDF, then go back to the folder tab, which was opened previously, and go to the "RESULT" folder : 

![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_18.png) ![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_17.png) ![Jupyter Page](https://github.com/CSaint-Hilaire/MetroloJA_Binder/blob/main/images/usage_17bis.png)
