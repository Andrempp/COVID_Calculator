'''
@info covid-19 predictability tool
@version 1.0
'''

import dash, gui_utils, numpy as np, pickle
import dash_html_components as html
from dash.dependencies import Input, Output


''' =========================== '''
''' ====== A: PARAMETERS ====== '''
''' =========================== '''

pagetitle = 'COVID-19: predictability tool'
stage = ['positive test','hospitalized','intensive care']
comorbidities = {
    'Asthma':'ASTH',
    'Cancer':'CANC',
    'Cardiovascular disease':'CARDIACDIS',
    'Chronic hematologic disease':'CHD',
    'Diabetes':'DIAB',
    'HIV':'HIV',
    'Kidney disease':'KIDNEY',
    'Hepatic disease':'LIVER',
    'Lung disease':'LUNG',
    'Neuromuscular disease':'NEUROMUS',
    'Dyslipidemia':'DISLIP',
    'Pregnant 1st quarter':'PREG1',
    'Pregnant 2nd quarter':'PREG2',
    'Pregnant 3rd quarter':'PREG3',
    'Post-pregancy':'PREGPOST'
}

result = [html.Br(),html.B('Result:'),html.Div('Input the patient profile...')]

parameters = [
    ("Patient profile",[
        ('stage',stage,gui_utils.Button.radio,'positive test'), 
        ('age','67',gui_utils.Button.input,None), 
        ('gender',['male','female'],gui_utils.Button.radio,'male')]),
    ("Clinical history",[('comorbidities',comorbidities.keys(),gui_utils.Button.multidrop,['Cancer','Diabetes','Hepatic disease'])])]

layout = gui_utils.get_layout(pagetitle,parameters,[('result',result,gui_utils.Button.html)])

models_path = "./calc_models/"
files = ["calc_hosp_recall", "calc_hosp_f1", "calc_ic1_recall", "calc_ic1_f1", "calc_ic2_recall", "calc_ic2_f1",
         "calc_out1_recall", "calc_out1_f1", "calc_out2_recall", "calc_out2_f1", "calc_out3_recall", "calc_out3_f1",
         "calc_rs_recall", "calc_rs_f1"]

classifiers = []

for file in files:
    filename = models_path + file + ".sav"
    clf = pickle.load(open(filename, 'rb'))
    classifiers.append(clf)

target_dict = {"Hosp": {"phrase": ("need hospitalization","needing"), "classifiers": (classifiers[0], classifiers[1])},
               "IC1": {"phrase": ("need intensive care","needing"), "classifiers": (classifiers[2], classifiers[3])},
               "IC2": {"phrase": ("need intensive care","needing"), "classifiers": (classifiers[4], classifiers[5])},
               "Outcome1": {"phrase": ("pass away","passing"), "classifiers": (classifiers[6], classifiers[7])},
               "Outcome2": {"phrase": ("pass away","passing"), "classifiers": (classifiers[8], classifiers[9])},
               "Outcome3": {"phrase": ("pass away","passing"), "classifiers": (classifiers[10], classifiers[11])},
               "RespSupport": {"phrase": ("need respiratory support","needing"), "classifiers": (classifiers[12], classifiers[13])},
               }
to_use = {"positive test": ["Hosp", "IC1", "Outcome1"], "hospitalized": ["IC2", "RespSupport","Outcome2"],
          "intensive care": ["Outcome3"]}

age_mean= 48.026216
age_std = 24.804093

''' ==========================='''
''' ====== C: UPDATE GUI ====== '''
''' =========================== '''

app = dash.Dash(__name__, assets_folder = 'assets', include_assets_files = True) 

@app.callback(Output('result','children'),[Input('button','n_clicks')],gui_utils.get_states(parameters)) #[State('stage','value'),State('age','value'),State('gender','value'),State('comorbidities','value')])
def update_map(inp,*args):
    states = dash.callback_context.states
    print("states",states)
    if inp is None: return result
    stage = states['stage.value']
    age = (int(states['age.value']) - age_mean) / age_std
    gender = 0 if states['gender.value'] == "female" else 1
    data = [age, gender]
    sel_comorbidities = states['comorbidities.value']
    #################################################
    if stage == "hospitalized" or stage == "intensive care": data.append(1)
    if stage == "intensive care": data.append(1)
    for comorb in comorbidities:
        if comorb in sel_comorbidities: data.append(1)
        else: data.append(0)
    data = np.array(data).reshape(1,-1)
    #################################################
    to_return = [html.Br(),html.B('Result:'),html.Br()]
    for target in to_use[stage]:
        print("Target: ",target)
        clf1 = target_dict[target]["classifiers"][0]
        clf2 = target_dict[target]["classifiers"][1]
        if target == "RespSupport":
            print("resp")
            pred1 = clf1.predict_proba(data)[0]
            pred2 = clf2.predict_proba(data)[0]
            result1 = [pred1[0]] + [pred1[1]+pred1[2]]
            result2 = [pred2[0]] + [pred2[1]+pred2[2]]
        else:
            result1 = clf1.predict_proba(data)[0]
            result2 = clf2.predict_proba(data)[0]
        print("Results for target: {}\n{}\n{}".format(target,result1,result2))
        yes1, yes2 = 'will' if result1[1]>0.5 else 'won\'t', 'will' if result2[1]>0.5 else 'won\'t'
        phrase = target_dict[target]["phrase"][0]
        verb = target_dict[target]["phrase"][1]
        to_return.append(html.Div('According to classifier that maximizes recall:'))
        to_return.append(html.Div('The patient ' + yes1 +" "+ phrase + ' (' + str(int(result1[1] * 100)) + '% of ' + verb +')'))
        to_return.append(html.Br(),)
        to_return.append(html.Div('According to classifier that maximizes F1-score:'))
        to_return.append(html.Div('The patient '+yes2+" "+ phrase +' ('+str(int(result2[1]*100))+'% of '+ verb+')'))
        to_return.append(html.Br())
        to_return.append(html.Br())
    return to_return

''' ===================== '''
''' ====== D: MAIN ====== '''
''' ====================== '''

if __name__ == '__main__':
    app.config.suppress_callback_exceptions = True
    app.layout = layout
    app.run_server()
