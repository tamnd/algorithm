---
tag: D0MMXM
kind: algorithm
slug: arc-standard-parsing
name: Arc-standard parsing
aliases:
- arc-standard transition system
area: natural-language-and-speech/natural-language-parsing
level: core
summary: "Transition-based dependency parsing with a stack, a buffer and the moves shift, left-arc and right-arc between the two top stack words."
solves: [dependency-parsing]
model: word-ram
complexity:
  vars: {n: "the number of words, with a scorer of constant cost for each of a fixed number of transitions"}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2004
  people: [Joakim Nivre, Hiroyasu Yamada, Yuji Matsumoto]
  note: "Yamada and Matsumoto (2003) parsed with shift and two arc actions between neighbouring words. Nivre (2004) defined the arc-standard system in its stack and buffer form, and Nivre (2008) proved its properties."
prereqs: [dependency-parsing, projective-dependency-tree, shift-reduce-parsing]
see_also: [arc-eager-parsing, arc-hybrid-parsing, swap-transition-system, chen-manning-parser, dynamic-oracle, beam-search, eisner-algorithm, stack]
sources:
  - paper: doi:10.1162/coli.07-056-R1-07-027
    title: "Joakim Nivre, Algorithms for deterministic incremental dependency parsing, Computational Linguistics 34(4), 513-553, 2008"
    locator: "the stack-based arc-standard system, its soundness and completeness for projective trees, and the bound of 2n transitions"
  - url: https://aclanthology.org/W04-0308/
    title: "Joakim Nivre, Incrementality in deterministic dependency parsing, Workshop on Incremental Parsing, ACL 2004"
    locator: the arc-standard and arc-eager strategies compared for incrementality
  - url: https://aclanthology.org/W03-3023/
    title: "Hiroyasu Yamada and Yuji Matsumoto, Statistical dependency analysis with support vector machines, IWPT 2003"
    locator: "the shift, right and left actions between neighbouring words, chosen by support vector machines"
  - book: isbn:9781598295962
    title: "Sandra Kübler, Ryan McDonald and Joakim Nivre, Dependency Parsing, Synthesis Lectures on Human Language Technologies, Morgan and Claypool, 2009"
    locator: "Chapter 3, Transition-Based Parsing (configurations, transition systems, oracles and classifiers)"
---

Arc-standard parsing builds a [dependency tree](/dependency-tree/) by reading the sentence from left to right with a [stack](/stack/) of partly processed words and a buffer of words still to come. There are three moves. SHIFT pushes the next word onto the stack. LEFT-ARC makes the top word the head of the word below it and removes the lower word. RIGHT-ARC makes the second word the head of the top word and removes the top word. A classifier chooses the move in each configuration, and the parser simply takes the move with the highest score, so the whole parse is $2n$ moves for $n$ words: one shift and one arc for each word. The system builds exactly the [projective trees](/projective-dependency-tree/), bottom up, since a word gets its head only after it has all its own dependents. It is the system of Nivre (2004, 2008), close to the parser of Yamada and Matsumoto (2003), and it is the base of the [Chen-Manning parser](/chen-manning-parser/) and the [arc-eager](/arc-eager-parsing/), [arc-hybrid](/arc-hybrid-parsing/) and [swap](/swap-transition-system/) systems.

## In plain words

Read the words one at a time and put each one on a pile. Look at the two words on top of the pile. If the top word governs the word below it, draw that arrow and take the lower word out; it is finished. If the lower word governs the top word, and the top word has already collected all its own dependents, draw that arrow and take the top word out. Otherwise read the next word onto the pile. At the end only the start symbol is left, and every word has exactly one arrow into it. A trained classifier makes these choices; it looks at the words near the top of the pile and at the next words to be read.

## The problem

The input is a sentence $w_1 \cdots w_n$, with tags and other features, and a scoring function that gives each legal transition in a configuration a number; it is usually a trained classifier. The output is a [dependency tree](/dependency-tree/) with labels. The goal of training is that the greedy choices rebuild the gold trees of a treebank. The system can build only projective trees; on a non-projective gold tree its static oracle gets stuck. In the main version the root may get any number of children. In the single-root version, RIGHT-ARC from the root is allowed only when the buffer is empty, so the root gets exactly one child.

## The algorithm

A configuration is a triple $(\sigma, \beta, A)$: the stack $\sigma$, written with its top on the right, the buffer $\beta$, written with its front on the left, and the set $A$ of labeled arcs built so far. The initial configuration is $([0], [1, \ldots, n], \emptyset)$, and the terminal ones are $([0], [\,], A)$. The transitions, for each label $l$:

