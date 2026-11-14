---
tag: H8PR83
kind: algorithm
slug: transition-function-image-computation
name: Coudert-Madre image computation
aliases:
- range computation image method
- transition function image computation
area: eda/hardware-verification
level: advanced
summary: Coudert, Berthet and Madre's BDD method that computes the image of a set of states from the next-state functions by recursive splitting and constrain, with no transition relation.
model: word-ram
complexity:
  vars: {m: the number of state bits, k: the number of primary inputs, b: the largest number of nodes of a BDD in the run}
  time: {worst: "O(2^m m b^2)"}
  space: {extra: "O(2^m m b^2)"}
properties: {deterministic: true, exact: true, recursive: true}
history:
  year: 1989
  people: [Olivier Coudert, Christian Berthet, Jean Christophe Madre]
  note: Coudert, Berthet and Madre computed images as ranges of constrained next-state functions in 1989. Coudert and Madre gave the unified framework at ICCAD 1990.
prereqs: [generalized-cofactor, reduced-ordered-bdd, symbolic-reachability]
see_also: [partitioned-transition-relation, bdd-quantification, product-machine, sequential-equivalence-checking, cofactor, shannon-expansion, variable-ordering, state-explosion-problem]
sources:
  - paper: "Olivier Coudert, Christian Berthet and Jean Christophe Madre, Verification of synchronous sequential machines based on symbolic execution, Automatic Verification Methods for Finite State Systems, Lecture Notes in Computer Science 407, 1989"
    title: O. Coudert, C. Berthet and J. C. Madre, Verification of synchronous sequential machines based on symbolic execution, LNCS 407, Springer, 1989
    locator: the image of a set of states as the range of the next-state functions constrained by the set, and the recursive range computation
  - paper: "Olivier Coudert and Jean Christophe Madre, A unified framework for the formal verification of sequential circuits, Proceedings of the International Conference on Computer-Aided Design, 126 to 129, 1990"
    title: O. Coudert and J. C. Madre, A unified framework for the formal verification of sequential circuits, ICCAD 1990, 126 to 129
    locator: sets of states and of transitions handled with the same image operators, and the restrict operator
  - paper: "Hervé J. Touati, Hamid Savoj, Bill Lin, Robert K. Brayton and Alberto Sangiovanni-Vincentelli, Implicit state enumeration of finite state machines using BDDs, ICCAD 1990"
    title: H. J. Touati, H. Savoj, B. Lin, R. K. Brayton and A. Sangiovanni-Vincentelli, Implicit state enumeration of finite state machines using BDDs, ICCAD 1990
    locator: the comparison of image computation from the transition relation and from the transition functions, and the image property of the generalized cofactor
  - book: doi:10.1007/978-1-4615-0817-5_13
    title: A. Kuehlmann and C. A. J. van Eijk, Combinational and sequential equivalence checking, in S. Hassoun and T. Sasao (editors), Logic Synthesis and Verification, Kluwer, 2002, 343 to 372
    locator: the section on sequential equivalence by state traversal of the product machine
---

Coudert-Madre image computation finds the set of next states of a set of states of a sequential circuit, with [BDDs](/reduced-ordered-bdd/), from the next-state functions $\delta_1, \ldots, \delta_m$ alone. It builds no transition relation. It first applies the constrain operator of the [generalized cofactor](/generalized-cofactor/) page to each next-state function, with the state set as care set. The image is then the range of the constrained vector of functions, which a recursion computes by splitting on one output bit at a time. This is the transition-function method. The other method uses the transition relation and a relational product, see [partitioned transition relation](/partitioned-transition-relation/). Both give the same image step of [symbolic reachability](/symbolic-reachability/).

## In plain words

A circuit with registers moves from state to state. Given a set of states, you want all states it can reach in one clock tick, for any input. The circuit gives you one formula per register bit: its next value from the present state and the inputs.

First, simplify each formula so that it only has to be right on the given set of states. Done the right way, the simplified formulas together can produce exactly the next states of the set and nothing else. Now ask which bit patterns these formulas can output. Look at the first bit. If it can be 1, find what the other bits can be when it is 1, and the same for 0. Each case is the same question with one bit fewer. Combine the answers.

## The problem

The present-state variables are $s = (s_1, \ldots, s_m)$, the inputs $x = (x_1, \ldots, x_k)$, and the next-state functions $\delta_i(s, x)$ are BDDs. A set of states $S$ is a BDD over $s$. The task is the BDD over fresh next-state variables $y = (y_1, \ldots, y_m)$ of

$$\mathrm{Img}(S) = \{\delta(s, x) : S(s) = 1,\ x \in \{0, 1\}^k\}.$$

With the transition relation $T(s, x, y) = \bigwedge_i (y_i \equiv \delta_i(s, x))$, this is $\mathrm{Img}(S)(y) = \exists s, x.\ S(s) \wedge T(s, x, y)$. Here "transition" means the next-state functions, not the relation: the method never forms $T$.

