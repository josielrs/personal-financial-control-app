from flask_openapi3.openapi import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS
from logger import logger
from schemas.financialEntrySchema import *
from schemas.error import *

from service.exception.businessRulesException import BusinessRulesException

from service.financialEntryService import insertFinancialEntry
from service.financialEntryService import updateFinancialEntry
from service.financialEntryService import deleteFinancialEntryById
from service.financialEntryService import searchAllFinancialEntryByType

from model.financial_entry import FinancialEntry

information = Info(title="Personal Financial Control", version="1.0.0")
app = OpenAPI(__name__, info=information)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
entry_tag = Tag(name="Movimentações Financeiras", description="Adição, visualização e remoção de movimentações financeiras à base")
credit_card_tag = Tag(name="Cartões de Crédito", description="Adição, visualização e remoção de cartões de crédito à base")
financial_control_tag = Tag(name="Controle Mensal", description="Adição, visualização e remoção de controle mensal à base")
auxiliar_operation_tag = Tag(name="Operações Auxiliares", description="Consulta de cadastros na base de dados")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/financialEntry', tags=[entry_tag],
          responses={"200": FinancialEntrySchema, "400": ErrorSchema, "500": ErrorSchema})
def insertNewFinancialEntry(form:FinancialEntrySchemaToInsert):

    try:
        if (not form):
            raise BusinessRulesException('Dados de entrada não foram informados')
        
        financialEntry: FinancialEntry = insertFinancialEntry(form.name,form.entry_type_id,form.recurrent,form.start_date,form.finish_date,form.value,form.financial_entry_category_id,form.value_type_id,form.credit_card_id)

        if (not financialEntry):
            raise Exception('Movimentação não retornada!')

        return showFinancialEntry(financialEntry), 200

    except BusinessRulesException as e:
        return {"message",str(e)}, 400
    except Exception as e:
        return {"message",str(e)}, 500
        

@app.get('/financialEntry', tags=[entry_tag],
          responses={"200": FinancialEntryCollectionSchema, "400": ErrorSchema, "500": ErrorSchema})
def searchFinancialEntries(form:FinancialEntrySchemaToSearch):

    try:
        if (not form):
            raise BusinessRulesException('Dados de busca não foram informados')
        
        if (not form.entry_type_id):
            raise BusinessRulesException('ID do tipo de movimentação não foi informado')        
        
        financialEntryCollectionSchema: FinancialEntryCollectionSchema = FinancialEntryCollectionSchema()
        financialEntryCollectionSchema.financialEntries = []

        finantialEntries: List[FinancialEntry] = searchAllFinancialEntryByType(form.entry_type_id)
        if (finantialEntries and len(finantialEntries)>0):
            for financialEntry in finantialEntries:
                financialEntryCollectionSchema.financialEntries.append(financialEntry)

        return financialEntryCollectionSchema, 200

    except BusinessRulesException as e:
        return {"message",str(e)}, 400
    except Exception as e:
        return {"message",str(e)}, 500
    

@app.patch('/financialEntry', tags=[entry_tag],
          responses={"200": FinancialEntrySchema, "400": ErrorSchema, "500": ErrorSchema})
def updateFinancialEntryData(form:FinancialEntrySchemaToUpdate):

    try:
        if (not form):
            raise BusinessRulesException('Dados de atualização não foram informados')
        
        financialEntry: FinancialEntry = updateFinancialEntry(form.id,None,None,None,form.start_date,form.finish_date,form.value,form.financial_entry_category_id,None,form.credit_card_id)

        if (not financialEntry):
            raise Exception('Movimentação não retornada!')

        return showFinancialEntry(financialEntry), 200

    except BusinessRulesException as e:
        return {"message",str(e)}, 400
    except Exception as e:
        return {"message",str(e)}, 500  


@app.delete('/financialEntry', tags=[entry_tag],
          responses={"200": FinancialEntrySchema, "400": ErrorSchema, "500": ErrorSchema})
def deleteFinancialEntryData(form:FinancialEntrySchemaToDelete):

    try:
        if (not form):
            raise BusinessRulesException('Dados de exclusão não foram informados')
        
        deleteFinancialEntryById(form.id)

        deleteData: FinancialEntryDelSchema = FinancialEntryDelSchema()
        deleteData.message = "Entrada excluida com sucesso."

        return deleteData, 200

    except BusinessRulesException as e:
        return {"message",str(e)}, 400
    except Exception as e:
        return {"message",str(e)}, 500       