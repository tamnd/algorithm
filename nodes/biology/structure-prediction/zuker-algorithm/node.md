---
tag: V18HE3
kind: algorithm
slug: zuker-algorithm
name: Zuker algorithm
aliases:
- Zuker-Stiegler algorithm
- mfold
- Minimum free energy folding
area: biology/structure-prediction
level: core
summary: Dynamic program that finds a minimum free energy RNA secondary structure under a loop energy model in O(n^3) time with a bound on internal loop size.
solves: [rna-secondary-structure-prediction]
model: word-ram
complexity:
  vars: {n: the length of the RNA sequence, L: the largest allowed size of a bulge or interior loop}
  time: {worst: Θ(n^3 + n^2 L^2), average: Θ(n^3 + n^2 L^2), best: Θ(n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1981
  people: [Michael Zuker, Patrick Stiegler]
  note: Zuker and Stiegler gave the loop based dynamic program for the minimum free energy structure in 1981. It became the mfold program and is the core of RNAfold and RNAstructure.
prereqs: [nussinov-algorithm, nearest-neighbor-model]
see_also: [mccaskill-algorithm, rna-secondary-structure-prediction, interval-dp, traceback, rna-pseudoknot-prediction, sankoff-rna-algorithm, rna-inverse-folding, rna-folding-kinetics]
sources:
  - paper: doi:10.1093/nar/9.1.133
    title: Michael Zuker and Patrick Stiegler, Optimal computer folding of large RNA sequences using thermodynamics and auxiliary information, Nucleic Acids Research 9(1), 1981, pages 133 to 148
    locator: the recursions for the minimum free energy with loop energies
  - paper: doi:10.1007/BF02459506
    title: Michael Zuker and David Sankoff, RNA secondary structures and their prediction, Bulletin of Mathematical Biology 46(4), 1984, pages 591 to 621
    locator: the loop decomposition of the energy and the recursions
  - paper: doi:10.1093/bioinformatics/15.6.440
    title: Rune B. Lyngsø, Michael Zuker and Christian N. S. Pedersen, Fast evaluation of internal loops in RNA secondary structure prediction, Bioinformatics 15(6), 1999, pages 440 to 445
    locator: O(n^3) evaluation of interior loops with no bound on the loop size
  - paper: doi:10.1126/science.2468181
    title: Michael Zuker, On finding all suboptimal foldings of an RNA molecule, Science 244(4900), 1989, pages 48 to 52
    locator: suboptimal structures from the inside and outside tables
  - paper: "Stefan Wuchty, Walter Fontana, Ivo L. Hofacker and Peter Schuster, Complete suboptimal folding of RNA and the stability of secondary structures, Biopolymers 49(2), 1999, pages 145 to 165"
    title: Complete suboptimal folding of RNA and the stability of secondary structures
    locator: the enumeration of all structures within an energy range of the minimum
  - paper: doi:10.1186/1748-7188-6-26
    title: Ronny Lorenz, Stephan H. Bernhart, Christian Höner zu Siederdissen, Hakim Tafer, Christoph Flamm, Peter F. Stadler and Ivo L. Hofacker, ViennaRNA Package 2.0, Algorithms for Molecular Biology 6, 2011, article 26
    locator: the RNAfold program and the Turner 2004 parameters
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 10, Section 10.2, RNA secondary structure prediction (energy minimisation and the Zuker algorithm), pages 267 to 276
---

The Zuker algorithm finds an [RNA secondary structure](/rna-secondary-structure/) of minimum free energy. The energy is a sum over the loops of the structure, as in the [nearest-neighbor model](/nearest-neighbor-model/): stacked pairs lower the energy, and hairpins, bulges, interior loops and multiloops raise it. The algorithm is an [interval dynamic program](/interval-dp/) like the [Nussinov algorithm](/nussinov-algorithm/), but it keeps a table $V(i, j)$ for intervals whose ends pair, and two tables for the parts of multiloops. With a bound $L$ on the size of interior loops, it runs in $\Theta(n^3 + n^2 L^2)$ time and $\Theta(n^2)$ space. It is the core of mfold, RNAfold and RNAstructure.

## In plain words

An RNA string folds into nested pairs of letters. The pairs form loops: a hairpin at the tip, a stack between two neighbor pairs, a bulge or interior loop between two pairs with free letters between them, and a multiloop where three or more helices meet. Each loop has an energy, and the energy of a fold is the sum. The task is to find the fold with the lowest energy.

Keep one table entry for each stretch whose two end letters pair. That pair closes exactly one loop. Try each kind of loop: a hairpin, a smaller pair inside with a short loop between, or a multiloop. A multiloop needs two more tables that hold the best way to fill a stretch with one or more helices. A last pass lists the helices along the outside of the fold.

## The problem

**Input.** A sequence $s = s_1 \cdots s_n$ over $\{A, C, G, U\}$ and an energy model. On this page the allowed pairs are AU, GC and GU (in both orders), the hairpin minimum is $m = 3$, and pseudoknots are not allowed.

**Output.** A secondary structure $P$ of $s$ with the smallest energy $E(P)$. The energy is $E(P) = \sum_{\text{loops } \ell} E(\ell)$, where each pair $(i, j)$ closes one loop and the exterior loop has energy 0. The loop closed by $(i, j)$ is a hairpin if no pair is inside it, an internal loop if one pair $(k, l)$ is directly inside, and a multiloop if two or more pairs are directly inside.

**The energy model of the code.** The real programs use the Turner 2004 parameters of the [nearest-neighbor model](/nearest-neighbor-model/) in kcal/mol. The code on this page uses a small integer model with the same loop types, so that the tests can check it against brute force:

- hairpin with $u \ge 3$ unpaired bases: $H(u) = 3 + u$;
- stack of $(i, j)$ on $(i + 1, j - 1)$: $-(w(s_i s_j) + w(s_{i+1} s_{j-1}))$, with $w = 3$ for GC, $2$ for AU and $1$ for GU;
- bulge with $u$ unpaired bases on one side: $2 + u$;
- interior loop with $u_1, u_2 \ge 1$ unpaired bases: $1 + u_1 + u_2 + |u_1 - u_2|$;
- bulges and interior loops with $u_1 + u_2 > L$ are not allowed (default $L = 30$);
- multiloop with $k$ branches, the closing pair included, and $u$ unpaired bases: $a + b k + c u$ (default $a = 3$, $b = 1$, $c = 0$).

## The algorithm

Let $H(i, j)$ be the energy of the hairpin closed by $(i, j)$, and $\mathrm{IL}(i, j, k, l)$ the energy of the stack, bulge or interior loop closed by $(i, j)$ with the inner pair $(k, l)$. The tables, with $\infty$ for an impossible case, are:

- $V(i, j)$: the smallest energy of the part of a structure inside $[i, j]$, given that $(i, j)$ is a pair;
- $\mathrm{WM1}(i, j)$: one branch that starts with a pair $(i, l)$, then unpaired bases up to $j$, with multiloop costs;
- $\mathrm{WM}(i, j)$: a part of a multiloop with at least one branch;
- $F(j)$: the smallest energy of the prefix $s_1 \cdots s_j$.

The recurrences are

$$V(i, j) = \min\Big(H(i, j),\ \min_{k, l} \big(\mathrm{IL}(i, j, k, l) + V(k, l)\big),\ \min_{u} \big(a + b + \mathrm{WM}(i + 1, u - 1) + \mathrm{WM1}(u, j - 1)\big)\Big),$$

$$\mathrm{WM1}(i, j) = \min\big(V(i, j) + b,\ \mathrm{WM1}(i, j - 1) + c\big), \qquad \mathrm{WM}(i, j) = \min_{i \le u \le j} \Big(\min\big(c (u - i),\ \mathrm{WM}(i, u - 1)\big) + \mathrm{WM1}(u, j)\Big),$$

$$F(j) = \min\Big(F(j - 1),\ \min_{k} \big(F(k - 1) + V(k, j)\big)\Big), \qquad F(0) = 0.$$

In $V$, the multiloop term asks $\mathrm{WM}$ for at least one branch and $\mathrm{WM1}$ for one more, so the loop has at least two inner branches. In $\mathrm{WM}$, the index $u$ is the start of the last branch.

```pseudo id=main
ZUKER(s[1 .. n])                           ▷ all of V, WM1, WM start at ∞
L1  for d ← m + 1 to n − 1 do                   ▷ the span j − i
L2      for i ← 1 to n − d do j ← i + d
L3          if (s_i, s_j) is allowed then
L4              V[i, j] ← H(i, j)                    ▷ hairpin
L5              for each (k, l) with i < k < l < j, l − k > m, (k − i − 1) + (j − l − 1) ≤ L do V[i, j] ← min(V[i, j], IL(i, j, k, l) + V[k, l])
L6              for u ← i + 2 to j − 1 do V[i, j] ← min(V[i, j], a + b + WM[i + 1, u − 1] + WM1[u, j − 1])
L7          WM1[i, j] ← min(V[i, j] + b, WM1[i, j − 1] + c)
L8          WM[i, j] ← min over u in [i, j] of (min(c · (u − i), WM[i, u − 1]) + WM1[u, j])
L9  F[0] ← 0; for j ← 1 to n do F[j] ← min(F[j − 1], min over k ≤ j − m − 1 of F[k − 1] + V[k, j])
L10 trace back from F[n] with a stack of cells: for each cell, find a case of its recurrence that gives its value, add the pair of each V cell to P, and push the cells of that case
L11 return F[n], P
```

All cells that lines L5 to L8 read have a shorter span, except $V(i, j)$ in line L7 and $\mathrm{WM1}(i, j)$ in line L8 (for $u = i$). Both are computed earlier in the same pass. The [traceback](/traceback/) of line L10 uses an explicit stack, as in the Nussinov algorithm, so it does not recurse.

## Example

Fold $s = $ GGAGGAAAACCCC ($n = 13$) in the model of the code. The four pairs of the result close these loops:

| cell | the best case | value |
|---|---|---|
| $V(5, 10)$, G with C | hairpin with $u = 4$: $3 + 4$ | 7 |
| $V(4, 11)$, G with C | stack on $(5, 10)$: $-(3 + 3) + 7$ | 1 |
| $V(2, 12)$, G with C | bulge with $u_1 = 1$, $u_2 = 0$ on $(4, 11)$: $(2 + 1) + 1$ | 4 |
| $V(1, 13)$, G with C | stack on $(2, 12)$: $-(3 + 3) + 4$ | $-2$ |

The other cases lose. For $V(2, 12)$, the interior loop on $(4, 10)$ costs $1 + 2 + 0 + 8 = 11$ and the bulge on $(5, 11)$ costs $4 + 8 = 12$. For $V(1, 13)$, the bulge on $(4, 12)$ costs $4 + 2 = 6$. Line L9 then gives $F(13) = F(0) + V(1, 13) = -2$, which is less than $F(12) = 0$. The minimum free energy is $-2$, with the structure

```
GGAGGAAAACCCC
((.((....))))
```

The unpaired A at position 3 is a bulge. It cannot pair with the C across from it, and the bulge of energy 3 costs less than the two GC stacks it keeps.

## Correctness

Each pair $(i, j)$ of a structure closes exactly one loop, and the type of that loop is fixed by the number of pairs directly inside it. So the structures inside a pair $(i, j)$ split into three disjoint groups: hairpin, one inner pair $(k, l)$, or a multiloop. In the last group, the last branch starts at a unique position $u$, and the part before $u$ has at least one branch. The energy is a sum over loops, so the best structure in each group is the loop energy plus the best values of the smaller parts. An induction on the span shows that each table holds its optimum, and the traceback rebuilds a structure with energy $F(n)$. The full proof is below.

## Complexity

- **Time.** There are $O(n^2)$ cells. Line L5 tries at most $(L + 1)(L + 2)/2$ inner pairs, lines L6 and L8 try $O(n)$ values of $u$, and line L9 takes $O(n^2)$ time in total. So the worst-case time is $\Theta(n^3 + n^2 L^2)$, which is $\Theta(n^3)$ for a fixed $L$ such as 30. Without a bound ($L = n$), line L5 tries $\Theta(n^2)$ pairs and the time is $\Theta(n^4)$. The cubic term of lines L6 and L8 runs on every input, so the time is also $\Omega(n^3)$ in the best case.
- **Interior loops in $O(n^3)$.** Lyngsø, Zuker and Pedersen (1999) showed that when the interior loop energy is a function of the size, an asymmetry term and terms for the two closing pairs, all interior loops of any size can be done in $O(n^3)$ total time, and in $O(n^2 L)$ time with the bound $L$.
- **Space.** Four tables of $O(n^2)$ cells, so $\Theta(n^2)$ words. The traceback stack holds $O(n)$ cells.

These bounds are in the [word RAM](/word-ram/) model. Real energy tables add a constant factor per loop.

## Properties

- **Exact for the model.** The algorithm finds a structure of smallest energy in its model. It does not say how close that structure is to the true one: that depends on the parameters and on effects the model leaves out, such as pseudoknots and tertiary contacts.
- **Unambiguous decomposition.** Each structure has one derivation in the recurrences. Replace min by sum and energies $E$ by Boltzmann weights $e^{-E/RT}$, and the same recurrences give the partition function of the [McCaskill algorithm](/mccaskill-algorithm/).
- **One optimum.** Many structures can have the minimum energy, or energies close to it. The traceback returns one of them.
- **No pseudoknots.** The split of the multiloop and of the exterior loop is valid only for nested pairs. See [RNA pseudoknot prediction](/rna-pseudoknot-prediction/).

## Variants and improvements

- **Turner energies.** Real programs add dangling ends and terminal mismatches, special hairpins with tabulated energies, and the AU and GU closure penalties. The loop structure of the recurrences does not change.
- **Suboptimal structures.** Zuker (1989) computed, with outside tables, the best structure that contains each pair. Wuchty, Fontana, Hofacker and Schuster (1999) list all structures within a given energy range of the minimum.
- **Partition function.** The [McCaskill algorithm](/mccaskill-algorithm/) uses the same recurrences with sums and products and gives base pair probabilities.
- **Comparative folding.** The [Sankoff algorithm](/sankoff-rna-algorithm/) folds and aligns several sequences at the same time, and [simultaneous alignment and folding](/simultaneous-alignment-and-folding/) gives faster forms of it.
- **Pseudoknots.** Extensions for some classes of crossing pairs cost $O(n^4)$ to $O(n^6)$ time; see [RNA pseudoknot prediction](/rna-pseudoknot-prediction/).
- **Sparse and linear-time heuristics.** Restrict the pairs to those with a chance to form, or use beam search over the sequence from left to right. These methods give up the guarantee of an exact minimum for speed.

## When to use it

Use the Zuker algorithm to predict the secondary structure of one RNA sequence of up to a few thousand bases from its sequence alone. Use it with the Turner 2004 parameters from a tested package, not with your own tables. If the energy landscape has several low structures, the single minimum can mislead; then use base pair probabilities from the [McCaskill algorithm](/mccaskill-algorithm/) or a set of suboptimal structures. If you have several related sequences, comparative methods are more accurate.

## Pitfalls

- **Double counting in the multiloop.** Ambiguous forms of WM (for example, "add an unpaired base on the left or on the right") are fine for the minimum but count structures many times in a partition function. Use one form, as in line L8, if you reuse the code for sums.
- **A multiloop with one branch.** The multiloop term must require at least two inner branches. Otherwise a pair with one inner pair can be scored as a multiloop and as an interior loop.
- **The loop bound in the traceback.** The traceback must use the same bound $L$ and the same loop energies as the fill. If not, it can fail to find a case that gives the value of a cell.
- **Infinite values.** Many cells are $\infty$. Test them before you add, or use a large finite value that cannot overflow.
- **Units and temperature.** Turner energies are in kcal/mol at 37 °C. Values at other temperatures need the enthalpy tables too.

## Implementations

## History

Michael Zuker and Patrick Stiegler published the algorithm in 1981. Before, Nussinov and Jacobson (1980) had scored each base pair, while Zuker and Stiegler scored loops, with stacking and loop energies from melting experiments. Zuker and Sankoff (1984) gave a general account of the loop decomposition. The program became mfold, and Zuker (1989) added suboptimal structures. The Vienna RNA package of Hofacker and others (1994) gave RNAfold, and Mathews, Turner and others measured the parameters of 1999 and 2004. Lyngsø, Zuker and Pedersen (1999) removed the need for a bound on interior loops.

## References
