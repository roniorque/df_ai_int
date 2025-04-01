import os
from classes.Target_Market import TargetMarketAnalyst
from helper.desc import Analysts, Analysts_Description, Data_Source

# SPECIFY API URL & ANALYST NAME
start = TargetMarketAnalyst(os.getenv('Model_Target_Market_Analyst'), Analysts['Analyst 6'], Data_Source['Analyst_Src 6'],Analysts_Description['Analyst_Desc 6'])

