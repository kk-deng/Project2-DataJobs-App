import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine= create_engine("postgres://irxrnnfx:8E4uvAlptBYdblhx20hS5t_elOsRbOxm@suleiman.db.elephantsql.com:5432/irxrnnfx")

Base = automap_base()
Base.prepare(engine, reflect=True)

# Set Tables to parameters
maintable = Base.classes.maintable
country = Base.classes.country
location = Base.classes.location
job = Base.classes.job
instituition = Base.classes.instituition
mentalhealth = Base.classes.mentalhealth

# Create session (link) from Python to the DB
session = Session(engine)

# SET UP FLASK
app = Flask(__name__)

# FRONT_END ROUTE
@app.route("/")
def main():
    return (

        render_template("index.html")

    )

# Dashboard ROUTE
@app.route("/dashboard")
def dashboard():
    return (

        render_template("dashboard.html")

    )

# Maps ROUTE
@app.route("/maps")
def maps():
    return (

        render_template("maps.html")

    )

# Word Cloud ROUTE
@app.route("/wordcloud")
def wordcloud():
    return (

        render_template("wordcloud.html")

    )

# Word Cloud ROUTE
@app.route("/rawdata")
def rawdata():
    return (

        render_template("rawdata.html")

    )

# SERVICE ROUTES

#---------------------------------------------------------------------------------------
# HEAT MAP - JOB POSTINGS and UNIVERSITY MARKERS
#---------------------------------------------------------------------------------------
@app.route("/api/jobs")
def heatmap(): 

    # Dataa for job postings
    job_data = session.query(maintable.job_id, job.job_title, country.country_name, location.city, location.state, location.lat, location.lng) \
                            .join(job, maintable.job_title_id == job.job_title_id) \
                            .join(country, maintable.country_id == country.country_id) \
                            .join(location, maintable.location_id == location.location_id)\
                            .all()

    dataset = []
    for item in job_data: 
        dataset.append(item)


    # Convert the query results to a dictionary 
    output= {"jobs" : [dataset]}

    return jsonify(output)

@app.route("/api/instituitions")
def instituitions():

    # Data for job postings
    instituition_data = session.query(instituition.institution, country.country_name)\
                        .join(country, instituition.country_id == country.country_id).all()

    dataset = []
    for item in instituition_data: 
        dataset.append(item)


    # Convert the query results to a dictionary 
    output= {"instituitions" : [dataset]}

    return jsonify(output)

#---------------------------------------------------------------------------------------
# GAUGE INDICATORS: BENEFITS AND WELLNESS
#---------------------------------------------------------------------------------------
@app.route("/api/benefits")
def benefits():

    # Set end_date and start_date
    benefits_data = session.query(mentalhealth.benefits, mentalhealth.state, country.country_name)\
                            .join(country, mentalhealth.country_id == country.country_id)\
                            .all()

    benefits_dataset = []

    for item in benefits_data: 
        benefits_dataset.append(item)


    # Convert the query results to a dictionary 
    output= {"Benefits" : benefits_dataset
            }

    return jsonify(output)

@app.route("/api/wellness_programs")
def wellness_programs():

    # Set end_date and start_date
    wellness_program = session.query(mentalhealth.wellness_program, mentalhealth.state, country.country_name)\
                                .join(country, mentalhealth.country_id == country.country_id)\
                                .all()

    wellness_dataset = []

    for item in wellness_program: 
        wellness_dataset.append(item)


    # Convert the query results to a dictionary 
    output= {"Wellness Program" : wellness_dataset
            }

    return jsonify(output)

#---------------------------------------------------------------------------------------
# BUBBLE CHART : EASE OF TAKING LEAVE
#---------------------------------------------------------------------------------------
@app.route("/api/leave")
def leave():

    # Set end_date and start_date
    leave_Data = session.query(mentalhealth.leave, mentalhealth.state, country.country_name)\
                                .join(country, mentalhealth.country_id == country.country_id)\
                                .all()


    leave_dataset = []
    for item in leave_Data: 
        leave_dataset.append(item)


    # Convert the query results to a dictionary 
    output= {"leave" : [leave_dataset]}

    return jsonify(output)

#---------------------------------------------------------------------------------------
# STACKED BAR CHART
#---------------------------------------------------------------------------------------
# Use jobs route from heatmap session

