---
tag: MG2ZX7
kind: technique
slug: dynamic-oracle
name: Dynamic oracle
aliases:
- dynamic oracle training
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: "Train a transition parser on its own possibly wrong configurations, with an oracle that gives the moves that can still reach the best tree."
prereqs: [arc-eager-parsing, arc-hybrid-parsing]
see_also: [arc-standard-parsing, swap-transition-system, chen-manning-parser, imitation-learning, dagger, exposure-bias, structured-perceptron, teacher-forcing]
sources:
  - url: https://aclanthology.org/C12-1059/
    title: "Yoav Goldberg and Joakim Nivre, A dynamic oracle for arc-eager dependency parsing, COLING 2012"
    locator: "the static oracle and its limits, the cost of a transition, the dynamic oracle for arc-eager parsing, and online training with error exploration"
  - paper: doi:10.1162/tacl_a_00237
    title: "Yoav Goldberg and Joakim Nivre, Training deterministic parsers with non-deterministic oracles, Transactions of the Association for Computational Linguistics 1, 2013"
    locator: "correct, complete and non-deterministic oracles, arc decomposition, and the dynamic oracles for arc-eager, arc-hybrid and easy-first parsing"
---

A dynamic oracle is a training method for transition-based parsers such as [arc-eager](/arc-eager-parsing/) and [arc-hybrid](/arc-hybrid-parsing/) parsing. A static oracle gives one correct move in each configuration on the path to the gold tree, so the classifier sees only gold configurations in training, and at test time it does not know what to do after its first mistake. A dynamic oracle is defined in every configuration, also the wrong ones: it gives all moves after which the best tree still reachable is as good as before. The parser can then follow its own predictions during training and learn to recover from its errors. Goldberg and Nivre (2012) introduced the method for arc-eager parsing, and Goldberg and Nivre (2013) gave the general form, with a simple and exact oracle for every system that is arc-decomposable.

## In plain words

A parser learns by copying a teacher. The usual teacher shows one right way to build each tree, step by step, and the parser only ever practises on the steps of that way. When it makes its first real mistake, it is in a state it has never seen, and the next mistakes come fast. A dynamic oracle is a better teacher. It can look at any state, even a bad one, and say which moves still lead to the best tree that can be built from there. So in training the parser is allowed to make its own mistakes, and the teacher tells it how to make the best of each one. When several moves are equally good, the teacher accepts all of them.

## When it applies

- A transition system for [dependency parsing](/dependency-parsing/), with a classifier that picks one move at a time, greedily or in a small beam.
- A loss on trees that adds up over words, usually the number of words with a wrong head, or with a wrong head or label; this is the loss behind the [attachment score](/attachment-score/).
- A way to compute the cost of a move: exactly and cheaply when the system is arc-decomposable (arc-eager, arc-hybrid), with more work otherwise (arc-standard), or by search over all sequences for short sentences.

## The template

**Definitions.** Let $G$ be the gold tree and $L(T)$ the loss of a tree $T$. For a configuration $c$, let $\mathrm{best}(c)$ be the least loss of a tree that some sequence of legal moves from $c$ can build. The cost of a legal move $t$ is

$$\mathrm{cost}(c, t) = \mathrm{best}(t(c)) - \mathrm{best}(c) \ge 0.$$

The dynamic oracle returns the set of legal moves of cost 0. It is *complete*: it is defined in every reachable configuration, and the set is never empty, since one move must keep the minimum. It is *correct*: a run that takes only moves of cost 0 from $c$ ends in a tree of loss $\mathrm{best}(c)$. It is *non-deterministic*: it returns all optimal moves, not one of them. A static oracle, in contrast, is defined only on the gold path and returns one move.

**Arc decomposition.** Call a gold arc reachable from $c$ if some tree reachable from $c$ contains it. A system is arc-decomposable if, for every $c$, the set of all gold arcs that are reachable one by one is also reachable all together, in one tree. Then $\mathrm{best}(c)$ is the number of gold arcs that are not reachable, and the cost of $t$ is the number of gold arcs that are reachable from $c$ but not from $t(c)$. This count can be read off the configuration with a few rules for each move. Goldberg and Nivre (2013) prove that arc-eager and arc-hybrid parsing are arc-decomposable for projective gold trees.

**Training.** The weights $w$ of the classifier score each move by $w \cdot \phi(c, t)$. One common scheme is an online perceptron with error exploration:

```pseudo id=main
TRAIN-WITH-DYNAMIC-ORACLE(treebank, epochs, k, p)
L1  w <- 0
L2  for epoch <- 1 to epochs do
L3      for each sentence x with gold tree G in the treebank do
L4          c <- the initial configuration of x
L5          while c is not terminal do
L6              t_p <- the legal move with the highest score w . phi(c, t)
L7              Z <- the legal moves t with cost(c, t) = 0
L8              t_o <- the move in Z with the highest score
L9              if t_p is not in Z then w <- w + phi(c, t_o) - phi(c, t_p)
L10             if epoch > k and random() < p then c <- t_p(c) else c <- t_o(c)
L11 return w
```

Line L8 lets the model choose among the correct moves, so it is not punished for a correct move that differs from the one a static oracle would pick. Line L10 is the exploration: in the first $k$ epochs the parser stays on correct paths, and later it follows its own prediction, right or wrong, with probability $p$. A neural parser uses the same loop with a loss such as the [cross-entropy](/cross-entropy-loss/) of the moves in $Z$ in place of the perceptron update.

## Classic examples

