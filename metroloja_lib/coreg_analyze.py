import os, glob, pathlib, time, datetime, shutil
import plotly.graph_objects as go
import plotly.express as px
import ipywidgets as widgets
from ipyfilechooser import FileChooser
import pandas as pd
from pathlib import Path

from alive_progress import alive_bar
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
    len_bar = (len(date_file)-1)*2
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
        DF_coreg = pd.DataFrame()
        DF_coreg_noComb = pd.DataFrame()
        idx = 0
        for process in all_processed_path:
            # r=root, d=directories, f = files
            for r, d, f in os.walk(process):
                for file in f:
                    if file == "summary.xls":
                        f_path = os.path.join(r, file)
                        TempName = all_image_name[idx]
                        for i in range(len(TempName)):
                            grp = TempName[i]
                            path_split = process.split(os.sep)

                            filename = grp
                            initTempDate = path_split[-3]
                            date = datetime.datetime.strptime(initTempDate, '%Y%m%d').date()
                            microscope = f'{path_split[-5]} : {path_split[-4]}'
                            '''
                            for fn in lf_name:
                                if fn in grp:
                                    fn2 = fn.replace(' ','')
                            '''

                            data = pd.read_csv(f_path, sep = "\t", header=None, names=range(8))
                            #data = pd.read_csv(f_path,
                            data = data.iloc[:, :-1] # Drop the last column

                            table_names = ["Ratios", "Raw Ratios", "Pixel shift", "Calibrated distances (in µm)", "Raw calibrated distancesµm)"]
                            groups = data[0].isin(table_names).cumsum()
                            tables = {g.iloc[0,0]: g.iloc[1:] for k,g in data.groupby(groups)} #dictionnary of each selected table 

                            df_ratios = tables["Raw Ratios"]
                            df_distances = tables["Raw calibrated distancesµm)"]

                            # Reindex column name
                            df_ratios = df_ratios.reset_index(drop=True)
                            df_ratios.columns = df_ratios.iloc[0]
                            df_ratios = df_ratios.reindex(df_ratios.index.drop(0)).reset_index(drop=True)
                            df_ratios.columns.name = None


                            df_distances = df_distances.reset_index(drop=True)
                            df_distances.columns = df_distances.iloc[0]
                            df_distances = df_distances.reindex(df_distances.index.drop(0)).reset_index(drop=True)
                            df_distances.columns.name = None


                            # Reindex row name
                            df_ratios = df_ratios.set_index('Combinations')

                            df_distances = df_distances.set_index('Combinations')


                            # Create dataframe
                            CombList = df_ratios.columns
                            for comb in CombList:
                                comb_val_ratio = df_ratios.loc[grp, comb]
                                comb_val_dist = df_distances.loc[grp, comb]

                                TempDataList = pd.DataFrame({'Date':[date], "Microscope":[microscope], "Image Name":[grp], "Combination":[comb], 'Distances (µm)':[comb_val_dist], 'Ratios':[comb_val_ratio]})
                                DF_coreg = pd.concat([DF_coreg,TempDataList])

                            TempDataList2 = pd.DataFrame({'Date':[date], "Microscope":[microscope], "Image Name":[grp]})
                            DF_coreg_noComb = pd.concat([DF_coreg_noComb,TempDataList2])
                            #DF_coreg_noComb  = DF_coreg_noComb.groupby(['Date', 'Image Name']).size().reset_index(name='n')
                            DF_coreg_noComb2 = DF_coreg_noComb.groupby(['Date']).size().reset_index(name='n')
                            time.sleep(.005)
                            bar()
                        
            idx += 1
                                
    DF_coreg.reset_index(drop=True, inplace=True)
    
    return(DF_coreg, DF_coreg_noComb2, df_distances.columns)

                            

    

    
