import random

def random_string(length):
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(letters) for i in range(length))

class FileUpload:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def save(self):
        with open(f'./uploads/{self.name}', 'wb') as f:
            f.write(self.content)