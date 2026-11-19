---
tag: XMKHK7
kind: algorithm
slug: biaffine-dependency-parser
name: Biaffine dependency parser
aliases:
- deep biaffine attention parser
area: natural-language-and-speech/natural-language-parsing
level: research
summary: "Score each head-dependent pair by a biaffine product of BiLSTM vectors, then decode the best tree under those arc scores."
solves: [dependency-parsing]
model: word-ram
complexity:
  vars: {n: "the number of words", k: "the size of the head and dependent vectors", r: "the size of the encoder vectors"}
  time: {worst: O(n^2 k + n k (k + r) + n^3), best: Θ(n^2 k + n k (k + r))}
  space: {extra: Θ(n^2 + n k)}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 2017
  people: [Timothy Dozat, Christopher D. Manning]
  note: "Dozat and Manning (2017) scored every head-dependent pair with a biaffine product of two small views of BiLSTM vectors, trained each word's head choice as a softmax classification, and decoded a tree from the scores."
prereqs: [mst-dependency-parsing, cross-entropy-loss]
see_also: [chen-manning-parser, edmonds-arborescence, eisner-algorithm, multiplicative-attention, bilstm-crf, elmo, bert, matrix-tree-theorem]
sources:
  - url: https://arxiv.org/abs/1611.01734
    title: "Timothy Dozat and Christopher D. Manning, Deep biaffine attention for neural dependency parsing, ICLR 2017"
    locator: "the head and dependent MLP views, the biaffine arc scorer with its head prior term, the label classifier, the softmax training of heads, and the decoding of a well-formed tree"
  - url: https://aclanthology.org/H05-1066/
    title: "Ryan McDonald, Fernando Pereira, Kiril Ribarov and Jan Hajič, Non-projective dependency parsing using spanning tree algorithms, HLT-EMNLP 2005"
    locator: "graph-based parsing with arc scores and the maximum spanning arborescence by Chu-Liu-Edmonds"
---

The biaffine dependency parser of Dozat and Manning (2017) is a graph-based parser. A bidirectional LSTM reads the sentence and gives one vector for each word and for the root. Two small feedforward layers turn each vector into a *head view* $a_i$ and a *dependent view* $e_i$, and a biaffine function $s(h, d) = a_h^\top U e_d + a_h^\top u$ scores every possible arc $h \to d$ at once, as one matrix product. In training, each word chooses its head by a softmax over all other words and the root, with a [cross-entropy loss](/cross-entropy-loss/). At test time the parser takes the tree with the highest total arc score: the best head of each word when these heads already form a tree, and otherwise the maximum spanning arborescence of [MST parsing](/mst-dependency-parsing/). A second biaffine classifier then gives each arc its label. The parser is simple, fast on a GPU, and was the most accurate on the standard English and Chinese benchmarks when it appeared.

## In plain words

First, a network reads the whole sentence in both directions, so each word gets a list of numbers that knows about its context. From that list, two small layers make two short lists for each word: one that says what the word is like as a head, and one that says what it is like as a child. To score "word h is the head of word d", the parser multiplies h's head list, a learned table, and d's child list. Every word looks at all the others and gives each a chance to be its head. In training, the parser learns to give the true head the highest chance. To parse, each word takes its best head; if this makes a loop, a spanning tree method fixes it. Then each word picks the best label for the link to its head.

## The problem

The input is a sentence $w_1 \cdots w_n$, and the encoder output vectors $r_0, r_1, \ldots, r_n$, with $r_0$ for the root. The output is a labeled [dependency tree](/dependency-tree/), with crossing arcs allowed. The root may have several children; if the treebank needs one root child, the decoder must add that constraint.

The code on this site takes the network outputs, the vectors $r_i$ and the weights, as given. It implements the views, the arc and label scores, the head loss with its gradients in $U$ and $u$, and the decoder; it does not train a network or run an LSTM.

## The algorithm

