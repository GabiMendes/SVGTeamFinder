from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests

app = Flask(__name__)

API_KEY = ''
BASE_URL = 'https://api.api-futebol.com.br/v1/'

def get_all_times_data():
    all_times_data = []

    for time_id in range(10):
        url = BASE_URL + f'times/{time_id}'
        headers = {'Authorization': f'Bearer {API_KEY}'}

        response = requests.get(url, headers=headers)
        data = response.json()

        all_times_data.append(data)

    return all_times_data

def get_time_data_by_id(time_id):
    url = BASE_URL + f'times/{time_id}'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(url, headers=headers)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/times/all')
def get_all_times():
    all_times_data = get_all_times_data()
    return render_template('times.html', times=all_times_data)

@app.route('/times/<int:id_time>', methods=['GET'])
def get_time_by_id(id_time):
    time_data = get_time_data_by_id(id_time)
    if 'erro' in time_data:
        return render_template('time_especifico.html', error='Time não encontrado')
    return render_template('time_especifico.html', time=time_data)

@app.route('/times/escudo/<int:id_time>', methods=['GET'])
def get_escudo(id_time):
    all_times_data = get_all_times_data()

    for time_data in all_times_data:
        if time_data['time_id'] == id_time:
            escudo_url = time_data['escudo']
            return jsonify({'escudo_url': escudo_url})

    return jsonify({'error': 'Time não encontrado'}), 404

@app.route('/times/escudo/imagem/<int:id_time>', methods=['GET'])
def redirect_to_escudo(id_time):
    all_times_data = get_all_times_data()

    for time_data in all_times_data:
        if time_data['time_id'] == id_time:
            escudo_url = time_data['escudo']
            return redirect(escudo_url)

    return jsonify({'error': 'Time não encontrado'}), 404

@app.route('/times/time', methods=['GET'])
def search_time_by_id():
    time_id = request.args.get('time_id', type=int)
    return redirect(url_for('get_time_by_id', id_time=time_id))

if __name__ == '__main__':
    app.run(debug=True)
