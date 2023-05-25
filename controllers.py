"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL, Field
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner

from . common import db, session, T, cache, auth, signed_url

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth.user, url_signer)
def index():
    ## TODO: Show to each logged in user the birds they have seen with their count.
    # The table must have an edit button to edit a row, and also, a +1 button to increase the count
    # by 1 (this needs to be protected by a signed URL).
    # On top of the table there is a button to insert a new bird.
    rows = db(db.story).select()
    return dict(rows=rows, url_signer=url_signer)

@action('submit', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'submit.html')
def add():
    form = Form(db.story, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # We simply redirect; the insertion already happened.
        redirect(URL('index'))
    # Either this is a GET request, or this is a POST but not accepted = with errors.
    return dict(form=form)

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
