---
tag: EDCXTM
kind: data-structure
slug: kronecker-functional-decision-diagram
name: Kronecker functional decision diagram
aliases:
- KFDD
area: logic-and-constraints/binary-decision-diagrams
level: research
summary: An ordered decision diagram that picks, per variable, the Shannon, positive Davio or negative Davio expansion. With a fixed order and type list, reduced KFDDs are canonical.
model: word-ram
complexity:
  vars: {f: the number of nodes of the first argument, g: the number of nodes of the second argument, n: the number of variables}
  time: {mk: O(1) expected, xor: O(f g) expected, evaluate: O(f), from_table: O(n 2^n) expected}
  space: {nodes: O(f)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 1994
  people: [Rolf Drechsler, Amr Sarabi, Michael Theobald, Bernd Becker, Marek A. Perkowski]
  note: Drechsler, Sarabi, Theobald, Becker and Perkowski defined ordered KFDDs, which contain OBDDs and OFDDs as special cases.
prereqs: [reduced-ordered-bdd, shannon-expansion, boolean-function]
see_also: [reduced-ordered-bdd, binary-moment-diagram, shannon-expansion, reed-muller-code, variable-ordering, bdd-sifting, algebraic-decision-diagram, boolean-function]
sources:
  - paper: "Rolf Drechsler, Amr Sarabi, Michael Theobald, Bernd Becker, Marek A. Perkowski, Efficient representation and manipulation of switching functions based on ordered Kronecker functional decision diagrams, Proceedings of the 31st ACM/IEEE Design Automation Conference (DAC), 1994, pages 415 to 419"
    title: Efficient representation and manipulation of switching functions based on ordered Kronecker functional decision diagrams
    locator: the three decompositions, the decomposition type list, the reduction rules, canonicity and the operations
  - paper: "Udo Kebschull, Endric Schubert, Wolfgang Rosenstiel, Multilevel logic synthesis based on functional decision diagrams, Proceedings of the European Conference on Design Automation (EDAC), 1992, pages 43 to 47"
    title: Multilevel logic synthesis based on functional decision diagrams
    locator: functional decision diagrams with the positive Davio expansion
  - paper: "Bernd Becker, Rolf Drechsler, Ralph Werchner, On the relation between BDDs and FDDs, Information and Computation 123(2), 1995, pages 185 to 197"
    title: On the relation between BDDs and FDDs
    locator: exponential gaps between OBDDs and OFDDs in both directions, and the cost of AND on OFDDs
  - paper: "Bernd Becker, Rolf Drechsler, Michael Theobald, On the expressive power of OKFDDs, Formal Methods in System Design 11(1), 1997, pages 5 to 21"
    title: On the expressive power of OKFDDs
    locator: the size relations between OKFDDs, OBDDs and OFDDs
---

A Kronecker functional decision diagram (KFDD, or OKFDD when ordered) is an ordered [decision diagram](/decision-diagram/) of a [Boolean function](/boolean-function/) in which each variable $x_v$ has one of three decomposition types. With $f_0$ and $f_1$ the cofactors by $x_v$ and $f_2 = f_0 \oplus f_1$, the types are the [Shannon expansion](/shannon-expansion/) $f = \bar{x} f_0 \oplus x f_1$, the positive Davio expansion $f = f_0 \oplus x f_2$, and the negative Davio expansion $f = f_1 \oplus \bar{x} f_2$. The list of types, one per variable, is the decomposition type list (DTL). With only Shannon types the KFDD is the [ROBDD](/reduced-ordered-bdd/); with only positive Davio types it is the ordered functional decision diagram (OFDD) of Kebschull, Schubert and Rosenstiel (1992), whose paths to the sink 1 are the products of the positive polarity Reed-Muller form. Drechsler, Sarabi, Theobald, Becker and Perkowski (1994) defined KFDDs and showed that, for a fixed order and DTL, reduced KFDDs are canonical. A good DTL can make the diagram much smaller than both the OBDD and the OFDD.

## In plain words

A BDD splits a function on each input into two cases: input off and input on. A KFDD may instead store "the case with the input off" and "what changes when the input is turned on". The second part is often much simpler. For example, a sum of products under exclusive or loses its product terms one by one this way. For each input the user picks one of three such splitting rules, and the choice is fixed for the whole diagram. With the order and the choices fixed, each function has exactly one diagram, so equal functions give the same diagram. The best choices depend on the function, and finding them is a search, like finding a good order of the inputs.

## The abstract type

The variables are $x_1, \ldots, x_n$ in this order, and $d = (d_1, \ldots, d_n) \in \{\mathrm{S}, \mathrm{pD}, \mathrm{nD}\}^n$ is the DTL. A node $u$ stands for a function $f_u : \{0, 1\}^n \to \{0, 1\}$.

| operation | result |
|---|---|
| MK$(v, lo, hi)$ | the function $b_{d_v, 0}(x_v) f_{lo} \oplus b_{d_v, 1}(x_v) f_{hi}$ |
| FROM-TABLE$(T)$ | the node of the function with the truth table $T$ |
| EVALUATE$(f, x)$ | $f(x)$ |
| XOR$(f, g)$ | $f \oplus g$ |
| EQUAL$(f, g)$ | whether $f = g$, by comparing ids |

Each type has a pair of basis functions $b_{t, 0}, b_{t, 1}$ of one variable, and its children are the coefficients:

| type | expansion | $b_{t, 0}, b_{t, 1}$ | $(lo, hi)$ | removed if |
|---|---|---|---|---|
| S | $\bar{x} f_0 \oplus x f_1$ | $\bar{x}, x$ | $(f_0, f_1)$ | $lo = hi$ |
| pD | $f_0 \oplus x f_2$ | $1, x$ | $(f_0, f_2)$ | $hi = 0$ |
| nD | $f_1 \oplus \bar{x} f_2$ | $1, \bar{x}$ | $(f_1, f_2)$ | $hi = 0$ |

Over GF(2), these coefficient maps are the matrices $\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$, $\begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$ and $\begin{pmatrix} 0 & 1 \\ 1 & 1 \end{pmatrix}$ applied to $(f_0, f_1)$. The whole truth table is transformed by their Kronecker product, which gives the name.

## Representation

Node 0 and node 1 are the two sinks. An inner node $(v, lo, hi)$ has both children on later levels and has the function in the first table. MK keeps three rules with a unique table:

- **Shannon elimination.** For $d_v = \mathrm{S}$, if $lo = hi$, return $lo$.
- **Davio elimination.** For $d_v \in \{\mathrm{pD}, \mathrm{nD}\}$, if $hi$ is the sink 0, return $lo$. Then $f_2 = 0$, so $f$ does not depend on $x_v$.
- **Merging.** If $(v, lo, hi)$ is stored, return the stored node.

In both elimination cases the function $b_{t,0} f_{lo} \oplus b_{t,1} f_{hi}$ equals $f_{lo}$, so MK returns a node of the right function. A Davio node with $lo = hi$ stays: for pD it stands for $(1 \oplus x) f_{lo} = \bar{x} f_{lo}$.

## Operations

```pseudo id=main
MK(v, lo, hi)
L1  if d_v = S and lo = hi then return lo                    ▷ Shannon elimination
L2  if d_v ∈ {pD, nD} and hi = 0 then return lo               ▷ Davio elimination
L3  if U holds (v, lo, hi) then return U[v, lo, hi]          ▷ merging
L4  otherwise make a new node u with U[v, lo, hi] ← u, and return u

FROM-TABLE(T)        ▷ T[a] = f(x), where bit v − 1 of a is x_v
L5  for v ← 1 to n, for each a with bit v − 1 equal to 0: (T[a], T[a + 2^{v−1}]) ← (lo, hi) of the type d_v, from (f_0, f_1) = (T[a], T[a + 2^{v−1}])
L6  layer ← the sinks T[0], ..., T[2^n − 1]; for v ← n down to 1 do; at the end return layer[0]
L7      layer ← (MK(v, layer[a], layer[a + 2^{v−1}]) for a ← 0 to 2^{v−1} − 1)

EVALUATE(u, x)       ▷ one pass over the nodes reachable from u, children first
L8  val[w] ← (x_v ? val[hi] : val[lo]) for S, val[lo] ⊕ x_v val[hi] for pD, val[lo] ⊕ (1 − x_v) val[hi] for nD; return val[u]
```

**XOR$(f, g)$** works child by child, since all three coefficient maps are linear over GF(2): if $f = b_0 f_{lo} \oplus b_1 f_{hi}$ and $g = b_0 g_{lo} \oplus b_1 g_{hi}$, then $f \oplus g = b_0 (f_{lo} \oplus g_{lo}) \oplus b_1 (f_{hi} \oplus g_{hi})$. With a cache it makes at most $\lvert f \rvert \cdot \lvert g \rvert$ calls, as [apply](/bdd-apply/) does on BDDs. A node on a later level has the parts $(u, u)$ for an S variable and $(u, 0)$ for a Davio variable.

**AND** is harder. For a pD variable, $(f_0 \oplus x f_2)(g_0 \oplus x g_2) = f_0 g_0 \oplus x (f_0 g_2 \oplus f_2 g_0 \oplus f_2 g_2)$, which needs XORs of recursive results, and the time is not bounded by the product of the sizes. Becker, Drechsler and Werchner (1995) showed that AND on OFDDs can produce exponential output from inputs of polynomial size.

## Example

Let $f = x_1 x_2 \oplus x_3 x_4$.

**Shannon only.** The ROBDD has a node for $x_1$, a node for $x_2$, nodes for $x_3 x_4$ and for its complement on the levels $x_3$ and $x_4$, and two sinks: 8 nodes.

**Positive Davio only.** At $x_1$: $f_0 = x_3 x_4$ and $f_2 = x_2$. The node $x_3 x_4$ skips $x_2$ by Davio elimination, since it does not depend on $x_2$, and becomes $(x_3, 0, (x_4, 0, 1))$. The node $x_2$ is $(x_2, 0, 1)$. That is 4 inner nodes and 2 sinks: 6 nodes. The paths to the sink 1 that take $hi$ at the variables of a set $S$ give the products $x_1 x_2$ and $x_3 x_4$, the Reed-Muller form of $f$.

**The DTL (S, pD, nD, nD).** Take the root $(x_1, A, B)$ with the Shannon type.

- $A = x_3 x_4$. The variable $x_2$ is skipped. At $x_3$ (nD), $f_1 = x_4$ and $f_2 = 0 \oplus x_4 = x_4$, so $A = (x_3, C, C)$ with $C = x_4$. At $x_4$ (nD), $f_1 = 1$ and $f_2 = 1$, so $C = (x_4, 1, 1)$.
- $B = x_2 \oplus x_3 x_4$. At $x_2$ (pD), $f_0 = x_3 x_4 = A$ and $f_2 = 1$, so $B = (x_2, A, 1)$.

The diagram has the 4 inner nodes root, $A$, $B$, $C$, and only the sink 1 is reachable: 5 nodes. **EVALUATE at $x = (1, 1, 1, 1)$**: $C = 1 \oplus 0 \cdot 1 = 1$, $A = C \oplus 0 \cdot C = 1$, $B = A \oplus 1 \cdot 1 = 0$, and the root takes $B$ since $x_1 = 1$. So $f = 0$, which is $1 \oplus 1$.

**Measured sizes** over all $3^n$ DTLs for the order $x_1, \ldots, x_n$, computed with the code of this page. The parity of products is $x_1 x_2 \oplus x_3 x_4 \oplus \cdots$; hwb is the [hidden weighted bit](/hidden-weighted-bit-lower-bound/) function; the random function uses the seed 6; and-or is $x_1 x_2 \lor x_3 x_4 \lor x_5 x_6$.

| function | $n$ | all S | all pD | all nD | best DTL |
|---|---|---|---|---|---|
| parity of products | 4 | 8 | 6 | 8 | 5 |
| parity of products | 6 | 12 | 8 | 9 | 7 |
| parity of products | 8 | 16 | 10 | 14 | 9 |
| hwb | 6 | 25 | 22 | 25 | 22 |
| hwb | 8 | 57 | 58 | 64 | 54 |
| random | 6 | 27 | 27 | 25 | 24 |
| and-or | 6 | 8 | 10 | 11 | 7 |

No single type is best for every function. In six of the seven rows the best DTL is smaller than all three pure DTLs, so it mixes types; for hwb with $n = 6$, all pD is already best. These are small cases and give no general bound.

## Correctness

For each type, the pair $(lo, hi)$ in the table is the only pair of functions without $x_v$ with $f = b_{t,0} \, lo \oplus b_{t,1} \, hi$: set $x_v$ to 0 and to 1 and solve. Also $f$ depends on $x_v$ exactly when the elimination condition fails. With these two facts the induction of [BDD canonicity](/bdd-canonicity/) goes through for a fixed order and DTL: every node depends on its variable, and two nodes with the same function have the same children, so they are merged. FROM-TABLE is correct because line L5 applies the Kronecker transform one coordinate at a time, and the loop of lines L6 and L7 then builds the expansion bottom-up. The full proofs are in [the proof file](proofs/correctness.md).

## Complexity

| operation | time | notes |
|---|---|---|
| MK | $O(1)$ expected | one hash lookup |
| XOR$(f, g)$ | $O(\lvert f \rvert \cdot \lvert g \rvert)$ expected | each pair of nodes once |
| AND$(f, g)$ | exponential in the worst case for Davio types | see above |
| EVALUATE | $O(\lvert f \rvert)$ | a Davio node can need both children |
| FROM-TABLE | $O(n 2^n)$ expected | the transform and $2^n - 1$ calls of MK |
| space | $O(\lvert f \rvert)$ | three fields per node |

For a DTL with only S types, EVALUATE follows one path in $O(n)$ time.

## Variants

- **OBDDs and OFDDs** are the DTLs with all S and all pD. An OFDD with complemented variables per position (pD or nD) is a fixed-polarity Reed-Muller diagram.
- **Choosing the DTL.** The DTL is a second parameter next to the [variable order](/variable-ordering/). Drechsler and Becker extended [sifting](/bdd-sifting/) to change the type of a level as well as its position; changing the type of the bottom level, or exchanging two adjacent levels of any types, are local operations.
- **Other decompositions.** Becker and Drechsler argued that, up to complement and the role of the children, S, pD and nD are the only decompositions over GF(2) that give essentially different diagrams.
- **Word-level analogues.** [BMDs](/binary-moment-diagram/) use the moment decomposition $f = f_0 + x (f_1 - f_0)$ over the integers, which is the integer form of the positive Davio type. Hybrid decision diagrams and K*BMDs mix decompositions for integer functions.

## When to use it

Use KFDDs when a function has many exclusive-or parts, as in arithmetic, parity and coding circuits, or when a Reed-Muller form is the goal of logic synthesis: the paths of a Davio diagram give an exclusive-or sum of products, which suits synthesis for circuits with XOR gates and their testability. For equivalence checking with many AND operations, plain OBDDs are safer, since AND is polynomial for them and not for Davio types. The [Reed-Muller codes](/reed-muller-code/) use the same algebra of products over GF(2).

## Pitfalls

- **The DTL is part of the key.** Two KFDDs are comparable by ids only if they use the same order and the same DTL.
- **Two elimination rules.** A Davio node with equal children is not redundant, and an S node with $hi = 0$ is not redundant either. Using the wrong rule breaks canonicity.
- **EVALUATE is not a path.** On a Davio node with $x_v = 1$ for pD, or $x_v = 0$ for nD, the value is the XOR of both children.
- **AND can blow up.** Plan operations around XOR, or convert to an OBDD for conjunctions.
- **The search space is large.** There are $3^n$ DTLs for each of the $n!$ orders, so tools search them with local moves and give measured results only.

## Implementations

## History

Kebschull, Schubert and Rosenstiel (1992) introduced functional decision diagrams, based on the positive Davio expansion, for multilevel logic synthesis. Becker, Drechsler and Werchner (1995) compared OBDDs and OFDDs and found exponential gaps in both directions. Drechsler, Sarabi, Theobald, Becker and Perkowski (1994) defined ordered KFDDs with one of three decompositions per variable, gave the reduction rules and canonicity, and built the package PUMA. Becker, Drechsler and Theobald (1997) studied the expressive power of OKFDDs, and Drechsler and Becker gave dynamic methods to choose the order and the DTL together.

## References