**Arc-eager parsing.** Goldberg and Nivre (2012) gave the costs: LEFT-ARC loses the gold dependents of the stack top that are still in the buffer, and its gold arc if the head is in the buffer after the front; REDUCE loses the gold dependents of the stack top in the buffer; SHIFT loses the gold arcs between the front and the stack words that could still be made; RIGHT-ARC loses the gold arc into the front if its head is another word, and the arcs from the front to stack words that have no head yet. The exact rules, with the root at the bottom of the stack, are on the [arc-eager](/arc-eager-parsing/) page. There, a first wrong RIGHT-ARC that attaches *the* to the root has cost 1, and the moves of cost 0 from there end in a tree with exactly one wrong head.

**Arc-hybrid parsing.** Take *the cat sat on the mat* with gold heads `[-1, 2, 3, 0, 6, 6, 3]`, and suppose the parser shifts twice at the start, so the stack is 0, *the*, *cat* and the front is *sat*. The second SHIFT had cost 1: *the* now lies under *cat* on the stack, so it can get its head only from the word below it or from the buffer front, and *cat* will never be either. In this configuration the costs are:

| move | cost | why |
|---|---|---|
| SHIFT | 2 | *sat* goes on top of *cat*, so *cat* can no longer get its head *sat*, and *sat* can no longer get the root, which is deeper in the stack |
| LEFT-ARC | 0 | it makes the gold arc *sat* $\to$ *cat* |
| RIGHT-ARC | 1 | it attaches *cat* to *the*, so *sat* $\to$ *cat* is lost |

After LEFT-ARC the stack is 0, *the*, and both LEFT-ARC (*sat* $\to$ *the*) and RIGHT-ARC (root $\to$ *the*) have cost 0: either way, *the* gets one wrong head and nothing else is lost. Following the oracle to the end gives a tree with one error, the least possible after the mistake. A static oracle has no answer in this configuration, because it is not on the gold path. The cost rules are on the [arc-hybrid](/arc-hybrid-parsing/) page, where the tests compare them with a search over all sequences.

**Arc-standard parsing is not arc-decomposable.** Take two words, both gold children of the root, and the configuration with stack 0, 1, 2 and an empty buffer. The arc $0 \to 1$ is reachable, by RIGHT-ARC $1 \to 2$ and then RIGHT-ARC $0 \to 1$. The arc $0 \to 2$ is reachable, by LEFT-ARC $2 \to 1$ and then RIGHT-ARC $0 \to 2$. But no sequence makes both, since 1 and 2 are on the stack together and one of them must become the head of the other. So the cost of the SHIFT that led here is 1, although it made no single gold arc unreachable, and the simple count does not work for [arc-standard parsing](/arc-standard-parsing/).

## Variations

- **Exact costs by search.** For any system, the cost can be found by a search over all move sequences from $c$. This takes exponential time, and is useful only to test cost rules on short sentences, as the tests of the arc-eager and arc-hybrid pages do.
- **Systems that are not arc-decomposable.** For arc-standard parsing and for systems with crossing arcs such as the [swap system](/swap-transition-system/), the cost needs more than a count of lost arcs; dynamic programs over the configuration, or approximate costs, have been used.
- **Static oracles with ambiguity.** Even without exploration, accepting every move of cost 0 on the gold path removes the arbitrary choice that a static oracle makes when a tree has several sequences.
- **Imitation learning.** Training on the parser's own configurations with an expert that knows the best move is an instance of [imitation learning](/imitation-learning/), close to [DAgger](/dagger/); the dynamic oracle is the expert. It is a remedy for [exposure bias](/exposure-bias/), the gap that [teacher forcing](/teacher-forcing/) leaves between training and test conditions.
- **Neural parsers.** The method is independent of the classifier: it works with feature-based perceptrons, with the feedforward network of the [Chen-Manning parser](/chen-manning-parser/), and with recurrent encoders.

## Pitfalls

- **Cost against the gold tree, not the gold path.** The cost compares with the best tree still reachable, not with the gold tree. After a mistake, the gold tree is out of reach, and a move can have cost 0 while the tree it leads to has errors.
- **Non-projective gold trees.** The cost rules of the projective systems assume a projective gold tree. For a tree with crossing arcs, the count of lost arcs is no longer exact, and the treebank must be made projective first, or the rules changed.
- **The root.** The rules must agree with how the system treats the root: whether the root sits at the bottom of the stack or at the end of the buffer, and whether it may get more than one child. A rule written for one convention gives wrong costs in the other. In the examples on this page the root is at the bottom of the stack and may have several children.
- **Exploring too early.** In the first epochs the model is poor, and following its predictions leads to configurations far from any useful one. Start exploring after some epochs, or with a small probability.
- **Labels.** If the loss counts labels, a move that makes an arc with the wrong label has cost 1 even if the head is right. Use the same loss in the oracle as in evaluation.

## Exercises

1. Show that in every configuration, at least one legal move has cost 0, and that a run of moves of cost 0 from $c$ ends in a tree of loss $\mathrm{best}(c)$.
2. In the arc-standard example above, list all trees reachable from the configuration with stack 0, 1, 2, and give the loss of each.
3. For arc-eager parsing, give a configuration in which SHIFT and RIGHT-ARC both have cost 0, and one in which REDUCE is the only move of cost 0.
4. Prove that in a configuration from which the gold tree can still be built, the moves of cost 0 are exactly the next moves of the sequences that build the gold tree. Use this to show that a dynamic oracle never disagrees with a correct static oracle on the gold path.
5. Write a search that computes $\mathrm{best}(c)$ by trying all sequences, and use it to check the arc-hybrid cost rules on all projective trees with four words.

## References
