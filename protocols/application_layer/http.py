class http:
    '''
    Http Header:
    -   Init
    -   Host
    -   Authorization: the almost standart oauth2 token
    -   Content-Type
    -   Content-Length
    '''
    def __init__(self, pdu, auth):
        self.init = len('POST / HTTP/1.0')
        self.host = 4
        self.authorization = 0
        if auth:
            self.authorization = len('Bearer ') + 27
        self.content_type = len('application/json')
        self.content_length = len(str(oct(pdu)))
        self.pdu = pdu

    def get_cost(self):
        return self.init + self.host + self.authorization + self.content_type + self.content_length + self.pdu
