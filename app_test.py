import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO

st.title("ENERGY LAB")
st.sidebar.title("Navigation")
uploaded_file = st.sidebar.file_uploader("Upload a file", type=["csv", "txt"])
options = st.sidebar.radio("pages", options=["Comfort EN", "Temperature", "Radiation", "Relative humidity", "Interior Temperature","Download excel file"])


if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, delimiter='\t', header=[0, 1])

    new_columns = [
        ('AirTemp', 'Min'),
        ('AirTemp', 'Average'),
        ('AirTemp', 'Max'),
        ('RelHumidity', 'Min'),
        ('RelHumidity', 'Average'),
        ('RelHumidity', 'Max'),
        ('TGlobe', 'Min'),
        ('TGlobe', 'Average'),
        ('TGlobe', 'Max'),
        ('WindSpeed', 'Min'),
        ('WindSpeed', 'Average'),
        ('WindSpeed', 'Max'),
        ('WindDir', 'RisDir'),
        ('WindDir', 'RisVel'),
        ('WindDir', 'StdDevDir'),
        ('WindDir', 'CalmPerc'),
        ('GlobRad', 'Min'),
        ('GlobRad', 'Average'),
        ('GlobRad', 'Max'),
        ('IntTemp', 'Instant'),
        ('BatteryTens', 'Instant'),
        ('x', 'x')
    ]

    df.columns = pd.MultiIndex.from_tuples(new_columns)
    df.drop(('x', 'x'), axis=1, inplace=True)
    df.columns = df.columns.map('_'.join)
    df.index = pd.to_datetime(df.index)
    df['Month'] = df.index.month_name()
    df['Year'] = df.index.year
    df['Day'] = df.index.day
    df['Average_Daily_Temp'] = df.groupby(['Year', 'Month', 'Day'])['AirTemp_Average'].transform('mean')

    def class_a(IntTemp_Instant, Average_Daily_Temp):
        lower_limit = max(18.8 - 2 + 0.33 * Average_Daily_Temp, 21)
        upper_limit = max(18.8 + 2 + 0.33 * Average_Daily_Temp, 23)
        if IntTemp_Instant >= lower_limit and IntTemp_Instant <= upper_limit:
            return 1
        else:
            return 0

    def class_b(IntTemp_Instant, Average_Daily_Temp):
        lower_limit = max(18.8 - 3 + 0.33 * Average_Daily_Temp, 20)
        upper_limit = max(18.8 + 3 + 0.33 * Average_Daily_Temp, 24)
        if IntTemp_Instant >= lower_limit and IntTemp_Instant <= upper_limit:
            return 1
        else:
            return 0

    def class_c(IntTemp_Instant, Average_Daily_Temp):
        lower_limit = max(18.8 - 4 + 0.33 * Average_Daily_Temp, 19)
        upper_limit = max(18.8 + 4 + 0.33 * Average_Daily_Temp, 25)
        if IntTemp_Instant >= lower_limit and IntTemp_Instant <= upper_limit:
            return 1
        else:
            return 0
    
    def main():
        st.title("DataFrame to Excel Conversion")
        st.write("Original DataFrame:")
        st.dataframe(df)
        # Export DataFrame to Excel file
        if st.button("Export to Excel"):
            # Create an in-memory Excel file
            excel_data = BytesIO()
            with pd.ExcelWriter(excel_data, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
            excel_data.seek(0)
    
            # Download button
            st.download_button(
                label="Download Excel file",
                data=excel_data,
                file_name="output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
    
    def comfort(df):
        months = df['Month'].unique()
        for month in months:
            month_df = df[df['Month'] == month]
            length_class_a = month_df['class_A'].sum()
            length_class_b = month_df['class_B'].sum()
            length_class_c = month_df['class_C'].sum()
            total_hours = len(month_df)
            discomfort_percentage = ((total_hours - length_class_c) / total_hours) * 100
            comfort_percentage = (length_class_c / total_hours) * 100
            class_a_percentage = (length_class_a / total_hours) * 100
            class_b_percentage = (length_class_b / total_hours) * 100
            class_c_percentage = (length_class_c / total_hours) * 100

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7.5))
            labels1 = ['Class A', 'Class B', 'Class C']
            sizes1 = [class_a_percentage, class_b_percentage, class_c_percentage]
            labels2 = ['Comfort', 'Discomfort']
            sizes2 = [comfort_percentage, discomfort_percentage]
            colors2 = ['green', 'red']

            if all(size != 0 for size in sizes1) and all(size != 0 for size in sizes2):
                ax1.pie(sizes1, labels=None, autopct='%1.1f%%', startangle=90, pctdistance=0.85)
                ax1.legend(labels1, loc='lower center')
                ax1.axis('equal')
                ax1.set_title('EN 15251 COMFORT HOURS - {}'.format(month))
                centre_circle1 = plt.Circle((0, 0), 0.70, fc='white')
                ax1.add_artist(centre_circle1)
                ax2.pie(sizes2, labels=None, colors=colors2, autopct='%1.1f%%', startangle=90, pctdistance=0.85)
                ax2.legend(labels2, loc='lower center')
                ax2.axis('equal')
                ax2.set_title('EN 15251 COMFORT VS DISCOMFORT - {}'.format(month))
                centre_circle2 = plt.Circle((0, 0), 0.70, fc='white')
                ax2.add_artist(centre_circle2)
            else:
                ax1.text(0.5, 0.5, 'NO COMFORT RANGE IN - {}'.format(month), horizontalalignment='center',
                         verticalalignment='center', transform=ax1.transAxes)
                ax2.text(0.5, 0.5, 'NO COMFORT RANGE IN - {}'.format(month), horizontalalignment='center',
                         verticalalignment='center', transform=ax2.transAxes)

            st.pyplot(fig)
            
    if options == "Comfort EN":
        if 'df' in locals():
            df["class_A"] = df.apply(lambda x: class_a(x["IntTemp_Instant"], x["Average_Daily_Temp"]), axis=1)
            df["class_B"] = df.apply(lambda x: class_b(x["IntTemp_Instant"], x["Average_Daily_Temp"]), axis=1)
            df["class_C"] = df.apply(lambda x: class_c(x["IntTemp_Instant"], x["Average_Daily_Temp"]), axis=1)
            comfort(df)
        else:
            st.write("Please upload a file.")
            
    if options == "Temperature":
        if 'df' in locals():
            st.subheader("Temperature Line Graph")
            fig = px.line(df, x=df.index, y='AirTemp_Average')
            st.plotly_chart(fig)
        else:
            st.write("Please upload a file.")

    if options == "Radiation":
        if 'df' in locals():
            st.subheader("Radiation Line Graph")
            fig = px.line(df, x=df.index, y='GlobRad_Average')
            st.plotly_chart(fig)
        else:
            st.write("Please upload a file.")

    if options == "Relative humidity":
        if 'df' in locals():
            st.subheader("Radiation Line Graph")
            fig = px.line(df, x=df.index, y='RelHumidity_Average')
            st.plotly_chart(fig)
        else:
            st.write("Please upload a file.")

    if options == "Interior Temperature":
        if 'df' in locals():
            st.subheader("Radiation Line Graph")
            fig = px.line(df, x=df.index, y='IntTemp_Instant')
            st.plotly_chart(fig)
        else:
            st.write("Please upload a file.")
                
    if options == "Download excel file" and 'df' in locals():
        main()

