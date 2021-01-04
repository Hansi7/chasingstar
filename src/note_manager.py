import girl_manager
from DBcontext import Note, DbEngine
from girl_manager import now
from serverJ import send_message

girls = girl_manager.get_girls()

session = DbEngine().DBSession()


def first_run_add_all():
    for girl in girls:
        fcodes = girl_manager.girls_movie(girl.scode)
        for fcode in fcodes:
            new_note = Note(girl_id=girl.id, fcode=fcode, date=now())
            session.add(new_note)
            session.commit()
            session.close()


def get_one(girl,mute=False):
    """
    
    """
    print(girl.name + '...')
    fcodes = girl_manager.girls_movie(girl.scode)
    for fcode in fcodes:
        if len(get_note(fcode)) == 0:
            print('NEW!!!==>{},{}'.format(fcode, girl.name))
            if not mute:
                import url_manager
                url_new = url_manager.UrlManager().show()[0].url + '/' + fcode
                send_message(girl.name + ' 有新片了' + fcode, girl.name + ' ' + fcode + '\r\n' + url_new)
            new_note = Note(girl_id=girl.id, fcode=fcode, date=now())
            session.add(new_note)
        else:
            # print(fcode + ' already saved.')
            pass
    session.commit()
    session.close()

def get_new(mute=False):
    for girl in girls:
        print(girl.name + '...')
        fcodes = girl_manager.girls_movie(girl.scode)
        for fcode in fcodes:
            if len(get_note(fcode)) == 0:
                print('NEW!!!==>{},{}'.format(fcode, girl.name))
                if not mute:
                    import url_manager
                    url_new = url_manager.UrlManager().show()[0].url + '/' + fcode
                    send_message(girl.name + ' 有新片了' + fcode, girl.name + ' ' + fcode + '\r\n' + url_new)
                new_note = Note(girl_id=girl.id, fcode=fcode, date=now())
                session.add(new_note)
            else:
                # print(fcode + ' already saved.')
                pass
        session.commit()
    session.close()


def get_note(fcode):
    return session.query(Note).filter(Note.fcode == fcode).all()


def get_note_by_id(id):
    return session.query(Note).filter(Note.id == id).first()


def get_note_list():
    return session.query(Note).order_by(Note.id)[-30:]


if __name__ == '__main__':
    print(get_note_list())
