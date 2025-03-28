from flask_openapi3.openapi import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS

from logger import logger

from schemas.financialEntrySchema import *
from schemas.creditCardSchema import *
from schemas.financialControlSchema import *
from schemas.financialEntryCategorySchema import *
from schemas.creditCardFlagSchema import *
from schemas.error import *

from pydantic import create_model

from service.exception.businessRulesException import BusinessRulesException
from service.financialEntryService import buildFinancialControl
from service.financialEntryService import insertFinancialEntry
from service.financialEntryService import updateFinancialEntry
from service.financialEntryService import deleteFinancialEntryById
from service.financialEntryService import searchAllFinancialEntryByType
from service.creditCardService import insertCreditCard
from service.creditCardService import updateCreditCard
from service.creditCardService import deleteCreditCard
from service.creditCardService import searchAllCreditCard
from service.creditCardService import searchCreditCardByNumber
from service.financialControlEntryService import updateFinancialControlEntry
from service.financialControlService import searchAllFinancialControl
from service.financialControlService import searchFinancialControlSummary
from service.financialControlEntryService import searchAllFinancialControlEntryByMonthAndYear
from service.financialEntryCategoryService import searchAllFinancialEntryCategory
from service.financialEntryCategoryService import searchFinancialEntryCategoryByEntryTypeId
from service.creditCardFlagService import searchAllCreditCardFlag
from service.domain.financialControlSummary import FinancialControlSummary

from model.financial_entry import FinancialEntry
from model.credit_card import CreditCard
from model.financial_control import FinancialControl
from model.financial_control_entry import FinancialControlEntry
from model.financial_entry_category import FinancialEntryCategory
from model.credit_card_flag import CreditCardFlag


information = Info(title="Personal Financial Control", version="1.0.0")
app = OpenAPI(__name__, info=information)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
entry_tag = Tag(name="Movimentações Financeiras", description="Adição, visualização e remoção de movimentações financeiras à base")
credit_card_tag = Tag(name="Cartões de Crédito", description="Adição, visualização e remoção de cartões de crédito à base")
financial_control_tag = Tag(name="Controle Mensal", description="Adição, visualização e remoção de controle mensal à base")
auxiliar_operation_tag = Tag(name="Operações Auxiliares", description="Consulta de cadastros na base de dados")


