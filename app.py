import pandas as pd
import numpy as np
import streamlit as st
import time

st.set_page_config(page_title="AHP", page_icon='🧐', layout="wide",initial_sidebar_state='auto')
# Hide the "Made with Streamlit" footer
hide_streamlit_style="""
    <style>
    #MainMenu{visibility:hidden;}
    footer{visibility:hidden;}
    h1{
        color: #FF5733;
        }
    h5{
        color: orange;
        } 
    h6{
        color: green;
        } 
    p{
        color: red;
        }
    </style>

    """
st.markdown(hide_streamlit_style,unsafe_allow_html=True)
st.title("Analytic Hierarchy Process",anchor=False)

# Gloabal Variables
add_Criteria = ['Yes','No']
add_Options = ['Yes','No']
rating = [0.11,0.12,0.14,0.16,0.20,0.25,0.33,0.50,1.00,2.00,3.00,4.00,5.00,6.00,7.00,8.00,9.00]
n=1
m=1
status =False
Factors = []
Options = []


def subheadingtext(text:str):
    message = []
    response = st.empty()
    tokens = list(text)
    for i in tokens:
        message.append(i)
        result = "".join(message)
        response.markdown(f'##### *{result}* ')
        time.sleep(0.04)

# st.select_slider("select",[1,2,3,4,5,6,7,8,9],value=1)
st.subheader("Let’s Begin with Defining Your Goal .",anchor=False)
goal = st.text_input("What is your Goal ?",placeholder="your Goal ?")
if goal!="":
    st.markdown("###### Fine , Your Goal is Defined , Now please identify your criteria.")
    # st.success(goal)
    criteria = st.text_input(f"Enter criteria : {n}",key="criteria"+str(n),placeholder="Factor "+str(n))
    Factors.append(criteria)
    if criteria !="":
        while n:
            # Factors.append(str(criteria))
            choose = st.radio('Add Criteria  ?',add_Criteria,index=1,key="choose"+str(n),horizontal=True)
            # st.warning(choose)
            if choose=='Yes':
                # st.info(choose)
                n+=1
                # st.success(n)
                # num = st.number_input("Enter a value 0-9",min_value=0,max_value=9,key=str(n)+"num")
                for i in range (n,n+1):
                    criteriaAdd = st.text_input(f"Enter criteria : {i}",key="criteriaAdd"+str(i),placeholder="Factor "+str(i))
                    Factors.append(criteriaAdd)
            else :
                # st.warning(criteria)
                opt=st.checkbox("Enter Options :")
                if opt:
                    status = True
                # st.info(choose)
                # status = True
                break
    # m = int(input("How many options do you have for comparision?"))
if status:
    #option priority :
    option = st.text_input(f"Enter option: {m}",key="optionAdd"+str(m))
    Options.append(option)
    if (option!=""):
        while m:
            addOption = st.radio('Add Option ?',add_Options,index=1,key="addOption"+str(m),horizontal=True)
            if addOption=='Yes':
                m+=1
                for i in range(m,m+1):
                    option = st.text_input(f"Enter option: {i}",key="optionAdd"+str(i))
                    Options.append(option)
            else:
                # st.warning(addOption)
                # st.info(choose)
                break

# st.write(Factors)
# st.write(Options)
# st.info(n)
# st.info(m)
if (((len(Options)) and (len(Factors)))):
    process = st.checkbox("Begin AHP :")
    try:
        if process:
            # AHP(n,m)
            final_df = pd.DataFrame(data = [], index = Options )
            RI = [0,0,0,0.58,0.90,1.12,1.24,1.32,1.42]
            for i in range (n):
                st.divider()
                data = {Factors[i] : Options}
                for j in range (m):
                    l = [1.]*m
                    data[Options[j]] = l
                df = pd.DataFrame(data).set_index(Factors[i])
                for j in range (m-1):
                    for k  in range (j+1,m):
                        # df.iloc[j][k] = st.number_input(f"Evaluate {Options[j]} with respect to {Options[k]} based on {Factors[i]}",min_value=0.1,max_value=9.0)
                        # st.write(f"Evaluate {Options[j]} with respect to {Options[k]} based on {Factors[i]}")
                        df.iloc[j][k] = st.select_slider(f"Evaluate {Options[j]} with respect to {Options[k]} based on {Factors[i]}",options=rating,value=1)
                        df.iloc[k][j] = 1 / df.iloc[j][k]
                df_org = df.copy()
                df = df.div(df.sum())
                df['Priorities'] = np.mean(df,axis=1)
                # st.dataframe(df)
                dot_product = np.dot(df_org,df['Priorities'])
                # st.dataframe(dot_product)
                consistency_vector = dot_product / df ['Priorities']
                # st.dataframe(consistency_vector)
                Lambda = consistency_vector.mean()
                # st.write(f"lambda = {Lambda}")
                consistency_index = (Lambda - m)/(m-1)
                # st.write(f"CI = {consistency_index}")
                # st.warning(df_org.values.sum())
                if(df_org.values.sum()==9.0):
                    st.write("update priorities")
                    exit(0)
                consistency_ratio = consistency_index / RI[m]
                if((consistency_ratio > 0.1)):
                    # st.write("Your answers are highly inconsistent with different choices.So a better option can not be selected with these priorities")
                    st.error(f"Consistency Ratio {consistency_ratio:.2f} > 0.1")
                    exit(0)
                # st.write(f"CR = {consistency_ratio}")
                


                final_df[Factors[i]] = df ['Priorities']
            # st.write(final_df)




            # FP (Factors Priority)
            FP = pd.DataFrame(data = np.ones((n,n)),index = Factors)
            # st.dataframe(FP)
            st.divider()
            for i in range (n-1):
                for j in range (i+1,n):
                    FP.iloc[i][j] = st.select_slider(f"Evaluate {Factors[i]} with respect to {Factors[j]}",options=rating,value=1)
                    FP.iloc[j][i] = (1)/(FP.iloc[i][j])


            FP_org = FP.copy()
            FP = FP.div(FP.sum())
            FP['Priorities'] = np.mean(FP,axis=1)
            # st.dataframe(FP)



            dot_product = np.dot(final_df,FP['Priorities'])
            # dot_product
            final_df['Priorities'] = dot_product
            # final_df
            message1 = str(final_df.loc[final_df['Priorities'] == final_df['Priorities'].max()].index[0])+" "
            message2 = str(int(final_df['Priorities'].max()*100))
            st.divider()
            showResult = st.checkbox("press to see the result")
            if showResult:
                subheadingtext(f"For the Goal : {goal}")
                subheadingtext(f"According to Your Priorities ; Going with {message1} will be the Best Option , with {message2} % Support")
                st.divider()
    except IndexError:
        st.error("please Answer the input fields .")