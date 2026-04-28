import re

# A tokenizer turns text <-> integer IDs. Models can't read strings; they need
# numbers. This class holds two lookup tables: token -> id (for `encode`) and
# id -> token (for `decode`).
class SimpleTokenizerV1:
    # `__init__` is the constructor: it runs once when you do
    # `tokenizer = SimpleTokenizerV1(vocab)`. `self` refers to the new instance,
    # so anything assigned to `self.x` becomes an attribute on that object.
    def __init__(self, vocab):
        # `vocab` comes in as a dict like {"hello": 0, "world": 1, ...}.
        self.str_to_int = vocab
        # Build the inverse map (id -> token) using a dict comprehension.
        # `vocab.items()` yields (key, value) pairs, i.e. (token, id), which we
        # unpack as `s, i`. Then `{i: s ...}` flips them: id becomes the key.
        self.int_to_str = {i: s for s, i in vocab.items()}

    # encode: text (str) -> list[int]
    def encode(self, text):
        # Split on punctuation, `--`, or any whitespace. The regex group `(...)`
        # tells re.split to KEEP the separators in the result, so punctuation
        # stays as its own token instead of being thrown away.
        preprocessed = re.split(r'([,.?_!"()\']|--|\s)', text) 
        # List comprehension that filters out empty / whitespace-only strings
        # (re.split produces those around the separators) and strips whitespace
        # from the ones we keep.
        preprocessed = [  
            item.strip() for item in preprocessed if item.strip()  
        ] 
        # Look up each token's integer id. KeyError will be raised here if a
        # token isn't in the vocab -- that's why V2 typically adds an <|unk|>
        # fallback token.
        ids = [self.str_to_int[s] for s in preprocessed]
        return ids

    # decode: list[int] -> text (str)
    def decode(self, ids):
        # Map ids back to tokens, then join them with single spaces.
        # `" ".join(seq)` glues the strings in `seq` together with " " between.
        text = " ".join([self.int_to_str[i] for i in ids])

        # Joining with spaces puts a space before every punctuation mark
        # ("Hello , world .") -- this regex removes the space before `,.?~"()'`
        # so the output reads naturally ("Hello, world.").
        text = re.sub(r'\s+([,.?!"()\'])', r'\1', text) 

        return text