import dash
import time
import uuid
import json
from dash import dcc
from dash.dependencies import Input, Output, State, ALL
import feffery_utils_components as fuc

from server import app
from api.log import get_operation_log_list_api, get_operation_log_detail_api, delete_operation_log_api, clear_operation_log_api, export_operation_log_list_api
from api.dict import query_dict_data_list_api


@app.callback(
    [Output('operation_log-list-table', 'data', allow_duplicate=True),
     Output('operation_log-list-table', 'pagination', allow_duplicate=True),
     Output('operation_log-list-table', 'key'),
     Output('operation_log-list-table', 'selectedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('operation_log-search', 'nClicks'),
     Input('operation_log-refresh', 'nClicks'),
     Input('operation_log-list-table', 'pagination'),
     Input('operation_log-operations-store', 'data')],
    [State('operation_log-title-input', 'value'),
     State('operation_log-oper_name-input', 'value'),
     State('operation_log-business_type-select', 'value'),
     State('operation_log-status-select', 'value'),
     State('operation_log-oper_time-range', 'value'),
     State('operation_log-button-perms-container', 'data')],
    prevent_initial_call=True
)
def get_operation_log_table_data(search_click, refresh_click, pagination, operations, title, oper_name, business_type, status_select, oper_time_range, button_perms):

    oper_time_start = None
    oper_time_end = None
    if oper_time_range:
        oper_time_start = oper_time_range[0]
        oper_time_end = oper_time_range[1]
    query_params = dict(
        title=title,
        oper_name=oper_name,
        business_type=business_type,
        status=status_select,
        oper_time_start=oper_time_start,
        oper_time_end=oper_time_end,
        page_num=1,
        page_size=10
    )
    triggered_id = dash.ctx.triggered_id
    if triggered_id == 'operation_log-list-table':
        query_params = dict(
            title=title,
            oper_name=oper_name,
            business_type=business_type,
            status=status_select,
            oper_time_start=oper_time_start,
            oper_time_end=oper_time_end,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if search_click or refresh_click or pagination or operations:
        option_table = []
        info = query_dict_data_list_api(dict_type='sys_oper_type')
        if info.get('code') == 200:
            data = info.get('data')
            option_table = [dict(label=item.get('dict_label'), value=item.get('dict_value'), css_class=item.get('css_class')) for item in data]
        option_dict = {item.get('value'): item for item in option_table}

        table_info = get_operation_log_list_api(query_params)
        if table_info['code'] == 200:
            table_data = table_info['data']['rows']
            table_pagination = dict(
                pageSize=table_info['data']['page_size'],
                current=table_info['data']['page_num'],
                showSizeChanger=True,
                pageSizeOptions=[10, 30, 50, 100],
                showQuickJumper=True,
                total=table_info['data']['total']
            )
            for item in table_data:
                if item['status'] == 0:
                    item['status'] = dict(tag='成功', color='blue')
                else:
                    item['status'] = dict(tag='失败', color='volcano')
                if str(item.get('business_type')) in option_dict.keys():
                    item['business_type'] = dict(
                        tag=option_dict.get(str(item.get('business_type'))).get('label'),
                        color=json.loads(option_dict.get(str(item.get('business_type'))).get('css_class')).get('color')
                    )
                item['key'] = str(item['oper_id'])
                item['cost_time'] = f"{item['cost_time']}毫秒"
                item['operation'] = [
                    {
                        'content': '详情',
                        'type': 'link',
                        'icon': 'antd-eye'
                    } if 'monitor:operlog:query' in button_perms else {},
                ]

            return [table_data, table_pagination, str(uuid.uuid4()), None, {'timestamp': time.time()}]

        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, {'timestamp': time.time()}]

    return [dash.no_update] * 5


app.clientside_callback(
    '''
    (reset_click) => {
        if (reset_click) {
            return [null, null, null, null, null, {'type': 'reset'}]
        }
        return window.dash_clientside.no_update;
    }
    ''',
    [Output('operation_log-title-input', 'value'),
     Output('operation_log-oper_name-input', 'value'),
     Output('operation_log-business_type-select', 'value'),
     Output('operation_log-status-select', 'value'),
     Output('operation_log-oper_time-range', 'value'),
     Output('operation_log-operations-store', 'data')],
    Input('operation_log-reset', 'nClicks'),
    prevent_initial_call=True
)


app.clientside_callback(
    '''
    (hidden_click, hidden_status) => {
        if (hidden_click) {
            return [
                !hidden_status,
                hidden_status ? '隐藏搜索' : '显示搜索'
            ]
        }
        return window.dash_clientside.no_update;
    }
    ''',
    [Output('operation_log-search-form-container', 'hidden'),
     Output('operation_log-hidden-tooltip', 'title')],
    Input('operation_log-hidden', 'nClicks'),
    State('operation_log-search-form-container', 'hidden'),
    prevent_initial_call=True
)


@app.callback(
    [Output('operation_log-modal', 'visible', allow_duplicate=True),
     Output('operation_log-modal', 'title'),
     Output('operation_log-title-text', 'children'),
     Output('operation_log-oper_url-text', 'children'),
     Output('operation_log-login_info-text', 'children'),
     Output('operation_log-request_method-text', 'children'),
     Output('operation_log-method-text', 'children'),
     Output('operation_log-oper_param-text', 'children'),
     Output('operation_log-json_result-text', 'children'),
     Output('operation_log-status-text', 'children'),
     Output('operation_log-cost_time-text', 'children'),
     Output('operation_log-oper_time-text', 'children'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    Input('operation_log-list-table', 'nClicksButton'),
    [State('operation_log-list-table', 'clickedContent'),
     State('operation_log-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def add_edit_operation_log_modal(button_click, clicked_content, recently_button_clicked_row):
    if button_click:
        oper_id = int(recently_button_clicked_row['key'])
        operation_log_info_res = get_operation_log_detail_api(oper_id=oper_id)
        if operation_log_info_res['code'] == 200:
            operation_log_info = operation_log_info_res['data']
            oper_name = operation_log_info.get('oper_name') if operation_log_info.get('oper_name') else ''
            oper_ip = operation_log_info.get('oper_ip') if operation_log_info.get('oper_ip') else ''
            oper_location = operation_log_info.get('oper_location') if operation_log_info.get('oper_location') else ''
            login_info = f'{oper_name} / {oper_ip} / {oper_location}'
            return [
                True,
                '操作日志详情',
                operation_log_info.get('title'),
                operation_log_info.get('oper_url'),
                login_info,
                operation_log_info.get('request_method'),
                operation_log_info.get('method'),
                operation_log_info.get('oper_param'),
                operation_log_info.get('json_result'),
                '正常' if operation_log_info.get('status') == 0 else '失败',
                f"{operation_log_info.get('cost_time')}毫秒",
                operation_log_info.get('oper_time'),
                {'timestamp': time.time()},
            ]

        return [dash.no_update] * 12 + [{'timestamp': time.time()}]

    return [dash.no_update] * 13


@app.callback(
    Output({'type': 'operation_log-operation-button', 'index': 'delete'}, 'disabled'),
    Input('operation_log-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_operation_log_delete_button_status(table_rows_selected):
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:
            if len(table_rows_selected) > 1:
                return False

            return False

        return True

    return dash.no_update


@app.callback(
    [Output('operation_log-delete-text', 'children'),
     Output('operation_log-delete-confirm-modal', 'visible'),
     Output('operation_log-delete-ids-store', 'data')],
    Input({'type': 'operation_log-operation-button', 'index': ALL}, 'nClicks'),
    State('operation_log-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def operation_log_delete_modal(operation_click, selected_row_keys):
    trigger_id = dash.ctx.triggered_id
    if trigger_id.index in ['delete', 'clear']:
        if trigger_id.index == 'delete':
            oper_ids = ','.join(selected_row_keys)

            return [
                f'是否确认删除日志编号为{oper_ids}的操作日志？',
                True,
                {'oper_type': 'delete', 'oper_ids': oper_ids}
            ]

        elif trigger_id.index == 'clear':
            return [
                f'是否确认清除所有的操作日志？',
                True,
                {'oper_type': 'clear', 'oper_ids': ''}
            ]

    return [dash.no_update] * 3


@app.callback(
    [Output('operation_log-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('operation_log-delete-confirm-modal', 'okCounts'),
    State('operation_log-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def operation_log_delete_confirm(delete_confirm, oper_ids_data):
    if delete_confirm:

        oper_type = oper_ids_data.get('oper_type')
        if oper_type == 'clear':
            params = dict(oper_type=oper_ids_data.get('oper_type'))
            clear_button_info = clear_operation_log_api(params)
            if clear_button_info['code'] == 200:
                return [
                    {'type': 'delete'},
                    {'timestamp': time.time()},
                    fuc.FefferyFancyMessage('清除成功', type='success')
                ]

            return [
                dash.no_update,
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('清除失败', type='error')
            ]
        else:
            params = dict(oper_ids=oper_ids_data.get('oper_ids'))
            delete_button_info = delete_operation_log_api(params)
            if delete_button_info['code'] == 200:
                return [
                    {'type': 'delete'},
                    {'timestamp': time.time()},
                    fuc.FefferyFancyMessage('删除成功', type='success')
                ]

            return [
                dash.no_update,
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('删除失败', type='error')
            ]

    return [dash.no_update] * 3


@app.callback(
    [Output('operation_log-export-container', 'data', allow_duplicate=True),
     Output('operation_log-export-complete-judge-container', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('operation_log-export', 'nClicks'),
    prevent_initial_call=True
)
def export_operation_log_list(export_click):
    if export_click:
        export_operation_log_res = export_operation_log_list_api({})
        if export_operation_log_res.status_code == 200:
            export_operation_log = export_operation_log_res.content

            return [
                dcc.send_bytes(export_operation_log, f'操作日志信息_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx'),
                {'timestamp': time.time()},
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('导出成功', type='success')
            ]

        return [
            dash.no_update,
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('导出失败', type='error')
        ]

    return [dash.no_update] * 4


@app.callback(
    Output('operation_log-export-container', 'data', allow_duplicate=True),
    Input('operation_log-export-complete-judge-container', 'data'),
    prevent_initial_call=True
)
def reset_operation_log_export_status(data):
    time.sleep(0.5)
    if data:

        return None

    return dash.no_update
