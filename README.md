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
## Input data    
The observation data for the past year were extracted from the Cape Grim Baseline Air Pollution Station database in the form of one csv file per observation. The format of the file name is *[date].cgbaps.[chart name].[obs name].csv. These files are stored in the `cape-grim-dashboard/data` directory  
The specifications for each of the charts that are required was saved in a csv file and can be found in `pgm/CBAPS_Daily_Reports.csv`  

## Database  
The dashboard creates the MongoDB database *cg_data* to manage the data and the users  
  
### Collections  
- *charts* &emsp; specifies which observations to use in the chart and the chart text  
- *obs_data* &emsp; observation Time, Name, and Value  
- *users* &emsp; name, password,role, email for each registered user  
  
### Creating the database  
Run `flask init-db` to make the *cg_data* database and initialise the *users* collection with a default admin account  

### Configuration of the charts
Use the jupyter notebook  notebooks/make_chart_config.ipynb to clean up  `CGBAPS_Daily_Reports.csv` and `CGBAPS-DailyReportPlots.csv` and output `temp.csv`.  
Open the output file temp.csv, make any changes as required, for example the Legend and DataName might need to be modified to match the input data file names. Save edited file as `app/chart_config.csv` 

### Configuring the application 
The configurations for the app are found in the `app/.env` file. The  file needs to contain the following  

SECRET_KEY= your secret key 
DB_URL= URL to the MongoDB database  
DB_NAME= the name of the collection 
ADMIN_NAME= the name for the admin user that is installed by init-db 
ADMIN_PW= the password for the admin user that is installed by init-db 

## Loading the database
Run `pgm/load_charts.py charts` to generate the charts collection in the database  
- `app/chart_config.csv` &emsp; Input csv configuration file  

Run `pgm/load_data.py obs_data`  to load the observation data into the database. The input data file names need to match the names in chart_config.csv. The [Legend] string in `app/chart_config.csv` must match the [legend] part of the data csv file. 

## Making the charts  
Run `flask make-charts [start time as yyyy.mm.ddThh:mm:ss]` to output the charts as html files to `cape-grim-dashboard/charts` Any missing time [hh,mm,ss] fields in the date string are assumed to be zero.  







