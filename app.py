# Standard library imports
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import os
import unicodedata

# Third party imports
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.api-futebol.com.br/v1/'

class API:
    """A class to interact with the API."""

    def get_data(self, endpoint):
        """
        Fetch data from the API for a given endpoint.

        Args:
            endpoint (str): The endpoint of the API to fetch data from.

        Returns:
            dict: The data returned from the API.
        """
        url = BASE_URL + endpoint
        headers = {'Authorization': f'Bearer {API_KEY}'}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        return data

class TeamDataAPI(API):
    """A class to fetch team data from the API."""

    def get_team_data(self, time_id):
        """
        Fetch data for a specific team.

        Args:
            time_id (int): The ID of the team to fetch data for.

        Returns:
            dict: The data for the team.
        """
        return self.get_data(f'times/{time_id}')

    def get_all_teams_data(self):
        """
        Fetch data for all teams.

        Returns:
            list: A list of data for all teams.
        """
        all_teams_data = {}
    
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_time_id = {executor.submit(self.get_team_data, time_id): time_id for time_id in range(5)}
            for future in concurrent.futures.as_completed(future_to_time_id):
                try:
                    data = future.result()
                    if data is not None:
                        all_teams_data[data['time_id']] = data
                except Exception as e:
                    print(f"An error occurred while getting result from future: {e}")
    
        return list(all_teams_data.values())

team_data_api = TeamDataAPI()

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/times/all')
def get_all_teams():
    """Render a page with data for all teams."""
    all_teams_data = team_data_api.get_all_teams_data()
    return render_template('times.html', times=all_teams_data)

@app.route('/times/<int:id_time>', methods=['GET'])
def get_time_by_id(id_time):
    """
    Render a page with data for a specific team.

    Args:
        id_time (int): The ID of the team to fetch data for.
    """
    team_data = team_data_api.get_team_data(id_time)
    if 'erro' in team_data:
        return render_template('not_found.html')
    return render_template('time_especifico.html', time=team_data)

@app.route('/times/escudo/<int:id_time>', methods=['GET'])
def get_escudo(id_time):
    """
    Get the URL of the shield for a specific team.

    Args:
        id_time (int): The ID of the team to fetch the shield URL for.

    Returns:
        str: The URL of the team's shield.
    """
    all_teams_data = team_data_api.get_all_teams_data()

    for team_data in all_teams_data:
        if team_data['time_id'] == id_time:
            escudo_url = team_data['escudo']
            return jsonify({'escudo_url': escudo_url})

    return render_template('not_found.html')

@app.route('/times/escudo/imagem/<int:id_time>', methods=['GET'])
def redirect_to_escudo(id_time):
    """
    Redirect to the URL of the shield for a specific team.

    Args:
        id_time (int): The ID of the team to redirect to the shield URL for.
    """
    all_teams_data = team_data_api.get_all_teams_data()

    for team_data in all_teams_data:
        if team_data['time_id'] == id_time:
            escudo_url = team_data['escudo']
            return redirect(escudo_url)

    return render_template('not_found.html')

def remove_accents(input_str):
    """
    Remove accents from a string.

    Args:
        input_str (str): The string to remove accents from.

    Returns:
        str: The string with accents removed.
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode()

@app.route('/times/team_name', methods=['GET'])
def search_team_by_name():
    """Search for a team by name and render a page with the team's data."""
    team_name_or_sigla = remove_accents(request.args.get('team_name', type=str).lower())
    all_teams_data = team_data_api.get_all_teams_data()

    for team_data in all_teams_data:
        if team_name_or_sigla in remove_accents(team_data['nome'].lower()) or team_name_or_sigla in remove_accents(team_data['sigla'].lower()):
            return render_template('time_especifico.html', time=team_data)

    return render_template('not_found.html')

if __name__ == '__main__':
    app.run(debug=True)