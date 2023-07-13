from utils.request import api_request


def get_dict_type_list_api(page_obj: dict):

    return api_request(method='post', url='/system/dictType/get', is_headers=True, json=page_obj)


def add_dict_type_api(page_obj: dict):

    return api_request(method='post', url='/system/dictType/add', is_headers=True, json=page_obj)


def edit_dict_type_api(page_obj: dict):

    return api_request(method='patch', url='/system/dictType/edit', is_headers=True, json=page_obj)


def delete_dict_type_api(page_obj: dict):

    return api_request(method='post', url='/system/dictType/delete', is_headers=True, json=page_obj)


def get_dict_type_detail_api(dict_id: int):

    return api_request(method='get', url=f'/system/dictType/{dict_id}', is_headers=True)


def get_dict_data_list_api(page_obj: dict):

    return api_request(method='post', url='/system/dictData/get', is_headers=True, json=page_obj)


def add_dict_data_api(page_obj: dict):

    return api_request(method='post', url='/system/dictData/add', is_headers=True, json=page_obj)


def edit_dict_data_api(page_obj: dict):

    return api_request(method='patch', url='/system/dictData/edit', is_headers=True, json=page_obj)


def delete_dict_data_api(page_obj: dict):

    return api_request(method='post', url='/system/dictData/delete', is_headers=True, json=page_obj)


def get_dict_data_detail_api(dict_id: int):

    return api_request(method='get', url=f'/system/dictData/{dict_id}', is_headers=True)