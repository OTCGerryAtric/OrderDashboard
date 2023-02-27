import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta

#Dashboard Design
st.set_page_config(page_title='Order Dashboard', layout='wide')
password = 'TU!FTW22'

# Create a function to check the password
def check_password(input_password):
    if input_password == password:
        return True
    else:
        return False


# Create a login page
def login():
    # Prompt the user to enter a password
    input_password = st.text_input("Enter the password", type="password")

    # Check if the password is correct
    if check_password(input_password):
        return True
    else:
        return False


# Display the app if the password is correct
if login():
    #Import Data
    dr_data = pd.read_csv(r'H:\Shared drives\02 Finance\Dashboard\Source Data\Deliverect Data.csv')
    dr_data = dr_data.loc[dr_data['FullWeekCheck'] == 'Yes']
    dr_data = dr_data.loc[~dr_data['OrderID'].isna()]

    # Creating Filters
    st.sidebar.write('PLEASE NOTE, This only looks at full weeks')
    restaurant_list = dr_data['Location'].unique()
    restaurant_select = st.sidebar.multiselect('Restaurant', restaurant_list)
    channel_list = dr_data['Channel'].unique()
    channel_select = st.sidebar.multiselect('Channel', channel_list)
    status_list = dr_data['Cleaned Status'].unique()
    status_select = st.sidebar.multiselect('Cleaned Status', status_list)
    time_select = st.sidebar.selectbox('Time Period', ('OrderDate', 'OrderWeek', 'OrderMonth'))

    # Filtering Data
    filtered_data = dr_data
    if restaurant_select:
        filtered_data = filtered_data[filtered_data['Location'].isin(restaurant_select)]
    if channel_select:
        filtered_data = filtered_data[filtered_data['Channel'].isin(channel_select)]
    if status_select:
        filtered_data = filtered_data[filtered_data['Cleaned Status'].isin(status_select)]

    # Data for chart
    if time_select == 'OrderDate':
        order_counts = filtered_data.groupby('OrderDate').size().reset_index(name='Count')
    elif time_select == 'OrderWeek':
        order_counts = filtered_data.groupby('OrderWeek').size().reset_index(name='Count')
    else:
        order_counts = filtered_data.groupby('OrderMonth').size().reset_index(name='Count')

    # Chart
    with st.expander('High Level Order Chart'):
        fig = go.Figure()
        fig.add_trace(go.Bar(x=order_counts[time_select],
                             y=order_counts['Count'],
                             text=order_counts['Count'],
                             textposition='auto',
                             name='Count'))
        fig.update_layout(title='Bar Chart',
                          xaxis_title=time_select,
                          yaxis_title='Count',
                          barmode='stack',
                          width=2000)
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig)

    # Data for chart
    if time_select == 'OrderDate':
        order_counts = filtered_data.groupby(['OrderDate', 'Channel']).size().reset_index(name='Count')
    elif time_select == 'OrderWeek':
        order_counts = filtered_data.groupby(['OrderWeek', 'Channel']).size().reset_index(name='Count')
    else:
        order_counts = filtered_data.groupby(['OrderMonth', 'Channel']).size().reset_index(name='Count')

    # Chart
    with st.expander('Channel Splits'):
        fig = go.Figure()
        for channel in order_counts['Channel'].unique():
            fig.add_trace(
                go.Bar(x=order_counts[order_counts['Channel']==channel][time_select],
                       y=order_counts[order_counts['Channel']==channel]['Count'],
                       text=order_counts[order_counts['Channel']==channel]['Count'],
                       textposition='auto',
                       name=channel))
        fig.update_layout(title='Stacked Bar Chart',
                          xaxis_title=time_select,
                          yaxis_title='Count',
                          barmode='stack',
                          width=2000)
        st.plotly_chart(fig)

    # Data for chart
    if time_select == 'OrderDate':
        order_counts = filtered_data.groupby(['OrderDate', 'Location']).size().reset_index(name='Count')
    elif time_select == 'OrderWeek':
        order_counts = filtered_data.groupby(['OrderWeek', 'Location']).size().reset_index(name='Count')
    else:
        order_counts = filtered_data.groupby(['OrderMonth', 'Location']).size().reset_index(name='Count')

    with st.expander('Restaurant Splits'):
        fig = go.Figure()
        for Location in order_counts['Location'].unique():
            fig.add_trace(
                go.Bar(x=order_counts[order_counts['Location']==Location][time_select],
                       y=order_counts[order_counts['Location']==Location]['Count'],
                       text=order_counts[order_counts['Location']==Location]['Count'],
                       textposition='auto', name=Location))

        fig.update_layout(title='Stacked Bar Chart', xaxis_title=time_select, yaxis_title='Count', barmode='stack', width=2000)
        st.plotly_chart(fig)

    with st.expander('Weekly Breakdown'):
        col1, col2 = st.columns(2)
        day_of_week_view = pd.pivot_table(filtered_data, index=['OrderWeek'], columns=['DayOfWeek'], values=['OrderID'], aggfunc='count', margins=True, margins_name='Total')
        day_of_week_view = day_of_week_view.iloc[:-1]
        col1.write(day_of_week_view)

        end_date = pd.to_datetime(filtered_data['OrderWeek'].max()) + relativedelta(days=+6)
        start_date = end_date + relativedelta(days=-6, weeks=-3)