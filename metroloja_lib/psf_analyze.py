import os, glob, pathlib, time, datetime, shutil
import plotly.graph_objects as go
import plotly.express as px
import ipywidgets as widgets
from ipyfilechooser import FileChooser
import pandas as pd
from pathlib import Path

from alive_progress import alive_bar
from tkinter import filedialog as fd
from PyPDF2 import PdfFileMerger
from functools import reduce
from scipy import stats



def select_folder(folder_selected):
    date_file = os.listdir(folder_selected)
    for i in date_file:
        if i.startswith('.'):
            date_file.remove(i)

    for i in date_file:
        if i == 'pdf_result':
            date_file.remove(i)

    f_folder = []
    for fl in date_file:
        f_folder.append(os.path.join(folder_selected, fl))

    all_image_name = []

    for k in range(len(f_folder)):
        l = []
        for path in glob.glob(f'{f_folder[k]}/*/**/', recursive=True):
            l.append(path)
        path_name = [l[i] for i in range(0,len(l),2)]

        img_name = []
        for j in path_name:
            TempPath = pathlib.PurePath(j)
            img_name.append(TempPath.name)

        del img_name[0]
        all_image_name.append(img_name)



    #print('Images name :')
    for indx in range(len(all_image_name)):
        allimages = all_image_name[indx]
        for i in range(len(allimages)-1):
            n = os.path.normpath(allimages[i])
            path_split = n.split(os.sep)
            f_n = path_split[-1]
            if f_n.startswith(".") == True:
                allimages.remove(allimages[i])
        for rm in allimages:
            if rm == 'Processed':
                allimages.remove(rm)
    len_tot_image = reduce(lambda count, l: count + len(l), all_image_name, 0)


    lf_name = []
    for indx in range(len(all_image_name)):
        #print(f'Date {indx + 1}')
        allimages = all_image_name[indx]
        for j in allimages:
            #print(f'   {j}')
            lf_name.append(j)
    
    return(folder_selected, date_file, all_image_name, lf_name, len_tot_image)




def processed_path(folder_selected, date_file):
    #print('Path of processed folder : \n')
    all_processed_path = []
    for j in date_file:
        dt_path = os.path.join(folder_selected, j)
        processed_path = os.path.join(dt_path,'Processed')

        for i in os.listdir(processed_path):
            try:
                if i.startswith('.') == False:
                    processed_path2 = os.path.join(processed_path,i)
                    #print(processed_path2)
                    all_processed_path.append(processed_path2)
                    
            except:
                print('No metroloJ_QC result')
    return(all_processed_path)



