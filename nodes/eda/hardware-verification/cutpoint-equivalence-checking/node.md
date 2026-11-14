---
tag: MX8Z1M
kind: algorithm
slug: cutpoint-equivalence-checking
name: Cutpoint-based equivalence checking
aliases:
- Kuehlmann-Krohm equivalence checking
- internal equivalence checking
area: eda/hardware-verification
level: advanced
summary: Kuehlmann and Krohm's method that finds equivalent internal nodes of two circuits, proves them and uses them as cut points so that hard outputs split into easy parts.
solves: [boolean-equivalence-checking]
model: word-ram
complexity:
  vars: {N: "the number of gates and gate inputs of both circuits", n: the number of primary inputs, C: the number of cut variables, P: the number of compared node pairs}
  time: {worst: "O((N + P C) 4^(n + C))"}
  space: {extra: "O((N + P C) 4^(n + C))"}
properties: {deterministic: true, exact: true, complete: true, recursive: true}
history:
  year: 1997
  people: [Andreas Kuehlmann, Florian Krohm]
  note: Berman and Trevillyan used internal equivalent points as cuts in 1989. Kuehlmann and Krohm combined BDDs, structural hashing, many cut frontiers and the removal of false negatives in 1997.
prereqs: [miter-circuit, boolean-equivalence-checking, reduced-ordered-bdd, bdd-compose]
see_also: [sat-sweeping, and-inverter-graph, signal-correspondence, boolean-function-composition, observability-dont-care, dont-care-condition, bit-parallelism, hash-consing]
sources:
  - paper: "Andreas Kuehlmann and Florian Krohm, Equivalence checking using cuts and heaps, Proceedings of the 34th Design Automation Conference, 263 to 268, 1997"
    title: A. Kuehlmann and F. Krohm, Equivalence checking using cuts and heaps, DAC 1997, 263 to 268
    locator: the cut frontiers, the BDDs over cut variables, and the elimination of false negatives by composition
  - paper: doi:10.1109/ICCAD.1989.76990
    title: C. L. Berman and L. H. Trevillyan, Functional comparison of logic designs for VLSI circuits, ICCAD 1989, 456 to 459
    locator: equivalent internal points used as cut points that split the two circuits
  - paper: "Daniel Brand, Verification of large synthesized designs, Proceedings of the International Conference on Computer-Aided Design, 534 to 537, 1993"
    title: D. Brand, Verification of large synthesized designs, ICCAD 1993, 534 to 537
    locator: internal equivalences found by test generation on a miter, and the replacement of proved points
  - paper: doi:10.1109/TCAD.2002.804386
    title: A. Kuehlmann, V. Paruthi, F. Krohm and M. K. Ganai, Robust Boolean reasoning for equivalence checking and functional property verification, IEEE Transactions on Computer-Aided Design 21(12), 1377 to 1394, 2002
    locator: the later engine that interleaves structural hashing, simulation, SAT and BDD sweeping
  - book: doi:10.1007/978-1-4615-0817-5_13
    title: A. Kuehlmann and C. A. J. van Eijk, Combinational and sequential equivalence checking, in S. Hassoun and T. Sasao (editors), Logic Synthesis and Verification, Kluwer, 2002, 343 to 372
    locator: the section on combinational equivalence checking with cut points and false negatives
---

Cutpoint-based equivalence checking decides [Boolean equivalence](/boolean-equivalence-checking/) of two combinational circuits that have much structure in common, as after logic synthesis. It finds internal nodes of the two circuits that compute the same function, proves each such pair with a [BDD](/reduced-ordered-bdd/), and then puts a fresh variable, the cut variable, in place of the pair. Later BDDs are built over the cut variables, so they stay small. A cut can hide the relation between the cut node and the other inputs, and then a difference of two nodes can look real while it is not. This is a false negative. The method resolves it by moving the cut back toward the primary inputs, through [composition](/bdd-compose/), until the difference is 0 or is a real counterexample.

