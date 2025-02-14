import pandas as pd
import pdfkit as pdf
import glob
import pickle
import numpy as np

def createPDFreport_spanish(patient_age, region, subjectANDoutput_dir, metric='vol', prediction_intervals_dir = '/home/neurocogn/N1.0Dir/NezihNiegu/neuroimaging_processor/Volumetry/batches/prediction_intervals/'):
    '''
    Returns a PDF and CSV report from subject with prediction interval and percentile for age
     
    Creates a PDF report with subject's measure, the controls' prediction interval, and the percentile for age and a CSV report with subjet's measure and percentile for age
     
    Args:
        patient_age (int): Age of the patient
        region (str): Freesurfer's brain part to create report from (Left hemisphere: "lh", Right hemisphere: "rh", Subcortical regions: "seg", Brainstem structures: "brainstem", Hippocampal subfields: "hippo")
        metric (str): Freesurfer's metric to create report of ( default is "vol", Volume: "vol", Surface area: "area", Thickness: "thick")
        subjectANDoutput_dir (str): Directory where the Freesurfer's stat files are and in which the report PDF and CSV will be saved
     
    Returns:
        .pdf (PDF): Subject report with prediction interval and percentile for age. Saved at subjectANDoutput_dir
        .csv (CSV): Subject report with percentile for age. Saved at subjectANDoutput_dir
    '''
    # In[190]:
    
    
    
    
    #patient_age = 81
    #region = 'lh' #seg, rh, brainstem, hippo
    #metric = 'vol' #area, thick
    #subjectANDoutput_dir = '/home/neurocogn/N1.0Dir/NezihNiegu/neuroimaging_processor/Volumetry/sub-00121/sub-00121/'
    #prediction_intervals_dir = '/home/neurocogn/N1.0Dir/NezihNiegu/neuroimaging_processor/Volumetry/batches/prediction_intervals/'
    
    
    # In[191]:
    
    
    subject = subjectANDoutput_dir.split("/")[-2]
    
    if metric == 'vol':
        pre_column_name = 'volume'
        col_unit = "mm3"
        round_digits = 0
    if metric == 'thick':
        pre_column_name = 'thickness'
        col_unit = "mm"
        round_digits = 2
    if metric == 'area':
        pre_column_name = 'area'
        col_unit = "mm2"
        round_digits = 0

    if region == 'lh':
        column_name = 'lh.aparc.'+pre_column_name
        separator="\t"
        report_label = "Hemisferio izquierdo"
        if metric == 'vol':
            report_names = '/home/neurocogn/N1.0Dir/NezihNiegu/neuroimaging_processor/Volumetry/python_scripts/CSVs_with_report_names/hemisphere_names.csv'
        if metric == 'thick':
            report_names = '/home/neurocogn/N1.0Dir/NezihNiegu/neuroimaging_processor/Volumetry/python_scripts/CSVs_with_report_names/hemisphere_names_thick.csv'
        if metric == 'area':
            report_names = '/home/neurocogn/N1.0Dir/NezihNiegu/neuroimaging_processor/Volumetry/python_scripts/CSVs_with_report_names/hemisphere_names_area.csv'
        
    if region == 'rh':
        column_name = 'rh.aparc.'+pre_column_name
        separator="\t"
        report_label = "Hemisferio derecho"
        if metric == 'vol':
            report_names = '/home/neurocogn/N1.0Dir/NezihNiegu/neuroimaging_processor/Volumetry/python_scripts/CSVs_with_report_names/hemisphere_names.csv'
        if metric == 'thick':
            report_names = '/home/neurocogn/N1.0Dir/NezihNiegu/neuroimaging_processor/Volumetry/python_scripts/CSVs_with_report_names/hemisphere_names_thick.csv'
        if metric == 'area':
            report_names = '/home/neurocogn/N1.0Dir/NezihNiegu/neuroimaging_processor/Volumetry/python_scripts/CSVs_with_report_names/hemisphere_names_area.csv'
        
    if region == 'seg':
        column_name = 'Measure:volume'
        separator="\t"
        report_label = "Estructuras subcorticales"
        report_names = '/home/neurocogn/N1.0Dir/NezihNiegu/neuroimaging_processor/Volumetry/python_scripts/CSVs_with_report_names/subcortical_names.csv'
        
    if region == 'brainstem' or region == 'hippo':
        column_name = 'Subject'
        separator=" "
        
    if region == 'hippo': 
        report_label = "Estructuras del hipocampo"
        report_names = '/home/neurocogn/N1.0Dir/NezihNiegu/neuroimaging_processor/Volumetry/python_scripts/CSVs_with_report_names/hippo_names.csv'
        
    if region == 'brainstem':
        report_label = "Estructuras del tallo cerebral"
        report_names = '/home/neurocogn/N1.0Dir/NezihNiegu/neuroimaging_processor/Volumetry/python_scripts/CSVs_with_report_names/brainstem_names.csv'
        
    if patient_age < 40:
        group_age = "lessthan40years"
    if patient_age >= 40:
        group_age = "40ormoreyears"
    
    
    # In[192]:
    
    
    for sub_stats_file in glob.iglob(subjectANDoutput_dir+'*'+region+'*'+metric+'*.txt'):
        print(sub_stats_file)
    
    subject_stats = pd.read_csv(sub_stats_file,sep=separator)
    subject_stats = subject_stats[subject_stats[column_name]==subject]
    subject_stats = subject_stats.loc[list(subject_stats.index)[0]]
    subject_stats = subject_stats.drop(column_name)
    
    
    # In[193]:


    for batch_file in glob.iglob(prediction_intervals_dir+'*'+region+'*'+metric+'*'+group_age+'*.pkl'):
        print(batch_file)
        
    f = open(batch_file,'rb')
    dictionary = pickle.load(f)
    f.close()
    
    
    # In[194]:
    
    
    low_reference = dictionary[patient_age][1]
    low_reference = [np.double(numeric_string) for numeric_string in low_reference]
    
    
    # In[195]:
    
    
    high_reference = dictionary[patient_age][2]
    high_reference = [np.double(numeric_string) for numeric_string in high_reference]
    
    
    # In[196]:
    
    
    P_slope = np.subtract(high_reference,low_reference)/(97.5-2.5)
    P_intercept = np.subtract(low_reference,P_slope*2.5)
    Percentiles = np.divide(np.subtract(subject_stats,P_intercept),P_slope)
    Percentiles = np.round(Percentiles.astype(np.double),2)
    Percentiles[Percentiles>100] = 100
    Percentiles[Percentiles<0] = 0
    
    
    # In[197]:
    
    
    reference_range = []
    mrexample_vols = []
    for k in range(len(low_reference)):
        if low_reference[k] <= 0.0:
            low_reference[k] = 0.0 
    for k in range(len(low_reference)):
        reference_range.append(str(np.round(low_reference[k],2)) + " - " + str(np.round(high_reference[k],2)))
        if subject_stats[k] >= np.round(low_reference[k],2) and subject_stats[k] <= np.round(high_reference[k],2):
            mrexample_vols.append(str(np.round(subject_stats[k],round_digits)))
        else:
            mrexample_vols.append(str(np.round(subject_stats[k],2)) + "*")
    
    report_names_df = pd.read_csv(report_names,encoding='latin1')
    print(list(report_names_df['Name_spanish']))
    reference_range_df = pd.DataFrame({'Región cerebral':list(report_names_df['Name_spanish']),'Resultado ('+col_unit+')':mrexample_vols,'Intervalo de referencia para la edad ('+col_unit+')':reference_range,'Percentil para la edad':Percentiles})
    reference_range_df = reference_range_df.reset_index(drop=True)
    
    
    # In[198]:
        
    HTML_TEMPLATE1 = '''
        <html>
        <head>
        <meta charset="utf-8">
        <style>
        header{
        text-align: center;
        }
        h4 {
        margin-right: 2%;
        }
        body {
        background-color: #FFFFFF;	
        }
        .flex-container {
        display: flex;
        margin: auto;
        width:80%
        }
        #left {
            text-align: left;
        }
        #right {
            text-align: right;
        margin-top: 6.5%;
        }
        
        h3 {
            text-align: center;
            font-family: Helvetica, Arial, sans-serif;
        }
        table { 
            margin-left: auto;
            margin-right: auto;
        }
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        th, td {
            padding: 5px;
            text-align: center;
            font-family: Helvetica, Arial, sans-serif;
            font-size: 90%;
        }
        table tbody tr:hover {
            background-color: #dddddd;
        }
        .wide {
            width: 90%; 
        }
        </style>
    
        </head>
        <body>
        <header>
        <div class="flex-container">
        <div class="logos" id="left"><img src="/home/neurocogn/N1.0Dir/NezihNiegu/neuroimaging_processor/Volumetry/logos/HZH.png" width="150%"></div>
        <div class="logos" id="right"><img src="/home/neurocogn/N1.0Dir/NezihNiegu/neuroimaging_processor/Volumetry/logos/NCO.png" width="70%"></div>
        </div>
        <div class="flex-container">
        <h4>Médico Solicitante: ___________________________________________________________________</h4>
        <h4>Área/Especialidad: __________________________________________________</h4>
        </div><br/>
        <div class="flex-container">
        <h4>Paciente: _______________________________________________________________________________</h4>
        <h4>Edad Actual: _________________</h4>
        <h4>Fecha: ___________________________</h4>
        </div><br/><br/><br/><br/><br/>
        <div style="text-align: center">	
        <h4>________________________________________</h4>
        <h4>PhD MSc MD Ricardo Caraza Camacho</h4>
        <h4></h4>	    
        </header>
    '''

    HTML_TEMPLATE2 = '''
    </body>
    </html>
    '''
    
        
    def to_html_pretty(df, filename='/tmp/out.html', title=''):
            '''
            Write an entire dataframe to an HTML file
            with nice formatting.
            Thanks to @stackoverflowuser2010 for the
            pretty printer see https://stackoverflow.com/a/47723330/362951
            '''
            ht = ""
            if title!= "":
                ht += '<h2> %s </h2>\n' % title
            ht += df.to_html(classes='wide', escape=False)
            with open(filename, 'w') as f:
                f.write(HTML_TEMPLATE1 + ht + HTML_TEMPLATE2)
    
    # In[199]:
    
    
    f = open(subjectANDoutput_dir+'intermediate_'+region+'_'+metric+'.html','w')
    a = reference_range_df.to_html(index_names=False)
    f.write(a)
    f.close()
    
    
    # In[200]:
    
    
    intermediate_html = subjectANDoutput_dir+'intermediate_'+region+'_'+metric+'.html'
    to_html_pretty(reference_range_df,intermediate_html,'Nombre: ' + subject + "; Edad = "+str(patient_age)+"; "+report_label)
    
    
    # In[201]:
    
    
    pdf.from_file(subjectANDoutput_dir+'intermediate_'+region+'_'+metric+'.html',subjectANDoutput_dir + 'report_'+region+'_'+metric+'.pdf',options={'encoding':'utf-8'})
    
    
    # In[202]:
    
    
    excel=pd.DataFrame()
    for i in range(0,len(subject_stats)):
        excel_tmp = pd.DataFrame(np.array([[subject_stats[i],Percentiles[i]]]),columns=[list(Percentiles.index)[i],list(Percentiles.index)[i]+'_perc'])
        excel = pd.concat([excel,excel_tmp],axis=1)
    excel.to_csv(subjectANDoutput_dir+'report_'+region+'_'+metric+'.csv')

