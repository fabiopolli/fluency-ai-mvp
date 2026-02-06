import re
from typing import Optional

class GuardrailService:
    """Serviço responsável por validar intenções antes de gastar tokens."""
    ADMIN_RESPONSES = {
        r"(preço|valor|custo|quanto custa)": "O valor dos nossos planos varia conforme a modalidade. Você pode conferir os detalhes em: fluency.io",
        r"(suporte|ajuda|atendimento|contato)": "Você pode falar com nosso suporte técnico pelo e-mail suporte@fluency.io ou pelo chat no portal do aluno.",
        r"(cancelar|cancelamento|estorno)": "Para solicitações de cancelamento, por favor entre em contato com nossa equipe financeira via portal do aluno."
    }

    @staticmethod
    def check(text: str) -> Optional[str]:
        for pattern, response in GuardrailService.ADMIN_RESPONSES.items():
            if re.search(pattern, text.lower()):
                return response
        return None