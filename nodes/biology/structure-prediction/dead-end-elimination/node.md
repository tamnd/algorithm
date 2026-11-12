---
tag: 161ER1
kind: algorithm
slug: dead-end-elimination
name: Dead-end elimination
aliases:
- DEE
- Dead-end elimination theorem
area: biology/structure-prediction
level: advanced
summary: Removes rotamers that cannot be in any global minimum of a pairwise side-chain energy, by comparing each rotamer with another rotamer of the same residue (Desmet 1992, Goldstein 1994).
solves: [side-chain-packing]
model: real-ram
complexity:
  vars: {n: the number of residues, p: the largest number of rotamers of one residue}
  time: {worst: "O(n^3 p^4)"}
  space: {extra: "O(n p)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1992
  people: [Johan Desmet, Marc De Maeyer, Bart Hazes, Ignace Lasters]
  note: Desmet, De Maeyer, Hazes and Lasters published the dead-end elimination theorem in 1992. Goldstein gave the stronger criterion in 1994.
prereqs: [side-chain-packing, rotamer]
see_also: [protein-design, dominance-pruning, brute-force-search, a-star-search, map-inference, energy-function]
sources:
  - paper: doi:10.1038/356539a0
    title: Johan Desmet, Marc De Maeyer, Bart Hazes and Ignace Lasters, The dead-end elimination theorem and its use in protein side-chain positioning, Nature 356(6369), 1992, 539-542
    locator: the dead-end elimination theorem (the bound with the minimum and maximum pair energies) and its use on side chains
  - paper: doi:10.1016/S0006-3495(94)80923-3
    title: Richard F. Goldstein, Efficient rotamer elimination applied to protein side-chains and related spin glasses, Biophysical Journal 66(5), 1994, 1335-1340
    locator: the criterion with the minimum of the energy differences, and its comparison with the original criterion
  - paper: doi:10.1126/science.278.5335.82
    title: Bassil I. Dahiyat and Stephen L. Mayo, De novo protein design, fully automated sequence selection, Science 278(5335), 1997, 82-87
    locator: the use of dead-end elimination to find the optimal sequence and rotamers for a fixed backbone
  - paper: doi:10.1093/protein/15.10.779
    title: Niles A. Pierce and Erik Winfree, Protein design is NP-hard, Protein Engineering 15(10), 2002, 779-782
    locator: the NP-hardness of the minimization that dead-end elimination prunes
---

Dead-end elimination (DEE) removes [rotamers](/rotamer/) that cannot occur in any global minimum of a [side-chain packing](/side-chain-packing/) energy. It compares two rotamers $r$ and $t$ of the same residue: if $r$ is worse than $t$ against every choice of the other side chains, then $r$ is a dead end and can go. The test is repeated until nothing more goes, and a search over the few rotamers that are left gives the exact optimum. DEE has no polynomial bound on the final search, because the problem is [NP-hard](/np-hard/), but on protein instances it often removes most rotamers before the search starts.

## In plain words

Each side chain of a protein can take a few standard shapes, and we want the combination of shapes with the lowest total energy. Trying all combinations is too slow, because their number grows very fast with the number of side chains.

Dead-end elimination throws away shapes that can never win. Take two shapes of one side chain. Suppose that the first shape is worse than the second one, whatever the neighbours do. Then no best combination can use the first shape: if one did, switching to the second shape would make it better. So the first shape is removed. Each removal makes the neighbours easier to judge, so the test runs again and again until it removes nothing. A small search over the shapes that remain finds the best combination.

## The problem

There are $n$ residues on a fixed backbone. Residue $i$ has a set $R_i$ of rotamers, with $|R_i| \le p$. An assignment $x$ picks one rotamer $x_i \in R_i$ for each residue, and its energy is

$$E(x) = \sum_{i} E_i(x_i) + \sum_{i < j} E_{ij}(x_i, x_j).$$

The self energy $E_i(r)$ holds the interaction of rotamer $r$ with the backbone and often a term from the rotamer library. The pair energy $E_{ij}(r, s)$ holds the interaction of two side chains; we write $E_{ij}(r, s) = E_{ji}(s, r)$, and $E_{ij} = 0$ when the residues are far apart. The goal is an assignment of least energy, the global minimum energy conformation (GMEC). This is the [side-chain packing](/side-chain-packing/) problem. DEE needs only that the energy has this pairwise form. It does not depend on the physics of the terms.

## The algorithm

For live sets $R = (R_1, \ldots, R_n)$ and two rotamers $r \ne t$ of residue $i$, the two classic tests are these.

**Desmet et al. (1992).** Rotamer $r$ is a dead end if

$$E_i(r) + \sum_{j \ne i} \min_{s \in R_j} E_{ij}(r, s) > E_i(t) + \sum_{j \ne i} \max_{s \in R_j} E_{ij}(t, s).$$

The left side is the best that $r$ can do, and the right side is the worst that $t$ can do.

**Goldstein (1994).** Rotamer $r$ is a dead end if

$$G_R(i; r, t) = E_i(r) - E_i(t) + \sum_{j \ne i} \min_{s \in R_j} \big[E_{ij}(r, s) - E_{ij}(t, s)\big] > 0.$$

This test compares $r$ and $t$ against the *same* neighbour rotamer $s$, so it succeeds whenever the Desmet test does, and often when it does not.

```pseudo id=main
DEE(E, R, TEST)                                ▷ TEST is the Desmet or the Goldstein test
L1  repeat
L2      changed ← false
L3      for i ← 1 to n do
L4          for each r in R_i do
L5              for each t in R_i with t ≠ r do
L6                  if TEST(E, R, i, r, t) then
L7                      R_i ← R_i − {r}, changed ← true
L8                      break                  ▷ go to the next r
L9  until not changed
L10 return R

SOLVE(E, R, TEST)
L11 R ← DEE(E, R, TEST)
L12 return an assignment of least energy over R_1 × ... × R_n    ▷ exhaustive search, or A*
```

Line L6 uses the current live sets, so each removal makes later tests easier to pass: a minimum over a smaller set is larger, and a maximum over a smaller set is smaller. The test of line L6 is strict. Two rotamers that tie are both kept, which is why the loop never empties a residue.

## Example

Three residues A, B and C have the rotamers A0, A1, A2, B0, B1, C0 and C1. The self energies are $E_A = (3, 4, 0)$, $E_B = (0, 0)$ and $E_C = (1, 0)$. The pair energies are zero, except $E_{AB}(A0, B1) = 1$, $E_{AB}(A2, B1) = 3$, $E_{AC}(A0, C1) = 2$, $E_{BC}(B0, C0) = 3$ and $E_{BC}(B0, C1) = 1$.

With all rotamers live, the best case and the worst case of each rotamer (self energy plus the minimum or the maximum pair energy over each neighbour) are:

| rotamer | A0 | A1 | A2 | B0 | B1 | C0 | C1 |
|---|---|---|---|---|---|---|---|
| best case | 3 | 4 | 0 | 1 | 0 | 1 | 0 |
| worst case | 6 | 4 | 3 | 3 | 3 | 4 | 3 |

**Desmet.** A1 has best case 4, and A2 has worst case 3. Since $4 > 3$, A1 goes. A0 has best case 3, which ties with the worst case 3 of A2, so A0 stays. No other test succeeds, now or after the removal. Six rotamers remain, and the search must try $2 \cdot 2 \cdot 2 = 8$ assignments.

**Goldstein.** The tests that succeed, in the order of the loop:

| pass | removed | by | value of $G$ | sets after the removal |
|---|---|---|---|---|
| 1 | A0 | A2 | $3 + \min(0, -2) + \min(0, 2) = 1$ | A1 A2, B0 B1, C0 C1 |
| 1 | A1 | A2 | $4 + \min(0, -3) + \min(0, 0) = 1$ | A2, B0 B1, C0 C1 |
| 1 | C0 | C1 | $1 + \min(0) + \min(2, 0) = 1$ | A2, B0 B1, C1 |
| 2 | B1 | B0 | $0 + \min(3) + \min(-1) = 2$ | A2, B0, C1 |

In pass 1, residue B is tested before C0 goes, and both tests fail: $G(B0, B1) = -2$ and $G(B1, B0) = 0$. In pass 2 the test of B1 against B0 sees only C1 and succeeds. Pass 3 removes nothing. One rotamer is left at each residue, so the answer is A2, B0, C1 with energy $0 + 0 + 0 + 0 + 0 + 1 = 1$. An exhaustive search over all 12 assignments gives the same unique minimum; the next lowest energy is 3, at A2, B1, C1.

## Correctness

The key fact is a swap bound. Let $x$ use rotamer $r$ at residue $i$ and live rotamers elsewhere, and let $x'$ be $x$ with $r$ replaced by $t$. Only the terms that contain residue $i$ change, so

$$E(x) - E(x') = E_i(r) - E_i(t) + \sum_{j \ne i} \big[E_{ij}(r, x_j) - E_{ij}(t, x_j)\big] \ge G_R(i; r, t).$$

If the Goldstein test succeeds, then $E(x') < E(x)$, so $x$ is not a global minimum. The Desmet left side minus its right side is at most $G_R(i; r, t)$, so the same holds for that test. By induction over the removals, each global minimum keeps all its rotamers live: the hypothesis that the other rotamers of the minimum are live is what makes the swap bound apply. So the exhaustive search of line L12 returns a true global minimum, and the set of minima over the live sets is exactly the set of global minima.

A second result compares the two tests. The value $G$ only grows when the live sets shrink, and it is transitive: $G(r, u) \ge G(r, t) + G(t, u)$. From these two facts, the final live sets of the Goldstein loop are subsets of the final live sets of the Desmet loop, for any order of the tests. The full proofs are in the proof file below.

## Complexity

One Goldstein or Desmet test of $(i, r, t)$ reads, for each other residue $j$, the $|R_j| \le p$ pair energies of $r$ and of $t$, so it costs $O(n p)$. One pass of lines L3 to L8 makes at most $n p^2$ tests, so it costs $O(n^2 p^3)$. Each pass except the last removes at least one of the at most $n p$ rotamers, so there are at most $n p - n + 1$ passes, and the elimination takes $O(n^3 p^4)$ time in the worst case. With pairs that interact only within a cutoff, a residue has $d$ neighbours with $d$ often near 10 to 20, and the cost of one test drops to $O(d p)$. The extra space is $O(np)$ for the live sets; the energy tables take $O(n^2 p^2)$, or $O(n d p^2)$ with a cutoff.

The search of line L12 takes $O(n^2 \prod_i |R_i|)$ time by brute force. There is no polynomial bound on it, because finding the GMEC is NP-hard (Pierce and Winfree 2002). Some instances defeat DEE completely. Encode [graph 3-coloring](/three-coloring/) as packing: one residue per vertex, three rotamers (the colours), self energies 0, and a pair energy 1 for equal colours on an edge. For a vertex of degree $k \ge 1$, the neighbour rotamer $s = r$ gives the difference $1 - 0$ and $s = t$ gives $0 - 1$, so $G(r, t) = -k < 0$ for each pair of colours, and no rotamer goes. DEE is a pruning step with a proof of safety, not a polynomial algorithm for the problem.

## Properties

- **Safe.** No global minimum is lost. This holds for any pairwise energy, positive or negative, with exact arithmetic.
- **Order independent.** Different orders of the loop can remove rotamers in different passes, but for a fixed test the final live sets are the same for every order. The proof is a corollary in the proof file.
- **Ties are kept.** If two rotamers are interchangeable, both stay, and the search sees all the global minima.
- **Exact.** Together with an exhaustive search or [A* search](/a-star-search/) over the survivors, the result is a certified global minimum, unlike Monte Carlo packing.

## Variants and improvements

- **Pair elimination.** Remove a pair of rotamers $(r, s)$ at residues $i$ and $j$ when a pair $(t, u)$ beats it against every choice of the other residues. A dead pair is not a dead rotamer, but it cuts the search and can make later single tests succeed.
- **Split and conditional tests.** Split the choices of one neighbour into groups and allow a different competitor $t$ for each group. A rotamer is a dead end if each group has some competitor that beats it.
- **DEE for design.** In [protein design](/protein-design/) the set $R_i$ holds rotamers of several amino acid types, so the same tests choose the sequence and the side chains at once.
- **DEE with A*.** After elimination, a best-first A* search over the residues, with a lower bound from the pair minima, finds the GMEC and can list the next best assignments in order of energy.

## When to use it

Use DEE before an exact search for side-chain packing or fixed-backbone design, when you need a certified global minimum and the energy is pairwise. It works best when a few strong pair terms (clashes) separate the rotamers. When the energy is very flat, few rotamers go, and a [tree decomposition](/tree-decomposition/) method or an integer program is the better exact tool.

## Pitfalls

- **Testing $\ge$ instead of $>$.** With a tie allowed, the swap gives only $E(x') \le E(x)$. Some global minimum still survives, but rotamers of other, tied global minima can go, so the search no longer sees all of them.
- **Floating-point energies.** A test that passes by a rounding error removes a rotamer that may be in the minimum. Compare with a small margin in the safe direction, or use exact or integer energies.
- **A missing neighbour.** The sum must run over each residue $j$ with a nonzero pair term. If the code uses a shorter neighbour list than the energy, the swap bound fails and a test can remove a rotamer of the minimum.
- **Non-pairwise terms.** A solvation term that depends on three or more side chains breaks the swap bound. Then the tests are no longer safe.

## Implementations

## History

Desmet, De Maeyer, Hazes and Lasters published the dead-end elimination theorem in Nature in 1992, with the test that compares the best case of one rotamer with the worst case of another, and used it to place the side chains of proteins. Goldstein (1994) replaced the two bounds by one bound on the energy difference and showed that the new test removes more. Dahiyat and Mayo (1997) used DEE to choose both the sequence and the rotamers in the first fully automated protein design. Pierce and Winfree (2002) showed that the underlying minimization is NP-hard, which explains why DEE is paired with an exact search and has no polynomial guarantee.

## References