def convert_to_df(all_processed_path, date_file, all_image_name, lf_name, len_tot_image, folder_selected):
    with alive_bar(len_tot_image, force_tty = True) as bar:
        dtm = pd.DataFrame()
        dtm_sbr = pd.DataFrame()
        idx = 0
        for process in all_processed_path:
            # r=root, d=directories, f = files
            for r, d, f in os.walk(process):
                for file in f:
                    for dt in range(len(all_image_name)):
                        TempDate = all_image_name[dt]
                        for i in range(len(TempDate)):
                            grp = TempDate[i]
                            path_split = process.split(os.sep)

                            filename = grp
                            initTempDate = path_split[-3]
                            date = datetime.datetime.strptime(initTempDate, '%Y%m%d').date()
                            microscope = f'{path_split[-6]} : {path_split[-5]}'
                            for fn in lf_name:
                                if fn in grp:
                                    fn2 = fn.replace(' ','')
                                    if file.endswith("_summary.xls") and file.startswith(fn2):
                                        f_path = os.path.join(r, file)
                                        #fullpath = os.path.abspath(f_path)
                                        data = pd.read_csv(f_path, delimiter = "\t", index_col = False, header= 0)
                                        data = data.iloc[:, :-1] # Drop the last column

                                        # Find "Channel" indexe(s)
                                        q = "Dimension"
                                        c = data.columns[0]

                                        irow = data.query(f'"{q}" in {c}').index


                                        # Split dataframe and take Dimension's part
                                        last_check = 0
                                        dfs = []
                                        for ind in [irow[0], len(data)]:
                                            dfs.append(data.loc[last_check:ind-1])
                                            last_check = ind

                                        df_dimension = dfs[1]

                                        # Take SBR part
                                        df_dimension_SBR = dfs[0]
                                        #Select data column
                                        sbr = df_dimension_SBR.iloc[:,1]

                                        # Reindex column name
                                        df_dimension.columns = df_dimension.iloc[0]
                                        df_dimension = df_dimension.reindex(df_dimension.index.drop(1)).reset_index(drop=True)
                                        df_dimension.columns.name = None

                                        # Reindex row name
                                        df_dimension = df_dimension.set_index('Dimension')


                                        # Create XYZ dataframe
                                        x_FWHM = df_dimension.loc["Measured FWHM (µm)","X"]
                                        y_FWHM = df_dimension.loc["Measured FWHM (µm)","Y"]
                                        z_FWHM = df_dimension.loc["Measured FWHM (µm)","Z"]


                                        x_R2 = df_dimension.loc["Fit Goodness","X"]
                                        y_R2 = df_dimension.loc["Fit Goodness","Y"]
                                        z_R2 = df_dimension.loc["Fit Goodness","Z"]

                                        x_ratio = df_dimension.loc["Mes./theory ratio","X"]
                                        y_ratio = df_dimension.loc["Mes./theory ratio","Y"]
                                        z_ratio = df_dimension.loc["Mes./theory ratio","Z"]


                                        wavelenght = sbr.name[14:22]



                                        image_path = os.path.join(folder_selected, str(date), filename)
                                        TempList = pd.DataFrame({'Date':[date], 'Image Path':[image_path], "Microscope":[microscope], "Wavelength":[wavelenght], "Fit (R2)":[x_R2], 'Resolution (µm) : FWHM':[x_FWHM], 'Mes./theory resolution ratio (µm)':[x_ratio], 'Axe':"X"})
                                        dtm = pd.concat([dtm,TempList])

                                        TempList = pd.DataFrame({'Date':[date], 'Image Path':[image_path], "Microscope":[microscope], "Wavelength":[wavelenght], "Fit (R2)":[y_R2], 'Resolution (µm) : FWHM':[y_FWHM], 'Mes./theory resolution ratio (µm)':[y_ratio], 'Axe':"Y"})
                                        dtm = pd.concat([dtm,TempList])

                                        TempList = pd.DataFrame({'Date':[date], 'Image Path':[image_path], "Microscope":[microscope], "Wavelength":[wavelenght], "Fit (R2)":[z_R2], 'Resolution (µm) : FWHM':[z_FWHM], 'Mes./theory resolution ratio (µm)':[z_ratio], 'Axe':"Z"})
                                        dtm = pd.concat([dtm,TempList])


                                        #Create SBR dataframe
                                        TempList = pd.DataFrame({'Date':[date], 'Image Path':[image_path], "Microscope":[microscope], "Wavelength":[wavelenght], 'Sig/Backgnd ratio':[sbr[0]]})
                                        dtm_sbr = pd.concat([dtm_sbr,TempList])

                                        time.sleep(.005)
                                        bar()

    dtm.reset_index(drop=True, inplace=True)
    dtm_sbr.reset_index(drop=True, inplace=True)
    df_XYZ = dtm
    df_SBR = dtm_sbr
    
    return(df_XYZ, df_SBR)

    

    
