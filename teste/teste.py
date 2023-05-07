my_list = [None, None, None, None, None, None]
print(next((x for x in my_list if x is not None), None))
