import streamlit as st
# Inject custom CSS to change the background color
st.markdown( 
    """ 
    <style> 
    .reportview-container { 
        background-color: black; 
    } 
    </style> 
    """, 
    unsafe_allow_html=True
    )
# Set the title of the app
st.title("Streamlit App with Markdown Field")
# Display a Markdown field
st.markdown(""" 
    # Welcome to the Streamlit App 
    
    This is an example of a simple app with a Markdown field. 
    
    ## Features: 
    - Display text in **Markdown** format 
    - Support for *italic*, **bold**, and other text formatting options. 
    
    ### Code Example: 
    ```python 
    import streamlit as st 
    st.markdown("Hello, **Streamlit!**") 
    ``` 
    
    - You can even include links: [Streamlit Website](https://www.youtube.com/watch?v=PnRFjKgiWWU)""")