---
tag: V1GHKA
kind: algorithm
slug: karp-miller-tree
name: Karp-Miller tree
aliases:
- Coverability tree
- Karp-Miller algorithm
area: logic-and-constraints/model-checking
level: research
summary: Build a finite tree of omega-markings that covers every reachable marking of a Petri net. It decides coverability and boundedness, and it always terminates by Dickson's lemma.
solves: [coverability]
model: word-ram
properties: {deterministic: true, recursive: false}
history:
  year: 1969
  people: [Richard M. Karp, Raymond E. Miller]
  note: Karp and Miller built the tree in their 1969 paper on parallel program schemata, to decide boundedness and coverability of vector addition systems.
prereqs: [petri-net, coverability, depth-first-search]
see_also: [petri-net-reachability-decidability, reachability-problem, state-explosion-problem, expspace]
sources:
  - paper: doi:10.1016/S0022-0000(69)80011-5
    title: Richard M. Karp and Raymond E. Miller, Parallel program schemata, Journal of Computer and System Sciences 3(2), 1969, pages 147 to 195
    locator: the construction of the coverability tree for vector addition systems and the proof that it is finite
  - paper: doi:10.1109/5.24143
    title: Tadao Murata, Petri nets, properties, analysis and applications, Proceedings of the IEEE 77(4), 1989, pages 541 to 580
    locator: Section on the coverability tree, with its construction and its limits for liveness and reachability
  - paper: "Ernst W. Mayr and Albert R. Meyer, The complexity of the finite containment problem for Petri nets, Journal of the ACM 28(3), 1981, pages 561 to 576"
    title: The complexity of the finite containment problem for Petri nets
    locator: nets whose reachability sets, and so whose coverability trees, are finite but larger than any primitive recursive bound
  - paper: doi:10.1016/0304-3975(78)90036-1
    title: Charles Rackoff, The covering and boundedness problems for vector addition systems, Theoretical Computer Science 6(2), 1978, pages 223 to 231
    locator: the bound on the length of a shortest covering sequence, which gives the EXPSPACE algorithm
  - paper: "Richard J. Lipton, The reachability problem requires exponential space, Research Report 62, Department of Computer Science, Yale University, 1976"
    title: The reachability problem requires exponential space
    locator: the exponential space lower bound for coverability and reachability
  - paper: "Alain Finkel and Philippe Schnoebelen, Well-structured transition systems everywhere!, Theoretical Computer Science 256(1-2), 2001, pages 63 to 92"
    title: Well-structured transition systems everywhere!
    locator: the backward coverability algorithm for well-structured transition systems
  - paper: "Alain Finkel, The minimal coverability graph for Petri nets, Advances in Petri Nets 1993, Lecture Notes in Computer Science 674, Springer"
    title: The minimal coverability graph for Petri nets
    locator: the minimal coverability set, and why the plain tree repeats work
---

The *Karp-Miller tree* of a [Petri net](/petri-net/) is a finite tree whose nodes are labelled with markings in which some places may hold the symbol $\omega$, read as "as many tokens as you like". Each reachable marking is covered by a label, and each label is approached by reachable markings, so the tree decides the [coverability problem](/coverability/) and the boundedness of each place. It is built like a search over the reachable markings, but when a marking is strictly larger than one of its ancestors, the places that grew are set to $\omega$; Dickson's lemma then makes the tree finite. The tree can be larger than any primitive recursive function of the net, so it is not an efficient algorithm, but it is the classic proof that coverability is decidable.

## In plain words

A Petri net moves tokens between places. Some nets can make tokens forever, so the set of reachable states is infinite, and a plain search never stops. The Karp-Miller tree stops anyway. It searches from the start state, and each new state is compared with the states on the path above it. If the new state has at least as many tokens as an earlier one in each place, and more in some places, then the steps in between can be repeated as often as you like, and those places can grow without limit. The tree writes "unbounded" in those places. A place that is unbounded stays unbounded below it. Each path down the tree can gain new unbounded places only a few times, so every path is finite. The tree then tells which token counts can be reached or passed.

## The problem

A Petri net with places $P = \{1, \ldots, k\}$ and transitions $T$ gives each transition $t$ two vectors $\mathrm{pre}(t), \mathrm{post}(t) \in \mathbb{N}^P$. A marking $M \in \mathbb{N}^P$ enables $t$ when $M \ge \mathrm{pre}(t)$ in each place, and firing $t$ gives $M - \mathrm{pre}(t) + \mathrm{post}(t)$. Given the net, an initial marking $M_0$ and a target $M_T$, the [coverability problem](/coverability/) asks whether some reachable marking $M$ has $M \ge M_T$. The boundedness problem asks whether the set of reachable markings is finite.

