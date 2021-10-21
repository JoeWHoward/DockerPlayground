"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
# From Google's Python Styleguide. https://google.github.io/styleguide/pyguide.html

from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, registry, relationship
from fastapi import FastAPI

app = FastAPI()

engine = create_engine("postgresql+psycopg2://vagrant:vagrant!@db/appdb", echo=True, future=True)
mapper_registry = registry()

metadata_obj = mapper_registry.metadata

# In the most common approach, each mapped class descends from a common base class known as the
# declarative base.

Base = mapper_registry.generate_base()


# alternatively, the above two steps can be combined into one with
# from sqlalchemy.orm import declarative_base
# Base = declarative_base()

# Note:  Declarative Base / Base is pretty much models.Model from Django
# Note:  A Session is pretty much an object manager from Django

class User(Base):
    """ A basic User object in the ORM.

    User is a declarative mapping, a representation of the database table.

    Attributes:
        id: An auto-generated primary key integer
        name: A string indicating the name
        fullname: A string indicating the full name
        addresses: A ForeignKey to the correspondant Address record

    """
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship("Address", back_populates="user")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}"


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))
    user = relationship("User", back_populates="addresses") # Not required, but useful for indication to the ORM
    # The above two lines are equivalent to user = models.ForeignKey(User, related_name='addresses') in Django

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

#  The above two mapped classes are now available for ORM use and querying
#  But they also contain Table objects that were generated as a part of the declarative
#  mapping process.

joe = User(name="Joe", fullname="Joe Howard") # id is not auto generated here
bob = User(name="Bob", fullname="Bob Howard")
a1 = Address(email_address="joseph.howard307@gmail.com", user=joe)
a2 = Address(email_address="bobthebugguy@gmail.com", user=bob)

# mapper_registry.metadata.create_all(engine)

with Session(engine) as session:

    @app.get("/")
    async def root():

        session.add(joe, bob)
        session.add(a1, a2)
        session.commit()
        return a1.as_dict()

    @app.get("/users/{user_id}")
    async def get_user(user_id):
        return session.query(User).get(user_id).as_dict()

    @app.get("/addresses/{address_id}")
    async def get_address(address_id):
        session.flush()
        return session.query(Address).get(address_id).as_dict()


# We can generate a reflection of the database by passing a table name to a constructor.
# some_table = Table("some_table", metadata_obj, autoload_with=engine)
# This will create a new Table object, placing it into the metadata_obj ORM library, that is constructed
# from the existing columns on the database's table, "some_table"