## In plain words

Two circuits that should do the same work are often almost the same inside. So the checker proves equality in small steps, from the inputs to the outputs. Quick random simulation shows which inside wires probably carry the same signal. The checker proves one such pair at a time. When a pair is proved, it gets a new name, and the rest of the work treats that name as if it were a new input. Each later check then only looks at the logic between the named wires, which is small.

The new names forget one thing: how the named wire depends on the real inputs. So a check can show a difference that no real input can cause. When that happens, the checker puts back what a name stands for, one name at a time, until the difference goes away or is real.

## The problem

The input is two combinational circuits $A$ and $B$ on the same primary inputs $x = (x_1, \ldots, x_n)$, with outputs paired as $(o_1, o_1'), \ldots, (o_k, o_k')$. The output is "equivalent" if $o_j(x) = o_j'(x)$ for every $j$ and every $x \in \{0, 1\}^n$, and otherwise an input vector on which some pair differs. This is the [Boolean equivalence checking](/boolean-equivalence-checking/) problem, the check that the [miter](/miter-circuit/) of $A$ and $B$ is 0 for every input. It is coNP-complete, so no method is fast on every input unless P = NP. This method is fast when the circuits share many internal equivalent nodes.

A *cut* is a set of nodes whose values are given names, the cut variables. Each cut variable $v$ stores its *definition* $\mathrm{def}(v)$, the BDD of its node over the variables that existed before it. The *cut miter* of two nodes is the XOR of their BDDs over the current cut variables.

## The algorithm

```pseudo id=main
CUTPOINT-EC(A, B, pairs)
L1  give each primary input a BDD variable, which is its own cut variable
L2  simulate A and B on W random input vectors; sig(u) ← the W values of node u
L3  for each gate u of A, then of B, in topological order do
L4      R(u) ← the gate of u applied to F of its fanins
L5      F(u) ← R(u)
L6      if an earlier node r has sig(r) = sig(u) then          (r is the first such node)
L7          if RESOLVE(R(u) ⊕ R(r)) = 0 then
L8              if r has no cut variable then make a fresh variable v_r; def(v_r) ← R(r); F(r) ← v_r
L9              F(u) ← v_r
L10 for each pair (o, o') do
L11     G ← RESOLVE(F(o) ⊕ F(o'))
L12     if G ≠ 0 then return "different", a satisfying assignment of G
L13 return "equivalent"

RESOLVE(G)
L14 while G ≠ 0 and the support of G has a cut variable do
L15     v ← the cut variable in the support of G with the largest index
L16     G ← G with v replaced by def(v)
L17 return G
```

Line L2 is cheap [bit-parallel](/bit-parallelism/) simulation. It only proposes pairs, the candidates; it proves nothing. Lines L4 and L5 build the BDD of the node over the current cut. Line L6 looks up the first node with the same simulation values, so each group of candidates has one representative.

Line L7 checks the pair. The difference $R(u) \oplus R(r)$ is a cut miter. If it is 0 at once, the pair is equal. If it is not 0 but depends on cut variables, it may be a false negative, so RESOLVE moves the cut back. Line L16 substitutes for the newest cut variable in the difference the function that it names. The definition of a cut variable uses only older variables, so the newest cut variable in the support goes down at each step, and the loop ends. When only primary inputs remain, a nonzero difference is real.

Lines L8 and L9 make the cut. The representative gets a cut variable if it has none, and both nodes use that variable from now on. A primary input is its own cut variable, so a node equal to an input becomes that input. Lines L10 to L12 do the same check on the output pairs. A nonzero result there has primary inputs only, so any satisfying assignment is a real counterexample.

## Example

