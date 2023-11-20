# MuberApp
MuberApp is a basic implementation of uber app


## Muber app is platform that lets registered passengers to add like/dislike to registered drivers.


##To interact with the API, utilize following endpoints:

```
""                        supports [get] method/s                     authentication_classes = [], permission_classes=[]
"passengers/register/"    supports [post] method/s                    authentication_classes = [], permission_classes=[]
"passengers/login/"       supports [post] method/s                    authentication_classes = [], permission_classes=[]
"passengers/detail/"      supports [get, patch] method/s              authentication_classes = [JSONWebTokenAuthentication], permission_classes=[]
"passengers/drivers/"     supports [get] method/s                     authentication_classes = [JSONWebTokenAuthentication], permission_classes=[]
"passengers/like/"        supports [post] method/s                    authentication_classes = [JSONWebTokenAuthentication], permission_classes=[IsPremiumPassenger]
"drivers/register/"       supports [post] method/s                    authentication_classes = [], permission_classes=[]
"drivers/login/"          supports [post] method/s                    authentication_classes = [],  permission_classes = []
"drivers/detail/"         supports [get,patch] method/s               authentication_classes = [JSONWebTokenAuthentication], permission_classes=[]


```



