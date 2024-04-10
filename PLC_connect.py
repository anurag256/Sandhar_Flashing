class PLC_reg:
    def __init__(self):
        self.load_config()

    def load_config(self):    
        try:
            with open("config.txt", "r") as f:
                data = f.read().split(",")
                self._host = data[0]
                self._port = data[1]
        except FileNotFoundError:
            # If config file doesn't exist, use default values
            self._host = '192.168.250.1'
            self._port = '1200'