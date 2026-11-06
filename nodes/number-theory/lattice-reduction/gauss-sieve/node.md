---
tag: 6BDMG5
kind: algorithm
slug: gauss-sieve
name: Gauss sieve
aliases:
- Micciancio-Voulgaris sieve
- GaussSieve
- Gauss Sieve
area: number-theory/lattice-reduction
level: research
summary: Practical sieve that keeps a list of mutually reduced vectors to solve SVP.
solves: [shortest-vector-problem]
model: word-ram
complexity:
  vars: {n: the rank of the lattice, m: the length of the vectors, τ_n: the kissing number in dimension n, at most 2^(0.401 n + o(n)), R: the total number of passes of the reduction loop over all iterations, finite but with no proved bound, H: the largest size of the stack}
  time: {worst: O(R τ_n m), per_pass: O(τ_n m), heuristic: 2^(0.415 n + o(n))}
  space: {extra: O((τ_n + H) m), heuristic: 2^(0.208 n + o(n))}
properties: {deterministic: false, randomized: true, recursive: false, exact_arithmetic: true, proved_optimal: false}
history:
  year: 2010
  people: [Daniele Micciancio, Panagiotis Voulgaris]
  note: Micciancio and Voulgaris introduced the List Sieve, with a proved running time, and the Gauss Sieve, a practical variant without one, at SODA 2010.
prereqs: [shortest-vector-problem, lagrange-gauss-reduction, lattice]
see_also: [lattice-sieving, gaussian-heuristic, lattice-enumeration, kannan-enumeration, bkz-algorithm, hermite-constant, fincke-pohst-enumeration, approximate-svp]
sources:
  - paper: "D. Micciancio and P. Voulgaris, Faster exponential time algorithms for the shortest vector problem, Proceedings of the 21st ACM-SIAM Symposium on Discrete Algorithms (SODA 2010)"
    locator: pages 1468 to 1480 (the List Sieve with its proved bound, and the Gauss Sieve with its experiments)
  - paper: "P. Q. Nguyen and T. Vidick, Sieve algorithms for the shortest vector problem are practical, Journal of Mathematical Cryptology 2(2) (2008)"
    locator: pages 181 to 207 (the heuristic sieve with time 2^(0.415 n) and memory 2^(0.208 n))
  - paper: "G. A. Kabatiansky and V. I. Levenshtein, Bounds for packings on a sphere and in space, Problems of Information Transmission 14(1) (1978)"
    locator: pages 1 to 17 (the upper bound 2^(0.401 n) on the kissing number)
  - paper: "A. Becker, L. Ducas, N. Gama and T. Laarhoven, New directions in nearest neighbor searching with applications to lattice sieving, SODA 2016"
    locator: pages 10 to 24 (locality-sensitive filtering and the heuristic time 2^(0.292 n))
---

The Gauss sieve finds short vectors of a [lattice](/lattice/) by keeping a list of lattice vectors in which every pair is reduced in the sense of [Lagrange-Gauss](/lagrange-gauss-reduction/): no vector of the list can be made shorter by adding or subtracting a multiple of another. New random lattice vectors are reduced against the list, and the list vectors that the new vector can shorten are taken out, reduced and processed again. Micciancio and Voulgaris introduced it in 2010. The list stays within the kissing number $2^{0.401 n + o(n)}$, which is proved; that the shortest list vector is a shortest vector of the lattice, and the running time of about $2^{0.415 n}$, are heuristic but borne out by experiments, and the Gauss sieve and its descendants are the fastest practical [shortest vector](/shortest-vector-problem/) algorithms in high dimension.

## In plain words

Keep a bag of grid arrows with one rule: no arrow in the bag may get shorter by adding or taking away another arrow of the bag.

Make a new arrow at random. Try every arrow in the bag on it, and shorten it while you can. If it shrinks to nothing, that is a collision: the bag already knew everything the new arrow had to say. Otherwise, put it in the bag, but first take out every longer arrow that the new one can shorten. Shorten those, and treat them as new arrows later.

Arrows in the bag point in clearly different directions, so the bag cannot grow without limit. As it fills up, more and more new arrows shrink to nothing, and once collisions come often, the shortest arrow in the bag is very likely a shortest arrow of the whole grid.

## The problem

**Input.** Linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$ of a lattice $L$, a collision limit $c \ge 1$ and a sample budget $M$.

**Output.** A nonzero $v \in L$, meant to satisfy $\|v\| = \lambda_1(L)$. The algorithm guarantees only that $v$ is a nonzero lattice vector no longer than any $b_i$ and that the final list is pairwise reduced; the equality $\|v\| = \lambda_1$ is the heuristic outcome for a large enough $c$.

