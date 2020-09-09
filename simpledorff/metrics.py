def nominal_metric(x, y):
    return 1 if x != y else 0
def interval_metric(x,y):
    return (x-y)**2