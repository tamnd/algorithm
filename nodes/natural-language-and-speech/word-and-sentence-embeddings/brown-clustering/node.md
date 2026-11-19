---
tag: HG0BRB
kind: algorithm
slug: brown-clustering
name: Brown clustering
aliases:
- Brown clusters
- class-based bigram clustering
area: natural-language-and-speech/word-and-sentence-embeddings
level: core
summary: Greedy agglomerative clustering of words that merges the two classes whose merge least lowers the mutual information of a class bigram model.
model: word-ram
complexity:
  vars: {V: the number of word types (the vocabulary size), N: the number of tokens, C: the number of classes asked for}
  time: {worst: "O(N + V^4)"}
  space: {extra: "Θ(V^2)"}
properties: {deterministic: true, exact: false, greedy: true, online: false, recursive: false}
history:
  year: 1992
  people: [Peter F. Brown, Peter V. deSouza, Robert L. Mercer, Vincent J. Della Pietra, Jenifer C. Lai]
  note: Brown and his colleagues at IBM grouped words into classes for a class-based n-gram language model. Their greedy merge gives a binary tree of the vocabulary, and the paths in that tree later became standard word features.
prereqs: [n-gram-language-model, agglomerative-clustering, pointwise-mutual-information]
see_also: [kullback-leibler-divergence, k-means, word-embedding, named-entity-recognition, dependency-parsing, greedy-algorithm, latent-semantic-analysis, shannon-entropy]
sources:
  - paper: "Peter F. Brown, Peter V. deSouza, Robert L. Mercer, Vincent J. Della Pietra and Jenifer C. Lai, Class-based n-gram models of natural language, Computational Linguistics 18(4), 1992, pages 467 to 479"
    title: Brown, deSouza, Mercer, Della Pietra and Lai 1992
    locator: "Section 3 (Word Classes): equation 9 (the likelihood as minus the entropy plus the average mutual information of adjacent classes), equations 10 to 17 (the merge formula and the bookkeeping that gives order V^3), the word exchange step, the binary tree of Figure 2, and the windowed algorithm used for 1000 classes"
  - paper: "Percy Liang, Semi-Supervised Learning for Natural Language, Master's thesis, Massachusetts Institute of Technology, 2005"
    title: Liang 2005
    locator: the description of Brown clustering with a window of C classes and its use as features
  - paper: "Terry Koo, Xavier Carreras and Michael Collins, Simple semi-supervised dependency parsing, Proceedings of ACL-08: HLT, 2008"
    title: Koo, Carreras and Collins 2008
    locator: prefixes of the Brown bit strings as word features of a dependency parser
  - paper: "Joseph Turian, Lev Ratinov and Yoshua Bengio, Word representations: a simple and general method for semi-supervised learning, Proceedings of ACL 2010"
    title: Turian, Ratinov and Bengio 2010
    locator: Brown clusters compared with word embeddings as features for chunking and named entity recognition
---

Brown clustering puts the words of a vocabulary into classes by greedy [agglomerative clustering](/agglomerative-clustering/). It starts with one class per word. At each step it merges the two classes whose merge loses the least average mutual information between the classes of adjacent words, which is the same as keeping the likelihood of a class bigram [language model](/n-gram-language-model/) as high as possible. If the merging goes on to one class, the merges form a binary tree, and the path from the root to a word is a bit string that serves as a word feature. Unlike [k-means](/k-means/) or a generic agglomerative clustering, the objective is not a distance between points: it is the information that one class carries about the class of the next word.

## In plain words

Words that can appear in the same places in a sentence should go in the same group. "Cat" and "dog" both come after "the" and before "runs", so a model that predicts the group of the next word loses almost nothing if it cannot tell them apart.

The method begins with every word alone. Then it tries every pair of groups, asks how much prediction power the merge would cost, and does the cheapest merge. It repeats this until the number of groups you asked for is left. If you keep going to one group, the order of the merges makes a family tree of the words. Each word gets a code of zeros and ones that says how to walk down the tree to it. Words with a long common prefix are close in the tree.

## The problem

The input is a corpus, a list of sentences of word tokens, and a number of classes $C \ge 1$. The bigrams are the adjacent token pairs inside each sentence, with no padding, and $n(u, w)$ counts the pair $(u, w)$; let $B$ be the total number of bigrams. A partition $\pi$ of the $V$ word types into classes gives class counts $n(l, m)$, the probabilities $p(l, m) = n(l, m) / B$, and the marginals $p_L(l) = \sum_m p(l, m)$ and $p_R(m) = \sum_l p(l, m)$. The average mutual information (AMI) of $\pi$ is

$$ I(\pi) = \sum_{l, m} p(l, m) \log \frac{p(l, m)}{p_L(l)\, p_R(m)} \quad (\log = \ln,\ \text{nats}), $$

which is the expected [pointwise mutual information](/pointwise-mutual-information/) of the class of a word and the class of the next word, or the [Kullback-Leibler divergence](/kullback-leibler-divergence/) of $p$ from $p_L \times p_R$. Brown et al. (equation 9) show that the log likelihood per bigram of the class bigram model $P(w \mid u) = P(c(w) \mid c(u)) P(w \mid c(w))$, with relative frequency parameters, is $I(\pi)$ minus an entropy that does not depend on $\pi$. So the best partition into $C$ classes is the one with the largest $I$. Brown et al. give no exact method for it, and Brown clustering is a greedy heuristic for it.

