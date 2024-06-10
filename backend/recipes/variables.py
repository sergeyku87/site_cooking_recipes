ALLOWED_LEN_NAME: int = 256
MINIMUM_TIME_COOKING: int = 1
REQUIRED_FIELDS_FOR_PATCH: tuple = ('ingredients', 'tags')

M2M = 'ManyRelatedManager'

FORMAT_ERR_PATCH: str = 'This field <| {} |> not correct'
FORMAT_FULL_LINK: str = '{}://{}/{}'
FORMAT_SHORT_LINK: str = '{}://{}/s/{}'
FORMAT_FILE_DOWNLOAD: str = '{} - {} {}\n'

ERROR_RESPONSE_CART: str = 'Этот товар уже в корзине'
ERROR_RESPONSE_FAVORITE: str = 'Этот товар уже в избранном'

VALIDATE_MSG_TAG: str = 'Поле тега не может быть пустым'
VALIDATE_MSG_UNIQUE_TAG: str = 'Тег должен быть уникальным'
VALIDATE_MSG_EXIST_TAG: str = 'Не существующий тег'

VALIDATE_MSG_INGREDIENT: str = 'Поле ингредиентов не может быть пустым'
VALIDATE_MSG_UNIQUE_INGREDIENT: str = 'Ингредиенты должны быть уникальными'
VALIDATE_MSG_COUNT_INGREDIENT: str = 'Количество ингредиентов меньше 1'
VALIDATE_MSG_EXIST_INGREDIENT: str = 'Не существующий ингредиент'

VALIDATE_MSG_COMMON: str = 'Не корректные данные'
VALIDATE_MSG_UNIQUE: str = "Такой рецепт с таким описанием уже есть."
VALIDATE_MSG_IMAGE: str = 'Некорректный тип загружаемого изображения'

PERMISSION_IS_AUTH: tuple = ('download_shopping_cart',)
PERMISSION_IS_OWNER: tuple = ('partial_update', 'update', 'destroy')
