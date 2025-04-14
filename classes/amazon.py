import streamlit as st
from dotenv import load_dotenv
from helper.telemetry import collect_telemetry
from helper.upload_File import uploadFile
from helper.button_behaviour import hide_button

class Amazon:
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
        if 'product_title_amazon' not in st.session_state:
            st.session_state['product_title_amazon'] = ''
        if 'images_amazon' not in st.session_state:
            st.session_state['images_amazon'] = ''
        if 'bullet_points_amazon' not in st.session_state:
            st.session_state['bullet_points_amazon'] = ''
        if 'product_description_amazon' not in st.session_state:
            st.session_state['product_description_amazon'] = ''

    def process(self):
        session = st.session_state.analyze
        if (self.product_title_amazon or self.images_amazon or self.bullet_points_amazon or self.product_description_amazon) and session == 'clicked':
                    try:
                        product_title_amazon = ""
                        images_amazon = ""
                        bullet_points_amazon = ""
                        product_description_amazon = ""

                        with st.spinner('Aamzon...', show_time=True):
                                st.write('')
                                # INITIALIZING SESSIONS
                                #combined_text += f"Client Summary: {st.session_state.nature}\n"
                                try:
                                    product_title_amazon += f"\nProduct Title: {self.product_title_amazon}"
                                except KeyError:
                                    pass
                                try:
                                    images_amazon += f"\nImages: {self.images_amazon}"
                                except KeyError:
                                    pass
                                try:
                                    bullet_points_amazon += f"\nBullet Points: {self.bullet_points_amazon}"
                                except KeyError:
                                    pass
                                try:
                                    product_description_amazon += f"\nProduct Description: {self.product_description_amazon}"
                                except KeyError:
                                    pass
                                
                                # OUTPUT FOR SEO ANALYST
                                #payload_txt = {"question": combined_text}
                                #result = self.request_model(payload_txt)
                                
                                #end_time = time.time()
                                #time_lapsed = end_time - start_time
                                
                                debug_info_product_title_amazon = {'data_field' : 'Product Title - Amazon', 'result': self.product_title_amazon}
                                debug_info_images_amazon = {'data_field' : 'Images - Amazon', 'result': self.images_amazon}
                                debug_info_bullet_points_amazon = {'data_field' : 'Bullet Points - Amazon', 'result': self.bullet_points_amazon}
                                debug_product_description_amazon = {'data_field' : 'Product Description - Amazon', 'result': self.product_description_amazon}

                                '''
                                debug_info = {
                                    #'analyst': self.analyst_name,
                                    'url_uuid': self.model_url.split("-")[-1],
                                    'time_lapsed': time_lapsed,
                                    'payload': payload_txt,
                                    'result': result,
                                }
                                '''
                                if self.product_title_amazon:
                                    st.session_state['product_title_amazon'] = 'uploaded'
                                    collect_telemetry(debug_info_product_title_amazon)
                                if self.images_amazon:
                                    st.session_state['images_amazon'] = 'uploaded'
                                    collect_telemetry(debug_info_images_amazon)
                                if self.bullet_points_amazon:
                                    st.session_state['bullet_points_amazon'] = 'uploaded'
                                    collect_telemetry(debug_info_bullet_points_amazon)
                                if self.product_description_amazon:
                                    st.session_state['product_description_amazon'] = 'uploaded'
                                    collect_telemetry(debug_product_description_amazon)
                                

                                st.session_state['analyzing'] = False 
                    except AttributeError:
                        st.info("Please upload CSV or PDF files first.")
                        hide_button() 

    def row1(self):
            self.product_title_amazon = st.text_input("Product Title - Amazon:", placeholder='Enter Product Title')
            self.images_amazon = st.text_input("Images - Amazon:", placeholder='Enter Images')
            self.bullet_points_amazon = st.text_input("Bullet Points - Amazon:", placeholder='Enter Bullet Points')
            self.product_description_amazon = st.text_input("Product Description - Amazon:", placeholder='Enter Product Description')

            self.process()
            
if __name__ == "__main__":
    st.set_page_config(layout="wide")

upload = uploadFile()