**Notation and cost model.** As on the other pages of this area, basis vectors are rows $b_1, \ldots, b_n$, $b_i^*$ and $\mu_{ij}$ are the Gram-Schmidt data, $\lambda_1$ is the first minimum, $\det(L)$ is the determinant and $\delta$ is the reduction parameter of a preprocessing step such as LLL. Two vectors are **Gauss-reduced** when $2 |\langle u, w \rangle| \le \min(\|u\|^2, \|w\|^2)$. The reference implementation uses exact rational arithmetic, and time counts arithmetic operations on rationals. The bound on the list size is proved; the running time, the memory in practice and the probability of success are heuristic or observed. Practical implementations use floating point or integers of fixed width.

## The algorithm

```pseudo id=main
GAUSS-SIEVE(B, c, M)                ▷ independent rows b_1..b_n, collision limit c, sample budget M
L1  𝓛 ← ∅; S ← (b_1, ..., b_n); K ← 0
L2  while S ≠ ∅ or (K < c and fewer than M samples drawn)
L3      v ← pop(S) if S ≠ ∅, else a new random lattice vector
L4      repeat: for w ∈ 𝓛 with ‖w‖ ≤ ‖v‖ and 2|⟨v, w⟩| > ‖w‖², v ← v − ⌊⟨v, w⟩ / ‖w‖²⌉ w; until no change
L5      if v = 0 then K ← K + 1; go to L2
L6      for each w ∈ 𝓛 with ‖w‖ > ‖v‖ and 2|⟨v, w⟩| > ‖v‖²
L7          remove w from 𝓛; push w − ⌊⟨w, v⟩ / ‖v‖²⌉ v onto S
L8      add v to 𝓛
L9  return a shortest vector of 𝓛
```

Here $\lfloor t \rceil$ is the nearest integer to $t$. Line L4 reduces the new vector against the shorter list vectors, and line L6 reduces the longer list vectors against the new one; together they keep every pair in the list Gauss-reduced. A vector moved to the stack on line L7 goes through line L4 again, because after its reduction it may be reducible by other list vectors.

The sampler of line L3 matters in practice. Micciancio and Voulgaris use Klein's randomized [nearest plane](/babai-nearest-plane/) algorithm on an [LLL](/lll-algorithm/)-reduced basis, which gives fairly short vectors. The reference implementation draws $\sum x_i b_i$ with $x_i$ uniform in $\{-2, \ldots, 2\}$, which is enough in dimension at most 6.

## Example

The basis $b_1 = (4, 4)$, $b_2 = (9, 10)$ of the lattice generated by $(2, 0)$ and $(1, 2)$, with $\lambda_1 = 2$, and $c = 3$. The samples come from the seed 0 of the reference implementation.

| Step | $v$ from L3 | Reductions on L4 | Action | List after the step |
|------|------|------|------|------|
| 1 | $b_1 = (4, 4)$ | none, the list is empty | add | $(4, 4)$ |
| 2 | $b_2 = (9, 10)$ | $q = \lfloor 76/32 \rceil = 2$: $(1, 2)$ | $(4, 4)$ is longer and $2 \cdot 12 > 5$: push $(4, 4) - 2 \cdot (1, 2) = (2, 0)$; add $(1, 2)$ | $(1, 2)$ |
| 3 | $(2, 0)$ from the stack | none, $(1, 2)$ is longer | $2 \cdot 2 \le 4$, so $(1, 2)$ stays; add | $(1, 2), (2, 0)$ |
| 4 | sample $(13, 14)$ | $(5, -2)$, $(-1, -2)$, $(0, 0)$ | collision $K = 1$ | unchanged |
| 5 | sample $(-8, -8)$ | $(-3, 2)$, $(-1, 2)$, $(-2, 0)$, $(0, 0)$ | collision $K = 2$ | unchanged |
| 6 | sample $(17, 18)$ | $(6, -4)$, $(0, -4)$, $(2, 0)$, $(0, 0)$ | collision $K = 3$, stop | unchanged |

The output is $(2, 0)$, a shortest vector. The final list $(1, 2), (2, 0)$ is Gauss-reduced: $2 |\langle (1, 2), (2, 0) \rangle| = 4 \le \min(5, 4)$. In step 4, the reduction of $(5, -2)$ by $(2, 0)$ has $t = \tfrac{10}{4} = 2.5$, a tie, which the implementation rounds up to $q = 3$. The test file checks the output and the final list.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Each reduction step subtracts the nearest integer multiple $q w$ with $|t| > 1/2$ for $t = \langle v, w \rangle / \|w\|^2$, and $\|v - q w\|^2 - \|v\|^2 = \|w\|^2 q (q - 2t) < 0$. So every step makes a lattice vector strictly shorter, and since squared lengths of lattice vectors lie in a discrete set, every reduction loop stops.

The list stays pairwise Gauss-reduced: line L4 handles the pairs with shorter list vectors, line L6 removes every longer vector that the new one could shorten, and pairs already in the list do not change. Two Gauss-reduced vectors make an angle between $60°$ and $120°$, so the directions of the list vectors are points on the unit sphere of $\operatorname{span}(L)$ with pairwise angles at least $60°$, and the list has at most $\tau_n$ vectors, the kissing number. The shortest list vector never gets longer, and every processed vector, in particular every $b_i$, is at least as long as it.

