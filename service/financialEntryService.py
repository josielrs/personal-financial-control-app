from repository.financialEntryRepository import insertFinancialEntry as insertFinancialEntryRep
from repository.financialEntryRepository import searchFinancialEntryById as searchFinancialEntryByIdRep
from repository.financialEntryRepository import searchAllFinancialEntry as searchAllFinancialEntryRep
from repository.financialEntryRepository import searchAllFinancialEntryByDates as searchAllFinancialEntryByDatesRep
from repository.financialEntryRepository import searchAllFinancialEntryByType as searchAllFinancialEntryByTypeRep
from repository.financialEntryRepository import updateFinancialEntry as updateFinancialEntryRep
from repository.financialEntryRepository import deleteFinancialEntryById as deleteFinancialEntryByIdRep
from model.financial_entry import FinancialEntry
from model.financial_control import FinancialControl
from model.financial_control_entry import FinancialControlEntry
from model.financial_entry_category import FinancialEntryCategory
from datetime import date
from service.domain.entryTypeEnum import EntryType
from service.domain.valueTypeEnum import ValueType
from service.domain.controlStatusEnum import ControlStatus
from service.financialEntryCategoryService import searchFinancialEntryCategoryById
from service.financialControlService import searchFinancialControlByInitialMonthAndYear
from service.financialControlService import searchAllFinancialControlWithNoEntries
from service.financialControlService import deleteFinancialControl
from service.financialControlService import insertFinancialControl
from service.creditCardService import searchCreditCardByNumber
from service.financialControlEntryService import insertFinancialControlEntry
from service.financialControlEntryService import searchAllFinancialControlEntryByInitialMonthAndYearAndEntryId
from service.financialControlEntryService import updateFinancialControlEntry
from service.financialControlEntryService import deleteFinancialControlEntry
from typing import List
from model.credit_card import CreditCard
from service.exception.businessRulesException import BusinessRulesException
import pandas as pd


def diff_month(d1:date, d2:date):
    return (d2.year - d1.year) * 12 + (d2.month - d1.month)


def __insertFinancialEntryData__(name:str,
                                entryTypeId:int,
                                recurrent:int,
                                startDate:date,
                                finishDate:date,
                                value:float,
                                financialEntryCategoryId:int,
                                valueTypeId:int,
                                creditCardNumber:int) -> int :
    
    if (not recurrent):
        recurrent = 0

    validateFinancialEntryData(name, entryTypeId, recurrent, startDate, finishDate, value, financialEntryCategoryId, valueTypeId, creditCardNumber, False, None, None)
        
    id: int = insertFinancialEntryRep(name, entryTypeId, recurrent, startDate, finishDate, value, financialEntryCategoryId, valueTypeId, creditCardNumber)

    # inserindo a movimentação dos controles mensais já criados
    financialControls: List[FinancialControl] = searchFinancialControlByInitialMonthAndYear(startDate.month,startDate.year)
    if (financialControls and (len(financialControls)>0)):
        for financialControl in financialControls:
            insertFinancialControlEntry(financialControl.month,financialControl.year,id,value,date(financialControl.year,financialControl.month,startDate.day))

    return id    
    

def insertFinancialEntry(name:str,
                         entryTypeId:int,
                         recurrent:int,
                         startDate:date,
                         finishDate:date,
                         value:float,
                         financialEntryCategoryId:int,
                         valueTypeId:int,
                         creditCardNumber:int) -> FinancialEntry:
      
    id: int = __insertFinancialEntryData__(name, entryTypeId, recurrent, startDate, finishDate, value, financialEntryCategoryId, valueTypeId, creditCardNumber)

    return searchFinancialEntryById(id)


def insertFinancialEntryByObject(financialEntry: FinancialEntry) -> FinancialEntry:

    if (not financialEntry):
        raise BusinessRulesException('Nenhuma movimentação finaceira foi informada para inserção !')
    
    id: int = __insertFinancialEntryData__(financialEntry.name,financialEntry.entry_type_id, financialEntry.recurrent,financialEntry.start_date,financialEntry.finish_date,
                               financialEntry.value,financialEntry.financial_entry_category_id,financialEntry.value_type_id,financialEntry.credit_card_number,False);

    return searchFinancialEntryById(id)


def searchAllFinancialEntry() -> List[FinancialEntry]:

    return searchAllFinancialEntryRep()


def searchAllFinancialEntryByType(entryTypeId:int) -> List[FinancialEntry]:

    if (not entryTypeId):
        raise BusinessRulesException('Tipo de movimentação finaceira deve ser informado !')
    
    if (entryTypeId and not EntryType.hasValue(entryTypeId)):
        raise BusinessRulesException('Tipo de movimentação financeira inválido !')    

    return searchAllFinancialEntryByTypeRep(entryTypeId)


