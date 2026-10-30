# tokenary

Exploring the o200k tokenizer from the tiktoken package as a frequency
dictionary of the internet.

`o200k_base` is the encoding that [tiktoken](https://github.com/openai/tiktoken)
uses for GPT-5, GPT-4.1, GPT-4o and the o1/o3/o4-mini models. This repository
lists all 200,000 of its tokens with their ids, as JSON, CSV and plain text,
so the whole vocabulary can be searched with `grep` or a spreadsheet without
writing any code.

## What is in the repository

| File | Contents |
|---|---|
| `extract_tokens.py` | The script that produced the three lists below. |
| `gpt5_tokens.json` | `{"token_id": "token"}` for all 200,000 tokens, pretty-printed. |
| `gpt5_tokens.csv` | Two columns, `token_id,token`, one row per token. |
| `gpt5_tokens.txt` | `id: 'token'` pairs in Python `repr` form. See *Known issues*. |

## Reading a token id as a frequency rank

The tokenizer was built by byte-pair encoding (BPE). Ids 0 to 255 are the 256
single bytes. Training then repeatedly takes the pair of adjacent pieces that
occurs most often in the training text and merges it into a new token, which
gets the next id. So a token's id is its merge order, and a lower id means,
roughly, a string that was more common in that text.

The order is easy to see in the lists:

| Id | Token |
|---|---|
| 256 | two spaces |
| 258 | `in` |
| 260 | ` t` |
| 290 | ` the` |
| 326 | ` and` |
| 6,179 | ` internet` |
| 7,595 | ` computer` |
| 32,949 | ` Hello` |
| 40,617 | ` hello` |
| 60,252 | ` banana` |
| 99,665 | ` tokenizer` |

Three limits on that reading:

- **It is an order, not a count.** Each merge is picked by how often the pair
  occurs at that step, after earlier merges have already joined pieces
  together, so ids are only roughly in frequency order. tiktoken does not
  ship the counts.
- **"The internet" is an assumption.** OpenAI has not published the text the
  tokenizer was trained on. The vocabulary mixes English, many other
  languages and pieces of source code, which fits web text, but the exact mix
  is unknown.
- **Two ids are not merges.** `<|endoftext|>` (199,999) and `<|endofprompt|>`
  (200,018) are special tokens added by hand.

## How it was produced

`extract_tokens.py` loads `o200k_base` with tiktoken and walks every id from
0 to the highest assigned id (200,018). For each id it asks tiktoken for the
token's raw bytes and decodes them as UTF-8, replacing any invalid bytes with
`U+FFFD`. Ids that are not assigned are skipped.

The result has 200,000 entries:

- 199,998 ordinary tokens, ids 0 to 199,997;
- two special tokens, `<|endoftext|>` (199,999) and `<|endofprompt|>` (200,018).

The other 19 ids in that range (199,998 and 200,000 to 200,017) are unassigned.

The committed files were checked on 2026-10-30. Rebuilding them from OpenAI's
published `o200k_base.tiktoken` file, whose SHA-256 matches the hash tiktoken
pins (`446a9538…5bf8b0cfb1a2d`), gives byte-identical output.

## Other things to know when reading the lists

- **Tokens are bytes, not always text.** 1,584 tokens contain part of a
  multi-byte UTF-8 character, including the 128 one-byte tokens for byte
  values `0x80` to `0xFF`. Decoded on their own, those parts come out as
  `U+FFFD` (`�`), so several different ids can show the same string: the
  200,000 ids map to 198,797 distinct strings. If you need exact bytes, call
  `tiktoken.get_encoding("o200k_base").decode_single_token_bytes(id)`.
- **Leading spaces are part of the token.** `" the"` and `"the"` are
  different tokens. About half the vocabulary (106,529 tokens) starts with a
  space.
- **Why "gpt5" in the file names.** tiktoken's own model table maps `gpt-5`
  to `o200k_base`. The same vocabulary is used by GPT-4o and GPT-4.1, so the
  lists are not specific to GPT-5.

## How to run it

The script needs Python 3 and tiktoken. It writes the three files into the
current directory, and tiktoken downloads the encoding file (about 3.6 MB)
the first time it runs.

```bash
uv run --with tiktoken python extract_tokens.py
```

or, without uv:

```bash
pip install tiktoken
python extract_tokens.py
```

## Known issues

- `gpt5_tokens.txt` was meant to hold one token per line. The script writes a
  literal `n` where it should write a newline, so the whole file is a single
  line. Use the JSON or CSV file instead.
- The script catches every exception while walking the ids, not only the
  error for an unassigned id, so an unexpected failure would silently shorten
  the list. The committed lists are complete (see the check above).

## Data source and licence

The vocabulary is OpenAI's `o200k_base` encoding as distributed for tiktoken,
which is released under the MIT licence. The encoding file itself carries no
separate licence; other MIT-licensed projects, such as
[tiktoken-rs](https://github.com/zurawiki/tiktoken-rs), redistribute the same
file. The tiktoken copyright and licence notice is reproduced in
[`NOTICE-DATA.md`](NOTICE-DATA.md).

The code in this repository is released under the Apache License 2.0; see
[`LICENSE`](LICENSE).