Take inputs $a, b$. Circuit $A$ has the gate $g = a \wedge b$ and the outputs $(g, a)$. Circuit $B$ has $p = \neg a$, $q = \neg b$, $r = p \vee q$, $z = \neg r$, $w = z \vee a$ and the outputs $(z, w)$. So $z = a \wedge b$ and $w = (a \wedge b) \vee a = a$, and the circuits are equivalent. The signature of a node is its value on the four vectors $ab = 00, 01, 10, 11$.

| step | node | function | sig | $R(u)$ over the current cut | first node with this sig | RESOLVE | $F(u)$ |
|---|---|---|---|---|---|---|---|
| L1 | $a$, $b$ | inputs | 0011, 0101 | $a$, $b$ | themselves | none | $a$, $b$ |
| 1 | $g$ | $a \wedge b$ | 0001 | $a \wedge b$ | $g$ | none | $a \wedge b$ |
| 2 | $p$ | $\neg a$ | 1100 | $\neg a$ | $p$ | none | $\neg a$ |
| 3 | $q$ | $\neg b$ | 1010 | $\neg b$ | $q$ | none | $\neg b$ |
| 4 | $r$ | $\neg a \vee \neg b$ | 1110 | $\neg a \vee \neg b$ | $r$ | none | $\neg a \vee \neg b$ |
| 5 | $z$ | $a \wedge b$ | 0001 | $a \wedge b$ | $g$ | $0$ at once | $v$, a new cut variable with $\mathrm{def}(v) = a \wedge b$; also $F(g) = v$ |
| 6 | $w$ | $a$ | 0011 | $v \vee a$ | $a$ | $(v \vee a) \oplus a = v \wedge \neg a$, then $v := a \wedge b$ gives $0$ | $a$ |

