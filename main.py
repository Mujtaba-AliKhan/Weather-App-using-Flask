from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    unit = request.form.get('unit-toggle')

    if unit:
        unitValue = "F"
        units = "imperial"
        distanceUnit = "MPH"
    else:
        unitValue = "C"
        units = "metric"
        distanceUnit = "mtrs/s"

    unit = unit == 'true'

    api_key = '76a137b18cdbbd073e4aa6bdac72ac71'

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_data = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'].upper(),
            'feels_like': data['main']['feels_like'],
            'wind_speed': data['wind']['speed'],
            'min_temp': data['main']['temp_min'],
            'max_temp': data['main']['temp_max'],
            'visibility': int(data['visibility']) / 1000,
            'background_image': data['weather'][0]['main'].lower() + '.jpg',
            'weather_icon': data['weather'][0]['main'].lower() + '.svg',
            'unitValue': unitValue,
            'distanceUnit': distanceUnit,
        }

        return render_template('weather.html', weather=weather_data, allweather=data)
    else:
        error_message = f"Error: '{city}' does not exists in our database"
        return render_template('error.html', message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
