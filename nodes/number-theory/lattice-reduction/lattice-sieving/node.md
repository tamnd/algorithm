---
tag: 8MN8JZ
kind: technique
slug: lattice-sieving
name: Lattice sieving
aliases:
- Ajtai-Kumar-Sivakumar sieve
- sieve algorithms
- AKS sieve
- lattice sieve
area: number-theory/lattice-reduction
level: research
summary: Sieving family that builds many short vectors and combines pairs to find shorter ones.
prereqs: [shortest-vector-problem, lattice-basis, gaussian-heuristic]
see_also: [gauss-sieve, lattice-enumeration, bkz-algorithm, closest-vector-problem, locality-sensitive-hashing, nearest-neighbor-search, hermite-constant, unique-svp]
sources:
  - paper: "M. Ajtai, R. Kumar and D. Sivakumar, A sieve algorithm for the shortest lattice vector problem, STOC 2001"
    locator: pages 601 to 610 (the first randomized algorithm for SVP in time 2^(O(n)), with perturbed samples and a sieve against centers)
  - paper: "P. Q. Nguyen and T. Vidick, Sieve algorithms for the shortest vector problem are practical, Journal of Mathematical Cryptology 2(2) (2008)"
    locator: pages 181 to 207 (the heuristic sieve with time 2^(0.415n) and space 2^(0.2075n), and the 60 degree argument)
  - paper: "D. Micciancio and P. Voulgaris, Faster exponential time algorithms for the shortest vector problem, SODA 2010"
    locator: pages 1468 to 1480 (the list sieve with a proved bound and the Gauss sieve, with the list size bounded by the kissing number)
  - paper: "A. Becker, L. Ducas, N. Gama and T. Laarhoven, New directions in nearest neighbor searching with applications to lattice sieving, SODA 2016"
    locator: pages 10 to 24 (locality-sensitive filters, which give heuristic time 2^(0.292n + o(n)))
  - paper: "D. Aggarwal, D. Dadush, O. Regev and N. Stephens-Davidowitz, Solving the shortest vector problem in 2^n time via discrete Gaussian sampling, STOC 2015"
    locator: the main theorem (a proved randomized sieve over discrete Gaussian samples in time and space 2^(n + o(n)))
  - paper: "M. R. Albrecht, L. Ducas, G. Herold, E. Kirshanova, E. W. Postlethwaite and M. Stevens, The general sieve kernel and new records in lattice reduction, Eurocrypt 2019"
    locator: the sieving framework with progressive sieving and dimensions for free, and its records on the Darmstadt SVP challenge
---

Lattice sieving is a technique for the [shortest vector problem](/shortest-vector-problem/) that keeps a large list of lattice vectors and repeatedly replaces a vector by its difference or sum with another list vector when that is shorter. Short vectors are produced from long ones the way a sieve leaves only the fine grains, and after enough rounds the list contains a shortest vector. Ajtai, Kumar and Sivakumar (2001) used it for the first algorithm with time $2^{O(n)}$ in the rank $n$. Its heuristic variants, such as the [Gauss sieve](/gauss-sieve/) and sieves with locality-sensitive filters, are the fastest known SVP methods in high dimension, with time about $2^{0.292 n}$, but they need memory exponential in $n$. The name has nothing to do with the sieve of Eratosthenes or the number field sieve.

## In plain words

Start with a big bag of points of a grid, all fairly far from the origin. Take two points of the bag. If the step from one to the other is shorter than the longer of the two, that step is itself a grid point closer to the origin, so throw the longer point away and keep the step instead. Repeat this with many pairs.

Two points that point in roughly the same direction always give a shorter step, and when the bag is big enough almost every point has such a partner. So the whole bag slowly moves toward the origin, and at the end its shortest point is a shortest point of the grid. The price is the size of the bag, which grows exponentially with the dimension.

## When it applies

- **The goal is SVP or a related problem** in a lattice given by a basis: exact or approximate SVP, [CVP](/closest-vector-problem/) with preprocessing, or SVP in the blocks of [BKZ](/bkz-algorithm/). The vectors are added and subtracted, so the set of candidates must be closed under these operations, which a lattice is.
- **Memory is available.** A sieve keeps about $2^{0.2075 n}$ vectors in the heuristic versions and $2^{c n}$ with a larger $c$ in the proved ones. Below a few dozen dimensions [enumeration](/lattice-enumeration/), which needs only polynomial space, is faster.
- **Short vectors are dense on spheres.** The heuristic analysis assumes that the list vectors behave like points spread uniformly over a sphere, which holds well for random lattices and for the projected blocks inside BKZ, and less well for lattices with a lot of structure.
- **Cost model.** The unit cost is one inner product or one vector addition in dimension $m$ on numbers of size polynomial in the input, done exactly on integer coefficient vectors or in floating point on Gram-Schmidt coordinates in practice. All bounds below have the form $2^{c n + o(n)}$ times a polynomial in the input size; the text says which are proved and which are heuristic.

