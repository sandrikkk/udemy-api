def wrapper(n):
    def inner(a, b):
        print("here")

        return n(a, b)

    return inner


@wrapper
def sums(a, b):
    return a + b


print(sums(4, 5))