def XYZ_stats(df_XYZ):
    df_XYZ = df_XYZ.explode('Fit (R2)')
    df_XYZ['Fit (R2)'] = df_XYZ['Fit (R2)'].astype('float')

    median_df_R2 = df_XYZ.groupby(['Date', 'Microscope', 'Wavelength', 'Axe'])['Fit (R2)'].median().to_frame('R2 median').reset_index()
    mean_df_R2 = df_XYZ.groupby(['Date', 'Microscope', 'Wavelength', 'Axe'])['Fit (R2)'].mean().to_frame('R2 mean').reset_index()
    std_df_R2 = df_XYZ.groupby(['Date', 'Microscope', 'Wavelength', 'Axe'])['Fit (R2)'].std().to_frame('R2 std').reset_index()
    max_df_R2 = df_XYZ.groupby(['Date', 'Microscope', 'Wavelength', 'Axe'])['Fit (R2)'].max().to_frame('R2 max').reset_index()



    df_XYZ = df_XYZ.explode('Resolution (µm) : FWHM')
    df_XYZ['Resolution (µm) : FWHM'] = df_XYZ['Resolution (µm) : FWHM'].astype('float')

    median_df_FWHM = df_XYZ.groupby(['Date', 'Microscope', 'Wavelength', 'Axe'])['Resolution (µm) : FWHM'].median().to_frame('FWHM median').reset_index()
    mean_df_FWHM = df_XYZ.groupby(['Date', 'Microscope', 'Wavelength', 'Axe'])['Resolution (µm) : FWHM'].mean().to_frame('FWHM mean').reset_index()
    std_df_FWHM = df_XYZ.groupby(['Date', 'Microscope', 'Wavelength', 'Axe'])['Resolution (µm) : FWHM'].std().to_frame('FWHM std').reset_index()
    max_df_FWHM = df_XYZ.groupby(['Date', 'Microscope', 'Wavelength', 'Axe'])['Resolution (µm) : FWHM'].max().to_frame('FWHM max').reset_index()



    df_XYZ = df_XYZ.explode('Mes./theory resolution ratio (µm)')
    df_XYZ['Mes./theory resolution ratio (µm)'] = df_XYZ['Mes./theory resolution ratio (µm)'].astype('float')

    median_df_ratio = df_XYZ.groupby(['Date', 'Microscope', 'Wavelength', 'Axe'])['Mes./theory resolution ratio (µm)'].median().to_frame('Mes./theory resolution ratio median').reset_index()
    mean_df_ratio = df_XYZ.groupby(['Date', 'Microscope', 'Wavelength', 'Axe'])['Mes./theory resolution ratio (µm)'].mean().to_frame('Mes./theory resolution ratio mean').reset_index()
    std_df_ratio = df_XYZ.groupby(['Date', 'Microscope', 'Wavelength', 'Axe'])['Mes./theory resolution ratio (µm)'].std().to_frame('Mes./theory resolution ratio std').reset_index()
    max_df_ratio = df_XYZ.groupby(['Date', 'Microscope', 'Wavelength', 'Axe'])['Mes./theory resolution ratio (µm)'].max().to_frame('Mes./theory resolution ratio max').reset_index()



    allDFstat = [median_df_R2, mean_df_R2, std_df_R2, max_df_R2, median_df_FWHM, mean_df_FWHM, std_df_FWHM, max_df_FWHM, median_df_ratio, mean_df_ratio, std_df_ratio, max_df_ratio]
    dfXYZ_MedStd = reduce(lambda  left,right: pd.merge(left,right,on=['Date', 'Microscope', 'Wavelength', 'Axe'], how='outer'), allDFstat)



    return(dfXYZ_MedStd)




def SBR_stats(df_SBR):
    df_SBR = df_SBR.explode('Sig/Backgnd ratio')
    df_SBR['Sig/Backgnd ratio'] = df_SBR['Sig/Backgnd ratio'].astype('float')

    median_df_SBR = df_SBR.groupby(['Date', 'Microscope', 'Wavelength'])['Sig/Backgnd ratio'].median().to_frame('Median').reset_index()
    mean_df_SBR = df_SBR.groupby(['Date', 'Microscope', 'Wavelength'])['Sig/Backgnd ratio'].mean().to_frame('Mean').reset_index()
    std_df_SBR  = df_SBR.groupby(['Date', 'Microscope', 'Wavelength'])['Sig/Backgnd ratio'].std().to_frame('Std').reset_index()
    eff_df_SBR  = df_SBR.groupby(['Date', 'Microscope', 'Wavelength']).size().reset_index(name='n')
    max_df_SBR  = df_SBR.groupby(['Date', 'Microscope', 'Wavelength'])['Sig/Backgnd ratio'].max().to_frame('Max').reset_index()


    allSBRstat = [median_df_SBR, mean_df_SBR, std_df_SBR, eff_df_SBR, max_df_SBR]
    df_MedStd_SBR = reduce(lambda  left,right: pd.merge(left,right,on=['Date', 'Microscope', 'Wavelength'], how='outer'), allSBRstat)

    leg_dict = {}
    for i in range(len(df_MedStd_SBR)):
        t = df_MedStd_SBR['Date'].iloc[i]
        leg_dict[str(t)] = str(t) + ' (n = ' + str(df_MedStd_SBR['n'].iloc[i]) + ')'

    return(df_MedStd_SBR, leg_dict)
    




