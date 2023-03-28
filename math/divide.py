def divide(x, y):
 
    # handle divisibility by 0
    if y == 0:
        print('Error!! Divisible by 0')
        exit(-1)
 
    # store sign of the result
    sign = 1
    if x * y < 0:
        sign = -1
 
    # convert both dividend and divisor to positive
    x = abs(x)
    y = abs(y)
 
    # initialize quotient and remainder by 0
    quotient = 0
    remainder = 0
 
    # loop till dividend `x` becomes less than divisor `y`
    while x >= y:
        x = x - y                   # perform a reduction on the dividend
        quotient = quotient + 1     # increase quotient by 1
 
    remainder = x
 
    # check if there is a remainder left
    if remainder > 0:
        quotient_str = str(quotient) + "."
        decimal_places = 0
        while decimal_places < 5:
            remainder *= 10
            quotient_digit = remainder // y
            quotient_str += str(quotient_digit)
            remainder = remainder % y
            decimal_places += 1
        quotient = float(quotient_str)
 
    return sign * quotient
 
 
if __name__ == '__main__':
 
    dividend = 22
    divisor = 2
 
    print(divide(dividend, divisor))
