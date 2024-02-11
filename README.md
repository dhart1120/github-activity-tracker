<p><a target="_blank" href="https://app.eraser.io/workspace/33sCr2vwTDjaBKFqHLCa" id="edit-in-eraser-github-link"><img alt="Edit in Eraser" src="https://firebasestorage.googleapis.com/v0/b/second-petal-295822.appspot.com/o/images%2Fgithub%2FOpen%20in%20Eraser.svg?alt=media&amp;token=968381c8-a7e7-472a-8ed6-4a6626da5501"></a></p>

# **Github Activity Tracker**
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
## Basic Architecture
![Initial Design](/.eraser/33sCr2vwTDjaBKFqHLCa___TjP6AZsOZLVedjA9LYrfglUMQCH2___---figure---3KwQkFK7_7DQf_7LryTYw---figure---PXS9QDibvvxzWK9fSKuMIA.png "Initial Design")




<!--- Eraser file: https://app.eraser.io/workspace/33sCr2vwTDjaBKFqHLCa --->