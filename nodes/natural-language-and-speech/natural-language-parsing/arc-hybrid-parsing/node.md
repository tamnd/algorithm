---
tag: TTAZ45
kind: algorithm
slug: arc-hybrid-parsing
name: Arc-hybrid parsing
aliases:
- arc-hybrid transition system
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: A transition system that takes left-arc from arc-eager and right-arc from arc-standard. It has a simple exact dynamic oracle.
solves: [dependency-parsing]
model: word-ram
complexity:
  vars: {n: "the number of words, with a scorer of constant cost for each of a fixed number of transitions"}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2011
  people: [Marco Kuhlmann, Carlos Gómez-Rodríguez, Giorgio Satta]
  note: "Kuhlmann, Gómez-Rodríguez and Satta (2011) defined the arc-hybrid system and a cubic dynamic program over its computations. Goldberg and Nivre (2013) gave its dynamic oracle."
prereqs: [arc-standard-parsing, arc-eager-parsing]
see_also: [dynamic-oracle, eisner-algorithm, swap-transition-system, chen-manning-parser, projective-dependency-tree, beam-search, imitation-learning, dagger]
sources:
  - url: https://aclanthology.org/P11-1068/
    title: "Marco Kuhlmann, Carlos Gómez-Rodríguez and Giorgio Satta, Dynamic programming algorithms for transition-based dependency parsers, ACL 2011"
    locator: "the arc-hybrid system and its deduction system over items [i, j] in cubic time"
  - paper: doi:10.1162/tacl_a_00237
    title: "Yoav Goldberg and Joakim Nivre, Training deterministic parsers with non-deterministic oracles, Transactions of the Association for Computational Linguistics 1, 2013"
    locator: "arc decomposition, and the costs of the arc-hybrid transitions for the dynamic oracle"
  - paper: doi:10.1162/coli.07-056-R1-07-027
    title: "Joakim Nivre, Algorithms for deterministic incremental dependency parsing, Computational Linguistics 34(4), 513-553, 2008"
    locator: "the arc-standard and arc-eager systems from which arc-hybrid takes its moves"
---

Arc-hybrid parsing is a transition system for [dependency parsing](/dependency-parsing/) that combines the moves of two older systems. Its LEFT-ARC is the one of [arc-eager parsing](/arc-eager-parsing/): the buffer front becomes the head of the stack top, which is popped. Its RIGHT-ARC is the one of [arc-standard parsing](/arc-standard-parsing/): the second stack word becomes the head of the stack top, which is popped. With SHIFT, these three moves build exactly the [projective trees](/projective-dependency-tree/) in exactly $2n$ moves for $n$ words, and every word gets its head at the moment it leaves the stack, with all its dependents already in place. Kuhlmann, Gómez-Rodríguez and Satta (2011) defined the system and showed that, for arc scores, its computations can be searched exactly in $O(n^3)$ time. Goldberg and Nivre (2013) showed that it has a simple exact [dynamic oracle](/dynamic-oracle/), which made it a common choice for greedy parsers trained on their own errors.

## In plain words

Read the words one at a time onto a pile. Look at the top word of the pile, the word under it, and the next unread word. When the top word has collected all its dependents, it is finished, and it gets its own head in one of two ways: the next unread word can become its head, or the word under it on the pile can become its head. Either way the top word leaves the pile. Otherwise read the next word onto the pile. In the end only the start symbol is left, and each word has one arrow into it. A trained classifier makes the choice at each step.

## The problem

The input is a sentence $w_1 \cdots w_n$ with features, and a scoring function on the legal transitions of a configuration. The output is a labeled projective [dependency tree](/dependency-tree/). In the version on this page the root may have several children: RIGHT-ARC can attach any number of words to the root. The rule of arc-standard parsing, RIGHT-ARC from the root only when the buffer is empty, gives exactly one root child here too.

## The algorithm

A configuration is $(\sigma, \beta, A)$ with stack top $s_0$, the word below it $s_1$, and buffer front $b$. The initial configuration is $([0], [1, \ldots, n], \emptyset)$ and the terminal ones are $([0], [\,], A)$. The transitions, for each label $l$:

| transition | before | after | condition |
|---|---|---|---|
| SHIFT | $(\sigma, b \mid \beta, A)$ | $(\sigma \mid b, \beta, A)$ | |
| LEFT-ARC$_l$ | $(\sigma \mid s_0, b \mid \beta, A)$ | $(\sigma, b \mid \beta, A \cup \{b \xrightarrow{l} s_0\})$ | $s_0 \ne 0$ |
| RIGHT-ARC$_l$ | $(\sigma \mid s_1 \mid s_0, \beta, A)$ | $(\sigma \mid s_1, \beta, A \cup \{s_1 \xrightarrow{l} s_0\})$ | |

