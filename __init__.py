from airflow.plugins_manager import AirflowPlugin

from tableau_plugin.hooks.tableau import TableauHook
from tableau_plugin.operators import TableauDSExtractRefreshOperator


class TableauPlugin(AirflowPlugin):
    name = "tableau_plugin"
    hooks = [TableauHook]
    operators = [TableauDSExtractRefreshOperator]

    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []
