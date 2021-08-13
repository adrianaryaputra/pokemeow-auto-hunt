from datetime import datetime

def dateprint(msg):
    print(f"""[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}""")

def dateinput(msg):
    return input(f"""[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}""")