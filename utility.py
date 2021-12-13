import pandas as pd
def get_tottime(csv_file_path):
    df = pd.read_csv(csv_file_path)
    
    arr = list(
    df[df['filename:lineno(function)'].isin([
        '{built-in method _hashlib.pbkdf2_hmac}',
        '{built-in method _socket.getaddrinfo}',
        '{built-in method _ssl.enum_certificates}',
        '{built-in method select.select}',
        "{method 'acquire' of '_thread.lock' objects}",
        "{method 'connect' of '_socket.socket' objects}",
        "{method 'do_handshake' of '_ssl._SSLSocket' objects}",
        "{method 'load_verify_locations' of '_ssl._SSLContext' objects}",
        "{method 'read' of '_ssl._SSLSocket' objects}",
        "{method 'write' of '_ssl._SSLSocket' objects}"
    ])]['tottime']
    )
    
    return arr

def get_function_name():
    return [
        '{built-in method _hashlib.pbkdf2_hmac}',
        '{built-in method _socket.getaddrinfo}',
        '{built-in method _ssl.enum_certificates}',
        '{built-in method select.select}',
        "{method 'acquire' of '_thread.lock' objects}",
        "{method 'connect' of '_socket.socket' objects}",
        "{method 'do_handshake' of '_ssl._SSLSocket' objects}",
        "{method 'load_verify_locations' of '_ssl._SSLContext' objects}",
        "{method 'read' of '_ssl._SSLSocket' objects}",
        "{method 'write' of '_ssl._SSLSocket' objects}"
    ]

