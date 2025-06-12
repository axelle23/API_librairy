import pytest
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.models.loans import Loan
from src.repositories.loans import LoanRepository
from src.services.loans import LoanService
from src.api.schemas.loans import LoanCreate, LoanUpdate


def test_create_loan(db_session: Session):
    """
    Teste la création d'un emprunt.
    """
    repository = LoanRepository(Loan, db_session)
    service = LoanService(repository)

    loan_in = LoanCreate(
        user_id=1,
        book_id=1,
        loan_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=14),
        return_date=None
    )

    loan = service.create(obj_in=loan_in)

    assert loan.user_id == 1
    assert loan.book_id == 1
    assert loan.return_date is None
    assert loan.due_date > loan.loan_date


def test_update_loan(db_session: Session):
    """
    Teste la mise à jour d'un emprunt (ex. retour du livre).
    """
    repository = LoanRepository(Loan, db_session)
    service = LoanService(repository)

    loan_in = LoanCreate(
        user_id=1,
        book_id=2,
        loan_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=7),
        return_date=None
    )

    loan = service.create(obj_in=loan_in)

    # Mise à jour pour marquer comme retourné
    return_date = datetime.utcnow()
    loan_update = LoanUpdate(return_date=return_date)
    updated_loan = service.update(db_obj=loan, obj_in=loan_update)

    assert updated_loan.return_date == return_date


def test_get_loan_by_id(db_session: Session):
    """
    Teste la récupération d'un emprunt par ID.
    """
    repository = LoanRepository(Loan, db_session)
    service = LoanService(repository)

    loan_in = LoanCreate(
        user_id=2,
        book_id=1,
        loan_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=10),
        return_date=None
    )

    loan = service.create(obj_in=loan_in)
    retrieved_loan = service.get(id=loan.id)

    assert retrieved_loan is not None
    assert retrieved_loan.id == loan.id


def test_search_loans_by_user(db_session: Session):
    """
    Teste la recherche des emprunts d’un utilisateur donné.
    """
    repository = LoanRepository(Loan, db_session)
    service = LoanService(repository)

    # Créer plusieurs emprunts pour le même utilisateur
    for i in range(3):
        loan_in = LoanCreate(
            user_id=3,
            book_id=i + 1,
            loan_date=datetime.utcnow(),
            due_date=datetime.utcnow() + timedelta(days=15),
            return_date=None
        )
        service.create(obj_in=loan_in)

    loans = service.search(user_id=3)
    assert len(loans) == 3
    assert all(loan.user_id == 3 for loan in loans)


def test_create_loan_duplicate(db_session: Session):
    """
    Teste la tentative de création d’un emprunt déjà existant (même utilisateur, même livre non retourné).
    """
    repository = LoanRepository(Loan, db_session)
    service = LoanService(repository)

    loan_in = LoanCreate(
        user_id=4,
        book_id=5,
        loan_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=7),
        return_date=None
    )

    service.create(obj_in=loan_in)

    # Tentative de recréer un emprunt actif pour le même livre et utilisateur
    with pytest.raises(ValueError):
        service.create(obj_in=loan_in)
