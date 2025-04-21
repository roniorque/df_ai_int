import json
import os
import streamlit as st
from helper.data_field import get_analyst_response, data_field, get_marketplace_response
import time

st.set_page_config(layout="centered") 

def write_client_footprint():

    try:
        web = get_analyst_response("Website and Tools Analyst")
        result_web = {item["category"]: item["current_footprint"] for item in web}
    except TypeError:
        result_web = None

    try:
        seo = get_analyst_response("SEO Analyst")
        seo = {item["category"]: item["current_footprint"] for item in seo}
    except TypeError:
        seo = None

    try:
        socmed = get_analyst_response("Social Media Analyst")
        socmed = {item["category"]: item["current_footprint"] for item in socmed}
    except TypeError:
        socmed = None

    def safe_get(data, key):
        value = data.get(key)
        return value if value else "N/A"
    
    markdown_table = "| Source/Channel | Current KPI |\n"
    markdown_table += "|---|---|\n"
    markdown_table += f"| Website Health Score | {safe_get(result_web, 'website_overall_health_score')} |\n"
    markdown_table += f"| Organic Traffic to the Website | {safe_get(seo, 'organic_traffic')} |\n"
    markdown_table += f"| Paid Traffic to the Website | {safe_get(seo, 'paid_traffic')} |\n"
    markdown_table += f"| Referral Traffic to the Website | {safe_get(seo, 'referral_traffic')} |\n"
    markdown_table += f"| Email Traffic to the Website | N/A |\n"
    markdown_table += f"| Direct Traffic to the Website | {safe_get(seo, 'direct_traffic')} |\n"
    markdown_table += f"| Social Traffic to the Website | N/A |\n"
    markdown_table += f"| Display Traffic to the Website | N/A |\n"
    markdown_table += f"| Email Database | N/A |\n"
    markdown_table += f"| Facebook Followers | {safe_get(socmed, 'facebook_followers')} |\n"
    markdown_table += f"| Twitter Followers | {safe_get(socmed, 'twitter_followers')} |\n"
    markdown_table += f"| Instagram Followers | {safe_get(socmed, 'instagram_followers')} |\n"
    markdown_table += f"| Linkedin Followers | {safe_get(socmed, 'linkedin_followers')} |\n"
    markdown_table += f"| Google My Business | N/A |\n"
    markdown_table += f"| # of Keywords Ranking in Top 10 | {safe_get(seo, 'keyword_ranking_in_top_10')} |\n"
    markdown_table += f"| # of Keywords Ranking in Top 100 | {safe_get(seo, 'keyword_ranking_in_top_100')} |\n"
    
    return markdown_table
    
def write_snapshot(data):
     
    if data:
        try:
            
            parsed_data = data
            
            if isinstance(parsed_data, list):
                # Create Markdown table header
                markdown_table = "| Channel | Status | Requirements | What's Needed to Deliver |\n"
                markdown_table += "|---|---|---|---|\n"

                # Loop through the list of dictionaries
                for item in parsed_data:
                    # Use .get() for safety in case keys are missing
                    channel = item.get('channel', 'N/A')
                    status = item.get('status', 'N/A')
                    requirements = item.get('requirements', 'N/A')
                    deliver = item.get('deliver', 'N/A')

                    # Add a row to the Markdown table string
                    # Replace underscores with spaces and apply title case to category
                                       # Replace underscores with spaces first
                    channel_temp = channel.replace('_', ' ')

                    # Apply title case if there are multiple words, otherwise uppercase
                    if ' ' in channel_temp: # Check for spaces directly
                        channel_formatted = channel_temp.title()
                    else:
                        channel_formatted = channel_temp.upper() # Use upper() instead of upper_case()
                   

                    markdown_table += f"| {channel_formatted} | {status} | {requirements} | {deliver} |\n"
                    

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
            st.text(data) # Show the raw string data
        except AttributeError:
             st.error("Error: Could not find expected keys ('channel', 'status', 'requirements', 'deliver') in the data.")
             st.write(parsed_data) # Show the data that caused the error
        except Exception as e:
            st.error(f"An unexpected error occurred while processing data: {e}")
            st.write(data) # Show the raw data
    else:
        st.warning("No data retrieved for analysis.")
    # --- End: Loop and display data ---
        
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

