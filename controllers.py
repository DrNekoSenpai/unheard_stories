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
        
        get_feed_url        =URL('get_feed',        signer=url_signer),
        get_comments_url    =URL('get_comments',    signer=url_signer),
        add_story_url       =URL('add_story',       signer=url_signer),
        add_comment_url     =URL('add_comment',     signer=url_signer),

        report_story_url    =URL('report_story',    signer=url_signer),
        report_comment_url  =URL('report_comment',  signer=url_signer),
        get_ismod_url       =URL('get_ismod',       signer=url_signer),
        get_rfeed_url       =URL('get_rfeed',       signer=url_signer),
        get_rcomments_url   =URL('get_rcomments',   signer=url_signer),
        
        #TODO functions
        mod_approve_url     =URL('mod_approve',     signer=url_signer),
        delete_story_url    =URL('delete_story',    signer=url_signer),
        delete_comment_url  =URL('delete_comment',  signer=url_signer),
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
    #if (not comment.get('mod_approved')):
    db(db.story.story_id     == story_id  ).update(reported        =True)
    db(db.comment.comment_id == comment_id).update(reported_comment=True)
    return "ok"

@action('get_ismod', method="POST")
@action.uses(db, auth.user, url_signer)
def get_reports():
    return dict(ismod=ismod())

@action('get_rfeed', method="POST")
@action.uses(db, auth.user, url_signer)
def get_reports():
    return dict(reports=db(db.story.reported == True).select().as_list())

@action('get_rcomments', method="POST")
@action.uses(db, auth.user, url_signer)
def get_reports():

    story_id = request.json.get('story_id')
    comments = db((db.comment.story_id == story_id) & (db.comment.reported_comment == True)).select().as_list()
    return dict(comments=comments[::-1]) # return reversed list

# untested, probably doesn't work
@action('mod_approve', method="POST")
@action.uses(db, auth.user, url_signer)
def mod_approve():
    # TODO: finish / test

    # use to decide if approving a comment or story
    obj_type   = request.json.get('obj_type')

    # story case, simple: just unamrk report, mark as approved
    if (obj_type == "story"):

        story_id   = request.json.get('obj_id') # just need story

        db(db.story.story_id == story_id).update(
            mod_approved    =True, 
            reported_story  =False)

    # comment case, less simple, unmark/mark specific comment
    elif (obj_type == "comment"):

        story_id   = request.json.get('obj_id') # need story and comment
        comment_id = request.json.get('comment_id')

        db(db.comment.comment_id == comment_id).update(
            mod_approved    =True, 
            reported        =False)

        # check if any other comments in the story are reported
        comments = db((db.comment.story_id == story_id) & 
        (db.comment.reported_comment == False)).select().as_list()

        if (comments == []):

            # check if the story itself is reported
            story = db(db.story.story_id == story_id).select.as_list()[0]
            if (story.get('reported_story') == False):
                db(db.story.story_id == story_id).update(reported = False)
        
    return "ok"

@action('delete_story', method="POST")
@action.uses(db, auth.user, url_signer)
def delete_story():
    # TODO
    return "ok"

@action('delete_comment', method="POST")
@action.uses(db, auth.user, url_signer)
def delete_story():
    # TODO
    return "ok"