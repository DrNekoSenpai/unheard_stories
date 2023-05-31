# This file defines actions, i.e. functions the URLs are mapped into
import datetime
from py4web                  import action, request, abort, redirect, URL, Field
from py4web.utils.form       import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner

from .common import db, session, T, cache, auth, signed_url

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth.user, url_signer)
def index():
    return dict(
        url_signer    =url_signer,
        get_feed_url  =URL('get_feed',  signer=url_signer),
        add_story_url =URL('add_story', signer=url_signer),
    )

@action('get_feed', method=["GET", "POST"])
@action.uses(db, url_signer, session, auth.user)
def get_feed():
    return dict(feed=db(db.story).select().as_list())

@action('add_story', method="POST")
@action.uses(db, session, auth.user, url_signer)
def add_story():
    db.story.insert(
        title=request.json.get('title'),
        content=request.json.get('content'),
        author=request.json.get('author'),
        creation_date=datetime.datetime.utcnow(),
        likes=0,
        dislikes=0,
    )
    return "ok"