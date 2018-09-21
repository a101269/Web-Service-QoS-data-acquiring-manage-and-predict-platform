"""wbqossite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from basepages import views as basepages
from get_qos import views as get_qos
from ws import views as ws



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^accounts/',include('users.urls')),
    url(r'^accounts/profile/',basepages.accounts_profile),
    url(r'^webservice/addurl/',get_qos.webservice_addurl),
    url(r'^webservice/url/', get_qos.webservice_url),
    url(r'^webservice/qos/gather', get_qos.webservice_qos_gather),
    url(r'^webservice/qos/collect/form/', get_qos.collect_form),
    url(r'^webservice/qos/collect/result/',get_qos.collect_result),
    url(r'^webservice/qos/collect/result2/', get_qos.collect_result2),
    url(r'^webservice/qos/attributes/choose/',get_qos.attributes_choose),
    url(r'^webservice/qos/attributes/setting/',get_qos.attributes_setting),
    url(r'^webservice/qos/monitor/setting/', get_qos.monitor_setting),
    url(r'^webservice/monitor/list/', get_qos.monitor_list),
    url(r'^webservice/monitor/addel/', get_qos.monitor_addel),
    url(r'^webservice/monitoring/', get_qos.monitoring),
    url(r'^examplebase/manage/', get_qos.epbase_manage),
    url(r'^predict/', get_qos.predict),
    url(r'^qos/predict/input/', get_qos.predict_input),
    url(r'^qos/predict/result/', get_qos.predict_result),
    url(r'^qosresponse', get_qos.monitoring_response),
    url(r'^collectresponse/', get_qos.collect_response),
    url(r'^timeinternalresponse/', get_qos.timeinternal_response),
    url(r'^webservice/t', get_qos.t),
    url(r'^home/', ws.home),
    url(r'^$',basepages.basepage),
    # url(r'^getqos', include('get_qos.urls', namespace="get_qos")),
    url(r'^announcement/release/', get_qos.announcement_release),
    url(r'^announcement/save/', get_qos.announcement_save),
    # url(r'^announcement/list/', get_qos.announcement_list),
    url(r'^announcement/list/(\d+)/$',get_qos.announcement_list),
    url(r'^announcement/content/(\d+)/$', get_qos.announcement_content,name='announcement_content'),
    url(r'^webservice/info/save/', ws.info_save),
    url(r'^webservice/manage/register/', ws.ws_register),
    url(r'^webservice/collection/del/', ws.collection_del),
    url(r'^webservice/collection/add/', ws.collection_add),
    url(r'^webservice/moin/add/', ws.moni_add),
    url(r'^webservice/collection/list/(\d+)/$', ws.collection_list),
    url(r'^webservice/search/', ws.search),
    # url(r'^webservice/dosearch/', ws.dosearch),
    url(r'^webservice/dosearch/(\d+)/$',ws.dosearch),
    url(r'^search/result/(\d+)/$', ws.ws_info, name='ws_info'),
    url(r'^recommand/response/$', ws.recommand_response),
    url(r'^webservice/recommand/page/$', ws.recommand_page),
    url(r'^down/', get_qos.down),
    url(r'^output/', get_qos.output)
]

