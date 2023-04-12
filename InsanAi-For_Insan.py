#
يتضمن الكود التالي إجراء العمليات الطارئة الحرجة 
في حالات السقوط والإغماء وإرشادات للتواصل مع #مستشفى_إنسان 
والتواصل مع الجيران والمسعفين، واستخدام إشارات الضوء والصوت، وتسجيل ما يحدث، وإرسال 
الملفات عبر شبكة #إنسانشين بتقنية ما بعد البلوكشين
التي طورتها شركة #إنسان_التقنية بقيادة المهندس عبدالله إسلام بن الحسن

The code for conducting critical emergency operations in cases of falls and fainting includes guidelines for contacting 
#Insan_Hospital, communicating with neighbors and paramedics, using light and sound signals, recording what happens, and 
sending files through our #Insanchain post-blockchain network, developed 
By #Insan_Technology Company and led by Eng. Abdullah Islam bin ElHassan
#

import time
import board
import digitalio
import adafruit_adxl34x
from insantechnology
import InsanAPI
import Insanchain
import requests
import numpy as np
import sounddevice as sd
import soundfile as sf
import firebase_admin
from firebase_admin 
import credentials, messaging
import googlemaps
from datetime 
import datetime
import matplotlib.pyplot as plt

threshold_acceleration = 30

fall_detection_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])

insan_api = InsanAPI("YOUR_API_KEY")

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

gmaps = googlemaps.Client(key="YOUR_API_KEY")

def send_alert(location):
    requests.post(
        "https://api.insantechnology.com/send_sms",
        data={
            "phone_number": "01200098000",
            "message": f"Fall detected for Insan person. Location: {location}. Please check InsanChain for medical report and audio recording."
        }
    )
    requests.post(
        "https://api.insantechnology.com/send_sms",
        data={
            "phone_number": "01200098000",
            "message": f"Fall detected for Insan person. Location: {location}. Please check InsanChain for medical report and audio recording."
        }
    )

def check_fall():
    i2c = board.I2C()
    int_pin = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
    acceleration_sensor = adafruit_adxl34x.ADXL345(i2c, int_pin=int_pin)

acceleration = np.array(acceleration_sensor.acceleration)
    acceleration_in_fall_detection_space = fall_detection_matrix.dot(acceleration)
    magnitude_of_acceleration_in_fall_detection_space = np.linalg.norm(acceleration_in_fall_detection_space)

    if magnitude_of_acceleration_in_fall_detection_space > threshold_acceleration:
        report = f"Medical report for Insan person:\n\nFall detected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        print(report)
        insan_api.send_report(report)
        send_alert(get_location())
        record_audio()
        send_push_notification(get_location())
        plot_acceleration(acceleration)

def plot_acceleration(acceleration):
    fig, ax = plt.subplots()
    x = np.arange(3)
    ax.bar(x, acceleration)
    ax.set_xticks(x)
    ax.set_xticklabels(('x', 'y', 'z'))
    ax.set_ylabel('Acceleration (m/s^2)')
    fig.savefig('acceleration.png')

def get_location():
    location = gmaps.geolocate()
    return f"{location['latitude']}, {location['longitude']}"

def record_audio():
    duration = 5
    sample_rate = 44100
    channels = 2

    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)

    sd.wait()

    sf.write("audio.wav", recording, sample_rate)

def send_push_notification(location):
    message = messaging.Message(
        notification=messaging.Notificatication            title="Fall detected for Insan person",
            body=f"Location: {location}. Please check InsanChain for medical report and audio recording."
        ),
        topic="Insan_fall_detection"
    )

    response = messaging.send(message)

while True:
    check_fall()
    time.sleep(5)
