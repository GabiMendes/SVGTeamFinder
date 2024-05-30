from flask import Flask, render_template, jsonify, request, redirect, url_for
from concurrent.futures import ThreadPoolExecutor
import requests
import concurrent.futures

app = Flask(__name__)

API_KEY = 'test_66e02a7647ab45ca54f819fab08840'
BASE_URL = 'https://api.api-futebol.com.br/v1/'

def get_team_data(time_id):
    try:
        url = BASE_URL + f'times/{time_id}'
        headers = {'Authorization': f'Bearer {API_KEY}'}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        return data
    except Exception as e:
        print(f"An error occurred while getting data for team {time_id}: {e}")
        return None

def get_all_teams_data():
    all_teams_data = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_time_id = {executor.submit(get_team_data, time_id): time_id for time_id in range(100)}
        for future in concurrent.futures.as_completed(future_to_time_id):
            try:
                data = future.result()
                if data is not None:
                    all_teams_data.append(data)
            except Exception as e:
                print(f"An error occurred while getting result from future: {e}")

    return all_teams_data

def get_team_data_by_id(time_id):
    url = BASE_URL + f'times/{time_id}'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(url, headers=headers)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/times/all')
def get_all_teams():
    all_teams_data = get_all_teams_data()
    return render_template('times.html', times=all_teams_data)

@app.route('/times/<int:id_time>', methods=['GET'])
def get_time_by_id(id_time):
    team_data = get_team_data_by_id(id_time)
    if 'erro' in team_data:
        return render_template('time_especifico.html', error='Team not found')
    return render_template('time_especifico.html', time=team_data)

@app.route('/times/escudo/<int:id_time>', methods=['GET'])
def get_escudo(id_time):
    all_teams_data = get_all_teams_data()

    for team_data in all_teams_data:
        if team_data['time_id'] == id_time:
            escudo_url = team_data['escudo']
            return jsonify({'escudo_url': escudo_url})

    return jsonify({'error': 'Team not found'}), 404

@app.route('/times/escudo/imagem/<int:id_time>', methods=['GET'])
def redirect_to_escudo(id_time):
    all_teams_data = get_all_teams_data()

    for team_data in all_teams_data:
        if team_data['time_id'] == id_time:
            escudo_url = team_data['escudo']
            return redirect(escudo_url)

    return jsonify({'error': 'Team not found'}), 404

@app.route('/times/time', methods=['GET'])
def search_time_by_id():
    time_id = request.args.get('time_id', type=int)
    return redirect(url_for('get_time_by_id', id_time=time_id))

def get_team_data_by_name(team_name):
    all_teams_data = get_all_teams_data()

    for team_data in all_teams_data:
        if team_data['nome'] == team_name:
            return team_data

    return None

@app.route('/times/team_name', methods=['GET'])
def search_team_by_name():
    team_name = request.args.get('team_name', type=str)
    team_data = get_team_data_by_name(team_name)

    if team_data is not None:
        return redirect(url_for('get_time_by_id', id_time=team_data['time_id']))

    return jsonify({'error': 'Team not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
