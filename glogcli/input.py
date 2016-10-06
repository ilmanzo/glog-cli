import getpass
import click
from glogcli.utils import cli_error
from glogcli import utils


class CliInterface(object):

    @staticmethod
    def select_stream(graylog_api, stream):
        is_admin = graylog_api.user["permissions"] == ["*"] or 'Admin' in graylog_api.user["roles"]
        stream = stream if stream is not None else graylog_api.default_stream

        if not stream:
            streams = graylog_api.streams()["streams"]
            click.echo("Please select a stream to query:")
            for i, st in enumerate(streams):
                stream_id = st["id"].encode(utils.UTF8)
                message = "{}: Stream '{}' (id: {})".format(i, st["title"].encode(utils.UTF8), stream_id)
                click.echo(message)

            if is_admin:
                message = "{}: Stream '{}'".format(len(streams), 'All Streams')
                click.echo(message)

            stream_index = click.prompt("Enter stream number:", type=int, default=0)

            if stream_index < len(streams):
                stream = streams[stream_index]["id"]
            elif stream_index >= len(streams) and not is_admin:
                CliInterface.select_stream(graylog_api, stream)

        if stream and stream != '*':
            return "streams:{}".format(stream)

    @staticmethod
    def select_saved_query(graylog_api):
        searches = graylog_api.get_saved_queries()["searches"]
        if not searches:
            cli_error("You have no saved queries to display.")

        for i, search in enumerate(searches):
            search_title = search["title"].encode(utils.UTF8)
            query = search["query"]["query"].encode(utils.UTF8) or "*"
            message = "{}: Query '{}' (query: {})".format(i, search_title, query)
            click.echo(message)
        search_index = click.prompt("Enter query number:", type=int, default=0)
        search = searches[search_index]
        query = search['query']['query'].encode(utils.UTF8) or '*'
        fields = search['query']['fields'].encode(utils.UTF8).split(',')
        return query, fields

    @staticmethod
    def prompt_password(host, port, username):
        prompt_message = "Enter password for {username}@{host}:{port}".format(username=username, host=host, port=port)
        return click.prompt(prompt_message, hide_input=True)

    @staticmethod
    def prompt_username(host, port):
        return click.prompt("Enter username for {host}:{port}".format(host=host, port=port), default=getpass.getuser())