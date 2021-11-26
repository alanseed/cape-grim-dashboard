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
    - `db.py`   
- pgm  
    - `CBAPS_Daily_Reports.csv`  
    - `load_data.py`  
    - `make_chart_config.py`  
- `cg-dash.py`  
- `README.md`  
- `requirements.txt`  
********  

## Database  
The dashboard creates the MongoDB database *cg_data* to manage the data and the users  
  
### Collections  
- *charts* &emsp; specifies which observations to use in the chart and the chart text  
- *obs_data* &emsp; observation Time, Name, and Value  
- *obs_names* &emsp; names of each of the observations  
- *users* &emsp; name, password,role, email for each registered user  
  
### Input data    
The observation data for the past year were extracted from the Cape Grim Baseline Air Pollution Station database in the form of one csv file per observation. The format of the file name is *[date].cgbaps.[chart name].[obs name].csv. These files are stored in the `cape-grim-dashboard/data` directory  
The specifications for each of the charts that are required was saved in a csv file and can be found in `pgm/CBAPS_Daily_Reports.csv`  
  
### Creating the database  
Use the Flask application function `flask init-db` to make the *cg_data* database and initialise the *users* collection with a default admin account  

Run `pgm/make_chart_config.py` to derive a list of the observations for each of the charts and output  
- `chart_config.csv` &emsp; for the configuration of each chart including a list of the observations for the chart, and  
- `obs_list.csv` &emsp; for the list of observations that were found in the data directory  

Run `pgm/load_data.py`  to load the chart configurations, the observation list, and the observation data into the database.  
The number of records per file varies from 2500 to 5,500,000, and loading the data from the larger files can take some time. The *obs_data* collection contains 77,818,990 documents and uses 5.4 GB of disk space. 




