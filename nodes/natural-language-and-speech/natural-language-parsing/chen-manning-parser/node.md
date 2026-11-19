---
tag: ZT8KWQ
kind: algorithm
slug: chen-manning-parser
name: Neural transition-based dependency parser
aliases:
- Chen-Manning parser
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: "A transition parser whose next move is chosen by a feedforward network on embeddings of words, tags and labels near the stack top."
solves: [dependency-parsing]
model: word-ram
complexity:
  vars: {n: "the number of words", d: "the embedding size", H: "the number of hidden units", T: "the number of transitions, 2 times the number of labels plus 1"}
  time: {worst: Θ(n H (d + T)), best: Θ(n H (d + T))}
  space: {extra: Θ(n + d + H + T)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2014
  people: [Danqi Chen, Christopher D. Manning]
  note: "Chen and Manning (2014) replaced the sparse feature templates of transition parsers by dense embeddings of words, tags and labels and a small feedforward network with a cube activation, and made it fast with a cache of first-layer products."
prereqs: [arc-standard-parsing, word-embedding]
see_also: [dynamic-oracle, biaffine-dependency-parser, beam-search, backpropagation, adagrad, dropout, cross-entropy-loss, softmax-regression]
sources:
  - paper: doi:10.3115/v1/D14-1082
    title: "Danqi Chen and Christopher D. Manning, A fast and accurate dependency parser using neural networks, EMNLP 2014"
    locator: "the arc-standard system, the 48 features, the embedding and cube layers, the softmax output, training by cross-entropy, and the pre-computation trick"
  - paper: doi:10.1162/coli.07-056-R1-07-027
    title: "Joakim Nivre, Algorithms for deterministic incremental dependency parsing, Computational Linguistics 34(4), 513-553, 2008"
    locator: "the arc-standard system and its properties"
  - book: isbn:9781598295962
    title: "Sandra Kübler, Ryan McDonald and Joakim Nivre, Dependency Parsing, Synthesis Lectures on Human Language Technologies, Morgan and Claypool, 2009"
    locator: "Chapter 3, Transition-Based Parsing (feature-based classifiers and oracles)"
---

The Chen-Manning parser is greedy [arc-standard parsing](/arc-standard-parsing/) in which the next move is chosen by a small neural network. In each configuration it reads 48 items near the top of the stack and the front of the buffer: 18 words, their 18 part-of-speech tags, and 12 arc labels of dependents already attached. Each item is mapped to a dense vector, an [embedding](/word-embedding/); the vectors are joined, passed through one hidden layer with the cube activation $g(x) = x^3$, and a softmax layer gives a probability for each transition. The parser takes the most probable legal transition. Chen and Manning (2014) showed that this dense model, with no hand-made feature combinations, is both more accurate and faster than the sparse feature-based parsers of the time. A cache of first-layer products for frequent words makes each step cost a few hundred additions.

## In plain words

The parser works like arc-standard parsing: a pile of words being built, a queue of words still to read, and three kinds of moves. To choose a move, it looks at a fixed set of nearby things: the top three words on the pile, the next three words in the queue, some of the children already joined to the top two words, and the tags and labels of these. Each thing is turned into a short list of numbers, learned from data. A small network mixes all these numbers and gives a score to each possible move. The parser takes the best allowed move and goes on. It never goes back, so it is fast, but an early error can lead to more.

## The problem

The input is a sentence $w_1 \cdots w_n$ with part-of-speech tags, and a trained network. The output is a labeled projective [dependency tree](/dependency-tree/). In the main version the root may get several children; with the single-root rule of arc-standard parsing, RIGHT-ARC from the root only when the buffer is empty, it gets exactly one. Training uses a treebank of projective trees: each sentence gives one example per configuration on its oracle path, with the gold transition as the class.

The code on this site takes the network weights as given, drawn from a seeded generator in the tests. It implements the features, the forward pass, the cache of first-layer products, the greedy parser, the oracle and the training loss with its gradient in the output layer, but it does not train the network.

## The algorithm

**Features.** Let $s_0, s_1, s_2$ be the top three stack words and $b_0, b_1, b_2$ the first three buffer words. For a word $w$, $lc_1(w)$ and $lc_2(w)$ are its leftmost and second leftmost dependents attached so far, and $rc_1(w)$, $rc_2(w)$ the rightmost and second rightmost. The 18 word positions are

$$s_0, s_1, s_2, b_0, b_1, b_2, \text{ and for } s \in \{s_0, s_1\}: lc_1(s), rc_1(s), lc_2(s), rc_2(s), lc_1(lc_1(s)), rc_1(rc_1(s)).$$

The 18 tag features are the tags of the same positions, and the 12 label features are the labels of the last 12 positions, the dependents. A missing position gives the special item NULL, and the root gives ROOT; unknown words give UNK.

**Network.** Each feature $k$ selects a column of its embedding table, $E^w$, $E^t$ or $E^l$, each with $d$ rows. The 48 vectors are joined into $x \in \mathbb{R}^{48d}$, and

$$h = (W_1 x + b_1)^3 \ \text{(per entry)}, \qquad z = W_2 h, \qquad p(t \mid c) = \frac{e^{z_t}}{\sum_{u \text{ legal}} e^{z_u}}.$$

```pseudo id=main
CHEN-MANNING-PARSE(words, tags, network)
L1  c <- ([0], [1, ..., n], {})
L2  while c is not terminal do
L3      f <- the 48 feature ids of c
L4      x <- the joined embeddings of f; h <- (W1 x + b1)^3; z <- W2 h
L5      log p <- the log softmax of z over the legal transitions of c
L6      t <- the legal transition with the largest z
L7      c <- t(c)
L8  return the tree A of c
```

**Training.** The gold sequence of a projective tree comes from a static oracle: LEFT-ARC if the gold head of $s_1$ is $s_0$; RIGHT-ARC if the gold head of $s_0$ is $s_1$ and $s_0$ has all its gold dependents; SHIFT otherwise. The loss is the [cross-entropy](/cross-entropy-loss/) $-\log p(t^\ast \mid c)$ of the gold transition, summed over all examples, with L2 regularization. The gradient flows by [backpropagation](/backpropagation/) through $W_2$, $W_1$ and into the embeddings, which are updated too. Chen and Manning trained with [AdaGrad](/adagrad/) and [dropout](/dropout/), and started the word embeddings from vectors trained on unlabeled text.

**The cache.** $W_1 x = \sum_{k=1}^{48} W_1^{(k)} e_k$, where $W_1^{(k)}$ is the block of columns of feature $k$ and $e_k$ its embedding. For a fixed feature position $k$ and a frequent item $v$, the vector $W_1^{(k)} E_{:,v}$ can be computed once and stored. Then the first layer is a sum of 48 stored vectors of length $H$, with no multiplications.

## Example

Take *the cat sat on the mat* (words 1 to 6) with the gold heads `[-1, 2, 3, 0, 6, 6, 3]` and the labels det, nsubj, root, case, det, obl. After SHIFT, SHIFT, LEFT-ARC$_{det}$, SHIFT, the stack is 0, *cat*, *sat* and the buffer is *on the mat*. Some of the 48 features:

| position | word | tag | label |
|---|---|---|---|
| $s_0$ | sat | VERB | |
| $s_1$ | cat | NOUN | |
| $s_2$ | ROOT | ROOT | |
| $b_0, b_1, b_2$ | on, the, mat | ADP, DET, NOUN | |
| $lc_1(s_0)$ | NULL | NULL | NULL |
| $lc_1(s_1)$ | the | DET | det |
| the other 10 dependents | NULL | NULL | NULL |

The gold move here is LEFT-ARC$_{nsubj}$, which makes *sat* the head of *cat*. The full oracle sequence has 12 moves: SH, SH, LA-det, SH, LA-nsubj, SH, SH, SH, LA-det, LA-case, RA-obl, RA-root.

**Greedy is not exact.** With the sentence *the cat sat down*, one label, $d = 3$, $H = 5$ and the weights drawn from the seed 10, the greedy parser takes SH, SH, SH, SH, LA, RA, LA, RA, with total log probability about $-1.731$. A search over all complete sequences finds SH, SH, SH, SH, LA, LA, LA, RA, with about $-1.406$. The tests check this case.

## Correctness

**The parser always returns a projective tree.** The network only chooses among the legal transitions of the arc-standard system, so every run is an arc-standard run: it ends after exactly $2n$ moves with a projective tree, with one root child under the single-root rule. This holds for any weights; the network affects only which tree. The tests check it for random weights and sentences.

**The oracle gives the training data.** The static oracle rebuilds every projective tree in $2n$ moves and gets stuck on every non-projective one, so a treebank must be projective, or made projective, before training. The tests check this for all trees with $n \le 5$.

**The cache is exact.** The first layer is linear in the joined vector, so the sum of the stored blocks equals $W_1 x$ before the cube. The tests compare the two hidden layers for every configuration of the example.

**The loss gradient.** For the softmax over the legal set $S$, $\partial(-\log p_{t^\ast}) / \partial z_t = p_t - [t = t^\ast]$ for $t \in S$, and 0 outside $S$. So the gradient in $W_2$ is $(p - e_{t^\ast}) h^\top$ restricted to the legal rows. The tests compare it with finite differences.

The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

**Time.** A parse has $2n$ steps. In each step, the embedding lookup reads $48d$ numbers, the first layer takes $\Theta(48dH)$ operations, and the output layer $\Theta(TH)$, so a parse takes $\Theta(nH(d + T))$ time, treating 48 as a constant. With the cache hit for every feature, the first layer costs $\Theta(48H)$ additions, and the time becomes $\Theta(nH(1 + T))$. The feature lookup takes constant time per step if each word keeps its leftmost and rightmost dependents; the code on this site scans the head list instead, for clarity, which adds $O(n)$ per step.

**Space.** $\Theta(n)$ for the configuration and $\Theta(d + H + T)$ for the vectors of one step, besides the model. The model has $(|V_w| + |V_t| + |V_l|)d + 48dH + H + TH$ numbers, and the cache $H$ numbers for each stored pair of feature position and item.

## Properties

- **Dense features.** Similar words and tags get similar vectors, so the model can share what it learns between them, which a sparse indicator feature cannot.
- **Cube activation.** $(a_1 x_1 + \cdots + a_m x_m + b)^3$ expands into products of up to three inputs, so one hidden unit can model a combination of three features, which feature-based parsers had to write by hand.
- **Greedy and projective.** It inherits the properties of greedy arc-standard parsing: linear time in $n$, projective trees, and no guarantee of the best sequence.
- **Locally normalized.** The softmax is computed for each configuration, not for whole sequences, so the score of a parse is a product of local probabilities.

## Variants and improvements

- **Other transition systems.** The same network can choose moves for [arc-eager](/arc-eager-parsing/), [arc-hybrid](/arc-hybrid-parsing/) or [swap](/swap-transition-system/) parsing; with the swap system the parser can output non-projective trees.
- **Dynamic oracle.** Training on the parser's own configurations with a [dynamic oracle](/dynamic-oracle/) reduces error propagation.
- **Beam search and global training.** Keeping several configurations with [beam search](/beam-search/) and training the scores of whole sequences addresses the label bias of local normalization; Weiss et al. (2015) and Andor et al. (2016) did this with the same kind of network.
- **Recurrent features.** Kiperwasser and Goldberg (2016) replaced the embedding features by the outputs of a bidirectional recurrent network over the sentence, so that a few positions suffice. Graph-based parsers with the same encoders, such as the [biaffine parser](/biaffine-dependency-parser/), became the most accurate.

## When to use it

Use it for fast greedy dependency parsing on modest hardware, when projective trees are enough and a small model is wanted. When the best accuracy matters more than speed, or non-projective trees are common, a graph-based parser with a recurrent or transformer encoder is better.

## Pitfalls

- **Stack numbering.** The paper numbers the stack from 1, so its $s_1$ is $s_0$ here. Mixing the two conventions shifts every feature.
- **The order of dependents.** $lc_2$ is the second leftmost dependent, not the second closest one; and the label features must use the labels of the same positions as the word features.
- **Illegal moves.** The network gives a score to every transition. Without a mask, the parser can choose LEFT-ARC on the root or SHIFT on an empty buffer. Choose the best legal move, and normalize over the legal moves only.
- **Non-projective training trees.** The static oracle gets stuck on a non-projective tree. Skip such trees, make them projective, or use a system that can build them.
- **Cube overflow.** The cube grows fast, so large first-layer values give very large hidden values. Small initial weights and regularization keep them in range.
- **Stale cache.** The cache must be recomputed whenever $W_1$ or the embeddings change; use it at test time.

## Implementations

## History

Transition-based parsers before 2014 used linear classifiers over millions of sparse indicator features, built from hand-made templates that combined words, tags and labels near the stack top; computing these features took most of the parse time. Chen and Manning (2014) replaced them by 48 dense embeddings and one hidden layer, and reported better accuracy and higher speed than the feature-based parsers of the time. Later work added beam search and global normalization, and replaced the hand-chosen positions by recurrent encoders.

## References
