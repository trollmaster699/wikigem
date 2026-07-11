from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Association table for Video to Categories (Many-to-Many)
video_category_association = Table(
    'video_category',
    Base.metadata,
    Column('video_id', Integer, ForeignKey('videos.id')),
    Column('category_name', String)
)

class Creator(Base):
    __tablename__ = 'creators'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    followers_count = Column(Integer, default=0)
    endorsement_score = Column(Integer, default=0)
    trust_score = Column(Float, default=0.0)
    
    videos = relationship("Video", back_populates="creator", cascade="all, delete-orphan")

class Video(Base):
    __tablename__ = 'videos'
    
    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey('creators.id'), nullable=False)
    url = Column(String, unique=True, nullable=False)
    summary = Column(String)
    
    # Relationship to creator
    creator = relationship("Creator", back_populates="videos")
    
    # Relationship to categories (many-to-many using association table)
    # Since category is just a string, we can use the association table directly,
    # or better yet, define a separate Category model if we want to query them easily.
    # To keep it simple and match the schema request, we'll store them via association.
    # We can handle retrieving them manually or define a simple Category model.
    # Let's do a proper Category model for cleaner ORM usage.
    
    tips = relationship("Tip", back_populates="video", cascade="all, delete-orphan")
    categories = relationship("Category", secondary=video_category_association, back_populates="videos")

class Category(Base):
    __tablename__ = 'categories'
    
    name = Column(String, primary_key=True)
    videos = relationship("Video", secondary=video_category_association, back_populates="categories")

class Tip(Base):
    __tablename__ = 'tips'
    
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey('videos.id'), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String)
    body_area = Column(String)
    target_muscles = Column(String)
    
    video = relationship("Video", back_populates="tips")
