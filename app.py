import os
import sqlite3

import openai
import json
import requests
from flask import Flask, redirect, render_template, request, url_for, jsonify


app = Flask(__name__)

conn = sqlite3.connect('exercise_videos.db')
c = conn.cursor()

data = [('Floor Angels','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00025_floor_angels.mp4',True,True,False,False,False),
('Both Knees Into Chest','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00075_both_knees_into_chest.mp4',False,False,True,False,False),
('Single Knee Into Chest','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00076_single_knee_into_chest.mp4',False,False,True,False,False),
('Hamstring Nerve Thread','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00077_hamstring_nerve_thread.mp4',False,False,True,True,True),
('Inner Thigh Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00078_inner_thigh_stretch.mp4',False,False,True,True,False),
('Glute Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00079_glute_stretch.mp4',False,False,True,True,False),
('Open Book','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00080_open_book.mp4',True,True,True,False,False),
('Child Pose','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00081_child_pose.mp4',True,True,True,False,False),
('Low Back Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00082_low_back_stretch.mp4',False,False,True,False,False),
('IT Band Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00083_it_band_stretch.mp4',False,False,True,True,False),
('Dynamic Quad Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00084_dynamic_quad_stretch.mp4',False,True,True,True,False),
('Chest Wave Kneeling','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00085_chest_wave_kneeling.mp4',True,True,True,False,False),
('Chest Wave Standing','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00086_chest_wave_standing.mp4',True,True,True,False,False),
('Side to Side Knees','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00087_side_to_side_knees.mp4',False,False,True,True,False),
('Glute Dynamic Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00088_glute_dynamic_stretch.mp4',False,False,True,True,False),
('Chest Stretch with Twist','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00089_chest_stretch_twist.mp4',True,True,True,False,False),
('Chest Nerve Thread','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00090_chest_nerve_thread.mp4',True,True,False,False,False),
('Lat Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00091_lat_stretch.mp4',True,True,False,False,False),
('Butterfly','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00092_butterfly.mp4',False,False,True,True,False),
('Prone Quad Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00093_prone_quad_stretch.mp4',False,False,True,True,False),
('Worlds Greatest Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00094_world_greatest_stretch.mp4',False,True,True,True,False),
('Pigeon Pose','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00095_pigeon_pose.mp4',False,False,True,True,False),
('Down Dog Calf Peddling','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00096_down_dog_calf_peddling.mp4',False,True,True,True,True),
('Hip Impingement Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00097_hip_imp_stretch.mp4',False,False,True,True,False),
('Big Toe Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00120_big_toe_stretch.mp4',False,False,False,False,True),
('Plantarflexor Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00121_plantarflexor_stretch.mp4',False,False,False,False,True),
('Feet Openers','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00132_feet_openers.mp4',False,False,False,False,True),
('All Fours Thoracic Openers','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00177_all_4_thoracic_opener.mp4',False,True,False,False,False),
('Hand Behind Head T Spine Openers','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00178_hand_behind_head_t_spine_opener.mp4',False,True,False,False,False),
('Standing Hip Flexor Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00180_standing_hip_flexor_stretch.mp4',False,False,True,True,True),
('Seated Shoulder Circles','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00198_seated_shoulder_circles.mp4',True,True,False,False,False),
('Tricep Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00203_tricep_stretch.mp4',True,True,False,False,False),
('Shoulder Breathing Technique','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00216_shoulder_breathing_technique.mp4',True,True,False,False,False),
('Decompression Breathing','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00217_decompress_breathing.mp4',True,False,False,False,False),
('Foundation Breathing','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00218_foundation_breathing.mp4',False,False,True,False,False),
('Neck Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00219_neck_stretch.mp4',True,False,False,False,False),
('Wall Angels','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00225_wall_angels.mp4',True,True,False,False,False),
('Wall Shoulder Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00228_wall_shoulder_stretch.mp4',True,True,False,False,True),
('Wall Open Book','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00229_wall_open_book.mp4',True,True,True,False,False),
('Serratus wall slides','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00230_serratus_wall_slide.mp4',False,True,False,False,False),
('Serratus wall slides with foam roller','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00231_serratus_wall_slide_foam_roll.mp4',False,True,False,False,False),
('Wall Chest Wave','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00233_wall_chest_wave.mp4',True,True,False,False,False),
('Wall Chest Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00234_wall_chest_stretch.mp4',True,True,False,False,False),
('Kneeling Quad Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00238_kneeling_quad_stretch.mp4',False,False,True,True,False),
('Calf Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00239_calf_stretch.mp4',False,False,False,True,True),
('Hamstring Stretch (with foam roller)','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00259_hamstring_stretch_foam_roll.mp4',False,False,True,True,False),
('Seated 90/90 Hip Turns (one side)','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00264_seated_90_hip_turns_one_side.mp4',False,False,True,True,False),
('Seated 90/90 Hip Turns (hands down)','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00265_seated_90_hip_turns_hands_down.mp4',False,False,True,True,False),
('Seated 90/90 Hip Turns (hands up)','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00266_seated_90_hip_turns_hands_up.mp4',False,False,True,True,False),
('Seated 90/90 Hip Turns to Knees','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00267_seated_90_hip_turns_to_knees.mp4',False,False,True,True,False),
('Standing Shoulder Flexion','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00282_standing_shoulder_flexion.mp4',True,True,False,False,False),
('Standing Shoulder Extension','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00283_standing_shoulder_extension.mp4',True,True,False,False,False),
('Hamstring Stretch (flat back)','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00284_hamstring_stretch_flat_back.mp4',False,False,True,True,False),
('Standing Adductor Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00285_standing_adductor_stretch.mp4',False,False,True,True,False),
('Standing Adductor Stretch (hands down)','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00285_standing_adductor_stretch.mp4',False,False,True,True,False),
('Standing Adductor Stretch (intermediate)','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00286_standing_adductor_stretch_int.mp4',False,False,True,True,False),
('Standing Adductor Stretch (advanced)','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00287_standing_adductor_stretch_adv.mp4',False,False,True,True,False),
('Seated Arm Extension Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00288_seated_arm_extension.mp4',False,True,False,False,False),
('Seated Arm Extension Stretch (advanced)','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00289_seated_arm_extension_stretch_adv.mp4',False,True,False,False,False),
('Big Toe Stretch (advanced)','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00290_big_toe_stretch_adv.mp4',False,False,False,False,True),
('Big Toe Stretch (intermediate)','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00291_big_toe_strech_int.mp4',False,False,False,False,True),
('Seated Pigeon Pose','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00292_seated_pigeon_pose.mp4',False,False,True,True,False),
('Dynamic Hamstring Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00293_dynamic_hamstring_stretch.mp4',False,False,False,True,False),
('Dynamic Hip Flexor Stretch (with knee tap)','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00294_dynamic_hip_flexor_stretch_knee_taps.mp4',False,False,False,True,False),
('Deep Squat Retractions','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00295_deep_squat_retractions.mp4',False,False,False,True,False),
('Deep Squat With T Spine Rotation','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00296_deep_squat_t_spine_rotation.mp4',False,True,True,True,False),
('Crescent Lunge','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00334_crescent_lunge.mp4',False,False,False,True,False),
('Crescent Lunge','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00335_crescent_lunge_adv.mp4',False,False,False,True,False),
('Forward Fold','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00336_forward_fold.mp4',False,False,True,True,False),
('Standing Eagle Arms','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00337_standing_eagle_arms.mp4',True,True,False,False,False),
('Hamstring Flossing','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00338_hamstring_flossing.mp4',False,False,True,True,False),
('Dynamic Adductor Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00339_dynamic_adductor_stretch.mp4',False,False,True,True,False),
('Oblique Seiza Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00340_oblique_seiza_stretch.mp4',False,True,True,False,False),
('Seated Eagle Arm Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00341_seated_eagle_arm_stretch.mp4',False,True,False,False,False),
('Trunk Rotations','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00359_trunk_rotations.mp4',False,True,True,False,False),
('Butterfly and Shoulder Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00347_butterfly_shoulder_stretch.mp4',True,True,True,True,False),
('Butterfly and Chest Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00348_butterfly_chest_stretch.mp4',True,True,True,True,False),
('Supine Twist Hold','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00349_supine_twist_hold.mp4',True,True,True,False,False),
('Seated Inner Thigh Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00350_seated_inner_thigh_stretch.mp4',False,False,True,True,False),
('Hip Flexor and Chest Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00360_hip_flexor_chest_stretch.mp4',True,True,True,False,False),
('Neck Flexor Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00372_neck_flexor_stretch.mp4',True,False,False,False,False),
('Eagle Arms','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00381_eagle_arms.mp4',True,True,True,False,False),
('Chest and Neck Flexor Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00387_chest_neck_flexor_stretch.mp4',True,True,False,False,False),
('Standing Oblique Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00388_standing_oblique_stretch.mp4',False,True,True,False,False),
('TFL and IT Band Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00389_tfl_it_band_stretch.mp4',False,True,True,True,False),
('Standing Chest Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00390_standing_check_stretch.mp4',True,True,False,False,False),
('Inner Thigh and Shoulder Stretch','https://pancea-media.s3.us-west-1.amazonaws.com/1080p/00394_inner_thigh_shoulder_stretch.mp4',False,True,True,False,False)
]
c.execute('''CREATE TABLE IF NOT EXISTS exercises
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT,
              url TEXT,
              neck BOOLEAN,
              shoulder BOOLEAN,
              lower_back BOOLEAN,
              knee BOOLEAN,
              feet BOOLEAN)''')

