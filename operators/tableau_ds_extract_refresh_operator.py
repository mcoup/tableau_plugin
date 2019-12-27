from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from tableau_plugin.hooks.tableau import TableauHook


class TableauDSExtractRefreshOperator(BaseOperator):
    """
    Tableau Datasource Extract Refresh Operator.

    :param tableau_conn_id:           The input tableau connection id.
    :type tableau_conn_id:            str
    :param datasource_name:   The name, including whitepaces, of the tableau datasource.
    :type datasource_name:    str
    """

    def __init__(self,
                 tableau_conn_id,
                 datasource_name,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.tableau_conn_id = tableau_conn_id
        self.datasource_name = datasource_name

    def execute(self, context):
        hook = TableauHook(tableau_conn_id=self.tableau_conn_id)
        hook.refresh_datasource(self.datasource_name)
