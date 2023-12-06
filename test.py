def a_new_decorator(name):
    def wrapper_fn(func):
        print('执行前，随便打印点什么')
        func(name)
        print('执行后，随便打印点什么')

    return wrapper_fn


@a_new_decorator(name='xxx')
def deco(n):
    print('测试装饰器')
    print(f'n是{n}')