For termination, samples are bounded by $M$, and between two samples the pair (multiset of squared lengths in list and stack, size of the stack) decreases in a well-founded order.

## Complexity

- **List size, proved.** $|\mathcal L| \le \tau_n \le 2^{0.401 n + o(n)}$ by the Kabatiansky-Levenshtein bound. One pass of line L4 or line L6 costs $O(|\mathcal L| m)$ operations.
- **Running time, open.** No bound on the number of iterations in terms of $n$ is proved: vectors can move between the list and the stack many times. The related List Sieve of the same paper, which never removes list vectors and uses perturbations, has the proved bound $2^{3.199 n + o(n)}$ time and $2^{1.325 n + o(n)}$ space.
- **Heuristic cost.** Under the heuristic that reduced vectors behave like uniform points on a sphere, the list grows to about $(4/3)^{n/2} = 2^{0.208 n}$ vectors and the time is about $(4/3)^{n} = 2^{0.415 n}$, as in the Nguyen-Vidick sieve. The experiments of Micciancio and Voulgaris fit running times that grow somewhat faster in the dimensions they reached, because of collisions and the cost of the stack.
- **Success.** The probability that the output equals $\lambda_1$ for a given $c$ is not proved. The usual stopping rule, a number of collisions proportional to the list size, worked in all reported experiments. On the random lattices of dimension 2 to 6 of the test file, every run with $c = 15$ found $\lambda_1$.
- **Exact arithmetic.** With rationals the entries can grow in the reductions; the list vectors are short, so in practice they stay small.

## Properties

- **Randomized.** The output depends on the samples; with a fixed seed it is deterministic.
- **Monotone.** The shortest vector in the list never gets longer, so stopping early still gives a short vector, at least as short as every basis vector.
- **Basis-independent list.** Unlike [enumeration](/lattice-enumeration/), the list depends on the lattice and the samples but not on the quality of the basis, except through the sampler.
- **Memory-bound.** The list is exponential in $n$; in high dimension memory, not time, is the first limit.

## Variants and improvements

- **Nguyen-Vidick sieve (2008).** Reduces a whole batch of vectors against centres in rounds; its heuristic analysis gives the $2^{0.415 n}$ time and $2^{0.208 n}$ memory that the Gauss sieve meets in practice.
- **List Sieve.** The provable variant of Micciancio and Voulgaris, with random perturbations that make the analysis possible.
- **Locality-sensitive hashing and filtering.** Search the list only for vectors near the new one: Laarhoven's HashSieve reaches $2^{0.337 n}$ heuristic time, and the filtering of Becker, Ducas, Gama and Laarhoven reaches $2^{0.292 n}$, the best known classical exponent; quantum search lowers it to about $2^{0.265 n}$.
- **Progressive and triple sieves.** Start in a lower dimension and add basis vectors as the list fills, or reduce triples of vectors to save memory.
- **Sieving in BKZ.** The G6K framework uses sieving as the oracle of [BKZ](/bkz-algorithm/) and holds records for the Darmstadt SVP challenge.

## When to use it

- For exact SVP in dimension above about 60 to 80, where sieving beats [enumeration](/lattice-enumeration/) in current implementations; below that, enumeration with pruning is faster and needs almost no memory.
- As the block oracle of BKZ with large blocks, in cryptanalysis of lattice schemes.
- Not when memory is tight: the list in dimension 100 has tens of millions of vectors.
- Not when a proved answer is needed: use [Kannan's enumeration](/kannan-enumeration/) or the proved $2^{O(n)}$ algorithms.

## Pitfalls

- **Forgetting to re-process removed vectors.** A list vector reduced on line L7 must go through line L4 again; inserting it straight back into the list breaks the pairwise reduction.
- **Strict inequalities.** Reduce only when $2 |\langle v, w \rangle| > \|w\|^2$. With $\ge$, ties loop forever, since $v - w$ then has the same length as $v$.
- **A bad sampler.** Sampling long vectors makes reductions slow and the list fills with long vectors; sample from an LLL- or BKZ-reduced basis.
- **Stopping on the first collisions.** Early collisions are common when the list is small; stop only after many, in proportion to the list size.
- **Reading the output as proved.** The shortest list vector is not certified; check it with enumeration if a proof is needed.

## Implementations

## History

Ajtai, Kumar and Sivakumar introduced sieving for the shortest vector problem in 2001, with a randomized algorithm of time $2^{O(n)}$ but large constants. Nguyen and Vidick showed in 2008 that a heuristic version is practical, with time about $2^{0.415 n}$. Micciancio and Voulgaris presented the List Sieve and the Gauss Sieve at SODA 2010; the Gauss sieve, with its pairwise reduced list and stack, became the base of later practical sieves. Laarhoven's HashSieve of 2015, the filtering of Becker, Ducas, Gama and Laarhoven of 2016, and the G6K framework of Albrecht, Ducas, Herold, Kirshanova, Postlethwaite and Stevens of 2019 made sieving the fastest method in practice, and it now sets the records of the Darmstadt SVP challenge.

## References
