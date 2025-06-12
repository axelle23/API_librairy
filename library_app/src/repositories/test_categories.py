import pytest
from sqlalchemy.orm import Session

from src.models.categories import Category
from src.repositories.categories import CategoryRepository


def test_create_category(db_session: Session):
    """
    Teste la création d'une catégorie.
    """
    repository = CategoryRepository(Category, db_session)

    category_data = {
        "name": "Science Fiction",
        "description": "Books about science and fiction"
    }

    category = repository.create(obj_in=category_data)

    assert category.id is not None
    assert category.name == "Science Fiction"
    assert category.description == "Books about science and fiction"


def test_get_category_by_name(db_session: Session):
    """
    Teste la récupération d'une catégorie par nom.
    """
    repository = CategoryRepository(Category, db_session)

    category_data = {
        "name": "History",
        "description": "Historical books"
    }

    repository.create(obj_in=category_data)

    category = repository.get_by_name(name="History")

    assert category is not None
    assert category.name == "History"
    assert category.description == "Historical books"


def test_get_or_create_category(db_session: Session):
    """
    Teste le comportement de get_or_create.
    """
    repository = CategoryRepository(Category, db_session)

    # Première insertion
    category_1, created_1 = repository.get_or_create(
        defaults={"description": "Classic novels"},
        name="Classics"
    )
    assert created_1 is True
    assert category_1.name == "Classics"

    # Deuxième appel, ne crée pas une nouvelle instance
    category_2, created_2 = repository.get_or_create(
        defaults={"description": "Should not be used"},
        name="Classics"
    )
    assert created_2 is False
    assert category_2.id == category_1.id
