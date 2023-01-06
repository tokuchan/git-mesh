import logging
import sh
import click

from rich import print
from rich.traceback import install
install(show_locals=True)

@click.group
def cli():
    print("Hello world!")


@cli.command
def sync():
    '''
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
    '''
    print("Sync")
