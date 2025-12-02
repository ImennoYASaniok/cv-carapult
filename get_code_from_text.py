from text_finder import find_similar_string


def return_code_from_text(text="", credulity=25, words=[]):
    datas = []
    for i in words:
        datas.append(find_similar_string(text, i[0], credulity))
    if min(datas) <= credulity/100:
        return words[datas.index(min(datas))][1]
    else:
        return -1

