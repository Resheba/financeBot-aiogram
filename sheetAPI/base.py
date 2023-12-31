import gspread, dotenv, json, os

dotenv.load_dotenv()

CREDENTIALS = json.loads(os.getenv('CREDENTIALS'))
AUTH_USER = json.loads(os.getenv('AUTH_USER'))
TABLE_NAME = os.getenv('TABLE_NAME')

LIST_USER_NAME = os.getenv('LIST_USER_NAME')
LIST_OPERATIONS_NAME = os.getenv('LIST_OPERATIONS_NAME')

LIST_DIRECTIOINS_NAME = os.getenv('LIST_DIRECTIOINS_NAME')
LIST_OPERATIONS_TYPES_NAME = os.getenv('LIST_OPERATIONS_TYPES_NAME')

gc, user = gspread.oauth_from_dict(credentials=CREDENTIALS, authorized_user_info=AUTH_USER)

SHEET = gc.open(TABLE_NAME)

OPERATIONS = SHEET.worksheet(LIST_OPERATIONS_NAME)
USERS = SHEET.worksheet(LIST_USER_NAME)

DATE_FORMAT = '%d.%m.%Y %H:%M:%S'
BUTTONS_IN_OUT = ('Приход', 'Расход')


def operation_types_load():
    operations_types = SHEET.worksheet(LIST_OPERATIONS_TYPES_NAME)
    result_dict = dict()
    table = operations_types.get_all_values()

    for row in table:
        A, B, C = row[:3]
        
        if not A:
            A = last_A
        else: 
            last_A = A
            result_dict[A] = dict()

        if not B:
            B = last_B
        else: 
            last_B = B
            result_dict[A][B] = list()
        
        result_dict[A][B].append(C) if C else None
        row[0:2] = [A, B]
    
    return result_dict


OPERATIONS_TYPES = operation_types_load()


def direction_types_loader():
    directions_sheet = SHEET.worksheet(LIST_DIRECTIOINS_NAME)
    directions_table = directions_sheet.get_all_values()
    values = [value[0] for value in directions_table]
    return values

DIRECTIONS_TYPES = direction_types_loader()
