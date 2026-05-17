import bcrypt
from repository import BookRepository

class LibraryService:
    def __init__(self, repository=None):
        self.repo = repository or BookRepository()

    # ─── Livros ───────────────────────────────────────────

    def add_book(self, book_id, title, author, genre, copies, location):
        # BUG CORRIGIDO: validação usava 'and' incorretamente
        # Original: if (a and b and c and d and f) == ""
        # Correto: verificar cada campo individualmente
        if not book_id or not title or not author or not genre or not location:
            return False, "Campos não podem estar vazios."
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
            return False, "Livro já cadastrado."

    def search_books(self, term):
        if not term:
            return False, "Campo de busca não pode estar vazio."
        results = self.repo.search_books(term.capitalize())
        if not results:
            return False, "Nenhum livro encontrado."
        return True, results

    def get_all_books(self):
        return self.repo.get_all_books()

    def delete_book(self, book_id):
        # BUG CORRIGIDO: condição estava invertida
        # Original: if ab != 0 → deletava mesmo com empréstimo ativo
        # Correto: verificar se há empréstimo ativo antes de deletar
        if self.repo.is_book_issued(book_id):
            return False, "Livro está emprestado e não pode ser deletado."
        self.repo.delete_book(book_id)
        return True, "Livro deletado com sucesso."

    def update_copies(self, book_id, amount, current_copies):
        if amount < 0:
            return False, "Quantidade não pode ser negativa."
        if amount > current_copies:
            return False, "Quantidade excede o número de cópias disponíveis."
        self.repo.update_copies(book_id, amount)
        return True, "Cópias atualizadas com sucesso."

    # ─── Empréstimos ──────────────────────────────────────

    def issue_book(self, book_id, student_id):
        # BUG CORRIGIDO: validação e ordem de verificação
        # Original: validava campos DEPOIS de consultar o banco
        # Original: except genérico mascarava erros reais
        if not book_id or not student_id:
            return False, "Campos não podem estar vazios."

        book = self.repo.get_book(book_id.capitalize())
        if not book:
            return False, "Livro não encontrado no banco de dados."

        if book[4] <= 0:
            return False, "Livro indisponível. Não há cópias disponíveis."

        if self.repo.is_book_issued(book_id.capitalize()):
            return False, "Livro já está emprestado para este estudante."

        self.repo.issue_book(book_id.capitalize(), student_id.capitalize())
        return True, "Livro emprestado com sucesso."

    def return_book(self, book_id, student_id):
        if not book_id or not student_id:
            return False, "Campos não podem estar vazios."

        book = self.repo.get_book(book_id.capitalize())
        if not book:
            return False, "Livro não encontrado no banco de dados."

        self.repo.return_book(book_id.capitalize(), student_id.capitalize())
        return True, "Livro devolvido com sucesso."

    def get_activity(self, term):
        return self.repo.get_issued_by(term.capitalize())

    def get_all_activity(self):
        return self.repo.get_all_issued()

    # ─── Autenticação ─────────────────────────────────────

    def verify_login(self, username, password, stored_hash):
        # BUG CORRIGIDO: senha era comparada em texto puro
        # Correto: verificar com bcrypt
        return bcrypt.checkpw(
            password.encode('utf-8'),
            stored_hash
        )

    def hash_password(self, password):
        return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )
