import os
from helper.desc import Analysts, Analysts_Description, Data_Source
from classes.Seo import SeoAnalyst

# SPECIFY API URL & ANALYST NAME
start = SeoAnalyst(os.getenv('MODEL_SEO_Analyst'), Analysts['Analyst 3'], Data_Source['Analyst_Src 3'],Analysts_Description['Analyst_Desc 3'])

