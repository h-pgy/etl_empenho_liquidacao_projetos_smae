from .base_client import RestClient
from core.utils.date import current_year
from core.utils.proc_num import ProcNumExtractor
from core.exceptions import SofRespError, ProcNumError
from config import SOF_API_TOKEN, SOF_API_HOST, SOF_API_VERSION, MAX_RETRIES, MES_PADRAO

class EmpenhosAPISOF:

    version = SOF_API_VERSION

    def __init__(self) -> None:

        self.client = RestClient(
            domain=SOF_API_HOST,
            token=SOF_API_TOKEN
        )

        self.mes_padrao = MES_PADRAO
        self.ano_padrao = current_year()

        self.extract_proc_num = ProcNumExtractor()

    def list_envelope_resp(self, resp:dict|list)->list:
        
        if not resp:
            return []

        if isinstance(resp, dict):
            return [resp]
        if isinstance(resp, list):
            return resp
        else:
            raise TypeError('Response must be a dict or a list')
        
    def __get_empenhos_by_proc(self, num_proc:int, mes:int, ano:int, retries:int=0)->list[dict]:

        api_resp = self.client.get(self.version, 
                                   endpoint='empenhos', 
                                   anoEmpenho=ano, 
                                   mesEmpenho=mes,
                                   numProcesso=num_proc
                                   )
        #mudou o nome do parametro
        status = api_resp['metaDados']['txtStatus']
        if status!='OK':
            if retries < MAX_RETRIES:
                retries +=1
                self.__get_empenhos_by_proc(num_proc, mes, ano, retries)
            else:
                raise SofRespError(f'Erro na resposta da API do SOF: {status}')
        
        data = api_resp['lstEmpenhos']
        return self.list_envelope_resp(data)
    
    def __call__(self, num_proc:str, mes:int|None=None, ano:int|None=None)->list[dict]:
        
        if mes is None:
            mes = self.mes_padrao
        if ano is None:
            ano = self.ano_padrao

        num_proc_extracted = self.extract_proc_num(num_proc)
        if num_proc_extracted is None:
            raise ProcNumError(f'Número de processo inválido: {num_proc}')

        return self.__get_empenhos_by_proc(num_proc_extracted, mes, ano)