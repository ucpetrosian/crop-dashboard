<b> Quick Start Guide to the Flux Dashboard. </b>

<i> What will you need? </i>
- Access to UC Davis Box
- Python 3.11 (packages in requirement.txt)
- (Optional) I use PythonAnywhere to host the app

<i> How to get the dashboard set up locally </i>
- Clone this repository to your system (I use Github Desktop).
- Run <b> daily_dashboard_data_update.py </b> on your system.
- Run <b> main.py </b> on your system. It should be accessible via <b> http://127.0.0.1:8050/dash/ </b>
- Both scripts are commented and require little set-up from user.

<i> General Notes About Repository </i>
- <b> reload_app.py </b> is a script I run on my computer every day after pulling new data to reset the app.
- The "read-in-csvs" folder contain static files that contain information about the equipment the towers use and the location of the towers.
- The "sample-data" folder contains data from the last month of collection from our towers via the dataloggers.
- Lynn is responsible for SLM_001, VOK_001, RIP_722, RIP_760 and Mina (mina.swintek@usda.gov) is responsible for the data collection of all other sites.
- Info about app deployment/hosting can be provided upon request.

If you have any questions about methods or data please feel free to email myself (crpetrosian@ucdavis.edu) or Mina for questions.