@app.get('/', summary="OpenApi Home", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# FINANTIAL ENTRY OPERATIONS 


@app.post('/financialEntry', summary="Salvar Nova Movimentação Financeira", tags=[entry_tag],
          responses={"200": FinancialEntrySchema, "400": ErrorSchema, "500": ErrorSchema})
def insertNewFinancialEntry(form:FinancialEntrySchemaToInsert):

    try:
        if (not form):
            raise BusinessRulesException('Dados de entrada não foram informados')
        
        logger.info(f'[insertNewFinancialEntry] - financial entry data received {form} !!')    
        
        financialEntry: FinancialEntry = insertFinancialEntry(form.name,form.entry_type_id,form.recurrent,form.start_date,form.finish_date,form.value,form.financial_entry_category_id,form.value_type_id,form.credit_card_id)

        if (not financialEntry):
            raise Exception('Movimentação não retornada!')

        logger.info(f'[insertNewFinancialEntry] - financial entry inserted with id {financialEntry.id}')
        return showFinancialEntry(financialEntry), 200

    except BusinessRulesException as e:
        logger.error(f'[insertNewFinancialEntry] - failed to insert financial entry : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[insertNewFinancialEntry] - failed to insert financial entry : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500
        


@app.get('/financialEntry/', summary="Obter movimentações filtradas por tipo", tags=[entry_tag],
          responses={"200": FinancialEntryCollectionSchema, "400": ErrorSchema, "500": ErrorSchema, "204":None})
def searchFinancialEntries(query:FinancialEntrySchemaToSearch):

    try:
        if (not query):
            raise BusinessRulesException('Dados de busca não foram informados')
        
        if (not query.entry_type_id):
            raise BusinessRulesException('ID do tipo de movimentação não foi informado')     

        logger.info(f'[searchFinancialEntries] - financial entry data received {query} !!')    
        
        financialSchemaEntries = []

        finantialEntries: List[FinancialEntry] = searchAllFinancialEntryByType(query.entry_type_id)
        if (finantialEntries and len(finantialEntries)>0):
            for financialEntry in finantialEntries:
                financialSchemaEntries.append(showFinancialEntry(financialEntry))

            logger.info(f'[searchFinancialEntries] - {0 if not finantialEntries else len(finantialEntries)} records founded !!')                

            return {"financialEntries":financialSchemaEntries}, 200
        else:
            return {}, 204

    except BusinessRulesException as e:
        logger.error(f'[searchFinancialEntries] - failed to search financial entries : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[searchFinancialEntries] - failed to search financial entries : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500
    


@app.patch('/financialEntry', summary="Atualizar Movimentação Financeira", tags=[entry_tag],
          responses={"200": FinancialEntrySchema, "400": ErrorSchema, "500": ErrorSchema})
def updateFinancialEntryData(form:FinancialEntrySchemaToUpdate):

    try:
        if (not form):
            raise BusinessRulesException('Dados de atualização não foram informados')
        
        logger.info(f'[updateFinancialEntryData] - financial entry data received {form} !!') 
        
        financialEntry: FinancialEntry = updateFinancialEntry(form.id,None,None,None,form.start_date,form.finish_date,form.value,form.financial_entry_category_id,None,form.credit_card_id)

        if (not financialEntry):
            raise Exception('Movimentação não retornada!')
        
        logger.info(f'[updateFinancialEntryData] - updated financial entry {financialEntry.id} !!') 

        return showFinancialEntry(financialEntry), 200

    except BusinessRulesException as e:
        logger.error(f'[updateFinancialEntryData] - failed to update financial entry : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[updateFinancialEntryData] - failed to update financial entry : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500  



@app.delete('/financialEntry', summary="Excluir Movimentação Financeira", tags=[entry_tag],
          responses={"200": FinancialEntryDelSchema, "400": ErrorSchema, "500": ErrorSchema})
def deleteFinancialEntryData(form:FinancialEntrySchemaToDelete):

    try:
        if (not form):
            raise BusinessRulesException('Dados de exclusão não foram informados')
        
        logger.info(f'[deleteFinancialEntryData] - financial entry data received {form} !!') 
        
        deleteFinancialEntryById(form.id)

        logger.info(f'[deleteFinancialEntryData] - deleted financial entry {form.id} !!') 

        return {"message":"Entrada excluida com sucesso."}, 200

    except BusinessRulesException as e:
        logger.error(f'[deleteFinancialEntryData] - failed to delete financial entry : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[deleteFinancialEntryData] - failed to delete financial entry : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500 
    

# CREDIT CARD OPERATIONS    


@app.post('/creditCard', summary="Salvar Cartão de Crédito", tags=[credit_card_tag],
          responses={"200": CreditCardSchema, "400": ErrorSchema, "500": ErrorSchema})
def insertNewCreditCard(form:CreditCardSchemaToInsert):

    try:
        if (not form):
            raise BusinessRulesException('Dados de entrada não foram informados')
        
        logger.info(f'[insertNewCreditCard] - credit data received {form} !!')    
        
        creditCard: CreditCard = insertCreditCard(form.name,form.number,form.valid_month_date,form.valid_year_date,form.credit_card_flag_id)

        if (not creditCard):
            raise Exception('Cartão de crédito não retornado!')

        logger.info(f'[insertNewCreditCard] - creditCard inserted with id {creditCard.id}')
        return showCreditCard(creditCard), 200

    except BusinessRulesException as e:
        logger.error(f'[insertNewCreditCard] - failed to insert credit card : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[insertNewCreditCard] - failed to insert credit card : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500



@app.get('/creditCard', summary="Obter cartões de crédito", tags=[credit_card_tag],
          responses={"200": CreditCardCollectionSchema, "400": ErrorSchema, "500": ErrorSchema, "204":None})
def searchCreditCards():

    try:  
        
        creditCardSchemas = []

        creditCards: List[CreditCard] = searchAllCreditCard()
        if (creditCards and len(creditCards)>0):
            for creditCard in creditCards:
                logger.info(creditCard)
                creditCardSchemas.append(showCreditCard(creditCard))

            logger.info(f'[searchCreditCards] - {0 if not creditCards else len(creditCards)} records founded !!')                

            return {"creditCards":creditCardSchemas}, 200
        else:
            return {}, 204

    except BusinessRulesException as e:
        logger.error(f'[searchCreditCards] - failed to search credit cards : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[searchCreditCards] - failed to search credit cards : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500
    


@app.get('/creditCard/', summary="Obter cartões de crédito pelo número",  tags=[credit_card_tag],
          responses={"200": CreditCardSchema, "400": ErrorSchema, "500": ErrorSchema, "204":None})
def searchCreditCardByGivenNumber(query:CreditCardSchemaToSearch):

    try:
        if (not query):
            raise BusinessRulesException('Dados de busca não foram informados')
        
        if (not query.number):
            raise BusinessRulesException('Numero do cartão não foi informado')     

        logger.info(f'[searchCreditCardByGivenNumber] - credit card data received {query} !!')    
        
        creditCard: CreditCard = searchCreditCardByNumber(query.number)

        if (creditCard):
            logger.info(f'[searchCreditCardByGivenNumber] - credit card founded {creditCard.id} !!')
            return showCreditCard(creditCard), 200
        else:
            return {}, 204

    except BusinessRulesException as e:
        logger.error(f'[searchFinancialEntries] - failed to search financial entries : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[searchFinancialEntries] - failed to search financial entries : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500



@app.patch('/creditCard', summary="Atualizar cartão de crédito",  tags=[credit_card_tag],
          responses={"200": CreditCardSchema, "400": ErrorSchema, "500": ErrorSchema})
def updateCreditCardData(form:CreditCardSchemaToUpdate):

    try:
        if (not form):
            raise BusinessRulesException('Dados de atualização não foram informados')
        
        logger.info(f'[updateCreditCardData] - credit card data received {form} !!') 
        
        creditCard: CreditCard = updateCreditCard(form.name,form.number,form.valid_month_date,form.valid_year_date,form.credit_card_flag_id)

        if (not creditCard):
            raise Exception('Cartão de Credito não retornado!')
        
        logger.info(f'[updateCreditCardData] - updated credit card {creditCard.id} !!') 

        return showCreditCard(creditCard), 200

    except BusinessRulesException as e:
        logger.error(f'[updateCreditCardData] - failed to update credit card : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[updateCreditCardData] - failed to update credit card : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500  



@app.delete('/creditCard', summary="Excluir cartão de crédito",  tags=[credit_card_tag],
          responses={"200": CreditCardDelSchema, "400": ErrorSchema, "500": ErrorSchema})
def deleteCreditCardData(form:CreditCardSchemaToDelete):

    try:
        if (not form):
            raise BusinessRulesException('Dados de exclusão não foram informados')
        
        logger.info(f'[deleteCreditCardData] - credit card data received {form} !!') 
        
        deleteCreditCard(form.number)

        logger.info(f'[deleteCreditCardData] - credit card id {form.number} !!') 

        return {"message":"Entrada excluida com sucesso."}, 200

    except BusinessRulesException as e:
        logger.error(f'[deleteCreditCardData] - failed to delete credit card : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[deleteCreditCardData] - failed to delete credit card : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500     



# FINANCIAL CONTROL OPERATIONS      



@app.post('/financialControl', summary="Criar novo controle mensal", tags=[financial_control_tag],
          responses={"200": None, "400": ErrorSchema, "500": ErrorSchema, "204": None})
def insertNewFinancialControlMonth(form:FinancialControlSchemaToInsert):

    try:
        if (not form):
            raise BusinessRulesException('Dados de entrada não foram informados')
        
        logger.info(f'[insertNewFinancialControlMonth] - financial control data received {form} !!')    
        
        buildFinancialControl(form.month,form.year)

        logger.info(f'[insertNewFinancialControlMonth] - control created !!')

        return {}, 204

    except BusinessRulesException as e:
        logger.error(f'[insertNewFinancialControlMonth] - failed to insert financial control : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[insertNewFinancialControlMonth] - failed to insert financial control : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500
        

       
@app.get('/financialControl', summary="Obter controles mensais criados", tags=[financial_control_tag],
          responses={"200": FinancialControlCollectionSchema, "400": ErrorSchema, "500": ErrorSchema, "204": None})
def searchFinancialControls():

    try:  
        
        financialControlSchemas = []

        financialControls: List[FinancialControl] = searchAllFinancialControl()
        if (financialControls and len(financialControls)>0):
            for financialControl in financialControls:
                financialControlSchemas.append(showFinancialControl(financialControl))
            
            logger.info(f'[searchFinancialControls] - {len(financialControls)} records founded !!') 
            
            return {"financialControls":financialControlSchemas}, 200
        else:
            return {}, 204

    except BusinessRulesException as e:
        logger.error(f'[searchFinancialControls] - failed to search financial controls : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[searchFinancialControls] - failed to search financial controls : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500
    


@app.get('/financialControl/', summary="Obter as Movimentações respectivas a um controle mensal", tags=[financial_control_tag],
          responses={"200": FinancialControlEntryCollectionSchema, "400": ErrorSchema, "500": ErrorSchema, "204":None})
def searchAllFinancialControlEntries(query:FinancialControlEntrySchemaToSearch):

    try:
        if (not query):
            raise BusinessRulesException('Dados de busca não foram informados')
        
        logger.info(f'[searchAllFinancialControlEntries] - method data received {query} !!')    
        
        financialControlEntries: List[FinancialControlEntry] = searchAllFinancialControlEntryByMonthAndYear(query.month,query.year)

        financialControlEntrySchemas = []

        if (financialControlEntries and len(financialControlEntries)>0):
            for financialControlEntry in financialControlEntries:
                financialControlEntrySchemas.append(showFinancialControlEntries(financialControlEntry))

            logger.info(f'[searchAllFinancialControlEntries] - {len(financialControlEntries)} records founded !!')                

            return {"financialControlEntries":financialControlEntrySchemas}, 200
        else:
            return {}, 204 

    except BusinessRulesException as e:
        logger.error(f'[searchAllFinancialControlEntries] - failed to search financial entries : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[searchAllFinancialControlEntries] - failed to search financial entries : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500



@app.get('/financialControl/summary/', summary="Obter o resumo de um controle mensal", tags=[financial_control_tag],
          responses={"200": FinancialControlSummarySchema, "400": ErrorSchema, "500": ErrorSchema, "204":None})
def searchFinancialControlSummaryData(query:FinancialControlSchemaToSearch):

    try:
        if (not query):
            raise BusinessRulesException('Dados de busca não foram informados')
        
        logger.info(f'[searchFinancialControlSummaryData] - financial control data received {query} !!')    
        
        financialControlSummary: FinancialControlSummary = searchFinancialControlSummary(query.month,query.year)

        if (financialControlSummary):
            logger.info(f'[searchFinancialControlSummaryData] - financial control summary founded !!')
            return showFinancialControlSummary(financialControlSummary), 200
        else:
            return {}, 204

    except BusinessRulesException as e:
        logger.error(f'[searchFinancialControlSummaryData] - failed to search financial control summary : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[searchFinancialControlSummaryData] - failed to search financial control summary : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500



@app.patch('/financialControl', summary="Atualizar a movimentação de um controle mensal", tags=[financial_control_tag],
          responses={"200": None, "400": ErrorSchema, "500": ErrorSchema, "204": None})
def updateFinancialControlEntryData(form:FinancialControlEntrySchemaToUpdate):

    try:
        if (not form):
            raise BusinessRulesException('Dados de atualização não foram informados')
        
        logger.info(f'[updateFinancialControlEntryData] - financial control entry data received {form} !!') 
        
        updateFinancialControlEntry(form.month,form.year,form.financialEntryId,form.value,None)
      
        logger.info(f'[updateFinancialControlEntryData] - updated !!') 

        return {}, 204

    except BusinessRulesException as e:
        logger.error(f'[updateFinancialControlEntryData] - failed to update financial control entry : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[updateFinancialControlEntryData] - failed to update financial control entry : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500  
    

# FINANCIAL CATEGORY QUERIES


@app.get('/financialControlCategory/', summary="Obter as categorias por tipo de movimentação", tags=[auxiliar_operation_tag],
          responses={"200": FinancialEntryCategoryCollectionSchema, "400": ErrorSchema, "500": ErrorSchema, "204":None})
def searchAllFinancialControlCategoriesByEntryTypeId(query:FinancialEntryCategorySchemaToSearch):

    try:
        if (not query):
            raise BusinessRulesException('Dados de busca não foram informados')
        
        logger.info(f'[searchAllFinancialControlCategoriesByEntryTypeId] - method data received {query} !!')    
        
        financialEntryCategories: List[FinancialEntryCategory] = searchFinancialEntryCategoryByEntryTypeId(query.entry_type_id)

        financialEntryCategorySchemas = []

        if (financialEntryCategories and len(financialEntryCategories)>0):
            for financialEntryCategory in financialEntryCategories:
                financialEntryCategorySchemas.append(showFinancialEntryCategorySchema(financialEntryCategory))

            logger.info(f'[searchAllFinancialControlCategoriesByEntryTypeId] - {len(financialEntryCategories)} records founded !!')                

            return {"financialEntryCategories":financialEntryCategorySchemas}, 200
        else:
            return {}, 204


    except BusinessRulesException as e:
        logger.error(f'[searchAllFinancialControlEntries] - failed to search financial entries : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[searchAllFinancialControlEntries] - failed to search financial entries : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500
    


@app.get('/financialControlCategory', summary="Obter as categorias de movimentação disponiveis",  tags=[auxiliar_operation_tag],
          responses={"200": FinancialEntryCategoryCollectionSchema, "400": ErrorSchema, "500": ErrorSchema, "204":None})
def searchAllFinancialControlCategoriesData():

    try:       
        financialEntryCategories: List[FinancialEntryCategory] = searchAllFinancialEntryCategory()

        financialEntryCategorySchemas = []

        if (financialEntryCategories and len(financialEntryCategories)>0):
            for financialEntryCategory in financialEntryCategories:
                financialEntryCategorySchemas.append(showFinancialEntryCategorySchema(financialEntryCategory))

            logger.info(f'[searchAllFinancialControlCategoriesData] - {len(financialEntryCategories)} records founded !!')                

            return {"financialEntryCategories":financialEntryCategorySchemas}, 200
        else:
            return {}, 204


    except BusinessRulesException as e:
        logger.error(f'[searchAllFinancialControlCategoriesData] - failed to search financial entries : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[searchAllFinancialControlCategoriesData] - failed to search financial entries : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500    
    

# CREDIT CARD FLAG QUERIES    


@app.get('/creditCardFlag', summary="Obter as bandeiras de cartão disponiveis", tags=[auxiliar_operation_tag],
          responses={"200": CreditCardFlagCollectionSchema, "400": ErrorSchema, "500": ErrorSchema, "204":None})
def searchAllCreditCardFlagsData():

    try:        
        creditCardFlags: List[CreditCardFlag] = searchAllCreditCardFlag()

        creditCardFlagSchemas = []

        if (creditCardFlags and len(creditCardFlags)>0):
            for creditCardFlag in creditCardFlags:
                creditCardFlagSchemas.append(showCreditCardFlagSchema(creditCardFlag))

            logger.info(f'[searchAllCreditCardFlagsData] - {len(creditCardFlags)} records founded !!')                

            return {"creditCardFlags":creditCardFlagSchemas}, 200
        else:
            return {}, 204


    except BusinessRulesException as e:
        logger.error(f'[searchAllCreditCardFlagsData] - failed to search credit card flags : {str(e)}',exc_info=True)
        return {"message":str(e)}, 400
    except Exception as e:
        logger.error(f'[searchAllCreditCardFlagsData] - failed to search credit card flags : {str(e)}',exc_info=True)
        return {"message":str(e)}, 500        