| transition | before | after | condition |
|---|---|---|---|
| SHIFT | $(\sigma, b \mid \beta, A)$ | $(\sigma \mid b, \beta, A)$ | buffer not empty |
| LEFT-ARC$_l$ | $(\sigma \mid s_1 \mid s_0, \beta, A)$ | $(\sigma \mid s_0, \beta, A \cup \{s_0 \xrightarrow{l} s_1\})$ | $s_1 \ne 0$ |
| RIGHT-ARC$_l$ | $(\sigma \mid s_1 \mid s_0, \beta, A)$ | $(\sigma \mid s_1, \beta, A \cup \{s_1 \xrightarrow{l} s_0\})$ | (single root: $s_1 \ne 0$ or $\beta$ empty) |

The greedy parser:

```pseudo id=main
ARC-STANDARD-PARSE(x, score)
L1  c <- ([0], [1, ..., n], {})
L2  while c is not terminal do
L3      T <- the legal transitions of c
L4      t <- argmax over t in T of score(c, t)
L5      if t = SHIFT then move the front of the buffer onto the stack
L6      if t = LEFT-ARC_l then add s0 -l-> s1 and remove s1 from the stack
L7      if t = RIGHT-ARC_l then add s1 -l-> s0 and remove s0 from the stack
L8  return the tree A
```

Ties in line L4 go to the first transition in the order SHIFT, LEFT-ARC, RIGHT-ARC, with the labels in a fixed order.

**The static oracle.** For training, the oracle turns each gold tree into one sequence of transitions, and the classifier learns the pairs of configuration and transition. In configuration $c$ with top words $s_1, s_0$: choose LEFT-ARC if $s_1$ is a gold dependent of $s_0$; choose RIGHT-ARC if $s_0$ is a gold dependent of $s_1$ and all gold dependents of $s_0$ already have their head; else SHIFT.

## Example

Parse *the cat sat on the mat* (words 1 to 6), with the gold heads `[-1, 2, 3, 0, 6, 6, 3]`. The oracle gives 12 transitions:

| step | transition | stack | buffer | new arc |
|---|---|---|---|---|
| 0 | | 0 | 1 2 3 4 5 6 | |
| 1 | SH | 0 1 | 2 3 4 5 6 | |
| 2 | SH | 0 1 2 | 3 4 5 6 | |
| 3 | LA-det | 0 2 | 3 4 5 6 | cat $\to$ the |
| 4 | SH | 0 2 3 | 4 5 6 | |
| 5 | LA-nsubj | 0 3 | 4 5 6 | sat $\to$ cat |
| 6 | SH | 0 3 4 | 5 6 | |
| 7 | SH | 0 3 4 5 | 6 | |
| 8 | SH | 0 3 4 5 6 | | |
| 9 | LA-det | 0 3 4 6 | | mat $\to$ the |
| 10 | LA-case | 0 3 6 | | mat $\to$ on |
| 11 | RA-obl | 0 3 | | sat $\to$ mat |
| 12 | RA-root | 0 | | root $\to$ sat |

At step 6, *sat* is on top and *mat* is still in the buffer. RIGHT-ARC cannot attach *mat* yet, because *mat* is not on the stack; and *sat* must stay, because it still needs *mat* as a dependent. The arc *sat* $\to$ *mat* comes only at step 11, after *mat* has collected *on* and *the*. The root has one child, so the single-root version gives the same sequence.

**Greedy search is not exact.** Let the score of an arc transition be an arc score $s(h, d)$, with $s(0, 1) = 1$, $s(1, 2) = s(1, 3) = 5$, $s(2, 1) = 3$ and 0 for all other arcs, and let SHIFT score 0. After the first SHIFT, RIGHT-ARC (score 1) beats SHIFT (score 0), so word 1 is attached to the root and leaves the stack at once. It can then never take its dependents 2 and 3. The greedy tree scores 1, while the best projective tree, $0 \to 1$, $1 \to 2$, $1 \to 3$, scores 11. The tests contain this case.

## Correctness

**Every run ends in a tree.** If the buffer is not empty, SHIFT is legal; if it is empty and the stack has two or more words, RIGHT-ARC is legal. So the parser never gets stuck before a terminal configuration. Each word enters the stack once and leaves it only by getting a head, so at the end every word has exactly one head. The arcs form a tree because a word leaves the stack when it gets a head and can never become the head of anything after that, so no cycle can close.

**The tree is projective.** At all times, the words on the stack cover consecutive intervals of positions with their subtrees built so far, in stack order, and together they cover the positions from 0 to just before the buffer. An arc joins the two top intervals into one interval. So every subtree is an interval, which is projectivity.

**Every projective tree is reached.** For a projective tree, build each subtree recursively: first the subtrees of the left dependents, then SHIFT the head and attach the left dependents with LEFT-ARC, then each right dependent's subtree followed by RIGHT-ARC. Because each subtree is an interval, these pieces follow each other in the buffer. This is the sequence that the static oracle produces. The proofs are in [the correctness proof](proofs/correctness.md). The tests check soundness and completeness by building every complete transition sequence for $n \le 5$, with and without the single-root rule: the sets of trees are exactly the projective trees, 1, 3, 12, 55, 273 of them, and 1, 2, 7, 30, 143 with one root child.