**Views and scores.** For each $i = 0, \ldots, n$,

$$a_i = \mathrm{ReLU}(W_a r_i + b_a), \qquad e_i = \mathrm{ReLU}(W_e r_i + b_e),$$

$$s(h, d) = a_h^\top U e_d + a_h^\top u.$$

In matrix form, with the views as the rows of $A$ and $E$, the score matrix is $S = A U E^\top + A u \mathbf{1}^\top$. The first term is a bilinear form, as in [multiplicative attention](/multiplicative-attention/). The second depends on the head only and adds a constant to row $h$: it is a prior on how likely $h$ is to take dependents at all. Labels have their own views $a'_i, e'_i$, and for each label $l$,

$$s_l(h, d) = a'^\top_h U_l e'_d + w_l^\top [e'_d; a'_h] + c_l.$$

**Training.** For each word $d$, $p(h \mid d)$ is the softmax of the column $s(\cdot, d)$ over $h \ne d$, and the head loss is $-\sum_d \log p(h^\ast(d) \mid d)$. The label loss is the cross-entropy of the label softmax at the gold head. The losses ignore the tree constraint: each word is a separate classification.

```pseudo id=main
BIAFFINE-PARSE(r_0, ..., r_n, weights)
L1  a_i <- ReLU(W_a r_i + b_a), e_i <- ReLU(W_e r_i + b_e) for each i
L2  S[h][d] <- a_h . (U e_d) + a_h . u for all h, d
L3  head(d) <- the h != d with the largest S[h][d], for d = 1..n
L4  if the heads form a tree then go to L6
L5  head <- the maximum spanning arborescence of S rooted at 0 (Chu-Liu-Edmonds)
L6  label(d) <- the label l with the largest s_l(head(d), d), for d = 1..n
L7  return head, label
```

## Example

**A cycle repaired.** For two words with the scores (row $h$, column $d$)

| | $d = 1$ | $d = 2$ |
|---|---|---|
| $h = 0$ | 1 | 0 |
| $h = 1$ | | 10 |
| $h = 2$ | 10 | |

each word prefers the other as its head, so line L3 gives the heads 2 and 1, a cycle with no root. Line L5 contracts the cycle: entering it from the root costs least through word 1, with score $1 - 10 + 20 = 11$, against $0 - 10 + 20 = 10$ through word 2. The tree is $0 \to 1 \to 2$, with score 11, the best of the 3 trees. If instead $S[0][1] = 5$ and $S[2][1] = 1$, line L3 gives the heads 0 and 1 directly, a tree, and line L5 is skipped.

**The head prior.** If $u$ is changed by $\delta$, every entry of row $h$ changes by the same amount $a_h^\top \delta$. So the prior moves a head up or down for all dependents at once; the tests check that $u$ adds a constant to each row.

## Correctness

**The decoder returns a best tree.** If the best heads of line L3 form a tree, this tree has the largest total score of all head lists, so of all trees. Otherwise, Chu-Liu-Edmonds returns a maximum spanning arborescence rooted at 0, by the correctness proof on the [MST parsing](/mst-dependency-parsing/) page. The tests compare the decoder with a search over all trees, $(n + 1)^{n - 1}$ of them, for $n \le 5$, and check that the cycle repair is needed in some cases.

**Scores and log probabilities give the same tree.** $\sum_d \log p(\mathrm{head}(d) \mid d) = \sum_d S[\mathrm{head}(d)][d] - \sum_d \log Z_d$, and each normalizer $Z_d$ does not depend on the tree. So the tree with the best total score also has the best total log probability. The tests check this for $n \le 4$.

**The gradient.** With $q_d(h) = p(h \mid d) - [h = h^\ast(d)]$, the gradient of the head loss in $S[h][d]$ is $q_d(h)$, so the gradients in $U$ and $u$ are $\sum_d \sum_h q_d(h)\, a_h e_d^\top$ and $\sum_d \sum_h q_d(h)\, a_h$. The tests compare them with finite differences. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

