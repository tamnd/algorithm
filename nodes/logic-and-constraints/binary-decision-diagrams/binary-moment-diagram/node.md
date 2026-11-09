---
tag: NFC4FF
kind: data-structure
slug: binary-moment-diagram
name: Binary moment diagram
aliases:
- BMD
area: logic-and-constraints/binary-decision-diagrams
level: research
summary: A canonical diagram for functions from bits to integers, built on the moment decomposition f = f_0 + x (f_1 - f_0). Integer multiplication X Y has a BMD of quadratic size.
model: word-ram
complexity:
  vars: {f: the number of nodes of the first argument, g: the number of nodes of the second argument, n: the number of variables}
  time: {mk: O(1) expected, add: O(f g) expected, evaluate: O(f), from_table: O(n 2^n) expected}
  space: {nodes: O(f)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 1995
  people: [Randal E. Bryant, Yirng-An Chen]
  note: Bryant and Chen introduced BMDs and their weighted form *BMDs to verify multipliers and other arithmetic circuits at the word level.
prereqs: [reduced-ordered-bdd, algebraic-decision-diagram, shannon-expansion]
see_also: [algebraic-decision-diagram, kronecker-functional-decision-diagram, multiplier-bdd-lower-bound, reduced-ordered-bdd, boolean-equivalence-checking, zero-suppressed-bdd, fast-walsh-hadamard-transform, bdd-apply]
sources:
  - paper: "Randal E. Bryant, Yirng-An Chen, Verification of arithmetic circuits with binary moment diagrams, Proceedings of the 32nd ACM/IEEE Design Automation Conference (DAC), 1995, pages 535 to 541"
    title: Verification of arithmetic circuits with binary moment diagrams
    locator: the moment decomposition, BMDs and *BMDs, the operations, and the sizes for words, sums and products
  - paper: "Randal E. Bryant, Yirng-An Chen, Verification of arithmetic circuits using binary moment diagrams, International Journal on Software Tools for Technology Transfer 3(2), 2001, pages 137 to 155"
    title: Verification of arithmetic circuits using binary moment diagrams
    locator: the journal version, with hierarchical verification of multipliers
  - paper: "Edmund M. Clarke, Masahiro Fujita, Xudong Zhao, Hybrid decision diagrams, overcoming the limitations of MTBDDs and BMDs, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 1995, pages 159 to 163"
    title: Hybrid decision diagrams
    locator: the comparison of MTBDDs and BMDs, and diagrams that mix the decompositions
---

A binary moment diagram (BMD) represents a function $f : \{0, 1\}^n \to \mathbb{Z}$ with the moment decomposition in place of the [Shannon expansion](/shannon-expansion/). For the top variable $x$, write $f = f_0 + x \cdot (f_1 - f_0)$, where $f_0$ and $f_1$ are the cofactors. The node stores the *constant moment* $f_0$ and the *linear moment* $f_1 - f_0$. Unfolded fully, a BMD lists the coefficients of the unique multilinear polynomial of $f$, shared as a graph. The reduction rules are: drop a node whose linear moment is the constant 0, and merge equal nodes. Then reduced BMDs are canonical for a fixed order. Bryant and Chen (1995) introduced BMDs to verify arithmetic circuits: a word $X = \sum_i 2^i x_i$ has a BMD of linear size, and the product $X \cdot Y$ has a BMD of size $w^2 + 3w$ for $w$-bit words, while every [OBDD](/reduced-ordered-bdd/) of the middle output bit has exponential size ([multiplier lower bound](/multiplier-bdd-lower-bound/)). With edge weights (*BMDs), $X \cdot Y$ has linear size.

## In plain words

A BMD stores a number-valued function of yes-or-no inputs as a sum of simple terms. Each term is a whole number times a product of some inputs, such as $6 \cdot x_1 x_3$. Every such function has exactly one such sum. The diagram walks over the inputs in a fixed order and, for each input, splits the terms into those without it and those with it. Equal parts are stored once, and an input with no terms is skipped. The product of two binary numbers has only a few kinds of terms, so its diagram stays small. A diagram that gives each output bit of the product as a separate yes-or-no function must be very large. This is why BMDs help to check multiplier circuits.

## The abstract type

The variables are $x_1, \ldots, x_n$ in this order. A node $u$ stands for a function $f_u : \{0, 1\}^n \to \mathbb{Z}$.

| operation | result |
|---|---|
| CONST$(k)$ | the constant function $k$ |
| MK$(v, c, l)$ | the function $f_c + x_v \cdot f_l$ |
| FROM-TABLE$(T)$ | the node of the function with the value table $T$ |
| EVALUATE$(f, x)$ | $f(x)$ |
| ADD$(f, g)$ | $f + g$ |
| MUL$(f, g)$ | $f \cdot g$ |
| EQUAL$(f, g)$ | whether $f = g$, by comparing ids |

Every $f$ has exactly one multilinear form

$$f(x) = \sum_{S \subseteq \{1, \ldots, n\}} C_f(S) \prod_{i \in S} x_i, \qquad C_f(S) = \sum_{T \subseteq S} (-1)^{\lvert S \rvert - \lvert T \rvert} f(\mathbf{1}_T),$$

where $\mathbf{1}_T$ is the input with $x_i = 1$ exactly for $i \in T$. The coefficients $C_f$ are the *moments* of $f$. The map from $f$ to $C_f$ is the Möbius transform over the subsets, with the inverse $f(\mathbf{1}_T) = \sum_{S \subseteq T} C_f(S)$.

## Representation

A sink $(n + 1, k)$ stores one integer $k$. An inner node $(v, c, l)$ stores the constant moment $c$ and the linear moment $l$, both on later levels, and stands for $f_c + x_v \cdot f_l$. MK keeps two rules with a unique table:

- **Zero linear moment.** If $l$ is the sink 0, return $c$, since $f_c + x_v \cdot 0 = f_c$.
- **Merging.** If $(v, c, l)$ is stored, return the stored node.

So a node is dropped when $f$ does not depend on $x_v$, which is when $f_1 - f_0 = 0$. A node whose two edges are equal stays: $c = l$ means $f = (1 + x_v) f_c$, which depends on $x_v$. This is the difference from the BDD rule.

A path that takes the $l$ edge exactly at the variables of $S$ and the $c$ edge at the other tested variables ends at the sink $C_f(S)$. A variable skipped by the path contributes through its $c$ edge, since its linear moment is 0. Evaluation therefore sums over many paths, not one: $f(x)$ is the sum of the sinks of all paths that take $l$ edges only at variables with $x_i = 1$.

## Operations

Let $\mathrm{mom}(u, v)$ be $(c, l)$ if $u = (v, c, l)$, and $(u, 0)$ if $u$ is on a later level.

```pseudo id=main
MK(v, c, l)
L1  if l is the sink 0 then return c                        ▷ zero linear moment
L2  if U holds (v, c, l) then return U[v, c, l]              ▷ merging
L3  otherwise make a new node u with U[v, c, l] ← u, and return u

FROM-TABLE(T)        ▷ first replace T by its moments C, by the Möbius transform
L4  layer ← the sinks C[0], ..., C[2^n − 1]; for v ← n down to 1 do; at the end return layer[0]
L5      layer ← (MK(v, layer[a], layer[a + 2^{v−1}]) for a ← 0 to 2^{v−1} − 1)

EVALUATE(u, x)       ▷ one pass over the nodes reachable from u, children first
L6  val[w] ← k for a sink (n + 1, k), and val[w] ← val[c] + x_v · val[l] for w = (v, c, l); return val[u]

ADD(f, g)            ▷ results are cached under {f, g}
L7  if f and g are sinks then return CONST(k_f + k_g)
L8  v ← min(var(f), var(g)); (a, b) ← mom(f, v); (c, d) ← mom(g, v); return MK(v, ADD(a, c), ADD(b, d))

MUL(f, g)            ▷ cached under {f, g}; v, (a, b), (c, d) as in ADD
L9  if f and g are sinks then return CONST(k_f · k_g)
L10 lin ← ADD(ADD(MUL(a, d), MUL(b, c)), MUL(b, d))
L11 return MK(v, MUL(a, c), lin)
```

ADD uses that the moments of a sum are the sums of the moments. MUL uses $x_v^2 = x_v$ on $\{0, 1\}$:

$$(a + x_v b)(c + x_v d) = ac + x_v (ad + bc + bd).$$

The transform before line L4 is the in-place Möbius transform: for each bit $i$ and each index $a$ with bit $i$ set, $C[a] \leftarrow C[a] - C[a \oplus 2^i]$. It has the same loop structure as the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/), with $O(n 2^n)$ steps.

