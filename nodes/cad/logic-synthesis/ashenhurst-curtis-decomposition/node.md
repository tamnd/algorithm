---
tag: WX0DTG
kind: technique
slug: ashenhurst-curtis-decomposition
name: Ashenhurst-Curtis decomposition
aliases:
- functional decomposition
- Ashenhurst decomposition
area: cad/logic-synthesis
level: advanced
summary: Writes f(X, Y) as g(h(X), Y) by counting the distinct columns of a decomposition chart, a method used in synthesis for lookup table FPGAs.
prereqs: [boolean-function, boolean-network, shannon-expansion]
see_also: [multi-level-logic-synthesis, lut-mapping, reduced-ordered-bdd, myhill-nerode-theorem, incompletely-specified-fsm-minimization, state-assignment, k-coloring, algebraic-division]
sources:
  - paper: "Robert L. Ashenhurst, The decomposition of switching functions, Proceedings of an International Symposium on the Theory of Switching, April 1957, Annals of the Computation Laboratory of Harvard University 29, Harvard University Press, 1959, pages 74 to 116"
    title: The decomposition of switching functions
    locator: decomposition charts and the test for a simple disjoint decomposition by the number of distinct columns
  - book: "H. Allen Curtis, A New Approach to the Design of Switching Circuits, Van Nostrand, 1962"
    title: A New Approach to the Design of Switching Circuits
    locator: the extension of decomposition charts to decompositions with several functions of the bound set
  - paper: doi:10.1147/rd.62.0227
    title: J. Paul Roth and Richard M. Karp, Minimization over Boolean graphs, IBM Journal of Research and Development 6(2), 1962, pages 227 to 238
    locator: the tests for decompositions of incompletely specified functions and the search for a minimum cost circuit
  - paper: "Yung-Te Lai, Massoud Pedram and Sarma B. K. Vrudhula, BDD based decomposition of logic functions with application to FPGA synthesis, Proceedings of the 30th Design Automation Conference (DAC), 1993, pages 642 to 647"
    title: BDD based decomposition of logic functions with application to FPGA synthesis
    locator: disjunctive and nondisjunctive decomposition on a BDD, with the bound variables above a cut
---

Ashenhurst-Curtis decomposition splits a [Boolean function](/boolean-function/) $f(X, Y)$ of two disjoint sets of variables into $g(h_1(X), \ldots, h_t(X), Y)$, where the new functions $h_i$ see only the bound set $X$. It works on a decomposition chart: a table of $f$ with one column for each assignment of $X$ and one row for each assignment of $Y$. If the chart has $\mu$ distinct columns, the decomposition exists with $t$ functions exactly when $\mu \le 2^t$. Ashenhurst (1957) proved the case $t = 1$, Curtis (1962) gave the general case, and Roth and Karp (1962) extended it to functions with don't-cares. The method fits [lookup tables](/lut-mapping/) of FPGAs well, because each $h_i$ and $g$ have fewer inputs than $f$, and Lai, Pedram and Vrudhula (1993) made it practical by reading the column count off a [BDD](/reduced-ordered-bdd/).

## In plain words

Suppose a function reads six switches, but your parts can read only four. Split the switches into two groups. Ask: for each setting of the first group, what does the function do as the second group changes? Write each answer as a column of a table. Often, many settings of the first group give the same column. If there are only two different columns, a small part can read the first group and say which column it is with one wire. A second part reads that wire and the second group and gives the answer. With four different columns you need two wires, and so on. The trick is to count the different columns, and to find a split of the switches with few of them.

## When it applies

- A function has more inputs than one cell can take, as in an FPGA with $K$-input lookup tables, and you want to split it into cells with fewer inputs.
- The function is given or can be built as a truth table or a BDD, so that its columns can be compared. A function of 20 inputs has a truth table of about $10^6$ bits, so the method works on single nodes or small groups of nodes of a [Boolean network](/boolean-network/), not on a whole chip.
- Some set of inputs affects the output only through a few patterns. A symmetric function is an example: it depends on a bound set of $s$ variables only through the number of ones in it, so the columns of two assignments with the same count are equal and $\mu \le s + 1$.
- The function has don't-cares that can merge columns, which can make $\mu$ smaller.

## The template

