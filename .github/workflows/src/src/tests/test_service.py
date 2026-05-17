import pytest
from unittest.mock import MagicMock
from src.service import LibraryService

@pytest.fixture
def service():
    mock_repo = MagicMock()
    return LibraryService(repository=mock_repo)

# ─── Testes de cadastro de livro ──────────────────────────

def test_add_book_campos_vazios(service):
    ok, msg = service.add_book("", "Titulo", "Autor", "Genero", 1, "Local")
    assert ok == False
    assert "vazios" in msg

def test_add_book_sucesso(service):
    service.repo.add_book.return_value = None
    ok, msg = service.add_book("001", "Titulo", "Autor", "Genero", 1, "Local")
    assert ok == True

def test_add_book_duplicado(service):
    service.repo.add_book.side_effect = Exception("duplicado")
    ok, msg = service.add_book("001", "Titulo", "Autor", "Genero", 1, "Local")
    assert ok == False
    assert "cadastrado" in msg

# ─── Testes de deleção ────────────────────────────────────

def test_delete_book_emprestado(service):
    # BUG CORRIGIDO: antes deletava mesmo com empréstimo ativo
    service.repo.is_book_issued.return_value = True
    ok, msg = service.delete_book("001")
    assert ok == False
    assert "emprestado" in msg

def test_delete_book_sucesso(service):
    service.repo.is_book_issued.return_value = False
    ok, msg = service.delete_book("001")
    assert ok == True

# ─── Testes de empréstimo ─────────────────────────────────

def test_issue_book_campos_vazios(service):
    ok, msg = service.issue_book("", "")
    assert ok == False
    assert "vazios" in msg

def test_issue_book_nao_encontrado(service):
    service.repo.get_book.return_value = None
    ok, msg = service.issue_book("001", "EST01")
    assert ok == False
    assert "não encontrado" in msg

def test_issue_book_sem_copias(service):
    # livro com 0 cópias: posição [4] da tupla
    service.repo.get_book.return_value = ("001", "Titulo", "Autor", "Genero", 0, "Local")
    ok, msg = service.issue_book("001", "EST01")
    assert ok == False
    assert "indisponível" in msg

def test_issue_book_sucesso(service):
    service.repo.get_book.return_value = ("001", "Titulo", "Autor", "Genero", 2, "Local")
    service.repo.is_book_issued.return_value = False
    ok, msg = service.issue_book("001", "EST01")
    assert ok == True

# ─── Testes de autenticação ───────────────────────────────

def test_hash_e_verify_senha(service):
    # BUG CORRIGIDO: senha era texto puro, agora usa bcrypt
    hashed = service.hash_password("root")
    assert service.verify_login("admin", "root", hashed) == True

def test_verify_senha_errada(service):
    hashed = service.hash_password("root")
    assert service.verify_login("admin", "errada", hashed) == False
