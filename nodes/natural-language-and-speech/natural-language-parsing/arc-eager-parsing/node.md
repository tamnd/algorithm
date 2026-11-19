---
tag: BSRJBW
kind: algorithm
slug: arc-eager-parsing
name: Arc-eager parsing
aliases:
- arc-eager transition system
- Nivre parser
area: natural-language-and-speech/natural-language-parsing
level: core
summary: "Transition-based parsing that adds right arcs as early as possible, with moves shift, left-arc, right-arc and reduce, in linear time."
solves: [dependency-parsing]
model: word-ram
complexity:
  vars: {n: "the number of words, with a scorer of constant cost for each of a fixed number of transitions"}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2003
  people: [Joakim Nivre]
  note: "Nivre (2003) gave a deterministic projective parser with the moves shift, reduce, left-arc and right-arc in linear time. Nivre (2004) named the strategy arc-eager, and Nivre (2008) proved its properties."
prereqs: [arc-standard-parsing]
see_also: [arc-hybrid-parsing, dynamic-oracle, swap-transition-system, projective-dependency-tree, beam-search, attachment-score, eisner-algorithm, shift-reduce-parsing]
sources:
  - url: https://aclanthology.org/W03-3017/
    title: "Joakim Nivre, An efficient algorithm for projective dependency parsing, IWPT 2003"
    locator: "the four transitions, the linear bound on their number, and projectivity of the output"
  - url: https://aclanthology.org/W04-0308/
    title: "Joakim Nivre, Incrementality in deterministic dependency parsing, Workshop on Incremental Parsing, ACL 2004"
    locator: the comparison of the arc-standard and arc-eager strategies
  - paper: doi:10.1162/coli.07-056-R1-07-027
    title: "Joakim Nivre, Algorithms for deterministic incremental dependency parsing, Computational Linguistics 34(4), 513-553, 2008"
    locator: "the arc-eager system in the stack and buffer form, its soundness, completeness and complexity"
  - url: https://aclanthology.org/C12-1059/
    title: "Yoav Goldberg and Joakim Nivre, A dynamic oracle for arc-eager dependency parsing, COLING 2012"
    locator: the cost of each transition and the dynamic oracle for arc-eager
  - book: isbn:9781598295962
    title: "Sandra Kübler, Ryan McDonald and Joakim Nivre, Dependency Parsing, Synthesis Lectures on Human Language Technologies, Morgan and Claypool, 2009"
    locator: "Chapter 3, Transition-Based Parsing"
---

Arc-eager parsing is a transition system for [dependency parsing](/dependency-parsing/) that adds each arc as soon as both of its words have been seen. Like [arc-standard parsing](/arc-standard-parsing/) it reads the sentence from left to right with a stack and a buffer, but its arcs join the top of the stack and the front of the buffer. LEFT-ARC makes the buffer front the head of the stack top and pops the stack. RIGHT-ARC makes the stack top the head of the buffer front and pushes the front, so a word is attached to its head on the left before its own right dependents are read. Because of this, a word can stay on the stack after it has its head, and a fourth move, REDUCE, pops it when it is finished. SHIFT pushes the buffer front as before. A parse takes at most $2n$ moves for $n$ words, and the system builds exactly the [projective trees](/projective-dependency-tree/). Nivre gave it in 2003. Goldberg and Nivre (2012) gave it a simple [dynamic oracle](/dynamic-oracle/), which lets a parser learn to recover from its own mistakes.

## In plain words

Read the words one at a time. Keep a pile of words that may still get dependents, and look at the top of the pile and at the next unread word. If the next word governs the top word, draw that arrow and take the top word off the pile. If the top word governs the next word, draw that arrow at once and put the next word on the pile, since it may still have its own dependents further on. If the top word already has its arrow and nothing more can attach to it, take it off the pile. Otherwise put the next word on the pile. When all words are read, any word still without an arrow is joined to the start symbol. A trained classifier makes the choice at each step.

## The problem

The input is a sentence $w_1 \cdots w_n$ with features, and a scoring function on the legal transitions of a configuration, usually a trained classifier. The output is a labeled projective [dependency tree](/dependency-tree/). In the version on this page, the root may have several children: RIGHT-ARC from the root can attach any number of words to it, and the words that are still without a head at the end are attached to it too. A parser that needs one root child must change the end of the parse; Nivre and Fernández-González (2014) study such changes.

## The algorithm

A configuration is $(\sigma, \beta, A)$, as in arc-standard parsing, with the stack top $s$ and the buffer front $b$. The initial configuration is $([0], [1, \ldots, n], \emptyset)$, and every configuration with an empty buffer is terminal. The transitions, for each label $l$:

