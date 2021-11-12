class AuthUser:
    def __init__(self, client, master):
        self.client = client
        self.master = master
        self.refresh = ""
        self.access = ""

    def check_token(self, callback=None):
        response = self.client.user.refresh(data={"refresh": self.refresh})

        if response.status_code == 200:
            self.access = response.json()['access']
            return True

        if callback:
            callback()

        return False

    def login(self, username, password):
        data = {"username": username, "password": password}

        response = self.client.user.login(data=data)

        if response.status_code == 200:
            data = response.json()
            self.refresh = data['refresh']
            self.access = data['access']

            return True

        return False
