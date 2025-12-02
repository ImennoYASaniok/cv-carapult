import string

def format_string(str):
    str = str.lower()
    special_chars = string.punctuation + '0123456789'
    str = ''.join([char for char in str if char not in special_chars])
    return str

def find_similar_string(main_string, target_string, threshold):
    main_string = format_string(main_string)
    target_string = format_string(target_string)
    if len(main_string) < len(target_string):
        return 1

    diff_threshold = int(len(target_string))

    for i in range(len(main_string) - len(target_string) + 1):
        diff_count = 0
        for j in range(len(target_string)):
            if main_string[ i +j] != target_string[j]:
                diff_count += 1
        if diff_count <= diff_threshold/2:
            try:
                return diff_count/diff_threshold
            except:
                return 0

    return 1