For a vector $g = (g_1, \ldots, g_r)$ of functions, $\mathrm{Range}(g)$ is the set of values $g(z)$ over all points $z$. We write $f \downarrow c$ for constrain, defined on the [generalized cofactor](/generalized-cofactor/) page.

## The algorithm

```pseudo id=main
IMAGE(δ₁, ..., δₘ, S)
L1  if S = 0 then return 0
L2  for i ← 1 to m do gᵢ ← δᵢ ↓ S
L3  return RANGE(g₁, ..., gₘ; y₁, ..., yₘ)

RANGE(g₁, ..., gᵣ; y₁, ..., yᵣ)
L4  if r = 0 then return 1
L5  if g₁ = 1 then return y₁ ∧ RANGE(g₂, ..., gᵣ; y₂, ..., yᵣ)
L6  if g₁ = 0 then return ¬y₁ ∧ RANGE(g₂, ..., gᵣ; y₂, ..., yᵣ)
L7  hi ← RANGE(g₂ ↓ g₁, ..., gᵣ ↓ g₁; y₂, ..., yᵣ)
L8  lo ← RANGE(g₂ ↓ ¬g₁, ..., gᵣ ↓ ¬g₁; y₂, ..., yᵣ)
L9  return (y₁ ∧ hi) ∨ (¬y₁ ∧ lo)
```

Line L2 does the main work. Constrain by $S$ maps every point outside $S$ to a point inside $S$, the same map for all $m$ functions, so the vector $g$ takes exactly the values that $\delta$ takes on $S$. The domain restriction is gone. Often $g_i$ becomes much smaller than $\delta_i$, or even constant.

Lines L4 to L9 compute a range by output splitting. A constant $g_1$ fixes the first bit, and the rest is the range of the other functions (lines L5 and L6). Otherwise the first bit can be both 1 and 0. The points with $g_1 = 1$ give the tails $(g_2, \ldots, g_r)$ on the set $g_1$, which is the range of the vector constrained by $g_1$, by the same property of constrain (line L7), and the same for $\neg g_1$ (line L8). Line L9 joins the two halves with $y_1$ as the top variable.

## Example

Take state bits $s_1, s_2, s_3$, one input $x$, the order $s_1, s_2, s_3, x$, and

$$\delta_1 = s_1 \oplus x,\qquad \delta_2 = s_1 \wedge s_2,\qquad \delta_3 = x \vee s_2,\qquad S = (s_1 \oplus s_2) \wedge \neg s_3 = \{100, 010\},$$

where a state is written $s_1 s_2 s_3$. By enumeration, state 100 goes to 100 ($x = 0$) and 001 ($x = 1$), and state 010 goes to 001 ($x = 0$) and 101 ($x = 1$). So the image is $\{100, 001, 101\}$.

| call | vector | first function | action | result |
|---|---|---|---|---|
| IMAGE, L2 | $(s_1 \oplus x,\ s_1 \wedge s_2,\ x \vee s_2) \downarrow S$ | | constrain each by $S$ | $g = (s_1 \oplus x,\ 0,\ \neg s_1 \vee x)$ |
| RANGE, depth 1 | $g$ | $s_1 \oplus x$, not constant | L7: $(0, \neg s_1 \vee x) \downarrow g_1 = (0, \neg s_1)$; L8: $(0, \neg s_1 \vee x) \downarrow \neg g_1 = (0, 1)$ | $(y_1 \wedge \mathrm{hi}) \vee (\neg y_1 \wedge \mathrm{lo})$ |
| hi, depth 2 | $(0, \neg s_1)$ | 0 | L6 | $\neg y_2 \wedge \mathrm{RANGE}(\neg s_1)$ |
| depth 3 | $(\neg s_1)$ | not constant | L7, L8 on empty vectors give 1 and 1 | $y_3 \vee \neg y_3 = 1$ |
| hi | | | | $\neg y_2$ |
| lo, depth 2 | $(0, 1)$ | 0 | L6, then L5 | $\neg y_2 \wedge y_3$ |
| result | | | L9 at depth 1 | $(y_1 \wedge \neg y_2) \vee (\neg y_1 \wedge \neg y_2 \wedge y_3)$ |

The result is the set $\{100, 101, 001\}$, as the enumeration gave. On $S$, $s_1 \wedge s_2$ is 0, so $g_2 = 0$, and constrain found that. On $S$, $s_2 = \neg s_1$, so $x \vee s_2$ became $\neg s_1 \vee x$ and $s_2$ and $s_3$ left all three functions. With $S$ replaced by all 8 states, the image has 6 states: every state except 010 and 110, since $y_2 = 1$ needs $s_1 = s_2 = 1$, which forces $y_3 = 1$.

## Correctness