## Example

Take $w = 2$, $X = x_1 + 2 x_2$ and $Y = x_3 + 2 x_4$, with the order $x_1, x_2, x_3, x_4$.

**The word $X$.** The constant moment by $x_1$ is $2 x_2$ and the linear moment is 1. So $X = (x_1, A, 1)$ with $A = (x_2, 0, 2)$. This is 2 inner nodes and the sinks 0, 1, 2, so $2w + 1 = 5$ nodes. In the same way $Y = (x_3, B, 1)$ with $B = (x_4, 0, 2)$.

**MUL$(X, Y)$.** Line L8 gives $v = 1$, $(a, b) = (A, 1)$ and $(c, d) = (Y, 0)$.

- Line L10: MUL$(A, 0) = 0$, MUL$(1, Y) = Y$ and MUL$(1, 0) = 0$, so $\mathit{lin} = Y$.
- Line L11 calls MUL$(A, Y)$. There $v = 2$, $(a, b) = (0, 2)$ and $(c, d) = (Y, 0)$. Line L10 gives $\mathit{lin} = $ MUL$(2, Y)$, which is $2Y = (x_3, (x_4, 0, 4), 2)$ by the same rules. Line L11 returns $P = (x_2, 0, 2Y)$, since MUL$(0, Y) = 0$.
- The result is $(x_1, P, Y)$.

