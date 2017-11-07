
def session_handle(req,obj):
        url_list = []
        url_dict = obj.roles.all().values("permissions__url").distinct()
        user = obj.username
        for url in url_dict:
            url_list.append(url["permissions__url"])
        req.session["url_list"] = url_list
        req.session["user"] = user
