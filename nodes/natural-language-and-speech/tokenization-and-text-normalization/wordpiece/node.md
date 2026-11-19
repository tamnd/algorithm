---
tag: N8960R
kind: algorithm
slug: wordpiece
name: WordPiece
aliases:
- WordPiece tokenization
area: natural-language-and-speech/tokenization-and-text-normalization
level: core
summary: Learn subword units by merging the pair that most raises a unigram likelihood, then encode each word by greedy longest match with ## pieces and [UNK].
solves: [text-tokenization]
model: word-ram
complexity:
  vars: {n: the length of one word in characters, m: the length of the longest training word, L: the total length of the distinct training words, K: the number of merges, V: the vocabulary size (number of types)}
  time: {train: O(K L m), encode_word: O(n^3)}
  space: {train: O(L), vocabulary: O(V m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2012
  people: [Mike Schuster, Kaisuke Nakajima]
  note: Schuster and Nakajima built the word piece inventory for Japanese and Korean voice search. Wu et al. (2016) used wordpieces in Google's translation system, and BERT (Devlin et al. 2019) made the ## form and greedy longest-match encoding common.
prereqs: [subword-tokenization, byte-pair-encoding, language-model]
see_also: [fast-wordpiece-tokenization, unigram-language-model-tokenization, byte-level-bpe, maximum-matching-segmentation, trie, bert, out-of-vocabulary-word, maximum-likelihood-estimation]
sources:
  - paper: doi:10.1109/ICASSP.2012.6289079
    title: Mike Schuster and Kaisuke Nakajima, Japanese and Korean voice search, ICASSP 2012, pages 5149 to 5152
    locator: Section 3, Segmentation and word inventory (page 5150, the four-step building algorithm and its speedups)
  - url: https://arxiv.org/abs/1609.08144
    title: Yonghui Wu et al., Google's neural machine translation system, Bridging the gap between human and machine translation, arXiv 1609.08144, 2016 (preprint)
    locator: Section 4.1, Wordpiece Model
  - paper: doi:10.18653/v1/N19-1423
    title: Jacob Devlin, Ming-Wei Chang, Kenton Lee and Kristina Toutanova, BERT, Pre-training of deep bidirectional transformers for language understanding, NAACL 2019, pages 4171 to 4186
    locator: Section 3, Input/Output Representations (a WordPiece vocabulary of 30,000 tokens)
  - url: https://github.com/google-research/bert/blob/master/tokenization.py
    title: Google Research, BERT reference code, tokenization.py
    locator: class WordpieceTokenizer (greedy longest-match-first, max_input_chars_per_word = 200)
  - paper: doi:10.18653/v1/2021.emnlp-main.160
    title: Xinying Song, Alex Salcianu, Yang Song, Dave Dopson and Denny Zhou, Fast WordPiece tokenization, EMNLP 2021, pages 2089 to 2103
    locator: Sections 1 and 2 (MaxMatch in WordPiece and its O(n^2) or O(nm) cost)
  - url: https://huggingface.co/learn/llm-course/chapter6/6
    title: Hugging Face, LLM Course, Chapter 6, WordPiece tokenization
    locator: the training score freq(ab) / (freq(a) freq(b)), and the remark that Google did not release its training code
---

WordPiece is a [subword tokenization](/subword-tokenization/) method in two parts: a training step that builds a vocabulary of word pieces by merging adjacent units, and an encoder that splits each word into the longest pieces of that vocabulary from left to right. Training is like [byte-pair encoding](/byte-pair-encoding/), but it picks the merge that most raises the likelihood of a unigram [language model](/language-model/) of the units, not the most frequent pair. The encoder is the greedy rule of [maximum matching segmentation](/maximum-matching-segmentation/) applied to pieces, with the prefix "##" on every piece that does not start a word and the token [UNK] for a word it cannot cover. [Fast WordPiece tokenization](/fast-wordpiece-tokenization/) gives the same output as this encoder in linear time.

## In plain words

Start with the single letters of every word in a training text. Then glue two neighboring pieces into a new piece, again and again. At each step, choose the glue that makes the text most probable under a simple model that counts how often each piece appears. A pair of pieces that almost always appear together is a good choice, even if it is not the most common pair. Stop when the list of pieces has the size you want.

To cut a new word, take the longest piece from the list that starts at the first letter. Then take the longest piece that fits after it, and so on. Pieces inside a word carry a mark, so the word can be put back together. If some position has no piece at all, the whole word becomes one unknown token.

## The problem

The training input is a map $C$ from distinct words to counts, and a number of merges $K$. Each word $w = w_1 \cdots w_n$ starts as the units $w_1, \#\#w_2, \ldots, \#\#w_n$. A merge of the adjacent units $a$ and $b$ makes the unit $ab$: the text of $a$ followed by the text of $b$ without its "##". The output is a vocabulary $V$ of units and the list of merges.

The criterion is the log likelihood of the corpus under a unigram model whose probabilities are the maximum likelihood estimates $c(x)/N$, where $c(x)$ counts the occurrences of unit $x$ and $N = \sum_x c(x)$:

$$\mathcal{L} = \sum_x c(x) \log \frac{c(x)}{N} = \sum_x F(c(x)) - F(N), \qquad F(x) = x \log x,\ F(0) = 0 \qquad (\log \text{ base } e).$$

Merging $k$ occurrences of $(a, b)$ changes only $c(a)$, $c(b)$, $c(ab)$ and $N$, so the gain has a closed form with eight terms when $a \ne b$:

$$g(a, b) = F(c_{ab} + k) - F(c_{ab}) + F(c_a - k) - F(c_a) + F(c_b - k) - F(c_b) - F(N - k) + F(N).$$

When $a = b$, the two middle differences become $F(c_a - 2k) - F(c_a)$. Choosing the largest gain at each step is a [greedy](/greedy-algorithm/) heuristic: it gives the best single step, and nothing is proved about the final vocabulary.

The encoding input is a word $w$ of $n$ characters and the vocabulary $V$. The output is the list of pieces that greedy longest match first gives, or [UNK].

## The algorithm

Training, with the unigram likelihood gain:

```pseudo id=main
WORDPIECE-TRAIN(C, K)                       ▷ C maps words to counts
L1  for each word w in C do S[w] ← [w1, ##w2, ..., ##wn]
L2  V ← set of all units in S
L3  repeat K times
L4      c ← unit counts, P ← pair counts (both weighted by C)
L5      if P is empty then stop
L6      for each pair (a, b) in P do g(a, b) ← closed-form gain with k = P(a, b)
L7      (a, b) ← pair with the largest g, ties to the smallest pair
L8      in every S[w], replace each occurrence of a b, from the left, by ab
L9      V ← V ∪ {ab}, append (a, b) to the merge list
L10 return V and the merge list
```

Encoding of one word, as in the BERT code:

```pseudo id=encode
WORDPIECE-ENCODE(w, V, maxlen)
E1  if |w| > maxlen then return [UNK]
E2  out ← empty list, start ← 0
E3  while start < |w| do
E4      end ← |w|, piece ← none
E5      while start < end do
E6          sub ← w[start..end), with "##" in front if start > 0
E7          if sub ∈ V then piece ← sub, and leave this loop
E8          end ← end - 1
E9      if piece = none then return [UNK]
E10     append piece to out, start ← end
E11 return out
```

Line L8 scans each word from the left and skips past each replaced pair, so a run such as $\#\#a\ \#\#a\ \#\#a$ gives one merge, not two. The pair count $k$ of line L4 counts the same non-overlapping occurrences, so the gain of line L6 matches the merge of line L8. The encoder of lines E5 to E8 tries the end positions from the right, so the first hit is the longest piece. Positions are 0-based, and $w[i..j)$ is the span $(i, j)$ in fencepost indices: it holds the characters $i + 1$ to $j$.

## Example

Take the counts hug 2, pug 2, pun 2, bun 10 and hugs 10. The first segmentation has $N = 88$ units, with $c(\#\#u) = 26$, $c(\#\#g) = 14$, $c(h) = 12$, $c(\#\#n) = 12$, $c(\#\#s) = 10$, $c(b) = 10$, $c(p) = 4$, and $\mathcal{L} = -161.1137$ nats. The pairs of the first step:

| pair | count $k$ | gain $g$ (nats) |
|---|---|---|
| ##g ##s | 10 | 22.7807 |
| ##u ##g | 14 | 20.6132 |
| h ##u | 12 | 17.1062 |
| ##u ##n | 12 | 17.1062 |
| b ##u | 10 | 13.8333 |
| p ##u | 4 | 5.1095 |

The most frequent pair is ##u ##g, which BPE would merge first. WordPiece merges ##g ##s, because every ##s follows a ##g, so the merge removes the unit ##s and makes the model sharper. The next four merges are ##u ##n, h ##u, b ##un and hu ##gs. In the second step, h ##u and ##u ##n tie at 15.5424, and the tie goes to ##u ##n because "##u" sorts before "h". In the fourth step, b ##un and hu ##gs tie at 20.4682, and the tie goes to b ##un. After five merges, $V$ has 12 units: ##g, ##gs, ##n, ##s, ##u, ##un, b, bun, h, hu, hugs and p.

Encoding "bugs" tries bugs, bug, bu and b, and takes b. At position 1 it tries ##ugs, ##ug and ##u, and takes ##u. At position 2 it takes ##gs at once. The result is b, ##u, ##gs after 8 lookups. The word "gun" gives [UNK], because no unit is a word-initial g. The word "hun" gives hu, ##n, while replaying the merges in order gives h, ##un: the encoder does not reproduce the training segmentation.

## Correctness

Training takes, at each step, the merge with the largest exact gain in the unigram log likelihood: the closed form above counts every unit that the merge changes and no other, because each replacement removes one $a$ and one $b$ and adds one $ab$. The encoder returns, at each position, the longest piece of $V$ that starts there, and its pieces join back into the word. Both proofs, with the loop invariants and the count of lookups, are in proofs/correctness.md. Neither result says that the vocabulary is the best of its size: the greedy choice is a heuristic.

## Complexity

- **Training.** In the word-RAM model, one step recounts the units and the pairs of all distinct words. A word of length $l$ has at most $l - 1$ pairs, and counting the non-overlapping occurrences of one pair costs $O(l)$, so a step costs $O(L m)$ for distinct words of total length $L$ and maximum length $m$. $K$ steps cost $O(K L m)$. Schuster and Nakajima list faster schemes: test only pairs that occur, and update only the counts that a merge changes.
- **Encoding.** For a word of $n$ characters, line E7 runs at most $n(n + 1)/2$ times. Building and hashing a piece of length up to $n$ costs $O(n)$, so the BERT code costs $O(n^3)$ character steps in the worst case, as for the vocabulary {a, ##a} and the word $a^n$. With pieces of length at most $m$ and a [trie](/trie/), the cost is $O(n m)$, and fast WordPiece reaches $O(n)$.
- **Space.** $O(L)$ for the segmentations and the counts, and $O(V m)$ for a vocabulary of $V$ pieces.

## Properties

- **Open vocabulary up to the alphabet.** Every character of the training text is a unit, so any word made only of training characters has an encoding. A word with an unseen character becomes [UNK] as a whole.
- **Not frequency order.** The merge order differs from the BPE order, as the example shows.
- **Gains can be negative.** In the fifth step of the example the pair hu ##g has the gain $-0.0434$. A fixed target size can therefore lower the likelihood near the end; Schuster and Nakajima also stop when the gain falls below a threshold.
- **Greedy encoding.** The encoder is a function of $V$ only, not of the merge order or of the counts. Hugging Face describes WordPiece models that save only the final vocabulary, not the merges.
- **Deterministic.** The same word always gets the same pieces, which is what subword regularization changes.

## Variants and improvements

- **Frequency ratio score.** The Hugging Face course trains with the score $\text{freq}(ab) / (\text{freq}(a)\,\text{freq}(b))$. This is a different heuristic from the likelihood gain above. Google never released its training code, so the exact original criterion is known only from the paper.
- **Word-start marks.** Schuster and Nakajima, and Wu et al. (2016), mark the start of a word with "_" instead of marking the inner pieces with "##".
- **Linear-time encoding.** LinMaxMatch adds failure links and failure pops to the trie of $V$ in the style of [Aho-Corasick](/aho-corasick/); see [fast WordPiece tokenization](/fast-wordpiece-tokenization/).
- **Unigram tokenization.** [Unigram language model tokenization](/unigram-language-model-tokenization/) keeps the likelihood but drops the greedy merges: it prunes a large vocabulary and segments with the Viterbi algorithm.

## When to use it

Use WordPiece when you must match a model trained with it, such as [BERT](/bert/): the vocabulary, the "##" convention, the lowercasing and the [UNK] rule must be the same as at training time. For a new model, byte-level BPE avoids [UNK] entirely, and the unigram method gives several segmentations for regularization.

## Pitfalls

- **[UNK] eats the whole word.** One unknown character, such as a rare symbol or emoji, turns the full word into [UNK], not only that character. This is an [out-of-vocabulary](/out-of-vocabulary-word/) failure at the character level.
- **Two conventions for the mark.** "##" on inner pieces (BERT) and "_" on word starts (Schuster and Nakajima, GNMT) are not interchangeable. Mixing them breaks detokenization.
- **The encoder is not the merge replay.** A word such as "hun" in the example gets different pieces from the two rules. Train and encode with the same rule if the pieces must agree.
- **Pre-tokenization comes first.** The encoder works on single words. The BERT code first splits on whitespace and punctuation (and, for the uncased model, lowercases and strips accents). A different split gives different pieces.
- **Length limit.** The BERT code returns [UNK] for a word of more than 200 characters, so a long URL or a long number loses all its content.

## Implementations

## History

Schuster and Nakajima (2012) introduced word pieces for Japanese and Korean voice search. They grew an inventory of up to 200,000 units by adding, at each step, the pair whose combination most increased the likelihood of a language model on the training data. Wu et al. (2016) used the same wordpiece model for Google's neural machine translation system, with 8,000 to 32,000 wordpieces. Devlin et al. (2019) used a WordPiece vocabulary of 30,000 tokens for BERT, and the BERT code made the "##" prefix and greedy longest-match encoding the common form. Song et al. (2021) gave the linear-time encoder.

## References
