from hashlib import sha256
from base64 import b64encode
from os import urandom
import sys
import json
import os
import random
import string


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
        return random.sample([ch for ch in list(string.ascii_lowercase) if ch not in vowels], 1)[0]
    if type == 'v':
        return random.sample(vowels, 1)[0]


def solrBasicAuthHash(password, salt):
    """
    Python translation of
    https://github.com/apache/lucene-solr/blob/master/solr/core/src/java/org/apache/solr/security/Sha256AuthenticationProvider.java#L112
    Translation made in:
    https://gist.github.com/OdyX/1513aacee2ca010dcf954d62af776469#file-solr_basic_auth-py
    """
    # Compute the SHA256 of (salt+password)
    m = sha256()
    m.update(salt)
    m.update(password.encode("utf-8"))
    # Compute the SHA256 of the previous
    # The solr hash is in fact sha256(sha256(salt+password))
    return sha256(m.digest()).digest()


def solrBasicAuthString(password, salt):
    """
    Return the full hash + salt as solr expects it
    """
    hashed = solrBasicAuthHash(password, salt)
    b64hashed = b64encode(hashed)
    b64salt = b64encode(salt)
    return "{} {}".format(str(b64hashed), str(b64salt))


def genSolrBasicAuth(password, saltlength):
    salt = urandom(saltlength)
    return solrBasicAuthString(password, salt)


if(len(sys.argv) > 1):
    password = gen_word(2, 10)
    hashedPassword = genSolrBasicAuth(password, 32)
    security_json = {
        "authentication": {
            "blockUnknown": True,
            "class": "solr.BasicAuthPlugin",
            "credentials": {"solr": hashedPassword}
        },
        "authorization": {
            "class": "solr.RuleBasedAuthorizationPlugin",
            "permissions": [{"name": "security-edit", "role": "admin"}],
            "user-role": {"solr": "admin"}
        }
    }

    output_path = sys.argv[1]
    with open(os.path.join(output_path, 'security.json'), 'w') as outfile:
        json.dump(security_json, outfile)

    password_file = open(os.path.join(output_path, 'password.txt'), "w")
    password_file.write(password)
    password_file.close()

else:
    print("Enter an output path")