# Insert the rows using the executemany() method
c.executemany('''INSERT INTO exercises (title, url, neck, shoulder, lower_back, knee, feet)
                  VALUES (?, ?, ?, ?, ?, ?, ?)''', data)

# Commit the changes to the database
conn.commit()

c.close()
conn.close()

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nPanceaAI: "
restart_sequence = "\nUser: "

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

# Define the route to handle the get_response request
@app.route('/get_response', methods=['POST'])
def get_response():
    # Get the user message from the request body
    user_message = request.json['user_message']
    # Get the message_thread from the request body
    message_thread = request.json['message_thread']
    
    # Make a call to the OpenAI GPT API to get the chatbot response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=generate_prompt(user_message, message_thread),
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" User:", " PanceaAI:"],
    )

    # Extract the chatbot response from the API response
    panceaAI_response = response.choices[0].text.strip()
    exercises = ""
    new_message_thread = ""
    # panceaAI_response = """Thank you for sharing that information with me. From what you've said, it sounds like you may be experiencing neck pain due to poor posture. I would recommend doing some stretches or exercises to help improve your posture and alleviate your pain. Here are some stretches that you can try:[DB_QUERY: {"discomfort_area":"neck", "discomfort_activity":"", "discomfort_level":""}]"""
    if 'DB_QUERY:' in panceaAI_response:
        # # Extract the query string between { and the }
        query_start = panceaAI_response.find('{')
        query_end = panceaAI_response.find('}', query_start) +1
        message_end = panceaAI_response.find("[DB_QUERY")
        query = panceaAI_response[query_start:query_end]
        truncated_response = panceaAI_response[:message_end]
        # Query our DB based on the query extracted from chatbot's response
        print("Here is the ", query)
        print(type(query))
        json_object = json.loads(query)
        print(type(json_object))
        exercises = get_exercises(query)
        # Add the user's message and the chatbot's truncated response to the message thread
        new_message_thread = add_message_to_thread(user_message, panceaAI_response, message_thread)
         # Return the chatbot response as a JSON object
        return jsonify({'panceaAI_response': truncated_response, 'exercises': exercises, 'message_thread': new_message_thread})  
    else :
        # Add the user's message and the chatbot's response to the message thread
        new_message_thread = add_message_to_thread(user_message, panceaAI_response, message_thread)
        # Return the chatbot response as a JSON object
        return jsonify({'panceaAI_response': panceaAI_response, 'exercises': exercises, 'message_thread': new_message_thread})

