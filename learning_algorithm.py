from utils import do_cprofile
from stringMask import stringMask


@do_cprofile
def learning_algorithm(file_pointer):
    """ Get exhaustive mask list from learning
        -Take the first word, build a minimal mask
        -Try the mask against the second word
            -If matches, continue
            -Else build a second mask
        -Try the 2 first masks against the 3rd word
        -So on...
    """
    masks = []
    line_count = 0
    total_generated_space = 0
    for line in file_pointer:
        line_count += 1
        word = line.rstrip('\n')
        for mask in masks:
            # pdb.set_trace()
            if mask.covers(word):
                mask.hitcount += 1
                break
        else:
            newmask = stringMask("", word)
            newmask.hitcount = 0
            total_generated_space += newmask.generated_space
            masks.append(newmask)
            masks.sort(key=lambda x: x.generated_space)
    else:
        return line_count, masks
