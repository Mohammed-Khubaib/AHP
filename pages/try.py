import streamlit as st
import time
if "See Result :" not in st.session_state:
    st.session_state['See Result :'] =True
# rating = [0.11,0.12,0.14,0.17,0.20,0.25,0.333,0.50,1.00,2.00,3.00,4.00,5.00,6.00,7.00,8.00,9.00]

# selected_option = st.radio("Select a value", rating,horizontal=True,index=8)

# # Show the values of object A and B
# st.write(f"Object A: {selected_option:.2f} | Object B: {1/selected_option:.2f}")
# # 
with st.expander("See Result :"):
    time.sleep(3)
    st.write("Hello world")
    
if st.session_state["See Result :"]:
    # User has expanded the expander
    print("The user has expanded the expander.")
else:
    # User has collapsed the expander
    print("The user has collapsed the expander.")
