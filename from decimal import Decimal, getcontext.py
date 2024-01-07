from decimal import Decimal, getcontext

# Set the precision to a sufficiently high value
getcontext().prec = 50

# Perform your calculations
result = Decimal('1330815614343216928') / Decimal('665407807171608464')

# Print the result
print(result)
