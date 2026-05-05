import urllib.request
import re
from simple_tokenizer_v1 import SimpleTokenizerV1

url = ("https://raw.githubusercontent.com/rasbt/"
       "LLMs-from-scratch/main/ch02/01_main-chapter-code/"
       "the-verdict.txt")

file_path = "the-verdict.txt"

urllib.request.urlretrieve(url, file_path)

# `with` is a context manager: it guarantees cleanup (here, closing the file)
# happens automatically when the block exits, even if an exception is raised.
# `open(path, "r", encoding="utf-8")` opens the file in read-mode as UTF-8 text
# and `as file` binds the file object to the name `file`.
with open(file_path, "r", encoding="utf-8") as file:
    raw_test = file.read()

# print("TOTAL number of characters in the file:", len(text))
# print(text[:99])

preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', raw_test)
# List comprehension: shape is `[<expr> for <item> in <iterable> if <condition>]`.
# Equivalent to a for-loop that appends `item` to a new list when the condition
# is truthy. Here `item.strip()` returns "" for empty/whitespace-only strings,
# and "" is falsy in Python, so those entries get filtered out.
preprocessed = [item for item in preprocessed if item.strip()]
print(len(preprocessed))

# print(preprocessed[:30])

all_words = sorted(set(preprocessed))
vocab_size = len(all_words)
print(f"Vocabulary size: {vocab_size}")


# Dict comprehension: shape is `{<key>: <value> for <vars> in <iterable>}`.
# `enumerate(all_words)` yields (index, item) pairs like (0, "!"), (1, '"'), ...
# We unpack each pair into `integer, token`, then flip them so the token becomes
# the key and the index becomes the value -- a token -> id lookup table.
vocab = {token: integer for integer, token in enumerate(all_words)}
for i, item in enumerate(vocab.items()):
    print(item)
    if i >= 50:
        break

# Instantiate the tokenizer. Pass in the vocabulary dictionary.
tokenizer = SimpleTokenizerV1(vocab)  

text = """"It's the last he painted, you know,"  
Mrs. Gisburn said with pardonable pride."""  

# Encode the text into a list of integers
ids = tokenizer.encode(text)  

print('Encoded text:', ids) 

print('Decoded text:', tokenizer.decode(ids))

text = "Hello, do you like tea?"
print(tokenizer.encode(text))

# def main():
#     print("Hello from setup-python-with-uv!")


# if __name__ == "__main__":
#     main()
