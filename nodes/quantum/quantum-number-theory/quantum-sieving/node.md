---
tag: Y3ARK8
kind: algorithm
slug: quantum-sieving
name: Quantum lattice sieving
aliases:
- quantum sieve for shortest vectors
- Grover-based lattice sieving
area: quantum/quantum-number-theory
level: research
summary: A lattice sieve whose search for reducing partners in its list uses quantum search. It lowers the heuristic SVP exponent from 0.292n to about 0.257n, a constant-factor gain in the exponent only.
solves: [shortest-vector-problem]
model: quantum-circuit-model
complexity:
  vars: {n: "the lattice dimension", N: "the number of vectors in the list", t: "the number of reducing partners in the list"}
  time: {quantum_gauss_sieve: 2^(0.312 n + o(n)), quantum_bdgl_sieve: 2^(0.2653 n + o(n)), quantum_walk_sieve: 2^(0.2570 n + o(n)), classical_bdgl_sieve: 2^(0.292 n + o(n)), provable_quantum_sieve: 2^(1.799 n + o(n)), partner_search_queries: O(sqrt(N / t))}
  space: {list: 2^(0.2075 n + o(n)), qram_words: 2^(0.2075 n + o(n))}
properties: {deterministic: false, exact: false, heuristic: true, quantum: true, needs_qram: true}
history:
  year: 2013
  people: [Thijs Laarhoven, Michele Mosca, Joop van de Pol]
  note: Laarhoven, Mosca and van de Pol put Grover search into the sieves of Nguyen and Vidick and of Micciancio and Voulgaris at PQCrypto 2013.
prereqs: [gauss-sieve, grover-search, amplitude-amplification, shortest-vector-problem, quantum-random-access-memory]
see_also: [lattice-sieving, core-svp-hardness, locality-sensitive-hashing, quantum-walk-search, learning-with-errors, post-quantum-cryptography, bkz-algorithm, regev-factoring-algorithm]
sources:
  - paper: arxiv:1301.6176
    title: Thijs Laarhoven, Michele Mosca and Joop van de Pol, Solving the shortest vector problem in lattices faster using quantum search, PQCrypto 2013
    locator: the abstract and the main results (heuristic 2^(0.312 n) for the quantum Nguyen-Vidick sieve and Gauss sieve; provable 2^(1.799 n))
  - paper: doi:10.1007/s10623-015-0067-5
    title: "Thijs Laarhoven, Michele Mosca and Joop van de Pol, Finding shortest lattice vectors faster using quantum search, Designs, Codes and Cryptography 77(2):375-400, 2015 (preprint IACR ePrint 2014/907)"
    locator: the quantum versions of the hash-based sieves (2^(0.268 n) in the journal version, 2^(0.286 n) in the ePrint version)
  - paper: "Thijs Laarhoven, Search problems in cryptography: from fingerprinting to lattice sieving, PhD thesis, Eindhoven University of Technology, 2016"
    title: "Thijs Laarhoven, Search problems in cryptography: from fingerprinting to lattice sieving, PhD thesis, Eindhoven University of Technology, 2016"
    locator: the chapter on sieving with locality-sensitive filters and its quantum version (2^(0.2653 n))
  - url: https://eprint.iacr.org/2021/570
    title: "André Chailloux and Johanna Loyer, Lattice sieving via quantum random walks, ASIACRYPT 2021, LNCS 13093, pages 63-91"
    locator: the main theorem (heuristic 2^(0.2570 n)) and the tradeoffs between time and quantum memory
  - paper: arxiv:2410.15565
    title: Beomgeun Cho, Minki Hhan, Taehyun Kim, Jeonghoon Lee and Yixin Shen, Does quantum lattice sieving require quantum RAM?, 2024
    locator: the abstract (a lower bound with bounded QRAM, and a QRAM-free circuit with exponentially many qubits)
  - url: https://eprint.iacr.org/2019/1161
    title: Martin R. Albrecht, Vlad Gheorghiu, Eamonn W. Postlethwaite and John M. Schanck, Estimating quantum speedups for lattice sieves, ASIACRYPT 2020 (revised as IACR ePrint 2019/1161)
    locator: the abstract and the conclusions on cryptanalytically relevant dimensions
  - paper: arxiv:quant-ph/9605034
    title: "Michel Boyer, Gilles Brassard, Peter Høyer and Alain Tapp, Tight bounds on quantum searching, Fortschritte der Physik 46:493-505, 1998"
    locator: the search algorithm for an unknown number of solutions and its expected number of iterations
  - paper: arxiv:quant-ph/9605043
    title: Lov K. Grover, A fast quantum mechanical algorithm for database search, STOC 1996
    locator: the search algorithm and its O(sqrt(N)) query count
  - paper: "Anja Becker, Léo Ducas, Nicolas Gama and Thijs Laarhoven, New directions in nearest neighbor searching with applications to lattice sieving, SODA 2016"
    title: "Anja Becker, Léo Ducas, Nicolas Gama and Thijs Laarhoven, New directions in nearest neighbor searching with applications to lattice sieving, SODA 2016"
    locator: the classical sieve with heuristic time 2^(0.292 n)
