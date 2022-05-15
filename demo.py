# def outer(fn):
#     def inner(*args):
#         print(args)
#         request.get('username')
#         print('我执行了')
#         fn()
#
#         return
#
#     return inner
#
#
# request = {'username': 'zhang'}
#
#
# @outer
# def main(request):
#     print(1)
#
#
# @outer
# def a():
#     pass
#
#
# # main = outer(main)
# # a = outer(a)
#
# b = main
import os
import sys

# print(sys.argv)

print(os.path.basename("demo.py"))

