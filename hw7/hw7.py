# Furuya Rei
# import module
import sympy as sp
import numpy as np
from numpy import linalg
import re
from sympy.parsing.sympy_parser import parse_expr

# calculate the Pearson correlation coefficient
def corrcoeff(x, y):
    n = float(len(x))
    x_deviation = x.copy()
    x_deviation = x_deviation.astype(float)  # cast to float type
    x_mean = np.sum(x) / n  # get the mean of x
    y_deviation = y.copy()
    y_deviation = y_deviation.astype(float)  # cast to float type
    y_mean = np.sum(y) / n  # get the mean of y
    for i in range(len(y)):
        x_deviation[i] = x[i] - x_mean  # set the deviation vector x
        y_deviation[i] = y[i] - y_mean  # set the deviation vector y

    # compute the returned coefficient according to the formula
    corr_coeff = np.dot(x_deviation, y_deviation) / float(linalg.norm(x_deviation, 2) * linalg.norm(y_deviation, 2))
    return corr_coeff


#x = np.array([3,4,6,1,2,3])
#y = np.array([2,3,1,4,1,2])
#print (corrcoeff(x, y))


# calculate the probability that a standard normal random variable falls in the interval between a and b
def normalcurve(a, b):
    x = sp.symbols('x')
    std_pdf = (1 / (sp.sqrt(2 * sp.pi))) * (sp.exp(-(x**2) / 2))  # calculate the probability density function
    precise = sp.integrate(std_pdf, (x, a, b))  # integrate the pdf using symbols
    numerical = sp.integrate(std_pdf, (x, a, b)).evalf()  # evaluate the value of the integral
    return precise, numerical


#print (normalcurve(0,1))


# this is a helper function to get the matrix we need to solve the linear equation system
def getmatrix(s):
    # split left side and right side
    left = re.split("=", s)[0]
    right = re.split("=", s)[1]

    # get the compounds for both sides, respectively
    l_chem = re.split('\s*\+\s*', left)
    r_chem = re.split('\s*\+\s*', right)

    n_chem = len(l_chem) + len(r_chem)

    elements = []
    l_list = []
    r_list = []

    for l_ele in l_chem:
        # a list of tuples which are forms of (element, number) for each compound in the left hand side
        help_list = re.findall(r'([A-Z][a-z]{0,1})(\d*)', l_ele)
        l_list.append(help_list)
        for ele in help_list:
            if ele[0] not in elements:
                elements.append(ele[0])

    for r_ele in r_chem:
        # a list of tuples which are forms of (element, number) for each compound in the right hand side
        help_list = re.findall(r'([A-Z][a-z]{0,1})(\d*)', r_ele)
        r_list.append(help_list)

    # print elements
    # print l_list
    # print r_list

    n_ele = len(elements)

    # initialize our matrix with zero
    our_matrix = sp.zeros(n_ele, n_chem + 1)
    m = 0

    for l_item in l_list:
        for l_tuple in l_item:
            if l_tuple[1] == '':
                a = 1
            else:
                a = int(l_tuple[1])
            row_m = elements.index(l_tuple[0])
            our_matrix[row_m, m] = our_matrix[row_m, m] + a
        m += 1

    for r_item in r_list:
        for r_tuple in r_item:
            if r_tuple[1] == '':
                a = 1
            else:
                a = int(r_tuple[1])
            row_m = elements.index(r_tuple[0])
            our_matrix[row_m, m] = our_matrix[row_m, m] - a
        m += 1

    return our_matrix


# this is the function we use to balance the chemical equation
def balance(eq):
    M = getmatrix(eq)
    left = re.split("=", eq)[0]
    right = re.split("=", eq)[1]

    # get the compounds for both sides, respectively
    l_chem = re.split('\s*\+\s*', left)
    r_chem = re.split('\s*\+\s*', right)
    # print l_chem
    # print r_chem

    elements = []

    for l_ele in l_chem:
        # a list of tuples which are forms of (element, number) for each compound in the left hand side
        help_list = re.findall(r'([A-Z][a-z]{0,1})(\d*)', l_ele)
        for ele in help_list:
            if ele[0] not in elements:
                elements.append(ele[0])

    n = len(l_chem) + len(r_chem)
    # print n
    x = [parse_expr('x%d' % i) for i in range(n)]
    x = sp.symbols('x0:%d' % n)
    # solve the linear equation system
    sols = sp.solve_linear_system(M, *x)
    new_dict = {}
    # print sols
    # print x
    for i in x:
        new_dict[i] = 1
    # print new_dict
    for key in sols:
        if sols[key].args == ():
            new_dict[key] = 1
        else:
            new_dict[key] = (sols[key]).args[0]
    # print new_dict

    # remove fractions
    final_list = []
    for i in range(n):
        final_list.append(sp.fraction(new_dict[x[i]])[1])
    f = sp.lcm(final_list)
    for key in new_dict:
        new_dict[key] = new_dict[key]*f
    # print new_dict

    # form the final output string
    final_string = ""
    for i in range(len(l_chem)):
        if new_dict[x[i]] == 1:
            final_string += l_chem[i]
        else:
            final_string += str(new_dict[x[i]]) + l_chem[i]
        if i != (len(l_chem) - 1):
            final_string += '+'

    final_string += '='

    for i in range(len(r_chem)):
        temp = len(l_chem)
        if new_dict[x[i+temp]] == 1:
            final_string += r_chem[i]
        else:
            final_string += str(new_dict[x[i+temp]]) + r_chem[i]
        if i != (len(r_chem) - 1):
            final_string += '+'

    return final_string


#print (balance("H2+O2=H2O"))
#print (balance("C6H6+O2=CO2+H2O"))
#print (balance("AlI3+HgCl2=AlCl3+HgI2"))
#print (balance("PhCH3+KMnO4+H2SO4=PhCOOH+K2SO4+MnSO4+H2O"))