The greedy parser:

```pseudo id=main
ARC-HYBRID-PARSE(x, score)
L1  c <- ([0], [1, ..., n], {})
L2  while c is not terminal do
L3      for each legal transition t of c
L4          compute score(c, t), and keep the best t
L5      if t = SHIFT then push b
L6      if t = LEFT-ARC_l then add b -l-> s0 and pop s0
L7      if t = RIGHT-ARC_l then add s1 -l-> s0 and pop s0
L8  return the tree A
```

**The static oracle.** If $s_0 \ne 0$ has all its gold dependents: LEFT-ARC if its gold head is $b$, RIGHT-ARC if its gold head is $s_1$. Otherwise SHIFT.

**The dynamic oracle.** The cost of a transition is the number of gold arcs that it makes impossible to build. For a projective gold tree, with $\sigma$ the stack below $s_1$ and $\beta$ the buffer after $b$:

- LEFT-ARC loses the gold dependents of $s_0$ in $\{b\} \cup \beta$, and the gold arc into $s_0$ if its head is $s_1$ or in $\beta$.
- RIGHT-ARC loses the gold dependents of $s_0$ in $\{b\} \cup \beta$, and the gold arc into $s_0$ if its head is $b$ or in $\beta$.
- SHIFT loses the gold dependents of $b$ on the stack, and the gold arc into $b$ if its head is on the stack below $s_0$.

The dynamic oracle allows every legal transition of cost 0. These costs are exact: the best tree still reachable loses exactly the arcs counted so far, so no move of cost 0 ever makes things worse.

## Example

Parse *the cat sat on the mat* (words 1 to 6) with the gold heads `[-1, 2, 3, 0, 6, 6, 3]`. The static oracle gives 12 transitions:

| step | transition | stack | buffer | new arc |
|---|---|---|---|---|
| 0 | | 0 | 1 2 3 4 5 6 | |
| 1 | SH | 0 1 | 2 3 4 5 6 | |
| 2 | LA-det | 0 | 2 3 4 5 6 | cat $\to$ the |
| 3 | SH | 0 2 | 3 4 5 6 | |
| 4 | LA-nsubj | 0 | 3 4 5 6 | sat $\to$ cat |
| 5 | SH | 0 3 | 4 5 6 | |
| 6 | SH | 0 3 4 | 5 6 | |
| 7 | SH | 0 3 4 5 | 6 | |
| 8 | LA-det | 0 3 4 | 6 | mat $\to$ the |
| 9 | LA-case | 0 3 | 6 | mat $\to$ on |
| 10 | SH | 0 3 6 | | |
| 11 | RA-obl | 0 3 | | sat $\to$ mat |
| 12 | RA-root | 0 | | root $\to$ sat |

The left arcs come as early as in arc-eager parsing (steps 2, 4, 8, 9), and the right arcs come bottom up as in arc-standard parsing (steps 11 and 12).

**A wrong step.** Suppose the parser shifts twice at the start, so that *the* lies under *cat* on the stack. The arc *cat* $\to$ *the* is lost: *the* can now get a head only from the buffer front or from the word under it, and *cat* is neither. The cost of the second SHIFT is 1, because *the* is a gold dependent of the buffer front *cat* and lies on the stack. Following the dynamic oracle from there gives a tree with exactly one wrong head, the least possible. The tests check this case.

## Correctness

**Every run ends in a tree after $2n$ moves.** SHIFT is legal while the buffer is not empty, and RIGHT-ARC is legal while the stack has two words, so a configuration that is not terminal always has a legal move. Each word is shifted once and popped once, by an arc that gives it its head, so there are exactly $2n$ moves and every word gets exactly one head. A word gets its head only when it leaves the stack, and after that it is never a head again, so no cycle can form.

**The tree is projective.** The partial subtrees of the stack words and of the buffer front are consecutive intervals in this order. LEFT-ARC joins the interval of $s_0$ to the interval of $b$ on its right, and RIGHT-ARC joins the two top intervals, so every subtree stays an interval.

**Every projective tree is reached.** For a word, build the subtrees of its left dependents one after the other, attach them with LEFT-ARC when the word is the buffer front, SHIFT the word, and then build each right dependent's subtree and attach it with RIGHT-ARC. The proofs are in [the correctness proof](proofs/correctness.md). The tests build all complete sequences for $n \le 5$ and find exactly the projective trees, each sequence of length $2n$.

