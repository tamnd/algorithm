---
tag: RRPKFP
kind: algorithm
slug: de-fazio-whitney-precedence-method
name: De Fazio-Whitney precedence method
aliases:
- Bourjault method
- liaison precedence method
area: cad/mechanism-and-assembly-design
level: advanced
summary: Generates all assembly sequences from precedence relations among liaisons, found by two questions per liaison, after Bourjault and De Fazio and Whitney.
solves: [assembly-sequence-planning]
model: word-ram
complexity:
  vars: {n: the number of parts, l: the number of liaisons, m: the number of motion directions, N: the number of connected sets of parts}
  time: {worst: O(N m l^2)}
  space: {extra: O(N l + m l^2)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1987
  people: [Thomas L. De Fazio, Daniel E. Whitney]
  note: They cut the questions of Bourjault's 1984 thesis down to two per liaison, with answers that are logical conditions on the liaisons already made.
prereqs: [liaison-graph, boolean-function, directed-acyclic-graph]
see_also: [assembly-sequence-planning, and-or-graph-of-assembly-plans, non-directional-blocking-graph, disassembly-sequence-planning, counting-linear-extensions, topological-sort, state-space-search, memoization]
sources:
  - paper: doi:10.1109/JRA.1987.1087132
    title: Thomas L. De Fazio and Daniel E. Whitney, Simplified generation of all mechanical assembly sequences, IEEE Journal of Robotics and Automation 3(6), 640 to 658 (1987)
    locator: the two questions per liaison, the precedence relations as logical expressions, and the diagram of liaison sequences
  - paper: "Thomas L. De Fazio and Daniel E. Whitney, Correction to Simplified generation of all mechanical assembly sequences, IEEE Journal of Robotics and Automation 4(6), 705 to 708 (1988)"
    locator: the corrected rules for reading the answers
  - paper: "Alain Bourjault, Contribution à une approche méthodologique de l'assemblage automatisé: élaboration automatique des séquences opératoires, Thèse d'État, Université de Franche-Comté, Besançon, 1984"
    locator: the liaison graph and the yes or no questions on the order of liaisons
  - paper: doi:10.1109/70.54734
    title: Luiz S. Homem de Mello and Arthur C. Sanderson, AND/OR graph representation of assembly plans, IEEE Transactions on Robotics and Automation 6(2), 188 to 199 (1990)
    locator: the comparison of the diagram of liaison states with the AND/OR graph and with precedence relations
---

The De Fazio and Whitney method lists every linear assembly sequence of a product from a short set of answers. It works on the [liaison graph](/liaison-graph/): one node for each part and one liaison for each contact. For each liaison $i$ it asks two questions. Which liaisons must be made before $i$? Which liaisons must not be made yet when $i$ is made? Each answer is a logical condition on the set of liaisons made so far. A state is a set of made liaisons, and a step is allowed when the conditions of every liaison it makes pass. The method then draws the diagram of all states and allowed steps and reads each sequence as a path through it. The answers come from an engineer or, on this page, from the geometry of boxes that move by translations along fixed directions. Under that model the paths are exactly the feasible orders, up to the order of the first two parts.

## In plain words

Think of a product as a set of joints. Each joint is a place where two parts touch. To plan how to build it, ask two questions about each joint. What must be done before this joint? What must not be done yet when this joint is made?

The answers are rules such as "the block must go on the base before the top plate closes the frame". With the rules, a program can try all orders of the joints. It starts with no joint, adds a part at each step, and keeps a step only if the rules allow it. All the orders that it keeps form a small map of states. Each road through the map from start to end is one way to build the product.

With two questions per joint, an engineer can answer them by hand for a small product.

## The problem

The input is a product with parts $P$, $|P| = n$, its liaison graph with liaisons $l_1, \ldots, l_l$, and a motion set $M$. The output is every feasible linear sequence. This page solves [assembly sequence planning](/assembly-sequence-planning/) in one restricted model. The problem page also covers two-handed plans, other motions and costs, and this method gives only the linear sequences under a fixed oracle for the questions.

The model is:

- **Hand model: linear and monotone.** Each step adds one part to the parts already placed, and a placed part never moves again. The first step joins two parts.
- **Connected steps.** The new part shares a liaison with a placed part, and the step makes all its liaisons with the placed parts at the same time.
- **Motion model: one translation.** The parts are axis-aligned boxes. A part comes in from infinity by one translation along $-d$, for some $d \in M$, where $M$ is a subset of the six axis directions. This is possible exactly when the part could leave the placed parts along $d$.

For a part $v$ and $d \in M$, $B(v, d)$ is the set of parts that block $v$ when it moves along $d$. A box $w$ blocks $v$ along $+x$ when their open $y$ and $z$ intervals overlap and $w$ lies at or to the right of the right face of $v$, and the same holds for the other directions.

## The algorithm

The answers are monotone logical formulas over the liaisons. For a part $w$, $\mathrm{present}(w) = \bigvee_{i \ni w} l_i$ says that $w$ is placed, which is true as soon as two or more parts are placed. A part $v$ is *stuck* when each direction has a placed blocker: $\mathrm{stuck}(v) = \bigwedge_{d \in M} \bigvee_{w \in B(v, d)} \mathrm{present}(w)$.

```pseudo id=main
DFW(P, liaisons, M)                      ▷ ask the questions, then draw the diagram
L1  for each liaison i = {u, v} do
L2      pre_i ← false if u and v interlock alone along every d ∈ M, else true          ▷ Q1
L3      post_i ← (present(u) ∧ stuck(v)) ∨ (present(v) ∧ stuck(u))                       ▷ Q2
L4  for each liaison i = {u, v}: if pre_i(∅) and not post_i(∅) then make {i} a start state, with parts {u, v}
L5  while a state X with parts Q is not expanded do
L6      for each part p ∉ Q with a liaison to Q do
L7          Δ ← the liaisons between p and Q
L8          if pre_i(X) and not post_i(X) for every i ∈ Δ then
L9              add the arc X → X ∪ Δ, with parts Q ∪ {p}
L10 return the number of paths from the start states to the full state     ▷ PATHS, memoized
```

**The two questions.** Q1, on line L2, asks which liaisons must be made before $l_i$. Blocking only gets worse when parts are added, so in this model no liaison must come first, and the only answer other than "none" is that the two parts of $l_i$ cannot be joined at all. Q2, on line L3, asks which liaisons must not be made yet: the step is wrong when one end of $l_i$ is already placed and the other end is stuck.

**A step makes several liaisons.** When the block comes in between two posts on a base, it makes three liaisons in one step. Line L7 makes them all, and line L8 checks the answers of each.

**Counting.** The diagram is a [directed acyclic graph](/directed-acyclic-graph/), because each arc adds a part. Line L10 counts its paths from each node to the full state with [memoization](/memoization/), so it visits each state and arc once. A list of all sequences is a walk of all those paths.

## Example

Take the frame of the [liaison graph](/liaison-graph/) page. Part 0 is the base plate, 1 and 2 are the left and right posts, 3 is a block between the posts on the base, and 4 is a top plate on the posts. The liaisons, numbered as pairs in order, are:

| liaison | $l_1$ | $l_2$ | $l_3$ | $l_4$ | $l_5$ | $l_6$ | $l_7$ |
|---|---|---|---|---|---|---|---|
| parts | 0, 1 | 0, 2 | 0, 3 | 1, 3 | 1, 4 | 2, 3 | 2, 4 |

Let the parts move in the plane of the frame only: $M = \{+x, -x, +z, -z\}$. No two parts interlock alone, so every $\mathrm{pre}_i$ is true. The block is stuck when the posts, the top plate and the base are all placed: the posts stop it along $\pm x$, the top plate along $+z$, and the base along $-z$. No other part is ever stuck, because each one can leave the frame along $-x$, $+x$, $-z$ or $+z$. So

- $\mathrm{post}_1, \mathrm{post}_2, \mathrm{post}_5, \mathrm{post}_7$ are false,
- $\mathrm{post}_3 = \mathrm{post}_4 = \mathrm{post}_6 = \mathrm{present}(0) \wedge \mathrm{present}(1) \wedge \mathrm{present}(2) \wedge \mathrm{present}(4)$, with $\mathrm{present}(4) = l_5 \vee l_7$ and so on.

In words: the block must be in before the frame closes around it. The diagram has 7 start states, one for each liaison, 22 states and 42 arcs. The state $\{l_1, l_2, l_5, l_7\}$ is the closed frame without the block, and it has no arc out. There are 32 paths. Each path is two orders of the parts, because the first two parts can come in either order, so 64 of the 120 orders of the parts are feasible. Of the 120 orders, 80 add a part that touches a placed part at each step, and the 16 that put the block after the closed frame are removed by the answers.

## Correctness

The proof uses the model above. If $Q$ is the connected set of placed parts and $|Q| \ge 2$, then $\mathrm{present}(w)$ is true on the state $E(Q)$ exactly when $w \in Q$, so the state names its parts and $\mathrm{stuck}(v)$ is true exactly when $v$ cannot come in. For a new part $p$ with a liaison $\{p, u\}$ to $Q$, the term $\mathrm{present}(p) \wedge \mathrm{stuck}(u)$ is false and $\mathrm{post}_i = \mathrm{stuck}(p)$, so line L8 passes exactly when $p$ can come in. The first step passes exactly when $\mathrm{pre}_i$ is true, that is, when one of the two parts can come in next to the other. Every state is the set of liaisons inside a connected set of parts, and the full state is reached only when all parts are placed. So the paths of the diagram are exactly the images of the feasible orders, and two feasible orders have the same image exactly when they differ in their first two parts. The full proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

The answers have size $O(m l)$ each, because $\mathrm{stuck}(v)$ has at most $m$ terms of at most $2l$ variables. A state is the set of liaisons inside a connected set $Q$ of at least two parts, so there are at most $N$ states. At each state, line L6 tries at most $n$ parts, and lines L7 and L8 evaluate the answers of at most $2l$ liaisons in all, so a state costs $O(m l^2)$ and the whole diagram costs $O(N m l^2)$. The diagram holds at most $N$ states of $O(l)$ liaisons and at most $N n$ arcs, so with the answers the space is $O(N l + m l^2)$. The method asks $2l$ questions, which is the reason for the method. The diagram is still exponential in the worst case: when one base part touches all others, $N \ge 2^{n-1}$.

## Properties

- **Exact under its model.** The paths are the feasible linear sequences, no more and no fewer, when the answers are the geometric ones of line L2 and L3. Answers from a person are only as good as the person.
- **Monotone answers.** Each answer is a formula with "and" and "or" and no "not". So a step that passes in a state still passes in a smaller state with the same new part.
- **Linear only.** The method cannot show a plan that builds two subassemblies and then joins them.
- **One state, many orders.** A state does not record the order in which its parts came in, so all orders that reach the same set of parts share one node.

## Variants and improvements

- **The earlier questions of Bourjault.** Bourjault's 1984 thesis asked yes or no questions about one liaison against others. The number of questions grows faster than the number of liaisons. De Fazio and Whitney put each answer into one logical condition, which gives $2l$ questions.
- **Precedence relations as a partial order.** When each answer is a conjunction of single liaisons, the relations are a partial order on the liaisons, and the sequences are its linear extensions. Their number is a [count of linear extensions](/counting-linear-extensions/), and one sequence is a [topological sort](/topological-sort/). The frame has a disjunction in its answers, so it is not of this kind.
- **Pruning the diagram.** A planner can also remove states that are bad for other reasons, such as an unstable subassembly or a state that needs a hard reorientation, and then pick paths by cost.
- **Two-handed plans.** The [AND/OR graph of assembly plans](/and-or-graph-of-assembly-plans/) holds the plans that join subassemblies. Homem de Mello and Sanderson compared the diagram of liaison states, the AND/OR graph and precedence relations as ways to hold the same sequences.
- **Automatic answers.** The [non-directional blocking graph](/non-directional-blocking-graph/) answers the geometric part of Q2 for all translation directions at once, and so removes the person from the loop.

## When to use it

Use it for products of up to a few tens of parts when an engineer must review the rules, because two questions per liaison are short to ask and to check. Use it when only linear sequences are allowed, as on many assembly lines with one fixture. When the parts are given as geometry, compute the answers as on this page instead of asking a person. Use the [AND/OR graph](/and-or-graph-of-assembly-plans/) when two-handed plans count, and a search of one branch when one plan is enough.

## Pitfalls

- **Answers by hand can be wrong.** A missed blocker lets through a sequence that cannot be built. A blocker that does not exist removes a good sequence. Check the answers against the geometry when there is geometry.
- **The empty state cannot tell which part came first.** On the first step, a condition on the liaisons sees neither part. If one of the first two parts must come first, for example because it is a fixture, that fact cannot be written as an answer. Check the first step on the parts.
- **One liaison at a time is wrong.** A step can make several liaisons. If the diagram adds one liaison per arc, it creates states with parts that touch but are not joined, which the model does not have.
- **A product in pieces.** If the liaison graph is not connected, no sequence exists under the connected model. The program must say so. It must not stop at a state that has all liaisons but not all parts.
- **All six directions.** With all six axis directions, a box is never stuck among five or fewer other boxes, because each other box blocks it along at most one direction. For small box products, only the connection rule then removes orders. The example keeps motion in the plane for that reason.

## Implementations

The Python module computes the answers to both questions from a list of boxes with integer or Fraction corners and a set of axis directions, as formulas that can be printed. It then draws the diagram, counts its paths and lists the sequences. A shared helper holds the box predicates. The tests check every order of up to 6 parts, with each step tested by moving the new part along each direction and sampling its positions, and compare the feasible orders with the paths of the diagram. They also check the frame, the dead state of the closed frame, and the fact that with all six directions every order with connected steps is feasible.

## History

Bourjault, in his 1984 thesis at Besançon, used the liaison graph to generate assembly sequences from the answers to many yes or no questions. De Fazio and Whitney published the two question method in 1987 and a correction to it in 1988. Homem de Mello and Sanderson compared it with the AND/OR graph and with other representations around 1990. Later work replaced the person by geometric reasoning on blocking graphs.

## References