#---------------------------------------------------------------------------------------
# SUMMARY TABLE
# Selection by User:______
# Number of Data Analyst Jobs:______
# Number of Data Scientist Jobs:_____
# Number of Data Engineer Jobs:_____
# Number of ML Jobs:_______
#---------------------------------------------------------------------------------------
@app.route("/api/summary")
def summary():

    # Get selection from user?


    # Get total counts of Data Analyst jobs
    analyst_data = session.query(maintable.job_id, country.country_name, location.state) \
                            .join(job, maintable.job_title_id == job.job_title_id) \
                            .join(country, maintable.country_id == country.country_id) \
                            .join(location, maintable.location_id == location.location_id)\
                            .filter(job.job_title == "Data Analyst")\
                            # .group_by(country.country_name).count()
                       
    
    # Get total counts of Data Scientist jobs
    scientist_data = session.query(maintable.job_id, country.country_name, location.state)\
                            .join(job, maintable.job_title_id == job.job_title_id) \
                            .join(country, maintable.country_id == country.country_id) \
                            .join(location, maintable.location_id == location.location_id)\
                            .filter(job.job_title == "Data Scientist")\
                            # .group_by(country.country_name).count()

    # Get total counts of Data Engineer jobs
    engineer_data = session.query(maintable.job_id, country.country_name, location.state)\
                            .join(job, maintable.job_title_id == job.job_title_id) \
                            .join(country, maintable.country_id == country.country_id) \
                            .join(location, maintable.location_id == location.location_id)\
                            .filter(job.job_title == "Data Engineer")\
                            # .group_by(country.country_name).count()

    # Get total counts of ML jobs
    ml_data = session.query(maintable.job_id, country.country_name, location.state)\
                            .join(job, maintable.job_title_id == job.job_title_id) \
                            .join(country, maintable.country_id == country.country_id) \
                            .join(location, maintable.location_id == location.location_id)\
                            .filter(job.job_title == "Machine Learning")\
                            # .group_by(country.country_name).count()


    # dataset = []
    # for item in analyst_data: 
    #     dataset.append(item)

    analyst = []
    for item in analyst_data: 
        analyst.append(item)

    scientist = []
    for item in scientist_data: 
        scientist.append(item)

    engineer = []
    for item in engineer_data: 
        engineer.append(item)

    ml = []
    for item in ml_data: 
        ml.append(item)        

    # Convert the query results to a dictionary 
    output= {"Data Analyst" : [analyst],
            "Data Scientist": [scientist],
            "Data Engineer": [engineer],
            "Machine Learning": [ml]
            }


    return jsonify(output)

@app.route("/api/keywords")
def title_keywords():

    # A list for all jobs
    jobs_dict = {"Data Analyst" : 1,
            "Data Scientist": 2,
            "Data Engineer": 3,
            "Machine Learning": 4}

    # A function to count each job title keywords in the job name, return the list of frequencies
    def get_keywords_count(job_title_name):
        # Getting values from database queries with job titles
        query_titles = session.query(maintable.job_title)\
                            .filter(maintable.job_title_id == jobs_dict[job_title_name]).all()

        # Crete an empty list and a dict for frequency count
        list_title = []
        dict_output = {}

        # Create a table (remove not desired charaters) for the translate later
        table = str.maketrans(dict.fromkeys('0123456789()[].,-/&!@#$+:–\\'))

        # For each title (lowercased) in the query result, 
        # remove characters and append each keyword to the empty list
        for title in query_titles:
            new_title = title[0].lower().translate(table)
            list_title += (new_title.split(" "))


        # Count the frequency of each keyword in the list from above
        for item in list_title:
            if item != "":
                dict_output[item] = dict_output.get(item, 0) + 1
        
        return dict_output
    
    # Create an empty dict, iterate the title in jobs_dict to create a dict of results
    output_titles = {}
    for kw in jobs_dict:
        # Assign function returned value to a new key
        output_titles[kw] = get_keywords_count(kw)

    return jsonify(output_titles)


# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    # if request.method == "POST":
    #     name = request.form["petName"]
    #     lat = request.form["petLat"]
    #     lon = request.form["petLon"]

    #     pet = Pet(name=name, lat=lat, lon=lon)
    #     db.session.add(pet)
    #     db.session.commit()
    #     return redirect("/", code=302)

    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug = True)