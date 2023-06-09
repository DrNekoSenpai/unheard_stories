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
    search = request.json.get('search')
    # Initialize query to get all stories
    query = db.story
    if search: 
        # Modify query to filter stories based on the search term in the title or content
        query = (db.story.title.lower().contains(search.lower())) | (db.story.content.lower().contains(search.lower()))
    # Fetch the first 20 stories that satisfy the query
    return dict(feed=db(query).select(limitby=(0, 20)).as_list())

@action('get_comments', method="POST")
@action.uses(db, auth.user, url_signer)
def get_comments():
    story_id = request.json.get('story_id')
    num_comments = request.json.get('num_comments')
    comments = db(db.comment.story_id == story_id).select().as_list()
    return dict(comments=comments[::-1]) # return reversed list

@action('add_comment', method="POST")
@action.uses(db, auth.user, url_signer)
def add_comment():
    story_id = request.json.get('story_id')
    db.comment.insert(
        story_id        = story_id,
        content         = request.json.get('content'),
        author          = auth.current_user.get('username'),
        creation_date   = datetime.datetime.utcnow(),
        likes           = 0,
    )

    # Count the number of comments for the story on the server-side
    num_comments = db(db.comment.story_id == story_id).count()
    db(db.story.story_id == story_id).update(num_comments=num_comments)
    return "ok"

@action('add_story', method="POST")
@action.uses(db, auth.user, url_signer)
def add_story():
    # tags = request.json.get('tags')
    # # Split tags into a list and remove leading/trailing whitespace from each tag
    # tag_list = [tag.strip() for tag in tags.split(',')]
    db.story.insert(
        title           =request.json.get('title'),
        content         =request.json.get('content'),
        # tags            =request.json.get('tags'),
        author          =auth.current_user.get('username'),
        creation_date   =datetime.datetime.utcnow(),
        likes           =0,
    )
    return "ok"