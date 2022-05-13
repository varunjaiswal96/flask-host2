# from crypt import methods
from flask import Flask,render_template,request
import pickle
import pandas as pd

app=Flask(__name__)

model=pickle.load(open('savemodel.sav','rb'))

@app.route('/')
def home():
    result =''
    return render_template('index.html',**locals())

@app.route('/predict',methods=['POST','GET'])
def predict():
    dest=request.form['destination']
    origin=request.form['origin']
    date=request.form['date']
    time=request.form['time']
    # print(dest)
    # print(origin)
    # print(datetime)
    resulttemp = pd.DataFrame(predict_delay(date,time,origin,dest))
    result=model.predict_proba(resulttemp)[0][0]
    # model.predict_proba(resulttest1)[0][0]
    result = result*100
    return render_template('index.html',**locals())


def predict_delay(date_req,time_req, origin, destination):
    print('inside fun 1st line')
    # print(date)
    # print(time)
    from datetime import datetime

    try:
        departure_date_parsed = datetime.strptime(date_req, '%Y-%m-%d')
        departure_time_parsed = datetime.strptime(time_req, '%H:%M')
        print(departure_date_parsed)
        print(departure_time_parsed)
    except ValueError as e:
        return 'Error parsing date/time - {}'.format(e)

    month = departure_date_parsed.month
    day = departure_date_parsed.day
    day_of_week = departure_date_parsed.isoweekday()
    hour = departure_time_parsed.hour

    print("after parsing")
    print(month)
    print(day)
    print(day_of_week)
    print(hour)

    origin = origin.upper()
    destination = destination.upper()

    input = [{'MONTH': month,
              'DAY': day,
              'DAY_OF_WEEK': day_of_week,
              'CRS_DEP_TIME': hour,
              'ORIGIN_ORD': 1 if origin == 'ORD' else 0,
              'ORIGIN_DFW': 1 if origin == 'DFW' else 0,
              'ORIGIN_DEN': 1 if origin == 'DEN' else 0,
              'ORIGIN_CLT': 1 if origin == 'CLT' else 0,
              'ORIGIN_LAX': 1 if origin == 'LAX' else 0,
              'ORIGIN_IAH': 1 if origin == 'IAH' else 0,
              'ORIGIN_PHX': 1 if origin == 'PHX' else 0,
              'ORIGIN_SFO': 1 if origin == 'SFO' else 0,
              'ORIGIN_LGA': 1 if origin == 'LGA' else 0,
              'ORIGIN_LAS': 1 if origin == 'LAS' else 0,
              'ORIGIN_DTW': 1 if origin == 'DTW' else 0,
              'ORIGIN_MSP': 1 if origin == 'MSP' else 0,
              'ORIGIN_BOS': 1 if origin == 'BOS' else 0,
              'ORIGIN_SEA': 1 if origin == 'SEA' else 0,
              'ORIGIN_MCO': 1 if origin == 'MCO' else 0,
              'ORIGIN_DCA': 1 if origin == 'DCA' else 0,
              'ORIGIN_EWR': 1 if origin == 'EWR' else 0,
              'ORIGIN_JFK': 1 if origin == 'JFK' else 0,
              'ORIGIN_PHL': 1 if origin == 'PHL' else 0,
              # 'ORIGIN_SLC': 1 if origin == 'SLC' else 0,
              'ORIGIN_BWI': 1 if origin == 'BWI' else 0,
              'DEST_ORD': 1 if destination == 'ORD' else 0,
              'DEST_ATL': 1 if destination == 'ATL' else 0,
              'DEST_LAX': 1 if destination == 'LAX' else 0,
              'DEST_DEN': 1 if destination == 'DEN' else 0,
              'DEST_BOS': 1 if destination == 'BOS' else 0,
              'DEST_SFO': 1 if destination == 'SFO' else 0,
              'DEST_DFW': 1 if destination == 'DFW' else 0,
              'DEST_LAS': 1 if destination == 'LAS' else 0,
              'DEST_SEA': 1 if destination == 'SEA' else 0,
              'DEST_PHX': 1 if destination == 'PHX' else 0,
              'DEST_MCO': 1 if destination == 'MCO' else 0,
              'DEST_CLT': 1 if destination == 'CLT' else 0,
              'DEST_IAL': 1 if destination == 'IAH' else 0,
              'DEST_DTW': 1 if destination == 'DTW' else 0,
              'DEST_MSP': 1 if destination == 'MSP' else 0,
              'DEST_LGA': 1 if destination == 'LGA' else 0,
              'DEST_JFK': 1 if destination == 'JFK' else 0,
              'DEST_EWR': 1 if destination == 'EWR' else 0,
              'DEST_DCA': 1 if destination == 'DCA' else 0,
              'DEST_SAN': 1 if destination == 'SAN' else 0,
              'DEST_BNA': 1 if destination == 'BNA' else 0
              }]
    # return model.predict_proba(pd.DataFrame(input))[0][0]
    # return pd.DataFrame(input)
    return input

# def predict_delay(date_req, time_req, origin, destination):
#     from datetime import datetime

#     try:
#         departure_date_parsed = datetime.strptime(date_req, '%Y-%m-%d')
#         departure_time_parsed = datetime.strptime(time_req, '%H:%M')
#     except ValueError as e:
#         return 'Error parsing date/time - {}'.format(e)

#     month = departure_date_parsed.month
#     day = departure_date_parsed.day
#     day_of_week = departure_date_parsed.isoweekday()
#     hour = departure_time_parsed.hour

#     cols = []
#     for i in train_x.columns:
#         cols.append(i)

#     origin_cols = [i for i in cols if i.startswith('ORIGIN')]
#     dest_cols = [i for i in cols if i.startswith('DEST')]
  
#     input = {}
#     input['MONTH'] = month
#     input['DAY'] = day
#     input['DAY_OF_WEEK'] = day_of_week
#     input['CRS_DEP_TIME'] = hour

#     for i in origin_cols:
#         if i.endswith(origin):
#             input[i] = 1
#         else:
#             input[i] = 0
#     for i in dest_cols:
#         if i.endswith(destination):
#             input[i] = 1
#         else:
#             input[i] = 0
#     return([input])

# resulttemp = predict_delay('1/10/2018 21:45:00', 'LAX', 'ATL')

if __name__=='__main__':
    app.run(debug=True)