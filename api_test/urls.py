from django.conf.urls import url

from api_test.api import ApiDoc, automationCase as case
from api_test.api.global_parameter import host_total, add_host, update_host, del_host, enable_host, disable_host
from api_test.api.projectList import project_list, add_project, update_project, del_project, disable_project, \
     enable_project
from api_test.api.projectTitle import project_info, api_total, dynamic_total, project_member

urlpatterns = [
    url(r'project/project_list', project_list),
    url(r'project/add_project', add_project),
    url(r'project/update_project', update_project),
    url(r'project/del_project', del_project),
    url(r'project/disable_project', disable_project),
    url(r'project/enable_project', enable_project),
    url(r'title/project_info', project_info),
    url(r'title/api_total', api_total),
    url(r'title/dynamic_total', dynamic_total),
    url(r'title/project_member', project_member),
    url(r'global/host_total', host_total),
    url(r'global/add_host', add_host),
    url(r'global/update_host', update_host),
    url(r'global/del_host', del_host),
    url(r'global/disable_host', disable_host),
    url(r'global/enable_host', enable_host),
    url(r'api/group', ApiDoc.group),
    url(r'api/add_group', ApiDoc.add_group),
    url(r'api/update_group', ApiDoc.update_group),
    url(r'api/del_group', ApiDoc.del_group),
    url(r'api/api_list', ApiDoc.api_list),
    url(r'api/add_api', ApiDoc.add_api),
    url(r'api/update_api', ApiDoc.update_api),
    url(r'api/select_api', ApiDoc.select_api),
    url(r'api/del_api', ApiDoc.del_api),
    url(r'api/update_api_group', ApiDoc.update_api_group),
    url(r'api/api_info', ApiDoc.api_info),
    url(r'api/add_history', ApiDoc.add_history),
    url(r'api/del_history', ApiDoc.del_history),
    url(r'automation/group', case.group),
    url(r'automation/add_group', case.add_group),
    url(r'automation/del_group', case.del_group),
    url(r'automation/update_group', case.update_group),
    url(r'automation/update_case_group', case.update_case_group),
    url(r'automation/case_list', case.case_list),
    url(r'automation/add_case', case.add_case),
    url(r'automation/update_case', case.update_case),
    url(r'automation/del_case', case.del_case),
    url(r'automation/api_list', case.api_list),
]