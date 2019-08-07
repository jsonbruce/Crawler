from flask import json
from sqlalchemy import exc, func
from . import db


class BaseModel():
    def add(self, resource):
        if resource is not None:
            try:
                db.session.add(resource)
                return db.session.commit()
            except exc.IntegrityError as e:
                db.session().rollback()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        if resource is not None:
            db.session.delete(resource)
            return db.session.commit()


class Project(BaseModel, db.Model, object):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    icon = db.Column(db.String())
    synopsis = db.Column(db.Text())
    accountId = db.Column(db.Integer())
    userName = db.Column(db.String())
    teamName = db.Column(db.String())
    email = db.Column(db.String())
    contactPhone = db.Column(db.String())
    typeCode = db.Column(db.Integer)
    typeName = db.Column(db.String())

    locationCode = db.Column(db.String())
    locationName = db.Column(db.String())
    cityCode = db.Column(db.String())
    cityName = db.Column(db.String())
    schoolId = db.Column(db.Integer)
    schoolName = db.Column(db.String())

    projectCompanyId = db.Column(db.Integer())
    progress = db.Column(db.Integer)
    status = db.Column(db.Integer())
    secretStatus = db.Column(db.Integer())
    eduCommitteeId = db.Column(db.Integer)
    createTime = db.Column(db.String())
    wasEquityStructure = db.Column(db.String())
    wasInvest = db.Column(db.Integer())
    wasRegister = db.Column(db.Integer())
    wasBindUniTechnology = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(**kwargs)

        if args:  # position args
            if len(args) == 1:  # only one data passed
                if isinstance(args[0], dict):
                    self.init_with_json(args[0])
        if kwargs:  # keywords args
            for arg in kwargs:
                if isinstance(kwargs[arg], dict):
                    self.init_with_json(kwargs[arg])
                else:
                    self.__dict__[arg] = kwargs[arg]

    def init_with_json(self, data):
        if isinstance(data, dict):
            if data.has_key('id'):
                self.id = data['id']
            if data.has_key('schoolId'):
                self.schoolId = data['schoolId']
            if data.has_key('contactPhone'):
                self.contactPhone = data['contactPhone']
            if data.has_key('projectCompanyId'):
                self.projectCompanyId = data['projectCompanyId']
            if data.has_key('schoolName'):
                self.schoolName = data['schoolName']
            if data.has_key('typeName'):
                self.typeName = data['typeName']
            if data.has_key('accountId'):
                self.accountId = data['accountId']
            if data.has_key('teamName'):
                self.teamName = data['teamName']
            if data.has_key('progress'):
                self.progress = data['progress']
            if data.has_key("email"):
                self.email = data['email']
            if data.has_key('status'):
                self.status = data['status']
            if data.has_key('cityCode'):
                self.cityCode = data['cityCode']
            if data.has_key('wasInvest'):
                self.wasInvest = data['wasInvest']
            if data.has_key('wasRegister'):
                self.wasRegister = data['wasRegister']
            if data.has_key('eduCommitteeId'):
                self.eduCommitteeId = data['eduCommitteeId']
            if data.has_key('createTime'):
                self.createTime = data['createTime']
            if data.has_key('locationCode'):
                self.locationCode = data['locationCode']
            if data.has_key('icon'):
                self.icon = data['icon']
            if data.has_key('userName'):
                self.userName = data['userName']
            if data.has_key('wasEquityStructure'):
                self.wasEquityStructure = data['wasEquityStructure']
            if data.has_key('name'):
                self.name = data['name']
            if data.has_key('typeCode'):
                self.typeCode = data['typeCode']
            if data.has_key('cityName'):
                self.cityName = data['cityName']
            if data.has_key('locationName'):
                self.locationName = data['locationName']
            if data.has_key('synopsis'):
                self.synopsis = data['synopsis']
            if data.has_key('wasBindUniTechnology'):
                self.wasBindUniTechnology = data['wasBindUniTechnology']
            if data.has_key('secretStatus'):
                self.secretStatus = data['secretStatus']
        return self

    def to_json(self):
        return {
            "id": self.id,
            "schoolId": self.schoolId,
            "contactPhone": self.contactPhone,
            "schoolName": self.schoolName,
            "typeName": self.typeName,
            "accountId": self.accountId,
            "teamName": self.teamName,
            "progress": self.progress,
            "email": self.email,
            "status": self.status,
            "cityCode": self.cityCode,
            "wasInvest": self.wasInvest,
            "wasRegister": self.wasRegister,
            "eduCommitteeId": self.eduCommitteeId,
            "createTime": self.createTime,
            "locationCode": self.locationCode,
            "icon": self.icon,
            "userName": self.userName,
            "wasEquityStructure": self.wasEquityStructure,
            "name": self.name,
            "typeCode": self.typeCode,
            "cityName": self.cityName,
            "locationName": self.locationName,
            "synopsis": self.synopsis,
            "wasBindUniTechnology": self.wasBindUniTechnology,
            "secretStatus": self.secretStatus,
            "projectCompanyId": self.projectCompanyId
        }


class PageInfo():
    def __init__(self, *args, **kwargs):
        self.countOfCurrentPage = 1
        self.currentPage = 1
        self.pageResults = []
        self.totalCount = 1
        self.totalPage = 1

        if args:  # position args
            if len(args) == 1:  # only one data passed
                if isinstance(args[0], dict):
                    self.init_with_json(args[0])
        if kwargs:  # keywords args
            for arg in kwargs:
                if isinstance(kwargs[arg], dict):
                    self.init_with_json(kwargs[arg])
                else:
                    self.__dict__[arg] = kwargs[arg]

    def init_with_json(self, data):
        if isinstance(data, dict):
            self.countOfCurrentPage = data['countOfCurrentPage']
            self.currentPage = data['currentPage']
            self.totalCount = data['totalCount']
            self.totalPage = data['totalPage']
            for p in data['pageResults']:
                self.pageResults.append(Project(p))

        return self


def getProvinces():
    result = db.session.query(Project.locationName).distinct().order_by(Project.locationName).all()
    datas = []
    for row in result:
        datas.append(row[0])
    return datas


def getCities():
    result = db.session.query(Project.cityName).distinct().order_by(Project.cityName).all()
    datas = []
    for row in result:
        datas.append(row[0])
    return datas


def getCityProjects():
    sql = """
        SELECT cityName, count(*) AS projectCounts
        FROM projects
        GROUP BY cityName
        ORDER BY projectCounts DESC
        """
    result = db.engine.execute(sql)
    datas = {}
    for row in result:
        datas[row[0]] = row[1]
    return datas

    # db.session.query(Project.cityName, func.count(Project.id))\
    #     .group_by(Project.cityName).order_by().all()