**The dynamic oracle.** The tests compare the cost formulas with the true cost, the loss of the best tree still reachable minus the loss already incurred, found by search over all transition sequences, in every reachable configuration, for every projective gold tree with $n \le 4$ and for 12 sampled gold trees with $n = 5$.

## Complexity

**Transitions.** Exactly $2n$: $n$ shifts and $n$ arcs.

**Time.** Each step scores at most $1 + 2|R|$ transitions, so the greedy parse takes $\Theta(n)$ time with a scorer of constant cost. The cost of a transition in the dynamic oracle takes $O(n)$ time as written, by a scan of the stack and the buffer.

**Exact search.** The deduction system of Kuhlmann et al. uses items $[i, j]$, $0 \le i < j \le n + 1$: a computation that pushes word $i$ and moves the buffer front from $i$ to $j$. Two adjacent items $[i, k]$ and $[k, j]$ combine into $[i, j]$ with the arc $j \to k$ (a LEFT-ARC, if $j \le n$) or the arc $i \to k$ (a RIGHT-ARC). With one score per arc this takes $O(n^3)$ time and $O(n^2)$ space, and finds the best projective tree. The tests check it against a search over all trees, and use the same system to count the complete sequences: 1, 3, 13, 67, 381 for $n = 1$ to 5.

## Properties

- **Sound and complete for projective trees,** in exactly $2n$ moves.
- **Bottom up.** Every word has all its dependents before it gets its head; there is no REDUCE.
- **Spurious ambiguity.** A tree can have several sequences: for $n = 1$ to 5 there are 1, 3, 13, 67, 381 sequences for 1, 3, 12, 55, 273 trees. The tree `[-1, 0, 3, 0]` has two: the arc root $\to$ 1 can be made before or after the arc $3 \to 2$.
- **Arc-decomposable.** If each gold arc is still reachable on its own from a configuration, all of them are reachable together. This is why the cost is a simple count, and why the dynamic oracle is exact.
- **Exact search in cubic time.** With arc scores, the computations can be searched by the deduction system above, the same order of time as the [Eisner algorithm](/eisner-algorithm/).
- **Not exact when greedy.** The greedy parser can miss the best tree under a given score.

## Variants and improvements

- **Training with the dynamic oracle.** Let the parser follow its own predictions during training, sometimes taking a wrong move on purpose, and train it to choose a move of cost 0 in every configuration it reaches. This is an instance of [imitation learning](/imitation-learning/), close to [DAgger](/dagger/).
- **Neural features.** Kiperwasser and Goldberg (2016) used arc-hybrid with features from a bidirectional recurrent network over the sentence, trained with the dynamic oracle.
- **Non-projective trees.** The system builds only projective trees. The [swap system](/swap-transition-system/) shows how a SWAP move that reorders words removes this limit for arc-standard parsing.
- **Beam search.** Keeping the $k$ best configurations, as in [beam search](/beam-search/), works as for the other systems.

## When to use it

Use arc-hybrid parsing for a greedy or beam parser of projective trees when training with a dynamic oracle, which is simpler and exact here, or when exact search over the transition sequences is wanted. For a system with eager right arcs, use arc-eager. For many crossing arcs, use the swap system or an MST parser.

## Pitfalls

- **LEFT-ARC needs a buffer.** The head of LEFT-ARC is the buffer front, so it is not legal when the buffer is empty; only RIGHT-ARC finishes the parse.
- **LEFT-ARC on the root.** The root must not get a head; the condition $s_0 \ne 0$ guards this.
- **Several root children.** Without the single-root rule, the parser can attach several words to the root.
- **Using arc-standard costs.** The dynamic oracle of arc-hybrid does not carry over to arc-standard, where the cost of a move is not a simple count; arc-standard is not arc-decomposable.
- **Spurious ambiguity in the dynamic program.** Sums over computations count trees with several sequences more than once; use the deduction system for maxima, or for counting sequences, not for counting trees.

## Implementations

## History

Kuhlmann, Gómez-Rodríguez and Satta (2011) studied dynamic programming for transition-based parsers and defined the arc-hybrid system, which joins the LEFT-ARC of arc-eager parsing with the RIGHT-ARC of arc-standard parsing; for it, the deduction system is cubic. Goldberg and Nivre (2012) introduced dynamic oracles for arc-eager parsing, and Goldberg and Nivre (2013) defined arc decomposition and gave dynamic oracles for arc-hybrid and other systems. Arc-hybrid with a dynamic oracle then became a standard base for neural greedy parsers.

## References