## The algorithm

Write $q(l, m) = p(l, m) \log \frac{p(l, m)}{p_L(l) p_R(m)}$, with $q = 0$ when $p(l, m) = 0$, and $s(i) = \sum_l q(l, i) + \sum_m q(i, m) - q(i, i)$, the part of $I$ in row $i$ and column $i$. For a merge of $i$ and $j$, write $i{+}j$ for the merged class, and $q(\cdot, i{+}j)$ for the value computed from the summed counts and the summed marginals.

```pseudo id=main
BROWN-CLUSTERING(corpus, C)
L1  V ← word types by decreasing count; class i ← {V[i]}
L2  n(l, m) ← count of the adjacent pairs of classes (l, m) in each sentence
L3  k ← |V|
L4  while k > C do
L5      compute p_L, p_R, q(l, m), s(l) and I ← sum of all q(l, m)
L6      for each pair i < j of current classes do
L7          I(i, j) ← I - s(i) - s(j) + q(i, j) + q(j, i) + q(i+j, i+j) + Σ_{l ≠ i, j} [q(l, i+j) + q(i+j, l)]
L8      (i, j) ← the pair with the largest I(i, j), the first pair on ties
L9      add row j to row i and column j to column i; delete row and column j
L10     record the merge (i, j); k ← k - 1
L11 return the k classes and the merges
```

Line L7 is equation 15 of Brown et al. It gives the AMI after the merge in $O(k)$ time, because the merge changes only the cells in rows and columns $i$ and $j$. Line L9 keeps the merged class at position $i$. The code breaks ties within $10^{-12}$ in favor of the first pair, so that rounding does not decide them.

**The tree and the bit strings.** Run the loop with $C = 1$. Each merge makes a tree node with the kept class $i$ as left child and the removed class $j$ as right child. The bit string of a word is the path from the root, 0 for left and 1 for right. Undoing the last $C$ merges gives the partition into $C + 1$ classes, and a prefix of length $b$ of the bit strings groups the words into at most $2^b$ clusters.

## Example

The corpus is one sentence of 15 tokens: "the cat runs and the dog sleeps and a dog runs and the cat sleeps". It has 14 bigrams and $V = 7$ types, ordered by count as and, the, cat, dog, runs, sleeps, a. The bigram counts are (row = first word):

| | and | the | cat | dog | runs | sleeps | a |
| --- | --- | --- | --- | --- | --- | --- | --- |
| and | 0 | 2 | 0 | 0 | 0 | 0 | 1 |
| the | 0 | 0 | 2 | 1 | 0 | 0 | 0 |
| cat | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| dog | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| runs | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| sleeps | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| a | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

The AMI of the partition into single words is 1.4377 nats. The merges, with the AMI after each one:

| step | classes before | merge | AMI after | loss |
| --- | --- | --- | --- | --- |
| 1 | 7 | runs + sleeps | 1.4377 | 0.0000 |
| 2 | 6 | the + a | 1.3761 | 0.0616 |
| 3 | 5 | cat + dog | 1.3761 | 0.0000 |
| 4 | 4 | and + {the, a} | 0.7375 | 0.6385 |
| 5 | 3 | {and, the, a} + {runs, sleeps} | 0.1175 | 0.6200 |
| 6 | 2 | all + {cat, dog} | 0.0000 | 0.1175 |

Step 1 loses nothing because "runs" and "sleeps" have proportional rows (both are followed only by "and") and equal columns (both follow "cat" once and "dog" once). Merging two classes with proportional rows and proportional columns never changes $I$. At step 2 the pairs (the, a) and (cat, dog) tie at 1.3761, and the tie rule takes (the, a) because it comes first in the order of line L6. After it, "cat" and "dog" have equal rows and proportional columns, so step 3 is free. Step 4 is again a tie, between "and" with {the, a} and "and" with {runs, sleeps}. With $C = 3$ the algorithm stops after step 4 with {and, the, a}, {cat, dog} and {runs, sleeps}. The full tree gives the bit strings and 000, the 0010, a 0011, runs 010, sleeps 011, cat 10 and dog 11.

## Correctness

The claim is that each merge joins the pair of classes whose merge gives the largest AMI among all pairs, and that the loop stops with $\min(C, V)$ classes. The key step is the merge formula of line L7: a merge leaves every cell outside rows and columns $i$ and $j$ unchanged, together with its marginals, and the cells inside are counted by $s(i) + s(j) - q(i, j) - q(j, i)$. The invariant of the loop is that the matrix $n$ holds the class bigram counts of the current partition, which line L9 keeps. By the likelihood identity of Brown et al., each step also gives the class bigram model of the highest likelihood among the partitions one merge away. The full proof, with the likelihood identity, is below.

The claim is about one step. The sequence of greedy merges does not find the best partition in general (see Pitfalls).

## Complexity

