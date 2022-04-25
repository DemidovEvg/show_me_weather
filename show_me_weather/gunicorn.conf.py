# Access log - records incoming HTTP requests
accesslog = "/var/www/jureti_project_1/show_me_weather/logs/gunicorn.access.log"
# Error log - records Gunicorn server goings-on
errorlog = "/var/www/jureti_project_1/show_me_weather/logs/gunicorn.error.log"
# Whether to send Django output to the error log
capture_output = True
# How verbose the Gunicorn error logs should be
loglevel = "debug"
