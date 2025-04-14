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
        '''
        if 'product_title_ebay' not in st.session_state:
            st.session_state['product_title_ebay'] = ''
        if 'category_ebay' not in st.session_state:
            st.session_state['category_ebay'] = ''
        if 'images_ebay' not in st.session_state:
            st.session_state['images_ebay'] = ''
        if 'product_description_ebay' not in st.session_state:
            st.session_state['product_description_ebay'] = ''

    def process(self):
        session = st.session_state.analyze
        if (self.product_title_ebay or self.category_ebay or self.images_ebay or self.product_description_ebay) and session == 'clicked':
                    try:
                        product_title_ebay = ""
                        category_ebay = ""
                        images_ebay = ""
                        product_description_ebay = ""

                        with st.spinner('eBay...', show_time=True):
                                st.write('')
                                # INITIALIZING SESSIONS
                                #combined_text += f"Client Summary: {st.session_state.nature}\n"
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
                                
                                # OUTPUT FOR SEO ANALYST
                                #payload_txt = {"question": combined_text}
                                #result = self.request_model(payload_txt)
                                
                                #end_time = time.time()
                                #time_lapsed = end_time - start_time
                                
                                debug_info_product_title_ebay = {'data_field' : 'Product Title - eBay', 'result': self.product_title_ebay}
                                debug_category_ebay = {'data_field' : 'Category - eBay', 'result': self.category_ebay}
                                debug_images_ebay = {'data_field' : 'Images - eBay', 'result': self.images_ebay}
                                debug_product_description_ebay = {'data_field' : 'Product Description - eBay', 'result': self.product_description_ebay}

                                '''
                                debug_info = {
                                    #'analyst': self.analyst_name,
                                    'url_uuid': self.model_url.split("-")[-1],
                                    'time_lapsed': time_lapsed,
                                    'payload': payload_txt,
                                    'result': result,
                                }
                                '''
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
                                

                                st.session_state['analyzing'] = False 
                    except AttributeError:
                        st.info("Please upload CSV or PDF files first.")
                        hide_button() 

    def row1(self):
            self.product_title_ebay = st.text_input("Product Title - eBay:", placeholder='Enter Product Title')
            self.category_ebay = st.text_input("Images - eBay:", placeholder='Enter Images')
            self.images_ebay = st.text_input("Bullet Points - eBay:", placeholder='Enter Bullet Points')
            self.product_description_ebay = st.text_input("Product Description - eBay:", placeholder='Enter Product Description')

            self.process()
            
if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
