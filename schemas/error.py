from pydantic import BaseModel, Field


class ErrorSchema(BaseModel):
    """ Define como uma mensagem de eero será representada
    """
    message: str = Field(description="Mensagem de erro, motivo da falha no processamento.") 
