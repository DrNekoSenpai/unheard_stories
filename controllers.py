# This file defines actions, i.e. functions the URLs are mapped into
import datetime
from py4web                  import action, request, abort, redirect, URL, Field
from py4web.utils.form       import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner

from yatl.helpers            import A
from . common                import db, session, T, cache, auth, signed_url

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth.user, url_signer)
def index():
    rows = db(db.story).select()
    return dict(
        rows=rows, 
        url_signer   =url_signer,
        get_feed_url =URL('get_feed', signer=url_signer),
        view_url     =URL('view',     signer=url_signer),
    )

@action('get_feed', method=["GET", "POST"])
@action.uses(db, url_signer, session, auth.user)
def get_feed():
    return dict(feed=db(db.story).select().as_list())

@action('load_add_story_form')
@action.uses('add_story.html', db, session, auth.user, url_signer)
def load_add_story_form():
    return dict(
        url_signer=url_signer,
        add_story_url   =URL('add_story', signer=url_signer),
        cancel_url      =URL('cancel',    signer=url_signer),
        index_url       =URL('index',     signer=url_signer),
    )

@action('add_story', method="POST")
@action.uses(db, session, auth.user, url_signer)
def add_story():
    title=request.json.get('title')
    content=request.json.get('content')
    author=request.json.get('author')
    creation_date=datetime.datetime.utcnow()

    db.story.insert(
        title=title,
        content=content,
        author=author,
        creation_date=creation_date,
        likes=0,
        dislikes=0,
    )
    return "ok"


@action('view', method="POST")
@action.uses('view.html', db, url_signer, auth.user)
def view():
    story_id = request.json.get('id')
    return dict(story=story)