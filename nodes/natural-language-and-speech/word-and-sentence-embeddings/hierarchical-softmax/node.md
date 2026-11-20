---
tag: 5QHTPW
kind: technique
slug: hierarchical-softmax
name: Hierarchical softmax
aliases:
- tree softmax
area: natural-language-and-speech/word-and-sentence-embeddings
level: core
summary: "Replace the softmax over V words by the product of the binary logistic decisions on the path to the word in a binary tree. A balanced tree has paths of length at most ceil(log2 V)."
model: real-ram
complexity:
  vars: {d: "the dimension of the vectors", V: "the vocabulary size, the number of types", H: "the base 2 entropy of the word distribution"}
  time: {worst: "O(d V)", average: "O(d (H + 1))"}
  space: {extra: "O(V)"}
history:
  year: 2005
  people: [Frederic Morin, Yoshua Bengio]
  note: "Morin and Bengio proposed the hierarchical softmax in 2005 to speed up a neural probabilistic language model, with a tree built from WordNet. Mikolov and colleagues used a Huffman tree over the word counts in word2vec in 2013."
prereqs: [softmax-regression, huffman-coding]
see_also: [negative-sampling, noise-contrastive-estimation, skip-gram-model, continuous-bag-of-words, neural-probabilistic-language-model, shannon-entropy, kraft-inequality, deepwalk]
sources:
  - paper: "Frederic Morin and Yoshua Bengio, Hierarchical probabilistic neural network language model, Proceedings of the Tenth International Workshop on Artificial Intelligence and Statistics (AISTATS 2005), pages 246 to 252"
    title: Morin and Bengio 2005
    locator: the decomposition of the conditional word probability into binary decisions along a tree, and the tree built from the WordNet hierarchy
  - paper: "Tomas Mikolov, Kai Chen, Greg Corrado and Jeffrey Dean, Efficient estimation of word representations in vector space, ICLR 2013 workshop track, arXiv:1301.3781"
    title: Mikolov, Chen, Corrado and Dean 2013
    locator: "Section 2 (the hierarchical softmax with a Huffman tree over the word frequencies, and the log2(V) term of the training complexity)"
  - paper: "Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado and Jeffrey Dean, Distributed representations of words and phrases and their compositionality, Advances in Neural Information Processing Systems 26 (NIPS 2013), pages 3111 to 3119, arXiv:1310.4546"
    title: Mikolov, Sutskever, Chen, Corrado and Dean 2013
    locator: the hierarchical softmax for the skip-gram model, written with the sign of each step on the path, and the Huffman tree
  - book: isbn:9780471241959
    title: "Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006"
    locator: "Chapter 5 (the Kraft inequality, the bound H <= L < H + 1 on the expected length of an optimal prefix code, and the optimality of Huffman codes)"
---

The hierarchical softmax computes the probability of one word out of $|V|$ without a sum over the vocabulary. The words are the leaves of a binary tree. Each inner node holds a vector, and the probability of a word is the product of the probabilities of the left or right turns on the path from the root to its leaf, each a logistic function of a dot product. A prediction costs one dot product per node on the path, so $\lceil \log_2 |V| \rceil$ of them in a balanced tree. The leaf probabilities sum to 1 by construction, so the model stays normalized. Morin and Bengio (2005) introduced it for a [neural probabilistic language model](/neural-probabilistic-language-model/). Mikolov et al. (2013) used a [Huffman tree](/huffman-coding/) over the word counts in word2vec, which gives frequent words short paths.

## In plain words

To pick one word out of a million, the normal way scores every word. The hierarchical softmax plays a game of twenty questions instead.

Put all the words at the bottom of a tree that splits in two at each step. At each split, the model asks a yes or no question about the input and gets a chance for "left" and a chance for "right" that add up to one. The chance of a word is the product of the chances along the way down to it.

