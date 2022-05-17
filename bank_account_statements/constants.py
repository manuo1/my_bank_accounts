DATE_FORMAT = '%d/%m/%Y'

##############################################################################
# banks
##############################################################################
CREDIT_AGRICOLE = "Crédit Agricole"
CREDIT_MUTUEL = "Crédit Mutuel"

##############################################################################
# dateparser
##############################################################################
DATEPARSER_FRENCH_CODE = 'fr'
DATEPARSER_ENGLISH_CODE = 'en'

##############################################################################
# specific to data extraction in credit agricole statements
##############################################################################

CA_HEADER_ROW_INDICATOR = 'þ'
CA_NEW_ROW_INDICATOR = '¨'
CA_CHECKSUM_KEY_WORD = 'Total des opérations'
CA_OLD_BALANCE_KEY_WORD = 'Ancien solde'
CA_NEW_BALANCE_KEY_WORD = 'Nouveau solde'

##############################################################################
# specific to data extraction in credit mutuel statements
##############################################################################

CM_COLUMNS_LABELS = [
    'Date',
    'Date valeur',
    'Opération',
    'Débit EUROS',
    'Crédit EUROS'
]

CM_BALANCE_KEY_WORDS = "SOLDE"
CM_ROWS_DATE_FORMAT = '%d/%m/%Y'