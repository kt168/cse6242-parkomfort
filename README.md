# ParKomfort
CSE 6242 Project - Fall 2021

## DESCRIPTION
This package contains the flask web app for ParKomfort, Jupyter notebooks/python scripts for data analyses/data wrangling, as well as aggregated/cleaned datasets.

## INSTALLATION
To install the application locally:
   - Clone the git repository.
   - Use Python version 3.7 or higher.
   - Run `pip install -r requirements.txt` to install packages for flask web app.
   - Create a mapbox free-tier account at https://www.mapbox.com/ to get a personal access token. Create `.mapbox_token` file under `data` directory and store the personal access token inside `.mapbox_token` file.
   - Run the following command in the app's directory to run your web app.
    `python app/run.py`
   - Go to http://127.0.0.1:5000/ 

## EXECUTION
Once server is up and running, navigate to http://127.0.0.1:5000/. There are two main functions to this app:
- **HOME**: Homepage shows the precinct level vehicle larceny and crime data for NYC. It also offers interaction with the data. For example, clicking each precinct and click `Magnifying Glass` button will show the statistics for that precinct, such as monthly fluctions or year-on-year change.
- **SEARCH**: Search page offers the functionality to look up closest parking meters near destinations, taking risk level and search radius into account, thus offering customized user experience. For example, input `123 Main St NYC` into search box, user risk level = 2, and search radius = 4 miles, click `GO` button will initiate look up. The map will display the 10 closest parking meters. If risk level is changed to 1, redoing the search will return another set of 10 closest parking meters locations in a safer precinct.

## APPENDIX
- Link to demo video: https://youtu.be/8VuHE4yrtNg
- Access to the geopy encoded data (access via Gatech Office 365 account)
https://gtvault.sharepoint.com/:f:/s/CS6242/Eha_3E_6odROrKRdHvav1WUBY_Secmeu8m_DNkNw6ATv2Q?e=ngnuX4