Write $X$ for the bound set with $s$ variables and $Y$ for the free set with the other $n - s$ variables. The column of an assignment $x$ of $X$ is the vector $\mathrm{col}[x] = (f(x, y))_y$ over all assignments $y$ of $Y$, in a fixed order. The column multiplicity $\mu$ is the number of distinct columns.

```pseudo id=main
DECOMPOSE(f, n, s)                          ▷ f: a truth table on n variables; s: the size of the bound set
L1  for each bound set X of s variables, in the order of CHOOSE-BOUND-SETS do
L2      Y ← the other n - s variables
L3      for each assignment x of X do
L4          col[x] ← (f(x, y) for each assignment y of Y)
L5      P ← GROUP(col)                      ▷ a partition of the assignments of X into classes
L6      t ← ⌈lg |P|⌉
L7      if t < s then
L8          e ← ENCODE(P, t)                ▷ a distinct code of t bits for each class
L9          h(x) ← e(the class of x) for each assignment x of X
L10         g(c, y) ← col[x][y] for any x with h(x) = c; a don't-care if no x has the code c
L11         return (X, h, g)
L12 return fail
```

The template has three holes.

- **CHOOSE-BOUND-SETS.** All $\binom{n}{s}$ subsets, or a heuristic order that tries first the variables that appear together.
- **GROUP.** For a completely specified $f$, the classes of equal columns, so $|P| = \mu$. With don't-cares, a partition into classes of pairwise compatible columns, where two columns are compatible if they agree wherever both are specified.
- **ENCODE.** Any injective map from the classes to $\{0,1\}^t$ is correct. The choice changes the size of $h$ and $g$.

Lines L3 and L4 build the decomposition chart one column at a time. Line L7 keeps only splits that save inputs: $h$ replaces $s$ variables by $t$ wires. Line L10 reads $g$ off the chart, and the codes of no class are don't-cares of $g$.

