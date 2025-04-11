import json
import os
import streamlit as st
from helper.data_field import get_analyst_response
import time

st.set_page_config(layout="centered") 

def write_table(website_and_tools_data):
     
    if website_and_tools_data:
        try:
            
            parsed_data = website_and_tools_data
            
            if isinstance(parsed_data, list):
                # Create Markdown table header
                markdown_table = "|  | Current Footprint | Best of Breed Solution |\n"
                markdown_table += "|---|---|---|\n"

                # Loop through the list of dictionaries
                for item in parsed_data:
                    # Use .get() for safety in case keys are missing
                    category = item.get('category', 'N/A')
                    current_footprint = item.get('current_footprint', 'N/A')
                    best_of_breed = item.get('best_of_breed_solution', 'N/A')

                    # Add a row to the Markdown table string
                    # Replace underscores with spaces and apply title case to category
                    category_formatted = category.replace('_', ' ').title()
                    current_footprint_formatted = current_footprint.replace('_', ' ')
                    best_of_breed_formatted = best_of_breed.replace('_', ' ')

                    markdown_table += f"| {category_formatted} | {current_footprint_formatted} | {best_of_breed_formatted} |\n"
                    

                # Display the complete Markdown table
                st.markdown(markdown_table)

            # Handle case if data is not a list (e.g., a single dictionary)
            elif isinstance(parsed_data, dict):
                 st.write("Analysis Result (Summary):")
                 # You might want to display dictionary data differently
                 st.json(parsed_data) # Example: Display as JSON
            else:
                 st.warning("data is not in the expected list format.")
                 st.write(parsed_data) # Show the raw data

        except json.JSONDecodeError:
            st.error("Error: Could not parse the data as JSON.")
            st.text(website_and_tools_data) # Show the raw string data
        except AttributeError:
             st.error("Error: Could not find expected keys ('category', 'current_footprint', 'best_of_breed_solution') in the data.")
             st.write(parsed_data) # Show the data that caused the error
        except Exception as e:
            st.error(f"An unexpected error occurred while processing data: {e}")
            st.write(website_and_tools_data) # Show the raw data
    else:
        st.warning("No data retrieved for analysis.")
    # --- End: Loop and display data ---

     
    
def display_outputs():
    client_name = "RMX Creatives"
    overview = f"""**{client_name}** is a financial services company based in Auckland, New Zealand, specializing in providing quick and flexible loan solutions for businesses and individuals. Represented by Paul Stone, LoansOne has enlisted ShoreMarketing to perform a deep dive into their digital footprint to have a view of the holistic status of their digital properties and determine how each property can play part in implementing a stronger digital marketing plan.\n
The Digital Marketing Footprint consists of deep-dive research by ShoreMarketing specialists to help the business leaders of LoansOne understand the effectiveness of their existing digital initiatives with the view of giving them an insight to developing a strategy and effectively allocating business resources to digital properties that will give them the best results.\n
This document represents the results of our audit of LoansOne’s digital marketing and management practices. Our audit covered reviews of key digital areas: Website and Tools, PPC/SEM, SEO, Social Media, and Market Places."""
    
    
    st.markdown("# Digital Marketing Audit")
    st.markdown(f"{client_name}")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("### DIGITAL FOOTPRINT OVERVIEW")
    st.markdown(f"{overview}")
    st.markdown("---")
    st.markdown("### Executive Summary")
    st.markdown(f"Simtech LED's digital footprint reveals significant strengths and areas for improvement that can enhance its competitive positioning in the casino, gaming, and entertainment LED market. The analysis highlights the following key findings and recommendations")
    st.markdown("---")
    
    st.markdown("### CLIENT FOOTPRINT")
    st.markdown(f"A")
    st.markdown("---")    
    
    st.markdown("### SNAPSHOT BY CHANNEL")
    st.markdown(f"A")
    st.markdown("---")
    
    st.markdown("## AUDITS PER CHANNEL")
    st.markdown("### WEBSITE AND TOOLS")
    st.markdown(f"""In today’s digital age, scaling a business is simply impossible without a website. Websites primarily serve as the center for all online conversions, which makes it equally important to guarantee that all pages are optimised to educate all traffic about the brand and ultimately to usher them into conversion. \n
In line with this, we have looked into the technology used by **{client_name}** as well as the different digital channels currently in place to see how they are structured and how they are performing.""")
    
    # Write W&T Table
    website_and_tools_data = get_analyst_response("Website and Tools Analyst")
    write_table(website_and_tools_data)
    
    st.markdown("---")
   
    st.markdown("### SEARCH ENGINE MARKETING/PPC")
    st.markdown(f"""Search engine marketing, or SEM, is one of the most effective ways to grow a business in an increasingly competitive industry such as solar energy. This is one of the easiest way to be seen by the market almost instantly - but with the certain cost per user clicks. \n
With several businesses out there all vying for the same eyeballs, it’s never been more important to advertise online, and search engine marketing is the most effective way to promote need-based, high-investment products and services such as solar energy services.\n
Currently, {client_name} has already explored numerous online advertising. Its competitors are also experienced in PPC in multiple platforms. """)
    
    # Write W&T Table
    sem_data = get_analyst_response("SEM PPC Analyst")
    write_table(sem_data)
    
    st.markdown("---")
    
    st.markdown("### SEARCH ENGINE OPTIMIZATION")
    st.markdown(f"""The purpose of Search Engine Optimization (SEO) is to strategically rearrange the website’s pages, attributes, content, and structure so that the website appears as high as possible in the results list displayed by search engines like Google, Bing, and Yahoo! when certain queries are entered by an internet user. Since high ranking positions are generally earned and worked for, ranking on the first page promotes trust between you and the search engine as well as to ultimately receive organic visibility with your users.\n 
There are two types of SEO based on where the optimization is implemented: On-page SEO (which refers to any type of optimization done within the website) and Off-page SEO (which is often called Link Building or Link Acquisition – the process of getting more “votes” for the website through other domains). Both are essential in increasing a website’s visibility in search results pages and in ranking for more business-related keywords. """)
    
    # Write W&T Table
    seo_data = get_analyst_response("SEO Analyst")
    write_table(seo_data)
    
    st.markdown("---")

if st.button("Back to Dashboard"):
        st.switch_page("pages/home.py")
display_outputs()