---

Quantum lattice sieving is a family of algorithms for the [shortest vector problem](/shortest-vector-problem/) that keep the structure of a classical [lattice sieve](/lattice-sieving/) and do the search for a reducing partner in the list with [Grover search](/grover-search/). For the [Gauss sieve](/gauss-sieve/) this changes the heuristic time from $2^{0.415 n}$ to $2^{0.312 n}$, and the best known quantum sieve reaches $2^{0.2570 n}$ against $2^{0.292 n}$ classically. The gain is a smaller constant in the exponent: the time stays exponential in the dimension $n$, and lattice problems are not known to be in [BQP](/bqp/).

## In plain words

A sieve keeps a long list of lattice vectors. Each new vector is compared with the list to find a partner that makes it shorter when one is subtracted from the other. Most of the classical time goes into this comparison, because the list is very long and partners are rare.

Quantum search finds a rare item in a list in about the square root of the number of checks that a scan needs. A quantum sieve uses it for the partner search and leaves the rest of the sieve as it is.

The list must be readable in superposition, so the method needs a large quantum memory of a special type. The saving is real but modest. The work is still exponential, so the sieve stays a slow attack, and the security estimates of lattice cryptography already allow for it.

## The problem

Given a basis of a lattice $\Lambda \subset \mathbb{Z}^n$, find a nonzero vector of $\Lambda$ of minimum Euclidean length. Sieves solve this heuristically: they do not prove that the output is a shortest vector, but under the heuristic assumptions of the [lattice sieving](/lattice-sieving/) page they find one with high probability. The quantum part works in the [quantum circuit model](/quantum-circuit-model/) with a [quantum random access memory](/quantum-random-access-memory/) (QRAM) that holds the list as classical data and answers queries in superposition.

## The algorithm

The sieve is the [Gauss sieve](/gauss-sieve/) of Micciancio and Voulgaris. A vector $w$ reduces $v$ if $2|\langle v, w \rangle| > \|w\|^2$, and then $\|v \mp w\| < \|v\|$, with the sign of $\langle v, w \rangle$. Each search in lines L4 and L6 is a call of SEARCH, the algorithm of Boyer, Brassard, Høyer and Tapp (BBHT) for an unknown number of marked items. Its oracle is the predicate $f$ evaluated on $L[i]$, with $L[i]$ read from QRAM; it is an instance of a [quantum oracle](/quantum-oracle/) and of [amplitude amplification](/amplitude-amplification/).

```pseudo id=main
QUANTUM-GAUSS-SIEVE(B, c_max)
L1  L ← empty list; S ← the rows of B; c ← 0
L2  while c < c_max do
L3      v ← pop(S) if S is not empty, else a random vector of the lattice
L4      while i ← SEARCH(L, w ↦ 2|⟨v,w⟩| > ‖w‖²) is not ⊥ do v ← v ∓ L[i]
L5      if v = 0 then c ← c + 1 and go to L2      ▷ a collision
L6      while i ← SEARCH(L, w ↦ 2|⟨v,w⟩| > ‖v‖²) is not ⊥ do move L[i] ∓ v from L to S
L7      append v to L
L8  return the shortest vector of L

SEARCH(L, f)                                     ▷ BBHT, with q = ⌈log₂ |L|⌉ index qubits
L9  m ← 1; spent ← 0
L10 while spent < C·√(2^q) do
L11     draw j uniformly from {0, ..., ⌈m⌉ − 1}; run j Grover iterations with oracle f; measure i
L12     if i < |L| and f(L[i]) then return i      ▷ one classical check
L13     m ← min(λm, √(2^q)) with λ = 6/5
L14 return ⊥
```

**Line L11.** If $t$ of the $2^q$ indices are marked and $\sin^2 \theta = t / 2^q$, then $j$ Grover iterations followed by a measurement give a marked index with probability $\sin^2((2j + 1)\theta)$. Since $t$ is unknown, no fixed $j$ is safe: too many iterations rotate past the marked states. BBHT draws $j$ at random from a range that grows by the factor $\lambda$ until a marked index appears.