**Time.** The views take $\Theta(n k r)$, the products $U e_d$ take $\Theta(n k^2)$, and the $n^2$ dot products take $\Theta(n^2 k)$. The best heads take $\Theta(n^2)$ and the tree test $O(n^2)$ as written. When they do not form a tree, Chu-Liu-Edmonds takes $O(n^3)$ as written, or $O(n^2)$ with Tarjan's version. The labels take $\Theta(n k' r + n L k'^2)$ for $L$ labels and label views of size $k'$, since only the chosen arc of each word is labeled. On a GPU, all arc scores come from one batched matrix product.

**Space.** $\Theta(n^2)$ for the score matrix and $\Theta(nk)$ for the views.

## Properties

- **Global decoding, local training.** The loss treats each word on its own, but the decoder enforces a tree. Line L5 runs only when the best heads of line L3 do not form a tree.
- **Non-projective.** The decoder can return any tree. For projective output, use the [Eisner algorithm](/eisner-algorithm/) on the same scores.
- **Separate head and dependent views.** The same word has different vectors as head and as dependent, so $s(h, d) \ne s(d, h)$ in general, which the direction of an arc requires.
- **The head prior.** The term $a_h^\top u$ lets the model learn that some words, such as verbs, take many dependents, apart from any particular dependent.
- **Small views.** The ReLU layers reduce the encoder vectors to a small size before the biaffine product, which removes information not needed for the head choice and keeps $U$ small.

## Variants and improvements

- **Other encoders.** The BiLSTM can be replaced by [ELMo](/elmo/) or [BERT](/bert/) vectors, or a transformer, with the same biaffine scorer.
- **Projective decoding.** Use the Eisner algorithm on the score matrix when the treebank is projective.
- **Tree-level training.** The [matrix-tree theorem](/matrix-tree-theorem/) gives the sum, over all trees, of the product of the exponentiated arc scores, so the loss can be the log probability of the gold tree under a distribution over trees instead of a product of head softmaxes.
- **Higher-order scores.** Scores of pairs of arcs, such as siblings and grandparents, can be added, with an approximate decoder.
- **Single root.** A decoder that allows only one arc from the root can be built by running the arborescence algorithm with each root child fixed, or by a direct method.

## When to use it

Use the biaffine parser when accuracy matters most and a GPU is available: it is a strong baseline for dependency parsing in many languages, and its scorer is easy to add on top of any encoder. For greedy linear-time parsing on a CPU with a small model, a transition-based parser such as the [Chen-Manning parser](/chen-manning-parser/) is simpler.

## Pitfalls

- **Rows and columns.** The softmax for word $d$ runs over the column of $d$, the candidate heads, not over the row. Mixing them gives a model that chooses dependents for each head.
- **Self-loops and the root column.** $S[d][d]$ must be excluded from the softmax and the decoder, and the root must never get a head.
- **Cycles and many roots.** The best heads may form a cycle, and without the tree decoder the output is then not a tree. Several words may also take the root, which is wrong when the treebank needs one root child; then use a single-root decoder.
- **Labels before heads.** The labels are chosen for the decoded heads, not the gold ones, at test time; train the label classifier at the gold head, but evaluate it at the predicted head.

## Implementations

## History

Graph-based parsing with arc scores and a maximum spanning tree decoder goes back to McDonald, Pereira, Ribarov and Hajič (2005), with arc scores from feature templates. Kiperwasser and Goldberg (2016) computed arc scores from BiLSTM vectors with a small feedforward network. Dozat and Manning (2017) replaced that network by a biaffine product of two reduced views, with a separate head prior term, and trained each word's head choice as a softmax; with careful regularization this gave the best results of the time on the English Penn Treebank and the Chinese Treebank. The biaffine scorer became a standard part of neural dependency parsers.

## References
