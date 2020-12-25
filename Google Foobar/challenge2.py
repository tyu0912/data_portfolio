def answer(l):
    overall_list = []
    output = []
    
    for item in l:
        the_input = item.split('.')
        the_input_num = []
        
        for num in the_input:
            the_input_num.append(int(num))
        
        while len(the_input_num) < 3:
            the_input_num.append(0)
        
        overall_list.append((the_input_num, item))
        
    rough1 = sorted(overall_list)

    for v in rough1:
        output.append(v[1])
        
    return output

c1 = ["1.1.2","1.0","1.3.3","1.0.12","1.0.2"]
c2 = [""]

test = answer()

print(test)
