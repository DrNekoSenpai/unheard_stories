# This file defines actions, i.e. functions the URLs are mapped into
import datetime
from py4web                  import action, request, abort, redirect, URL, Field
from py4web.utils.form       import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner

from . common import db, session, T, cache, auth, signed_url

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
@action.uses('load_add_story.html', db, session, auth.user, url_signer)
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

@action('submit', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'submit.html')
def submit():
    form = Form(db.story, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # We simply redirect; the insertion already happened.
        redirect(URL('index'))
    # Either this is a GET request, or this is a POST but not accepted = with errors.
    return dict(form=form)

# To do: make a view_story button and page
@action('view/<story_id:int>')
@action.uses(db, session, auth.user, 'view.html')
def view(story_id = None):
    assert story_id is not None
    rows = db(db.story.story_id == story_id).select()
    story = rows[0]
    return dict(story=story, url_signer=url_signer)

# Dummy comment

# @action('edit/<bird_id:int>', method=["GET", "POST"])
# @action.uses('edit.html', url_signer, db, session, auth.user)
# def edit(bird_id=None):
#     assert bird_id is not None
#     # We read the product being edited from the db.
#     # b = db(db.bird.id == bird_id).select().first()
#     b = db.bird[bird_id]
#     if b is None:
#         # Nothing found to be edited!
#         redirect(URL('index'))
#     # Edit form: it has record=
#     form = Form(db.bird, record=b, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
#     if form.accepted:
#         # The update already happened!
#         redirect(URL('index'))
#     return dict(form=form)

# @action('delete/<bird_id:int>')
# @action.uses(db, session, auth.user, url_signer.verify())
# def delete(bird_id=None):
#     assert bird_id is not None
#     db(db.bird.id == bird_id).delete()
#     redirect(URL('index'))

# @action('inc/<bird_id:int>')
# @action.uses(db, auth.user, url_signer.verify())
# def inc(bird_id=None):
#     assert bird_id is not None
#     bird = db.bird[bird_id]
#     db(db.bird.id == bird_id).update(n_sightings=bird.n_sightings + 1)
#     redirect(URL('index'))

# # This is an example only, to be used as inspiration for your code to increment the bird count.
# # Note that the bird_id parameter ...
# @action('capitalize/<bird_id:int>') # the :int means: please convert this to an int.
# @action.uses(db, auth.user, url_signer.verify())
# # ... has to match the bird_id parameter of the Python function here.
# def capitalize(bird_id=None):
#     assert bird_id is not None
#     bird = db.bird[bird_id]
#     db(db.bird.id == bird_id).update(bird_name=bird.bird_name.capitalize())
