from .models import Contract
from datetime import datetime, timedelta


# TODO (pejman) log crontab
def expired_contract_demand():
    expiration_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    expired_contracts = Contract.objects.filter(status=Contract.Status.ACTIVE)
    for contract in expired_contracts:
        exp = contract.create_time.strftime('%Y-%m-%d %H:%M:%S')
        if exp < expiration_date:
            contract.status = Contract.Status.ACCEPTED
            contract.save()
