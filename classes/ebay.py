import streamlit as st
from dotenv import load_dotenv
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button

class eBay:
    def __init__(self, model_url):
        self.file_dict = {}
        self.model_url = model_url
        #self.analyst_name = analyst_name
        #self.data_src = data_src
        #self.analyst_description = analyst_description
        self.initialize()
        self.row1()

    def initialize(self):
        # FOR ENV
        load_dotenv()
        '''
        # AGENT NAME
        st.header(self.analyst_name)

        # EVALUATION FORM LINK
        url = os.getenv('Link')
        st.write('Evaluation Form: [Link](%s)' % url)

        # RETURN BUTTON
        try:
            if st.button("Return", type='primary'):
                st.switch_page("./pages/home.py")
        except Exception:
            pass

        if 'product_title_ebay' not in st.session_state:
            st.session_state['product_title_ebay'] = ''
        if 'category_ebay' not in st.session_state:
            st.session_state['category_ebay'] = ''
        if 'images_ebay' not in st.session_state:
            st.session_state['images_ebay'] = ''
        if 'product_description_ebay' not in st.session_state:
            st.session_state['product_description_ebay'] = ''
        '''
        if 'ebay_marketplace_questionnaires' not in st.session_state:
            st.session_state['ebay_marketplace_questionnaires'] = ''

    def process(self):
        session = st.session_state.analyze
        if (self.ebay_marketplace_questionnaires) and session == 'clicked':
                    try:
                        #product_title_ebay = ""
                        #category_ebay = ""
                        #images_ebay = ""
                        #product_description_ebay = ""
                        ebay_marketplace_questionnaires = ""

                        with st.spinner('eBay...', show_time=True):
                                st.write('')
                                # INITIALIZING SESSIONS
                                #combined_text += f"Client Summary: {st.session_state.nature}\n"
                                '''
                                try:
                                    product_title_ebay += f"\nProduct Title: {self.product_title_ebay}"
                                except KeyError:
                                    pass
                                try:
                                    category_ebay += f"\nImages: {self.category_ebay}"
                                except KeyError:
                                    pass
                                try:
                                    images_ebay += f"\nBullet Points: {self.images_ebay}"
                                except KeyError:
                                    pass
                                try:
                                    product_description_ebay += f"\nProduct Description: {self.product_description_ebay}"
                                except KeyError:
                                    pass
                                '''
                                try:
                                    ebay_marketplace_questionnaires += f"Marketplace Questionnaires - eBay: {self.ebay_marketplace_questionnaires}"
                                except KeyError:
                                    pass
                                
                                # OUTPUT FOR SEO ANALYST
                                #payload_txt = {"question": combined_text}
                                #result = self.request_model(payload_txt)
                                
                                #end_time = time.time()
                                #time_lapsed = end_time - start_time
                                
                                #debug_info_product_title_ebay = {'data_field' : 'Product Title - eBay', 'result': self.product_title_ebay}
                                #debug_category_ebay = {'data_field' : 'Category - eBay', 'result': self.category_ebay}
                                #debug_images_ebay = {'data_field' : 'Images - eBay', 'result': self.images_ebay}
                                #debug_product_description_ebay = {'data_field' : 'Product Description - eBay', 'result': self.product_description_ebay}

                                debug_ebay_marketplace_questionnaires = {'data_field' : 'Marketplace Questionnaires - eBay', 'result': self.ebay_marketplace_questionnaires}

                                '''
                                debug_info = {
                                    #'analyst': self.analyst_name,
                                    'url_uuid': self.model_url.split("-")[-1],
                                    'time_lapsed': time_lapsed,
                                    'payload': payload_txt,
                                    'result': result,
                                }
                                
                                if self.product_title_ebay:
                                    st.session_state['product_title_ebay'] = 'uploaded'
                                    collect_telemetry(debug_info_product_title_ebay)
                                if self.category_ebay:
                                    st.session_state['category_ebay'] = 'uploaded'
                                    collect_telemetry(debug_category_ebay)
                                if self.images_ebay:
                                    st.session_state['images_ebay'] = 'uploaded'
                                    collect_telemetry(debug_images_ebay)
                                if self.product_description_ebay:
                                    st.session_state['product_description_ebay'] = 'uploaded'
                                    collect_telemetry(debug_product_description_ebay)
                                '''
                                if self.ebay_marketplace_questionnaires:
                                    st.session_state['ebay_marketplace_questionnaires'] = 'uploaded'
                                    collect_telemetry(debug_ebay_marketplace_questionnaires)

                                st.session_state['analyzing'] = False 
                    except AttributeError:
                        st.info("Please upload CSV or PDF files first.")
                        hide_button() 

    def row1(self):
            #self.product_title_ebay = st.text_input("Product Title - eBay:", placeholder='Enter Product Title')
            #self.category_ebay = st.text_input("Images - eBay:", placeholder='Enter Images')
            #self.images_ebay = st.text_input("Bullet Points - eBay:", placeholder='Enter Bullet Points')
            #self.product_description_ebay = st.text_input("Product Description - eBay:", placeholder='Enter Product Description')

            self.ebay_marketplace_questionnaires = st.text_area(
                                                        "Marketplace Questionnaires - eBay:",
                                                        "Product Title:\n"
                                                        "a. Is the title within the 80-character limit?\n"
                                                        "b. Does the title include important details (e.g., brand, color, quantity, compatibility)?\n"
                                                        "c. Are search keywords used effectively in the title?\n"
                                                        "d. Other Remarks:\n\n"
                                                        "Category:\n"
                                                        "a. Is the product listed under the correct eBay category?\n"
                                                        "b. Other Remarks:\n\n"
                                                        "Images:\n"
                                                        "a. Are the product images on a white background?\n"
                                                        "b. Are there any text, logos, or watermarks on the images?\n"
                                                        "c. Are the images high-resolution and zoomable?\n"
                                                        "d. Other Remarks:\n\n"
                                                        "Product Description:\n"
                                                        "a. Is the product description complete and detailed?\n"
                                                        "b. Are bullet points used to highlight features and benefits?\n"
                                                        "c. Are there images embedded in the description?\n"
                                                        "d. Are there any technical issues (e.g., broken images, loading errors)?\n"
                                                        "e. Is there consistent keyword usage in the description?\n"
                                                        "f. Other Remarks:",
                                                        height=600
                                                    )
            self.process()
            
if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
