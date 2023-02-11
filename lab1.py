# Solve the quadratic equation ax**2 + bx + c = 0

# import complex modules
import cmath

a = 1
b = 2
c = 3

# calc Discriminant
d = (b**2) - (4*a*c)

# find solutions
x1 = (-b-cmath.sqrt(d))/(2*a)
x2 = (-b+cmath.sqrt(d))/(2*a)

print( 'The solutions are {0} and {1}'.format(x1,x2))