At step 6 the cut miter $v \wedge \neg a$ is satisfied by $v = 1, a = 0$. No input vector gives that point: $v = 1$ means $a = b = 1$. This is the false negative. The cut at $z$ hid the fact that $z = 1$ forces $a = 1$, a [don't care](/dont-care-condition/) of $w$ seen from the cut. Composing $\mathrm{def}(v) = a \wedge b$ into the cut miter gives $((a \wedge b) \vee a) \oplus a = 0$, so the pair is equal and $w$ becomes the variable $a$.

At lines L10 to L12, the pair $(g, z)$ has $F(g) \oplus F(z) = v \oplus v = 0$ and the pair $(a, w)$ has $a \oplus a = 0$. The answer is "equivalent", with 2 merges and 1 false negative. If $w$ were $z \vee b$ instead, then $w = b$. Step 6 would merge $w$ with the input $b$ after the same kind of false negative, $v \wedge \neg b$. The output pair $(a, w)$ would then give $a \oplus b$, a BDD over primary inputs only, and line L12 would return the real counterexample $a = 0, b = 1$.

## Correctness

The answer is exact: "equivalent" if and only if every output pair computes the same function, and a returned vector always separates a pair. The key fact is that substitution keeps meaning. Read each cut variable as the function of primary inputs that its definition gives. Then every BDD $R(u)$ and $F(u)$ means the true function of $u$, and RESOLVE never changes the meaning of its argument. RESOLVE stops only at 0 or at a BDD with primary inputs only, and such a BDD means itself. So a 0 result proves equality, and a nonzero result is a real difference. A satisfying point of a cut miter that still has cut variables may assign a cut variable a value that its definition cannot take at the same inputs, which is the false negative. Moving the cut back to the primary inputs gives the exact miter of the two nodes. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM with hashing in expected constant time. Let $N$ count the gates and gate inputs of both circuits, $C$ the cut variables and $P$ the node pairs that reach line L7 or L11. Every BDD in the run is over at most $n + C$ variables, so it has at most $2^{n + C} + 1$ nodes: at most $2^i$ nodes test the variable at depth $i$, plus the two sinks.

- Simulation at line L2 costs $O(N)$ word operations for $W$ up to the word size.
- Line L4 makes one apply per gate input. An apply of BDDs with $s$ and $t$ nodes costs $O(st)$ with the operation cache, so each costs $O(4^{n + C})$.
- RESOLVE makes at most $C$ compositions (Lemma 2 of the proof), each two restrictions and an if-then-else, that is, a constant number of applies of $O(4^{n + C})$ each, plus a support scan of linear cost.

The total is $O((N + PC)\, 4^{n + C})$ time, and the unique table and cache hold at most one entry per step, which gives the same space bound. This bound is far from what happens on circuits that share structure: there each cut miter has a few nodes, $C$ is close to the number of merged pairs, and the run time is close to linear in $N$. No bound that is polynomial on every input is expected, since the problem is coNP-complete.

## Properties

- Exact and complete: it always ends with "equivalent" or a real counterexample. The random simulation affects only the speed.
- Deterministic for a fixed seed.
- When RESOLVE must go all the way back to the primary inputs, it builds the full BDDs of the two nodes, so a hard pair costs what a monolithic BDD check of that pair costs.
- The result does not depend on the variable order, but the cost does.

## Variants and improvements

- **SAT in place of BDDs.** The check at line L7 can be a SAT call on the cut miter. A satisfying point then has to be checked against the real inputs, or the cut is moved back as here. [SAT sweeping](/sat-sweeping/) is this idea on one [and-inverter graph](/and-inverter-graph/) for synthesis, with no cut variables; its counterexamples refine the simulation classes.
- **Many cut frontiers.** Kuehlmann and Krohm keep several cut frontiers and control how far a false negative moves the cut back. Line L15, one variable at a time from the newest, is the simplest such rule.
- **Structural hashing.** Merging gates with the same operator and the same fanins before line L3 finds many equal pairs for free, see [hash-consing](/hash-consing/).
- **Complemented pairs.** A node can be equal to the complement of another node. Signatures that are equal up to complement find such pairs; the code here uses plain equality.
- **Sequential circuits.** With the latches matched by [latch mapping](/latch-mapping/), each pair of next-state functions is a combinational check. Without a match, [signal correspondence](/signal-correspondence/) proves equalities across time by induction.

## When to use it

Use it when the two circuits are related by synthesis steps that keep many internal signals: technology mapping, buffering, local rewrites. Then most internal nodes have a partner, and the BDDs between cuts stay small. When the circuits share little inside, as for a multiplier against a different multiplier architecture, few pairs merge, the cuts help little, and a monolithic BDD or a plain SAT check of the miter costs the same or less. Arithmetic with no common structure needs other methods altogether.

## Pitfalls

- **Returning the cut miter's point as a counterexample.** A version that returns "different" as soon as $R(u) \oplus R(r)$ or $F(o) \oplus F(o')$ is nonzero reports false negatives as bugs. In the example it would report $v = 1, a = 0$, which is not an input vector. Lines L7 and L11 must call RESOLVE first, and line L12 must return only a point of a BDD over primary inputs.
- **Merging on simulation alone.** Equal signatures at line L6 do not prove anything. Merging there without line L7 makes the method unsound: two different nodes that the $W$ vectors did not separate become one variable.
- **Losing the definition order.** RESOLVE ends because each definition uses only older variables (line L15 takes the newest). If a cut variable were defined from a newer one, composition could loop.
- **Cutting at a primary input twice.** A node equal to a primary input must reuse the input's own variable, as line L8 does. A second variable for the same input loses the link between them and makes more false negatives.

## Implementations

## History

Berman and Trevillyan (ICCAD 1989) compared two designs by finding internal points that are equivalent and treating them as new inputs of the parts beyond them. Brand (ICCAD 1993) found internal equivalences with test generation on a miter and replaced proved points. Kuehlmann and Krohm (DAC 1997) built BDDs over cut variables with structural hashing, kept many cut frontiers, and removed false negatives by composing back. Kuehlmann, Paruthi, Krohm and Ganai (2002) folded these steps, with SAT, into one engine on an and-inverter graph.

## References
