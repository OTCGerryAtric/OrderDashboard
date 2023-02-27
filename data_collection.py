import datetime
from datetime import timedelta
import pandas as pd
from dateutil.relativedelta import relativedelta

# Functions
def day_of_week(date):
    date = date.iloc[0]  # extract first element of the Series object
    day_of_week = datetime.timedelta(days=date.weekday())
    return day_of_week

# Import Data
import_1 = pd.read_csv(
    r'H:\Shared drives\99 - Data\01 - Source Data\01 - Deliverect\CSV Files\Orders\22.12 - Dec 22 Orders.csv')
import_2 = pd.read_csv(
    r'H:\Shared drives\99 - Data\01 - Source Data\01 - Deliverect\CSV Files\Orders\23.01 - Jan 23 Orders.csv')
import_3 = pd.read_csv(
    r'H:\Shared drives\99 - Data\01 - Source Data\01 - Deliverect\CSV Files\Orders\23.02 - Feb 23 Orders.csv')
import_4 = pd.read_csv(
    r'H:\Shared drives\99 - Data\01 - Source Data\01 - Deliverect\CSV Files\Orders\23.03 - Mar 23 Orders.csv')
import_5 = pd.read_csv(
    r'H:\Shared drives\99 - Data\01 - Source Data\01 - Deliverect\CSV Files\Orders\23.04 - Apr 23 Orders.csv')
import_6 = pd.read_csv(
    r'H:\Shared drives\99 - Data\01 - Source Data\01 - Deliverect\CSV Files\Orders\23.05 - May 23 Orders.csv')
import_7 = pd.read_csv(
    r'H:\Shared drives\99 - Data\01 - Source Data\01 - Deliverect\CSV Files\Orders\23.06 - Jun 23 Orders.csv')
dr_data = pd.concat([import_1, import_2, import_3, import_4, import_5, import_6, import_7])

# Clean Data
dr_data['Location'] = dr_data['Location'].str.replace('Birdie Birdie ', '')
dr_data['Channel'] = dr_data['Channel'].str.replace('TakeAway Com', 'Lieferando')
dr_data['Cleaned Status'] = dr_data['Status']
dr_data['Cleaned Status'] = dr_data['Cleaned Status'].str.replace('FAILED', 'Failed')
dr_data['Cleaned Status'] = dr_data['Cleaned Status'].str.replace('Failed_RESOLVED', 'Delivered')
dr_data['Cleaned Status'] = dr_data['Cleaned Status'].str.replace('DELIVERECT_PARSED', 'Delivered')
dr_data['Cleaned Status'] = dr_data['Cleaned Status'].str.replace('DELIVERED', 'Delivered')
dr_data['Cleaned Status'] = dr_data['Cleaned Status'].str.replace('ACCEPTED', 'Delivered')
dr_data['Cleaned Status'] = dr_data['Cleaned Status'].str.replace('CANCELED', 'Cancelled')
dr_data['Cleaned Status'] = dr_data['Cleaned Status'].str.replace('CANCEL', 'Cancelled')
dr_data['Cleaned Status'] = dr_data['Cleaned Status'].str.replace('FAILED_RESOLVED', 'Delivered')
dr_data['Cleaned Status'] = dr_data['Cleaned Status'].str.replace('READY_FOR_PICKUP', 'Delivered')
dr_data['Cleaned Status'] = dr_data['Cleaned Status'].str.replace('AUTO_FINALIZED', 'Delivered')
dr_data['Cleaned Status'] = dr_data['Cleaned Status'].str.replace('IN_DELIVERY', 'Delivered')
dr_data['Cleaned Status'] = dr_data['Cleaned Status'].str.replace('DUPLICATE', 'Delivered')
dr_data['CreatedTime'] = pd.to_datetime((dr_data['CreatedTime']))
dr_data['OrderDate'] = dr_data['CreatedTime'].dt.date
dr_data['OrderTime'] = dr_data['CreatedTime'].dt.time
dr_data['MaxDate'] = max(dr_data['OrderDate'])
dr_data['OrderWeek'] = dr_data['OrderDate'].apply(lambda x: x - timedelta(days=x.weekday()))
dr_data['EndOfOrderWeek'] = dr_data['OrderWeek'] + timedelta(days=6)
dr_data['FullWeekCheck'] = dr_data.apply(lambda x: 'Yes' if x['EndOfOrderWeek'] <= x['MaxDate'] else 'No', axis=1)
dr_data['OrderMonth'] = dr_data['OrderDate'].apply(lambda x: x.replace(day=1))
dr_data['EndOfOrderMonth'] = dr_data['OrderMonth'] + relativedelta(months=1, days=-1)
dr_data['FullMonthCheck'] = dr_data.apply(lambda x: 'Yes' if x['EndOfOrderMonth'] <= x['MaxDate'] else 'No', axis=1)
dr_data['DayOfWeek'] = dr_data['OrderDate'].apply(lambda x: x.weekday()) + 1
dr_data['HasDiscount'] = dr_data['DiscountTotal'].apply(lambda x: 'Yes' if x != 0 else 'No')
dr_data['HasRebate'] = dr_data['Rebate'].apply(lambda x: 'Yes' if x != 0 else 'No')
dr_data['HasDeliveryFee'] = dr_data['DeliveryCost'].apply(lambda x: 'Yes' if x != 0 else 'No')
dr_data['HasTip'] = dr_data['Tip'].apply(lambda x: 'Yes' if x != 0 else 'No')

# Export Data
dr_data = dr_data[
    ['OrderDate', 'OrderTime', 'DayOfWeek', 'OrderWeek', 'FullWeekCheck', 'OrderMonth', 'FullMonthCheck', 'Location', 'Channel', 'OrderID', 'Type', 'Status', 'Cleaned Status',
     'HasDiscount', 'HasRebate', 'SubTotal', 'DiscountTotal', 'Rebate', 'Tip', 'DeliveryCost', 'PaymentAmount']]

dr_data = dr_data.sort_values(['OrderDate', 'OrderTime'])

dr_data.to_csv(r'H:\Shared drives\02 Finance\Dashboard\Source Data\Deliverect Data.csv', index=False)