import bcrypt
from src.repository import BookRepository

class LibraryService:
    def __init__(self, repository=None):
        self.repo = repository or BookRepository()

    def add_book(self, book_id, title, author, genre, copies, location):
        if not book_id or not title or not author or not genre or not location:
            return False, "Campos nao podem estar vazios."
        try:
            self.repo.add_book(
                book_id.capitalize(),
                title.capitalize(),
                author.capitalize(),
                genre.capitalize(),
                copies,
                location.capitalize()
            )
            return True, "Livro adicionado com sucesso."
        except Exception:
            return False, "Livro ja cadastrado."

    def search_books(self, term):
        if not term:
            return False, "Campo de busca nao pode estar vazio."
        results = self.repo.search_books(term.capitalize())
        if not results:
            return False, "Nenhum livro encontrado."
        return True, results

    def get_all_books(self):
        return self.repo.get_all_books()

    def delete_book(self, book_id):
        if self.repo.is_book_issued(book_id):
            return False, "Livro esta emprestado e nao pode ser deletado."
        self.repo.delete_book(book_id)
        return True, "Livro deletado com sucesso."

    def update_copies(self, book_id, amount, current_copies):
        if amount < 0:
            return False, "Quantidade nao pode ser negativa."
        if amount > current_copies:
            return False, "Quantidade excede o numero de copias disponiveis."
        self.repo.update_copies(book_id, amount)
        return True, "Copias atualizadas com sucesso."

    def issue_book(self, book_id, student_id):
        if not book_id or not student_id:
            return False, "Campos nao podem estar vazios."
        book = self.repo.get_book(book_id.capitalize())
        if not book:
            return False, "Livro nao encontrado no banco de dados."
        if book[4] <= 0:
            return False, "Livro indisponivel. Nao ha copias disponiveis."
        if self.repo.is_book_issued(book_id.capitalize()):
            return False, "Livro ja esta emprestado para este estudante."
        self.repo.issue_book(book_id.capitalize(), student_id.capitalize())
        return True, "Livro emprestado com sucesso."

    def return_book(self, book_id, student_id):
        if not book_id or not student_id:
            return False, "Campos nao podem estar vazios."
        book = self.repo.get_book(book_id.capitalize())
        if not book:
            return False, "Livro nao encontrado no banco de dados."
        self.repo.return_book(book_id.capitalize(), student_id.capitalize())
        return True, "Livro devolvido com sucesso."

    def get_activity(self, term):
        return self.repo.get_issued_by(term.capitalize())

    def get_all_activity(self):
        return self.repo.get_all_issued()

    def verify_login(self, username, password, stored_hash):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            stored_hash
        )

    def hash_password(self, password):
        return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )
