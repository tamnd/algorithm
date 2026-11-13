---
tag: QEG4BF
kind: algorithm
slug: brassard-hoyer-tapp-collision
name: Brassard-Høyer-Tapp collision algorithm
aliases:
- BHT collision algorithm
area: quantum/quantum-search
level: advanced
summary: Finds two inputs with the same value of an r-to-one function on N points with O((N/r)^(1/3)) expected queries, by Grover search against a table of (N/r)^(1/3) values.
solves: [collision-finding]
model: quantum-query-model
complexity:
  vars: {N: the size of the domain, r: the number of inputs per value, k: the size of the table}
  queries: {expected: O(k + (N/(r k))^(1/2)), best: O((N/r)^(1/3))}
  space: {extra: O(k)}
properties: {deterministic: false, exact: false, las_vegas: true, oracle: bit}
history:
  year: 1997
  people: [Gilles Brassard, Peter Høyer, Alain Tapp]
  note: Posted as arXiv:quant-ph/9705002 in 1997 and published at LATIN 1998. Aaronson and Shi proved the matching lower bound in 2002 to 2004.
prereqs: [grover-search, birthday-paradox, quantum-oracle, quantum-query-model]
see_also: [collision-finding, birthday-attack, amplitude-amplification, bbht-search, ambainis-element-distinctness, element-distinctness, quantum-random-access-memory, polynomial-method]
sources:
  - paper: doi:10.1007/BFb0054319
    title: "Gilles Brassard, Peter Høyer and Alain Tapp, Quantum cryptanalysis of hash and claw-free functions, Proceedings of LATIN 1998, LNCS 1380, pages 163-169"
    locator: the conference version of arXiv:quant-ph/9705002
  - paper: arxiv:quant-ph/9705002
    title: "Gilles Brassard, Peter Høyer and Alain Tapp, Quantum algorithm for the collision problem, arXiv:quant-ph/9705002, 1997"
    locator: Section 2, algorithm Collision(F, k), Theorem 1 (two-to-one), Theorem 2 (r-to-one), Corollary 3 (the space-time tradeoff), Theorems 4 and 5 (claws), Section 3 (discussion of quantum memory)
  - paper: doi:10.1145/1008731.1008735
    title: "Scott Aaronson and Yaoyun Shi, Quantum lower bounds for the collision and the element distinctness problems, Journal of the ACM 51(4), 2004, pages 595-605"
    locator: the main theorem (Omega((N/r)^(1/3)) queries for an r-to-one function, and Omega(N^(2/3)) for element distinctness)
  - paper: arxiv:quant-ph/9605034
    title: "Michel Boyer, Gilles Brassard, Peter Høyer and Alain Tapp, Tight bounds on quantum searching, Fortschritte der Physik 46(4-5), 1998, pages 493-505"
    locator: Sections 2 to 4 (Grover search with t known solutions and with t unknown, used in step 4)
---

The Brassard-Høyer-Tapp algorithm finds a *collision* of a function $F : X \to Y$, two inputs $x_0 \ne x_1$ with $F(x_0) = F(x_1)$, when $F$ is $r$-to-one: each value has exactly $r$ preimages. It reads $F$ on a set $K$ of $k$ inputs, and then runs [Grover search](/grover-search/) for an input outside $K$ whose value is already in the table. With $|X| = N$ and $k \approx (N/r)^{1/3}$, it makes $O((N/r)^{1/3})$ queries in expectation and always returns a correct collision. Classical algorithms need $\Theta(\sqrt{N/r})$ queries, by the [birthday paradox](/birthday-paradox/). This page is the quantum query algorithm; its use against hash functions, and why its real cost is debated, are on the page [collision finding](/collision-finding/).

## In plain words

A function sends pairs of inputs to the same output, and you want one such pair. A normal method tries random inputs and waits for two equal outputs. With a million inputs this takes about a thousand tries.

The quantum method first tries about a hundred inputs and writes their outputs in a sorted list. Each of these hundred inputs has a partner somewhere among the other inputs. So now a hundred inputs are "good": their output is in the list. A quantum search finds a good input among a million with about a hundred questions, because there are a hundred good ones. The total is about two hundred questions instead of a thousand. A larger list makes the search shorter but costs more to build, and the best balance is at the cube root of the number of inputs.

## The problem

The input is a function $F : X \to Y$ with $|X| = N$, given by the bit oracle $O_F |x\rangle|y\rangle = |x\rangle|y \oplus F(x)\rangle$. $F$ is promised to be $r$-to-one for a known $r \ge 2$, so $r$ divides $N$ and $F$ has $N/r$ values. The output is a collision. The cost is the number of evaluations of $F$ in the [quantum query model](/quantum-query-model/), as an expected value, since the algorithm is Las Vegas: it repeats until it finds a collision, and it checks each candidate. Without the promise this is the general [collision finding](/collision-finding/) problem. When $F$ is one-to-one except for one pair, it is [element distinctness](/element-distinctness/), which is harder; see Pitfalls.

## The algorithm

Let $H : X \to \{0, 1\}$ be $H(x) = 1$ if $x \notin K$ and $F(x) = F(x_0)$ for some $x_0 \in K$. A query of $H$ uses one query of $F$ and a search of the sorted table.

```pseudo id=main
BHT-COLLISION(O_F, N, r, k)          ▷ F is r-to-one on N points; k is the table size
L1  pick a set K of k inputs
L2  read F(x) for each x in K        ▷ k queries; the table L holds the pairs (F(x), x)
L3  sort L by value
L4  if two pairs in L have the same value
L5      return their inputs
L6  t ← (r - 1) k                    ▷ the number of x with H(x) = 1
L7  run Grover search for H with t solutions   ▷ floor(pi / (4 theta)) queries, sin theta = sqrt(t / N)
L8  measure; let x1 be the result
L9  if H(x1) = 1 (one more query)    ▷ otherwise go back to L7
L10     find (F(x1), x0) in L and return x0, x1
```

Brassard, Høyer and Tapp take $k = \sqrt[3]{N}$ for two-to-one functions (Theorem 1) and $k = \sqrt[3]{N/r}$ for $r$-to-one functions (Theorem 2). For a general function with $|X| \ge r|Y|$ they pick $K$ at random and use the version of Grover search for an unknown number of solutions, [BBHT search](/bbht-search/), at line L7.

## Example

Take $N = 64$, $r = 2$ and $F(x) = x \bmod 32$, with $K = \{5, 17, 40\}$, so $k = 3$, close to $\sqrt[3]{32} \approx 3.17$.

1. Lines L2 and L3: the sorted table is $(5, 5), (8, 40), (17, 17)$, three queries. All values differ, so there is no collision inside $K$.
2. Line L6: the inputs outside $K$ with a value in the table are $37$ (value 5), $8$ (value 8) and $49$ (value 17), so $t = 3 = (r - 1)k$.
3. Line L7: $\sin\theta = \sqrt{3/64}$, so $\theta \approx 0.2183$ and the number of iterations is $\lfloor \pi/(4\theta) \rfloor = 3$.

The simulator (6 qubits, qubit 0 the least significant bit of $x$, exact amplitudes) gives the probability that the measurement hits one of $\{8, 37, 49\}$:

| iterations $j$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| simulated | 0.046875 | 0.370789 | 0.787068 | 0.998139 | 0.853118 |
| $\sin^2((2j+1)\theta)$ | 0.046875 | 0.370789 | 0.787068 | 0.998139 | 0.853118 |

With the random generator `random.Random(1)` the run measures $x_1 = 8$, checks $H(8) = 1$, and returns the collision $(40, 8)$, since $F(40) = F(8) = 8$. It used $3 + 3 + 1 = 7$ queries. A classical birthday search on 64 inputs needs about $\sqrt{64} = 8$ queries for a constant success probability; the gain grows with $N$.

The query count $k + \lfloor \pi/(4\theta) \rfloor + 1$ with $k = \mathrm{round}(\sqrt[3]{N/2})$ and $r = 2$, from the closed form, against $\sqrt{N}$:

| $N$ | $2^{10}$ | $2^{20}$ | $2^{30}$ | $2^{40}$ |
|---|---|---|---|---|
| $k$ | 8 | 81 | 813 | 8192 |
| Grover iterations | 8 | 89 | 902 | 9099 |
| total queries, one round | 17 | 171 | 1716 | 17292 |
| $\sqrt{N}$ | 32 | 1024 | 32768 | 1048576 |

The tests compare the simulated success probability with $\sin^2((2j+1)\theta)$ to within $10^{-9}$ for random 2-to-one and 4-to-one functions on 64 to 256 points (seed 11), check every returned pair against brute force, and check that the mean query count over 40 runs (seed 5, $N = 256$) is at most $k + (\lfloor \pi/(4\theta) \rfloor + 1)/p$, where $p$ is the success probability of one round.

## Correctness

