---
tag: R7WDW3
kind: algorithm
slug: rete-algorithm
name: Rete algorithm
aliases:
- Rete network
- Forgy's Rete
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: Compile the rule conditions into a network that stores the partial matches, so each change of working memory updates the conflict set without matching all rules again.
model: word-ram
complexity:
  vars: {n: the number of elements in working memory, r: the number of rules, m: the largest number of conditions in a rule, a: the largest arity of an element}
  time: {worst: O(r m a n^m)}
  space: {extra: O(r m n^m)}
properties: {deterministic: true, incremental: true}
history:
  year: 1982
  people: [Charles L. Forgy]
  note: Forgy developed the network match for the OPS production system languages at Carnegie-Mellon in the 1970s, described it in his 1979 thesis, and published the full algorithm in 1982.
prereqs: [production-system, forward-chaining, nested-loop-join]
see_also: [treat-algorithm, conflict-resolution-strategy, incremental-view-maintenance, semi-naive-evaluation, discrimination-tree, hash-join, np-complete]
sources:
  - paper: doi:10.1016/0004-3702(82)90020-0
    title: "Charles L. Forgy, Rete: A fast algorithm for the many pattern/many object pattern match problem, Artificial Intelligence 19(1), 17 to 37 (1982)"
    locator: the description of the pattern and data representations, the network and its node types, and the operations of the matcher
  - paper: "Robert B. Doorenbos, Production Matching for Large Learning Systems, PhD thesis, Carnegie Mellon University, technical report CMU-CS-95-113 (1995)"
    locator: the chapter on the basic Rete algorithm (alpha memories, beta memories, join nodes and tree-based removal)
  - paper: "Charles L. Forgy, OPS5 User's Manual, technical report CMU-CS-81-135, Carnegie-Mellon University (1981)"
    locator: the description of the recognize-act cycle that the matcher serves
  - book: isbn:9780201106473
    title: Lee Brownston, Robert Farrell, Elaine Kant and Nancy Martin, Programming Expert Systems in OPS5, Addison-Wesley (1985)
    locator: the parts on the Rete match and on writing efficient OPS5 programs
---

The Rete algorithm solves the match step of a [production system](/production-system/): after each change to the working memory, find the conflict set, the set of all instantiations of all rules. A plain [forward chaining](/forward-chaining/) loop matches every rule against the whole memory again in each cycle. Rete compiles the conditions of all rules into one network. *Alpha memories* hold the working memory elements that pass the tests of a single condition, and *join nodes* hold the partial matches (*tokens*) of the first $i$ conditions of a rule. A change to working memory then only flows through the nodes that it touches. Rules that share conditions share the nodes. Forgy designed it for OPS5, and the commercial rule engines that came later use variants of it.

## In plain words

A rule system checks its rules after every small change to its facts. Most of the work it did in the last check is still valid, because only one fact changed. Rete keeps that work. For each condition it keeps the list of facts that fit the condition. For each rule it keeps the groups of facts that fit its first condition, its first two conditions, and so on. A new fact is checked only against the lists it can join, and the new groups that it makes are passed on to the next condition. When a fact is removed, the groups that hold it are removed. Two rules that start with the same conditions share these lists. The cost is memory: the saved groups can be many.

## The problem

A *working memory element* (WME) is a ground tuple, such as $\mathit{block}(b_1, \mathit{red})$. A rule has the form

$$\rho: c_1, \ldots, c_m \Rightarrow \text{actions},$$

where each condition $c_k$ is a pattern with variables. An *instantiation* of $\rho$ in the working memory $W$ is a tuple $(w_1, \ldots, w_m)$ of elements of $W$ with one binding $\theta$ of the variables such that $c_k\theta = w_k$ for each $k$. The *conflict set* $CS(W)$ is the set of pairs $(\rho, (w_1, \ldots, w_m))$ over all rules.

The task is incremental: given the rules once, and then a sequence of changes, each of which inserts or deletes one element, keep $CS(W)$ correct after each change. This page treats positive conditions only. Finding even one instantiation of one rule is the conjunctive query problem, which is [NP-complete](/np-complete/) in combined complexity, so the incremental task cannot have a polynomial worst case in the size of the rules either.

## The algorithm

