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
        url_signer       =url_signer,
        get_feed_url     =URL('get_feed',       signer=url_signer),
        get_comments_url =URL('get_comments',   signer=url_signer),
        add_story_url    =URL('add_story',      signer=url_signer),
        add_comment_url  =URL('add_comment',    signer=url_signer),
    )

@action('get_feed', method="POST")
@action.uses(db, auth.user, url_signer)
def get_feed():
    return dict(feed=db(db.story).select().as_list())

@action('get_comments', method="POST")
@action.uses(db, auth.user, url_signer)
def get_feed():
    story_id = request.json.get('story_id')
    num_comments = request.json.get('num_comments')
    comments = db(db.comment.story_id == story_id).select().as_list()
    return dict(comments=comments[::-1]) # return reversed list

@action('add_comment', method="POST")
@action.uses(db, auth.user, url_signer)
def add_comment():
    db.comment.insert(
        story_id        =request.json.get('story_id'),
        content         =request.json.get('content'),
        author          =auth.current_user.get('username'),
        creation_date   =datetime.datetime.utcnow(),
        likes           =0,
    )

    # Increment the number of comments for the story
    db(db.story.story_id == request.json.get('story_id')).update(num_comments=request.json.get('num_comments'))
    return "ok"

@action('add_story', method="POST")
@action.uses(db, auth.user, url_signer)
def add_story():
    db.story.insert(
        title           =request.json.get('title'),
        content         =request.json.get('content'),
        author          =auth.current_user.get('username'),
        creation_date   =datetime.datetime.utcnow(),
        likes=0,
    )
    return "ok"