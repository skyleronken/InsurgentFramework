#!/usr/bin/env python

class Translator:
    
    def __init__(self, xml):
        self.xml = xml
        decoders = self.parse_decoders(xml)
        encoders = self.parse_encoders(xml)
        if encoders is None:
            encoders = reversed(decoders)

    def parse_encoders(self,xml):
        pass
    
    def parse_decoders(self,xml):
        pass
    
    def import_codecs(self):
        pass
    
    def map_codecs(self):
        pass

    def decode(self):
        pass

    def encode(self):
        pass