## Complexity

**Number of transitions.** A SHIFT lowers the buffer by one, and an arc transition lowers the stack by one. Take the potential $2 |\beta| + |\sigma|$: it is $2n + 1$ at the start and 1 at the end, and every transition lowers it by exactly one. So every complete sequence has exactly $2n$ transitions, $n$ shifts and $n$ arcs.

**Time.** Each step scores at most $1 + 2|R|$ transitions for the label set $R$. With a scorer that takes constant time for a fixed label set and fixed feature templates, the parse takes $\Theta(n)$ time. In general it is $2n$ times the cost of one classifier call.

**Space.** The stack, the buffer pointer and the head list take $\Theta(n)$.

## Properties

- **Sound and complete for projective trees.** Every terminal configuration holds a projective tree, and every projective tree has a sequence.
- **Bottom up.** A word is attached to its head only after all its dependents are attached. Right dependents therefore wait on the stack, which can grow to $n + 1$ words, for example in a chain of right arcs.
- **Spurious ambiguity.** A tree can have several sequences. A head with one dependent on each side can take the left one first or the right one first. For $n = 1$ to 5 there are 1, 3, 13, 67, 381 complete sequences for 1, 3, 12, 55, 273 trees; the tree `[-1, 2, 0, 2]` has two sequences. The static oracle picks one of them, the one with left arcs as early as possible.
- **Incremental, with lookahead.** The words are read in order, and a decision uses only the stack and a few buffer words. The final tree is known only at the end.
- **Not exact.** Greedy choices can lose the best tree under a given score, as in the example. Beam search and exact search over the transition sequences are the alternatives.

## Variants and improvements

- **Beam search.** Keep the $k$ best configurations at each step, as in [beam search](/beam-search/), and train the scores of whole sequences with a global perceptron or a global loss.
- **Neural classifiers.** The Chen-Manning parser chooses the arc-standard move with a feedforward network on embeddings of the words near the top of the stack.
- **Arc-eager and arc-hybrid.** The [arc-eager system](/arc-eager-parsing/) attaches right dependents as soon as they are read; the [arc-hybrid system](/arc-hybrid-parsing/) builds left arcs between the stack top and the buffer front.
- **Non-projective trees.** The [swap system](/swap-transition-system/) adds a SWAP move that reorders words and builds all trees. Pseudo-projective parsing instead transforms the treebank and undoes the transformation after parsing.
- **Exact search.** Under scores that depend on a few top elements, the space of arc-standard sequences can be searched by dynamic programming. Kuhlmann, Gómez-Rodríguez and Satta (2011) give such a deduction system in $O(n^5)$ time, or $O(n^4)$ with a further trick; this is slower than the arc-hybrid and arc-eager systems, for which the same method gives $O(n^3)$.
- **Dynamic oracles.** Arc-standard has a dynamic oracle as well, but it is less simple than those of arc-eager and arc-hybrid; see the [dynamic oracle](/dynamic-oracle/) page.

## When to use it

Use arc-standard parsing when speed matters more than exact search, when the trees are projective or can be made projective, and when a simple classifier on local features is enough. It is a good default for greedy neural parsers. When most errors come from early right attachments that wait too long, or when a simple dynamic oracle is needed, the arc-hybrid system is the usual alternative. For languages with many crossing arcs, use the swap system or an MST parser.

## Pitfalls

- **LEFT-ARC on the root.** The root must never become a dependent; the condition $s_1 \ne 0$ guards this.
- **Early RIGHT-ARC.** Attaching a word to its head before it has its own right dependents removes it from the stack for ever. The static oracle must check that $s_0$ is complete before choosing RIGHT-ARC; a classifier that does this too early cannot recover.
- **Several root children.** Without the single-root rule, a greedy parser can attach several words to the root. If the treebank requires one root child, use the rule.
- **Non-projective training trees.** The static oracle gets stuck on them. Remove such trees, projectivize them, or use the swap system.
- **Ties.** The order of ties changes the tree when scores are equal, so fix the order and keep it the same in training and parsing.

## Implementations

## History

Shift-reduce parsing is a classic method for context-free grammars. Yamada and Matsumoto (2003) used a deterministic parser with the actions shift, right and left between neighbouring words, chosen by support vector machines, which took several passes over the sentence. Nivre (2003, 2004) gave stack-based systems that make one left-to-right pass, and named the arc-standard and arc-eager strategies; Nivre (2008) set them in a common framework of transition systems and proved their soundness and completeness. Chen and Manning (2014) replaced the feature-based classifier with a neural network, which made greedy arc-standard parsing both fast and accurate.

## References
