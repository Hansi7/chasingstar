# 导入:
from sqlalchemy import Column, String, create_engine, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, selectinload
from sqlalchemy.ext.declarative import declarative_base
import os

# 创建对象的基类:
Base = declarative_base()
# 配置
dbfile = 'db.sqlite'


# 定义User对象:
class Url(Base):
    # 表的名字:
    __tablename__ = 'urls'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String)
    date = Column(String)

    def __repr__(self):
        return '<Url:{},url:{}>'.format(self.id, self.url)


class Girl(Base):
    # 表的名字:
    __tablename__ = 'girls'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    scode = Column(String)
    date = Column(String)

    def __repr__(self):
        return "ID:{}\t {} \tSCODE:{}  UPDATED:{} ".format(self.id, self.name, self.scode, self.date)


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    girl_id = Column(Integer, ForeignKey('girls.id'))
    fcode = Column(String)
    date = Column(String)

    girl = relationship("Girl", back_populates="notes")

    def __repr__(self):
        return "ID:{}\t {}\t {}\t UPDATE:{}".format(self.id, self.girl.name, self.fcode, self.date)
        # return '<NOTE:id:' + str(self.id) + ', Girl_id:' + str(self.girl_id) + ', Fcode:' + self.fcode + '>'


Girl.notes = relationship("Note", order_by=Note.id, back_populates="girl")


class DbEngine:
    # 初始化数据库连接:
    engine = create_engine('sqlite:///' + dbfile, echo=False)
    # engine = create_engine('mysql+mysqlconnector://root:@localhost:3306/test')

    if not os.path.exists(dbfile):
        Base.metadata.create_all(engine)  # 创建表结构

    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)


if __name__ == '__main__':
    engine = DbEngine()
    session = engine.DBSession()
    # 创建新User对象:
    new_url = Url(url='https://www.javbus.com', date='2019-09-09')
    new_girl = Girl(scode='abc', date='2018-09-09', name='RIO')
    new_girl2 = Girl(scode='ab3', date='2018-09-10', name='MARY')
    new_note = Note(girl=new_girl, fcode='IPTD-999', date='2028-09-09')
    new_note2 = Note(girl=new_girl, fcode='IPTD-777', date='2028-09-03')
    # 添加到session:
    session.add(new_url)
    session.add(new_girl)
    session.add(new_girl2)
    session.add(new_note)
    session.add(new_note2)

    # 提交即保存到数据库:
    session.commit()
    session.close()
    for g, n in session.query(Girl, Note). \
            filter(Girl.id == Note.girl_id). \
            all():
        print(g)
        print(n)
    print('===================================')
    girls = session.query(Girl).join(Note).all()
    for girl in girls:
        print(girl)
    query = session.query(Girl, Note).select_from(Note).join(Girl).all()
    for q, n in query:
        print(q, n)
    print("==================================")
    g1 = session.query(Girl).options(selectinload(Girl.notes)).filter_by(name='RIO').one()
    print(g1)
    print(g1.notes)