| transition | before | after | condition |
|---|---|---|---|
| SHIFT | $(\sigma, b \mid \beta, A)$ | $(\sigma \mid b, \beta, A)$ | |
| LEFT-ARC$_l$ | $(\sigma \mid s, b \mid \beta, A)$ | $(\sigma, b \mid \beta, A \cup \{b \xrightarrow{l} s\})$ | $s \ne 0$, $s$ has no head |
| RIGHT-ARC$_l$ | $(\sigma \mid s, b \mid \beta, A)$ | $(\sigma \mid s \mid b, \beta, A \cup \{s \xrightarrow{l} b\})$ | |
| REDUCE | $(\sigma \mid s, \beta, A)$ | $(\sigma, \beta, A)$ | $s$ has a head |

The greedy parser:

```pseudo id=main
ARC-EAGER-PARSE(x, score)
L1  c <- ([0], [1, ..., n], {})
L2  while the buffer of c is not empty do
L3      for each legal transition t of c
L4          compute score(c, t), and keep the best t
L5      if t = SHIFT then push b
L6      if t = LEFT-ARC_l then add b -l-> s and pop s
L7      if t = RIGHT-ARC_l then add s -l-> b and push b
L8      if t = REDUCE then pop s
L9  attach every word without a head to the root 0, with the label root
L10 return the tree A
```

**The static oracle.** For a projective gold tree: choose LEFT-ARC if $b$ is the gold head of $s$; RIGHT-ARC if $s$ is the gold head of $b$; REDUCE if $s$ has its head and no gold dependent of $s$ is still in the buffer; SHIFT otherwise. The labels come from the gold tree.

## Example

Parse *the cat sat on the mat* (words 1 to 6) with the gold heads `[-1, 2, 3, 0, 6, 6, 3]`. The oracle gives 10 transitions, against 12 for arc-standard:

| step | transition | stack | buffer | new arc |
|---|---|---|---|---|
| 0 | | 0 | 1 2 3 4 5 6 | |
| 1 | SH | 0 1 | 2 3 4 5 6 | |
| 2 | LA-det | 0 | 2 3 4 5 6 | cat $\to$ the |
| 3 | SH | 0 2 | 3 4 5 6 | |
| 4 | LA-nsubj | 0 | 3 4 5 6 | sat $\to$ cat |
| 5 | RA-root | 0 3 | 4 5 6 | root $\to$ sat |
| 6 | SH | 0 3 4 | 5 6 | |
| 7 | SH | 0 3 4 5 | 6 | |
| 8 | LA-det | 0 3 4 | 6 | mat $\to$ the |
| 9 | LA-case | 0 3 | 6 | mat $\to$ on |
| 10 | RA-obl | 0 3 6 | | sat $\to$ mat |

At step 5 *sat* gets its head before any of its right dependents is read, which arc-standard parsing cannot do. The buffer is empty after step 10, so the parse stops; *sat* and *mat* stay on the stack, but they already have their heads, and no REDUCE is needed. The root has one child here, by the choice of the oracle.

**A wrong step and the dynamic oracle.** Suppose the parser starts with RIGHT-ARC, which attaches *the* (word 1) to the root. The gold arc *cat* $\to$ *the* is now lost, since a word gets only one head. The cost of this move is 1: the number of gold arcs that no longer can be built. From the new configuration, the dynamic oracle allows the moves of cost 0, and following them gives a tree with exactly one wrong head, the least possible. The tests check this case, and they check the cost formulas against a search over all transition sequences.

## Correctness

**Every run gives a tree.** While the buffer is not empty, SHIFT is legal, so the parser never gets stuck. LEFT-ARC is allowed only for a word without a head, and RIGHT-ARC attaches the buffer front, which has no head yet, so each word gets at most one head; line L9 gives the rest a head. A new arc cannot close a cycle: the buffer front has no head when LEFT-ARC makes it a head, and the ancestors of a stack word are all below it on the stack, so they never include the buffer front.

**The tree is projective.** The stack is increasing in position. An arc always joins the stack top $s$ and the buffer front $b$, and every word between them has been pushed after $s$ and popped. No arc can pass over a word that is still on the stack, because that word would sit between the top and the front. From this it follows that no two arcs cross, including the root arcs of line L9.

**Every projective tree is reached.** The static oracle builds every projective tree. The key step is that when a word leaves the buffer, all gold arcs between it and the words to its left are already built; projectivity rules out every configuration in which SHIFT would leave one behind. The proofs are in [the correctness proof](proofs/correctness.md). The tests also build every complete transition sequence for $n \le 5$: the trees obtained are exactly the 1, 3, 12, 55, 273 projective trees.

## Complexity

**Number of transitions.** SHIFT and RIGHT-ARC each take one word from the buffer, so there are exactly $n$ of them. LEFT-ARC and REDUCE each pop a word that some earlier SHIFT or RIGHT-ARC pushed, so there are at most $n$ of them. A complete sequence therefore has between $n$ and $2n$ transitions; with the terminal condition of this page the tests find at most $2n - 1$.

