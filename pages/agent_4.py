import os
from classes.Social_Media import SocialMediaAnalyst
from helper.desc import Analysts, Analysts_Description, Data_Source

# SPECIFY API URL & ANALYST NAME
start = SocialMediaAnalyst(os.getenv('MODEL_Social_Media_Analyst'), Analysts['Analyst 4'], Data_Source['Analyst_Src 4'],Analysts_Description['Analyst_Desc 4'])

