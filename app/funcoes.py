from datetime import date, timedelta

def funcao_data(i):
    array = []
    dt = date.today()
    array.append(dt)
    while i > 0:
        prev = dt.replace(day=1) - timedelta(days=1)
        dt = prev        
        array.append(prev)
        i = i - 1
    return array