from apps.investments.models import TransactionLog


class ReconciliationService:
    def reconcile(self, user_wallet, external_tx_list):
        mismatches = []

        for tx in external_tx_list:
            if not TransactionLog.objects.filter(reference_id=tx["tx_id"]).exists():
                mismatches.append(tx)

        return mismatches
