import streamlit as st
import pandas as pd
import numpy as np
import time
import s3fs

access_key_id=st.secrets["AWS_ACCESS_KEY_ID"]
secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
bucket_name = st.secrets["bucket_name"]

s3 = s3fs.S3FileSystem(anon=False)

st.set_page_config(page_title="Annotation Demo", page_icon="📈")

st.title('Text Annotation')
password = st.text_input('Please Enter your Password')

groups = ['<select>',"Group1", "Group2", "Group3"]
default_groups = groups.index("<select>")
group = st.selectbox("Please choose the group you have been selected for", groups, index=default_groups)

if group == "Group1":
    df = pd.read_excel('annotation_batch_2.xlsx')
    df = df[:250]
    df["Column1"] = df.index.values
elif group == "Group2":
    df = pd.read_excel('annotation_batch_2.xlsx')
    df = df[250:]
    indexlist = list(range(0,250))
    df["Column1"] = indexlist
else:
    df = pd.read_excel('annotation_batch_3.xlsx')
    indexlist = list(range(0,250))
    df["Column1"] = indexlist
   
def submit():
    st.session_state.label_list.append(st.session_state.label_input)
    df["Label"][st.session_state.count] = st.session_state.label_input
    st.session_state.count += 1
    with s3.open(f"{bucket_name}/{group}_label_list_{prolificid}.csv",'w') as f:
        df.to_csv(f, encoding="utf-8")

def success_message():
    st.write("Progress: ", st.session_state.count, "/", len(df))
    st.success("Thank you! All done!")

if st.session_state.get('count') is None:
    st.session_state.count = 0
    st.session_state.label_list = []


if password == st.secrets["access_pw"]:
    st.session_state['state']=0
else:
    st.session_state['state']=-5

prolificid = st.text_input(f"Please Enter your Lastname or Prolific ID \n (Please make sure to remember the exact name. \n In case you get a connection error your progress will be lost if you don't type in your previous username.): ")
st.info(f'Your Prolific ID: {prolificid} ')

last_label = 0

def form_submit():      
    if st.session_state['state']== 0 or st.session_state['state']==last_label:
        success = st.success("Password acepted!")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        with st.form("my_form"):
            if st.session_state.count < len(df):
                st.write("Progress: ", st.session_state.count + 1, "/", len(df))
                st.write("")
                st.write("")
                st.write("")
                text = df.iloc[st.session_state.count]['Text']
                id = df.iloc[st.session_state.count]['Id']
                col1 = df.iloc[st.session_state.count]['Column1']
                st.write(text)
                st.write("")
                st.write("")
                st.write("")
                values = ['<select>',"HOF", "NOT","Not Sure"]
                default_ix = values.index("<select>")
                label = st.selectbox("Classification:", values, index=default_ix, key='label_input')
                submitted = st.form_submit_button("Submit & Next", on_click=submit)      
            else:
                st.write("Progress: ", st.session_state.count, "/", len(df))
                st.success("Thank you! All done!")
                st.balloons()
                st.write("Here is the Completion Code: ", st.secrets["completion_code"])
                st.write("Here is Your Unique Completion Code :", st.secrets['u_completion_code'])
                submitted = st.form_submit_button("View List")
                if submitted:
                    st.write(st.session_state.label_list)
    else:
        st.error("Please provide the right password or ask the administrator for help!")


if s3.exists(f"{bucket_name}/{group}_label_list_{prolificid}.csv"):
    with s3.open(f"{bucket_name}/{group}_label_list_{prolificid}.csv",'r') as file:
        df_old = pd.read_csv(file)
        df_old.drop(df_old.filter(regex="Unname"),axis=1, inplace=True)
        last_value = df_old.index.values[-1]
        if ((df_old.Label.iloc[last_value] == 'HOF' or df_old.Label.iloc[last_value] == 'NOT' or df_old.Label.iloc[last_value] == 'Not Sure')) == False:
            last_label = df_old.Column1[(df_old.Label == "Choose�")].iloc[0]
            st.session_state.count = last_label
        else:
            st.write("Finished")
        df = df_old
        form_submit()
else:
    df = df
    form_submit()