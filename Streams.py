import json
import sys
from PyQt5.QtCore import *
from ComponentSelector import compound_selected

class MaterialStream():
    counter = 1
    def __init__(self, compound_names = []):

        self.name = 'MaterialStream' + str(MaterialStream.counter)
        self.type = 'MaterialStream'

        self.compound_names = compound_names
        self.count = MaterialStream.counter
        self.thermo_package ="RaoultsLaw"
        self.mode1 = "P"
        self.mode2 = "T"

        self.mode1_val = ""
        self.mode2_val = ""
        self.OM_data_init = ''
        self.OM_data_eqn = ''
        self.no_of_inputs = 1
        self.no_of_outputs = 1
        self.x = 2500-30
        self.y = 2500-30
        self.pos = QPointF(self.x, self.y)
        MaterialStream.counter+=1
        self.start_dict = {}
        self.eqn_dict = {}
        self.modes_list = ["PT", "PH", "PVF", "TVF", "PS"]
        self.saved = False
        self.mode = self.modes_list[0]
        
        self.variables = {
            'P'     : {'name':'Pressure',         'value':101325,    'unit':'Pa'},         
            'T'     : {'name':'Temperature',      'value':300,       'unit':'K'},
            
            'xvap'   : {'name':'Vapour Mole Fraction',          'value':None,       'unit':''},
            'H_p[1]'  : {'name':'Mixture Molar Entalpy',        'value':None,       'unit':'J/mol'},
            'S_p[1]'  : {'name':'Mixture Molar Entropy',        'value':None,       'unit':'J/mol.K'},
            'F_p[1]'  : {'name':'Mixture Molar Flow',           'value':100,       'unit':'mol/s'},
            'Fm_p[1]' : {'name':'Mixture Mass Flow',            'value':None,    'unit':'g/s'},

            'H_p[2]'  : {'name':'Liquid Molar Entalpy',        'value':None,       'unit':'J/mol'},
            'S_p[2]'  : {'name':'Liquid Molar Entropy',        'value':None,       'unit':'J/mol.K'},
            'F_p[2]'  : {'name':'Liquid Molar Flow',            'value':None,       'unit':'mol/s'},

            'H_p[3]'  : {'name':'Vapour Molar Entalpy',        'value':None,       'unit':'J/mol'},
            'S_p[3]'  : {'name':'Vapour Molar Entropy',        'value':None,       'unit':'J/mol.K'},
            'F_p[3]'  : {'name':'Vapour Molar Flow',            'value':None,       'unit':'mol/s'},

            'x_pc'  : {'name':'Mole Fraction',    'value':[],      'unit':''},
            'xm_pc' : {'name':'Mass Fraction',    'value':None,     'unit':''},
            
            'F_pc'  : {'name':'Mole Flow',        'value':100,      'unit':'mol/s'},
            'Fm_pc' : {'name':'Mass Flow',        'value':None,     'unit':'g/s'},
        }
        self.init_variables()

    def update_compounds(self):
        self.compound_names = compound_selected

    def init_variables(self):
        Nc = len(self.compound_names)
        for i, val in enumerate(self.compound_names):
            self.variables['x_pc[1,'+ str(i+1)+']'] = {'name':val + ' Mixture Mole Fraction', 'value':round(1/Nc,4), 'unit':''}
            self.variables['xm_pc[1,'+ str(i+1)+']'] = {'name':val + ' Mixture Mass Fraction', 'value':None, 'unit':''}
            self.variables['F_pc[1,'+ str(i+1)+']'] = {'name':val + ' Mixture Mole Flow', 'value':None, 'unit':'mol/s'}
            self.variables['Fm_pc[1,'+ str(i+1)+']'] = {'name':val + ' Mixture Mass Flow', 'value':None, 'unit':'g/s'}

            self.variables['x_pc[2,'+ str(i+1)+']'] = {'name':[val + ' Liquid Mole Fraction'], 'value':None, 'unit':''}
            self.variables['xm_pc[2,'+ str(i+1)+']'] = {'name':[val + ' Liquid Mass Fraction'], 'value':None, 'unit':''}
            self.variables['F_pc[2,'+ str(i+1)+']'] = {'name':[val + ' Liquid Mole Flow'], 'value':None, 'unit':'mol/s'}
            self.variables['Fm_pc[2,'+ str(i+1)+']'] = {'name':[val + ' Liquid Mass Flow'], 'value':None, 'unit':'g/s'}

            self.variables['x_pc[3,'+ str(i+1)+']'] = {'name':[val + ' Vapour Mole Fraction'], 'value':None, 'unit':''}
            self.variables['xm_pc[3,'+ str(i+1)+']'] = {'name':[val + ' Vapour Mass Fraction'], 'value':None, 'unit':''}
            self.variables['F_pc[3,'+ str(i+1)+']'] = {'name':[val + ' Vapour Mole Flow'], 'value':None, 'unit':'mol/s'}
            self.variables['Fm_pc[3,'+ str(i+1)+']'] = {'name':[val + ' Vapour Mass Flow'], 'value':None, 'unit':'g/s'}

        for i in self.compound_names:
            self.variables[i] = {'value':''}

    def param_getter_tooltip(self,mode):
        dict = {}

        temp = []
        for i, val in enumerate(self.compound_names):
            try:
                temp.append(self.variables['x_pc[1,' + str(i+1) + ']']['value'])
            except:
                pass
        self.variables['x_pc']['value'] = temp

        if(mode=="PT"):
            self.mode1 = 'P'
            self.mode2 = 'T'
            mode1_n = self.variables['P']['name']
            mode2_n = self.variables['T']['name']
            dict = {mode1_n:str(self.variables['P']['value'])+' '+self.variables['P']['unit'], 
					mode2_n:str(self.variables['T']['value'])+' '+self.variables['T']['unit']}
        elif(mode=="PH"):
            self.mode1 = 'P'
            self.mode2 = 'H_p[1]'
            mode1_n = self.variables['P']['name']
            mode2_n = self.variables['H_p[1]']['name']
				
            dict = {mode1_n:str(self.variables['P']['value'])+' '+self.variables['P']['unit'], 
		    		mode2_n:str(self.variables['H_p[1]']['value'])+' '+self.variables['H_p[1]']['unit']}
        elif(mode=="PVF"):
            self.mode1 = 'P'
            self.mode2 = 'xvap'
            mode1_n = self.variables['P']['name']
            mode2_n = self.variables['xvap']['name']
		
            dict = {mode1_n:str(self.variables['P']['value'])+' '+self.variables['P']['unit'], 
					mode2_n:str(self.variables['xvap']['value'])+' '+self.variables['xvap']['unit']}
        elif(mode=="TVF"):
            self.mode1 = 'T'
            self.mode2 = 'xvap'
            mode1_n = self.variables['T']['name']
            mode2_n = self.variables['xvap']['name']
            dict = {mode1_n:str(self.variables['T']['value'])+' '+self.variables['T']['unit'], 
					mode2_n:str(self.variables['xvap']['value'])+' '+self.variables['xvap']['unit']}
			
        elif(mode=="PS"):
            self.mode1 = 'P'
            self.mode2 = 'S_p[1]'
            mode1_n = self.variables['P']['name']
            mode2_n = self.variables['S_p[1]']['name']

            dict = {mode1_n:str(self.variables['P']['value'])+' '+self.variables['P']['unit'], 
					mode2_n:str(self.variables['S_p[1]']['value'])+' '+self.variables['S_p[1]']['unit']}
				
        dict['Mole Flow'] = str(self.variables['F_p[1]']['value'])+' '+self.variables['F_p[1]']['unit']
        dict[self.variables['x_pc']['name']] = str(self.variables['x_pc']['value'])+' '+self.variables['x_pc']['unit']
        dict['Thermo Package'] = self.thermo_package
        return dict
    
    def param_getter_tooltip_selectedVar(self):
        dict = {}

        pressure_name = self.variables['P']['name']
        pressure_val = self.variables['P']['value']
        pressure_unit =  self.variables['P']['unit']
        temp_name = self.variables['T']['name']
        temp_val = self.variables['T']['value']
        temp_unit =  self.variables['T']['unit']
        mixMolEntal_name = self.variables['H_p[1]']['name']
        mixMolEntal_val = round(float(self.variables['H_p[1]']['value']),2)
        mixMolEntal_unit =  self.variables['H_p[1]']['unit']
        mixMolEntro_name = self.variables['S_p[1]']['name']
        mixMolEntro_val = round(float(self.variables['S_p[1]']['value']),2)
        mixMolEntro_unit =  self.variables['S_p[1]']['unit']
        vapMolFrac_name = self.variables['xvap']['name']
        vapMolFrac_val = self.variables['xvap']['value']
        vapMolFrac_unit =  self.variables['xvap']['unit']
        mixMolFlo_name = self.variables['F_p[1]']['name']
        mixMolFlo_val = self.variables['F_p[1]']['value']
        mixMolFlo_unit =  self.variables['F_p[1]']['unit']
        mixMassFlo_name = self.variables['Fm_p[1]']['name']
        mixMassFlo_val = round(float(self.variables['Fm_p[1]']['value']),2)
        mixMassFlo_unit =  self.variables['Fm_p[1]']['unit']
        
        dict = {pressure_name:str(pressure_val)+' '+pressure_unit, 
                temp_name:str(temp_val)+' '+temp_unit,
                vapMolFrac_name:str(vapMolFrac_val)+' '+vapMolFrac_unit,
				mixMolEntal_name:str(mixMolEntal_val)+' '+mixMolEntal_unit,
                mixMolEntro_name:str(mixMolEntro_val)+' '+mixMolEntro_unit,
                mixMolFlo_name:str(mixMolFlo_val)+' '+mixMolFlo_unit,
                mixMassFlo_name:str(mixMassFlo_val)+' '+mixMassFlo_unit}
        return dict

    def param_getter(self,mode):
        dict = {}

        temp = []
        for i, val in enumerate(self.compound_names):
            try:
                temp.append(self.variables['x_pc[1,' + str(i+1) + ']']['value'])
            except:
                pass
        self.variables['x_pc']['value'] = temp

        if(mode=="PT"):
            self.mode1 = 'P'
            self.mode2 = 'T'
            
            dict = {self.mode1:self.variables['P']['value'], self.mode2:self.variables['T']['value'],
                    "MolFlow":self.variables['F_p[1]']['value'],"x_pc":self.variables['x_pc']['value'],
                    "Thermo Package": self.thermo_package}
            #print('dictionary is :' + str(dict))

        elif(mode=="PH"):
            self.mode1 = 'P'
            self.mode2 = 'H_p[1]'
            dict = {self.mode1:self.variables['P']['value'], self.mode2:self.variables['H_p[1]']['value'],
                    "MolFlow":self.variables['F_p[1]']['value'], "x_pc":self.variables['x_pc']['value'],
                    "Thermo Package": self.thermo_package}
        elif(mode=="PVF"):
            self.mode1 = 'P'
            self.mode2 = 'xvap'
            dict = {self.mode1:self.variables['P']['value'], self.mode2:self.variables['xvap']['value'],
                    "MolFlow":self.variables['F_p[1]']['value'], "x_pc":self.variables['x_pc']['value'],
                    "Thermo Package": self.thermo_package}
        elif(mode=="TVF"):
            self.mode1 = 'T'
            self.mode2 = 'xvap'
            dict = {self.mode1:self.variables['T']['value'], self.mode2:self.variables['xvap']['value'],
                    "MolFlow":self.variables['F_p[1]']['value'], "x_pc":self.variables['x_pc']['value'],
                    "Thermo Package": self.thermo_package}
        elif(mode=="PS"):
            self.mode1 = 'P'
            self.mode2 = 'S_p[1]'
            dict = {self.mode1:self.variables['P']['value'], self.mode2: self.variables['S_p[1]']['value'],
                    "MolFlow":self.variables['F_p[1]']['value'], "x_pc":self.variables['x_pc']['value'],
                    "Thermo Package": self.thermo_package}
        
        return dict

    def param_setter(self,dict):
        self.variables['x_pc']['value'] = dict['x_pc'].split(",")
        #print('xpc is :' + str(self.variables['x_pc']['value']))
        self.thermo_package = dict['Thermo Package']
        self.variables['F_p[1]']['value'] = dict['MolFlow']
        self.variables[self.mode1]['value'] = dict[self.mode1]
        self.variables[self.mode2]['value'] = dict[self.mode2]
        
        for i in range(len(self.compound_names)):
            if self.variables['x_pc']['value'][i]:
                self.variables['x_pc[1,'+str(i+1)+']']['value'] = self.variables['x_pc']['value'][i]
            else:
                self.variables['x_pc[1,'+str(i+1)+']']['value'] = None
            self.variables['xm_pc[1,'+str(i+1)+']']['value'] = self.variables['xm_pc']['value']

            self.variables['F_pc[1,'+str(i+1)+']']['value'] = None
            self.variables['Fm_pc[1,'+str(i+1)+']']['value'] = None
        for i in range(0,len(self.compound_names)):
            self.variables['x_pc[2,'+str(i+1)+']']['value'] = None
            self.variables['xm_pc[2,'+str(i+1)+']']['value'] = None
            self.variables['F_pc[2,'+str(i+1)+']']['value'] = None
            self.variables['Fm_pc[2,'+str(i+1)+']']['value'] = None

            self.variables['x_pc[3,'+str(i+1)+']']['value'] = None
            self.variables['xm_pc[3,'+str(i+1)+']']['value'] = None
            self.variables['F_pc[3,'+str(i+1)+']']['value'] = None
            self.variables['Fm_pc[3,'+str(i+1)+']']['value'] = None 
    
    def set_pos(self,pos):
        self.pos = pos

    def get_min_eqn_values(self):
        x_pclist = []
        for i in range(0,len(self.compound_names)):
            x_pclist.append(self.variables['x_pc[1,'+str(i+1)+']']['value'])
        x_pc = json.dumps(x_pclist)
        x_pc = x_pc.replace('[','{')
        x_pc = x_pc.replace(']','}')
        x_pc = x_pc.replace('"','')
        
        if self.variables[self.mode1]['value']:
            self.eqn_dict[self.mode1] = self.variables[self.mode1]['value']
        if self.variables[self.mode2]['value']:
            self.eqn_dict[self.mode2] = self.variables[self.mode2]['value']
        if self.variables['x_pc']['value']:
            self.eqn_dict['x_pc[1,:]'] = x_pc
        if self.variables['F_pc']['value']:
            self.eqn_dict['F_p[1]'] = self.variables['F_p[1]']['value']

    def get_start_values(self):
        try:
            if self.variables[self.mode1]['value']:
                self.start_dict[self.mode1] = self.variables[self.mode1]['value']
            
            if self.variables[self.mode2]['value']:
                self.start_dict[self.mode2] = self.variables[self.mode2]['value']
            

            if self.variables['x_pc[2,1]']['value'] != None:
                x_pcarr = []
                for i in range(1,4):
                    cmf = []
                    for j in range(1,len(self.compound_names)+1):
                        cmf.append(str(self.variables['x_pc['+str(i)+','+str(j)+']']['value']))
                    x_pcarr.append(cmf)
                x_pcstr = json.dumps(x_pcarr)
                x_pcstr = x_pcstr.replace('[','{')
                x_pcstr = x_pcstr.replace(']','}')
                x_pcstr = x_pcstr.replace('"','')
                self.start_dict['x_pc'] = x_pcstr

            if self.variables['xm_pc[2,1]']['value'] != None:
                xm_pcarr = []
                for i in range(1,4):
                    cmf = []
                    for j in range(1,len(self.compound_names)+1):
                        cmf.append(str(self.variables['xm_pc['+str(i)+','+str(j)+']']['value']))
                    xm_pcarr.append(cmf)
                xm_pcstr = json.dumps(x_pcarr)
                xm_pcstr = xm_pcstr.replace('[','{')
                xm_pcstr = xm_pcstr.replace(']','}')
                xm_pcstr = xm_pcstr.replace('"','')
                self.start_dict['xm_pc'] = xm_pcstr

            if self.variables['Fm_pc[2,1]']['value'] != None:
                Fm_pcarr = []
                for i in range(1,4):
                    cmf = []
                    for j in range(1,len(self.compound_names)+1):
                        cmf.append(str(self.variables['Fm_pc['+str(i)+','+str(j)+']']['value']))
                    Fm_pcarr.append(cmf)
                Fm_pcstr = json.dumps(x_pcarr)
                Fm_pcstr = Fm_pcstr.replace('[','{')
                Fm_pcstr = Fm_pcstr.replace(']','}')
                Fm_pcstr = Fm_pcstr.replace('"','')
                self.start_dict['Fm_pc'] = Fm_pcstr

            if self.variables['F_pc[2,1]']['value'] != None:
                F_pcarr = []
                for i in range(1,4):
                    cmf = []
                    for j in range(1,len(self.compound_names)+1):
                        cmf.append(str(self.variables['F_pc['+str(i)+','+str(j)+']']['value']))
                    F_pcarr.append(cmf)
                F_pcstr = json.dumps(F_pcarr)
                F_pcstr = F_pcstr.replace('[','{')
                F_pcstr = F_pcstr.replace(']','}')
                F_pcstr = F_pcstr.replace('"','')
                self.start_dict['F_pc'] = F_pcstr

            if self.variables['MW_p[2]']['value'] != None:
                MW_pArr = []
                for i in range(1,4):
                    MW_pArr.append(self.variables['MW_p['+str(i)+']']['value'])
                MW_pStr = json.dumps(MW_pArr)
                MW_pStr = MW_pStr.replace('[','{')
                MW_pStr = MW_pStr.replace(']','}')
                MW_pStr = MW_pStr.replace('"','')
                self.start_dict['MW_p'] = MW_pStr

            if self.variables['F_p[2]']['value'] != None:
                F_pArr = []
                for i in range(1,4):
                    F_pArr.append(self.variables['F_p['+str(i)+']']['value'])
                F_pStr = json.dumps(F_pArr)
                F_pStr = F_pStr.replace('[','{')
                F_pStr = F_pStr.replace(']','}')
                F_pStr = F_pStr.replace('"','')
                self.start_dict['F_p'] = F_pStr

            if self.variables['Cp_p[2]']['value'] != None:
                Cp_pArr = []
                for i in range(1,4):
                    Cp_pArr.append(self.variables['Cp_p['+str(i)+']']['value'])
                Cp_pStr = json.dumps(Cp_pArr)
                Cp_pStr = Cp_pStr.replace('[','{')
                Cp_pStr = Cp_pStr.replace(']','}')
                Cp_pStr = Cp_pStr.replace('"','')
                self.start_dict['Cp_p'] = Cp_pStr

            if self.variables['H_p[2]']['value'] != None:
                H_pArr = []
                for i in range(1,4):
                    H_pArr.append(self.variables['H_p['+str(i)+']']['value'])
                H_pStr = json.dumps(H_pArr)
                H_pStr = H_pStr.replace('[','{')
                H_pStr = H_pStr.replace(']','}')
                H_pStr = H_pStr.replace('"','')
                self.start_dict['H_p'] = H_pStr


            if self.variables['S_p[2]']['value'] != None:
                S_pArr = []
                for i in range(1,4):
                    S_pArr.append(self.variables['S_p['+str(i)+']']['value'])
                S_pStr = json.dumps(S_pArr)
                S_pStr = S_pStr.replace('[','{')
                S_pStr = S_pStr.replace(']','}')
                S_pStr = S_pStr.replace('"','')
                self.start_dict['S_p'] = S_pStr

            if self.variables['Fm_p[2]']['value'] != None:
                Fm_pArr = []
                for i in range(1,4):
                    Fm_pArr.append(self.variables['Fm_p['+str(i)+']']['value'])
                Fm_pStr = json.dumps(Fm_pArr)
                Fm_pStr = Fm_pStr.replace('[','{')
                Fm_pStr = Fm_pStr.replace(']','}')
                Fm_pStr = Fm_pStr.replace('"','')
                self.start_dict['Fm_p'] = Fm_pStr

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type,exc_tb.tb_lineno)
            print(e)
            print('error')

    def OM_Flowsheet_Initialize(self,addedcomp):
        self.OM_data_init = ''
        self.OM_data_init = self.OM_data_init + ("model ms"+str(self.count)+"\n")
        self.OM_data_init = self.OM_data_init + ("extends Simulator.Streams.MaterialStream;\n" )
        self.OM_data_init = self.OM_data_init + ("extends Simulator.Files.ThermodynamicPackages."+self.thermo_package+";\n")
        self.OM_data_init = self.OM_data_init + ("end ms"+str(self.count)+";\n")
        comp_count = len(addedcomp)
       
        self.OM_data_init = self.OM_data_init + "ms"+str(self.count) +" " + self.name +"(Nc = " + str(comp_count)
        self.OM_data_init = self.OM_data_init + ",C = {"
        C = str(addedcomp).strip('[').strip(']')
        C = C.replace("'","")
        self.OM_data_init = self.OM_data_init + C + "},"
        
        self.OM_data_init = self.OM_data_init[:-1]
        self.OM_data_init = self.OM_data_init + ');\n'        
        return self.OM_data_init

    def OM_Flowsheet_Equation(self,addedcomp,method):
        self.OM_data_eqn = ''
        self.comp_count = len(addedcomp)
        if method == 'Eqn':
            self.eqn_dict = {}
            self.get_min_eqn_values()
        if method == 'SM':
            self.eqn_dict = {}
            self.get_min_eqn_values()
           
        for key,value in self.eqn_dict.items():
            self.OM_data_eqn = self.OM_data_eqn + self.name + '.'+ key + ' = ' + str(value) + ';\n'
        return self.OM_data_eqn
    
    def disableInputDataTab(self,dockwidget):
        #setting the value of input data tab in dock widget and disabling them
        dockwidget.comboBox.setDisabled(True)
        dockwidget.input_dict['P'].setText(str(round(float(self.variables['P']['value']),2)))
        dockwidget.input_dict['P'].setDisabled(True)
        dockwidget.input_dict['T'].setText(str(round(float(self.variables['T']['value']),2)))
        dockwidget.input_dict['T'].setDisabled(True)
        dockwidget.input_dict['MolFlow'].setText(str(round(float(self.variables['F_p[1]']['value']),2)))
        dockwidget.input_dict['MolFlow'].setDisabled(True)
        dockwidget.cbTP.setCurrentText(str(self.thermo_package))
        dockwidget.cbTP.setDisabled(True)
        dockwidget.pushButton_2.setDisabled(True)
        for index,k in enumerate(dockwidget.x_pclist):
            k.setText(str(round(float(self.variables['x_pc[1,'+ str(index+1)+']']['value']),2)))
            k.setDisabled(True)
