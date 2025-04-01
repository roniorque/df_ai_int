import os
from helper.desc import Analysts, Analysts_Description, Data_Source
from classes.Seo_On_Page import SeoOnPageAnalyst

# SPECIFY API URL ANALYST NAME, DATA SOURCE & DESCRIPTION
start = SeoOnPageAnalyst(os.getenv('MODEL_On_Page_Analyst'), Analysts['Analyst 2'], Data_Source['Analyst_Src 2'],Analysts_Description['Analyst_Desc 2'])

