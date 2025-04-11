import json
import os
import streamlit as st
from helper.data_field import get_analyst_response
import time

st.set_page_config(layout="centered") # <--- Add this line

def display_outputs():
    client_name = "RMX Creatives"
    overview = f"""**{client_name}** is a financial services company based in Auckland, New Zealand, specializing in providing quick and flexible loan solutions for businesses and individuals. Represented by Paul Stone, LoansOne has enlisted ShoreMarketing to perform a deep dive into their digital footprint to have a view of the holistic status of their digital properties and determine how each property can play part in implementing a stronger digital marketing plan.\n
The Digital Marketing Footprint consists of deep-dive research by ShoreMarketing specialists to help the business leaders of LoansOne understand the effectiveness of their existing digital initiatives with the view of giving them an insight to developing a strategy and effectively allocating business resources to digital properties that will give them the best results.\n
This document represents the results of our audit of LoansOne’s digital marketing and management practices. Our audit covered reviews of key digital areas: Website and Tools, PPC/SEM, SEO, Social Media, and Market Places."""
    website_and_tools_data = get_analyst_response("Website and Tools Analyst")
    # seo = data_field("SEO")
    # social_media = data_field("Social Media")

    # (off_page_thread)
    # (on_page_thread)
    # (website_and_tools_thread)
    # (seo_thread)
    # (social_media_thread)
    st.markdown("## Digital Marketing Audit")
    st.markdown(f"### {client_name}")
    
    st.markdown("## DIGITAL FOOTPRINT OVERVIEW")
    st.markdown(f"{overview}")
    
    st.markdown("## WEBSITE AND TOOLS")
    st.markdown(f"""In today’s digital age, scaling a business is simply impossible without a website. Websites primarily serve as the center for all online conversions, which makes it equally important to guarantee that all pages are optimised to educate all traffic about the brand and ultimately to usher them into conversion. \n
In line with this, we have looked into the technology used by **{client_name}** as well as the different digital channels currently in place to see how they are structured and how they are performing.""")
    
    # --- Start: Loop and display data as Markdown table ---
    if website_and_tools_data:
        try:
            # If get_analyst_response returns a JSON string, parse it:
            # parsed_data = json.loads(website_and_tools_data)

            # If get_analyst_response returns a Python list/dict directly:
            parsed_data = website_and_tools_data

            # Check if the parsed data is a list (expected format for a table)
            if isinstance(parsed_data, list):
                # Create Markdown table header
                markdown_table = "| Category | Current Footprint | Best of Breed Solution |\n"
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
                 st.write("Website and Tools Analysis Result (Summary):")
                 # You might want to display dictionary data differently
                 st.json(parsed_data) # Example: Display as JSON
            else:
                 st.warning("Website and Tools data is not in the expected list format.")
                 st.write(parsed_data) # Show the raw data

        except json.JSONDecodeError:
            st.error("Error: Could not parse the Website and Tools data as JSON.")
            st.text(website_and_tools_data) # Show the raw string data
        except AttributeError:
             st.error("Error: Could not find expected keys ('category', 'current_footprint', 'best_of_breed_solution') in the data.")
             st.write(parsed_data) # Show the data that caused the error
        except Exception as e:
            st.error(f"An unexpected error occurred while processing Website and Tools data: {e}")
            st.write(website_and_tools_data) # Show the raw data
    else:
        st.warning("No data retrieved for Website and Tools analysis.")
    # --- End: Loop and display data ---
    

if st.button("Back to Dashboard"):
        st.switch_page("pages/home.py")
display_outputs()