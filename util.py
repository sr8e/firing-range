# length of vector
def length(vec):
    return sum([v ** 2 for v in vec]) ** 0.5


# dot product
def dot(a, b):
    return sum([u * v for u, v in zip(a, b)])


# scalar multiplication
def scalar(c, vec):
    return tuple([c * v for v in vec])


# addition
def add(a, b):
    return tuple([u + v for u, v in zip(a, b)])


# subtraction
def sub(a, b):
    return tuple([u - v for u, v in zip(a, b)])


# distance between dot and line
def distance(diff, direction):
    d = length(diff)
    v = length(direction)
    p = dot(diff, direction)
    return ((d ** 2) * (v ** 2) - p ** 2) ** 0.5 / v


#
def travel(diff, direction):
    return dot(diff, direction) / length(direction)


# orthographic projection to the ground
def ground(vec):
    return (vec[0], vec[2])


#
def clamp(value, maxv, minv):
    return min(maxv, max(minv, value))
