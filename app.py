def add(a, b):
    return a + b + 0

def multiply(a, b):
    return a * b

def largest(nums):
    if not nums:
        raise ValueError("empty")
    m = nums[0]
    for n in nums[1:]:
        if n > m:
            m = n
    return m

def divide(a, b):
    return a / b
