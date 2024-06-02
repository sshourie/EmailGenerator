import streamlit as st
import openai
from backend import ml_backend
import os

if __name__== '__main__':
    # add a github repo link. see: https://ghbtns.com/
    IFRAME = '<iframe src="https://ghbtns.com/github-btn.html?user=sshourie&repo=Folium_map&type=star&size=large&text=false" frameborder="0" scrolling="0" width="40" height="30" title="GitHub"></iframe>'

    st.set_page_config(
        page_title="GPT Email Generator",
        page_icon=":email:",
        # layout="wide",
        # initial_sidebar_state="auto",
    )

    st.markdown(
        f"""
        # GPT Email Helper {IFRAME}

        #### Play around with the inputs to generate different emails
        #### In the end, you can click a button to automatically send the email via Gmail.
        """,
        unsafe_allow_html=True,
    )

    with st.form(key="form"):
        prompt = st.text_input("Prompt: Describe the Kind of Email you want to be written.", value = 'Write me a professional sounding email to my boss')
        st.text(f"(This provides some context to the bot)")

        subject = st.text_input("Provide the email subject", value = 'Project discussion meeting!')
        # st.text(f"(Example: Hello, I wanted to discuss...")

        token_slider = st.slider("How many tokens do you want your email to be? ", min_value=100, max_value=500, value=150, step =10)
        st.text("(A typical email is around 100 words ≈ 150 tokens)")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            api_key = st.text_input(
                    '''Enter your OpenAI API Key: (click [here](https://platform.openai.com/account/api-keys) to obtain a new key if you do not have one
                    and read [here](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety) for best practices for API key safety.)''',
                    type="password",
            )
        backend = ml_backend(api_key)

        submit_button = st.form_submit_button(label='Generate Email')

        if submit_button:
            with st.spinner("Generating Email..."):
                output = backend.generate_email(prompt, subject, token_slider)
        
            # output = 'Hello, I wanted to discuss some important updates regarding our current project. \n\nI would appreciate the opportunity to schedule a meeting with you at your earliest convenience to go over these details in person. Please let me know a time that works best for you.\n\nThank you for your attention to this matter.\n\nBest regards,\n[Your Name]'
            with st.chat_message("assistant"):
                st.markdown("### Email Output:")
                st.write(output)

            # st.markdown("# Send Your Email")
            st.markdown("#### You can press the Generate Email Button again to get a new output")
            
            st.text("Once satisfied with the output, click the button to send it via Gmail")
            url = f"https://mail.google.com/mail/?view=cm&fs=1&to=&su={subject}&body={backend.gmail_friendly(output)}"

            st.link_button("Click me to send the email", url)