An *$\omega$-marking* is a vector in $(\mathbb{N} \cup \{\omega\})^P$ with $k < \omega$ and $\omega \pm k = \omega$ for each $k \in \mathbb{N}$. The order $\le$ on $\omega$-markings is componentwise.

## The algorithm

```pseudo id=main
KARP-MILLER(N, M_0)                        ▷ ℓ(x) is the label of node x
L1  create the root r with ℓ(r) = M_0, W ← {r}
L2  while W ≠ ∅ do
L3      remove a node x from W
L4      if a proper ancestor y of x has ℓ(y) = ℓ(x) then continue    ▷ x stays a leaf
L5      for each transition t with pre(t) ≤ ℓ(x) do
L6          N ← ℓ(x) − pre(t) + post(t), M ← N
L7          for each node y on the path from r to x with ℓ(y) ≤ N and ℓ(y) ≠ N do
L8              for each place p with ℓ(y)(p) < N(p) do M(p) ← ω
L9          add a child z of x with ℓ(z) = M and the edge label t, W ← W ∪ {z}
L10 return the tree
```

Line L4 stops at a node that repeats the label of an ancestor: its subtree would repeat the subtree of that ancestor. Lines L5 and L6 fire each enabled transition with the $\omega$ arithmetic. Lines L7 and L8 are the *acceleration*. If an ancestor $y$ has $\ell(y) \le N$ and $\ell(y) \ne N$, the transitions on the path from $y$ to the new node can fire again from $N$, and each repetition adds the same nonnegative amount to the places that are finite. So the places where $N$ is strictly larger can be pumped as high as you like, and they become $\omega$. The order in which $W$ is processed does not change the tree; the implementation uses a stack.

To decide coverability of $M_T$, build the tree and answer yes if and only if some label $\ell(x) \ge M_T$. A place $p$ is bounded if and only if no label has $\omega$ in place $p$.

## Example

The net has places $p$, $q$, $r$ and $M_0 = (1, 0, 0)$.

| transition | pre (p, q, r) | post (p, q, r) | effect |
|---|---|---|---|
| t1 | (1, 0, 0) | (1, 1, 0) | the token in p makes one more token in q |
| t2 | (1, 0, 0) | (0, 0, 1) | the token moves from p to r |
| t3 | (0, 1, 1) | (1, 0, 0) | the token in r eats one token of q and goes back to p |

The tree has six nodes. Each row is one new node.

| node | parent, transition | N | ancestors y with ℓ(y) ≤ N and ℓ(y) ≠ N | label | expanded |
|---|---|---|---|---|---|
| 0 | root | (1, 0, 0) | none | (1, 0, 0) | yes |
| 1 | 0, t1 | (1, 1, 0) | node 0: q grew | (1, ω, 0) | yes |
| 2 | 0, t2 | (0, 0, 1) | none | (0, 0, 1) | yes, but no transition is enabled |
| 3 | 1, t1 | (1, ω, 0) | node 0: q grew | (1, ω, 0) | no, it repeats node 1 |
| 4 | 1, t2 | (0, ω, 1) | none | (0, ω, 1) | yes |
| 5 | 4, t3 | (1, ω, 0) | node 0: q grew | (1, ω, 0) | no, it repeats node 1 |

So place $q$ is unbounded, and $p$ and $r$ are bounded by 1. The target $(0, 5, 1)$ is coverable, by node 4: fire t1 five times, then t2. The target $(1, 0, 1)$ is not coverable, because no label has a token in both $p$ and $r$. This matches the place invariant $M(p) + M(r) = 1$, which each transition keeps.

## Correctness

**Theorem.** For every Petri net and initial marking, KARP-MILLER terminates. For the tree it returns:

1. (cover) for each reachable marking $M$ there is a node $x$ with $\ell(x) \ge M$;
2. (approach) for each node $x$ and each $k \in \mathbb{N}$ there is a reachable marking $M$ with $M(p) = \ell(x)(p)$ where $\ell(x)(p) < \omega$ and $M(p) \ge k$ where $\ell(x)(p) = \omega$.

So $M_T$ is coverable if and only if some label is $\ge M_T$, and place $p$ is bounded if and only if no label has $\omega$ in place $p$.

