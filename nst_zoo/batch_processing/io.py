from nst_zoo.nst_main import main
from nst_zoo.config import NSTConfig

import json
import itertools
import click
from redis import Redis
redis_connection = None


def _get_redis_connection(host, port):
    global redis_connection
    if not redis_connection:
        redis_connection = Redis(host=host, port=port)
    return redis_connection


@click.group(name="nst-processor")
def cli():
    return


@cli.command()
@click.option(
    "--host",
    "-h",
    required=True,
    envvar="NST_REDIS_HOST",
    type=str,
    help="Redis host where list of trials exists"
)
@click.option(
    "--port",
    "-p",
    required=True,
    envvar="NST_REDIS_PORT",
    type=int,
    help="Redis port where list of trials exists"
)
@click.option(
    "--name",
    "-n",
    required=True,
    envvar="NST_REDIS_NAME",
    type=str,
    help="Redis name to lpop trials from"
)
def process_from_queue(host, port, name):
    redis = _get_redis_connection(host, port)
    config_kwargs = redis.lpop(name)

    while config_kwargs:
        main(NSTConfig(**json.loads(config_kwargs)))
        config_kwargs = _get_redis_connection(host, port)


@cli.command()
@click.option(
    "--config-filepath",
    "-fp",
    default="nst_zoo/batch_processing/data/config.json"
)
@click.option(
    "--host",
    "-h",
    required=True,
    envvar="NST_REDIS_HOST",
    type=str,
    help="Redis host where list of trials exists"
)
@click.option(
    "--port",
    "-p",
    required=True,
    envvar="NST_REDIS_PORT",
    type=int,
    help="Redis port where list of trials exists"
)
@click.option(
    "--name",
    "-n",
    required=True,
    envvar="NST_REDIS_NAME",
    type=str,
    help="Redis name to lpop trials from"
)
def send_to_queue(config_filepath, host, port, name):
    with open(config_filepath, "r") as fd:
        configs = json.load(fd)
    redis = _get_redis_connection(host, port)
    click.echo(
        redis.lpush(name, *[json.dumps(i) for i in _parameter_grid(configs)])
    )

def _parameter_grid(param_grid):
    """
    Inspired by sklearn.model_selection.ParameterGrid
    """
    # sort keys for reproducibility
    items = sorted(param_grid.items())
    if not items:
        yield {}
    else:
        keys, values = zip(*items)
        for v in itertools.product(*values):
            params = dict(zip(keys, v))
            yield params


@cli.command()
@click.option(
    "--host",
    "-h",
    required=True,
    envvar="NST_REDIS_HOST",
    type=str,
    help="Redis host where list of trials exists"
)
@click.option(
    "--port",
    "-p",
    required=True,
    envvar="NST_REDIS_PORT",
    type=int,
    help="Redis port where list of trials exists"
)
def flush(host, port):
    redis = _get_redis_connection(host, port)
    click.echo(
        redis.flushdb()
    )


if __name__ == '__main__':
    cli()