Each $x_0 \in K$ has exactly $r - 1$ partners with the same value, since $F$ is $r$-to-one. If line L4 finds no collision, the values in $K$ are distinct, so the partners of different $x_0$ are different, and none of them is in $K$. So exactly $t = (r-1)k$ inputs have $H(x) = 1$, and each of them, with its partner $x_0$, is a collision. Grover search with $t$ known solutions measures a solution with probability $\sin^2((2j+1)\theta) \ge 1 - t/N$ for $j = \lfloor \pi/(4\theta) \rfloor$. Line L9 checks the candidate, so the output is always a collision. The full proof, with the expected count, is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Queries.** Lines L2 and L4 make $k$ queries. One round of lines L7 to L9 makes $\lfloor \pi/(4\theta) \rfloor + 1 \le \frac{\pi}{4}\sqrt{N/((r-1)k)} + 1$ queries and succeeds with probability at least $1 - t/N$. So the expected number of queries is $k + O(\sqrt{N/(rk)})$ (Theorem 2). The two terms balance at $k = \Theta((N/r)^{1/3})$, which gives $O((N/r)^{1/3})$.
- **Lower bound.** Aaronson and Shi proved that every bounded-error quantum algorithm needs $\Omega((N/r)^{1/3})$ queries for an $r$-to-one function. Their first proof needed a range of size at least $3N/2$; Kutin and Ambainis removed this condition in 2005. So the algorithm is optimal in queries up to a constant factor.
- **Classical.** A randomized classical algorithm needs $\Theta(\sqrt{N/r})$ queries, by the birthday bound. The gap is a power $2/3$ in the exponent, in query counts.
- **Space.** The table holds $k$ pairs, so the space is $\Theta(k)$ entries (Theorem 1). Corollary 3 states the tradeoff: with space $S$ and $T$ expected evaluations, $S T^2 \ge |F(X)|$ suffices, for every $1 \le S \le T$.
- **Time.** Each query of $H$ looks up $F(x)$ in the sorted table in superposition. This is $O(\log k)$ comparisons if the table can be read in superposition, which is the model of a [quantum random access memory](/quantum-random-access-memory/). Without it, each lookup costs $\Theta(k)$ gates, and the time grows to about $k \sqrt{N/(rk)}$, which is $\Theta(\sqrt{N/r})$ at best.

## Properties

- Las Vegas: the output is always correct, and only the number of queries is random.
- The table is built classically. Only its lookups happen in superposition.
- With $t$ known, the number of Grover iterations is fixed in advance.
- The algorithm is a combination of the classical birthday method (a table of size $\sqrt{N}$) and the plain quantum method (Grover search for the partner of one fixed $x_0$, $O(\sqrt{N})$ queries). The paper describes it so.

## Variants and improvements

- **Claws.** For two one-to-one functions $F : X \to Z$ and $G : Y \to Z$ with $|X| = |Y| = |Z| = N$, a table of $k$ values of $F$ and a Grover search over $G$ find a claw $F(x) = G(y)$ with $k$ evaluations of $F$ and $O(\sqrt{N/k})$ of $G$, so $O(N^{1/3})$ in total with $k = \sqrt[3]{N}$ (Theorem 4). Theorem 5 is the $r$-to-one version.
- **General functions.** For $|X| \ge r|Y|$ without the exact promise, pick $K$ at random and use BBHT search for the unknown number of solutions.
- **Element distinctness.** With only one collision, the method gives $O(N^{3/4})$ queries at best; Buhrman, Dürr, Heiligman, Høyer, Magniez, Santha and de Wolf gave an $O(N^{3/4})$ algorithm of this kind, and [Ambainis's quantum walk](/ambainis-element-distinctness/) reaches the optimal $O(N^{2/3})$.
- **Many collisions and random functions.** For a random function, later work counts the queries to find many collisions; this is described on the page [collision finding](/collision-finding/), with Zhandry's lower bound for random functions.

## When to use it

- When $F$ is many-to-one and you count queries to $F$, for example as a black box in a query-complexity argument.
- When a quantum random access memory of size $(N/r)^{1/3}$ is available. Without it, the gain in time is lost, and a classical parallel collision search can be cheaper. The page [collision finding](/collision-finding/) gives this argument for hash functions.
- Not for one-to-one functions with a single collision. Use the [element distinctness](/ambainis-element-distinctness/) algorithm.

## Pitfalls

- **$O(N^{1/3})$ is for two-to-one functions.** For an $r$-to-one function the bound is $O((N/r)^{1/3})$, which is smaller for large $r$. A bound written as "$O(N^{1/3})$ for $r$-to-one functions" is not wrong as an upper bound, but it is not the bound of the paper.
- **One evaluation per query of $H$.** The paper counts one evaluation of $F$ for each evaluation of $H$. A reversible circuit that computes $F(x)$, compares it with the table and uncomputes $F(x)$ makes two calls of the bit oracle. This changes only the constant.
- **The number of solutions.** $t = (r-1)k$ only when $K$ has no internal collision and $F$ is exactly $r$-to-one. For other functions, $t$ is unknown and fixed iterations can overshoot; use BBHT search.
- **Queries are not time.** The query bound assumes free superposed lookups in a table of $k$ entries. Quantum memory of this size is not a small cost.
- **Element distinctness is harder.** With one collision in an otherwise one-to-one function, $t \le 1$ and the method gives only $O(N^{3/4})$, against the lower bound $\Omega(N^{2/3})$ of Aaronson and Shi.

## Implementations

## History

Brassard, Høyer and Tapp posted the algorithm in May 1997 as "Quantum algorithm for the collision problem", and published it at LATIN 1998 under the title "Quantum cryptanalysis of hash and claw-free functions". Whether $O(N^{1/3})$ was optimal stayed open until Aaronson proved $\Omega(N^{1/5})$ at STOC 2002 and Shi improved it to $\Omega(N^{1/3})$ for large ranges the same year. The two results were joined in the Journal of the ACM in 2004.

## References
