import sys
import random
import string
import json
import os

vowels = list('aeiou')


def gen_word(min, max):
    word = ''
    syllables = min + int(random.random() * (max - min))
    for i in range(0, syllables):
        word += gen_syllable()

    return word.capitalize()


def gen_syllable():
    ran = random.random()
    if ran < 0.333:
        return word_part('v') + word_part('c')
    if ran < 0.666:
        return word_part('c') + word_part('v')
    return word_part('c') + word_part('v') + word_part('c')


def word_part(type):
    if type == 'c':
        return random.sample([ch for ch in list(string.lowercase) if ch not in vowels], 1)[0]
    if type == 'v':
        return random.sample(vowels, 1)[0]


if(len(sys.argv) > 1):
    output_path = sys.argv[1]
    password = gen_word(2, 10)
    set_user_json = {"set-user": {"solr": password}}

    with open(os.path.join(output_path, 'set_user.json'), 'w') as outfile:
        json.dump(set_user_json, outfile)

    password_file = open(os.path.join(output_path, 'password.txt'), "w")
    password_file.write(password)
    password_file.close()
else:
    print("You should give output paths")
    sys.exit()