## The template

The template works on a list $S$ of nonzero lattice vectors. The named holes, written in capitals, are filled differently by each member of the family.

```pseudo id=main
SIEVE(B)                                          ▷ basis rows b_1..b_n of L; returns a short nonzero v ∈ L
L1  S ← SAMPLE(B, N)                              ▷ hole SAMPLE: N lattice vectors, N set by LIST-SIZE
L2  repeat
L3      for each pair (u, w) in S with ‖u‖ ≥ ‖w‖ chosen by PAIRS(S) do    ▷ hole PAIRS
L4          r ← the shorter of u − w and u + w
L5          if ‖r‖ < ‖u‖ then replace u by r in S       ▷ a reduction; r ∈ L
L6      remove the zero vectors from S, counting them as collisions
L7  until STOP(S)                                 ▷ hole STOP: no reduction in a pass, enough collisions, or a target length
L8  return a shortest vector of S
```

**The holes.**

- *SAMPLE* draws lattice vectors: random small combinations of a reduced basis, Klein's randomized [nearest plane](/babai-nearest-plane/) method, or discrete Gaussian samples. In the proved AKS sieve a sample is a pair of a small random perturbation $e$ and the lattice point $x$ with $x + e$ reduced modulo the basis.
- *LIST-SIZE* $N$ must be large enough that most vectors find a partner; heuristically $N \approx (4/3)^{n/2}$.
- *PAIRS* chooses which pairs to test: all pairs, a list against a fresh vector as in the Gauss sieve, or only pairs that fall in a common bucket of a [locality-sensitive hash](/locality-sensitive-hashing/), which is a [nearest neighbor search](/nearest-neighbor-search/) for the vector $\pm w$ closest to $u$.
- *STOP* decides when the list is done.

**Why line L5 makes progress.** For $\|u\| \ge \|w\|$, $\|u - w\|^2 = \|u\|^2 + \|w\|^2 - 2 \langle u, w \rangle$, which is less than $\|u\|^2$ exactly when $2 \langle u, w \rangle > \|w\|^2$. If $\|u\| = \|w\|$, this says that the angle between $u$ and $w$ is less than $60°$. Line L4 also tries $u + w$, which covers the angles above $120°$. Every replacement strictly lowers $\sum_{v \in S} \|v\|^2$, which is a nonnegative integer for an integer basis, so the loop ends.

**What a finished list looks like.** When no pair can be reduced, every pair $u, w$ with $\|w\| \le \|u\|$ has $2 |\langle u, w \rangle| \le \|w\|^2 \le \|w\| \|u\|$, so the angle between them is at least $60°$ and at most $120°$. The directions $u / \|u\|$ then form a set of points on the unit sphere with pairwise angles at least $60°$, so the list has at most the kissing number $\tau_n \le 2^{0.401 n}$ vectors (Kabatiansky and Levenshtein). This is the bound Micciancio and Voulgaris prove for the Gauss sieve.

**The heuristic count.** Two independent uniform directions on the sphere have angle below $60°$ with probability about $(\sin 60°)^n = (3/4)^{n/2} = 2^{-0.2075 n}$. So a list of $N = (4/3)^{n/2} = 2^{0.2075 n}$ vectors of about the same length gives each vector a partner, and testing all pairs costs $N^2 = 2^{0.415 n}$ per pass. Each pass shrinks the lengths by a constant factor until they reach about the [Gaussian heuristic](/gaussian-heuristic/) value of $\lambda_1$, so a polynomial number of passes suffices. This is the analysis of Nguyen and Vidick, under the assumption that the list vectors stay uniformly spread; it is a heuristic confirmed by experiments, not a theorem.

**Walk-through.** Take the basis $(1, 1, 1), (-1, 0, 2), (3, 5, 6)$, with $\lambda_1, \lambda_2, \lambda_3 = 1, \sqrt 2, \sqrt 5$. Let SAMPLE return 6 random combinations with coefficients in $\{-2, \ldots, 2\}$ (seed 5), with squared lengths $12, 114, 161, 26, 266, 114$; two of them are $\pm (7, 7, 4)$. Let PAIRS test all ordered pairs in order and STOP end after a pass with no reduction. The squared lengths after the passes are

| pass | squared lengths in $S$ |
|---|---|
| 1 | $12, 24, 27, 6, 57, 12$ |
| 2 | $10, 4, 9, 6, 6, 0$ |
| 3 | $6, 4, 3, 2, 0, 0$ |
| 4 | $5, 1, 0, 2, 0, 0$ |
| 5 | no reduction |

The final list is $(1, 0, -2), (0, 1, 0), (1, 0, 1)$ with three collisions, and the shortest vector $(0, 1, 0)$ is a shortest vector of the lattice. Here the surviving vectors even reach all three successive minima; in high dimension the list instead fills a shell near $\lambda_1$.

## Classic examples

