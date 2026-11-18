---
tag: ZZH1HW
kind: algorithm
slug: bpe-dropout
name: BPE-dropout
aliases:
- byte-pair encoding dropout
area: natural-language-and-speech/tokenization-and-text-normalization
level: research
summary: Apply the BPE merges in order but skip each candidate merge with probability p at training time, which yields random segmentations of each word.
solves: [text-tokenization]
model: word-ram
complexity:
  vars: {n: the length of the word in characters, K: the number of merges in the table}
  time: {sample: O(n^2)}
  space: {sample: O(n), table: O(K)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2020
  people: [Ivan Provilkov, Dmitrii Emelianenko, Elena Voita]
  note: Provilkov, Emelianenko and Voita showed that the BPE merge table alone can give many segmentations of a word, and that training on them improves translation.
prereqs: [byte-pair-encoding, subword-tokenization, dropout]
see_also: [subword-regularization, unigram-language-model-tokenization, byte-level-bpe, wordpiece, data-augmentation, machine-translation, transformer, ancestral-sampling]
sources:
  - paper: doi:10.18653/v1/2020.acl-main.170
    title: Ivan Provilkov, Dmitrii Emelianenko and Elena Voita, BPE-dropout, Simple and effective subword regularization, ACL 2020, pages 1882 to 1892
    locator: Section 2.1 (BPE segmentation), Section 3 and Algorithm 1 with footnote 1 (page 1884), Table 1 (the values of p), Section 4.2 (vocabularies), and the abstract (the BLEU gains)
  - paper: doi:10.18653/v1/P18-1007
    title: Taku Kudo, Subword regularization, Improving neural network translation models with multiple subword candidates, ACL 2018, pages 66 to 75
    locator: the method that BPE-dropout is compared with (a unigram language model with sampling)
  - paper: doi:10.18653/v1/P16-1162
    title: Rico Sennrich, Barry Haddow and Alexandra Birch, Neural machine translation of rare words with subword units, ACL 2016
    locator: the merge table and the segmentation procedure of BPE
---

BPE-dropout is a way to get many different segmentations of the same word from one [byte-pair encoding](/byte-pair-encoding/) merge table. It segments a word as BPE does, but at each step it drops each possible merge at random with probability $p$, so the word stops at a random level of detail. A model is trained on these random segmentations and is then used with plain BPE. It is a form of [subword regularization](/subword-regularization/) that needs no new tokenizer.

## In plain words

Plain BPE always cuts a word the same way. A model then sees "unrelated" as the same few pieces every time and never learns that the pieces of a rare word mean the same as the pieces inside a common one.

BPE-dropout cuts words with the usual list of gluing rules, but at each step it forgets some of the rules for that step, at random. A word sometimes comes out as one piece, sometimes as smaller pieces, and sometimes as single letters. During training, the model sees many cuts of each word and learns how the pieces fit together. When the model is used, the forgetting is turned off, so the cut is the normal one.

## The problem

The input is a word $w$ of $n$ characters, a merge table (a list of pairs of units, where an earlier pair has a higher priority) and a probability $p$. The output is a random segmentation of $w$ into units, that is, a list of strings that joins back to $w$. With $p = 0$ the output must be the plain BPE segmentation, and with $p = 1$ it must be the list of characters. Provilkov et al. describe the plain BPE segmentation as: split the word into characters, then merge the adjacent pair of highest priority, and repeat until no pair of the table is left.

## The algorithm

Algorithm 1 of Provilkov et al., with the rule of their footnote 1 that each occurrence of a merge is dropped on its own:

```pseudo id=main
BPE-DROPOUT(w, merges, p)
L1  u ← the characters of w
L2  repeat
L3      O ← the positions i where (u_i, u_{i+1}) is a pair of merges
L4      remove each position from O, independently, with probability p
L5      if O is empty then return u
L6      (a, b) ← the pair of highest priority at a position in O
L7      join a b at the positions of O that hold (a, b), from the left, skipping overlaps
```

The run stops as soon as all occurrences of one pass are dropped, even if a later pass could have merged something. Line L7 joins all kept occurrences of the chosen pair, as plain BPE joins all occurrences. For a pair such as (a, a) in "aaa", the two occurrences overlap; line L7 takes the left one when both are kept. The Sennrich et al. code adds an end-of-word symbol to each word before segmenting; this page leaves it out to keep the example short.

## Example

Learn 6 merges from the counts low 5, lower 2, newest 6 and widest 3. Plain BPE gives the table (e, s), (es, t), (l, o), (lo, w), (e, w), (ew, est), in this order of priority, and segments "lowest" as low, est.

With $p = 0.1$, the word "low" has one occurrence at the start, (l, o). It is dropped with probability 0.1, and the run returns l, o, w. Otherwise lo, w is formed, and the occurrence (lo, w) is dropped with probability 0.1, which returns lo, w with probability $0.9 \cdot 0.1 = 0.09$. The rest, 0.81, gives low.

The word "lowest" has 9 possible outputs. Their exact probabilities, from enumerating every pattern of drops:

| segmentation | probability |
|---|---|
| low est | 0.807003 |
| lo w est | 0.08748 |
| l o w est | 0.081 |
| l o w e s t | 0.01 |
| l o w es t | 0.009 |
| low es t | 0.002187 |
| lo w es t | 0.00162 |
| lo w e s t | 0.0009 |
| low e s t | 0.00081 |

The first pass sees (l, o) and (e, s); both are dropped with probability $0.1 \cdot 0.1 = 0.01$, which is the row of single characters. With $p = 0.5$ the plain segmentation low, est has probability 0.171875, and the single characters have 0.25.

## Correctness

Each pass that does not stop joins at least one pair, and a join keeps the characters, so the run stops after at most $n - 1$ joins and returns a segmentation of $w$ into characters and joined pairs of the table. With $p = 0$ nothing is dropped, so each pass merges the pair of highest priority at all its occurrences, which is plain BPE; with $p = 1$ the first pass stops. The law of the output is a sum over the patterns of drops at the first pass, which the code evaluates exactly with rational numbers; the tests check the sampled frequencies against it. These are theorems, proved in proofs/correctness.md. That the random segmentations help a model is a measurement, not a theorem.

## Complexity

In the word-RAM model with a hash table for the ranks, one pass costs $O(n)$ to list the occurrences, draw the drops and join, and there are at most $n$ passes, so one sample costs $O(n^2)$ time and $O(n)$ space. Plain BPE has the same bound. The rank table takes $O(K)$ space. A sample is drawn every time a word is seen in training, so this cost is paid in each epoch, unlike plain BPE, whose output can be cached.

## Properties

- **The same vocabulary.** No new unit is created: every output unit is a character or a unit of the BPE table, so the model and its vocabulary stay as for BPE. Provilkov et al. keep the vocabulary of plain BPE; a unit that appears only through dropout then becomes an unknown token, which is rare (Section 4.2).
- **A tunable level of detail.** The value of $p$ moves the output between the BPE segmentation and the characters.
- **Not a product law.** The probability of a segmentation is not a product of one factor per merge. One dropped pass can end the run, as the row l, o, w, e, s, t shows.
- **Measured gains.** Provilkov et al. report gains of up to 2.3 BLEU over BPE and up to 0.9 BLEU over the subword regularization of Kudo (2018), on their translation tasks. They usually use $p = 0.1$, and $p = 0.6$ for Chinese and Japanese (Table 1).

## Variants and improvements

- **Unigram sampling.** Kudo's [subword regularization](/subword-regularization/) samples from a [unigram language model](/unigram-language-model-tokenization/) of the pieces. It needs that model, while BPE-dropout needs only the merge table.
- **Byte level.** The same drops apply to the merges of [byte-level BPE](/byte-level-bpe/).
- **Choice of p.** A larger $p$ gives finer pieces. A language with many characters, where BPE units are long, may need a larger $p$, as Table 1 of the paper shows.

## When to use it

Use it when you train a model on text segmented by BPE and want the effect of subword regularization without changing the tokenizer, for example in [machine translation](/machine-translation/) with a [transformer](/transformer/). Turn it off ($p = 0$) at test time. It is a kind of [data augmentation](/data-augmentation/): it changes the input, not the model.

## Pitfalls

- **Dropout at test time.** Inference must use $p = 0$. Random segmentations at test time make the output random and usually worse.
- **Per occurrence, not per pair.** Dropping a pair type for the whole word at once is a different law. Footnote 1 of the paper drops each occurrence on its own.
- **Stopping early.** A pass that keeps no occurrence ends the run. An implementation that skips such a pass and goes on with the next one gives a different, coarser law.
- **Vocabulary.** Units that only dropout produces may be missing from a vocabulary built from plain BPE output, and become unknown tokens.

## Implementations

## History

Kudo (2018) introduced subword regularization with a unigram language model, and noted that plain BPE gives only one segmentation per word. Provilkov, Emelianenko and Voita (2020) showed that the BPE merge table already allows many segmentations: dropping merges at random, in the spirit of [dropout](/dropout/) in neural networks, gives them without a second model.

## References