Because the two chances at each split add up to one, the chances of all the words add up to one too. Only the splits on one path need work, which is about twenty for a million words. If common words sit near the top, the usual path is even shorter.

## When it applies

Use it when a model ends in a softmax over a large discrete set, here the vocabulary, and you need a normalized distribution or an exact log-likelihood at a lower cost. The signals are a training loss of the form $-\log P(w \mid \vec h)$ for one target word at a time, a vocabulary of thousands to millions of words, and a fixed tree, or one that you can build once from counts. When you need the probabilities of all words, for example to sample or to rank the whole vocabulary, the cost is $O(|V| d)$ again and a plain softmax is simpler. When you need only vectors, [negative sampling](/negative-sampling/) is simpler still.

## The template

The holes are the tree, the vector $\vec u_n$ of each inner node $n$ and the input vector $\vec h$ (the word vector in [skip-gram](/skip-gram-model/), the mean of the context vectors in [CBOW](/continuous-bag-of-words/)). The tree is a full binary tree with the $|V|$ words as leaves, so it has $|V| - 1$ inner nodes. The path of word $w$ is the list of pairs $(n_1, b_1), \ldots, (n_L, b_L)$ of an inner node and the bit of the child taken. With $s_n = \vec u_n \cdot \vec h$, the child 0 of node $n$ has probability $\sigma(s_n)$ and the child 1 has probability $\sigma(-s_n)$, where $\sigma(x) = 1/(1 + e^{-x})$. Then

$$P(w \mid \vec h) = \prod_{j=1}^{L} \sigma\big((1 - 2b_j)\, s_{n_j}\big).$$

```pseudo id=main
HS-LOG-PROB(h, u, path of w)
L1  for each (n, b) on the path of w, from the root do
L2      s ← u_n · h
L3      total ← total + log σ(s) if b = 0, else total + log σ(-s)
L4  return total                                 ▷ log P(w | h)
```

The gradient of $-\log P(w \mid \vec h)$ comes from the same loop. With $e_n = \sigma(s_n) - [b = 0]$ for each node on the path,

$$\frac{\partial}{\partial \vec u_n} = e_n\,\vec h, \qquad \frac{\partial}{\partial \vec h} = \sum_{(n, b) \text{ on the path}} e_n\,\vec u_n.$$

Only the $L$ node vectors on the path change in a training step.

**The probabilities sum to 1.** *Claim.* For every inner node $n$, the products of the factors from $n$ down to each leaf below $n$ sum to 1. *Proof by induction on the height of $n$.* The product below a leaf is empty, so it is 1. For an inner node $n$ with subtrees whose sums are $S_0 = S_1 = 1$ by the hypothesis, the sum below $n$ is $\sigma(s_n) S_0 + \sigma(-s_n) S_1 = \sigma(s_n) + \sigma(-s_n) = 1$, since $\sigma(x) + \sigma(-x) = 1$. At the root this gives $\sum_{w \in V} P(w \mid \vec h) = 1$ for every $\vec h$ and every choice of the node vectors. $\blacksquare$

The proof needs every inner node to have two children. A node with one child would lose the mass of the other branch.

**Example.** Take four words and the tree whose paths are a $= (0, 0)$, b $= (0, 1), (1, 0)$, c $= (0, 1), (1, 1), (2, 0)$ and d $= (0, 1), (1, 1), (2, 1)$. With $d = 1$, $h = 1$ and node values $u_0 = 0.5$, $u_1 = -1$, $u_2 = 2$:

| word | factors | probability |
|---|---|---|
| a | $\sigma(0.5)$ | 0.6225 |
| b | $\sigma(-0.5)\,\sigma(-1)$ | 0.1015 |
| c | $\sigma(-0.5)\,\sigma(1)\,\sigma(2)$ | 0.2431 |
| d | $\sigma(-0.5)\,\sigma(1)\,\sigma(-2)$ | 0.0329 |

The sum is 1. Word a costs one dot product, and words c and d cost three.