**Line L10.** The budget $C \sqrt{2^q}$ ends a search that finds nothing. A search with no partner then costs $O(\sqrt{|L|})$ queries, where a scan costs $|L|$. A search can also end with $\perp$ when partners exist; this is a miss, and its effect is discussed under Pitfalls.

## Example

Take the lattice $\Lambda$ of $y \in \mathbb{Z}^4$ with $y_0 \equiv 865 y_1 + 395 y_2 + 777 y_3 \pmod{1009}$, with basis rows $(1009, 0, 0, 0)$, $(865, 1, 0, 0)$, $(395, 0, 1, 0)$ and $(777, 0, 0, 1)$. Suppose the list is

$$L = [(0, 2, -3, -2),\ (1, 5, 3, 2),\ (6, 1, -1, 2),\ (1, -2, 4, -5)]$$

and the new vector is $v = (-1222, 1, 1, 2)$, a vector of $\Lambda$ because $865 + 395 + 1554 - (-1222) = 4036 = 4 \cdot 1009$. The inner products of $v$ with the list are $-5$, $-1210$, $-7328$ and $-1230$, and the squared lengths are $17$, $39$, $42$ and $46$. So the last three entries reduce $v$, and $t = 3$ of the $2^q = 4$ indices are marked.

Then $\sin^2 \theta = 3/4$ and $\theta = \pi/3$. With $j = 0$ the measurement gives a marked index with probability $\sin^2(\pi/3) = 3/4$. With $j = 1$ the probability is $\sin^2(\pi) = 0$: one Grover iteration rotates past the marked states. With $j = 2$ it is $3/4$ again. This is why line L11 draws $j$ at random. If the search returns $i = 2$, then $v$ becomes $v + (6, 1, -1, 2) = (-1216, 2, 0, 4)$, which is shorter.

The page's implementation simulates SEARCH exactly. It samples the measured index from the distribution above; the tests check this rule against a full state-vector simulation. On this lattice, with sieve seed 100 and $c_{\max} = 50$, the quantum sieve returns $(0, 2, -3, -2)$, of squared length 17. A brute-force search over the box confirms that 17 is the squared length of a shortest vector. In that run one search missed, and $v = (-1222, 1, 1, 2)$ stayed in the final list without reduction.

For one search on a list of $N = 1024$ items with $t$ marked items, the simulator gives these mean query counts over seeds 0 to 199. A query is a Grover iteration or a classical check; the scan counts one query per item it reads.

| $t$ | quantum, mean | quantum, largest | $\sqrt{N/t}$ | classical scan, mean |
|---|---|---|---|---|
| 1 | 51.2 | 139 | 32 | 507.2 |
| 4 | 26.8 | 98 | 16 | 210.6 |
| 16 | 12.6 | 30 | 8 | 55.8 |

## Correctness

The sieve keeps every vector of $L$ and $S$ in $\Lambda$, because it only adds and subtracts lattice vectors. Every reduction makes a vector strictly shorter, so the loops in L4 and L6 end. SEARCH checks each measured index classically in L12, so it never returns a non-partner. If no search misses, every pair $u, w$ in the final list satisfies $2|\langle u, w \rangle| \le \min(\|u\|^2, \|w\|^2)$, as in the classical Gauss sieve. That the shortest vector of $L$ is a shortest vector of $\Lambda$ is the heuristic claim of the classical sieve, and the quantum search does not change it. The proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

All bounds are heuristic, for the dimension $n \to \infty$, in the quantum circuit model with QRAM access to the classical list. The cost of one QRAM query is counted as one time step. Under this cost model, the exponents of the time are as follows.

| Classical sieve | classical time | quantum time | quantum result |
|---|---|---|---|
| Nguyen-Vidick sieve and Gauss sieve | $2^{0.415 n}$ | $2^{0.312 n}$ | Laarhoven, Mosca and van de Pol, 2013 |
| HashSieve with angular hashing | $2^{0.337 n}$ | $2^{0.286 n}$ | the same authors, ePrint version, 2014 |
| sieve with spherical hashing (Laarhoven and de Weger) | $2^{0.298 n}$ | $2^{0.268 n}$ | the same authors, journal version, 2015 |
| sieve with spherical filters (Becker, Ducas, Gama and Laarhoven) | $2^{0.292 n}$ | $2^{0.2653 n}$ | Laarhoven, PhD thesis, 2016 |
| spherical filters with a quantum random walk | $2^{0.292 n}$ | $2^{0.2570 n}$ | Chailloux and Loyer, 2021 |

