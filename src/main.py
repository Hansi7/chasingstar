# coding=<utf8>
from note_manager import get_new, first_run_add_all, get_note_list, get_note_by_id, get_one
import click
from girl_manager import get_girls, subscribe_girl, unsubscribe_girl, girls_movie_by_id
from url_manager import UrlManager


@click.command(help='check if any new movie by these girls')
@click.option('-m', '--mute', is_flag=True, default=False, help='dont send message when found new movies this time.')
@click.option('-g', '--girlid', default=None, help='check only this girl')
def ck(mute, girlid=None):
    if mute:
        if not girlid:
            print('Checking update once...no message will send')
            first_run_add_all()
        else:
            girl = get_girls(girlid)[0]
            print('Checking one girl update once...no message will send',girl.name)
            get_one(girl)
    else:
        if not girlid:
            print('Checking update once...')
            get_new()
        else:
            girl = get_girls(girlid)[0]
            print('Checking one girl update once...',girl.name)
            get_one(girl)


@click.command(help='show all girls')
def ls():
    gs = get_girls()
    for g in gs:
        print(g)


@click.command(help='add girl to watch list')
@click.argument('scode')
def add(scode):
    subscribe_girl(scode)


@click.command(help='remove girl from watch list')
@click.argument('id')
def rm(id):
    unsubscribe_girl(id)


@click.command()
def initdb():
    print('init db ...')
    print('url_manager.first_run() init new Urls in DB')
    UrlManager().first_run()
    print('run this to add a girl : python3 main.py add b64')
    print('run this to fill db : python3 main.py ck --mute True')
    print('Now good to go')


@click.command(help='show recent mv of one girl')
@click.argument('id')
def show(id):
    girls_movie_by_id(id)


@click.command(help='show note list')
def note():
    for i in get_note_list():
        print(i)


@click.command(help='show note N')
@click.argument('id')
def n(id):
    n0 = (get_note_by_id(id))
    print(UrlManager().show()[0].url + '/' + n0.fcode)


@click.command(help='test function')
def test():
    print(123)


@click.group()
def run():
    pass


run.add_command(initdb)
run.add_command(ck)
run.add_command(ls)
run.add_command(add)
run.add_command(rm)
run.add_command(show)
run.add_command(note)
run.add_command(n)
run.add_command(test)

if __name__ == '__main__':
    run()
