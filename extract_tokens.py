import tiktoken
import json
import csv

# Load the encoding used by GPT-5
enc = tiktoken.get_encoding("o200k_base")

# Extract all tokens from the vocabulary
# Iterate through all possible token IDs
vocab = {}
for token_id in range(enc.max_token_value + 1):
    try:
        # Decode each token ID to get the token string
        token_bytes = enc.decode_single_token_bytes(token_id)
        vocab[token_id] = token_bytes.decode('utf-8', errors='replace')
    except:
        # Some token IDs might not be valid
        continue

# Save to JSON file
with open('gpt5_tokens.json', 'w', encoding='utf-8') as f:
    json.dump(vocab, f, ensure_ascii=False, indent=2)

# Save to CSV file
with open('gpt5_tokens.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['token_id', 'token'])
    for token_id, token in sorted(vocab.items()):
        writer.writerow([token_id, token])

print(f"Extracted {len(vocab)} tokens")
print(f"Token vocabulary size: {enc.max_token_value + 1}")

# Optional: Save in a more readable format (token_id: token)
with open('gpt5_tokens.txt', 'w', encoding='utf-8') as f:
    for token_id, token in sorted(vocab.items()):
        f.write(f"{token_id}: {repr(token)}n")

print("Done! Saved to gpt5_tokens.json, gpt5_tokens.csv, and gpt5_tokens.txt")