The product $XY = x_1 x_3 + 2 x_1 x_4 + 2 x_2 x_3 + 4 x_2 x_4$ has 6 inner nodes, namely the root, $P$, $Y$, $B$, $2Y$ and $(x_4, 0, 4)$, and the sinks 0, 1, 2, 4. That is $10 = w^2 + 3w$ nodes. The path that takes $l$ at $x_2$ and at $x_4$ goes root, $P$, $2Y$, $(x_4, 0, 4)$, and ends at the sink 4, which is $C(\{2, 4\})$.

**EVALUATE at $x = (1, 1, 0, 1)$.** Bottom-up: $B = 0 + 1 \cdot 2 = 2$, $Y = B + 0 \cdot 1 = 2$, the node $(x_4, 0, 4)$ gives 4, $2Y = 4$, $P = 0 + 1 \cdot 4 = 4$, and the root gives $4 + 1 \cdot 2 = 6$. Indeed $X = 3$ and $Y = 2$.

**Measured sizes** of $X \cdot Y$ for $w$-bit words, with the $X$ bits before the $Y$ bits (computed with the code of this page and an ADD package):

| $w$ | ADD of $X \cdot Y$ | BMD of $X \cdot Y$ | BMD of $X$ |
|---|---|---|---|
| 1 | 4 | 4 | 3 |
| 2 | 19 | 10 | 5 |
| 3 | 82 | 18 | 7 |
| 4 | 330 | 28 | 9 |
| 5 | 1332 | 40 | 11 |

An [ADD](/algebraic-decision-diagram/) needs one sink per value of the product, so it grows exponentially. The BMD has $w^2 + 3w$ nodes; the proof file shows this for all $w$.

## Correctness

**Canonicity.** The map $f \mapsto (f_0, f_1 - f_0)$ is a bijection from the functions on levels $v$ and above to the pairs of functions on later levels, with the inverse $(c, l) \mapsto c + x_v l$. And $f$ depends on $x_v$ if and only if its linear moment is not 0. With these two facts, the induction of [BDD canonicity](/bdd-canonicity/) goes through: every node depends on its variable, and two nodes with the same function have the same moments, so the merging rule makes them one node. **ADD** and **MUL** are correct by the moment identities above. **FROM-TABLE** is correct because the Möbius transform gives $C_f$ and the bottom-up loop builds a node for each block of coefficients. The full proofs, and the size $w^2 + 3w$ of $X \cdot Y$, are in [the proof file](proofs/correctness.md).