def searchFinancialEntryById(id:int) -> FinancialEntry:

    if (not id):
        raise BusinessRulesException('Identificador da movimentação finaceira deve ser informado !')

    return searchFinancialEntryByIdRep(id)


def searchAllFinancialEntryByDates(startDate:date, finishDate:date) -> List[FinancialEntry]:

    if (not startDate and not finishDate):
        raise BusinessRulesException('Favor informar um dos parametros de data !!')
    
    if (startDate and finishDate and (startDate > finishDate)):
        raise BusinessRulesException('Data de inicio da movimentação financeira deve ser menor que a data fim !')    

    return searchAllFinancialEntryByDatesRep(startDate,finishDate)


def searchAllFinancialEntryByGivenMonthAndYear(month:int, year:int) -> List[FinancialEntry]:

    if (not month):
        raise BusinessRulesException('Mês de consulta deve ser informado !')    
    if (month < 1 or month > 12):
        raise BusinessRulesException('O mês informado para consulta, está inválido !!')
    if (not year):
        raise BusinessRulesException('Ano de consulta deve ser informado !')    
    if (year < 1900 or year > 2999):
        raise BusinessRulesException('O ano informado para consulta, está inválido !!')    

    return searchAllFinancialEntryByDates(date(year,month,1),pd.Period(year=year,month=month,day=1,freq='M').end_time.date())


def updateFinancialEntry(id:int,
                         name:str,
                         entryTypeId:int,
                         recurrent:int,
                         startDate:date,
                         finishDate:date,
                         value:float,
                         financialEntryCategoryId:int,
                         valueTypeId:int,
                         creditCardNumber:int) -> FinancialEntry:
    
    if (not id):
        raise BusinessRulesException('ID da Movimentação Financeira deve ser informado.')
    
    if (not recurrent):
        recurrent = 0    
    
    existingFinancialEntry : FinancialEntry = searchFinancialEntryById(id)

    validateFinancialEntryData(name, entryTypeId, recurrent, startDate, finishDate, value, financialEntryCategoryId, valueTypeId, creditCardNumber, True, existingFinancialEntry, id)

    updateFinancialEntryRep(id,name,entryTypeId,recurrent,startDate,finishDate,value,financialEntryCategoryId,valueTypeId,creditCardNumber)
    
    isFixValueChanged: bool = (value and (ValueType.FIXO.value == existingFinancialEntry.value_type_id) and (value != existingFinancialEntry.value))

    # Se o tipo de movimentacao tiver valor fixo ou teve alteração de dia nas datas de inicio e fim, procura os controles mensais e atualiza os dados
    if ( isFixValueChanged or ( startDate and (startDate != existingFinancialEntry.start_date) )):
        financialEntries: List[FinancialControlEntry] = searchAllFinancialControlEntryByInitialMonthAndYearAndEntryId(existingFinancialEntry.start_date.month,existingFinancialEntry.start_date.year,id)
        if (financialEntries and len(financialEntries)>0):
            for financialEntry in financialEntries:
                newValue: float = value if isFixValueChanged else financialEntry.value
                updateFinancialControlEntry(financialEntry.financial_control_month,financialEntry.financial_control_year,id,newValue,date(financialEntry.financial_control_year,financialEntry.financial_control_month,startDate.day))       

    return searchFinancialEntryById(id)


def deleteFinancialEntryById(id:int) -> None:

    if (not id):
        raise BusinessRulesException('Identificador da movimentação finaceira deve ser informado !')
    
    financialEntry:FinancialEntry = searchFinancialEntryById(id)
    if (financialEntry):

        #excluindo a movimentação dos controles existentes
        financialEntries: List[FinancialControlEntry] = searchAllFinancialControlEntryByInitialMonthAndYearAndEntryId(financialEntry.start_date.month,financialEntry.start_date.year,id)          
        if (financialEntries and len(financialEntries)>0):
            for financialEntry in financialEntries:
                deleteFinancialControlEntry(financialEntry.financial_control_month,financialEntry.financial_control_year,id) 

        #excluindo controles de meses sem nenhuma movimentacao associada            
        financialControls: List[FinancialControl] = searchAllFinancialControlWithNoEntries()
        if (financialControls and len(financialControls)>0):
            for financialControl in financialControls:
                deleteFinancialControl(financialControl.month,financialControl.year)

    deleteFinancialEntryByIdRep(id)


