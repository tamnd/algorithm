---
tag: 70F55E
kind: algorithm
slug: espresso
name: Espresso
aliases:
- Espresso heuristic logic minimizer
- Espresso-II
area: cad/logic-synthesis
level: core
summary: Brayton and coauthors' heuristic two-level minimizer that loops expand, irredundant cover and reduce on a cover of cubes until the cost stops falling.
solves: [two-level-logic-minimization]
model: word-ram
complexity:
  vars: {n: the number of variables, c: the number of cubes of F and D, r: "the largest number of cubes in a complement that the program builds, at most 3^n"}
  time: {worst: "O(n^2 c^3 (n^2 (r + c) + 2^n (c + r^2)))"}
  space: {extra: O(n^2 (c + r))}
properties: {deterministic: true, exact: false, online: false, recursive: true}
history:
  year: 1984
  people: [Robert K. Brayton, Gary D. Hachtel, Curtis T. McMullen, Alberto L. Sangiovanni-Vincentelli]
  note: The 1984 book of Brayton, Hachtel, McMullen and Sangiovanni-Vincentelli described Espresso-II and its operators. Rudell and Sangiovanni-Vincentelli extended it to multiple-valued variables as Espresso-MV in 1987.
prereqs: [two-level-logic-minimization, prime-implicant, unate-recursive-paradigm, dont-care-condition]
see_also: [quine-mccluskey, petricks-method, unate-function, local-search, local-optimum, karnaugh-map, sum-of-products, multi-level-logic-synthesis]
sources:
  - book: isbn:9780898381641
    title: Robert K. Brayton, Gary D. Hachtel, Curtis T. McMullen and Alberto L. Sangiovanni-Vincentelli, Logic Minimization Algorithms for VLSI Synthesis, Kluwer, 1984
    locator: Chapter 4 (Sections 4.1 Complementation, 4.2 Tautology and 4.3 Expand, and the later sections on the other steps of the loop), Chapter 6 (experimental results on a set of test PLAs) and Chapter 7 (comparisons with MINI, POP and PRESTO)
  - paper: doi:10.1109/TCAD.1987.1270318
    title: Richard L. Rudell and Alberto L. Sangiovanni-Vincentelli, Multiple-valued minimization for PLA optimization, IEEE Transactions on Computer-Aided Design 6(5), 1987
    locator: Espresso-MV, the loop for multiple-valued variables
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 7, Two-Level Combinational Logic Optimization (heuristic minimization, the expand, reduce and irredundant operators)
  - book: isbn:9780792397465
    title: Gary D. Hachtel and Fabio Somenzi, Logic Synthesis and Verification Algorithms, Kluwer, 1996
    locator: Chapter 5, Heuristic Minimization of Two-Level Circuits
  - paper: doi:10.1016/0167-9260(94)00007-7
    title: Olivier Coudert, Two-level logic minimization, an overview, Integration, the VLSI Journal 17(2), 97 to 140, 1994
    locator: heuristic minimization and the place of Espresso among the exact and heuristic methods
---

