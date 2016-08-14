# Scraper Monitor
SONNT Aug 2016

## Install

- Install nginx: http://nginx.org/en/linux_packages.html
- Clone source code: $ git clone https://github.com/sonnguyenthai/scraper_monitor.git 
- Got to the project dir: $ cd scraper_monitor
- Install project:
    - Install python packages: $ pip install -r requirements.txt
    - Initiate db: $ python manage.py migrate
    - Load data: $ python manage.py loaddata sites
    
- For local run:
    - $ python manage.py runserver
    - C'est fini
    
- For production:
     - Build static files: $ python manage.py collectstatic
     - Edit scraper_monitor/settings.py to change:
        - DEBUG = False
        - ALLOWED_HOSTS = ["*"]
- Give nginx user permission to read/write/execute the project dir.
- Copy conf files to: 
    - supervisor conf dir: $ cp conf/scraper_monitor_sup.conf /etc/supervisor/conf.d/
    - nginx conf dir: $ cp conf/scraper_monitor_nginx.conf /etc/nginx/conf.d  . Please remove /etc/nginx/conf.d/default.conf to make it work
- Edit those files with correct project path in the server, also correct server name in nginx conf file.
- Restart nginx and supervisord:
    - $ service nginx restart
    - $ supervisorctl update (adding daemon without restart supervisord)
    
    
## Add scrapers:
- Go to Admin Panel in the site
- Click Add Scraper and enter:
    - Name: Optional. Whatever you want
    - Host Name: where the scraper is located
    - Port: port of the above host
    - Spider Name: Don't touch if you edit it in the scraper settings
    - Scraper Project Name: Don't touch if you edit it in the scraper settings
    
## Start/Stop
- When the scraper status is "Not running" you can start it Or start it again with "Finished" status
- Because the scraper run asynchronously, stop command will take a bit time (depends on number of processing requests) to really stop. You
will still see the scraper status is Running for a period of time. Please wait for the scraper finish its processing requests.