The network is built from the rules before the first change. Each condition gets an *alpha memory*, keyed by the condition with its variables renamed by first occurrence, so that $\mathit{on}(x, y)$ and $\mathit{on}(b, t)$ share one memory. It holds the WMEs that pass the constant tests of the condition and the equality tests between its own variables. Each prefix $c_1, \ldots, c_i$ of a rule gets a *join node* at depth $i$, whose parent is the node of $c_1, \ldots, c_{i-1}$; rules with equal prefixes share the nodes. The join node reads the alpha memory of $c_i$ and keeps a *beta memory* of tokens, one for each match of $c_1, \ldots, c_i$. The node of the full condition list of a rule is its *production node*. A token records its parent token, its WME and its children, and each WME records its tokens, for removal.

```pseudo id=main
INSERT(w)
L1  for each alpha memory α whose tests w passes do
L2      add w to α
L3  sort the join nodes that read these alpha memories by depth, deepest first
L4  for each such join node j do RIGHT-ACTIVATE(j, w)

RIGHT-ACTIVATE(j, w)            ▷ a new element arrives from the alpha side
L5  for each token t in the beta memory of the parent of j (the empty token if j has depth 1) do
L6      if the condition of j matches w with a binding that extends the binding of t then
L7          MAKE-TOKEN(j, t, w)

MAKE-TOKEN(j, t, w)
L8  add the token t + w to the beta memory of j, link it to t and to w; if j is the production node of a rule ρ then add (ρ, t + w) to the conflict set; for each child c of j do LEFT-ACTIVATE(c, t + w)

LEFT-ACTIVATE(c, t)             ▷ a new token arrives from the parent side
L9  for each element w in the alpha memory of c do
L10     if the condition of c matches w with a binding that extends the binding of t then
L11         MAKE-TOKEN(c, t, w)

DELETE(w)
L12 remove w from every alpha memory
L13 for each token t that records w do
L14     remove t and all its descendants from their beta memories, and their instantiations from the conflict set
```

Line L3 is needed when one element can match two conditions of the same rule. Deepest first, the deeper node joins $w$ with the old tokens of its parent before the shallower node adds new tokens there, so no match is made twice. Deletion by the token tree (lines L13 and L14) is the *tree-based removal* of Doorenbos; Forgy's original network sent a delete token through the same joins as an insert.

## Example

Two rules share their first two conditions:

$$\begin{aligned} R_1 &: \mathit{goal}(g), \mathit{block}(b, \mathit{red}), \mathit{on}(b, t) \Rightarrow \ldots \\ R_2 &: \mathit{goal}(g), \mathit{block}(b, \mathit{red}), \mathit{clear}(b) \Rightarrow \ldots \end{aligned}$$

The network has 4 alpha memories, for $\mathit{goal}(\cdot)$, $\mathit{block}(\cdot, \mathit{red})$, $\mathit{on}(\cdot, \cdot)$ and $\mathit{clear}(\cdot)$, and 4 join nodes: $J_1$ for $\mathit{goal}$, $J_2$ for $\mathit{goal}, \mathit{block}$, and the production nodes $J_3$ of $R_1$ and $J_4$ of $R_2$, both children of $J_2$.

| insert | alpha memory | join activity | new tokens |
|---|---|---|---|
| $\mathit{goal}(g_1)$ | goal | $J_1$ joins with the empty token | $[g_1]$ at $J_1$ |
| $\mathit{block}(b_1, \mathit{red})$ | block red | $J_2$ joins with $[g_1]$; $J_3$ and $J_4$ find empty alpha memories | $[g_1, b_1]$ at $J_2$ |
| $\mathit{block}(b_2, \mathit{red})$ | block red | as before | $[g_1, b_2]$ at $J_2$ |
| $\mathit{block}(b_3, \mathit{blue})$ | none | the constant test $\mathit{red}$ rejects it | none |
| $\mathit{on}(b_1, \mathit{table})$ | on | $J_3$ joins with the two tokens of $J_2$; only $b = b_1$ is consistent | $[g_1, b_1, \mathit{on}]$ at $J_3$, an instantiation of $R_1$ |
| $\mathit{clear}(b_2)$ | clear | $J_4$ joins with the two tokens of $J_2$; only $b = b_2$ is consistent | $[g_1, b_2, \mathit{clear}]$ at $J_4$, an instantiation of $R_2$ |

