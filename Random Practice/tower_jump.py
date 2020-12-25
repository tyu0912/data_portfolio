def tower_jump(array):
    the_index = 0
    the_value = array[the_index]
    print(helper(array,the_index,the_value, 1))

def helper(array,the_index,the_value, i):
    
    print(str(the_index) + ' ' + str(the_value) + ' ' + str(i))

    if the_value - i == the_index:
        return False
    else:
        try:
            the_value = array[the_value-i]
        except:
            return True

    if the_value == 0:
        return helper (array, the_index,the_value, i+1)
    else:
        the_index = array[the_index+the_value-i]
        the_value = array[the_index]
        return helper(array,the_index,the_value,1)


tower_jump([4,2,0,0,2,0])

https://www.youtube.com/watch?v=kHWy5nEfRIQ