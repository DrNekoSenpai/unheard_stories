# This file defines the database models

from .common import db, Field, auth
from pydal.validators import *

# Define a story table. 
# This will store all the stories shared on the blog site. 

# reported in story is true if 
    # the story's comments OR 
    # the story contents are reported

# reported_story is for if the story itself is reported

# reported_comment is for if the comment itself is reported

# mod_approved is set if a mod reviews a reported story/comment
# and decides that it should NOT be deleted, and no more reports should occur 
# for that comment / story

db.define_table(
    'story',
    Field('story_id',       'id'),                     # Primary Key
    Field('title',                                     requires=IS_NOT_EMPTY()),
    Field('content',        'text',                    requires=IS_NOT_EMPTY()),
    Field('author',         'text',                    requires=IS_NOT_EMPTY()),
    Field('creation_date',  'datetime',                requires=IS_NOT_EMPTY()),
    Field('likes',          'integer',                 default=0),
    Field('dislikes',       'integer',                 default=0),
    Field('comments',       'list:reference comment'),
    Field('num_comments',   'integer',                 default=0),
    Field('tags',           'list:string'),
    Field('reported',       'boolean',                 default=False),
    Field('reported_story', 'boolean',                 default=False),
    Field('mod_approved',   'boolean',                 default=False),
)

# most fields will not be editable by the user.
db.story.story_id.writable      = False
db.story.creation_date.writable = False
db.story.likes.writable         = False 
db.story.dislikes.writable      = False
db.story.comments.writable      = False
db.story.num_comments.writable  = False

# Define a comment table. 
# This will store all the comments shared on the blog site.

db.define_table(
    'comment',
    Field('comment_id',       'id'),                     # Primary Key
    Field('story_id',         'reference story',         requires=IS_NOT_EMPTY()),
    Field('content',          'text',                    requires=IS_NOT_EMPTY()),
    Field('author',                                      requires=IS_NOT_EMPTY()),
    Field('creation_date',    'datetime',                requires=IS_NOT_EMPTY()),
    Field('likes',            'integer',                 default=0),
    Field('replies',          'list:reference comment'),
    Field('reported_comment', 'boolean',                 default=False),
    Field('mod_approved',     'boolean',                 default=False),
)

# Most fields date not be editable by the user.
db.comment.comment_id.writable      = False
db.comment.creation_date.writable   = False
db.comment.likes.writable           = False
db.comment.replies.writable         = False

db.commit()