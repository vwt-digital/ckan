import hashlib
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
    output_path_security = sys.argv[1]
    output_path_answers = sys.argv[2]

    user = gen_word(2, 4)
    salt = gen_word(2, 4)
    password = gen_word(2, 4)
    hashed_password = hashlib.sha256(salt.encode()).hexdigest()
    security_json = {
        "authentication": {
            "blockUnknown": "true",
            "class": "solr.BasicAuthPlugin",
            "credentials": {user: hashed_password}
        },
        "authorization": {
            "class": "solr.RuleBasedAuthorizationPlugin",
            "user-role": {user: "admin"},
            "permissions": [{"name": "security-edit",
                            "role": "admin"}]
        }
    }

    with open(os.path.join(output_path_security, 'security.json'), 'w') as outfile:
        json.dump(security_json, outfile)

    user_file = open(os.path.join(output_path_answers, 'user.txt'), "w")
    user_file.write(user)
    user_file.close()
    password_file = open(os.path.join(output_path_answers, 'password.txt'), "w")
    password_file.write(password)
    password_file.close()
else:
    print("You should give output paths")
    sys.exit()
