import pandas as pd
import numpy as np
import streamlit as st
import time
import json
import requests
from streamlit_lottie import st_lottie
st.set_page_config(page_title="AHP", page_icon='🧐', layout="wide",initial_sidebar_state='auto')

# Using the st_lottie function to load and display the animation
def load_lottie_url(url:str):
    r=requests.get(url)
    if r.status_code!=200:
        st.warning('No image')
        return None
    return r.json()

def load_lottie_file(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
lottie_file1 =load_lottie_file('./assets/f1.json')
lottie_file2 =load_lottie_file('./assets/f2.json')
# Hide the "Made with Streamlit" footer
hide_streamlit_style="""
    <style>
    #MainMenu{visibility:hidden;}
    footer{visibility:hidden;}
    h1{
        color: #66C4FF;
        }
    h4{
        # color: #FF5733;
        color:   #E04078;
        text-align: center;
        }
    h5{
        color: #A3D7FF;
        }
    span {
        # color : #A3D7FF;
        font-size: inherit;
        font-weight: inherit;
    }
    h6{
        color: #7AC917;
        # color:  #A3D7FF;
        } 
    p{

        color:  #5A88A6;
        # color: skyblue;
        }
    .option1 {
        color:#00CED1;
    }
    .option2 {
        color: #FFDB58;
    }
    .factors {
        color: #FF9800;
    }
    </style>


    """
st.markdown(hide_streamlit_style,unsafe_allow_html=True)
c1 , c2  = st.columns([0.75,2])
with c1 :
    st_lottie(lottie_file1,speed=0.5,reverse=False,height=120,width=180)
with c2 :
    st.title("Analytic Hierarchy Process",anchor=False)
# Gloabal Variables
add_Criteria = ['Yes','No']
add_Options = ['Yes','No']
rating = [0.11,0.12,0.14,0.17,0.20,0.25,0.333,0.50,1.00,2.00,3.00,4.00,5.00,6.00,7.00,8.00,9.00]
n=1
m=1
status =False
Factors = []
Options = []

#262730

def subheadingtext(text:str):
    message = []
    response = st.empty()
    tokens = list(text)
    for i in tokens:
        message.append(i)
        result = "".join(message)
        response.markdown(f'##### {result} ',unsafe_allow_html=True)
        time.sleep(0.012)
# st.divider()
with st.sidebar:
    st_lottie(lottie_file2,speed=0.5,reverse=False,height=180,width=280)
    st.header("Preference Scale :")
    st.write("""
            1 : Equally preferred\n
            2 : Equally to moderately preferred\n
            3 : Moderately preferred\n
            4 : Moderately to strongly preferred\n
            5 : strongly preferred\n
            6 : strongly to very strongly preferred\n
            7 : very strongly preferred\n
            8 : very to extremely preferred\n
            9 : Extremely preferred\n
        """)
st.markdown(f"<h3 style='text-align: center;'>Let’s Begin with Defining Your Goal .</h3>", unsafe_allow_html=True)
# st.radio("select",[1,2,3,4,5,6,7,8,9],value=1)
# s=st.markdown(f"<h2 style='text-align: center;'>Let’s Begin with Defining Your Goal .</h2>", unsafe_allow_html=True)
goal = st.text_input("What is your Goal ?",placeholder="your Goal ?")
if goal!="":
    st.markdown(f"<h6 style='text-align: center;'> Fine , Your Goal is Defined , Now please identify your criteria.</h6>", unsafe_allow_html=True)
    # st.markdown("###### Fine , Your Goal is Defined , Now please identify your criteria.")
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
            count = 0
            st.divider()
            for i in range (n):
                data = {Factors[i] : Options}
                for j in range (m):
                    l = [1.]*m
                    data[Options[j]] = l
                df = pd.DataFrame(data).set_index(Factors[i])
                for j in range (m-1):
                    for k  in range (j+1,m):
                        # df.iloc[j][k] = st.number_input(f"Evaluate {Options[j]} with respect to {Options[k]} based on {Factors[i]}",min_value=0.1,max_value=9.0)
                        # st.write(f"Evaluate {Options[j]} with respect to {Options[k]} based on {Factors[i]}")
                        st.markdown(f'<h4>How would you rate <span class="option1">{Options[j]}</span> compared to <span class="option2">{Options[k]}</span> based on <span class="factors">{Factors[i]}</span> ?</h4>', unsafe_allow_html=True)
                        
                        # st.markdown(f"<h4 style='text-align: center;'>rate </h4><h5>{Options[j]}</h5><h4>compared to </h4><h5>{Options[k]}</h5><h4>based on </h4><h5>{Factors[i]}</h5>", unsafe_allow_html=True)
                        df.iloc[j][k] = st.radio(f"Rank {Options[j]} based on {Factors[i]}",options=rating,index=8,horizontal=True,key="radio"+str(count))
                        count+=1
                        df.iloc[k][j] = 1 / df.iloc[j][k]
                        # space = "&nbsp;&nbsp;"*50 
                        st.markdown(f"<h5 style='text-align: center;'>{Options[j]}: {(df.iloc[j][k]):.2f} | {Options[k]}: {(df.iloc[k][j]):.2f}</h5>", unsafe_allow_html=True)
                        st.divider()
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
                # st.info(f"n = {n} , m={m}")
                # st.dataframe(df_org)
                # st.warning(df_org.values.sum())
                if(df_org.values.sum()%3==0):
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
            # st.divider()
            count = 0 # for keeping the key unique
            for i in range (n-1):
                for j in range (i+1,n):
                    st.markdown(f'<h4> <span class="option2">{Factors[i]}</span> vs <span class="factors">{Factors[j]}</span></h4>', unsafe_allow_html=True)
                    FP.iloc[i][j] = st.radio(f"Evaluate {Factors[i]} with respect to {Factors[j]}",options=rating,index=8,horizontal=True,key="radio "+str(count))
                    count+=1
                    FP.iloc[j][i] = (1)/(FP.iloc[i][j])
                    st.markdown(f"<h5 style='text-align: center;'>{Factors[i]}: {(FP.iloc[i][j]):.2f} | {Factors[j]}: {(FP.iloc[j][i]):.2f}</h5>", unsafe_allow_html=True)


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
            # st.divider()
            exp =False
            # with st.expander("See Result :"):
            col1 , col2  = st.columns([2.5,4])
            col3 , col4 = st.columns([1,3])
            st.divider()
            with col2:
                if st.button("Generate Recommendation",help="submit",key="1"):
                        # st.markdown(f'<p><span class="highlight">highlighted 1 {subheadingtext(f"For the Goal: {goal}")}{subheadingtext(f"According to Your Priorities; Going with {message1} will be the Best Option, with {message2}% Support")}</span></p>',unsafe_allow_html=True)
                        with col4:
                            subheadingtext(f'For the Goal:  <span class="factors">{goal}<span>')
                            subheadingtext(f'*According to Your Priorities; Going with <span class="factors">{message1}</span> will be the Best Option, with <span class="factors">{message2}%</span> Support*')

            # st.divider()
    except IndexError:
        st.error("please Answer the input fields .")