def create_XYZ_box(df_XYZ, param, table_column_param, med_column_param, im_path,
                   result, ttest_table_column, df_MedStd_SBR, leg_dict, sys_name, 
                   dfX_MedStd, dfY_MedStd, dfZ_MedStd):
    date1 = df_MedStd_SBR["Date"].tolist()
    date2 = date1.copy()
    date2[0] = "first date"
    
    df_XYZ = df_XYZ.explode(table_column_param)
    df_XYZ[table_column_param] = df_XYZ[table_column_param].astype('float')
    

    fig = px.box(df_XYZ, x = "Date", y = table_column_param, color = "Date", category_orders={"Date" : date1},
                 facet_row="Axe", title = f"{sys_name[0]}           {param} Box plot           PICT-BDD           (Update : {datetime.datetime.today().strftime('%Y-%m-%d')})<br><sub><b>Statistical T-Tests are carried out between a date and the date immediately preceding it</b></sub>", points="outliers", height=1000, width=900).update_yaxes(matches=None)

    fig.update_layout(showlegend=True)
    fig.update_layout(title_x=0.5)
    
    
    
    fig.for_each_trace(lambda t: t.update(name = leg_dict[t.name],
                                          legendgroup = leg_dict[t.name],
                                          hovertemplate = t.hovertemplate.replace(t.name, leg_dict[t.name])
                                         )
                      )



    fig.add_trace(
        go.Scatter(x=dfX_MedStd["Date"].tolist(), y=dfX_MedStd[med_column_param].tolist(), showlegend=False, mode='lines+markers', line=dict(color="#000000")), row=3, col=1
    )
    fig.add_trace(
        go.Scatter(x=dfY_MedStd["Date"].tolist(), y=dfY_MedStd[med_column_param].tolist(), showlegend=False, mode='lines+markers', line=dict(color="#000000")), row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=dfZ_MedStd["Date"].tolist(), y=dfZ_MedStd[med_column_param].tolist(), showlegend=False, mode='lines+markers', line=dict(color="#000000")), row=1, col=1
    )



    dfXY = df_XYZ[(df_XYZ["Axe"] == "X") | (df_XYZ["Axe"] == "Y")]

    max_df_FWHM = dfXY.groupby(['Date', 'Microscope', 'Wavelength', 'Axe'])[table_column_param].max().to_frame('max').reset_index()
    min_df_FWHM = dfXY.groupby(['Date', 'Microscope', 'Wavelength', 'Axe'])[table_column_param].min().to_frame('min').reset_index()

    merge_MinMax_FWHM = pd.merge(min_df_FWHM, max_df_FWHM, how='left', on=['Date', 'Microscope', 'Wavelength', 'Axe'])


    # Select XY range for boxplot
    range_min_FWHM = merge_MinMax_FWHM["min"].min() - 0.02
    range_max_FWHM = merge_MinMax_FWHM["max"].max() + 0.02


    fig.update_yaxes(range=[range_min_FWHM, range_max_FWHM], row=2)
    fig.update_yaxes(range=[range_min_FWHM, range_max_FWHM], row=3)
    
    
    
    

    dfX = df_XYZ[df_XYZ["Axe"] == "X"]
    dfY = df_XYZ[df_XYZ["Axe"] == "Y"]
    dfZ = df_XYZ[df_XYZ["Axe"] == "Z"]
    

        

    for i in range(len(date1)-1):
        dfX = dfX.explode(table_column_param)
        dfX[table_column_param] = dfX[table_column_param].astype('float')
        
        TempDF_X1 = dfX[dfX["Date"] == date1[i]]
        TempDF_X2 = dfX[dfX["Date"] == date2[i + 1]]

        X = date2[i + 1]
        Yx = dfX_MedStd[dfX_MedStd["Date"]==X]
        Yx = Yx[ttest_table_column]
        tX, pX = stats.ttest_ind(TempDF_X1[table_column_param], TempDF_X2[table_column_param], equal_var=False)
        
        if pX >= 0.05:
            symbolX = '<sup><sup><b>ns</b></sup></sup>'
            sz = 30
        elif pX >= 0.01: 
            symbolX = '<sup><b>*</b></sup>'
            sz = 20
        elif pX >= 0.001:
            symbolX = '<sup><b>**</b></sup>'
            sz = 20
        else:
            symbolX = '<sup><b>***</b></sup>'
            sz = 20
        fig.add_annotation(dict(font=dict(size=sz), 
                                x=X, y=float(Yx),
                                text=symbolX,
                                showarrow=False,
                                arrowhead=1,
                                xref='x1',
                                yref='y3'))



        dfY = dfY.explode(table_column_param)
        dfY[table_column_param] = dfY[table_column_param].astype('float')
        
        TempDF_Y1 = dfY[dfY["Date"] == date1[i]]
        TempDF_Y2 = dfY[dfY["Date"] == date2[i + 1]]

        Yy = dfY_MedStd[dfY_MedStd["Date"]==X]
        Yy = Yy[ttest_table_column]
        tY, pY = stats.ttest_ind(TempDF_Y1[table_column_param], TempDF_Y2[table_column_param], equal_var=False)
        
        if pY >= 0.05:
            symbolY = '<sup><sup><b>ns</b></sup></sup>'
            sz = 30
        elif pY >= 0.01: 
            symbolY = '<sup><b>*</b></sup>'
            sz = 20
        elif pY >= 0.001:
            symbolY = '<sup><b>**</b></sup>'
            sz = 20
        else:
            symbolY = '<sup><b>***</b></sup>'
            sz = 20
        
        fig.add_annotation(dict(font=dict(size=sz), 
                                x=X, y=float(Yy),
                                text=symbolY,
                                showarrow=False,
                                arrowhead=1,
                                xref='x1',
                                yref='y2'))



        dfZ = dfZ.explode(table_column_param)
        dfZ[table_column_param] = dfZ[table_column_param].astype('float')
        
        TempDF_Z1 = dfZ[dfZ["Date"] == date1[i]]
        TempDF_Z2 = dfZ[dfZ["Date"] == date2[i + 1]]

        Yz = dfZ_MedStd[dfZ_MedStd["Date"]==X]
        Yz = Yz[ttest_table_column]
        tZ, pZ = stats.ttest_ind(TempDF_Z1[table_column_param], TempDF_Z2[table_column_param], equal_var=False)
        
        if pZ >= 0.05:
            symbolZ = '<sup><sup><b>ns</b></sup></sup>'
            sz = 30
        elif pZ >= 0.01: 
            symbolZ = '<sup><b>*</b></sup>'
            sz = 20
        elif pZ >= 0.001:
            symbolZ = '<sup><b>**</b></sup>'
            sz = 20
        else:
            symbolZ = '<sup><b>***</b></sup>'
            sz = 20
        
        
        fig.add_annotation(dict(font=dict(size=sz), 
                                x=X, y=float(Yz),
                                text=symbolZ,
                                showarrow=False,
                                arrowhead=1,
                                xref='x1',
                                yref='y1'))
    
    

    fig.show()
    
    if result == 'Yes':
        global XYZpdf_name
        param = param.replace(" ", "_")
        param = param.replace(".", "")
        param = param.replace("/", "_")
        XYZpdf_name = f'{param}_boxplot.pdf'
        XYZpdf_path = os.path.join(im_path, XYZpdf_name)
        fig.write_image(XYZpdf_path)
    