def coreg_stats(DF_coreg0, DF_coreg1):
    '''
    DF_coreg = DF_coreg.explode('Distances (µm)')
    DF_coreg['Distances (µm)'] = DF_coreg['Distances (µm)'].astype('float')
    '''
    
    #eff_df  = DF_coreg0.groupby(['Date']).size().reset_index(name='n')
    median_df_dist = DF_coreg0.groupby(['Date', 'Microscope', 'Combination'])['Distances (µm)'].median().to_frame('Distances Median').reset_index()
    max_df_dist  = DF_coreg0.groupby(['Date', 'Microscope', 'Combination'])['Distances (µm)'].max().to_frame('Distances Max').reset_index()
    median_df_ratio = DF_coreg0.groupby(['Date', 'Microscope', 'Combination'])['Ratios'].median().to_frame('Ratios Median').reset_index()
    max_df_ratio  = DF_coreg0.groupby(['Date', 'Microscope', 'Combination'])['Ratios'].max().to_frame('Ratios Max').reset_index()


    allStat = [median_df_dist, max_df_dist, median_df_ratio, max_df_ratio]
    df_MedStd = reduce(lambda  left,right: pd.merge(left,right,on=['Date', 'Microscope', 'Combination'], how='outer'), allStat)
    df_MedStd = df_MedStd.merge(DF_coreg1, on='Date', how='outer')

    leg_dict = {}
    for i in range(len(df_MedStd)):
        t = df_MedStd['Date'].iloc[i]
        leg_dict[str(t)] = str(t) + ' (n = ' + str(df_MedStd['n'].iloc[i]) + ')'

    return(df_MedStd, leg_dict)



box_layout = widgets.Layout(display='flex', flex_flow='column', align_items='center')


def select_param(button_boxplot, button_final_param, box_layout=box_layout):
    print('\n')
    text2 = '2. Check all the measurements you want to plot'
    Lab2 = widgets.HTML(value = f"<b><font color='green', size='5'>{text2}</b>")
    Lab_box2 = widgets.HBox([Lab2],layout=box_layout)
    display(Lab_box2)
    

    values = ["Distances (µm)", "Ratios"]
    checkboxes = [widgets.Checkbox(value=False, description=label) for label in values]

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
    for i in range(2):
        checkboxes_output.children[i].observe(disable_param_button)

    check_box = widgets.HBox([checkboxes_output],layout=box_layout)
    display(check_box)

    get_box = widgets.HBox([get_lab, button_param_selected, output1],layout=box_layout2)

    button_param_selected.on_click(return_param)
    display(get_box)
    return(output1)




def create_box(df, param, table_column_param, med_column_param, im_path,
               result, ttest_table_column, leg_dict, sys_name, DC_var, df_MedStd, date_list):
    date1 = date_list
    date2 = date1.copy()
    date2[0] = "first date"
    
    df = df.explode(table_column_param)
    df[table_column_param] = df[table_column_param].astype('float')
    

    fig = px.box(df, x = "Date", y = table_column_param, color = "Date", category_orders={"Date" : date1},
                 facet_row="Combination", title = f"{sys_name[0]}           {param} Box plot           PICT-BDD           (Update : {datetime.datetime.today().strftime('%Y-%m-%d')})<br><sub><b>Statistical T-Tests are carried out between a date and the date immediately preceding it</b></sub>", points="outliers", height=3000, width=900).update_yaxes(matches=None)

    fig.update_layout(showlegend=True)
    fig.update_layout(title_x=0.5)
    
    
    
    fig.for_each_trace(lambda t: t.update(name = leg_dict[t.name],
                                          legendgroup = leg_dict[t.name],
                                          hovertemplate = t.hovertemplate.replace(t.name, leg_dict[t.name])
                                         )
                      )



        
    listAllComb = list(DC_var.keys())
    nb_listAllComb = len(listAllComb)
    for lac in listAllComb:
        TempDF_Med = DC_var[lac]
        Which_channel = TempDF_Med['Combination'][0]

        fig.add_trace(
            go.Scatter(x=TempDF_Med["Date"].tolist(), y=TempDF_Med[med_column_param].tolist(), showlegend=False, mode='lines+markers',
                       line=dict(color="#000000")), row=nb_listAllComb, col=1
        )


            


        dfTempComb = df[df["Combination"] == Which_channel]



        
        for i in range(len(date1)-1):
            dfTempComb = dfTempComb.explode(table_column_param)
            dfTempComb[table_column_param] = dfTempComb[table_column_param].astype('float')

            TempDF_1 = dfTempComb[dfTempComb["Date"] == date1[i]]
            TempDF_2 = dfTempComb[dfTempComb["Date"] == date2[i + 1]]



            X = date2[i + 1]
            Y = TempDF_Med[TempDF_Med["Date"]==X]
            Y = Y[ttest_table_column]
            t, p = stats.ttest_ind(TempDF_1[table_column_param], TempDF_2[table_column_param], equal_var=False)
            sz = 14

            
            if p >= 0.05:
                symbol = '<b>ns</b>'
            elif p >= 0.01: 
                symbol = '<b>*</b>'
            elif p >= 0.001:
                symbol = '<b>**</b>'
            else:
                symbol = '<b>***</b>'
            

            fig.add_annotation(dict(font=dict(size=sz), 
                                    x=X, y=float(Y),
                                    text=symbol,
                                    showarrow=False,
                                    arrowhead=1,
                                    yanchor='bottom',
                                    xref='x1',
                                    yref='y' + str(nb_listAllComb)))
            
        nb_listAllComb -= 1
    

    fig.show()
    
    if result == 'Yes':
        global XYZpdf_name
        param = param.replace(" ", "_")
        param = param.replace(".", "")
        param = param.replace("/", "_")
        XYZpdf_name = f'{param}_boxplot.pdf'
        XYZpdf_path = os.path.join(im_path, XYZpdf_name)
        fig.write_image(XYZpdf_path)
    







