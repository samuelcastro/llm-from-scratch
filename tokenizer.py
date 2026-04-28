import re

text = "Hello, world. This-- is a test."
result = re.split(r'([,.:;?_!]|--|\s)', text)
result = [item for item in result if item.strip()]
print(result)

# __name__ == "__main__":
#     main()