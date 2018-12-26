#!/usr/bin/env python3

inp = 540561
# inp = 18

inputs = [3, 7]
ind1, ind2 = 0, 1

while len(inputs) < (inp + 10):
    inp_sum = str(inputs[ind1] + inputs[ind2])
    inputs.append(int(inp_sum[0]))
    if len(inp_sum) == 2:
        inputs.append(int(inp_sum[1]))

    ind1 = (ind1 + 1 + inputs[ind1]) % len(inputs)
    ind2 = (ind2 + 1 + inputs[ind2]) % len(inputs)

print("".join(map(str, inputs[-10:])))
