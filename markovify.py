import markovify

# Open the raw text to parse.
with open("/resources/rawText.txt") as f:
    text = f.read()

# Build the model
text_model = markovify.Text(text)

# print randomly-generated sentences
for i in range(5):
    print(text_model.make_sentence())

# Print randomly generated sentences of no more than 140 characters
for i in range(3):
    print(text_model.make_short_sentence(140))