# call the DB to pull the exercises
def get_exercises(query):
    # Connect to the database
    conn = sqlite3.connect('exercise_videos.db')
    c = conn.cursor()
    query_object = json.loads(query)
    discomfort_area = query_object["discomfort_area"]
    da_query = ""
    if discomfort_area == "neck":
        da_query = '''SELECT DISTINCT * FROM exercises WHERE neck = true ORDER BY RANDOM() LIMIT 3'''
    elif discomfort_area == "shoulder":
        da_query = '''SELECT DISTINCT * FROM exercises WHERE shoulder = true ORDER BY RANDOM() LIMIT 3'''
    elif discomfort_area == "lower_back":
        da_query = '''SELECT DISTINCT * FROM exercises WHERE lower_back = true ORDER BY RANDOM() LIMIT 3'''
    elif discomfort_area == "knee":
        da_query = '''SELECT DISTINCT * FROM exercises WHERE knee = true ORDER BY RANDOM() LIMIT 3'''
    elif discomfort_area == "feet":
        da_query = '''SELECT DISTINCT * FROM exercises WHERE feet = true ORDER BY RANDOM() LIMIT 3'''
    else:
        da_query = '''SELECT DISTINCT * FROM exercises ORDER BY RANDOM() LIMIT 3'''

    # Query the videos table to get all the rows
    c.execute(da_query)
    exercises = []
    # Fetch all the rows and create a object with title and media
    rows = c.fetchall()
    for row in rows:
        content = {
            "title": row[1],
            "media": row[2]
        }
        exercises.append(content)

    # Close the cursor and connection
    c.close()
    conn.close()
    print(exercises)
    return exercises