def seo_on_page_table(df_data):
     
    if df_data:
        try:
            
            parsed_data = df_data
            
            if isinstance(parsed_data, list):
                # Create Markdown table header
                markdown_table = "| Element | Description | Remarks |\n"
                markdown_table += "|---|---|---|\n"

                # Loop through the list of dictionaries
                for item in parsed_data:
                    # Use .get() for safety in case keys are missing
                    element = item.get('elements', 'N/A')
                    description = item.get('description', 'Static information')
                    remarks = item.get('remarks', 'N/A')

                    # Add a row to the Markdown table string
                    # Replace underscores with spaces and apply title case to element
                    element_formatted = element.replace('_', ' ').title()
                    description_formatted = description.replace('_', ' ')
                    remarks_formatted = remarks.replace('_', ' ')

                    markdown_table += f"| {element_formatted} | {description_formatted} | {remarks_formatted} |\n"
                    

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
            st.text(df_data) # Show the raw string data
        except AttributeError:
             st.error("Error: Could not find expected keys ('category', 'current_footprint', 'best_of_breed_solution') in the data.")
             st.write(parsed_data) # Show the data that caused the error
        except Exception as e:
            st.error(f"An unexpected error occurred while processing data: {e}")
            st.write(df_data) # Show the raw data
    else:
        st.warning("No data retrieved for analysis.")
    # --- End: Loop and display data ---
    
