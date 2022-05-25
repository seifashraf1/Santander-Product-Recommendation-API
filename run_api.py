from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd
from datetime import date
import model

app = Flask(__name__)

#api = Api(app, version='1.0', title='Recommender System API v1.0')


@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    employee_index = request.form.get('employee_index')
    country_residence = request.form.get('country_residence')
    sex = request.form.get('sex')
    age = request.form.get('age')
    province_name = request.form.get('province_name')

    # making some of the attributes dynamic and the rest of them are static, taken from the test_ver2 dataset
    customer_profile = pd.DataFrame([{
        'fecha_dato': "2016-06-28",
        'ncodpers': 15889,
        'ind_empleado': employee_index,
        'pais_residencia': country_residence,
        'sexo': sex,
        'age': age,
        'fecha_alta': "1995-01-16",
        'ind_nuevo': '0',
        'antiguedad': 256,
        'indrel': '1',
        'ult_fec_cli_1t': "",
        'indrel_1mes': '1.0',
        'tiprel_1mes': "A",
        'indresi': "S",
        'indext': "N",
        'conyuemp': "N",
        'canal_entrada': "KAT",
        'indfall': "N",
        'tipodom': 1,
        'cod_prov': 28.0,
        'nomprov': province_name,
        'ind_actividad_cliente': '1',
        'renta': 326124.90,
        'segmento': "03 - UNIVERSITARIO"
    }])

    # write the json object to csv file for the model to read
    print("Writing the customer profile to csv file...")
    customer_profile.to_csv('data/test_ver2.csv', index=True)

    # run the model
    print("Running the model...")
    banking_products = model.main()

    print("Returning the recommendations...")
    return banking_products["added_products"][0]


if __name__ == "__main__":
    app.run(host='localhost', port=5000)