**Why it works (Curtis).** For a completely specified $f$, functions $h_1, \ldots, h_t$ of $X$ and $g$ with $f(x, y) = g(h(x), y)$ exist if and only if $\mu \le 2^t$. *Proof.* If $f = g(h(X), Y)$, two assignments $x, x'$ with $h(x) = h(x')$ have equal columns, since $f(x, y) = g(h(x), y) = f(x', y)$ for all $y$. So there are at most as many distinct columns as values of $h$, which is $2^t$. Conversely, if $\mu \le 2^t$, give each distinct column its own code of $t$ bits, let $h(x)$ be the code of $\mathrm{col}[x]$, and let $g(c, y) = \mathrm{col}[x][y]$ for any $x$ with $h(x) = c$. All such $x$ have the same column, because the code is injective, so $g$ is well defined and $g(h(x), y) = f(x, y)$. $\square$ The case $t = 1$, $\mu \le 2$, is Ashenhurst's simple disjoint decomposition. With don't-cares, the same proof works for any partition into classes of pairwise compatible columns: each class has a common column that agrees with all of its members where they are specified.

**Cost.** For one bound set, the chart has $2^n$ entries. Hashing the columns finds the classes in $O(2^n)$ expected word operations on a [word RAM](/word-ram/), when a column fits in a constant number of words. Trying all bound sets of size $s$ costs $\binom{n}{s}$ times this. Grouping with don't-cares is a coloring problem, below.

**Worked example.** Let $f(a, b, c, d) = (a \oplus b) c + \bar{d}$, with the bound set $X = \{a, b\}$ and the free set $Y = \{c, d\}$.

| $c d$ \ $a b$ | 00 | 01 | 10 | 11 |
|---|---|---|---|---|
| 00 | 1 | 1 | 1 | 1 |
| 01 | 0 | 0 | 0 | 0 |
| 10 | 1 | 1 | 1 | 1 |
| 11 | 0 | 1 | 1 | 0 |

The columns of $ab = 00$ and $11$ are equal, and so are those of $01$ and $10$, so $\mu = 2$ and $t = 1 < 2$. With the code 0 for the first class and 1 for the second, $h = a \oplus b$. The column of class 0 is $\bar{d}$ and the column of class 1 is $c + \bar{d}$, so $g(h, c, d) = h c + \bar{d}$. A script computed $\mu$ for every bound set. The other five bound sets of two variables have $\mu = 3$, so they need $t = 2$ and give no saving. Of the bound sets of three variables, $\{a, b, c\}$ has $\mu = 2$, with $h = (a \oplus b) c$ and $g = h + \bar{d}$, $\{a, b, d\}$ has $\mu = 3$, and the other two have $\mu = 4$.

**How often it works.** A bound set of three variables of a 4-variable function leaves columns of 2 entries, so $\mu \le 4$ and $t = 2 < 3$ always. So every function of 4 variables is $g(h_1(X), h_2(X), y)$ for any bound set $X$ of 3 variables, with three functions of 3 inputs. Simple decompositions are rarer. An exhaustive count found that of the 64594 functions of 4 variables that depend on all 4, exactly 7354 have a bound set of 2 or 3 variables with $\mu \le 2$.

## Classic examples

- **[LUT mapping](/lut-mapping/).** A node with more than $K$ inputs is split with a bound set of at most $K$ variables, so that each $h_i$ fits in one lookup table, and $g$ is split again if it is still too large.
- **[Reduced ordered BDD](/reduced-ordered-bdd/).** Put the bound variables first in the order. Each node of a reduced ordered BDD stands for one distinct subfunction, so $\mu$ is the number of distinct nodes reached from the root by the assignments of $X$. Lai, Pedram and Vrudhula use this cut to find decompositions without a truth table.
- **[Myhill-Nerode theorem](/myhill-nerode-theorem/).** The distinct columns are the distinct residual functions $f(x, \cdot)$, in the same way that the states of a minimum DFA are the distinct residual languages of prefixes. Counting columns is counting these classes.
- **[Incompletely specified FSM minimization](/incompletely-specified-fsm-minimization/).** Merging columns with don't-cares into compatible classes is the same problem as merging compatible states, and in both cases compatibility is not transitive.
- **[k-coloring](/k-coloring/).** With don't-cares, build the graph with a vertex per column and an edge between incompatible columns. A partition of compatible classes is a proper coloring, and $t$ wires suffice if the graph is $2^t$-colorable.
- **[State assignment](/state-assignment/).** The choice of the codes in ENCODE is an encoding problem like the choice of state codes, with the same goal of simple logic after encoding.

## Variations

- **Simple disjoint decomposition.** The case $t = 1$ of Ashenhurst, where $h$ is a single function and $g$ has $n - s + 1$ inputs.
- **Several functions of the bound set.** The general case $t \ge 1$ of Curtis, with the test $\mu \le 2^t$.
- **Non-disjoint decomposition.** Some variables $Z$ go to both $h$ and $g$: $f = g(h(X, Z), Y, Z)$. For each assignment of $Z$ the chart is split into its own part, and the classes are counted in each part, so the codes may differ between the parts.
- **Don't-cares.** Roth and Karp (1962) gave the tests for functions with don't-cares, where GROUP is a coloring of the incompatibility graph. The don't-cares of $g$ at unused codes, from line L10, can also make $g$ smaller.
- **Multiple outputs.** For several functions with the same bound set, the column is the tuple of their columns, and the functions $h_i$ are shared.
- **BDD-based.** The method of Lai, Pedram and Vrudhula (1993) reads $\mu$ off a BDD cut and builds $h$ and $g$ as BDDs, for both disjoint and non-disjoint bound sets.

## Pitfalls

- **Accepting a split that saves nothing.** With $\mu = 3$ and $s = 2$, $t = 2$ and the split replaces two inputs by two wires. Line L7 must test $t < s$, not $\mu \le 2^s$, which always holds.
- **Treating compatibility as an equivalence.** The columns $(1, *)$, $(*, 0)$ and $(0, *)$ show the problem: the middle one is compatible with each of the others, but the first and the last conflict in their first entry. Putting all three in one class gives a wrong $g$. GROUP must check every pair in a class. Finding the fewest classes is NP-hard in general, because every graph is the incompatibility graph of some chart: give each edge its own row, with 0 and 1 in the columns of its two ends and $*$ in the others, and then the fewest classes is the chromatic number.
- **Treating $*$ as a third value.** Comparing columns with $*$ as a symbol gives a correct result but throws away the freedom, so $\mu$ can be larger than needed.
- **Forgetting the unused codes.** When $\mu < 2^t$, some codes of $h$ never occur, and $g$ may take any value there. Fixing them to 0 can make $g$ larger.
- **Truth tables of large functions.** The chart has $2^n$ entries for each bound set, and there are $\binom{n}{s}$ bound sets. Use a BDD or a small window of the network for more than about 20 inputs.

## References