The model is the [word-RAM](/word-ram/), with the arithmetic on floating point numbers counted as unit cost.

- **Counting.** Line L2 reads each token once: $O(N)$ time and $\Theta(V^2)$ space for the dense matrix.
- **One merge with $k$ classes.** Line L5 costs $O(k^2)$. Lines L6 to L8 evaluate $k(k-1)/2$ pairs at $O(k)$ each, so $O(k^3)$. Line L9 costs $O(k^2)$ with a dense matrix stored as lists.
- **All merges.** From $k = V$ down to $C + 1$ the cost is $\sum_k O(k^3) = O(V^4)$, so the total is $O(N + V^4)$ for the version on this page.
- **Better bookkeeping.** Brown et al. keep the table of the losses $I - I(i, j)$ for all pairs and update it after each merge with their equation 17 in $O(k^2)$ time, which gives $O(V^3)$ in all (page 473). Recomputing $I$ from scratch for each pair would cost $O(k^2)$ per pair and $O(V^5)$ in all, the cost they give for the straightforward method.
- **Windowed version.** With only $C + 1$ active classes at a time (see Variants), each step has $O(C^2)$ pairs, so the cost is about $O(V C^2)$ with the bookkeeping, plus the counting. This bound is our count, not a figure of the paper.

## Properties

- **Greedy and deterministic.** The result depends on the order of the words through the tie rule, and on nothing random.
- **Hard clustering.** Each word type gets exactly one class and one bit string. The different senses of an ambiguous word share them.
- **Hierarchical.** One run to $C = 1$ gives the partitions for every number of classes at once, nested in each other.
- **Monotone AMI.** A merge never increases $I$, because merging classes is a function of the class variables and mutual information cannot grow under such a function (data processing). So the losses are never negative, up to rounding.
- **Not optimal.** The final partition need not have the largest $I$ among the partitions into $C$ classes.

## Variants and improvements

- **Word exchange.** After the $V - C$ merges, Brown et al. move single words to the class that gives the largest AMI, one at a time, until no move helps. This is a [local search](/local-search/) step after the greedy start.
- **Windowed clustering.** Put the $C$ most frequent words in their own classes. At each step, add the next most frequent word as a new class and merge the best pair among the $C + 1$ classes. Brown et al. used this to put a vocabulary of 260,741 words into 1000 classes. The implementation of Liang 2005 works this way and is the one most later work uses.
- **Bit string features.** Koo, Carreras and Collins 2008 and others use prefixes of several lengths of the bit strings, together with the full strings, as features of a parser or a tagger. A short prefix gives a coarse class and a long prefix a fine one.

## When to use it

Use Brown clusters when you need cheap word features learned from unlabeled text for a tagger, a [named entity recognizer](/named-entity-recognition/) or a [parser](/dependency-parsing/) trained on little labeled data; Turian, Ratinov and Bengio 2010 compared them with [word embeddings](/word-embedding/) as features for chunking and named entity recognition and found them competitive, a measurement on their data sets. Use dense embeddings when you need graded similarity or one vector per word for a network. The method models only the next word, so it captures syntactic classes well and topical similarity less well than a [word-context matrix](/word-context-matrix/) with a wide window.

## Pitfalls

- **Recomputing the AMI for each pair.** Computing $I(\pi')$ from scratch in line L7 is correct but costs $O(k^2)$ per pair and $O(V^5)$ in all. Use the merge formula of line L7, and the loss table of Brown et al. for $O(V^3)$.
- **Greedy is not optimal.** On the one-sentence corpus "e a d b c a" the first two merges are unique (c with e, then b with d), and the third is a tie whose two choices both give $I = 0.1185$ for two classes. The partition {a, b}, {c, d, e} has $I = 0.6730$. Line L8 chooses only the best next merge, and no later step undoes a merge.
- **Sentence edges.** Line L2 counts pairs inside sentences. A word seen only at the end of sentences has an empty row, and a word seen only at the start has an empty column, so merging such a pair costs nothing, even if the words have nothing in common. On "the cat runs", "the dog runs", "a cat sleeps", "a dog sleeps", "the dog sleeps" the first merge is "sleeps" with "the". Pad the sentences with boundary symbols or join them into one stream when this matters.
- **Ties decided by rounding.** Two merges with the same exact AMI can differ by $10^{-16}$ after rounding. Compare with a tolerance in line L8, or the order of the floating point sums decides the tie.
- **The log base.** Nats and bits change all values of $I$ by the same factor and do not change any choice. Say which one you print.

## Implementations

## History

Brown, deSouza, Mercer, Della Pietra and Lai built class-based n-gram models at IBM, published in Computational Linguistics in 1992. They derived the link between the likelihood of the class bigram model and the AMI, gave the greedy merge with the bookkeeping that costs order $V^3$, the word exchange step, the binary tree with a figure for 1000 words, and the windowed version. Liang 2005 wrote the implementation with a window that most later work used. Miller, Guinness and Zamanian 2004 and Koo, Carreras and Collins 2008 used bit string prefixes as features for name tagging and dependency parsing, and Turian, Ratinov and Bengio 2010 compared these features with neural word embeddings.

## References
