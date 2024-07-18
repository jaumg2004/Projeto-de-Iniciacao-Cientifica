from abc import ABC, abstractmethod

class CenárioBase(ABC):
    def __init__(self, media, variancia, ntestes):
        self.media = media
        self.variancia = variancia
        self.ntestes = ntestes

    @abstractmethod
    def cenario(self):
        pass

    @abstractmethod
    def calculaY(self):
        pass