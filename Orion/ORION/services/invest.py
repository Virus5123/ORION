from t_tech.invest import AsyncClient

class InvestService:

    def __init__(self, token):
        self.token = token

    async def get_accounts(self):
        ...