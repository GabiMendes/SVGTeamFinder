from flask import Flask, render_template, jsonify, request, redirect, url_for
from concurrent.futures import ThreadPoolExecutor
import requests
import concurrent.futures
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.api-futebol.com.br/v1/'

class API:
    def get_data(self, endpoint):
        url = BASE_URL + endpoint
        headers = {'Authorization': f'Bearer {API_KEY}'}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        return data

class TeamDataAPI(API):
    def get_team_data(self, time_id):
        return self.get_data(f'times/{time_id}')

    def get_all_teams_data(self):
        all_teams_data = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_time_id = {executor.submit(self.get_team_data, time_id): time_id for time_id in range(100)}
            for future in concurrent.futures.as_completed(future_to_time_id):
                try:
                    data = future.result()
                    if data is not None:
                        all_teams_data.append(data)
                except Exception as e:
                    print(f"An error occurred while getting result from future: {e}")

        return all_teams_data

team_data_api = TeamDataAPI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/times/all')
def get_all_teams():
    all_teams_data = team_data_api.get_all_teams_data()
    return render_template('times.html', times=all_teams_data)

@app.route('/times/<int:id_time>', methods=['GET'])
def get_time_by_id(id_time):
    team_data = team_data_api.get_team_data(id_time)
    if 'erro' in team_data:
        return render_template('not_found.html')
    return render_template('time_especifico.html', time=team_data)

@app.route('/times/escudo/<int:id_time>', methods=['GET'])
def get_escudo(id_time):
    all_teams_data = team_data_api.get_all_teams_data()

    for team_data in all_teams_data:
        if team_data['time_id'] == id_time:
            escudo_url = team_data['escudo']
            return jsonify({'escudo_url': escudo_url})

    return render_template('not_found.html')

@app.route('/times/escudo/imagem/<int:id_time>', methods=['GET'])
def redirect_to_escudo(id_time):
    all_teams_data = team_data_api.get_all_teams_data()

    for team_data in all_teams_data:
        if team_data['time_id'] == id_time:
            escudo_url = team_data['escudo']
            return redirect(escudo_url)

    return render_template('not_found.html')

@app.route('/times/time', methods=['GET'])
def search_time_by_id():
    time_id = request.args.get('time_id', type=int)
    return redirect(url_for('get_time_by_id', id_time=time_id))

@app.route('/times/team_name', methods=['GET'])
def search_team_by_name():
    team_name = request.args.get('team_name', type=str)
    all_teams_data = team_data_api.get_all_teams_data()

    for team_data in all_teams_data:
        if team_data['nome'] == team_name:
            return redirect(url_for('get_time_by_id', id_time=team_data['time_id']))

    return render_template('not_found.html')

if __name__ == '__main__':
    app.run(debug=True)