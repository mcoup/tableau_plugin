import tableauserverclient as tsc

from airflow.exceptions import AirflowConfigException, AirflowException
from airflow.hooks.base_hook import BaseHook


class TableauHook(BaseHook):
    """
    Interact with Tableau Online/ Server.

    :param tableau_conn_id: Tableau connection to use.
    :type tableau_conn_id: str
    """

    def __init__(self, tableau_conn_id):
        self.tableau_conn_id = tableau_conn_id
        self.client = None
        self.connect()

    def get_conn(self):
        self.log.debug('Creating tableau client')

        conn = self.get_connection(self.tableau_conn_id)
        if not conn.extra:
            raise AirflowConfigException('no extra options set for connection id: {}'.format(self.tableau_conn_id))

        extras = conn.extra_dejson

        site_uri = extras.get('site_uri', None)
        username = extras.get('username', None)
        password = extras.get('password', None)
        site_name = extras.get('site_name', None)

        tableau_auth = tsc.TableauAuth(username, password, site_name)
        tableau_server = tsc.Server(site_uri, use_server_version=True)

        tableau_server.auth.sign_in(tableau_auth)
        if not tableau_server.is_signed_in():
            raise AirflowConfigException('could not connect to tableau server')

        self.client = tableau_server

        return self.client

    def connect(self):
        if not self.client:
            self.get_conn()

    def get_datasource_by_name(self, datasource_name):
        """
        Gets tableau datasource item object by name.

        :param datasource_name: Name of the datasource including whitespace.
        :type  datasource_name: str
        :return: tableau datasource item object.
        :rtype: tableauserverclient.DatasourceItem
        """
        self.connect()

        for ds in tsc.Pager(self.client.datasources):
            if ds.name == datasource_name:
                return ds

        raise AirflowException("datasource with name: '{}' not found".format(datasource_name))

    def refresh_datasource(self, datasource_name):
        """
        Refreshes a tableau datasource extract.

        All refreshes are asynchronous! Meaning we won't poll for a success/ fail.

        :param datasource_name: Name of the datasource including whitespace.
        :type datasource_name: str
        """
        d = self.get_datasource_by_name(datasource_name)

        # @TODO: poll for success/ fail of refresh to avoid misrepresenting landing times in SLA functionality.
        self.client.datasources.refresh(d)
