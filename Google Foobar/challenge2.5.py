def answer(total_lambs):
    
    def generous(total_lambs):
        if total_lambs < 1:
            return 0

        employees = 2
        base_value = 1
        next_value = 2 

        print(base_value)
        print(next_value)

        total_lambs = total_lambs - base_value - next_value

        while total_lambs > 0:
            if total_lambs >= next_value*2:
                total_lambs = total_lambs - next_value*2

                base_value = next_value
                next_value = next_value *2

                employees = employees + 1

            else:
                if total_lambs >= base_value + next_value:
                    next_value = total_lambs
                    total_lambs = total_lambs - next_value
                    employees = employees + 1
                else:
                    break


                print(next_value)
                print('total lambs: ' + str(total_lambs))
                
        return employees
                
            
            

        """employees = 1
        value = 1

        total_lambs = total_lambs - value

        while total_lambs > 0:
            value = value*2
            total_lambs = total_lambs - value
            if total_lambs >=0:
                employees = employees + 1"""
        #print(total_lambs)
        

    """ def stingy(total_lambs):
        employees = 1 
        base_value = 1
        remain_lambs = total_lambs - base_value

        if_one_more = 1 

        remain_lambs = remain_lambs - if_one_more

        employees = employees + 1 

        lambs_allowed = 0

        while remain_lambs > 0:
            lambs_allowed = base_value + if_one_more
            remain_lambs = remain_lambs - lambs_allowed
            if remain_lambs >=0:
                employees = employees + 1
                base_value = if_one_more
                if_one_more = lambs_allowed

        return employees """

    def stingy(total_lambs):
        if total_lambs < 1:
            return 0

        employees = 2 
        base_value = 1 
        next_value = 1 

        #print(base_value)
        #print(next_value)

        total_lambs = total_lambs - base_value - next_value

        while total_lambs > 0:
            if employees % 2 == 1:
                base_value = base_value + next_value
                total_lambs = total_lambs - base_value
                #print(base_value)
            else:
                next_value = next_value + base_value
                total_lambs = total_lambs - next_value
                #print(next_value)

            if total_lambs < 0:
                break
            else:
                employees = employees + 1
        
        return employees


    print('Stingy is: ' + str(stingy(int(total_lambs))))
    print('Generous is: ' + str(generous(int(total_lambs))))
    return stingy(int(total_lambs)) - generous(int(total_lambs))
    #print(stingy(int(total_lambs)))
    #return generous(int(total_lambs))

c1 = 100
c2 = 143
c3 = 13

test= (answer(143))

print('Final Answer is: ' + str(test))
    
  



    