**Time.** Each step scores at most $2 + 2|R|$ transitions. With a scorer of constant cost for a fixed label set, the parse takes $\Theta(n)$ time, and line L9 adds $O(n)$.

**Space.** $\Theta(n)$ for the stack, the buffer pointer and the head list.

## Properties

- **Sound and complete for projective trees.** Every terminal configuration, after line L9, holds a projective tree, and every projective tree has a sequence.
- **Eager right arcs.** A word is attached to a head on its left as soon as both have been read. The partial tree is more connected at each step than in arc-standard parsing, which was the reason Nivre called the strategy incremental.
- **Spurious ambiguity.** A tree can have several sequences. With this page's terminal condition there are 2, 8, 40, 224, 1344 complete sequences for $n = 1$ to 5; already for $n = 1$ both SHIFT and RIGHT-ARC lead to the single tree, since a word left without a head goes to the root.
- **Early commitment.** A wrong RIGHT-ARC fixes a head before the parser has seen the words that could show it to be wrong. This is the main source of errors that the dynamic oracle trains against.
- **Arc-decomposable.** The gold arcs that can still be built from a configuration can be built all together, so the cost of a move is a count of lost gold arcs that can be read off from the configuration. This is why the dynamic oracle is simple and exact.
- **Not exact.** Greedy choices can miss the best tree under a given score. Beam search over sequences is the usual remedy.

## Variants and improvements

- **Dynamic oracle.** The cost of LEFT-ARC is the number of gold dependents of $s$ in the buffer, plus 1 if the gold head of $s$ is in the buffer after $b$ or is the root. The cost of RIGHT-ARC counts the gold arc into $b$ if its head is deeper in the stack or later in the buffer, plus the headless stack words whose gold head is $b$. The cost of REDUCE is the number of gold dependents of $s$ in the buffer. SHIFT loses the gold arcs between $b$ and the stack words that could still be built, except an arc from the root, which line L9 still gives. These are the formulas of Goldberg and Nivre (2012), adapted to the root at the bottom of the stack; the code computes them and the tests compare them with a search over all sequences.
- **Arc-hybrid.** The [arc-hybrid system](/arc-hybrid-parsing/) keeps LEFT-ARC of arc-eager and takes RIGHT-ARC of arc-standard; it needs no REDUCE.
- **Beam search and global training.** Keeping the $k$ best configurations at each step, as in [beam search](/beam-search/), with a structured perceptron over whole sequences, gives large gains over greedy parsing.
- **Exact search.** For a scorer that looks only at the stack top and the buffer front, Kuhlmann, Gómez-Rodríguez and Satta (2011) give a deduction system for arc-eager in $O(n^3)$ time.
- **Non-projective trees.** Pseudo-projective parsing transforms the treebank and undoes the transformation after parsing; the [swap system](/swap-transition-system/) is the arc-standard route to all trees.

## When to use it

Use arc-eager parsing for fast greedy or beam parsing of projective trees, especially when the partial tree should be as connected as possible at each word, as in incremental processing, or when training with a dynamic oracle. For a system without REDUCE and without the end-of-parse root rule, arc-hybrid is simpler. For many crossing arcs, use the swap system or an MST parser.

## Pitfalls

- **REDUCE of a headless word.** Popping a word without a head leaves it unattached for ever; the condition on REDUCE prevents this. In the other direction, LEFT-ARC must not give a second head to a word that already has one.
- **The end of the parse.** Words that are still on the stack without a head when the buffer becomes empty go to the root. This can give the root several children, even when every gold tree has one.
- **The static oracle's REDUCE condition.** REDUCE must wait until no gold dependent of $s$ remains in the buffer; otherwise the dependent can no longer reach its head.
- **Spurious ambiguity in training.** The static oracle picks one sequence among several correct ones, and the classifier is penalized for choosing another correct move. The dynamic oracle accepts all moves of cost 0.
- **Root as the stack top.** LEFT-ARC with $s = 0$ would make the root a dependent; it is not allowed, and REDUCE of the root is not allowed either.

## Implementations

## History

Nivre (2003) described a deterministic parser for projective dependency trees with the four moves of this page, and proved that it runs in linear time. Nivre (2004) compared it with the arc-standard strategy and called it arc-eager, because right dependents are attached at the first opportunity. Nivre (2008) set both systems in a common framework of transition systems with formal proofs, and they became the base of the MaltParser system. Zhang and Clark (2008) and others added beam search and global training. Goldberg and Nivre (2012) defined the dynamic oracle for arc-eager parsing and showed that training on the parser's own errors improves accuracy, and Goldberg and Nivre (2013) extended the idea to other systems.

## References
