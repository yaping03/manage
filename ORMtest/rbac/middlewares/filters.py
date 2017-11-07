import re

from django.shortcuts import render,redirect,HttpResponse
from django.conf import settings


class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

class MyFilter(MiddlewareMixin):
    def process_request(self,req):
        url_list = req.session.get('url_list')
        url = req.path_info
        allow_url = settings.ALLOW_URL
        print(url_list)
        for u in allow_url:
            if re.match(u,url):
                return None
        flag = False
        if not url_list:
            return redirect("/login")
        for u in url_list:
            res = "^{0}$".format(u)
            print(res,url)
            if re.match(res, url):
                flag = True
                print("yes")
                return None
        if not flag:
            return HttpResponse("您访问的页面不存在或无权访问")