def create_SBR_box(df_SBR, result, im_path, df_MedStd_SBR, leg_dict, sys_name):
    date1 = df_MedStd_SBR["Date"].tolist()
    date2 = date1.copy()
    date2[0] = "first date"
    
    df_SBR = df_SBR.explode("Sig/Backgnd ratio")
    df_SBR["Sig/Backgnd ratio"] = df_SBR["Sig/Backgnd ratio"].astype('float')
    
    
    fig = px.box(df_SBR, x = "Date", y = "Sig/Backgnd ratio", color = "Date", category_orders={"Date" : date1},
                 title = f"{sys_name[0]}           Sig/Backgnd ratio Box plot           PICT-BDD           (Update : {datetime.datetime.today().strftime('%Y-%m-%d')})<br><sub><b>Statistical T-Tests are carried out between a date and the date immediately preceding it</b>", points="outliers", height=1000, width=900).update_yaxes(matches=None)

    fig.update_layout(showlegend=True)
    fig.for_each_trace(lambda t: t.update(name = leg_dict[t.name],
                                          legendgroup = leg_dict[t.name],
                                          hovertemplate = t.hovertemplate.replace(t.name, leg_dict[t.name])
                                         )
                      )
    
    fig.add_trace(
        go.Scatter(x=df_MedStd_SBR["Date"].tolist(), y=df_MedStd_SBR["Median"].tolist(), showlegend=False, mode='lines+markers', line=dict(color="#000000"))
    )
    fig.update_layout(title_x=0.5)
    
    


    for i in range(len(date1)-1):
        
        TempDF_SBR1 = df_SBR[df_SBR["Date"] == date1[i]]
        TempDF_SBR2 = df_SBR[df_SBR["Date"] == date2[i + 1]]

        X = date2[i + 1]
        Y = df_MedStd_SBR[df_MedStd_SBR["Date"]==X]
        Y = Y["Max"]
        t, p = stats.ttest_ind(TempDF_SBR1["Sig/Backgnd ratio"], TempDF_SBR2["Sig/Backgnd ratio"], equal_var=False)
        
        if p >= 0.05:
            symbol = '<sup><sup><b>ns</b></sup></sup>'
            sz = 30
        elif p >= 0.01: 
            symbol = '<sup><b>*</b></sup>'
            sz = 20
        elif p >= 0.001:
            symbol = '<sup><b>**</b></sup>'
            sz = 20
        else:
            symbol = '<sup><b>***</b></sup>'
            sz = 20
        fig.add_annotation(dict(font=dict(size=sz), 
                                x=X, y=float(Y),
                                text=symbol,
                                showarrow=False,
                                arrowhead=1))

    
    fig.show()
    
    if result == 'Yes':
        global SBRpdf_name
        SBRpdf_name = f'SBR_boxplot.pdf'
        SBRpdf_path = os.path.join(im_path, SBRpdf_name)
        fig.write_image(SBRpdf_path)

        