- **The AKS sieve (proved).** Ajtai, Kumar and Sivakumar sample perturbed points and sieve them against a set of centers, shrinking the lengths by a constant factor per round. The perturbations hide whether a point stands for $x$ or $x + s$ with $s$ a shortest vector, so at the end a difference of two list points is $s$ with probability bounded below. The time and space are $2^{O(n)}$, proved; later analyses give constants such as $2^{2.465 n}$ for the time (Pujol and Stehlé).
- **The Nguyen-Vidick sieve (heuristic).** The pair sieve of the template with all pairs tested, time $2^{0.415 n}$ and space $2^{0.2075 n}$.
- **The [Gauss sieve](/gauss-sieve/) (heuristic, practical).** Micciancio and Voulgaris keep the list pairwise reduced and reduce each new vector against it, and the list vectors against the new one. Its space is at most the kissing number, proved, but its running time has no proved bound; in practice it is faster than the Nguyen-Vidick sieve. Their list sieve, which reduces only new vectors against the list, has proved time $2^{3.199 n}$.
- **Sieves with nearest neighbor search (heuristic).** Bucketing the list with locality-sensitive hashing (Laarhoven's HashSieve, about $2^{0.337 n}$) or with locality-sensitive filters (Becker, Ducas, Gama and Laarhoven, $2^{0.292 n + o(n)}$) tests only pairs that are likely to reduce. The space stays $2^{0.2075 n}$.
- **Discrete Gaussian sieving (proved).** Aggarwal, Dadush, Regev and Stephens-Davidowitz pair up discrete Gaussian samples $x, y$ in the same coset of $2L$ and keep $(x + y)/2 \in L$, which shrinks the Gaussian parameter by $\sqrt 2$ while keeping the distribution exactly discrete Gaussian, and solve SVP in time and space $2^{n + o(n)}$, the best proved bound.
- **Sieving inside BKZ.** The general sieve kernel of Albrecht and others uses a sieve as the SVP oracle of [BKZ](/bkz-algorithm/), with progressive sieving and the "dimensions for free" trick of Ducas, which solves SVP in rank $n$ with a sieve in rank $n - \Theta(n / \log n)$. It holds the records of the Darmstadt SVP challenge.

## Variations

- **Tuple sieving.** Combine three or more vectors at a time, $u \pm w \pm z$. The list can be smaller, about $2^{0.1887 n}$ for triples, at the cost of more time; useful when memory is the limit.
- **Sieving for CVP.** Sieve the vectors $t - v$ for a target $t$ against a list of short lattice vectors, or preprocess the list once and answer many targets.
- **Quantum sieving.** Grover search over the list for a partner gives heuristic time about $2^{0.265 n}$ with locality-sensitive filters. This figure is from Laarhoven's PhD thesis. Laarhoven, Mosca and van de Pol gave the first quantum sieves, with larger exponents.
- **Progressive sieving.** Sieve first in a projected sublattice of small rank, then lift and extend the list one dimension at a time; this saves a constant factor in practice.

## Pitfalls

- **Memory, not time, is the wall.** In dimension 100 the heuristic list has about $(4/3)^{50} \approx 1.8 \times 10^6$ vectors, and in dimension 150 about $2.4 \times 10^9$. Each vector has $m$ coordinates, so the memory reaches terabytes well before the time becomes infeasible.
- **Too small a list.** With $N$ well below $(4/3)^{n/2}$, most vectors have no partner and the list stops shrinking at a length far above $\lambda_1$; the output is then only an approximate shortest vector.
- **Collisions.** Different list vectors can reduce to the same vector or to 0. Zero vectors must be removed (line L6), and many collisions are a sign that the list is saturated, which is what the Gauss sieve uses as its STOP rule.
- **Heuristic versus proved.** The exponents $0.415$, $0.337$ and $0.292$ rest on the uniform distribution heuristic. The proved exponents are much larger, from $2.465$ down to $1$, and they come from different algorithms. Security estimates use the heuristic ones, with their $o(n)$ terms fitted from experiments.
- **Not a reduction by itself.** A sieve returns short vectors, not a reduced basis. Inserting the vectors into a basis needs a step such as LLL on the extended generating set, to remove the dependencies.

## Exercises

1. Show that for nonzero $u, w$ with $\|u\| = \|w\|$, $\|u - w\| < \|u\|$ if and only if the angle between $u$ and $w$ is less than $60°$, and that $\|u + w\| < \|u\|$ if and only if it is more than $120°$.
2. Prove that the sum of the squared lengths strictly decreases at each replacement of line L5, and conclude that SIEVE terminates on an integer basis.
3. Prove that a list in which no pair can be reduced has at most $\tau_n$ vectors, where $\tau_n$ is the kissing number in dimension $n$.
4. Compute $(4/3)^{n/2}$ for $n = 60, 100, 150$, and the memory of such a list when each vector is stored as $n$ coordinates of 4 bytes.
5. Run the template on $\mathbb{Z}^2$ with the samples $(3, 1), (2, 1), (5, 2), (1, 1)$ and list the replacements.

## References
