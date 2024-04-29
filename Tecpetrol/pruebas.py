a = [1, 4, 9, 16]
pen = []
dt = 1
for i in range(len(a)):
    if i > 0:
        m = (a[i] - a[i - 1])/dt
    else: continue