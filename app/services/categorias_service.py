from fastapi import Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_session
from app.repositories.categorias_repository import CategoryRepository
from app.schemas.categorias_schema import CategoryCreate
from app.models.categorias_model import Category
import uuid

class CategoryService:
    def __init__(self, session: Session = Depends(get_session)):
        self.repo = CategoryRepository(session)

    def get_all_categories(self) -> list[Category]:
        return self.repo.get_all_categories()

    def get_category_by_id(self, id: uuid.UUID) -> Category:
        category = self.repo.get_category_by_id(id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    def create_category(self, category: CategoryCreate) -> Category:
        return self.repo.create_category(category)

    def update_category(self, id: uuid.UUID, category_data: CategoryCreate) -> Category:
        updated_category = self.repo.update_category(id, category_data)
        if not updated_category:
            raise HTTPException(status_code=404, detail="Category not found")
        return updated_category

    def delete_category(self, id: uuid.UUID):
        success = self.repo.delete_category(id)
        if not success:
            raise HTTPException(status_code=404, detail="Category not found")
