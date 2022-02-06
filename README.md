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
## Dependencies  
Python 3.10 
MongoDB   
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

## Configuring the Python environment 
The Python environment is managed by venv and the environment requirements are found in the `requirements.txt` file   
From the `cape-grim-dashboard`  
`python3 -m pip install --upgrade pip` to make sure that you are using the latest pip installer 
`python -m venv venv` to generate the virtual environment for the application, then   
`source venv/bin/activate` to activate the environment (LINUX)  or `source venv/Scripts/activate` if using bash on windows  
`pip install -r requirements.txt` to load the required environment  

## Configuring the application   
Add your configuration settings    
Create a `.env` file in the `app` directory with the following  

SECRET_KEY= your secret key   
DB_URI='mongodb://localhost:27017'&emsp; - URI to the MongoDB database   
DB_NAME='cg_demo'&emsp; - the name of the collection   
ADMIN_NAME='admin'&emsp; - the name for the admin user that is installed by init-db   
ADMIN_PW='admin'&emsp;- the password for the admin user that is installed by init-db   

## Creating the database  
Run `flask init-db` to make the *cg_data* database and initialize the *users* collection with a default admin account  

## Loading the demo data set 
A data  for the period 1-10 July 2021 can be found in the `demo` directory  
Run `pgm/load_data.py` to load the demo data into the `cg-demo` collection at URI `mongodb://localhost:27017/`     
Run `flask make-charts 2021-07-01` etc to load up the chart cache  

## Making the chart cache   
There are 2 ways to generate the charts in the cache:   
`cd cape-grim-dashoard` change diectory to the base directory  
`source venv/bin/activate` to set up the Python environment  
`flask make-charts [date]` where date is yyyy-mm-dd 

If the mongo database is local then  
Start the dashboard and logon as admin and use the 'Add charts' tab to select a day if the database is local.  

## Runing the web page  
### Development web page on local host  
`cd cape-grim-dashoard` change diectory to the base directory  
`flask run`  run the web page then  
Use your web browser to open the url `http://127.0.0.1:5000` or `localhost:5000` to view the dashboard  

### Running operational web page  
`cd cape-grim-dashoard` change diectory to the base directory  
`source venv/bin/activate` to set up the Python environment  
`pip install gunicorn` to install the gunicorn package to run the flask application 

You will need to copy `venv/bin/gunicorn` to `/usr/local/bin/gunicorn` so that it can be run by systemd 

More details on how to set up gunicorn for linux can be found at this [tutorial](https://www.edmondchuc.com/deploying-python-flask-with-gunicorn-nginx-and-systemd)  

Examples of the configuration files needed for a virtual machine (EC2) can be found in the `config` directory  
where  
`cgdash.service` is the configuration for setting up `systemctl` and  
`nginx.conf` sets up the proxy server needed for external access to the web page  

Details of setting up the nginx service can be found in the [beginners guide](https://nginx.org/en/docs/beginners_guide.html)  

Use the example `config/nginx.conf` file to edit the server block in `/etc/nginx/nginx.conf` file so that it includes the details for the cgdash service as needed  

Set up the root directory and logs for the web site  
`sudo mkdir -p /var/www/cgdash/`  
`sudo midir -p /var/log/nginx/cgdash`    

Set up the SE context for the root of the web page:  
`sudo semanage fcontext -a -t httpd_sys_content_t "/var/www/cgdash(/.*)?"`  
`sudo restorecon -Rv /var/www/cgdash/`  

Tell nginx that we want to forward messages  
`sudo setsebool -P httpd_can_network_connect 1`     

Then re-start Nginx with the new configuration  
`sudo systemctl restart nginx`  

You should be able to view the cgdash web page 
`http://localhost/main/met`  

Have not worked out yet how to get a signed certificate so that we can use https  

 
