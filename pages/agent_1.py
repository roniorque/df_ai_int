import os
from helper.desc import Analysts, Analysts_Description, Data_Source
from classes.Off_Page import SeoOffPageAnalyst

# SPECIFY API URL & ANALYST NAME
start = SeoOffPageAnalyst(os.getenv('MODEL_Off_Page_Analyst'))

