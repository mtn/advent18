#!/usr/bin/env python3

inp = 540561
# inp = 18
inp_digits = list(map(int, str(inp)))

inputs = [3, 7]
ind1, ind2 = 0, 1

# Can add two
while inputs[-len(inp_digits):] != inp_digits and inputs[-len(inp_digits)-1: -1] != inp_digits:
    inp_sum = str(inputs[ind1] + inputs[ind2])
    inputs.append(int(inp_sum[0]))
    if len(inp_sum) == 2:
        inputs.append(int(inp_sum[1]))

    ind1 = (ind1 + 1 + inputs[ind1]) % len(inputs)
    ind2 = (ind2 + 1 + inputs[ind2]) % len(inputs)

ans = len(inputs) - len(str(inp))
if inputs[-len(inp_digits):] != inp_digits:
    ans -= 1

print(ans)
