Go into the dashboard folder and run the following code to get the sebsite running on your local server. 

    python manage.py runserver

**TODO:** Maybe change the nvidia jetson to a raspberry pi 3 (which is what we are using). [homepage.html]

Login and Signup pages are working as intended.  [login.html , signup.html  in the registration folder]

For the dashboard [base.html] is a template which contains the navigation bar and the side menu. 

On logging in, dashboard homepage is the sensor data, which shows the current data for the four sensors. [sensordata.html]

The side menu also has options to show individual sensor data in four different pages, [sensor1.html , sensor2.html , sensor3.html , sensor4.html]

Each individual sensor page shows the following:
1. The current sensor data (also shown on dahsboard home)
2. The water reading (1 for suitable, 0 for unsuitable) 
3. Any errors (1 for error, 0 for no error)

**TODO:** The extra pages such as recovery of password, changing of password and so on are currently linked to a 404 page [404.html] . 

## Working

*views.py* is the main python file where the backend functions are implemented. 

The working of these functions have been documented in the functions itself (check the comments in *views.py*)

Data is taken from the Firebase using a config file. The testing config is the one being used right now and it would be better to not change that even for the final evaluation.

In firebase, data is stored as:

    ---Username
        |
        Key
            |
            "sensor1": data
            "sensor2": data
            "sensor3": data
            "sensor4": data
            "time": time
        |
        Key
            |
            "sensor1": data
            "sensor2": data
            "sensor3": data
            "sensor4": data
            "time": time
and so on...


The username is the one to be used for logging into our dashboard. 
**The code searches under the current user's username in  firebase.**

After the data has been fetched, it is preprocessed. Any negative values ( corresponding to any sensor errors ) are converted are reported back using the *get_indices()* function  . 

**TODO:** Currently, the *check()* function is used to 'check' whether the water is suitable or not based on the sensor datas. Average of the data is taken, if there is an error, then that value is ignored and so on. **Threshold for classification has been set to 0.4** 

The graphs in the website take the newest 15 values to plot. 

## Artificial Data 

A notebook that randomly sends sensor data every 5 seconds to firebase is also included. Credentials for the capstone google account (on which firebase) is running is also mentioned there. 


