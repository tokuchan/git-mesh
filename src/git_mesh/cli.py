import logging
import sh
import click
import logging

from rich import print
from rich.traceback import install

install(show_locals=True)


@click.group
@click.pass_context
@click.option(
    "-d/-D",
    "--dry-run/--no-dry-run",
    help="Don't actually do anything, just log what I would have done.",
)
@click.option('-v','--verbose',help='Increase logging verbosity',count=True)
@click.option('-q','--quiet',help='Decrease logging verbosity',count=True)
def cli(context: click.Context, dry_run: bool, verbose: int, quiet: int):
    """
    Sync changes between git repositories in a nonintrusive manner.
    """
    logging_level= logging.WARN - (10 * verbose) + (10 * quiet)
    logging.basicConfig(level=logging_level)
    log= logging.getLogger('git-mesh.cli')
    log.info('Configuring system')
    log.debug('Creating global context')
    context.obj = dict()
    log.debug('Processing global options')
    context.obj["dry_run"] = dry_run


@cli.command
@click.pass_obj
@click.option(
    "-i", "--pull-remote", help="Specify a remote to sync changes from.", multiple=True
)
@click.option(
    "-o", "--push-remote", help="Specify a remote to sync changes to", multiple=True
)
@click.argument("refname")
def sync(obj: dict, pull_remote: list[str], push_remote: list[str], refname):
    """
    Synchronize the specified branches with the specified remotes.

    The synchronization process
    ===========================

    All synchronization activity takes place against a "sync" branch, with the
    same name as the "ref" branch you specify. This allows us to retain atomic
    semantics w.r.t. your work. That is, all pull syncs take place sctrictly
    before I attempt to merge that work into your ref branch. It also means
    that all push syncs take place after I have merged your ref branch back to
    the sync brannch.

    A pull sync consists of fetching the sync branch from a remote, then
    atomically merging the changes with the sync branch. Each such merge commit
    is labeled with the phrase "PULL-SYNC: <remote-name>:<branch-name>". I
    perform a pull sync for each pair of branch and remote you specify.

    A local sync consists of merging the sync branch to the ref branch, then
    merging the ref branch back to the sync branch. Each local sync merge
    commit is labeled with the phrase "LOCAL-SYNC: sync->ref", or "LOCAL-SYNC:
    ref->sync" as appropriate.

    A push sync consists of pushing the sync branch to each of the specified
    remotes. No additional merge commits are created, of course.
    """
    log= logging.getLogger('git-mesh.sync')
    if(obj['dry_run']):
        log.warn('Not actually syncing')
    else:
        log.info('Synching data')


@cli.command
@click.pass_obj
@click.argument("refname")
@click.argument("remote", nargs=-1)
def push(obj: dict, refname: str, remote: list[str]):
    """
    Given a (required) refname, and optional remote, sync changes.

    There are two modes push can operate in: local or remote.

    In local mode, this command merges changes from the refname to the
    corresponding sync refname, creating it if needed.

    In remote mode, this command pushes changes from the refname up to the
    corresponding sync refname on the remote, creating it if needed.
    """
    log= logging.getLogger('git-mesh.push')
    if obj['dry_run']:
        log.warn('not actually pushing')
    else:
        log.info("pushing data")


@cli.command
@click.pass_obj
@click.argument("refname")
@click.argument("remote", nargs=-1)
def pull(obj:dict, refname: str, remote: list[str]):
    """
    Given a (required) refname, and optional remotes, sync changes.

    There are two modes pull can operate in: local or remote.

    In local mode, this command merges changes from the sync-version of
    refname, creating refname if needed.

    In remote mode, this command fetches changes from the remote refname to a
    local sync-version of refname, creating it if needed.
    """
    log= logging.getLogger('git-mesh.pull')
    if obj['dry_run']:
        log.warn('not actually pulling')
    else:
        log.info("pulling data")
