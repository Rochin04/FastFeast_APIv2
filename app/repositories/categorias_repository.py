from sqlmodel import Session, select
from app.models.categorias_model import Category
from app.schemas.categorias_schema import CategoryCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import uuid

class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_categories(self) -> list[Category]:
        return self.session.exec(select(Category)).all()

    def get_category_by_id(self, id: uuid.UUID) -> Category | None:
        return self.session.get(Category, id)

    def create_category(self, category: CategoryCreate) -> Category:
        db_category = Category.model_validate(category)
        self.session.add(db_category)
        try:
            self.session.commit()
            self.session.refresh(db_category)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una categoría con el nombre '{category.name}'."
            )
        return db_category

    def update_category(self, id: uuid.UUID, category_data: CategoryCreate) -> Category | None:
        db_category = self.get_category_by_id(id)
        if db_category:
            db_category.name = category_data.name
            self.session.add(db_category)
            try:
                self.session.commit()
                self.session.refresh(db_category)
            except IntegrityError:
                self.session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe una categoría con el nombre '{category_data.name}'."
                )
        return db_category

    def delete_category(self, id: uuid.UUID) -> bool:
        db_category = self.get_category_by_id(id)
        if db_category:
            self.session.delete(db_category)
            self.session.commit()
            return True
        return False
