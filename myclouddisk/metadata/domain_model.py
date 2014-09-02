'''

@author: jipingzh
'''

import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

import datetime
#SQLAlchemy
# engine = create_engine('sqlite:///meta.db', echo=True)
engine = create_engine('mysql+mysqldb://root:123456@localhost/scloud')
Base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))

class Domain(Base):
    __tablename__ = 'domain'
    '''
    mysql> describe domain;
    +----------------+------------------+------+-----+---------+----------------+
    | Field          | Type             | Null | Key | Default | Extra          |
    +----------------+------------------+------+-----+---------+----------------+
    | id             | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
    | name           | varchar(255)     | NO   |     | NULL    |                |
    | domain_type_id | int(11)          | NO   | MUL | NULL    |                |
    | space_id       | int(11)          | NO   | MUL | NULL    |                |
    | size           | int(11)          | NO   |     | 0       |                |
    | left           | int(11)          | NO   |     | 2       |                |
    | is_active      | int(11)          | NO   |     | 1       |                |
    | created        | datetime         | NO   |     | NULL    |                |
    | modified       | datetime         | NO   |     | NULL    |                |
    +----------------+------------------+------+-----+---------+----------------+
    '''
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    domain_type_id = Column(Integer, nullable=False)
    space_id = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False, default=0)
    left = Column(Integer, nullable=False, default=2)#left means how much space left in the domain
    is_active = Column(Integer, nullable=False, default=1)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)
    
    def __init__(self, name, domain_type_id, space_id, created, modified, size=0, left=2, is_active=1):
            self.name = name
            self.domain_type_id = domain_type_id
            self.space_id = space_id
            self.size = size
            self.left = left
            self.is_active = is_active
            self.created = created
            self.modified = modified

    def __repr__(self):
        return '{"id":"%s", "name":"%s", "domain_type_id":"%s", "space_id":"%s", "size":"%s", "left":"%s", "is_active":"%s", "created":"%s", "modified":"%s"}' % \
             (self.id, self.name, self.domain_type_id, self.space_id, self.size, \
                         self.left, self.is_active, self.created, self.modified)



def transactional(fn):
    """add transactional semantics to a method."""

    def transact(self, **args):
        session = Session()
        try:
            if fn.__name__ == 'get_by_kwargs':
                return fn(self, session, **args)
            else:
                fn(self, session, **args)
            session.commit()
        except Exception, e:
            print e
            session.rollback()
            raise
    transact.__name__ = fn.__name__
    return transact


class DomainLogic(object):
    """Performs Actions based on mask values"""
    
    def __init__(self):
        pass

    @transactional
    def add_data(self, session, **kwargs):
        create_record = Domain(**kwargs)
        print session.add(create_record)
        
    @transactional
    def delete_data_by_id(self, session, **kwargs):
        idx = kwargs.get('id','')
        delete_record = session.query(Domain).filter_by(id=idx).one()
        session.delete(delete_record)
        
    @transactional
    def update_data_by_id(self, session, **kwargs):
        idx = kwargs.get('id','')
        if idx != '':
            kwargs.pop('id')
            session.query(Domain).filter_by(id=idx).update(kwargs)
            
    @transactional
    def get_by_kwargs(self, session, **kwargs):
        return session.query(Domain).filter_by(**kwargs).all()
        



        

if __name__ == '__main__':
    
    domain_opr = DomainLogic()
#     add an data
#     i = 0
#     kwargs = {
# 
#                   'name' : 'testd',
#                   'domain_type_id' : 1,
#                   'space_id' : 1,
#                   'created' : datetime.datetime.now(),
#                   'modified' : datetime.datetime.now(),
#                   }      
#        
#     data_opr.add_data(**kwargs)
#         i = i + 1
        
#     delete a data by id
#     kwargs = {'id' : 4}
#     data_opr.delete_data_by_id(**kwargs)
#     
# #     update data by id
#     kwargs = {'id':7, 'm_storage_name':'niuniu', 'm_tenant_name':'hahahaahah'}
#     data_opr.update_data_by_id(**kwargs)
#     
# #     get data by conditions
    kwargs = {'name':'d1'}
    print (domain_opr.get_by_kwargs(**kwargs)[0]).id
#     result = str(data_opr.get_by_kwargs(**kwargs)[0])
#     import json
#     print json.loads(result).get('id')
#     print json.loads(result)
    
