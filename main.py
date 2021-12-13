from numpy import select
import streamlit as st
from utility import *
import numpy as np
from modelDetails import Query2 , Query1
import pickle
import bz2

viewDF = viewAreaChart = viewBarChart = classifier_name = isAnyFileUploaded = isAllFileUploaded = query_no = clickPredict = False
val1 = val2 = val3 = Model = df = q = None


def main_screen_top():
    global isAnyFileUploaded , isAllFileUploaded , query_no , val1 , val2 , val3 , df
    
    file1 = file2 = file3 = None
    if query_no != "Select Query":
        file1 = st.file_uploader("Choose 1st cProfile CSV file", type=[".csv"])
        file2 = st.file_uploader("Choose 2nd cProfile CSV file", type=[".csv"])
        file3 = st.file_uploader("Choose 3rd cProfile CSV file", type=[".csv"])
    else:
        st.write("""
            # Propose Data Model for Health Care..
        """)

    if file1 != None or file2 != None or file3 != None:
        val1 = val2 = val3 = None
        df = pd.DataFrame()
        df['function_name'] = get_function_name()

        if file1 != None:
            val1 = get_tottime(file1)
            df['Schema1_time']  = val1

        if file2 != None:
            val2 = get_tottime(file2)
            df['Schema2_time']  = val2

        if file3 != None:
            val3 = get_tottime(file3)
            df['Schema3_time']  = val3

        isAllFileUploaded = file1 != None and file2 != None and file3 != None
        isAnyFileUploaded = file1 != None or file2 != None or file3 != None
        
    
def side_screen_top():
    global query_no
    query_no = st.sidebar.selectbox("Select Query" , ("Select Query" , "Query 1" , "Query 2"))

def side_screen_bottom():
    global isAllFileUploaded , isAnyFileUploaded , viewDF , viewBarChart , viewAreaChart , classifier_name , query_no , clickPredict
    
    if isAnyFileUploaded:
        st.sidebar.write("""
            ## Schema Analysis
        """)
        viewDF = st.sidebar.checkbox('View Uploaded DataFrame')

        if isAllFileUploaded:
            viewBarChart = st.sidebar.checkbox('Bar Chart With Total totime for Schemas')
            viewAreaChart = st.sidebar.checkbox('Area Chart for each Schemas')
            classifier_name = st.sidebar.selectbox("Select Classifier" , ("Select Classifier" , "Decision Tree" , "Random Forest"))

def add_model_parameter():
    global classifier_name , query_no , clickPredict , Model , q
    if query_no == "Query 2":
        q = Query2
    elif query_no == "Query 1":
        q = Query1

    max_depth = None
    v = None
    if classifier_name == "Decision Tree":
        v = q = q['decision_tree']
        max_depth = st.sidebar.slider("Max Depth" , q['start'] , q['end'])
    elif(classifier_name == 'Random Forest'):
        v = q = q['randomForest']
        max_depth = st.sidebar.slider("Max Depth" , q['start'] , q['end'])

    if v != None:
        model_path = v['classifierPath']
        model_name = v['accuracy'][max_depth]['file_path']
        model_loc = model_path + model_name
        
        with open(model_loc, 'rb') as pickle_file:
            Model = pickle.load(pickle_file)
            if isAllFileUploaded and classifier_name != "Select Classifier":
                clickPredict = st.sidebar.button('Predict best Schema')
    
    return max_depth

def main_screen_bottom():
    global df , viewDF , viewAreaChart , viewBarChart

    if viewDF or viewAreaChart or viewBarChart:
        st.markdown('***')
        st.write("""
            ### Analysis Of 3 Schemas
        """)

    if viewDF:
        st.write("""
            #### Uploaded DataFrame
        """)
        st.dataframe(df)

    if viewBarChart:
        st.write("""
            #### Total time Comparison
        """)

        identity_sum = np.identity(3)
        identity_sum[0][0] = sum(val1)
        identity_sum[1][1] = sum(val2)
        identity_sum[2][2] = sum(val3)

        chart_data = pd.DataFrame(
            np.array(identity_sum),
            columns=["1st Schema", "2nd Schema", "3rd Schema"],
            index=["1st Schema", "2nd Schema", "3rd Schema"]
        )
        st.bar_chart(chart_data)

    if viewAreaChart:
        st.write("""
            #### Area Chart for Function Calls
        """)

        chart_data = pd.DataFrame(
            np.array(np.transpose([val1, val2, val3])),
            columns=["1st Schema", "2nd Schema", "3rd Schema"],
            index=get_function_name()
        )
        st.area_chart(chart_data)

def main_prediction(max_depth):
    if clickPredict:
        st.markdown('***')
        st.write("""
            ### Machine Learning To Predict Best Schema
        """)
        
        if classifier_name == "Decision Tree":
            st.write("""
                #### Decision Tree Algorithm
            """)
        elif classifier_name == "Random Forest":
            st.write("""
                #### Random Forest Algorithm
            """)
        st.markdown('***')
        s = "##### Training Accuracy : %.3f %% and Testing Accuracy : %.3f %% " % (q['accuracy'][max_depth]["training_accuracy"] * 100 , q['accuracy'][max_depth]["testing_accuracy"] * 100 )
        
        st.markdown(s)

        s = "##### Predicted Data Model : Schema "+str(Model.predict([val1 + val2 + val3])[0])
        st.markdown(s)

if __name__ == "__main__":
    side_screen_top()
    main_screen_top()
    side_screen_bottom()
    max_depth = add_model_parameter()
    main_screen_bottom()
    main_prediction(max_depth)