The method is exact. The key fact is the range property of constrain: for $c \ne 0$, the vector $g \downarrow c$ takes exactly the values $\{g(z) : c(z) = 1\}$. It holds because constrain by $c$ is composition with one map onto the points of $c$ that keeps those points fixed, the same map for every function of the vector. The [generalized cofactor](/generalized-cofactor/) page proves the composition form. With $c = S$ this gives $\mathrm{Img}(S) = \mathrm{Range}(\delta \downarrow S)$, and with $c = g_1$ and $c = \neg g_1$ it gives lines L7 and L8. Induction on the number of functions then shows that RANGE returns the range. The full proof is in [the correctness proof](proofs/correctness.md). The tests also compare each result with the relational product $\exists s, x.\ S \wedge T$ and with enumeration of all states and inputs.

## Complexity

The model is the word RAM, with hashing in expected constant time. Let $b$ be the largest number of nodes of a BDD in the run. Each call of RANGE removes one function, so the calls form a binary tree of depth at most $m$, with at most $2^{m + 1} - 1$ calls. A call does at most $2(m - 1)$ constrain operations, each $O(b^2)$ with its cache, and a constant number of applies on BDDs over $y$, also $O(b^2)$. Line L2 adds $m$ constrain operations. The total is $O(2^m m b^2)$ time, and the unique table grows by at most one node per step, which bounds the space the same way.

The $2^m$ factor is real for this simple recursion: a range with many states can need many calls. Practical versions reduce it with a cache of ranges, by splitting on a domain variable in place of an output, and by handling outputs that do not share support separately (see the variants below). Those changes are not in the pseudocode above, and no bound better than the one above is proved here. Against the relational product, the trade is this: the method never builds $T$, whose BDD can be much larger than the next-state functions, but it pays for many constrain calls.

## Properties

- Exact for every variable order; the order changes only the sizes.
- Needs only the BDDs of the next-state functions, not of $T$.
- Works for a care set $c(s, x)$ on states and inputs together, giving $\{\delta(z) : c(z) = 1\}$.
- The recursion depth is $m$.

## Variants and improvements

- **Input splitting.** Split on a variable of $s$ or $x$ in place of an output: $\mathrm{Img} = \mathrm{Range}(g|_{v=0}) \cup \mathrm{Range}(g|_{v=1})$, with [cofactors](/cofactor/). This is a [Shannon expansion](/shannon-expansion/) of the domain, not of the range.
- **Range cache.** Different branches often meet the same vector after constrain. A table of solved vectors removes repeated calls.
- **Disjoint support.** If the functions split into groups with no common variable, the range is the product of the ranges of the groups.
- **Relation-based image.** Build $T$ as a conjunction of parts and quantify $s$ and $x$ early. See [partitioned transition relation](/partitioned-transition-relation/); it is the method of most later model checkers.
- **Preimage.** The set of states that reach $S$ in one step is $\exists x.\ S(\delta(s, x))$, a [composition](/boolean-function-composition/), with no range computation.

## When to use it

Use it when the next-state functions have small BDDs but the transition relation does not, for example circuits with many latches whose next-state logic shares much structure. It also suits [sequential equivalence](/sequential-equivalence-checking/) checks of a [product machine](/product-machine/), where the next-state functions are given by the circuits. For large designs, the partitioned relation with early quantification usually won in later practice, because it can quantify inputs and state bits one group at a time. Symbolic reachability can use either; the choice changes only the cost of the image step.

## Pitfalls

- **Restrict in place of constrain at line L2.** Restrict also agrees with each function on $S$, but it does not use one common map for all functions, so the range of the vector can be too large. With $\delta = (s_1 \wedge s_2,\ s_2)$ and $S = \{00, 11\}$, restrict gives $(s_1, s_2)$, whose range is all four states, while the image is $\{00, 11\}$. Constrain gives $(s_1, s_1)$, whose range is right.
- **Constraining by 0.** Constrain by the zero function has no meaning. Line L1 handles $S = 0$, and lines L5 and L6 must come before lines L7 and L8, because a constant $g_1$ makes $g_1$ or $\neg g_1$ zero.
- **Mixing $y$ with $s$.** The output variables $y$ must be fresh. If $y_i$ is the same variable as $s_i$, line L9 builds a function of the present state mixed with the next state, and the result is wrong. Rename $y$ to $s$ only after the image is done.
- **Forgetting the inputs.** The image is over all inputs. Constraining by $S$ alone is right because $S$ does not depend on $x$; a care set that does restrict $x$ gives the image under those inputs only.

## Implementations

## History

Coudert, Berthet and Madre (1989) verified synchronous machines by symbolic execution and introduced constrain to compute the image as a range. Coudert and Madre (ICCAD 1990) put the operations on sets of states and of transitions into one framework and added restrict. Touati, Savoj, Lin, Brayton and Sangiovanni-Vincentelli (ICCAD 1990) compared the transition-function method with the transition-relation method and gave the image property of the generalized cofactor. Later work, from Burch, Clarke and Long (1991) on, mostly used partitioned relations, but range computation stayed in use for [product machines](/product-machine/) and for synthesis.

## References