def display_outputs():
    client_name = data_field("Client Name")
    client_website = data_field("Client Website")
    
    
    
    overview = get_analyst_response("DF Overview Analyst")    
    
    st.markdown("# Digital Marketing Audit")
    st.markdown(f"for: **{client_name} ({client_website})**")
    st.write("")
    st.write("")
    
    st.markdown("#### Table of Contents")
    st.markdown("""<ul><li><a href='#digital-footprint-overview'>Digital Footprint Overview</a></li>
    <li><a href='#executive-summary'>Executive Summary</a></li>
    <li><a href='#client-footprint'>Client Footprint</a></li>
    <li><a href='#snapshot-by-channel'>Snapshot by Channel</a></li>
    <li><a href='#website-and-tools'>Website and Tools</a></li>
    <li><a href='#search-engine-marketing'>Search Engine Marketing</a></li>
    <li><a href='#search-engine-optimization'>Search Engine Optimization</a></li>
    <li><a href='#social-media'>Social Media</a></li>
    <li><a href='#content'>Content</a></li>
    <li><a href='#market-place'>Market Place</a></li>
    <li><a href='#target-market'>Target Market</a></li>
    <li><a href='#desired-outcomes'>Desired Outcomes</a></li>
    </ul>""", unsafe_allow_html=True)
    
    st.markdown("---")  
    
    st.write("")
    st.write("")
    st.markdown("### DIGITAL FOOTPRINT OVERVIEW")
    st.markdown(f"{overview}")
    st.markdown("---")
    st.markdown("### Executive Summary")
    st.markdown(get_analyst_response("Executive Summary"))
    st.markdown("---")
    
    st.markdown("### CLIENT FOOTPRINT")
    st.markdown(write_client_footprint())
    st.markdown(
        """
        <style>
        table{
            width: 100%;
        }
            
            """,
            unsafe_allow_html=True,
    )
    st.markdown("---")    
    
    st.markdown("### SNAPSHOT BY CHANNEL")    
    write_snapshot(get_analyst_response("Snapshot Analyst")) #write_snapshot
    st.markdown("---")
    
    st.markdown("## AUDITS PER CHANNEL")
    st.markdown("### WEBSITE AND TOOLS")
    st.markdown(f"""In today’s digital age, scaling a business is simply impossible without a website. Websites primarily serve as the center for all online conversions, which makes it equally important to guarantee that all pages are optimised to educate all traffic about the brand and ultimately to usher them into conversion. \n
In line with this, we have looked into the technology used by **{client_name}** as well as the different digital channels currently in place to see how they are structured and how they are performing.""")
    
    # Write W&T Table
    website_and_tools_data = get_analyst_response("Website and Tools Analyst")
    write_table(website_and_tools_data)
    
    st.markdown("<a href='#top'>Go to top</a>", unsafe_allow_html=True)
    st.markdown("---")
   
    st.markdown("### SEARCH ENGINE MARKETING/PPC")
    st.markdown(f"""Search engine marketing, or SEM, is one of the most effective ways to grow a business in an increasingly competitive industry such as solar energy. This is one of the easiest way to be seen by the market almost instantly - but with the certain cost per user clicks. \n
With several businesses out there all vying for the same eyeballs, it’s never been more important to advertise online, and search engine marketing is the most effective way to promote need-based, high-investment products and services such as solar energy services.\n
Currently, {client_name} has already explored numerous online advertising. Its competitors are also experienced in PPC in multiple platforms. """)
    
    # Write SEM Table
    sem_data = get_analyst_response("SEM/PPC Analyst")
    write_table(sem_data)
    
    st.markdown("<a href='#top'>Go to top</a>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### SEARCH ENGINE OPTIMIZATION")
    st.markdown(f"""The purpose of Search Engine Optimization (SEO) is to strategically rearrange the website’s pages, attributes, content, and structure so that the website appears as high as possible in the results list displayed by search engines like Google, Bing, and Yahoo! when certain queries are entered by an internet user. Since high ranking positions are generally earned and worked for, ranking on the first page promotes trust between you and the search engine as well as to ultimately receive organic visibility with your users.\n 
There are two types of SEO based on where the optimization is implemented: On-page SEO (which refers to any type of optimization done within the website) and Off-page SEO (which is often called Link Building or Link Acquisition – the process of getting more “votes” for the website through other domains). Both are essential in increasing a website’s visibility in search results pages and in ranking for more business-related keywords. """)
    
    # Write SEO Table
    seo_data = get_analyst_response("SEO Analyst")
    write_table(seo_data)
    
    st.markdown("<a href='#top'>Go to top</a>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Write On Page Table
    st.markdown("### ON-PAGE OPTIMIZATION")
    on_page_data = get_analyst_response("On Page Analyst")
    seo_on_page_table(on_page_data)
    
    st.markdown("<a href='#top'>Go to top</a>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Write Off Page Table
    st.markdown("### OFF PAGE OPTIMIZATION")
    on_page_data = get_analyst_response("SEO Off Page Analyst")
    seo_on_page_table(on_page_data)
    
    st.markdown("<a href='#top'>Go to top</a>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Write SocMed Table
    st.markdown("### SOCIAL MEDIA")
    st.markdown(f"""Social Media Marketing for the B2B industry is tricky. While B2C businesses can easily have millions of fans through social media, B2B lead generation such as {client_name} sources from a significantly smaller market.
    
Regardless, it is still a great channel worth investing to improve a business’ lead generation if handled correctly. {client_name}, along with its competitors, are found to be using different social media platforms to extend their brand presence. """)
    social_media_data = get_analyst_response("Social Media Analyst")
    write_table(social_media_data)
    
    st.markdown("<a href='#top'>Go to top</a>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Write SocMed Table
    st.markdown("### CONTENT")
    st.markdown(f"""Content is king in digital marketing. People log into the internet to look for and consume information in different formats: text-based, video, audio, or image. Content is what help businesses establish their expertise in the industry, convert leads into customers, guide their customers through their sales funnel, and build relationships with their customers. """)
    content_data = get_analyst_response("Content Analyst")
    write_table(content_data)
    st.markdown("<a href='#top'>Go to top</a>", unsafe_allow_html=True)
    st.markdown("---")

    # if (get_analyst_response("Marketplace Analyst")):
    #     st.markdown("### MARKET PLACE")
    #     st.table(get_analyst_response("Marketplace Analyst"))
    #     st.markdown("<a href='#top'>Go to top</a>", unsafe_allow_html=True)
    #     st.markdown("---")
    
    
    st.markdown("## OTHER INFORMATION")
    st.markdown("### DIGITAL MARKETING APPROACH: CUSTOMER CENTRIC INBOUND MARKETING")
    st.markdown(f"""Digital Marketing is often called in-bound marketing in a sense that it is not intrusive: a person must search for the information before the marketing stimulus is served to them. Unlike the traditional offline marketing which is more brand-centric in style and intrusive (they are served to you even though you did not intend to see the marketing stimulus), digital marketing is customer-centric: it takes into account the needs, thoughts, and considerations of the customer in all stages in the sales funnel while strategically serving them the appropriate content at the right time, at the right frequency, and through the correct channel. We suggest that {client_name} looks into the details below with the view of understanding where the brand’s footing is in some stages in their customer’s decision and buying journey. """)
    
    
    
    target_market_data = get_analyst_response("Target Market Analyst")
    st.markdown("##### TARGET MARKET")
    st.write(target_market_data['target_market'])
    
    st.markdown("##### PRODUCT/SERVICE DEMOGRAPHICS")
    st.write(target_market_data['demographics'])
    
    st.markdown("##### MARKETING MESSAGE SUMMARY")
    st.write(target_market_data['summary'])
    
    st.markdown("##### WHAT IS THE DESIRED OUTCOMES OF DIGITAL MARKETING?")
    st.markdown(get_analyst_response("Desired Outcomes Analyst"))
    
    st.markdown("##### WHAT IS THE PULL-THROUGH OFFER?")
    pull_through_data = get_analyst_response("Pull through offers Analyst")
    st.write(pull_through_data)
    
    
    st.markdown("##### WEBSITE AUDIENCE ACQUISITION")
    website_audience_data = get_analyst_response("Website Audience Acquisition")
    st.write(website_audience_data)
    
    #LLD/PM/LN
    lld_data = get_analyst_response("LLD/PM/LN Analyst")
    st.markdown("##### LEAD LIST DEVELOPMENT")
    st.write(lld_data.get('lead_list_development', None))
    
    st.markdown("##### PROSPECTING MECHANISM")
    st.write(lld_data.get('prospecting_mechanism', None))
    
    st.markdown("##### LEAD NURTURING")
    st.write(lld_data.get('lead_nurturing', None))
    
    st.markdown("<a href='#top'>Go to top</a>", unsafe_allow_html=True)
    st.markdown("---")
    
    
    st.markdown("#### CONTENT - PROCESS AND ASSETS")
    st.write(f"""Content is king in digital marketing. People log into the internet to look for and consume information in different formats: text-based, video, audio, or image. Content is what help businesses establish their expertise in the industry, convert leads into customers, guide their customers through their sales funnel, and build relationships with their customers. \n
We have evaluated the process of content development strategy and existing content assets of {client_name} based on how they serve clients throughout the customer journey. """)
    
    
    pna_data = get_analyst_response("Content - Process and Assets Analyst")
    if pna_data:
        st.markdown("##### AWARENESS STAGE")
        st.write(pna_data.get('awareness_stage', 'N/A'))
        st.markdown("##### CONSIDERATION STAGE")
        st.write(pna_data.get('consideration_stage', 'N/A'))
        st.markdown("##### DECISION STAGE")
        st.write(pna_data.get('decision_stage', 'N/A'))
        
    else:
        st.markdown("##### AWARENESS STAGE")
        st.write(None)
        st.markdown("##### CONSIDERATION STAGE")
        st.write(None)
        st.markdown("##### DECISION STAGE")
        st.write(None)
        
    
    st.markdown("<a href='#top'>Go to top</a>", unsafe_allow_html=True)
    st.markdown("---")       
    
    
    conversion = get_analyst_response("Conversion Analyst")
    st.markdown("#### CONVERSION –  ACTIVATION OF VISITORS")
    
    if conversion:
        st.markdown("##### AWARENESS TO TRAFFIC")
        st.write(conversion.get('awareness_to_traffic', 'N/A'))
        
        st.markdown("##### TRAFFIC TO LEAD CONVERSION")
        st.write(conversion.get('traffic_to_lead', 'N/A'))
        
        st.markdown("##### LEAD TO SALES CONVERSION")
        st.write(conversion.get('lead_to_sales', 'N/A'))
        
        st.markdown("##### CONVERSION TO BRAND LOYALTY")
        st.write(conversion.get('conversion_to_brand', 'N/A'))
    else:
        st.markdown("##### AWARENESS TO TRAFFIC")
        st.write(None)
        st.markdown("##### TRAFFIC TO LEAD CONVERSION")
        st.write(None)
        st.markdown("##### LEAD TO SALES CONVERSION")
        st.write(None)
        st.markdown("##### CONVERSION TO BRAND LOYALTY")
        st.write(None)
    
    
    conversion = get_analyst_response("Connection Analyst")
    st.markdown("##### CONNECTION OF ALL ONLINE AND OFFLINE TOUCH POINTS")
    st.write(conversion)
    
    st.markdown("<a href='#top'>Go to top</a>", unsafe_allow_html=True)
    


st.markdown("<div id='top'></div>", unsafe_allow_html=True);    
if st.button("Back to Dashboard", icon="🏠"):
        st.switch_page("pages/home.py")
display_outputs()