def select_param(button_boxplot, button_final_param):
    print('\n')
    text2 = '2. Check all the measurements you want to plot'
    Lab2 = widgets.HTML(value = f"<b><font color='green', size='5'>{text2}</b>")
    box_layout = widgets.Layout(display='flex', flex_flow='column',
                                align_items='center')
    
    Lab_box2 =widgets.HBox([Lab2],layout=box_layout)
    display(Lab_box2)
    
    data = ["FWHM", "Fit (R2)", "Mes./theory resolution ratio", "SBR"]
    checkboxes = [widgets.Checkbox(value=False, description=label) for label in data]

    button_param_selected = widgets.Button(description="Get Selected!",  
                                           style=dict(font_weight='bold', button_color = 'GreenYellow'))
    box_layout2 = widgets.Layout(display='flex', flex_flow='row', justify_content='center', align_items='baseline')
    get_lab = widgets.Label('1st : ')
    output1 = widgets.Output()
    
    button_param_selected.layout.visibility = 'hidden'


    def return_param(b):
        with output1:
            selected_param = []
            for i in range(0, len(checkboxes)):
                if checkboxes[i].value == True:
                    selected_param = selected_param + [checkboxes[i].description]

            button_boxplot.layout.visibility = 'visible'
            button_final_param.layout.visibility = 'visible'
            print(selected_param)


    def disable_param_button(b):
        button_param_selected.layout.visibility = 'visible'

    def send_param(b):
        with param_output:
            print(output1.outputs[0]['text'])
    checkboxes_output = widgets.VBox(children=checkboxes)
    for i in range(4):
        checkboxes_output.children[i].observe(disable_param_button)

    check_box = widgets.HBox([checkboxes_output],layout=box_layout)
    display(check_box)

    get_box = widgets.HBox([get_lab, button_param_selected, output1],layout=box_layout2)

    button_param_selected.on_click(return_param)
    display(get_box)
    return(output1)
    
    
        
    
values = {
    "FWHM" : "1",
    "Fit (R2)" : "2",
    "Mes./theory resolution ratio" : "3",
    "SBR" : "4"
}


