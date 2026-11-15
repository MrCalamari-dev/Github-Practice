def add(a, b):
    return a - b

def largest(nums):
    if not nums:
        raise ValueError("empty")
    m = nums[0]
    for n in nums[1:]:
        if n > m:
            m = n
    return m

def subtract(a, b):
    return a - b

def power(a, b):
    return a ** b

def clamp(x, lo, hi):
    return max(lo, min(hi, x))
