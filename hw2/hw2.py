import math


def solve(f, x0, e):
    x0 = float(x0)  # cast to float type to avoid loss of accuracy due to integer division
    func = f(x0)
    delta = abs(func[0])
    counter = 0
    while delta > e:
        x0 = x0 - func[0] / func[1]
        func = f(x0)
        delta = abs(func[0])
        counter += 1

    # print (counter)   this line is to print the number of iterations
    return x0


# the following print functions are used to test "solve" function with the arguments provided by the professor
'''print solve(lambda x: [x**2-1, 2*x], 3, 0.0001)
print solve(lambda x: [x**2-1, 2*x], -1, 0.0001)
print solve(lambda x: [math.exp(x)-1, math.exp(x)], 1, 0.0001)
print solve(lambda x: [math.sin(x), math.cos(x)], 0.5, 0.0001)'''

# the output for the above tests are:
# f(x) = x^2 - 1, f'(x) = 2x, x0 = 3: 1.00003051804
# f(x) = x^2 - 1, f'(x) = 2x, x0 = -1: -1.0
# f(x) = exp(x) - 1, f'(x) = exp(x), x0 = 1: 1.5641107899e-06
# f(x) = sin(x), f'(x) = cos(x), x0 = 0.5: 3.31180213264e-05

# then we use calculator to test if the solutions provided are correct.
# It shows that these solutions are correct


# Finally, we test the function with different values of tolerance to find a pattern.
# For the function f(x) = x^2 - 1 with x0 = 3:
#       tolerance 1e-03 : 4 iterations
#       tolerance 1e-04 : 4 iterations
#       tolerance 1e-05 : 5 iterations
#       tolerance 1e-06 : 5 iterations
#       tolerance 1e-07 : 5 iterations
# For the function f(x) = exp(x) - 1 with x0 = 1:
#       tolerance 1e-03 : 4 iterations
#       tolerance 1e-04 : 4 iterations
#       tolerance 1e-05 : 4 iterations
#       tolerance 1e-06 : 5 iterations
#       tolerance 1e-07 : 5 iterations
# For the function f(x) = sin(x) with x0 = 0.5:
#       tolerance 1e-03 : 2 iterations
#       tolerance 1e-04 : 2 iterations
#       tolerance 1e-05 : 3 iterations
#       tolerance 1e-06 : 3 iterations
#       tolerance 1e-07 : 3 iterations
# Note: For the function f(x) = x^2 - 1 with x0 = -1, the number of iteration is zero regardless of tolerance.

# As we can see, if the value of tolerance becomes smaller, then the number of iterations is likely to increase.
# This is because we need more iterations to make |f(x)| smaller than the value of tolerance, which means more accuracy.
# Also, the number of iterations tend to converge because our solution will be closer and closer to the exact solution.
# The Newton's method perhaps will achieve quadratic convergence. Here is a simple mathematics proof:
# Using Taylor's theorem to write the f(x):
# f(a) = f(xn) + f'(xn)(a-xn) + (f''(b)/2)(a-xn)^2 where b is in the interval (xn, a)
# then xn - f(xn)/f'(xn) - a = (f''(b)/2f'(xn))(xn-a)^2
# using the next term in the newton method, the equation becomes:
# x[n+1] - a = (f''(b)/2f'(xn))(xn - 1)^2
# Take the absolute values of both sides
# let the values of tolerance in the n+1th term be TOL1 = |x[n+1] - a|
# let the values of tolerance in the nth term be TOL2 = |xn - a|
# Then we have TOL1 = C*TOL2^2  Q.E.D
# Therefore the number of iterations may achieve quadratic convergence.
# And there will be an increase in the number of iterations as the values of tolerance become smaller.
