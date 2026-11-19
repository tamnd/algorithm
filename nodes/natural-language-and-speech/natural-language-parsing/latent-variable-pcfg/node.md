---
tag: MN4Q6R
kind: model
slug: latent-variable-pcfg
name: Latent-variable PCFG
aliases:
- PCFG-LA
- split-merge grammar
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: "A PCFG whose nonterminals are split into latent subcategories learned by EM, with repeated split, merge and smoothing rounds."
history:
  year: 2005
  people: [Takuya Matsuzaki, Yusuke Miyao, Jun'ichi Tsujii]
  note: "Matsuzaki, Miyao and Tsujii gave every nonterminal a hidden annotation from a fixed set and trained it with EM. In 2006 Petrov, Barrett, Thibaux and Klein learned the splits by repeated split, merge and smoothing rounds."
prereqs: [probabilistic-context-free-grammar, expectation-maximization, treebank]
see_also: [inside-outside-algorithm, parent-annotation, lexicalized-pcfg, most-probable-parse, hidden-markov-model, np-hard, probabilistic-cky, constituency-parsing]
sources:
  - paper: doi:10.3115/1219840.1219850
    title: "Takuya Matsuzaki, Yusuke Miyao and Jun'ichi Tsujii, Probabilistic CFG with Latent Annotations, ACL 2005"
    locator: "pp. 75-82; the model, the EM training, the NP-hardness sketch of Section 3 and the approximate decoders of Sections 3.1 and 3.2"
  - paper: doi:10.3115/1220175.1220230
    title: "Slav Petrov, Leon Barrett, Romain Thibaux and Dan Klein, Learning Accurate, Compact, and Interpretable Tree Annotation, ACL 2006"
    locator: "pp. 433-440; the X-bar starting grammar, split and merge, smoothing, max-rule decoding with coarse-to-fine pruning, and the results"
  - paper: doi:10.3115/993268.993392
    title: "Khalil Sima'an, Computational complexity of probabilistic disambiguation by means of tree-grammars, COLING 1996"
    locator: "pp. 1175-1180; the NP-hardness of the most probable parse for stochastic tree-substitution grammars"
  - paper: doi:10.3115/1075096.1075150
    title: "Dan Klein and Christopher D. Manning, Accurate Unlexicalized Parsing, ACL 2003"
    locator: "pp. 423-430; the hand-made splits of categories that latent-variable grammars learn automatically"
---

A latent-variable PCFG is a [probabilistic context-free grammar](/probabilistic-context-free-grammar/) whose nonterminals are each split into several hidden subcategories. A treebank shows the label NP, but the model works with NP-1, NP-2 and so on, and the subcategory of each node is never observed. The probability of a tree is the sum over all ways to give its nodes subcategories. The rule probabilities of the subcategories are learned with [expectation-maximization](/expectation-maximization/), so the data decides which distinctions matter. The subcategories can, for example, separate subject from object noun phrases, a split that [parent annotation](/parent-annotation/) makes by hand. Matsuzaki, Miyao and Tsujii introduced the model in 2005. Petrov, Barrett, Thibaux and Klein (2006) learned the splits in rounds of split, merge and smoothing, and reached an $F_1$ of 90.7 on the development set of the Penn Treebank with no head words. Training is easy, but parsing is not: finding the most probable tree is NP-hard, so parsers use approximate decoders.

## The machine

**The grammar.** Start from a PCFG $G = (N, \Sigma, R, S)$ in which every rule is binary, unary or lexical. Each nonterminal $A \in N$ gets a finite set of subcategories $A_1, \ldots, A_{k_A}$. Every rule $A \to B\, C$ of $G$ becomes the set of rules $A_x \to B_y\, C_z$, each with its own probability $q(A_x \to B_y\, C_z)$, every unary rule $A \to B$ becomes the rules $A_x \to B_y$, and every lexical rule $A \to a$ becomes the rules $A_x \to a$. For each subcategory $A_x$, the probabilities of its rules sum to 1. The start symbol $S$ has a single subcategory. Its rules may have any number of children in the treebank, and binarization turns them into binary rules, as for any other symbol.

**The tree probability.** An annotation of a tree $t$ assigns a subcategory to each node. With $a$ ranging over the annotations,

$$P(t) = \sum_{a} \prod_{\text{nodes } u \text{ of } t} q\big(\text{rule at } u \text{ under } a\big).$$

The tree $t$ is observed and $a$ is hidden. Matsuzaki, Miyao and Tsujii use one set of $k$ subcategories for every symbol. Petrov et al. let the number of subcategories differ from symbol to symbol.

**Training on observed trees.** EM alternates two steps. The E-step computes, for each training tree, the posterior probability of each annotated rule at each node. Because the tree is fixed, this is an inside and outside pass over the nodes of the tree, not over the spans of the sentence. The M-step sets each $q$ to the expected count of the rule divided by the expected count of its left side.

**Split, merge and smoothing.** Petrov et al. grow the grammar in cycles:

1. **Split.** Split every subcategory into two, copy the rule probabilities, and add 1% of randomness to break the symmetry. Run EM.
2. **Merge.** For each split, estimate the loss in likelihood if the two halves were merged back. Undo the 50% of the new splits with the smallest loss.
3. **Smooth.** Replace each rule probability by $p' = (1 - \alpha)\, p + \alpha\, \bar p$, where $\bar p$ is the mean over the subcategories of the same symbol and $\alpha = 0.01$. Run EM again.

They start from an X-bar grammar with 98 symbols (45 tags, 27 phrasal categories and 26 intermediate symbols from binarization), 236 unary rules and 3840 binary rules. The split, the merge fraction and the smoothing weight are heuristics, set by measurements on held-out data.

## What it counts

The model gives a probability to each observed tree $t$ by the sum above, and through it a distribution over the trees of a sentence.

**The probability of a fixed tree.** Compute an inside value for each node $u$ and each subcategory $x$ of its label: for a leaf, $\beta_u(x) = q(A_x \to a)$; for a node with children $v$ and $w$,

$$\beta_u(x) = \sum_{y, z} q(A_x \to B_y\, C_z)\, \beta_v(y)\, \beta_w(z),$$

and for a node with one child $v$, $\beta_u(x) = \sum_{y} q(A_x \to B_y)\, \beta_v(y)$. Then $P(t) = \beta_{\text{root}}(1)$. With $m$ nodes and at most $k$ subcategories per symbol, this takes time $O(m k^3)$.

**The best tree differs from the best derivation.** Take a sentence of one word $a$ and the rules

| rule | $q$ | rule | $q$ |
|---|---|---|---|
| $S \to A_1$ | 0.2 | $A_1 \to a$ | 1 |
| $S \to A_2$ | 0.2 | $A_2 \to a$ | 1 |
| $S \to B_1$ | 0.3 | $B_1 \to a$ | 1 |
| $S \to B_2$ | 0.3 | $B_2 \to b$ | 1 |

The sentence has two trees, (S (A a)) and (S (B a)). The first has two annotated derivations, so its probability is $0.2 + 0.2 = 0.4$. The second has one derivation of probability $0.3$, because $B_2$ cannot produce $a$. The most probable derivation is S, $B_1$, $a$, with $0.3$, and it gives the tree (S (B a)). The most probable tree is (S (A a)), with $0.4$, and conditional probability $0.4 / 0.7 = 4/7$. A Viterbi parser over the split grammar therefore returns the wrong tree. The max-rule decoder of Petrov et al. returns the right one here: the posterior of the rule $S \to A$ is $4/7$ and that of $S \to B$ is $3/7$.

## Relation to other models

- **The inside-outside algorithm.** The [inside-outside algorithm](/inside-outside-algorithm/) trains a PCFG from sentences without trees, summing over all trees of each sentence in time cubic in its length. A latent-variable PCFG is trained from trees, and EM sums only over the annotations of one fixed tree, in time linear in the number of nodes. At parse time, the inside-outside passes over the whole sentence come back, to compute the rule posteriors that the decoders need.
- **Parent annotation.** [Parent annotation](/parent-annotation/) splits each label by a fixed, observed feature. A latent-variable PCFG learns its splits, and Petrov et al. start from a grammar without parent labels. The hand-made splits of Klein and Manning (2003) are another fixed choice that the learned splits replace.
- **Lexicalized PCFG.** A [lexicalized PCFG](/lexicalized-pcfg/) splits each label by its head word, which gives very many fine categories and a parser of time $O(n^5)$ without special algorithms. A latent-variable PCFG uses a few learned subcategories per label, so the chart stays cubic in $n$, and the cost moves into the grammar constant.
- **Hidden Markov model.** A [hidden Markov model](/hidden-markov-model/) has a hidden state for each position of a chain. A latent-variable PCFG has a hidden subcategory for each node of a tree, and training on a fixed tree is the tree version of the forward-backward pass.
- **Tree substitution grammars.** A stochastic tree substitution grammar can be written as a latent-variable PCFG, which is the basis of the hardness result below.

## Known results in the model

- **Training (theorem).** Each EM iteration does not decrease the likelihood of the training trees, as for any use of [expectation-maximization](/expectation-maximization/). EM can stop at a local maximum, which is one reason for the random noise and the gradual splits.
- **Exact probability of a tree (theorem).** $P(t)$ is computed in time $O(m k^3)$ by the inside pass on the tree.
- **The most probable tree is NP-hard (theorem, with a sketched proof).** Matsuzaki, Miyao and Tsujii state that finding the most probable observable tree is [NP-hard](/np-hard/) for general latent-variable PCFGs. They sketch the proof: a stochastic tree substitution grammar can be written as a latent-variable PCFG, and Sima'an proved the problem NP-hard for such grammars. Petrov et al. also note that the most likely unannotated tree is intractable to find. See [most probable parse](/most-probable-parse/).
- **Approximate decoders (heuristics).** Matsuzaki et al. compare reranking the $N$ best derivations, taking the tree of the best derivation, and taking the best tree under a simpler distribution fitted to the posterior. Petrov et al. choose the tree that maximizes the expected number of correct rules, computed from posteriors, and prune the chart with a coarse grammar first, dropping items with posterior below $e^{-8}$.
- **Accuracy (measurement).** The X-bar starting grammar of Petrov et al. has labeled precision and recall of 65.8 and 59.8 on the development set. After 6 split and merge cycles the grammar has 1043 symbols and reaches an $F_1$ of 90.7 on the development set, section 22. They train on sections 2 to 21 and test on section 23.

## References
