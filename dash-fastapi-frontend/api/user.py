from utils.request import api_request


def forget_user_pwd_api(page_obj: dict):

    return api_request(method='post', url='/login/forgetPwd', is_headers=False, json=page_obj)


def get_user_list_api(page_obj: dict):

    return api_request(method='post', url='/system/user/get', is_headers=True, json=page_obj)


def add_user_api(page_obj: dict):

    return api_request(method='post', url='/system/user/add', is_headers=True, json=page_obj)


def edit_user_api(page_obj: dict):

    return api_request(method='patch', url='/system/user/edit', is_headers=True, json=page_obj)


def delete_user_api(page_obj: dict):

    return api_request(method='post', url='/system/user/delete', is_headers=True, json=page_obj)


def get_user_detail_api(user_id: int):

    return api_request(method='get', url=f'/system/user/{user_id}', is_headers=True)


def change_user_avatar_api(page_obj: dict):

    return api_request(method='patch', url='/system/user/profile/changeAvatar', is_headers=True, json=page_obj)


def change_user_info_api(page_obj: dict):

    return api_request(method='patch', url='/system/user/profile/changeInfo', is_headers=True, json=page_obj)


def reset_user_password_api(page_obj: dict):

    return api_request(method='patch', url='/system/user/profile/resetPwd', is_headers=True, json=page_obj)


def batch_import_user_api(page_obj: dict):

    return api_request(method='post', url='/system/user/importData', is_headers=True, json=page_obj)


def download_user_import_template_api():

    return api_request(method='post', url='/system/user/importTemplate', is_headers=True, stream=True)


def export_user_list_api(page_obj: dict):

    return api_request(method='post', url='/system/user/export', is_headers=True, json=page_obj, stream=True)


def get_allocated_role_list_api(page_obj: dict):

    return api_request(method='post', url='/system/user/authRole/allocatedList', is_headers=True, json=page_obj)


def get_unallocated_role_list_api(page_obj: dict):

    return api_request(method='post', url='/system/user/authRole/unallocatedList', is_headers=True, json=page_obj)


def auth_role_select_all_api(page_obj: dict):

    return api_request(method='post', url='/system/user/authRole/selectAll', is_headers=True, json=page_obj)


def auth_role_cancel_api(page_obj: dict):

    return api_request(method='post', url='/system/user/authRole/cancel', is_headers=True, json=page_obj)


