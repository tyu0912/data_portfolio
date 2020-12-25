def ransom_note(magazine, ransom):
    
    for word in ransom:
        #print('looking for ' + word + ' in ' + ' '.join(magazine) )
        if word in magazine:
            del magazine[magazine.index(word)]
        else:
            return False
    
    return True

    #ransom_count = {}
    #magazine_count = {}
    
    #for word in ransom:
    #    if hasattr(ransom_count,word):
    #        continue
    #    else:
    #        ransom_count[word] = ransom.count(word)
            
    #for word in magazine:
    #    if hasattr(magazine_count,word):
    #        continue
    #    else:
    #        magazine_count[word] = magazine.count(word)
    
    
    #for k,v in ransom_count.items():
    #    if magazine_count[k] >= v:
    #        continue
    #    else:
    #        return False
        
    #return True

m, n = map(int, input().strip().split(' '))
magazine = input().strip().split(' ')
ransom = input().strip().split(' ')
answer = ransom_note(magazine, ransom)
if(answer):
    print("Yes")
else:
    print("No")
    
