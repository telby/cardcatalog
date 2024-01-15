from flask import Flask, render_template, redirect, url_for, request, session
import csv
import os

app = Flask(__name__)
app.secret_key = '123456'  # Set a secret key for session management
CSV_FILE = r'D:\football\catalog\trading_cards.csv'

# Mapping of NFL team abbreviations to team names
team_mapping = {
    'ARI': 'Arizona Cardinals',
    'ATL': 'Atlanta Falcons',
    'BAL': 'Baltimore Ravens',
    'BUF': 'Buffalo Bills',
    'CAR': 'Carolina Panthers',
    'CHI': 'Chicago Bears',
    'CIN': 'Cincinnati Bengals',
    'CLE': 'Cleveland Browns',
    'DAL': 'Dallas Cowboys',
    'DEN': 'Denver Broncos',
    'DET': 'Detroit Lions',
    'GB': 'Green Bay Packers',
    'HOU': 'Houston Texans',
    'IND': 'Indianapolis Colts',
    'JAX': 'Jacksonville Jaguars',
    'KC': 'Kansas City Chiefs',
    'LV': 'Las Vegas Raiders',
    'LAC': 'Los Angeles Chargers',
    'LAR': 'Los Angeles Rams',
    'MIA': 'Miami Dolphins',
    'MIN': 'Minnesota Vikings',
    'NE': 'New England Patriots',
    'NO': 'New Orleans Saints',
    'NYG': 'New York Giants',
    'NYJ': 'New York Jets',
    'PHI': 'Philadelphia Eagles',
    'PIT': 'Pittsburgh Steelers',
    'SF': 'San Francisco 49ers',
    'SEA': 'Seattle Seahawks',
    'TB': 'Tampa Bay Buccaneers',
    'TEN': 'Tennessee Titans',
    'WAS': 'Washington Football Team',
}

# Default folder path (can be changed dynamically)
app.config['FOLDER_PATH'] = r'D:\football\catalog\static\images'

def write_to_csv(current_card, form_data):
    with open(CSV_FILE, 'a', newline='') as csvfile:
        fieldnames = ['card_id', 'front_image_path', 'back_image_path', 'year', 'brand', 'set_name', 'player_name', 'card_type', 'card_subtype', 'card_number', 'team', 'serial_number', 'position', 'rookie', 'autograph', 'memorabilia_relic']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            'card_id': current_card['card_id'],
            'front_image_path': current_card['front_image_path'],
            'back_image_path': current_card['back_image_path'],
            'year': form_data.get('year'),
            'brand': form_data.get('brand'),
            'set_name': form_data.get('set'),
            'player_name': form_data.get('player_name'),
            'card_type': form_data.get('card_type'),
            'card_subtype': form_data.get('card_subtype'),
            'card_number': form_data.get('card_number'),
            'team': form_data.get('team'),
            'serial_number': form_data.get('serial_number'),
            'position': form_data.get('position'),
            'rookie': form_data.get('rookie'),
            'autograph': form_data.get('autograph'),
            'memorabilia_relic': form_data.get('memorabilia_relic')
        })

@app.route('/')
def index():
    return render_template('index.html', folder_path=app.config['FOLDER_PATH'])

@app.route('/process_folder', methods=['GET', 'POST'])
def process_folder():
    folder_path = app.config['FOLDER_PATH']

    cards_data = get_cards_data(folder_path)

    if request.method == 'POST':
        current_card_index = int(request.form.get('current_card_index', 0))
        current_card = cards_data[current_card_index]
        team_abbreviation = current_card['card_id'].split('_')[0].upper()
        team_name = team_mapping.get(team_abbreviation, 'Unknown Team')
        
        if 'submit' in request.form:
            # Only process the form data when the submit button is pressed
            current_card_index += 1  # Increment the index after processing the current card
            write_to_csv(current_card, request.form)

        

    else:
        current_card_index = 0

    if current_card_index < len(cards_data):
        current_card = cards_data[current_card_index]
        return render_template('process_folder.html', current_card=current_card, current_card_index=current_card_index, team_name=team_name)
    else:
        return redirect(url_for('index'))

def get_cards_data(folder_path):
    cards_data = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith('_A.png'):
            card_id = file_name.replace('_A.png', '')
            front_image_path = os.path.join(folder_path, file_name)
            back_image_path = os.path.join(folder_path, f'{card_id}_B.png')
            cards_data.append({'card_id': card_id, 'front_image_path': front_image_path, 'back_image_path': back_image_path})

    return cards_data

@app.route('/submit_cards', methods=['POST'])
def submit_cards():
    return redirect(url_for('process_folder'))

if __name__ == '__main__':
    app.run(debug=True)