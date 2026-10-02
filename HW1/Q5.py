sentence = input("Enter a sentence: ")

words = sentence.split()

word_count = len(words)
longest_word = max(words, key=len)
reverse_words = words[::-1]

print("Number of words:", word_count)
print("Longest word:", longest_word)
print("Reverse word order:", " ".join(reverse_words))
