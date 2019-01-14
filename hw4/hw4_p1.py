# import module
import turtle as t


# a function that draws regular n-gons
# INPUT: n
def ngon(n):
    tt = t.Turtle()  # I found this line is necessary to use fd and rt without warning
    side_length = 30
    angle = 360 / n
    for i in range(n):
        tt.fd(side_length)
        tt.rt(angle)

    t.done()
    t.bye()  # the function works with t.bye()
    return


# ngon(7)  # a function call to test my function

