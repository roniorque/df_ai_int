import os
from classes.Lead_List import LeadListAnalyst
from helper.desc import Analysts, Analysts_Description, Data_Source

# SPECIFY API URL & ANALYST NAME
start = LeadListAnalyst(os.getenv('Model_Lead_list_Analyst'), Analysts['Analyst 5'], Data_Source['Analyst_Src 5'],Analysts_Description['Analyst_Desc 5'])

