# This file defines the database models

from .common import db, Field, auth
from pydal.validators import *

# Define a story table. This will store all the stories shared on the blog site. 
# It'll have fields like story ID, title, content, author, creation date, etc. 
# The story ID will be the primary key.

db.define_table(
    'story',
    Field('story_id', 'id'),
    Field('title', requires=IS_NOT_EMPTY()),
    Field('content', 'text', requires=IS_NOT_EMPTY()),
    Field('author', requires=IS_NOT_EMPTY()),
    Field('creation_date', 'datetime', requires=IS_NOT_EMPTY()),
    Field('likes', 'integer', default=0),
    Field('dislikes', 'integer', default=0),
    Field('comments', 'list:reference comment'),
)

# The story ID and creation date will not be editable by the user.
# db.story.story_id.readable -- when you submit a new form, if it's not writable, then it won't show up in the form
db.story.story_id.readable = db.story.story_id.writable = False
db.story.creation_date.writable = False

# We should be able to view likes, dislikes, and comments; but they shouldn't be editable. 
db.story.likes.writable = False 
db.story.dislikes.writable = False
db.story.comments.writable = False

# Define a comment table. This will store all the comments shared on the blog site.
# It'll have fields like comment ID, story ID, content, author, creation date, etc.
# The comment ID will be the primary key.

db.define_table(
    'comment',
    Field('comment_id', 'id'),
    Field('story_id', 'reference story'),
    Field('content', 'text', requires=IS_NOT_EMPTY()),
    Field('author', requires=IS_NOT_EMPTY()),
    Field('creation_date', 'datetime', requires=IS_NOT_EMPTY()),
    Field('likes', 'integer', default=0),
    Field('dislikes', 'integer', default=0),
    Field('replies', 'list:reference comment'),
)

# The comment ID and creation date will not be editable by the user.
db.comment.comment_id.readable = db.comment.comment_id.writable = False
db.comment.creation_date.writable = False

# We should be able to view likes, dislikes, and other comments; but they shouldn't be editable.
db.comment.likes.writable = False
db.comment.dislikes.writable = False
db.comment.replies.writable = False

db.commit()