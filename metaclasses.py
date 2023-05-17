import dis


class ServerMaker(type):
    def __init__(self, name, bases, dct):
        methods = []
        attributes = []
        for func in dct:
            try:
                gen = dis.get_instructions(dct[func])
            except TypeError:
                pass
            else:
                for i in gen:
                    if i.opname == "LOAD_GLOBAL":
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == "LOAD_ATTR":
                        if i.argval not in attributes:
                            attributes.append(i.argval)
        print(methods)
        if "connect" in methods:
            raise TypeError("Использование метода connect недопустимо")
        if not ("SOCK_STREAM" in attributes and "AF_INET" in attributes):
            raise TypeError("Некорректная инициализация сокета.")
        super().__init__(name, bases, dct)


class ClientMaker(type):
    def __init__(self, name, bases, dct):
        methods = []
        for func in dct:
            try:
                ret = dis.get_instructions(dct[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == "LOAD_GLOBAL":
                        if i.argval not in methods:
                            methods.append(i.argval)
        for command in ("accept", "listen", "socket"):
            if command in methods:
                raise TypeError("В классе обнаружено использование запрещённого метода")
        if "get_message" in methods or "send_message" in methods:
            pass
        else:
            raise TypeError("Отсутствуют вызовы функций, работающих с сокетами.")
        super().__init__(name, bases, dct)