The first row shows where the gain comes from. The list holds about $N = (4/3)^{n/2} = 2^{0.2075 n}$ vectors. The classical sieve does about $N$ searches of cost $N$ each, so the time is $N^2 = 2^{0.415 n}$. With SEARCH each search costs $O(\sqrt{N})$ queries, so the time is $N^{3/2} = 2^{0.311 n}$, which the authors round to $2^{0.312 n}$. The list size, and so the classical memory and the QRAM, stay at $2^{0.2075 n}$. A sieve with a provable bound gets the same kind of gain: Laarhoven, Mosca and van de Pol give $2^{1.799 n}$ against $2^{2.465 n}$ for the classical provable sieve.

The 2016 exponent $0.265$ (rounded) is the quantum constant that [core-SVP hardness](/core-svp-hardness/) uses to rate lattice schemes such as those based on [learning with errors](/learning-with-errors/).

## Properties

- **Still exponential.** Every quantum sieve takes $2^{\Theta(n)}$ time. No quantum algorithm is known that solves the shortest vector problem, or the approximate versions used in cryptography, in polynomial time. The hidden-subgroup methods behind [Shor's algorithm](/shor-algorithm/) do not apply in a known way, which is why lattice schemes are a main part of [post-quantum cryptography](/post-quantum-cryptography/).
- **A square root per search at most.** Grover search is optimal for [unstructured search](/unstructured-search/), so a quantum search in place of a scan gains at most a square root in that step. Larger gains need a change in the classical structure, such as the buckets of the filter-based sieves.
- **Randomized.** Even when the classical sieve is deterministic, the measurements make each run random, and two runs can build different lists.

## Variants and improvements

- **Search in hash buckets.** Sieves with [locality-sensitive hashing](/locality-sensitive-hashing/) or filters look for partners only among list vectors that share a bucket with $v$. The quantum versions use Grover search inside the bucket; this is a quantum form of [nearest-neighbor search](/nearest-neighbor-search/).
- **Quantum random walks.** Chailloux and Loyer find the close pairs inside a filter bucket with a [quantum walk search](/quantum-walk-search/) instead of repeated Grover searches. Their analysis also gives tradeoffs between time and quantum memory.
- **Sieving without QRAM.** Cho, Hhan, Kim, Lee and Shen prove a lower bound for quantum sieving with a QRAM of bounded size. Under their assumptions there is no quantum speedup without QRAM. They also give a circuit with no QRAM and better depth than the classical sieves, but it needs exponentially many qubits.
- **Use inside BKZ.** A sieve is the SVP solver in each block of [BKZ](/bkz-algorithm/); a quantum sieve lowers the cost of each block call in the same way.

## When to use it

Quantum sieving is a tool for security estimates, not a practical algorithm today. Designers of lattice schemes use its exponents as a conservative bound on a future quantum attack. Albrecht, Gheorghiu, Postlethwaite and Schanck build circuits for the search step and count their cost. They find only a small speedup in cryptographically relevant dimensions, and only under optimistic assumptions. For actual SVP computations, classical sieves on classical hardware remain the method of choice.

## Pitfalls

- **The QRAM cost.** The exponents in the table count a query to an exponentially large QRAM as one step. If each query costs time proportional to the memory size, most or all of the gain is lost.
- **Fixed iteration counts.** The number of partners in the list is not known, and a fixed number of Grover iterations can give a success probability near zero, as in the example. Use BBHT or quantum counting first.
- **Misses.** A search with a budget can end without a partner when partners exist. The sieve stays correct, but the list is no longer fully reduced and can hold long vectors. A larger budget makes misses rarer at a cost of more queries.
- **Reading the exponents.** The $o(n)$ terms are dropped, and the bounds rest on heuristics. For dimensions of a few hundred, the constant factors and the circuit depth decide the real cost.

## Implementations

## History

Nguyen and Vidick gave the first practical heuristic sieve in 2008, and Micciancio and Voulgaris gave the Gauss sieve in 2010. In 2013 Laarhoven, Mosca and van de Pol showed that Grover search speeds up the partner search of both sieves, and in 2014 and 2015 they applied the same idea to the hash-based sieves. Laarhoven's 2016 thesis gave the quantum version of the filter-based sieve of Becker, Ducas, Gama and Laarhoven, and its exponent became the standard quantum figure in the security analyses of the NIST lattice candidates. Chailloux and Loyer replaced Grover search by a quantum random walk in 2021. Since 2020, work has turned to the real cost of the quantum memory, with the circuit estimates of Albrecht, Gheorghiu, Postlethwaite and Schanck and the QRAM lower bound of Cho, Hhan, Kim, Lee and Shen in 2024.

## References
