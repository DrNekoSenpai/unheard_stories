"""
This file defines the database models
"""

from .common import db, Field, auth, T as translate
from pydal.validators import *

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#

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
db.story.story_id.readable = db.story.story_id.writable = False
db.story.creation_date.writable = False

# Translate the labels using the translate function
db.story.title.label = translate('Title')
db.story.content.label = translate('Content')
db.story.author.label = translate('Author')
db.story.creation_date.label = translate('Creation Date')
db.story.likes.label = translate('Likes')
db.story.dislikes.label = translate('Dislikes')
db.story.comments.label = translate('Comments')

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
)

# The comment ID and creation date will not be editable by the user.
db.comment.comment_id.readable = db.comment.comment_id.writable = False
db.comment.creation_date.writable = False

# Translate the labels using the translate function
db.comment.story_id.label = translate('Story ID')
db.comment.content.label = translate('Content')
db.comment.author.label = translate('Author')
db.comment.creation_date.label = translate('Creation Date')
db.comment.likes.label = translate('Likes')
db.comment.dislikes.label = translate('Dislikes')

db.commit()