def validateFinancialEntryData(name:str,
                               entryTypeId:int,
                               recurrent:int,
                               startDate:date,
                               finishDate:date,
                               value:float,
                               financialEntryCategoryId:int,
                               valueTypeId:int,
                               creditCardNumber:int,
                               isUpdate: bool,
                               financialEntry: FinancialEntry,
                               id: int) -> None:
    
    if (isUpdate and not financialEntry):
        raise BusinessRulesException(f'Movimentação Financeira não encontrada com esse identificador:{id}')

    if (not name and not isUpdate):
        raise BusinessRulesException('A movimentação finaceira deve ter um nome associado a ela !')

    if (not entryTypeId and not isUpdate):
        raise BusinessRulesException('O tipo de movimentação finaceira deve ser informado !')

    if (entryTypeId and not EntryType.hasValue(entryTypeId)):
        raise BusinessRulesException('Tipo de movimentação financeira inválido !')
    
    if (entryTypeId and isUpdate and entryTypeId != financialEntry.entry_type_id):
        raise BusinessRulesException('Não é permitido mudar o tipo da movimentação financeira !')
    
    if (recurrent and not (recurrent == 0 or recurrent == 1)):
        raise BusinessRulesException('O parametro "recurrent" deve ser 0 (não) ou 1 (sim) !!')

    if (recurrent and isUpdate and recurrent != financialEntry.recurrent):
        raise BusinessRulesException('Não é permitido mudar a recorrencia da movimentação financeira !')          
    
    if (not startDate and not isUpdate):
        raise BusinessRulesException('Data de inicio da movimentação financeira deve ser informada !')

    if (finishDate and (recurrent == 0)):
        raise BusinessRulesException('Data fim só deve ser informada em movimentações recorrentes !')

    if (finishDate and (startDate > finishDate)):
        raise BusinessRulesException('Data de inicio da movimentação financeira deve ser menor que a data fim !')
    
    if (finishDate and diff_month(startDate,finishDate) <= 0):
        raise BusinessRulesException('Data de inicio e fim da movimentação financeira deve ser ter no minimo 1 mês de diferença !')  
    
    if (startDate and finishDate and startDate.day != finishDate.day):
        raise BusinessRulesException('O dia da Data de inicio e fim da movimentação financeira deve ser o mesmo !') 

    if (startDate and isUpdate and startDate.month != financialEntry.start_date.month):
        raise BusinessRulesException('Na data de inicio da movimentação financeira, não se pode alterar o mês !') 
    
    if (startDate and isUpdate and startDate.year != financialEntry.start_date.year):
        raise BusinessRulesException('Na data de inicio da movimentação financeira, não se pode alterar o ano !')     

    if (finishDate and isUpdate and not financialEntry.finish_date):   
        raise BusinessRulesException('A data fim da movimentação financeira não pode ser incluida !')     

    if (finishDate and isUpdate and finishDate.month != financialEntry.finish_date.month):
        raise BusinessRulesException('Na data fim da movimentação financeira, não se pode alterar o mês !')        
    
    if (finishDate and isUpdate and finishDate.year != financialEntry.finish_date.year):
        raise BusinessRulesException('Na data fim da movimentação financeira, não se pode alterar o ano !')      

    if (value and value < 0):
        raise BusinessRulesException('Valor da movimentação financeira não pode ser negativo !') 
    
    if (not financialEntryCategoryId and not isUpdate):
        raise BusinessRulesException('A categoria da movimentação finaceira deve ser informada !')
    
    if (financialEntryCategoryId):
        category:FinancialEntryCategory = searchFinancialEntryCategoryById(financialEntryCategoryId)
        if (not category):
            raise BusinessRulesException('A categoria da movimentação finaceira informada é inválida !')
    
    if (not valueTypeId and not isUpdate):
        raise BusinessRulesException('O tipo de valor da movimentação finaceira deve ser informado !')

    if (valueTypeId and not ValueType.hasValue(valueTypeId)):
        raise BusinessRulesException('Tipo de valor da movimentação financeira inválido !')
    
    if (valueTypeId and isUpdate and valueTypeId != financialEntry.value_type_id):
        raise BusinessRulesException('Não é permitido mudar o tipo de valor da movimentação financeira !')
    
    if (valueTypeId and ValueType.FIXO.value == valueTypeId and not value and not isUpdate):
        raise BusinessRulesException('A movimentação financeira com valor fixo deve ter um valor informado já no cadastro !')
    
    if (creditCardNumber and not(isUpdate and creditCardNumber == -1)):

        if (not EntryType.DESPESA.value == entryTypeId):
            raise BusinessRulesException('Cartão de crédito deve ser informado apenas em movimentações de DESPESA !')

        creditCardObj: CreditCard = searchCreditCardByNumber(creditCardNumber)
        if (not creditCardObj):
            raise BusinessRulesException('Cartão de crédito informado não encontrado !') 
        

""" 
buildFinancialControl, busca as movimentacões que compoem o mes informado
"""        

def buildFinancialControl(month: int, 
                           year: int) -> None:
    
    insertFinancialControl(month,year,ControlStatus.ABERTO.value)

    financialEntries:List[FinancialEntry] = searchAllFinancialEntryByGivenMonthAndYear(month,year)

    if (financialEntries and len(financialEntries)>0):

        for financialEntry in financialEntries:
            financialEntryDay:int = financialEntry.start_date.day
            insertFinancialControlEntry(month,year,financialEntry.id,financialEntry.value,date(year,month,financialEntryDay))