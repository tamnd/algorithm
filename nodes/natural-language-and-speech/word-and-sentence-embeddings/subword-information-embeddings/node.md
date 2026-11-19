---
tag: 3998JC
kind: algorithm
slug: subword-information-embeddings
name: Subword information skip-gram
aliases:
- fastText embeddings
- character n-gram embeddings
area: natural-language-and-speech/word-and-sentence-embeddings
level: advanced
summary: Skip-gram in which a word vector is the sum of the vectors of its character n-grams, so rare and unseen words still get vectors.
model: real-ram
complexity:
  vars: {N: "the number of tokens in the corpus", C: "the window radius", k: "the number of noise words per pair", G: "the largest number of n-grams of a word", d: "the dimension of the vectors", T: "the number of epochs", B: "the number of hash buckets", V: "the vocabulary size, the number of types"}
  time: {worst: "O(T N C (k + G) d)"}
  space: {extra: "O((V + B) d)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2017
  people: [Piotr Bojanowski, Edouard Grave, Armand Joulin, Tomas Mikolov]
  note: "Bojanowski, Grave, Joulin and Mikolov at Facebook AI Research published the model in 2017 (a preprint appeared in 2016) and released it in the fastText library."
prereqs: [skip-gram-model, negative-sampling, fnv-hash]
see_also: [word-embedding, subword-tokenization, byte-pair-encoding, hash-collision, universal-hashing, glove, word-analogy, continuous-bag-of-words]
sources:
  - paper: "Piotr Bojanowski, Edouard Grave, Armand Joulin and Tomas Mikolov, Enriching word vectors with subword information, Transactions of the Association for Computational Linguistics 5, 2017, pages 135 to 146"
    title: Bojanowski, Grave, Joulin and Mikolov 2017
    locator: "Section 3 (the skip-gram model with negative sampling, and the subword model: the boundary symbols < and >, the n-grams for n from 3 to 6, the word itself in its set of n-grams, the score as a sum over the n-grams, and the FNV-1a hash into 2 million buckets), Section 4 (the training settings), and the experiments on words outside the vocabulary"
  - paper: "Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado and Jeffrey Dean, Distributed representations of words and phrases and their compositionality, Advances in Neural Information Processing Systems 26 (NIPS 2013), pages 3111 to 3119, arXiv:1310.4546"
    title: Mikolov, Sutskever, Chen, Corrado and Dean 2013
    locator: the skip-gram model with negative sampling that the subword model extends
---

The subword information skip-gram learns word vectors from the character n-grams inside each word. A word is the set of its character n-grams, for $n$ from 3 to 6, taken from the word with a boundary symbol added at each end, plus the word itself. Each n-gram has its own vector, and the vector of the word is the sum of the vectors of its n-grams. The model is then trained like the [skip-gram model](/skip-gram-model/) with [negative sampling](/negative-sampling/). Words that share pieces, such as "walk", "walked" and "walking", share parameters, so rare words get better vectors, and a word never seen in training still gets a vector from its n-grams. Bojanowski, Grave, Joulin and Mikolov (2017) proposed it and released it in the fastText library. To keep the memory fixed, the n-grams are hashed into a fixed number of rows.

## In plain words

A normal word vector model learns one vector per word and knows nothing about a word it has never seen. It also learns "walking" and "walked" as two unrelated words.

This method looks inside the word. It cuts the word into short overlapping pieces of three to six letters, with a marker for the start and the end of the word, and it learns a vector for each piece. The vector of a word is the sum of the vectors of its pieces and of the word itself.

Training is the same game as in skip-gram: tell real neighbor words from random ones. Because related words share pieces, what the model learns from one helps the others. A new word, such as a misspelling or a rare form, gets a vector from the pieces it shares with known words.

## The problem

The input is a corpus of $N$ tokens, the window radius $C$, the number $k$ of noise words, the dimension $d$, the n-gram lengths from $n_{\min}$ to $n_{\max}$ and the number $B$ of hash buckets. For a word $w$, let $\mathcal{G}_w$ be the list of the rows of the input matrix $Z$ that belong to $w$: the row of $w$ itself if $w$ is in the vocabulary, and the row $|V| + (\mathrm{hash}(g) \bmod B)$ of each character n-gram $g$ of the string "<" $w$ ">". The score of a word $w$ and a context word $c$ is

$$s(w, c) = \sum_{g \in \mathcal{G}_w} \vec z_g \cdot \vec v_c = \Big(\sum_{g \in \mathcal{G}_w} \vec z_g\Big) \cdot \vec v_c,$$

and the loss of an observed pair with noise words $n_1, \ldots, n_k$ is the negative sampling loss $-\log\sigma(s(w, c)) - \sum_i \log\sigma(-s(w, n_i))$. The output is $Z$, from which any word, seen or not, gets the vector $\sum_{g \in \mathcal{G}_w} \vec z_g$.

The boundary symbols make prefixes and suffixes different from the same letters inside a word: the word "her" is the sequence "<her>", which differs from the trigram "her" of "where". The paper uses $n$ from 3 to 6 and $B = 2$ million, and hashes with the [FNV-1a hash](/fnv-hash/).

## The algorithm

```pseudo id=main
SUBWORD-SKIP-GRAM(corpus, C, k, d, T, η, n_min, n_max, B)
L1  for each word w: G_w ← its own row, then |V| + FNV-1a(g) mod B for each n-gram g of <w>
L2  Z ← small uniform random values, (|V| + B) rows; the context vectors v ← 0
L3  for each epoch and each window pair (w, c) with noise words n_1..n_k do h ← Σ_{g ∈ G_w} z_g
L4      for each (x, y) in (c, 1), (n_1, 0), ..., (n_k, 0) do
L5          s ← h · v_x
L6          e ← σ(s) - y
L7          g_h ← g_h + e v_x; v_x ← v_x - η e h
L8      for each g in G_w do z_g ← z_g - η g_h          ▷ every n-gram row gets the same step
L9  return the vector Σ_{g ∈ G_w} z_g for any word w
```

Line L1 builds the list of rows of each word once. Line L2 makes one row for each word of the vocabulary and one for each bucket; buckets that no n-gram reaches stay at their random start and are never used. Lines L3 to L7 are the [negative sampling](/negative-sampling/) step with the sum $\vec h$ in place of the word vector. Since $s$ depends on the rows of $\mathcal{G}_w$ only through their sum, the gradient with respect to each of them is the same vector $\vec g_h$, and line L8 applies it to every row. A row that occurs twice in $\mathcal{G}_w$ gets the step twice. Line L9 works for a word outside the vocabulary: its list has no own row, only the n-gram rows.

## Example

The word "where" becomes "<where>". Its 14 n-grams, by start position, are

<wh, <whe, <wher, <where, whe, wher, where, where>, her, here, here>, ere, ere>, re>

and with its own row, "where" has 15 rows. Its trigrams are <wh, whe, her, ere and re>, the example of Bojanowski et al. A word of $m$ characters has $\sum_{n=3}^{6} \max(0, m + 3 - n)$ n-grams, so a long word has about $4m$.

The hash maps each n-gram to a bucket. With the sign quirk of the library described under Pitfalls, FNV-1a gives

| n-gram | FNV-1a (hex) | bucket for $B = 2{,}000{,}000$ |
|---|---|---|
| <wh | 3e79c4e4 | 167652 |
| whe | 34f43a4d | 420941 |
| her | f4b48d8c | 1473420 |
| ere | 7b978ac9 | 1529033 |
| re> | 7af4dc2a | 867498 |
| <her> | 65814d14 | 972692 |

The trigram "her" of "where" and the word "her" (the sequence <her>) get different rows. The word "her" also has the trigram "her" (from "<her>"), so the two words share that row.

On a planted corpus whose words in one group all start with "pak" and in the other with "zot", trained with n-grams of length 3 and 4, the unseen word "pakar" gets a vector closer to the mean of the "pak" group than to the mean of the "zot" group, through the shared n-grams "<pa", "<pak" and "pak".

## Correctness

The claims are about what each line computes; the training itself has no guarantee of a global optimum. Line L1 lists exactly the substrings of "<" $w$ ">" of length $n_{\min}$ to $n_{\max}$, one per start position and length, and maps each to a row in $[|V|, |V| + B)$. Lines L5 to L8 compute the exact gradient of the negative sampling loss of the pair, because $s(w, x) = \vec h \cdot \vec v_x$ and $\partial \vec h / \partial \vec z_g$ is the identity for each occurrence of $g$ in $\mathcal{G}_w$. The vector of line L9 is defined for every word with at least one character, because "<" $w$ ">" then has length at least 3 and so at least one trigram. The full proof is in the proof file.

## Complexity

Line L1 costs $O(m)$ per n-gram for the hash, so $O(G m)$ per word of length $m$, once. Each window pair costs $O(G d)$ for the sum $\vec h$, $O((k + 1) d)$ for lines L4 to L7 and $O(G d)$ for line L8. A pass emits $O(NC)$ pairs, so the training costs $O(TNC(k + G)d)$, about $(k + G)/(k + 1)$ times the cost of plain skip-gram with negative sampling. The memory is $(|V| + B)\,d$ numbers for $Z$ and $|V|\,d$ for the context vectors; with $B = 2$ million and $d = 300$, $Z$ has at least 600 million numbers, whatever the vocabulary.

## Properties

- **Vectors for unseen words.** Any word with at least one character has a vector, built from the hashed n-grams it shares with the training words.
- **Fixed memory.** The number of rows does not grow with the number of distinct n-grams. Different n-grams can share a bucket ([hash collision](/hash-collision/)), which adds noise but bounds the memory.
- **Shared parameters.** Words with common prefixes, suffixes or stems share rows, so frequent forms help rare ones. This matters most for languages with rich morphology.
- **Randomized.** The start, the noise words and the order of the data are random.
- **Contains skip-gram.** With no n-grams ($n_{\min} > n_{\max}$), $\mathcal{G}_w$ is the word's own row and the model is skip-gram with negative sampling.

## Variants and improvements

- **Mean instead of sum.** The fastText library divides the sum by $|\mathcal{G}_w|$ when it builds $\vec h$; the paper defines the score with the plain sum. The mean keeps the scale of $\vec h$ the same for short and long words.
- **CBOW with n-grams.** The library also trains a [continuous bag-of-words](/continuous-bag-of-words/) model whose input is the n-gram rows of all the context words.
- **Other units.** The n-grams can be replaced by morphemes or by subword units from [byte-pair encoding](/byte-pair-encoding/) or other [subword tokenizations](/subword-tokenization/).
- **Bucket count and lengths.** A smaller $B$ saves memory and adds collisions. Shorter n-gram ranges, such as 3 to 3, reduce the cost per word.

## When to use it

Use it when the text has many rare words, many word forms or many words not seen in training: languages with rich morphology, social media text with misspellings, or technical text with compounds. On frequent words of English the gain over plain [skip-gram](/skip-gram-model/) is small, and the model is slower and needs memory for the buckets. When no vector is needed for unseen words and the vocabulary is small, plain skip-gram or [GloVe](/glove/) is simpler.

## Pitfalls

- **Missing boundary symbols.** Line L1 must take the n-grams of "<" $w$ ">", not of $w$. Without the symbols, prefixes and suffixes are not marked, and a short word such as "a" has no n-gram at all.
- **Signed bytes in the hash.** The fastText library reads each byte as a signed char before the XOR, so bytes 128 to 255 (every non-ASCII character in UTF-8) are sign extended to 32 bits. Standard FNV-1a does not do this. For "é" the library gives 3cfa68c1 and standard FNV-1a gives 1e9de8c1, so a reimplementation that uses the standard hash cannot load vectors trained by the library for non-ASCII n-grams.
- **Offset of the buckets.** Line L1 adds $|V|$ to the bucket number. Without the offset, n-grams share rows with whole words.
- **Updating each row with its own gradient.** Line L8 must give every row of $\mathcal{G}_w$ the same step $\eta \vec g_h$, computed before any row changes. Computing $\vec h$ again after each row update gives a different, wrong step.
- **Sum against mean.** Vectors from the library are means, not sums. Mixing the two conventions changes the norms of all vectors, which matters for dot products though not for cosines.

## Implementations

## History

Character-level information had been added to word vectors before, for example through morphological segmentation, but Bojanowski, Grave, Joulin and Mikolov made it simple and fast: a bag of hashed character n-grams added to skip-gram. Their preprint appeared in 2016, the year the fastText library was released, and the TACL paper followed in 2017. Facebook later released pretrained fastText vectors for many languages.

## References
