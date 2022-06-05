from trace import Trace
from bank_account_statements.models import Transaction
from current_month.selectors import get_transactions_ws_list


def create_transactions_with_bank_web_site_data():
    Transaction.objects.filter(statement__isnull=True).delete()
    transactions_ws = get_transactions_ws_list()


# class Transaction(models.Model):
#     statement = models.ForeignKey(
#         Statement, blank=True, null=True, on_delete=models.CASCADE
#     )
#     date = models.DateField()
#     label = models.CharField(max_length=255)
#     value = models.DecimalField(max_digits=20, decimal_places=2)
#     category = models.ForeignKey(
#         Category, blank=True, null=True, on_delete=models.SET_NULL
#     )
#     extended_label = models.CharField(max_length=255, blank=True)
#     custom_label = models.CharField(max_length=255, blank=True)


# dateOperation ="May 10, 2022, 12:00:00 AM"
# dateValeur ="May 10, 2022, 12:00:00 AM"
# typeOperation ="6"
# codeTypeOperation ="26"
# familleTypeOperation ="6"
# libelleOperation ="WEB OUDOT ROMANE temp pb google"
# libelleTypeOperation ="VIREMENT EMIS           "
# montant =-71.62
# idDevise = "EUR"
# libelleDevise ="€"
# libelleComplementaire ="temp pb google"
# referenceMandat =""
# idCreancier =""
# libelleCash1 =""
# libelleCash2 =""
# idCarte =""
# indexCarte =-1
# referenceClient ="temp pb google"
# pictogrammeCSS ="npc-transfer"
# fitid ="6792431482362"