# call the generate_prompt function to generate the prompt
def generate_prompt(user_message, message_thread):
    prompt = """You're an enthusiastic and empathetic Physical Therapist and Health Coach called PanceaAI who loves helping people live their best, most active lives. You're here to guide and support individuals on their journey towards better health and well-being. As a chatbot, your goal is to provide personalized advice, motivation, and practical tips to help users overcome physical challenges, improve their fitness, and optimize their overall wellness.
    Your tone should be uplifting and positive, offering encouragement and celebrating even small victories. You should be a reliable source of information, capable of explaining complex concepts in simple terms. Your responses should reflect empathy, understanding, and a genuine desire to help users feel better.
    Throughout your interactions, focus on building a rapport with users by showing genuine interest in their progress, asking about their goals, and tailoring your advice to their specific needs. Some of the information you should try to gather is listed below under User Information
    Feel free to incorporate light-hearted humor and engaging language to create a lively and enjoyable experience. Remember, your ultimate aim is to empower users, motivate them to stay active, and foster a sense of well-being. 
    When appropriate, you can offer exercises by generating a code snippet that will trigger a call to an exercise database. The code snippet should have the following format

        Example Code Snippet:
        [DB_QUERY: {"discomfort_area":"neck", "discomfort_activity":"turning_head", "discomfort_level":"8"}]

        User Information:
        - first name
        - discomfort area
        - discomfort activity
        - discomfort level

        choices for discomfort_area: neck, shoulder, lower_back, knee, feet
        choices for discomfort_levl: 1,2,3,4,5,6,7,8,9,10
    

        example prompt completion:  
        {prompt: my lower back hurts when I twist from side to side \n
        completion: I am sorry to hear that! Lets get you a few simple exercises that will help with your issue: [DB_QUERY: {"discomfort_area":"lower_back", "discomfort_activity":"twisting", "discomfort_level":""}]}
        """
        
    for message in message_thread:
        prompt += "\n User: " + message["user_message"] + "\n PanceaAI: " + message["panceaAI_response"]
    prompt += "\n User: " + user_message + "\n PanceaAI: "

    # print(prompt)
    return prompt 

# Define function to add message to thread
def add_message_to_thread(user_message, panceaAI_response, message_thread):
    # Create a dictionary to represent the new message
    new_message = {
        "user_message": user_message,
        "panceaAI_response": panceaAI_response
    }

    # Add the new message to the thread
    message_thread.append(new_message)

    return message_thread

#Call our email API to generate an email with the chat thread
@app.route('/submit_chat_thread', methods=['POST'])
def submit_chat_thread():
    #define endpoint
    url = 'https://dev.panceatech.com/feedback'

    message_thread = request.json['message_thread']

    #define request payload
    payload = {
        'email': 'dev+panceaAI@pancea.ai',
        'text': message_thread
    }
    
    #define request headers
    headers = {
        'Content-Type': 'application/json'
    }

    #Make the API call
    response = requests.post(url, json=payload, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # API call was successful
        data = response.json()
        # Process the data returned from the API call
        print(data)
        return jsonify(data)
    else:
        # API call failed
        print('API call failed with status code:', response.status_code)
        print('Error message:', response.text)
        return jsonify(response.status_code)
    