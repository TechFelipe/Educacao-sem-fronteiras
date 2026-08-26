from werkzeug.security import check_password_hash, generate_password_hash
from repositories.usuario_repository import UsuarioRepository


class AuthService:
    @staticmethod
    def cadastrar(email, senha, confirmar_senha):
        email = (email or '').strip().lower()
        senha = senha or ''
        confirmar_senha = confirmar_senha or ''

        if not email or not senha or not confirmar_senha:
            return False, 'Preencha todos os campos.'

        if '@' not in email or '.' not in email.split('@')[-1]:
            return False, 'Digite um e-mail válido.'

        if len(senha) < 6:
            return False, 'A senha deve ter pelo menos 6 caracteres.'

        if senha != confirmar_senha:
            return False, 'As senhas não coincidem.'

        if UsuarioRepository.buscar_por_email(email):
            return False, 'Este e-mail já está cadastrado.'

        # O protótipo não possui campo de nome; usamos a parte anterior ao @.
        nome = email.split('@')[0].replace('.', ' ').replace('_', ' ').title()
        UsuarioRepository.criar(nome, email, generate_password_hash(senha))
        return True, 'Cadastro realizado com sucesso!'

    @staticmethod
    def autenticar(email, senha):
        email = (email or '').strip().lower()
        senha = senha or ''
        usuario = UsuarioRepository.buscar_por_email(email)

        if not usuario:
            return None

        if check_password_hash(usuario.senha, senha):
            return usuario

        return None
