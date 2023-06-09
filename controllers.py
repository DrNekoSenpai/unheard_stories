# This file defines actions, i.e. functions the URLs are mapped into
import datetime
from py4web                  import action, request, abort, redirect, URL, Field
from py4web.utils.form       import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner

from .common import db, session, T, cache, auth, signed_url

url_signer = URLSigner(session)

def ismod():
    if auth.current_user.get('username') == "mod":
        return True
    else:
        return False

    # Note: access is obj.get('field_name'):

@action('index')
@action.uses('index.html', db, auth.user, url_signer)
def index():
    return dict(
        url_signer          =url_signer,
        
        # get/set for stories/comments/replies
        get_feed_url            =URL('get_feed',            signer=url_signer),
        get_comments_url        =URL('get_comments',        signer=url_signer),
        add_story_url           =URL('add_story',           signer=url_signer),
        add_comment_url         =URL('add_comment',         signer=url_signer),

        add_reply_url           =URL('add_reply',           signer=url_signer),
        get_replies_url         =URL('get_replies',         signer=url_signer),

        # user report functions  
        report_story_url        =URL('report_story',        signer=url_signer),
        report_comment_url      =URL('report_comment',      signer=url_signer),

        # mod misc      
        get_ismod_url           =URL('get_ismod',           signer=url_signer),
        get_rfeed_url           =URL('get_rfeed',           signer=url_signer),
        get_rcomments_url       =URL('get_rcomments',       signer=url_signer),

        # mod actions       
        approve_story_url       =URL('approve_story',       signer=url_signer),
        approve_comment_url     =URL('approve_comment',     signer=url_signer),
        delete_story_url        =URL('delete_story',        signer=url_signer),
        delete_comment_url      =URL('delete_comment',      signer=url_signer),

        # like function
        set_story_like_url      =URL('set_story_like',      signer=url_signer),
        set_comment_like_url    =URL('set_comment_like',    signer=url_signer),
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

@action("add_reply", method="POST")
@action.uses(db, auth.user, url_signer)
def add_reply():
    content     = request.json.get('content')
    parent_id   = request.json.get('parent_id')
    story_id    = request.json.get('story_id')
    reply_count = request.json.get('reply_count')

    db.comment.insert(
        story_id        = story_id,
        parent_id       = parent_id,
        reply_count     = 0,

        author          = auth.current_user.get('username'),
        content         = content,
        creation_date   = datetime.datetime.utcnow(),
    )

    db(db.comment.comment_id == parent_id).update(reply_count=reply_count + 1)

    return "ok"

@action("get_replies", method="POST")
@action.uses(db, auth.user, url_signer)
def get_replies():
    parent_id = request.json.get('parent_id')
    return dict(replies=db(db.comment.parent_id == parent_id).select().as_list()[::-1])

@action('add_story', method="POST")
@action.uses(db, auth.user, url_signer)
def add_story():
    # tags = request.json.get('tags')
    # # Split tags into a list and remove leading/trailing whitespace from each tag
    # tag_list = [tag.strip() for tag in tags.split(',')]
    db.story.insert(
        title           =request.json.get('title'),
        content         =request.json.get('content'),
        # tags          =request.json.get('tags'),
        author          =auth.current_user.get('username'),
        creation_date   =datetime.datetime.utcnow(),
        likes           =0,
    )
    return "ok"

@action('report_story', method="POST")
@action.uses(db, auth.user, url_signer)
def report_story():
    story_id = request.json.get('story_id')
    story = db(db.story.story_id == story_id).select().as_list()[0]

    # update reported and reported story if not not mod_approved
    if (not story.get('mod_approved')):
        db(db.story.story_id == story_id).update(
            reported        =True, 
            reported_story  =True)
    return "ok"

@action('report_comment', method="POST")
@action.uses(db, auth.user, url_signer)
def report_comment():
    
    story_id    = request.json.get('story_id')
    comment_id  = request.json.get('comment_id')
    
    comment = db(db.comment.comment_id == comment_id).select().as_list()[0]
    
    # update reported and the reported comment not mod_approved
    if (not comment.get('mod_approved')):
        db(db.story.story_id     == story_id  ).update(reported        =True)
        db(db.comment.comment_id == comment_id).update(reported_comment=True)
    return "ok"

@action('get_ismod', method="POST")
@action.uses(db, auth.user, url_signer)
def get_ismod():
    return dict(ismod=ismod())

@action('get_rfeed', method="POST")
@action.uses(db, auth.user, url_signer)
def get_rfeed():
    return dict(reports=db(db.story.reported == True).select().as_list())

@action('get_rcomments', method="POST")
@action.uses(db, auth.user, url_signer)
def get_rcomments():

    story_id = request.json.get('story_id')
    comments = db((db.comment.story_id == story_id) & (db.comment.reported_comment == True)).select().as_list()
    return dict(comments=comments[::-1]) # return reversed list

@action('approve_story', method="POST")
@action.uses(db, auth.user, url_signer)
def approve_story():

    if (not ismod()):
        return "insufficent permissions"

    # mark story as approved, remove reported_story bool
    story_id   = request.json.get('story_id')
    db(db.story.story_id == story_id).update(
        mod_approved    =True, 
        reported_story  =False)

    # check if any other comments in the story are reported
    comments = db((db.comment.story_id == story_id) & 
    (db.comment.reported_comment == True)).select().as_list()
    # if not, remove reported bool from story
    if (comments == []):
        db(db.story.story_id == story_id).update(reported = False)
    return "ok"

@action('approve_comment', method="POST")
@action.uses(db, auth.user, url_signer)
def approve_comment():

    if (not ismod()):
        return "insufficent permissions"

    # mark comment as approved, and no longer reported
    story_id   = request.json.get('story_id')
    comment_id = request.json.get('comment_id')
    db(db.comment.comment_id == comment_id).update(
        mod_approved     =True, 
        reported_comment =False)

    # check if any other comments in the story are reported
    comments = db((db.comment.story_id == story_id) & 
    (db.comment.reported_comment == True)).select().as_list()
    # if not
    if (comments == []):
        # check if the story itself is reported
        story = db(db.story.story_id == story_id).select().as_list()[0]
        # if not, set whole story not not reported
        if (story.get('reported_story') == False):
            db(db.story.story_id == story_id).update(reported = False)
    return "ok"

@action('delete_story', method="POST")
@action.uses(db, auth.user, url_signer)
def delete_story():

    if (not ismod()):
        return "insufficent permissions"

    # delete story without remorse
    story_id   = request.json.get('story_id')
    db(db.story.story_id == story_id).delete()
    return "ok"

@action('delete_comment', method="POST")
@action.uses(db, auth.user, url_signer)
def delete_comment():

    if (not ismod()):
        return "insufficent permissions"

    story_id   = request.json.get('story_id')
    comment_id = request.json.get('comment_id')
    db(db.comment.comment_id == comment_id).delete()

    # check if any other comments in the story are reported
    comments = db((db.comment.story_id == story_id) & 
    (db.comment.reported_comment == True)).select().as_list()
    # if not
    if (comments == []):
        # check if the story itself is reported
        story = db(db.story.story_id == story_id).select().as_list()[0]
        # if not, set whole story to not reported
        if (story.get('reported_story') == False):
            db(db.story.story_id == story_id).update(reported = False)
    return "ok"

@action('set_story_like', method="POST")
@action.uses(db, auth.user, url_signer)
def set_story_like():
    username    = auth.current_user.get('username')
    story_id    = request.json.get('story_id')
    likes       = request.json.get('likes')

    like = db((db.story_like.username == username) & 
    (db.story_like.story_id == story_id)).select().as_list()

    if (like == []):
        db.story_like.insert(username=username, story_id=story_id)
        db(db.story.story_id == story_id).update(likes=likes + 1)
        return dict(r= 1)
    else:
        db((db.story_like.username == username) 
        & (db.story_like.story_id == story_id)).delete()

        db(db.story.story_id == story_id).update(likes=likes - 1)
        return dict(r= -1)

@action('set_comment_like', method="POST")
@action.uses(db, auth.user, url_signer)
def set_comment_like():

    username    = auth.current_user.get('username')
    comment_id  = request.json.get('comment_id')
    likes       = request.json.get('likes')

    like = db((db.comment_like.username == username) & 
    (db.comment_like.comment_id == comment_id)).select().as_list()

    if (like == []):
        db.comment_like.insert(username=username, comment_id=comment_id)
        db(db.comment.comment_id == comment_id).update(likes=likes + 1)
        return dict(r= 1)
    else:
        db((db.comment_like.username == username) 
        & (db.comment_like.comment_id == comment_id)).delete()

        db(db.comment.comment_id == comment_id).update(likes=likes - 1)
        return dict(r= -1)