**Path lengths.** In a balanced tree every path has $\lceil \log_2 |V| \rceil$ or fewer nodes. In a Huffman tree built from the word counts, the expected path length per token $\bar L = \sum_w p_w L_w$ is the expected length of an optimal binary [prefix code](/prefix-code/), so $H \le \bar L < H + 1$, where $H$ is the [entropy](/shannon-entropy/) in base 2 of the word distribution. For the counts $(5, 2, 1, 1)$ the Huffman path lengths are $(1, 2, 3, 3)$, $\bar L = 15/9 = 1.6667$ and $H = 1.6577$, against 2 for the balanced tree. The cost of the training pass per token is $d \bar L$, so frequent words are cheap. The worst path in a Huffman tree can have $|V| - 1$ nodes, for example for counts that grow like powers of 2. So one prediction with a Huffman tree costs $O(d|V|)$ in the worst case and $O(d(H + 1))$ on average over the tokens, and the extra memory is $O(|V|)$ for the tree and the paths.

## Classic examples

- **[Neural probabilistic language model](/neural-probabilistic-language-model/).** Morin and Bengio replaced the output softmax of the model by a tree built from the WordNet hierarchy, to make the language model faster to train and to evaluate.
- **[Skip-gram model](/skip-gram-model/).** word2vec uses a Huffman tree over the word counts, with the center word vector as $\vec h$, and predicts each context word along its path.
- **[Continuous bag-of-words](/continuous-bag-of-words/).** The same tree, with the mean of the context vectors as $\vec h$ and the center word as the target.
- **[DeepWalk](/deepwalk/).** Skip-gram on random walks over a graph, trained with a hierarchical softmax whose leaves are the vertices.

## Variations

- **The choice of tree.** A balanced tree gives the best worst case. A Huffman tree gives the shortest expected path for the training tokens. A tree built from word similarity (from WordNet or by clustering word vectors) puts similar words in the same subtree, and each decision is then easier to learn. A random tree trains, but the decisions near the root then mix unrelated words.
- **Two levels.** Splitting the vocabulary into about $\sqrt{|V|}$ classes and predicting the class and then the word in the class costs $O(\sqrt{|V|}\, d)$ per prediction. It is a tree of depth 2 with a softmax at each node.
- **Sampled methods.** [Negative sampling](/negative-sampling/) and [noise-contrastive estimation](/noise-contrastive-estimation/) also avoid the full sum, but by sampling. The hierarchical softmax is exact and needs no sampling, at the price of a fixed tree.

## Pitfalls

- **The sign convention.** Line L3 must use $\sigma(s)$ for one child and $\sigma(-s)$ for the other. If both children use $\sigma(s)$, the sum over the leaves is no longer 1 and the model is not normalized. The word2vec code stores the bit as a label $1 - b$, which is the same convention written differently.
- **The cost of all probabilities.** The fast path is for one target word. Computing $P(w \mid \vec h)$ for every word still costs $O(|V| d)$, so ranking or sampling the whole vocabulary does not get faster.
- **Unbalanced worst case.** With a Huffman tree a rare word can have a path much longer than $\log_2 |V|$. The average cost is low, but a single prediction of a rare word is not.
- **Comparing losses.** The log-likelihood of the tree model is a different model from the flat softmax, and its value depends on the tree. Compare models by perplexity on held-out data, not by the training loss of two different trees.

## Exercises

1. Show that a full binary tree with $|V|$ leaves has exactly $|V| - 1$ inner nodes, so the hierarchical softmax has the same number of output vectors as the flat softmax, less one.
2. Build the Huffman tree for the counts $(8, 4, 2, 1, 1)$, compute the expected path length and compare it with the entropy of the distribution.
3. Show that with all node vectors equal to zero, every word gets the probability $2^{-L_w}$, and use the [Kraft inequality](/kraft-inequality/) to show that these sum to 1 for a full binary tree.

## References
