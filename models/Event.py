from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from database.database import Base


class Event(Base):
    __tablename__ = "event"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    client: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(512))
    createdBy: Mapped[str] = mapped_column(String(64))
    createdOn: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return  f"Event(id={self.id!r}, client={self.client!r}, description={self.description!r}, createdBy={self.createdBy!r}, createdOn={self.createdOn!r})"
    
    def __init__(self, id, client, description, createdBy, createdOn = datetime.now()):
        self.id = id
        self.client = client
        self.description = description
        self.createdBy = createdBy
        self.createdOn = createdOn
    
    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id
        return
    
    def getClient(self):
        return self.client
    
    def setClient(self, client):
        self.client = client
        return
    
    def getDescription(self):
        return self.description
    
    def setDescription(self, description):
        self.description = description
        return
    
    def getCreatedBy(self):
        return self.createdBy
    
    def setCreatedBy(self, createdBy):
        self.createdBy = createdBy
        return
    
    def getCreatedOn(self):
        return self.createdOn
    
    def setCreatedOn(self, createdOn):
        self.createdOn = createdOn
        return
    
    def fromJSON(json):
        if json is list:
            objectList = []
            for item in json:
                objectList.append(Event(item['id'], item['client'], item['description'], item['createdBy'], item.get('createdOn', datetime.now())))
            return objectList
        return Event(json['id'], json['client'], json['description'], json['createdBy'], json.get('createdOn', datetime.now()))
    
    def toJSON(self):
        jsonData = {
            "id" : self.id,
            "client" : self.client,
            "description" : self.description,
            "createdBy" : self.createdBy,
            "createdOn" : self.createdOn
        }
        return jsonData