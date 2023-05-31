# This file defines the database models

from .common import db, Field, auth
from pydal.validators import *

# Define a story table. 
# This will store all the stories shared on the blog site. 

db.define_table(
    'story',
    Field('story_id',       'id'),      # Primary Key
    Field('title',                      requires=IS_NOT_EMPTY()),
    Field('content',        'text',     requires=IS_NOT_EMPTY()),
    Field('author',                     requires=IS_NOT_EMPTY()),
    Field('creation_date', 'datetime',  requires=IS_NOT_EMPTY()),
    Field('likes',          'integer',                              default=0),
    Field('dislikes',       'integer',                              default=0),
    Field('comments',       'list:reference comment'),
)

# most fields will not be editable by the user.
db.story.story_id.writable      = False
db.story.creation_date.writable = False
db.story.likes.writable         = False 
db.story.dislikes.writable      = False
db.story.comments.writable      = False

# Define a comment table. 
# This will store all the comments shared on the blog site.

db.define_table(
    'comment',
    Field('comment_id',     'id'),          # Primary Key
    Field('story_id',       'reference story'),
    Field('content',        'text',         requires=IS_NOT_EMPTY()),
    Field('author',                         requires=IS_NOT_EMPTY()),
    Field('creation_date', 'datetime',      requires=IS_NOT_EMPTY()),
    Field('likes',         'integer',                                default=0),
    Field('dislikes',      'integer',                                default=0),
    Field('replies',       'list:reference comment'),
)

# Most fields date not be editable by the user.
db.comment.comment_id.writable      = False
db.comment.creation_date.writable   = False
db.comment.likes.writable           = False
db.comment.dislikes.writable        = False
db.comment.replies.writable         = False

db.commit()