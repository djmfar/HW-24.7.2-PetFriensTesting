from api_my import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='name', animal_type='animal_type',
                                    age=5, pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", 3, "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если спиок питомцев пустой, то добавляем нового питомца и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, name + animal_type + str(age), animal_type, age, "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Пробуем обновить имя, тип и возраст 1-го питомца из списка своих питомцев
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == name


# Мои тесты для задания 24.7.2

# Позитивные тесты для 2-х новых методов из файла api_my.py
def test_add_new_pet_without_photo_with_valid_data(name='Мурка', animal_type='киса', age=1):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_update_photo_of_pet_with_valid_pet_photo(pet_photo='images/P1040103.jpg'):
    """Проверяем, что можно обновить фото существующего питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Если спиок питомцев пустой, то добавляем нового питомца без фото и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, 'Барсик', 'котик', 2)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Выполняем запрос на обновление фото 1-го питомца из списка своих питомцев
    status, result = pf.update_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['id'] == my_pets['pets'][0]['id']


# Негативные тесты со статусом отличным от 200, описанными в документации
def test_get_api_key_for_invalid_email(email=valid_email * 2, password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 403 с некорректным email"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    #assert 'key' not in result


def test_get_all_pets_with_invalid_auth_key(filter=''):
    """ Проверяем, что запрос всех питомцев с некорректным ключом auth_key возвращается статус 403"""

    # Приравниваем переменной auth_key заведомо некорректное значение
    auth_key = {'key': valid_email}

    # Выполняем API запрос на получение списка питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    #assert 'pets' not in result


def test_add_new_pet_with_invalid_auth_key(name='name', animal_type='animal_type', age=5,
                                           pet_photo='images/cat1.jpg'):
    """Проверяем, что при добавлении питомца с корректными данными, но с некорректным ключом auth_key,
    возвращается статус 403"""

    # Приравниваем переменной auth_key заведомо некорректное значение
    auth_key = {'key': valid_email}

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Выполняем запрос на добавление питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    #assert 'pets' not in result


def test_add_new_pet_with_invalid_data(name=None, animal_type=None, age=None, pet_photo='images/cat1.jpg'):
    """Проверяем, что нельзя добавить питомца с некорректными name, animal_type и age"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    #assert 'pets' not in result


def test_unsuccessful_delete_self_pet_with_invalid_auth_key():
    """Проверяем невозможность удаления питомца с некорректным auth_key"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового питомца без фото
    # и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Суперкот", "кот", 3)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Приравниваем переменной auth_key заведомо некорректное значение
    auth_key = {'key': valid_email}

    # Берём корректный id 1-го питомца из списка, полученного с корректным auth_key
    # и отправляем запрос на удаление с некорректным auth_key
    status, _ = pf.delete_pet(auth_key, my_pets['pets'][0]['id'])

    # Проверяем что статус ответа равен 403
    assert status == 403


def test_unsuccessful_update_self_pet_info_with_invalid_auth_key(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем невозможность обновления информации о питомце с некорректным auth_key"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # если спиок питомцев пустой, то добавляем нового питомца без фото и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, name + animal_type + str(age), animal_type, age)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Приравниваем переменной auth_key заведомо некорректное значение
    auth_key = {'key': valid_email}

    # Берём корректный id первого питомца из списка, полученного с корректным auth_key
    # и отправляем запрос на обновление с некорректным auth_key
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем что статус ответа равен 403
    assert status == 403


def test_unsuccessful_update_self_pet_info_with_invalid_data(name=None, animal_type=None, age=None):
    """Проверяем невозможность обновления информации о питомце с некорректными name, animal_type и age"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если спиок питомцев пустой, то добавляем нового питомца без фото и снова получаем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, str(name), str(animal_type), 1)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Пробуем обновить имя, тип и возраст 1-го питомца из списка своих питомцев
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], type(name), animal_type, age)

    # Проверяем что статус ответа = 400
    assert status == 400


def test_add_new_pet_without_photo_with_invalid_auth_key(name='Мурка', animal_type='киса', age=1):
    """Проверяем, что невозможно добавить питомца с корректными данными без фото с некорректным auth_key"""

    # Приравниваем переменной auth_key заведомо некорректное значение
    auth_key = {'key': valid_email}

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


def test_add_new_pet_without_photo_with_invalid_data(name=None, animal_type=None, age=None):
    """Проверяем, что невозможно добавить питомца с некорректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_update_photo_of_pet_with_invalid_auth_key(pet_photo='images/cat1.jpg'):
    """Проверяем, что невозможно обновить фото существующего питомца с некорректным auth_key"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если спиок питомцев пустой, то добавляем нового питомца без фото и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, 'Барсик', 'котик', 2)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Приравниваем переменной auth_key заведомо некорректное значение
    auth_key = {'key': valid_email}

    # Выполняем запрос на обновление фото 1-го питомца из списка своих питомцев
    status, result = pf.update_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


def test_update_photo_of_pet_with_invalid_pet_photo(pet_photo='images/cat1.txt'):
    """Проверяем, что невозможно обновить фото существующему питомцу некорректным файлом фото"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если спиок питомцев пустой, то добавляем нового питомца без фото и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, 'Барсик', 'котик', 2)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Выполняем запрос на обновление фото 1-го питомца из списка своих питомцев
    status, result = pf.update_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400