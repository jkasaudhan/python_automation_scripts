# Installing Library
# !pip install lmproof

# Importing Library
import lmproof as lm

# Function for proofreading


def Proofread(text):
    proof = lm.load("en")
    error_free_text = proof.proofread(text)
    return error_free_text


# Sample Text
TEXT = 'There is many apples'  # Place sample Text here

# Function Call
print(Proofread(TEXT))
