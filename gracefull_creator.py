import json
import os

from decoration import Decoration
from google_cloud_connector import google_cloud_connection

from CONSTAINS import BUCKET_NAME

class ConfigFiles:
    def __init__(self):
        ...
    
    @classmethod
    def gracefull_create(self):
        
        self.obj = {
            "type": "service_account",
            "project_id": "graceful-byway-385815",
            "client_email": "creative-houre-servise-account@graceful-byway-385815.iam.gserviceaccount.com",
            "client_id": "112172202864725306768",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/creative-houre-servise-account%40graceful-byway-385815.iam.gserviceaccount.com"
                }
        self.__privat_key = os.getenv("private_key")
        self.obj["private_key_id"] = os.getenv("private_key_id")
        self.obj["private_key"] = F"-----BEGIN PRIVATE KEY-----\n{self.__privat_key}\nwP1ZCtku09M97RHSX293mYJRfDEuh3SQYZptDjQth+DpsX52TiUqbYsDKpy5iVUi\n5X0JxeN1o6ELHAQT7Cw1Oh8ll10O5OVKkwL/x34HpxUTHgx+89aJMlrD5wgX3yfj\nwqetbEk0iH/lwIPdCwpKZ5ypnL0F+ZoVjsq6LJYR293yEjSKQF3itMR5E1MZeET0\njWd6G7qr0G4ZTJ9+AEHba30bh782QD3afHJeqa6ys7NNKccBpBf1rrWIOodo5y0h\n2j3LkbRaW9GLIvrQ62/Tv3FCVEsLF3HUTIpv6QEcs4j0PhQMpQIVh3XlW2PuLKjs\nRNb1VegHAgMBAAECggEAA/I9N+HVRKmHvo9hpKBFo7jDs77SFkqpkeFHW7l1wYiT\nf/k+bqWVbIW0q91srr+Rq9NX0fHtmp+owIYexAMZ7sxZG7ZjFXzByXmYIMhwBA9O\ncA3+vvcMM2wtv+whyGTd0dNqhnKQnGPU549pfLrifplzr6YC/G+wu51mwrDUF4aE\nteux17t77vZcsWwzsURSsoIXRSl5JmR/veG+zwASeORnNr9K5TXMg6LIsMR6t4oL\n0Vr0vQXJrRF+GPVmOmtgoA6gWeQsVP+kkQN8g2ITiDRfZj2DxwS8nsUIjpNFEEjV\nZzI3fc8YKaKKvkxugkshegHq8usEejROgh92PvTnXQKBgQDxuSptqIFvg0mNfHKi\nyM4cGrBk5WJVZ3KtDS3qbppq9R68NEV8CqJR3eoAMGpJcA2IK9iYvILV+MYUGEP8\nm4oP14V6B2Qc3jv9cGuxWSjwQFSbCvV+vLVmxoL7lNVDzkBRZsG04Eux2ktMT3Z3\n5G72QxbNj5+bmRXdalaMRbLC/QKBgQDjJVr3ZGWNJSwF2IrqkzJco0xtCiyySUFB\nxSjsBsDv1PAo5JoXa29nmbtOYMzTAYQNK9b1oFd08JhrIeW3MEvXnvBtCVeW6VxE\nZQcLyN4dqygG2bde4WWz8/CQOknsZ8hL6HB4EnrjL0rAupwO7cxwkKYqr/f9/117\nRcj9bPpwUwKBgBoGZZsI2Wa4K+Mf0vfTxt0fwn4adEvdp2saUCc9YULCwVxiBFkm\ni/NkgR0kGU1u0wYmMlu/cBa5ghoHwsoftO2ftq88vHqfMrZGtFGT1+SGCJXoyCWt\nC5rVJKURkSSLwEEDXzeqLnwnlJPSul6OKaQ59OqM3BJUmRYNrOPNXUHBAoGBAJOr\nP15CCLsgBWSviHBDzaPoDdF9od0uPpxxfs8i/N9uQct0ArFjCQQDL4Ae8knjXGPr\nsk3xNaoymARd/yd+4G+HRqq8PhNAFtnoDBKfPbdwBA+gDtRCGIpK9oPtQQ3N0qt2\nq1eEPBviLOjq6HXUJuqvPzfVOpYIJE/16FrJNG89AoGAK7+6RCsY9T4nURC/3OSt\nUYkjXC3NjdXAXbc16Wo8Nr8eAfPLp6uD6C69LnLzfSxB2BqqbMrP4ndyNhMfvSpB\nke6dPfr0WTOnIXKhz30YbkMVMTdBH8pFzIL+y1Bwt1/IHlks9JwQiuJHJe5rI9Lt\nmQXgt89img6yoH0+msmxt9w=\n-----END PRIVATE KEY-----\n",
        with open("gracefull_obj.json", "w") as f:
            json.dump(self.obj, f)
        return self.obj
            
    @classmethod
    def constants_create(self):
        try:
            google_cloud_connection(file_config="gracefull_obj.json",
                                    file_name="CONSTANT.json",
                                    bucket_name=BUCKET_NAME)
        except Exception as e:
            Decoration._write_logs(e)
            
if __name__ == "__main__":
    ConfigFiles.gracefull_create()