Espresso is a heuristic for [two-level logic minimization](/two-level-logic-minimization/). It works on a cover of cubes, a [sum of products](/sum-of-products/), and never lists all the [prime implicants](/prime-implicant/) or minterms. It first computes the off-set $R$ as the complement of the on-set plus the [don't-care](/dont-care-condition/) set. Then it repeats three steps. EXPAND grows each cube into a prime, as long as it stays away from $R$, and lets the grown cubes swallow other cubes. IRREDUNDANT removes cubes that the other cubes and the don't-cares already cover. REDUCE shrinks each cube to the smallest cube that still holds the points only it covers, which gives EXPAND room to grow it in another direction. The loop stops when the cost stops falling. The result is a prime and irredundant cover, a local optimum. It is not always a minimum cover. Brayton, Hachtel, McMullen and Sangiovanni-Vincentelli (1984) built it on the [unate recursive paradigm](/unate-recursive-paradigm/), and it became the standard minimizer for programmable logic arrays.

## In plain words

You start with any list of AND terms that gives the right outputs. Make each term as large as it can be without turning on an input that must be 0. Large terms swallow small ones, so throw out the swallowed ones. Then throw out any term whose 1s other terms already give.

Now the list may be stuck. So shrink each term back, as far as it can go without losing a 1 that only it gives. Then grow the terms again. They may grow in new directions and swallow more terms. Repeat while the list gets shorter or cheaper, and stop when a round brings no gain.

## The problem

The input is the number of variables $n$, a cover $F$ of the on-set and a cover $D$ of the don't-care set, both lists of cubes. The output is a cover $G$ with $F \subseteq G \subseteq F \cup D$ as sets of points, where each cube of $G$ is a prime implicant of $F \cup D$ and no cube of $G$ can be removed. The cost is the number of cubes, then the number of literals. A cube is a string over $\{0, 1, -\}$.

## The algorithm

```pseudo id=main
ESPRESSO(F, D)
L1  R ← COMPLEMENT(F ∪ D)                            ▷ the off-set
L2  F ← EXPAND(F, R)
L3  F ← IRREDUNDANT(F, D)
    loop
L4      before ← cost(F)
L5      G ← REDUCE(F, D)
L6      G ← IRREDUNDANT(EXPAND(G, R), D)
L7      if cost(G) ≥ before then return F
        F ← G

EXPAND(F, R)
    for each cube c of F, fewest literals first do
L8      if c lies in a cube expanded before then skip c
        repeat
L9          raises ← the cubes made from c by removing one literal that meet no cube of R
L10         if raises = ∅ then stop: c is prime
L11         c ← the raise that contains the most other cubes of F, ties by the first position
        add c to the result
    return the result without the cubes that lie in another of its cubes

IRREDUNDANT(F, D)
L12 E ← the cubes c of F that do not lie in (F - c) ∪ D          ▷ relatively essential
L13 P ← the other cubes of F that do not lie in E ∪ D             ▷ drop the totally redundant
L14 for each c of P, most literals first: if c lies in E ∪ (P - c) ∪ D then remove c from P
    return E ∪ P

REDUCE(F, D)
    for each cube c of F, fewest literals first do
L15     free ← the points of c in no other cube of F and not in D
L16     if free = ∅ then remove c
L17     else c ← the smallest cube that contains free
    return F
```

COMPLEMENT and the containment tests "lies in" of lines L12 to L14 are the operators of the [unate recursive paradigm](/unate-recursive-paradigm/): a cube $c$ lies in a cover $H$ exactly when the cofactor $H_c$ is a tautology. Line L15 computes free as the complement of the cofactor of the other cubes and $D$ by $c$.

EXPAND treats the large cubes first, because they are the most likely to swallow others. Line L9 keeps a raise only when it meets no point of $R$, so every cube stays inside $F \cup D$. Line L11 is a greedy choice of the direction to grow. IRREDUNDANT keeps every cube that alone covers some point, removes the cubes that those cubes and $D$ cover, and then removes the remaining redundant cubes one at a time, each time testing against what is left. REDUCE works in turn, so a cube that shrinks first leaves more points to the cubes after it. The cube of line L17 is the supercube of free. It can be smaller than $c$ in many variables at once.

## Example

Take the cyclic function $f = \sum m(1, 2, 3, 4, 5, 6)$ over $x_1 x_2 x_3$ with no don't-cares, given by its six minterms.

| step | line | cover | cost |
|---|---|---|---|
| off-set | L1 | R = 000, 111 | |
| expand | L2 | -01, -10, 0-1, 1-0 | (4, 8) |
| irredundant | L3 | -01, -10, 0-1, 1-0 | (4, 8) |
| reduce | L5 | 101, 010, 0-1, 1-0 | |
| expand and irredundant | L6 | 0-1, 1-0, -01, -10 | (4, 8) |
| stop | L7 | -01, -10, 0-1, 1-0 | (4, 8) |

At line L2, the cube 001 can grow to -01 or to 0-1, each of which swallows one more minterm, and the tie goes to the first position. Then 010 grows to -10, 011 to 0-1, and 100 to 1-0, and 101 and 110 lie in cubes grown before. Every cube of the result is needed, so line L3 removes nothing. REDUCE shrinks -01 to 101, since 001 is also in 0-1, and -10 to 010. EXPAND grows them back the same way, and the cost does not fall. The result has 4 cubes, but the minimum, for example $\bar{x}_2 x_3 + \bar{x}_1 x_2 + x_1 \bar{x}_3$, has 3. The cover is prime and irredundant, and still not minimum.

On the BCD function $\sum m(5, 6, 7, 8, 9) + d(10, \ldots, 15)$ over four variables, the off-set is R = 00--, 0100. Line L2 grows the five minterms to -1-1, -11- and 1---, at cost (3, 5). REDUCE shrinks them to 0101, 011- and 100-, line L6 grows them back, and the loop stops with $x_2 x_4 + x_2 x_3 + x_1$, which is a minimum cover.

## Correctness

Three facts hold after each step, and the [full proof](proofs/correctness.md) gives the details. First, the cover $G$ stays between $F$ and $F \cup D$ on the care points: line L9 never lets a cube meet $R$, line L8 and the final filter of EXPAND only drop cubes that lie in another cube, lines L12 to L14 only drop a cube that the rest and $D$ cover, and line L17 keeps every point that only $c$ covers. Second, the output of EXPAND is prime, because line L10 stops only when no literal can be removed without meeting $R$, and the output of IRREDUNDANT is irredundant, because a cube that line L14 keeps was not covered by a larger set of cubes, and removals only make that set smaller. The loop returns the output of an IRREDUNDANT step on the output of an EXPAND step, so the result is prime and irredundant. Third, the loop stops, because the cost is a pair of nonnegative integers that falls strictly at each pass that goes on.

Espresso is not exact. The cyclic example above ends in a cover of 4 cubes when 3 are enough. Prime and irredundant covers can differ in cost, and the loop only moves between them by local steps, so it can stop at a [local optimum](/local-optimum/).

## Complexity

The bounds below are for the code of this page and use plain lists of cubes. The cost pair falls at each pass, and it is at most $(c, nc)$, so the loop runs $O(n c^2)$ times. One EXPAND tries at most $n$ raises at each of at most $n$ rounds per cube, and checks each raise against $R$ and $F$ in $O(n(r + c))$ time, which gives $O(n^3 c (r + c))$. IRREDUNDANT and REDUCE make $O(c)$ calls to tautology and complement. Each such call is a recursion of depth at most $n$ with at most $2^n$ leaves, at $O(n(c + r^2))$ per node for the cofactors and the containment filter of the merge, so $O(2^n n (c + r^2))$ per call. Together this gives the bound of the front matter. The space is $O(n(c + r))$ per level of the recursion, $O(n^2 (c + r))$ in all.

These worst cases are far from typical. The off-set alone can have exponentially many cubes, as the complement of $x_1 x_2 + x_3 x_4 + \cdots + x_{2k-1} x_{2k}$ needs $2^k$ cubes, and tautology is [co-NP-complete](/co-np-complete/). On the PLAs of the 1984 book, the recursions stop early, and the book reports run times and results on a set of test PLAs in its Chapter 6 and compares them with other minimizers in Chapter 7.

## Properties

- **Heuristic.** The result is prime and irredundant, not always minimum.
- **Deterministic.** The orders of lines L8, L11, L14 and L15 and their tie rules fix the output.
- **Works on covers.** The input and every middle result are lists of cubes, so the time depends on the sizes of $F$, $D$ and $R$, not on $2^n$, except inside the recursions.
- **Uses don't-cares.** Cubes grow into $D$ freely, since only $R$ limits EXPAND.
- **Measured.** In our own tests of the code of this page, which leaves out the ESSENTIAL, LAST_GASP and MAKE_SPARSE steps of the full program, the result was above the minimum for 2 of the 256 functions of three variables and for 3055 of the 65536 functions of four variables (about 4.7 percent), with no don't-cares, compared against Quine-McCluskey on every function. These counts describe this small version only.

## Variants and improvements

- **ESSENTIAL.** The full program finds the essential primes early, moves them to the don't-care set while the loop runs, and adds them back at the end. This makes the covers in the loop smaller.
- **LAST_GASP.** When the loop stops, reduce every cube against the original cover at once, expand the small cubes, and try to replace two or more cubes by one. Its aim is to get out of local optima like the one in the cyclic example.
- **MAKE_SPARSE.** After the loop, a last pass lowers the number of connections in the output part of the PLA, with no increase in the number of cubes.
- **Multiple outputs and multiple values.** Espresso-MV of Rudell and Sangiovanni-Vincentelli (1987) treats the outputs as one more variable with many values, and so minimizes all outputs of a PLA together.
- **Exact modes.** The program also has an exact mode that lists the primes and solves the covering problem, which plays the role of [Quine-McCluskey](/quine-mccluskey/) with [Petrick's method](/petricks-method/) or a branch and bound.
- **In multi-level synthesis.** [Multi-level logic synthesis](/multi-level-logic-synthesis/) calls Espresso on the function of each node of a network, with don't-cares from the rest of the network.

## When to use it

Use Espresso for functions with many inputs and outputs, where listing all minterms or all primes is too expensive, and a cover close to the minimum is enough. For small functions where a proved minimum is needed, use [Quine-McCluskey](/quine-mccluskey/). For hand work on up to four variables, a [Karnaugh map](/karnaugh-map/) is simpler.

## Pitfalls

- **The wrong off-set.** Line L1 must complement $F \cup D$, not $F$. With the complement of $F$ alone, line L9 never lets a cube grow into $D$, and the don't-cares are lost.
- **Stopping on strict increase only.** Line L7 must stop when the cost is equal too. In the cyclic example the loop returns the same cover at the same cost, and a test of $>$ in place of $\ge$ loops forever.
- **Reducing all cubes at once.** Line L15 must use the cubes as they are after the earlier reductions. If every cube is reduced against the original cover, two equal cubes each find the other, both become empty at line L16, and their points are lost.
- **Removing redundant cubes in one batch.** Line L14 must test each cube against the cubes that are still in $P$. Two cubes can each be covered by the rest while the rest without both of them is not a cover.
- **Equal cubes in EXPAND.** The final filter of EXPAND must keep one of two equal cubes. A test that drops each cube lying in another drops both.
- **Calling the result optimal.** The cover is prime and irredundant, and the cyclic example shows that it can have more cubes than the minimum.

## Implementations

## History

Brayton, Hachtel, McMullen and Sangiovanni-Vincentelli described Espresso-II in their 1984 book, from work at IBM and at the University of California, Berkeley. The book takes ideas from earlier heuristic minimizers, compares Espresso with MINI, POP and PRESTO, and builds all its operators on the unate recursive paradigm. Rudell and Sangiovanni-Vincentelli (1987) gave Espresso-MV for multiple-valued variables. The Berkeley program espresso became the standard two-level minimizer and is still used as a step of multi-level synthesis.

## References