## Complexity

| operation | time | notes |
|---|---|---|
| MK, CONST | $O(1)$ expected | one hash lookup |
| ADD$(f, g)$ | $O(\lvert f \rvert \cdot \lvert g \rvert)$ expected | each pair of nodes once |
| MUL$(f, g)$ | no general polynomial bound is given here | each pair once, but each step runs ADD on intermediate results |
| EVALUATE | $O(\lvert f \rvert)$ | all reachable nodes, not one path |
| FROM-TABLE | $O(n 2^n)$ expected | the transform and $2^n - 1$ calls of MK |
| space | $O(\lvert f \rvert)$ | three fields per node |

The sinks hold integers that can be large: the moments of a product of words go up to $2^{2w - 2}$, so arithmetic on them costs more than $O(1)$ for wide words.

## Variants

- ***BMDs.** Bryant and Chen also gave BMDs with multiplicative weights on the edges, normalized so that each function has one form. Common factors such as the $2^i$ of a word move into the weights, and then $X$, $X + Y$, $X \cdot Y$ and $2^X$ have *BMDs of linear size.
- **Hybrid decision diagrams** (Clarke, Fujita and Zhao, 1995) choose for each variable one of several decompositions, Shannon, moment and others, in the manner of [KFDDs](/kronecker-functional-decision-diagram/).
- **K*BMDs** (Drechsler, Becker and Ruppertz, 1996) combine the Kronecker choice of decompositions with additive and multiplicative weights.
- **Taylor expansion diagrams** (Ciesielski, Kalla and Askar, 2006) carry the idea to polynomials over integer words, with a Taylor expansion per word variable.
- **ADDs and EVBDDs.** An [ADD](/algebraic-decision-diagram/) uses the Shannon expansion for integer functions; an EVBDD (Lai and Sastry, 1992) adds additive edge weights to it. For a 0-1 valued $f$, the BMD is the integer analogue of the positive Davio form of [KFDDs](/kronecker-functional-decision-diagram/), where the subtraction is over the integers and not modulo 2.

## When to use it

Use BMDs and *BMDs for word-level verification of arithmetic circuits: adders and multipliers, where the specification $X \cdot Y$ is small as a BMD and the bit-level OBDDs are not. A common method checks the circuit block by block, comparing each block to a word-level specification, and then composes the specifications. BMDs fit linear and polynomial word functions. For comparisons, bit-level control logic and other 0-1 valued functions, OBDDs are often smaller. Today, the verification of multipliers also uses computer algebra on polynomial forms, which shares the idea of exact integer coefficients.

## Pitfalls

- **Evaluation is not a path.** A node with $x_v = 1$ adds both children, so EVALUATE visits all nodes. The test with one path, as in BDDs, gives wrong results.
- **The reduction rule differs from BDDs.** Drop a node when its linear moment is 0, not when its two edges are equal. A node with $c = l$ stands for $(1 + x_v) f_c$.
- **MUL can be slow.** Each step calls ADD on intermediate results, and products of general BMDs can grow fast. Bryant and Chen built BMDs of multipliers from word-level parts, not by multiplying bit by bit through the gates.
- **Big integers.** The sinks hold exact integers. A fixed-width integer type overflows for words wider than about 31 bits.
- **0-1 results.** A BMD of a 0-1 valued function is exact, but it is not the same graph as the BDD, and its size can be different. Measure both before you choose.

## Implementations

## History

Bryant and Chen (1995) introduced BMDs and *BMDs at the Design Automation Conference, with hierarchical verification of multipliers and other arithmetic circuits; the journal version appeared in 2001. The work followed Bryant's 1991 proof that OBDDs of multiplication are exponential. Clarke, Fujita and Zhao (1995) compared BMDs and MTBDDs and proposed hybrid decision diagrams. Drechsler, Becker and Ruppertz (1996) gave K*BMDs. Chen and Bryant later gave power hybrid decision diagrams for floating-point circuits, and Ciesielski, Kalla and Askar (2006) gave Taylor expansion diagrams.

## References
