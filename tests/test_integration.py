import pytest
from src.repository import BookRepository
from src.service import LibraryService

@pytest.fixture
def service():
    repo = BookRepository(db_path=':memory:')
    repo.initialize()
    return LibraryService(repository=repo)

def test_adicionar_e_buscar_livro(service):
    service.add_book("001", "Python", "Autor", "Tech", 3, "A1")
    ok, results = service.search_books("Python")
    assert ok == True
    assert len(results) > 0

def test_busca_livro_inexistente(service):
    ok, msg = service.search_books("Inexistente")
    assert ok == False

def test_deletar_livro_sem_emprestimo(service):
    service.add_book("002", "Java", "Autor", "Tech", 2, "B1")
    ok, msg = service.delete_book("002")
    assert ok == True

def test_deletar_livro_com_emprestimo(service):
    service.add_book("003", "Clean Code", "Martin", "Tech", 1, "C1")
    service.issue_book("003", "EST01")
    ok, msg = service.delete_book("003")
    assert ok == False
    assert "emprestado" in msg

def test_emprestar_e_devolver_livro(service):
    service.add_book("004", "DDD", "Evans", "Tech", 2, "D1")
    ok, msg = service.issue_book("004", "EST02")
    assert ok == True
    ok, msg = service.return_book("004", "EST02")
    assert ok == True

def test_emprestar_livro_sem_copias(service):
    service.add_book("005", "Refactoring", "Fowler", "Tech", 0, "E1")
    ok, msg = service.issue_book("005", "EST03")
    assert ok == False
    assert "indisponivel" in msg

def test_emprestar_livro_inexistente(service):
    ok, msg = service.issue_book("999", "EST04")
    assert ok == False
    assert "nao encontrado" in msg

def test_cadastro_campos_vazios(service):
    ok, msg = service.add_book("", "", "", "", 0, "")
    assert ok == False
    assert "vazios" in msg
