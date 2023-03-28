def multiply(x, y):
    result = 0
    # determine sign of the result
    sign = 1 if x >= 0 and y >= 0 or x < 0 and y < 0 else -1
    # convert both numbers to positive
    x, y = abs(x), abs(y)
    # compute product
    for i in range(y):
        result += x
    # round it to 5 decimal places
    result = round(result, 5)
    # adjust sign of result if necessary
    if sign == -1:
        result = -result
    # return the product
    return result
 
if __name__ == '__main__':
 
    num1 = 3.567
    num2 = 5
 
    print('Product is', multiply(num1, num2))  # Output: Product is 17.8
 
    num1 = 3
    num2 = 5
 
    print('Product is', multiply(num1, num2))  # Output: Product is 15

    num1 = -3
    num2 = 5
 
    print('Product is', multiply(num1, num2))  # Output: Product is -15

    num1 = -3.139
    num2 = 5
 
    print('Product is', multiply(num1, num2))  # Output: Product is 15
