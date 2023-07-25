from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

engine = create_engine('postgresql://postgres:1qazxswedrT@localhost/ylabdb_new')
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


class Menu(Base):
    __tablename__ = "Menu"

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True, unique=False)
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)
    submenus = relationship('Submenu', back_populates='menu_items')

    def add_submenu_count(self, value: int):
        self.submenus_count += value

    def add_dishes_count(self, value: int):
        self.dishes_count += value

    def delete_submenu_count(self, value: int):
        self.submenus_count -= value

    def delete_dishes_count(self, value: int):
        self.dishes_count -= value


class Submenu(Base):
    __tablename__ = "Submenu"

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True, unique=False)
    dishes_count = Column(Integer, default=0)
    menu_id = Column(UUID, ForeignKey(Menu.id, ondelete='CASCADE'))
    menu_items = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu_items')

    def update_dishes_count(self, value: int):
        self.dishes_count += value

    def delete_dishes_count(self, value: int):
        self.dishes_count -= value


class Dish(Base):
    __tablename__ = "Dish"

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True, unique=False)
    price = Column(String)
    submenu_id = Column(UUID, ForeignKey(Submenu.id, ondelete='CASCADE'))
    submenu_items = relationship('Submenu', back_populates='dishes')


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    print('Database creation, please wait')
    Base.metadata.create_all(engine)
