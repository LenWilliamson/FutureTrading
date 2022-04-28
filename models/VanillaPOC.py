def f(input):
    for entry in input:
        try:
            print(f'entry={entry}')
            r = 1/int(entry)
        except TypeError as te:
            print(f'TypeError: {te}')
        except ValueError as ve:
            print(f'ValueError: {ve}')
        except ZeroDivisionError as zde:
            print(f'ZeroDivisionError: {zde}')
        except Exception as e:
            print(e)
    print(f'The reciprocal of r is {r}')

def g(input):
    for entry in input:
        raise ValueError("A")
        if entry == 0:
            raise ValueError(f'Input {entry} equals 0. Divison by zero not possible!')
            continue
        if isinstance('s', str):
            raise ValueError(f'Input {entry} is string. Divison by string not possible!')
            continue
        r = 1/int(entry)
    print(f'The reciprocal of r is {r}')

#f(['a', 0, 2])

try:
    g(['a', 0, 2])
except ValueError as ve:
    print(ve)