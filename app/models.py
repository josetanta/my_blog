import bleach
from flask import url_for
from markdown import markdown
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, jsonify, url_for
from datetime import datetime
from slugify import slugify
from . import db, login_manager


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_POST = 0x04
    MODERATE_COMMENTS = 0x08
    PERMITE_API = 0x32
    ADMINISTER = 0xff


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, index=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='joined')

    @staticmethod
    def generate_roles():
        roles = {
            'User': (True,
                     Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_POST),
            'Moderator': (False,
                          Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_POST |
                          Permission.MODERATE_COMMENTS |
                          Permission.PERMITE_API),
            'Admin': (False, 0xff),
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.default = roles[r][0]
            role.permissions = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def has_permission(self, permissions):
        # Return a boolean of permission´s users
        '''
        Determinar si el objeto, tiene un privilegios de realizar
        acciones determnidas según el rol que le corresponda.
        '''
        return self.permissions & permissions == permissions

    def __repr__(self):
        return "<Role %s>" % self.name


class Follow(db.Model):
    __tablename__ = 'follows'
    followed_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), primary_key=True)
    follower_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(40), nullable=False,
                         unique=True, index=True)
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    name = db.Column(db.String(60), nullable=True)
    address = db.Column(db.String(60), nullable=True)
    password_hash = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    date_register = db.Column(
        db.DateTime, default=datetime.now, nullable=False)
    status = db.Column(db.Boolean, default=True, index=True)
    upload = db.Column(db.String(200), nullable=True, default='def')
    role_id = db.Column(db.Integer, db.ForeignKey(
        'roles.id'), index=True, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author',
                            lazy=True, cascade='all, delete-orphan')
    comments = db.relationship(
        'Comment', backref='author', lazy=True, cascade='all, delete-orphan')

    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan'
                               )

    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan'
                                )

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['EMAIL_BLOG_ADMIN']:
                self.role = Role.query.filter_by(
                    permissions=Permission.ADMINISTER).first()
                self.confirmed = True
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def get_reset_token(self, expires_sec=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        token = s.dumps({'user_id': self.id}).decode('utf-8')
        return token

    @staticmethod
    def verificar_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        return User.query.get(user_id)

    def __setattr__(self, key, value):
        super(User, self).__setattr__(key, value)
        if key == 'username':
            self.slug = self.__generate_slug(self.username)

    def __generate_slug(self, username):
        return slugify(username)

    def to_json(self):
        return dict({
            'username': self.username,
            'image': self.upload_path
        })

    @property
    def upload_path(self):
        return url_for('static', filename='uploads/users/' + self.upload)

    def api_to_json(self):
        return dict({
            'username': self.username,
            'address': self.address,
            'status': self.status,
            'upload': self.upload,
            'self': url_for('v1.user_api', user_id=self.id, _external=True),
            'image': self.upload_path,
            'posts': [post.to_json() for post in self.posts],
        })

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followed.filter_by(followed_id=user.id).first()

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first()

    def can(self, permissions):
        p = self.role is not None and self.role.has_permission(permissions)
        return p

    @property
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    # Generate a token for confimed of account user
    def generate_confirmed_token(self, expiration=3600):
        s = Serializer(current_app.config.get('SECRET_KEY'), expiration)
        token = s.dumps({'confirm': self.id}).decode('utf-8')
        return token

    # Confirm account of user
    def confirm(self, token):
        s = Serializer(current_app.config.get('SECRET_KEY'))
        try:
            data = s.loads(token)
        except Exception as e:
            return False

        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        raise AttributeError("La contraseña no puede ser leida.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def followers_list(self):
        return db.session.query(User)\
            .select_from(Follow)\
            .filter_by(followed_id=self.id)\
            .join(User, Follow.follower_id == User.id).all()

    @property
    def followeds_list(self):
        return db.session.query(User)\
            .select_from(Follow)\
            .filter_by(follower_id=self.id)\
            .join(User, Follow.followed_id == User.id).all()

    def __repr__(self):
        return f"<User {self.email} {self.slug}>"


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


login_manager.anonymous_user = AnonymousUser


class Post(UserMixin, db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(120), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    content_html = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(100), nullable=False, unique=True, index=True)
    date_register = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    publishied = db.Column(db.Boolean, default=True, index=True)
    upload = db.Column(db.String(200), nullable=True, default='def')
    url_image = db.Column(db.String(600), nullable=True, default='')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    comments = db.relationship(
        'Comment', backref='post', lazy=True, cascade="all, delete-orphan")

    def __setattr__(self, key, value):
        super(Post, self).__setattr__(key, value)
        if key == 'title':
            self.slug = self.__generate_slug(self.title)

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote',
            'code', 'em', 'i', 'li', 'ol', 'pre',
            'strong', 'ul', 'h1', 'h2',
            'h3', 'p', 'h4', 'h5', 'h6'
        ]
        target.content_html = bleach.linkify(
            bleach.clean(
                markdown(value, output_format='html'),
                tags=allowed_tags, strip=True
            )
        )

    def __generate_slug(self, title):
        return slugify(title)

    def __repr__(self):
        return f"<Post {self.title}>"

    @property
    def upload_path(self):
        return url_for('static', filename='uploads/posts/' + self.upload)

    def to_json(self):
        obj = dict({
            'title': self.title,
            'author': self.author.to_json(),
            'content': self.content,
            'publishied': self.publishied,
            'self': url_for('v1.post_api', post_id=self.id, _external=True),
            'image': self.upload_path,
            'created': self.date_register,
            'comments': [comment.to_json() for comment in self.comments]
        })
        return obj

    def get_id(self):
        obj = dict({
            'id': self.id,
            'publishied': self.publishied,
        })
        return obj


db.event.listen(Post.content, 'set', Post.on_change_body)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), index=True)
    publishied = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_json(self):
        return dict({
            'post': self.post.title,
            'body': self.body,
            'author': self.author.username,
            'self': url_for('v1.comment_api', comment_id=self.id, _external=True)
        })

    def get_id(self):
        obj = dict({
            'id': self.id,
            'publishied': self.publishied,
        })
        return obj

    def __repr__(self):
        return '<Comment %d %s>' % (self.id, self.publishied)
