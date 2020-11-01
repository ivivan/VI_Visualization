import streamlit as st
import altair as alt
import operator
import numpy as np
import pandas as pd
import io
import time

st.set_option('deprecation.showfileUploaderEncoding', False)


def play_line_plots(df):
    df_temp = pd.DataFrame(df.values, columns=['NDVI'])
    base = alt.Chart(df_temp.reset_index()).mark_line().encode(
        x=alt.X('index', axis=alt.Axis(title='Day')),
        y=alt.Y('NDVI', axis=alt.Axis(title='NDVI'))).properties(
        width=600,
        height=400).interactive()
    st.altair_chart(base)


def play_bar_plots(df):
    df_temp = pd.DataFrame(df, columns=['Attention'])

    base = alt.Chart(df_temp.reset_index()).mark_bar().encode(
        x=alt.X('index', axis=alt.Axis(title='Day')),
        y=alt.Y('Attention', axis=alt.Axis(title='Attention'))).properties(
        width=600,
        height=400).interactive()
    st.altair_chart(base)



if __name__ == '__main__':
    st.sidebar.header("VI Visualizer")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Using Steps")
    st.sidebar.markdown("---")
    st.sidebar.markdown("1. Upload VI Data")
    st.sidebar.markdown("2. Choose Visualizer Options")
    st.sidebar.markdown("3. Check Visulization")
    st.sidebar.markdown("---")

    st.header('VI Visualizer')
    st.subheader("Upload VI Data")
    # k = st.number_input("Maximum No. of Rows to Read", min_value=10,
    #                     max_value=1000, step=1, value=10, key='readinput')

    # results = None
    uploaded_file = st.file_uploader(
        "Choose VI file (CSV)", type="csv", key='test')
    st.subheader("Upload Label CSV")
    ground_truth_file = st.file_uploader(
        "Choose Label file (Should Match the VI CSV)", type="csv", key='truth')
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data)
        st.subheader("VI Overview")
        max_row = data.shape[0]-1
        rows = st.slider('Select first few rows to plot',
                         0, max_row, max_row//100)

        st.write('Values:', rows)
        data = data.iloc[0:rows, :]
        st.line_chart(data.T.to_numpy())

        st.subheader("Plot single VI")
        ndvi_nrow = st.number_input(
            "Pick up a row", min_value=0, max_value=rows, step=1, value=0, key='singleinput')
        picked_ndvi = data.iloc[ndvi_nrow]
        show_ndvi = st.button("Show single VI")
        if show_ndvi:
            play_line_plots(picked_ndvi)
            if ground_truth_file is not None:
                label_data = pd.read_csv(ground_truth_file)
                st.write('This crop type is:', label_data.iloc[[ndvi_nrow]])
