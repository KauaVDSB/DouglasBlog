class AuthenticationError(Exception):
    """Erro de autenticação: credenciais inválidas ou permissão negada."""


class EncryptationFailureError(Exception):
    """Erro ao verificar método de encriptação,"""


class QueryObjectManagementError(Exception):
    """Incapaz de modificar objeto no banco de dados."""


class GetAPIError(Exception):
    """API incapaz de retornar objetos requisitados."""


class ResourceNotSentError(Exception):
    """Recurso exigido não foi enviado."""


class ResourceNotFoundError(Exception):
    """Recurso não encontrado no banco de dados ou no armazenamento."""


class SupabaseManagementFileError(Exception):
    """Incapaz de executar ações do supabase no arquivo existente referenciado.
    Verifique se o arquivo foi manipulado manualmente."""
