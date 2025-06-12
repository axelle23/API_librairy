
import pytest
from sqlalchemy.orm import Session
from datetime import datetime

from src.models.loans import Loan as LoanModel
from src.repositories.loans import LoanRepository
from src.services.loans import LoanService
from src.api.schemas.loans import LoanCreate, LoanUpdate





def test_search_loans(db_session: Session):
    """
    Test de recherche des emprunts.
    """
    # Arrange
    repository = LoanRepository(LoanModel, db_session)
    service = LoanService(repository)
    # Créer plusieurs livres pour le test
    users_data = [       
        {
        "email": "test@example.com",
        "full_name": "test",
        "is_active": true,
        "is_admin": false,
        "password": "test123"
        }
    ]
    for user_data in users_data:
        db_session.add(LoanModel(**user_data))
        # Créer plusieurs livres pour le test
    books_data = [
        
        {
            "title": "Advanced Python",
            "author": "Jane Smith",
            "isbn": "2222222222222",
            "publication_year": 2021,
            "quantity": 2
        },
        {
            "title": "Java Programming",
            "author": "Bob Johnson",
            "isbn": "3333333333333",
            "publication_year": 2022,
            "quantity": 3
        }
    ]

    for book_data in books_data:
        db_session.add(LoanModel(**book_data))

    # Créer plusieurs emprunts pour le test
    loans_data = [
        
          {
            "user_id": 1,
            "book_id": 1,
            "loan_date": "2025-06-12T08:36:28.901Z",
            "return_date": "2025-06-12T08:36:28.901Z",
            "due_date": "2025-06-12T08:36:28.901Z"
            }
    ]
    
    for loan_data in loans_data:
        db_session.add(LoanModel(**loan_data))
    
    db_session.commit()
    
    # Act
    python_books = service.search(query="Python")
    
    # Assert
    assert len(python_books) == 2
    assert all("Python" in book.title for book in python_books)