Termination uses two facts. The tree is finitely branching, so by König's lemma an infinite tree has an infinite path, on which every node is expanded and no two labels are equal. Along a path the set of $\omega$-places only grows, so it is constant from some node on. By *Dickson's lemma*, each infinite sequence of vectors in $\mathbb{N}^P$ has two indices $i < j$ with $v_i \le v_j$; applied to the finite places, it gives an ancestor that is strictly smaller than a later node, and then line L8 must add a new $\omega$, which is a contradiction. The cover property follows by induction on the length of a firing sequence. The approach property needs a pumping argument: the transition sequence from an accelerating ancestor has a nonnegative effect on the finite places and a positive effect on the new $\omega$-places. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The tree is always finite, but its size has no primitive recursive bound in the size of the net. Mayr and Meyer (1981) built nets whose reachability sets are finite and larger than any primitive recursive function of the size of the net. For a bounded net no acceleration happens, because a strictly larger descendant of a marking would give an unbounded place by the approach property. So the labels are exactly the reachable markings, and the tree has at least that many nodes.

Each node costs $O(|T| \cdot k \cdot h)$ time, where $h$ is its depth, for the comparisons with the ancestors in lines L4 and L7, and the space is that of the tree. No better worst-case bound in terms of the net size exists for this algorithm. The coverability problem itself is [EXPSPACE](/expspace/)-complete: Rackoff (1978) bounded the length of a shortest covering sequence by a doubly exponential function of the net size, which gives an algorithm in exponential space, and Lipton (1976) proved the matching lower bound. The Karp-Miller tree does not meet that bound; it is used for its simplicity and because it answers all coverability and boundedness questions for one net at once.

## Properties

- **Terminates on every net**, bounded or not, unlike a breadth-first search of the reachable markings.
- **Exact on bounded nets.** If no label has $\omega$, the labels are exactly the reachable markings.
- **Over-approximation for reachability.** A label with $\omega$ stands for an infinite set of markings, but not all of them are reachable. The tree does not decide reachability.
- **Order of exploration.** Any order of the work set gives the same tree, because each node depends only on its ancestors.

## Variants and improvements

- **Coverability graph.** Merge nodes with equal labels anywhere in the tree, not only on one path. This gives a finite graph that is often much smaller, with the same cover and approach properties.
- **Minimal coverability set.** Finkel (1993) keeps only the maximal labels and prunes subtrees of labels that are covered by other labels. Later work corrected and sped up this pruning.
- **Backward coverability.** Start from the upward-closed set of markings $\ge M_T$ and compute predecessors as a finite set of minimal elements. This also terminates by Dickson's lemma, and it is the basis of the well-structured transition systems of Abdulla, Cerans, Jonsson and Tsay and of Finkel and Schnoebelen.
- **Rackoff's bound.** Search only firing sequences up to the doubly exponential length bound, in exponential space.

## When to use it

Use the Karp-Miller tree for small nets when you want all the coverability and boundedness answers at once, or as a reference to test faster tools. For one coverability query on a large net, a backward algorithm or a tool based on Rackoff's bound and on SMT pruning is in most cases much faster. For a bounded net, a plain search over the reachable markings gives the same answer without the ancestor comparisons. Do not use the tree for [reachability](/petri-net-reachability-decidability/): it loses the exact counts in the $\omega$-places.

## Pitfalls

- **Comparing only with the parent.** Line L7 must compare with every ancestor, not only the parent. Take a net with a transition that moves the token from $p$ to $r$ and one that moves it back to $p$ and adds a token to $q$. Each marking is incomparable with its parent, so a parent-only test never accelerates, and the tree is infinite.
- **Comparing with nodes on other branches.** In the tree of line L7, acceleration must use ancestors only. A marking on another branch is not reachable from the current node, so it gives no pumpable sequence, and the $\omega$ is wrong.
- **Reading reachability from the tree.** Take a net with places $p$, $q$, the marking $(1, 0)$ and one transition that keeps the token in $p$ and adds two tokens to $q$. The root gets the child $(1, \omega)$, but only the markings with an even number of tokens in $q$ are reachable, so $(1, 3)$ is covered by a label and not reachable. Reachability needs the algorithm of [Mayr and Kosaraju](/petri-net-reachability-decidability/).
- **Expanding repeated labels.** Without the test of line L4, the tree is infinite even on a bounded net with a cycle.

## Implementations

## History

Richard Karp and Raymond Miller introduced the tree in 1969 to decide boundedness and coverability for vector addition systems, a model equivalent to Petri nets. Rackoff (1978) gave the exponential space algorithm for coverability and boundedness, and Lipton (1976) the exponential space lower bound. Mayr and Meyer (1981) showed that the reachability sets of bounded nets can be of non-primitive-recursive size, so the tree has no primitive recursive size bound. Finkel (1993) proposed the minimal coverability set.

## References