The network now holds 5 tokens, and the conflict set holds one instantiation of each rule. Deleting $\mathit{block}(b_1, \mathit{red})$ removes the token $[g_1, b_1]$ and its child at $J_3$, so 3 tokens and the instantiation of $R_2$ remain. No join runs for the delete.

## Correctness

The [correctness proof](proofs/correctness.md) shows an invariant: each alpha memory holds exactly the elements that pass its tests, each join node holds exactly one token for each match of its prefix, and the conflict set holds exactly the matches of the production nodes. For an insert, a new match gets its token at the first position where the new element occurs, by the right activation of that node, and then by left activations down the chain; the deepest-first order rules out a second copy. For a delete, the matches that contain the element are exactly the tokens that record it and their descendants.

## Complexity

The costs depend on the data much more than on the number of rules. An insert costs the size of the parent memories of the join nodes that $w$ reaches, plus, for each new token, the size of the alpha memories of the child nodes. A delete costs the number of tokens that it removes when the token lists are linked lists. In the worst case a join node at depth $i$ holds up to $n^i$ tokens, so one change can cost $O(r\, m\, a\, n^m)$ time and the network can hold $O(r\, m\, n^m)$ tokens: the same order as matching every rule again, with more memory. This is the combined complexity; the match problem itself is NP-complete when the rules are part of the input, and for fixed rules (data complexity) the cost is polynomial in $n$.

The advantage of Rete is a measured one. Forgy's measurements of OPS programs found that most of their run time went into the match, and that a typical cycle changes few elements, so the saved state removes most of the work. Doorenbos (1995) measured the basic algorithm and his extensions on learning systems with more than a hundred thousand rules. These are results on particular programs, not bounds.

## Properties

- **Incremental.** The state between cycles holds every partial match, and each change does work only for the matches it creates or destroys.
- **State saving.** The memory can be much larger than the working memory: the price of the speed.
- **Sharing.** Equal conditions share alpha memories, and equal prefixes share join nodes. The order of the conditions in a rule decides how much is shared and how large the beta memories are.
- **Exact.** The conflict set after each change is the same as a full rematch gives, with no duplicates.

## Variants and improvements

- **Negated conditions.** A *negative node* keeps, for each token, the count of the elements that match the negated condition, and passes the token on only while the count is zero. This page does not implement it.
- **Hashed memories.** Index alpha and beta memories by the values of the join variables, so a join reads only the consistent partners, as in a [hash join](/hash-join/).
- **Rete/UL.** Doorenbos added *unlinking* of nodes whose memory is empty and other changes, so that very large learned rule sets do not slow each change.
- **TREAT.** The [TREAT algorithm](/treat-algorithm/) of Miranker keeps no beta memories and recomputes the joins after each insert, trading time on inserts for memory and cheap deletes.
- **Later designs.** Rete II and Rete-NT (Forgy's commercial versions), LEAPS (lazy matching) and Gator networks (which choose the join structure by cost) all change which partial matches are stored.

## When to use it

Use Rete when many rules are matched again and again against a working memory that changes a little in each cycle, as in OPS5, CLIPS, Jess and Drools. The saved state pays off when the same partial matches are needed in many cycles. Use [TREAT](/treat-algorithm/) when memory is short or when elements are often removed, and use a plain query when the rules are run once over static data.

## Pitfalls

- **Cross products.** A rule whose first conditions share no variables makes beta memories with the product of their alpha memories. Order the conditions so that each one joins with the earlier ones.
- **Duplicate tokens.** When an element can match two conditions of a rule, right activations must run deepest first, or the same match is made twice.
- **Modify as delete plus insert.** A change to an element in OPS5 is a delete and an insert, so the tokens of the element are removed and made again.
- **Memory growth.** The number of tokens can grow as $n^m$, and a few bad rules can fill the memory.

## Implementations

## History

Forgy developed the network match at Carnegie-Mellon in the 1970s, for the OPS family of production system languages, described it in his 1979 thesis, and published the full algorithm in Artificial Intelligence in 1982. OPS5 (1981) made it widely known. Miranker (1987) proposed TREAT as a lighter alternative. Doorenbos (1995) gave the now standard description with tree-based removal and the Rete/UL extensions. CLIPS, Jess and Drools use Rete variants.

## References
