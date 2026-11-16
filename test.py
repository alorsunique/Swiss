import string

lowercase_letters = list(string.ascii_lowercase)
print(lowercase_letters)



input_string = input()

word_list = []

segment_word_count = 0
for word in input_string.split(' '):
    segment_word_count += 1
    new_word = ''
    count = 0
    for char in word:
        count += 1
        # print(lowercase_letters.index(char))
        index = lowercase_letters.index(char)
        print(index)
        print(count)
        print(segment_word_count)
        new_index = ((count*index) + 2**index + count + (count*segment_word_count)) % 26
        print(new_index)

        new_word += lowercase_letters[new_index]

    word_list.append(new_word)

out_string = ' '.join(word for word in word_list)

print(out_string)