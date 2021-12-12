# cape-grim-dashboard
Web page to view the data collected at the Cape Grim Baseline Air Pollution Station
********   

## Directory structure 
- app  
    - auth  
        - `__init__.py`  
        - `auth.py`  
        - `forms.py`  
    - main  
        - `__init__.py`  
        - `main.py`  
        - `chart.py`
    - static  
        - `style.css`   
    - templates  
        - auth  
            - `login.html`  
            - `register.html`  
        - main  
            - `__init__.py`  
            - `main.py`  
        - `main_base.html`  
        - `user_base.html`
    - `__init__.py`  
    - `config.py`  
    - `db.py`  
    - `chart_config.csv`  
    -    
- instance  
- notebooks  
- pgm  
    - `CBAPS_Daily_Reports.csv`  
    - `load_data.py`  
    - `make_chart_config.py`  
- `cg-dash.py`  
- `README.md`  
- `requirements.txt`  
********  
## Input data provided   
The observation data for the past year were extracted from the Cape Grim Baseline Air Pollution Station database in the form of one csv file per observation. 

The specifications for each of the charts that are required were provided by the `pgm/CBAPS_Daily_Reports.csv` and  `CGBAPS-DailyReportPlots.csv`  files.  

## Database  
The dashboard creates the MongoDB database *cg_data* to manage the data and the users  
  
### Collections  
- *charts* &emsp; specifies which observations to use in the chart and the chart text  
- *chart_data* &emsp; cache of chart data ready to be displayed by Plotly  
- *obs_data* &emsp; observation Time, Name, and Value  
- *users* &emsp; name, password,role, email for each registered user  
  
### Creating the database  
Run `flask init-db` to make the *cg_data* database and initialise the *users* collection with a default admin account  

### Configuring the application 
The configurations for the app are found in the `app/.env` file. The file needs to contain the following  

SECRET_KEY= your secret key 
DB_URL= URL to the MongoDB database  
DB_NAME= the name of the collection 
ADMIN_NAME= the name for the admin user that is installed by init-db 
ADMIN_PW= the password for the admin user that is installed by init-db 

## Loading the database
Data for the demo are found in the demo directory  

Configuration for the charts is found in `/demo/chart_config.csv`. This configuration was built using the Notebook script  
`make_chart_config.ipnb` and then manually edited to make it an exact match for the input data files. 

### Demo data set
A demo sub-set of the data was generated using `/pgm/export_data.py`   
The data are for the period 1-10 July 2021 

Time series data that are compatible with the chart configurations are found in 
`demo/[Start time].cgbaps.[chart name].[legend name].csv` 

Run `pgm/load_data.py` to load the demo data into the `cg-demo` collection at URI "mongodb://localhost:27017/"   

## Making the chart cache   
There are 2 ways to generate the charts in the cache: 
Run `flask make-charts [start time as yyyy.mm.dd]`, or  
Start the dashboard and logon as admin and use the 'Add charts' tab to select a day  







