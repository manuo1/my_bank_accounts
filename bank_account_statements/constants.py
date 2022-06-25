DATE_FORMAT = "%d/%m/%Y"

##############################################################################
# dateparser
##############################################################################
DATEPARSER_FRENCH_CODE = "fr"
DATEPARSER_ENGLISH_CODE = "en"

##############################################################################
# banks data
##############################################################################
CREDIT_AGRICOLE = "Crédit Agricole"
CREDIT_MUTUEL = "Crédit Mutuel"
FILENAME_DATE_FORMAT_CHOICES = [
    (DATEPARSER_FRENCH_CODE, "Jour / Mois / Année"),
    (DATEPARSER_ENGLISH_CODE, "Année / Mois / Jour"),
]
BANK_NAME_CHOICES = [
    (CREDIT_MUTUEL, CREDIT_MUTUEL),
    (CREDIT_AGRICOLE, CREDIT_AGRICOLE),
]

##############################################################################
# specific to data extraction in credit agricole statements
##############################################################################

CA_HEADER_ROW_INDICATOR = "þ"
CA_NEW_ROW_INDICATOR = "¨"
CA_CHECKSUM_KEY_WORD = "Total des opérations"
CA_OLD_BALANCE_KEY_WORD = "Ancien solde"
CA_NEW_BALANCE_KEY_WORD = "Nouveau solde"

##############################################################################
# specific to data extraction in credit mutuel statements
##############################################################################

CM_COLUMNS_LABELS = [
    "Date",
    "Date valeur",
    "Opération",
    "Débit EUROS",
    "Crédit EUROS",
]
CM_BALANCE_KEY_WORDS = "SOLDE"
CM_ROWS_DATE_FORMAT = "%d/%m/%Y"

##############################################################################
# other
##############################################################################

USELESS_WORDS_AT_THE_START_OF_THE_LABEL = [
    "carte",
    "prlv",
    "virement",
    "vir",
]


STARTING_BANK_BALANCE = 867.2
