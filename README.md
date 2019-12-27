# Plugin - Tableau
This Airflow plugin provides tableau online/ server interactions.

## Getting Started
### Installation
1. Add this folder to `$AIRFLOW_HOME/plugins`
2. Install requirements `pip3 install -r requirements.txt`

### Set-up
1. Add a connection using the airflow UI `Admin > Connections > Create`
2. Set `Conn Id` to `[YOUR CONN ID]` usually this is `tableau`
3. Add to `Extra` the following configration:

Example:

```
{
  "username":   "john.doe@example.com",
  "password":   "secret",
  "site_name":  "acme",
  "site_uri":   "https://dub01.online.tableau.com"
}
```

### Usage
Create a dag and use it like:
```
from tableau_plugin.operators import TableauDSExtractRefreshOperator

run_this = TableauDSExtractRefreshOperator(
    dag=dag,
    task_id="task1",
    tableau_conn_id='[YOUR CONN ID]',
    datasource_name='[YOUR DATASOURCE NAME]',
)
```

## Contributing
Kindly check the open issues and raise a PR where applicable.

## License
Apache 2.0.
