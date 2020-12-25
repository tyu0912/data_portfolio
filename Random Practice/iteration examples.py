def all_subsets(given_array):
    subset = [None] * len(given_array)
    helper(given_array, subset, 0)

def helper(given_array, subset, i):
    
    if i == len(given_array):
        print(subset)
    else:
        subset[i] = None
        helper(given_array,subset, i+1)
        subset[i] = given_array[i]
        helper(given_array,subset,i+1)

#all_subsets([1,2])

from itertools import chain, combinations

def powerset(iterable):
    xs = list(iterable)
    # note we return an iterator rather than a list
    return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

print(list(powerset([1,2,3])))

#for x in (range(len([0,1,2]))):
#    print (x)