def display_selected_plot(selected_param, folder_selected, df_XYZ, df_SBR, dfXYZ_MedStd, df_MedStd_SBR, leg_dict, values=values):
    print('\n')
    selected_param = selected_param.replace("'", "")
    selected_param = selected_param.replace("]\n", "")
    selected_param = selected_param.strip('][').split(', ')
    
    style = {'description_width': 'initial'}
    save_button_selection = widgets.ToggleButtons(
        options=['Yes', 'No'],
        description='Do you want to save your figures in PDF format ? ',
        disabled=False,
        button_style='info', 
        style=style,
        value=None,
    )
    out = widgets.Output()
    
    
    button_boxplot2 = widgets.Button(description="Show Boxplot!", button_style='success', style=dict(font_weight='bold'))

    
    out2 = widgets.Output()
    button_boxplot2.layout.visibility = 'hidden'
    
    
    pdf_path = None
    
    def fun(obj):
        with out:
            button_boxplot2.layout.visibility = 'visible'
            if save_button_selection.value == 'Yes':
                global pdf_path
                pdf_path = os.path.join(folder_selected, "pdf_result")
                

                if not os.path.exists(pdf_path):
                    os.makedirs(pdf_path)
                return(pdf_path)
                    
            
            
            
    save_button_selection.observe(fun, 'value')
    display(save_button_selection, out)    
    
    
    
    def boxp(obj):
        with out2:
            im_path = fun(None)
            result = save_button_selection.value
            sys_name = df_XYZ["Microscope"].unique()

            dfX_MedStd = dfXYZ_MedStd.loc[dfXYZ_MedStd['Axe'] == 'X']
            dfY_MedStd = dfXYZ_MedStd.loc[dfXYZ_MedStd['Axe'] == 'Y']
            dfZ_MedStd = dfXYZ_MedStd.loc[dfXYZ_MedStd['Axe'] == 'Z']

            
                
            for i in selected_param:
                if i in values:
                    param = i
                    if int(values[i]) in range(1, 4):
                        if param == 'FWHM':
                            table_column_param = 'Resolution (µm) : FWHM'
                            med_column_param = "FWHM median"
                            ttest_table_column = 'FWHM max'

                        elif param == 'Fit (R2)':
                            table_column_param = 'Fit (R2)'
                            med_column_param = "R2 median"
                            ttest_table_column = 'R2 max'


                        elif param == 'Mes./theory resolution ratio':
                            table_column_param = 'Mes./theory resolution ratio (µm)'
                            med_column_param = "Mes./theory resolution ratio median"
                            ttest_table_column = 'Mes./theory resolution ratio max'

                        
                        create_XYZ_box(df_XYZ, param, table_column_param, med_column_param, im_path,
                                       result, ttest_table_column, df_MedStd_SBR, leg_dict, sys_name, 
                                       dfX_MedStd, dfY_MedStd, dfZ_MedStd)
                    if int(values[i]) == 4:
                        create_SBR_box(df_SBR, result, im_path, df_MedStd_SBR, leg_dict, sys_name)

            if save_button_selection.value == 'Yes':

                pdfs = os.listdir(im_path)
                merger = PdfFileMerger()

                for pdf in pdfs:

                    p = os.path.join(im_path, pdf)
                    merger.append(p)

                home = str(Path.home())
                result_path = f'{home}/RESULT'
                if not os.path.exists(result_path):
                    os.makedirs(result_path)
                fnew = f"{datetime.datetime.today().strftime('%Y%m%d')}_PLOT_RESULT.pdf"
                final_pdf = os.path.join(result_path, fnew)
                counter = 0
                root, ext = os.path.splitext(fnew)
                while os.path.exists(f'{final_pdf}'):
                    counter += 1
                    fnew = '%s_(%i)%s' % (root, counter, ext)    
                    final_pdf = os.path.join(result_path, fnew)

                merger.write(final_pdf)
                merger.close()

                if folder_selected == '':
                    os.remove(fnew)
                    print(f'No PDF file created !')
                else:
                    print(f'{fnew} is created')
                    print(f'PATH : {result_path}')



                im_path = pathlib.Path(im_path)
                if im_path.exists() and im_path.is_dir():
                    shutil.rmtree(im_path)



            else:
                print("No saving")

    button_boxplot2.on_click(boxp)
    display(button_boxplot2, out2)
        