def display_selected_plot(selected_param, df, df_MedStd, folder_selected, leg_dict, list_comb, date_list, box_layout=box_layout):
    values = ["Distances (µm)", "Ratios"]
    
    print('\n')
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
    
    
    button_boxplot2 = widgets.Button(description="Show Boxplot!", button_style='warning', style=dict(font_weight='bold'), 
                                     layout = widgets.Layout(width = '40%', height = '60px'))

    box2 = widgets.HBox(children=[button_boxplot2],layout=box_layout)
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
    print('\n')
    
    
    
    def boxp(obj):
        with out2:
            im_path = fun(None)
            result = save_button_selection.value

            sys_name = df["Microscope"].unique()

            index = 0
            DC_var = {}
            for a in range(len(list_comb)):
                index += 1
                DC_var["Comb" + str(index)] = df_MedStd.loc[df_MedStd['Combination'] == list_comb[a]].reset_index(drop=True)

            for i in selected_param:
                if i in values:
                    param = i
                    if param == 'Distances (µm)':
                        table_column_param = param
                        med_column_param = "Distances Median"
                        ttest_table_column = 'Distances Max'


                    else:
                        table_column_param = param
                        med_column_param = "Ratios Median"
                        ttest_table_column = 'Ratios Max'



                    create_box(df, param, table_column_param, med_column_param, im_path,
                                   result, ttest_table_column, leg_dict, sys_name, 
                                   DC_var, df_MedStd, date_list)

                    print('\n')

            if result == 'Yes':
                pdfs = os.listdir(im_path)
                merger = PdfFileMerger()

                for pdf in pdfs:
                    p = os.path.join(im_path, pdf)
                    merger.append(p)

                home = str(Path.home())
                result_path = f'{home}/RESULT'
                if not os.path.exists(result_path):
                    os.makedirs(result_path)
                
                fnew = f"{datetime.datetime.today().strftime('%Y%m%d')}_PLOT_RESULT_Coreg.pdf"
                final_pdf = os.path.join(result_path, fnew)
                counter = 0
                root, ext = os.path.splitext(fnew)
                while os.path.exists(f'{final_pdf}'):
                    counter += 1
                    fnew = '%s_(%i)%s' % (root, counter, ext)    
                    final_pdf = os.path.join(result_path, fnew)

                merger.write(final_pdf)
                merger.close()

                if result_path == '':
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
    display(box2, out2)
    
