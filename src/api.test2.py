def f():
    # generator function
    l = [1, 2, 3, 4]
    for i in l:
        yield i
    return
    print("After yielding {}".format(i))

g = f()
for i in g:
    print(i)