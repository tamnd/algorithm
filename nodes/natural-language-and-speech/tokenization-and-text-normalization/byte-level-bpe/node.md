---
tag: HZ50C6
kind: algorithm
slug: byte-level-bpe
name: Byte-level BPE
aliases:
- byte-level byte-pair encoding
area: natural-language-and-speech/tokenization-and-text-normalization
level: advanced
summary: Byte-pair encoding run on the UTF-8 bytes of a text instead of its characters, so the base vocabulary has 256 symbols and no input is out of vocabulary.
solves: [text-tokenization]
model: word-ram
complexity:
  vars: {n: the length of the text to encode in bytes, b: the length of its longest pre-token in bytes, L: the total length of the distinct training pre-tokens in bytes, K: the number of merges, V: the vocabulary size (256 + K)}
  time: {train: O(K L), encode: O(n b), recover: O(n)}
  space: {train: O(L + K), vocabulary: O(V)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2019
  people: [Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever]
  note: GPT-2 ran BPE on bytes with a base vocabulary of 256 and blocked merges across character categories. Wang, Cho and Gu (2020) studied byte-level BPE for translation and gave a program to recover characters from bad byte output.
prereqs: [byte-pair-encoding, utf-8, subword-tokenization]
see_also: [wordpiece, unigram-language-model-tokenization, bpe-dropout, generative-pretrained-transformer, out-of-vocabulary-word, regular-expression, unicode-text-segmentation, dag-shortest-paths]
sources:
  - url: https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf
    title: Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei and Ilya Sutskever, Language models are unsupervised multitask learners, OpenAI technical report, 2019
    locator: Section 2.2, Input Representation (a base vocabulary of 256, no merges across character categories except for spaces), and Section 2.3 (a vocabulary of 50,257)
  - url: https://github.com/openai/gpt-2/blob/master/src/encoder.py
    title: OpenAI, GPT-2 reference code, encoder.py
    locator: bytes_to_unicode, the pre-tokenization pattern, and Encoder.bpe (merge the pair of lowest rank first)
  - paper: doi:10.1609/aaai.v34i05.6451
    title: Changhan Wang, Kyunghyun Cho and Jiatao Gu, Neural machine translation with byte-level subwords, AAAI 2020, volume 34(05), pages 9154 to 9160
    locator: the sections Encoding Byte-Level Representation and Decoding with Byte-Level Subwords (Equation 1, the recovery program)
  - paper: doi:10.18653/v1/P16-1162
    title: Rico Sennrich, Barry Haddow and Alexandra Birch, Neural machine translation of rare words with subword units, ACL 2016
    locator: the section on byte pair encoding (the merge learning algorithm over characters)
---

Byte-level BPE is [byte-pair encoding](/byte-pair-encoding/) applied to the [UTF-8](/utf-8/) bytes of a text, not to its characters. The base vocabulary is the 256 byte values, so every string has an encoding and no token is ever unknown. GPT-2 made the method common, with a pre-tokenizer that keeps merges inside runs of letters, of digits or of other symbols. Because a token can stop in the middle of a character, a model can emit byte sequences that are not valid UTF-8, and Wang, Cho and Gu (2020) give a small dynamic program that recovers as many characters as possible.

## In plain words

Computers store text as bytes, and there are only 256 different bytes. A letter such as "a" is one byte, while a Japanese character or an emoji takes three or four.

Byte-level BPE starts from these 256 bytes as its pieces. It then counts which two neighboring pieces appear together most often in a training text, glues them into a new piece, and repeats. Common words soon become single pieces. A rare character still has its bytes, so nothing is ever unknown.

Before counting, the text is cut into chunks such as a word with the space in front of it, a number, or a run of punctuation. Gluing never crosses a chunk border. A piece can hold only part of a character, so a model that writes pieces can write broken text, and a short repair step keeps all the characters that are still whole.

## The problem

Training: given texts and a number of merges $K$, learn a merge list of length at most $K$. Encoding: given a text and the merge list, return a list of tokens whose bytes join to the UTF-8 code of the text. Decoding: join the bytes of a token list and read them as UTF-8. Recovery: given any byte string, find the largest number of whole characters that can be read from it. The vocabulary has $V = 256 + K$ tokens; GPT-2 used 50,257, which is 256 bytes, 50,000 merges and one end-of-text token.

The pre-tokenizer of GPT-2 is the [regular expression](/regular-expression/) `'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+`. It splits off English contractions, then takes an optional space with a run of letters, of digits or of other symbols, and runs of whitespace; a run of spaces before a word gives its last space to the word. Every merge stays inside one pre-token.

## The algorithm

Training is BPE on bytes:

```pseudo id=main
BBPE-TRAIN(texts, K)
L1  C ← counts of the pre-tokens of all texts
L2  for each pre-token x in C do S[x] ← the list of the UTF-8 bytes of x
L3  merges ← empty list
L4  repeat K times
L5      P ← counts of adjacent pairs over all S[x], weighted by C(x)
L6      if P is empty then stop
L7      (a, b) ← the pair with the largest count, ties to the smallest pair
L8      in every S[x], replace each occurrence of a b, from the left, by ab
L9      append (a, b) to merges
L10 return merges
```

Encoding follows the GPT-2 code: inside each pre-token, merge the pair of lowest rank until no pair has a rank.

```pseudo id=encode
BBPE-ENCODE(text, merges)
E1  rank(a, b) ← the position of (a, b) in merges
E2  out ← empty list
E3  for each pre-token x of text do
E4      u ← the list of the UTF-8 bytes of x
E5      while some adjacent pair of u has a rank do
E6          (a, b) ← the adjacent pair of lowest rank
E7          replace each occurrence of a b in u, from the left, by ab
E8      append the tokens of u to out
E9  return out
```

Decoding joins the bytes and reads them as UTF-8, with a replacement character for each bad part. Recovery is the program of Wang, Cho and Gu, in the $(\max, +)$ semiring. For bytes $d_1 \cdots d_n$, $g(i, j) = 1$ if $d_i \cdots d_j$ is the code of one character and 0 otherwise, and $f(k)$ is the most characters that the first $k$ bytes can give:

```pseudo id=recover
RECOVER(d1 ... dn)
R1  f(0) ← 0
R2  for k ← 1 to n do
R3      f(k) ← max over t = 1 .. min(4, k) of f(k - t) + g(k - t + 1, k)
R4      back(k) ← a t that gives this maximum
R5  walk back from n by back(k) and keep the chunks with g = 1
```

This is a longest path in a [DAG](/dag-shortest-paths/) whose nodes are the byte positions 0 to $n$ and whose edges span 1 to 4 bytes. Byte positions use fencepost spans: $d[i..j)$ holds the bytes $i + 1$ to $j$.

## Example

Train on the text "日本 日本 日日". The pre-tokens are "日本", " 日本" and " 日日", once each. In UTF-8, 日 is E6 97 A5, 本 is E6 9C AC, and the space is 20. The first counts of adjacent pairs:

| pair | count |
|---|---|
| 97 A5 | 4 |
| E6 97 | 4 |
| A5 E6 | 3 |
| 20 E6 | 2 |
| 9C AC | 2 |
| E6 9C | 2 |

The first two tie, and 97 A5 wins by byte order. It becomes token 256, which is two continuation bytes and not valid UTF-8 by itself. The next merges are E6 with 97 A5, which gives token 257 = 日, then 20 with 日, which gives 258 = " 日", then 9C AC as 259, and E6 with 9C AC, which gives 260 = 本. Three more merges join each pre-token into a single token, and then no pair is left.

With the first five merges, " 日本語" is one pre-token. It encodes as 258, 260, 232, 170, 158: " 日", 本, and the three bytes E8 AA 9E of 語, which never occurred in training. Nothing is unknown, and decoding gives the text back.

If a model emits token 256 and then token 257, the bytes 97 A5 E6 97 A5 decode to two replacement characters followed by 日, and RECOVER keeps the one character 日. The bytes E6 97 E6 97 A5 61 A5 C3 A9 give 3 characters, 日, a and é: the incomplete E6 97 and the stray A5 are dropped.

## Correctness

The pre-tokens join to the text, a merge never changes the bytes, and every byte has a token, so decoding an encoding always gives the original text back; this is a theorem for every string. Training merges, at each step, a pair of largest count, which is a heuristic for a short encoding, not an optimum. RECOVER is correct by the usual argument for a longest path: the last chunk of a best split of the first $k$ bytes has 1 to 4 bytes, and the rest is a best split of a shorter prefix. The proofs are in proofs/correctness.md.

Encoding by lowest rank first is the rule of the GPT-2 code. It is not proved here that it gives the same tokens as replaying the merges in their order: for the hand-made list $(x, ab)$, $(a, b)$ and the text $xab$ the two differ. On merge lists made by training, the tests found no difference.

## Complexity

- **Training.** In the word-RAM model with a hash table for the counts, one pass over the distinct pre-tokens counts the pairs and another applies the merge, so a step costs $O(L)$ and $K$ steps cost $O(K L)$. Implementations that update only the counts near each merge are much faster in practice.
- **Encoding.** A pre-token of $b'$ bytes needs at most $b' - 1$ rounds of lines E5 to E7, each $O(b')$, so a text of $n$ bytes costs $O(n b)$. A [priority queue](/priority-queue/) of the pairs brings one pre-token to $O(b' \log b')$.
- **Recovery.** Each position tries 4 chunks of at most 4 bytes, so RECOVER costs $O(n)$ time and space.

## Properties

- **No unknown token.** This is the main point of the method, and it holds for any Unicode string, including emoji and unseen scripts.
- **A small base.** The base has 256 symbols. A character-level BPE that covers all of Unicode would need a base of over 130,000 symbols, as the GPT-2 report notes.
- **Longer sequences for rare scripts.** A text in a script that the merges do not cover comes out as raw bytes, up to 4 tokens per character. Wang, Cho and Gu note that a byte sequence can be up to 4 times longer than the character sequence.
- **Tokens need not be text.** A token can be part of a character, as token 256 in the example. Tools that show tokens use the GPT-2 map from bytes to 256 printable characters, which writes a space as Ġ.

## Variants and improvements

- **Merge rules.** GPT-2 stops merges across character categories, with an exception for spaces, because plain BPE on bytes learned many versions of words such as dog. Other systems use other pre-tokenization patterns, and each pattern gives a different vocabulary.
- **Byte-level BPE for translation.** Wang, Cho and Gu (2020) used byte-level vocabularies of 2K to 32K tokens and the recovery step for decoding.
- **Regularization.** [BPE-dropout](/bpe-dropout/) skips merges at random while the model trains, and it applies to byte merges in the same way.
- **Other subword models.** [WordPiece](/wordpiece/) and [unigram language model tokenization](/unigram-language-model-tokenization/) start from characters, so they need an unknown token or a byte fallback for unseen characters.

## When to use it

Use it when the input can be any text, such as web pages, code, or many languages, and an unknown token is not acceptable. It suits generative models such as a [generative pretrained transformer](/generative-pretrained-transformer/), which must write any string. If the text is in a few known scripts and sequence length matters more, a character-level vocabulary can be shorter per character for those scripts.

## Pitfalls

- **Decoding single tokens.** Decoding a stream token by token can split a character, and each half becomes a replacement character. Buffer the bytes until a character is complete.
- **The pre-tokenizer is part of the model.** A different pattern, or a regex engine without `\p{L}`, gives other pre-tokens and other tokens than the trained model expects.
- **Merges can be wasted on bytes.** Without the pre-tokenizer, merges join words with punctuation and spaces in many variants.
- **Ties.** The merge order depends on how ties are broken. Reproduce a vocabulary only with the same rule.

## Implementations

## History

Sennrich, Haddow and Birch (2016) brought byte-pair encoding to neural machine translation, with characters as the base symbols. Radford et al. (2019) moved the base to bytes for GPT-2, so that the model could assign a probability to any Unicode string, and added the rule against merges across character categories. Wang, Cho and Gu (2020) called the method BBPE, tested it in translation, and gave the recovery program for invalid output.

## References
