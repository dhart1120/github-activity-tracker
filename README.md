# Github Activity Tracker

This repo is a simple tool for getting and transforming Github Events. It's useful for building other tools or keep tabs on what has changed recently. Right now, it's pretty limited, but can be expanded in many ways. It can be run as a REST API or from a script if you just need to see the results.

This app currently only supports the repo events. 

This assumed you have `pyenv` installed.

```shell
# Activate the virtual env so you can use the correct version of python and limit pip to this project
source ./venv/bin/activate

# Starts the web service on localhost:5000
# The mapped endpoints are printed on startup
python main.py


# Alternatively, ef you can just run the scipt to see the results. You can change the filter for whatever you need, but don't commit the changes unless there is an improvement. 
python script.py
```