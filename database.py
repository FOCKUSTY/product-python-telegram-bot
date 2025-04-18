from sqlalchemy import create_engine, Column, Integer, String, Float, select
from sqlalchemy.orm import declarative_base, sessionmaker, session

engine = create_engine("sqlite:///test.db")
Base = declarative_base()

class ProductBase(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    address = Column(String(100), nullable=False)

    description = Column(String(255))
    image_url = Column(String(255))

    def get(self, *whereclause):
        return session.scalars(select(self).where(whereclause)).one()

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price}, count={self.count}, address={self.description})>"

Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

class Product:
    def create(self):
        session.add(ProductBase(
            name=self.name,
            price=self.price,
            count=self.count,
            address=self.address,
            description=self.description,
            image_url=self.image_url,
        ))

        session.commit()

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price}, count={self.count}, address={self.description})>"

    def __init__(self, name: str, price: float, address: str, count: int, description: str, image_url: str):
        self.name = name
        self.price = price
        self.count = count
        self.address = address
        self.description = description
        self.image_url = image_url

        self.create()
        
def get(data, *whereclause):
    if whereclause: return session.scalars(select(data).where(whereclause)).all()
    else: return session.scalars(select(data)).all()

if __name__ == "__main__":
    Product("NewName", 500.00, "г. Уфа ул. Пушкина 56", 10, "", "")
    Product("1234", 1500.00, "г. Якутия ул. Мерзлякина 33", 1200, "", "")
    Product("0000", 100.00, "г. Моска ул. ул. Бурга 10", 1400, "", "")