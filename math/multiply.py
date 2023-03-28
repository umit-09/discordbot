def multiply(x, y):
 
    # handle multiplication by 0
    if x == 0 or y == 0:
        return 0
 
    # determine sign of the result
    sign = 1
    if x * y < 0:
        sign = -1
 
    # convert both numbers to positive
    x = abs(x)
    y = abs(y)
 
    # compute product and round it to 5 decimal places
    product = round(x * y, 5)
 
    # return the product with the correct sign
    return sign * product
 
if __name__ == '__main__':
 
    num1 = 3.56
    num2 = 5
 
    print('Product is', multiply(num1, num2))  # Output: Product is 17.8
 
    num1 = 3
    num2 = 5
 
    print('Product is', multiply(num1, num2))  # Output: Product is 15

    num1 = -3
    num2 = 5
 
    print('Product is', multiply(num1, num2))  # Output: Product is -15

    num1 = -3.56
    num2 = 5
 
    print('Product is', multiply(num1, num2))  # Output: Product is 15
