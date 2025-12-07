import pandas as pd 
import plotly.express as px 
import streamlit as st

st.set_page_config(page_title = 'health_insurance_EDA')

df=pd.read_csv('health_insurance_cleaned.csv',index_col=0)
st.markdown("<h1 style=color:white;text-align:center;> 💊 Health Insurance EDA</h1",unsafe_allow_html=True)
st.image('health_image.jpg')
page=st.sidebar.radio('page',['Home','Univariate','Multivariate'])

if page=='Home':
    column_description=pd.read_csv('column_description.csv',index_col=0)
    st.dataframe(df)
    st.dataframe(column_description)


elif page=='Univariate':

    tab_num,tab_cat=st.tabs(['numbers','catrgorical'])

    col_cat=tab_cat.selectbox('column',df.select_dtypes(include='object').columns)
    col_num=tab_num.selectbox('column',df.select_dtypes(include='number').columns)

    cat_counts = df[col_cat].value_counts().sort_values(ascending=False).reset_index()
    cat_counts.columns = [col_cat, 'count']

    tab_num.plotly_chart(px.histogram(data_frame=df,x=col_num))
    chart = tab_cat.selectbox('Chart', ['Histogram', 'Pie'])
    if chart == 'Pie':

        tab_cat.plotly_chart(px.pie(data_frame=df,names=col_cat))
    elif chart == 'Histogram':
        tab_cat.plotly_chart(px.bar(cat_counts,x=col_cat,y='count'))


elif page == 'Multivariate':

    st.header('Total income per Plan Type')
    plan_income = df.groupby('plan_type')['income'].sum().round(2).reset_index()
    plan_income = plan_income.sort_values(by='income', ascending=False)
    st.plotly_chart(px.bar(plan_income,x='plan_type',y='income',labels={'plan_type':'Plan Type', 'income':'Total income'},text_auto=True,title='Average Income by Plan Type'))

    st.header('Gender vs Number of Claims')
    st.plotly_chart(px.histogram(df,x='sex',y='claims_count',color='sex',barmode='group',title='Total Claims by Gender'))

    st.header('Impact of Smoker Status on Average Annual Medical Cost')
    smoker_avg_cost = df.groupby('smoker')['annual_medical_cost'].mean().round(2).reset_index()
    st.plotly_chart(px.bar(smoker_avg_cost,x='smoker',y='annual_medical_cost',text='annual_medical_cost',title='Average Annual Medical Cost by Smoker Status'))

    st.header('Average Risk Score by BMI Range')

    df['bmi_group'] = pd.cut(df['bmi'], bins=5)
    df['bmi_group_str'] = df['bmi_group'].astype(str)
    bmi_risk = df.groupby('bmi_group_str')['risk_score'].mean().reset_index()

    st.plotly_chart(px.bar( bmi_risk,x='bmi_group_str',y='risk_score',text='risk_score',title='Average Risk Score by BMI Range'))

st.markdown("""<hr style="margin:30px 0;"><p style="text-align:center; color:gray; font-size:14px;">Developed by <strong>Mohamed shaban</strong></p>""",unsafe_allow_html=True)
