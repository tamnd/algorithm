---
tag: 8WE1PE
kind: algorithm
slug: pollard-rho-discrete-logarithm
name: Pollard's rho algorithm for discrete logarithms
aliases:
- Pollard rho for DLP
- rho method for discrete logarithms
area: number-theory/discrete-logarithm
level: advanced
summary: Walks x = g^a h^b pseudorandomly until Floyd's method finds x_i = x_2i, then solves a linear congruence for log_g h. Heuristic O(n^(1/2)) group operations with O(1) memory.
solves: [discrete-logarithm-problem]
model: generic-group-model
complexity:
  vars:
    n: the order of g, usually a prime r after Pohlig-Hellman
    k: the number of binary digits of the modulus p, when the group is a subgroup of (Z/pZ)^*
  time:
    heuristic: O(n^(1/2))
  space:
    extra: O(1)
  bit_operations:
    heuristic: O(n^(1/2) k^2)
properties:
  deterministic: false
  recursive: false
prereqs: [discrete-logarithm-problem, floyd-cycle-detection, birthday-paradox, linear-congruence]
see_also: [pollard-rho, baby-step-giant-step, distinguished-points, parallel-collision-search, pollard-kangaroo, pohlig-hellman, brent-cycle-detection, shoup-generic-lower-bound]
sources:
  - paper: doi:10.1090/S0025-5718-1978-0491431-9
    title: John M. Pollard, Monte Carlo methods for index computation (mod p), Mathematics of Computation 32(143), 1978
    locator: pages 918 to 924 (the rho method for discrete logarithms, with the three-set walk)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 3, Section 3.6.3, Pollard's rho algorithm for logarithms (Algorithm 3.60, Example 3.61 with Table 3.2, Fact 3.62)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 14, Section 14.2 (Definition 14.2.1 of the rho walks, Lemma 14.2.3 on Floyd's method, Heuristic 14.2.10 and the theorem after it giving (3.093 + o(1)) r^(1/2), Section 14.2.3 on other cycle finding methods, Section 14.2.5 with Theorem 14.2.23 of Miller and Venkatesan)
  - paper: doi:10.1007/bfb0054891
    title: Edlyn Teske, Speeding up Pollard's rho method for computing discrete logarithms, ANTS-III, Lecture Notes in Computer Science 1423, 1998
    locator: pages 541 to 554 (r-adding walks, which behave closer to random maps than the original walk)
---

Pollard's rho algorithm for discrete logarithms solves $g^x = h$ in a cyclic group of order $n$ with about $\sqrt n$ group operations and only a constant number of stored elements. It iterates a pseudorandom map on elements of the form $g^a h^b$, keeping track of $a$ and $b$, until two of them coincide; a coincidence $g^a h^b = g^A h^B$ gives the linear congruence $(b - B) x \equiv A - a \pmod n$. [Floyd's cycle detection](/floyd-cycle-detection/) finds the coincidence without a table. The running time is heuristic: it assumes that the walk behaves like a random map, and the [birthday paradox](/birthday-paradox/) then gives about $\sqrt{\pi n / 2}$ steps before a repeat.

## In plain words

Imagine a large circle of numbered stones, and a rule that tells you, from the stone you stand on, which stone to jump to next. The rule mixes three kinds of jumps, and you keep a note of how many of each you have made. Because there are only so many stones, the path must eventually come back to a stone it has visited, and from then on it goes round in a loop.

Two walkers start together; one makes one jump per turn and the other two. The fast one enters the loop first and catches the slow one from behind. When they stand on the same stone, their two notes describe the same stone in two ways, and comparing the notes reveals the secret count. Nothing has to be remembered except the two walkers and their notes.

## The problem

**Input.** A prime $p$, an element $g$ of $(\mathbb{Z}/p\mathbb{Z})^*$ of known order $n$, and an element $h$. The method works the same way in any cyclic group with a unique representation of elements, such as an elliptic curve subgroup.

**Output.** The $x \in \{0, \dots, n - 1\}$ with $g^x = h$, or NONE if $h \notin \langle g \rangle$.

**Cost model.** The group is the cyclic subgroup $\langle g \rangle$ of order $n$, usually a prime $r$ because [Pohlig-Hellman](/pohlig-hellman/) has removed the small factors first. One group operation is a multiplication modulo $p$, which costs $O(k^2)$ bit operations for a $k$-bit $p$ with schoolbook arithmetic, and arithmetic on the exponents modulo $n$ is cheaper and is ignored. The algorithm is generic: it uses multiplication, equality and a function of the representation that picks the partition class. The bound in group operations is heuristic, under the assumption that the walk behaves like a random map on $\langle g \rangle$; Galbraith's analysis gives $(3.093 + o(1))\sqrt r$ with Floyd's method for prime order $r$. The lower bound $\Omega(\sqrt r)$ is proved in the [generic group model](/generic-group-model/).

## The algorithm

Fix a partition of $\langle g \rangle$ into three sets $S_1, S_2, S_3$ of about equal size. Pollard's original choice for $(\mathbb{Z}/p\mathbb{Z})^*$ is by the residue of the representative modulo $3$: $S_1 = \{x \equiv 1\}$, $S_2 = \{x \equiv 0\}$, $S_3 = \{x \equiv 2\}$. The map $f$ multiplies by $h$ on $S_1$, squares on $S_2$ and multiplies by $g$ on $S_3$. Exponents are taken modulo $n$.

```pseudo id=main
POLLARD-RHO-LOG(g, h, n)               ▷ ⟨g⟩ cyclic of order n; returns x with g^x = h, or NONE
L1  if h^n ≠ 1 then return NONE         ▷ in a cyclic group, h ∈ ⟨g⟩ exactly when h^n = 1
L2  if h = 1 then return 0
L3  (a₀, b₀, S) ← (0, 0, S₀)            ▷ Pollard's start x₀ = 1 and partition by x mod 3
L4  loop
L5      x ← g^a₀ · h^b₀ ; (a, b) ← (a₀, b₀)
L6      (X, A, B) ← (x, a, b)
L7      repeat                          ▷ Floyd: x = x_i and X = x_2i
L8          (x, a, b) ← STEP(x, a, b)
L9          (X, A, B) ← STEP(STEP(X, A, B))
L10     until x = X
L11     s ← (b − B) mod n ; d ← gcd(s, n)
L12     if s ≠ 0 and d ≤ ⌊√n⌋ + 1 then
L13         y ← ((A − a)/d) · (s/d)^(−1) mod (n/d)
L14         for t ← 0 to d − 1 do       ▷ the d solutions of s x ≡ A − a (mod n)
L15             if g^(y + t n/d) = h then return y + t n/d
L16     (a₀, b₀, S) ← random a₀, b₀ in Z/nZ and a fresh random partition
STEP(x, a, b)                           ▷ keeps x = g^a h^b
L17 if x ∈ S₁ then return (x · h, a, b + 1)
L18 if x ∈ S₂ then return (x², 2a, 2b)
L19 return (x · g, a + 1, b)            ▷ x ∈ S₃
```

Line L1 decides membership: $\langle g \rangle$ is the unique subgroup of order $n$ of the cyclic group $(\mathbb{Z}/p\mathbb{Z})^*$, so it consists of the elements whose order divides $n$. Line L2 removes the trivial target. Lines L5 to L10 run one attempt: the tortoise $(x, a, b)$ moves one step per round and the hare $(X, A, B)$ two, and lines L17 to L19 keep the invariant $x = g^a h^b$ for both. Line L10 stops at the first $i$ with $x_i = x_{2i}$, which exists by [Floyd's argument](/floyd-cycle-detection/). Then $g^a h^b = g^A h^B$, so with $h = g^x$, $(b - B) x \equiv A - a \pmod n$. Line L11 computes the coefficient $s$ and $d = \gcd(s, n)$. If $s \ne 0$ the congruence has exactly $d$ solutions modulo $n$, which lines L13 to L15 enumerate as in a [linear congruence](/linear-congruence/); for prime $n$, $d = 1$ and line L13 alone gives the answer. If $s = 0$ the collision carries no information, and if $d$ is large the enumeration would be too expensive; line L16 then starts again with a random start $g^{a_0} h^{b_0}$ and a new partition.

## Example

This is HAC's Example 3.61: $p = 383$, $g = 2$ of prime order $n = 191$, and $h = 228$, with the partition by $x \bmod 3$ and $x_0 = 1$. The table lists $(x_i, a_i, b_i)$ and $(x_{2i}, a_{2i}, b_{2i})$ after round $i$.

| $i$ | $x_i$ | $a_i$ | $b_i$ | $x_{2i}$ | $a_{2i}$ | $b_{2i}$ |
|---|---|---|---|---|---|---|
| 1 | 228 | 0 | 1 | 279 | 0 | 2 |
| 2 | 279 | 0 | 2 | 184 | 1 | 4 |
| 3 | 92 | 0 | 4 | 14 | 1 | 6 |
| 4 | 184 | 1 | 4 | 256 | 2 | 7 |
| 5 | 205 | 1 | 5 | 304 | 3 | 8 |
| 6 | 14 | 1 | 6 | 121 | 6 | 18 |
| 7 | 28 | 2 | 6 | 144 | 12 | 38 |
| 8 | 256 | 2 | 7 | 235 | 48 | 152 |
| 9 | 152 | 2 | 8 | 72 | 48 | 154 |
| 10 | 304 | 3 | 8 | 14 | 96 | 118 |
| 11 | 372 | 3 | 9 | 256 | 97 | 119 |
| 12 | 121 | 6 | 18 | 304 | 98 | 120 |
| 13 | 12 | 6 | 19 | 121 | 5 | 51 |
| 14 | 144 | 12 | 38 | 144 | 10 | 104 |

In round $14$, $x_{14} = x_{28} = 144$. Line L11 gives $s = 38 - 104 \equiv 125 \pmod{191}$ and $d = 1$, and line L13 gives $y = (10 - 12) \cdot 125^{-1} \equiv -2 \cdot 136 \equiv 110 \pmod{191}$. Indeed $2^{110} \equiv 228 \pmod{383}$, so the answer is $110$, found with $42$ group operations in the walk. With $p = 23$, $g = 2$ of order $11$ and $h = 5$, line L1 finds $5^{11} \equiv 22 \ne 1$ and returns NONE.

## Correctness

The invariant $x = g^a h^b$ holds at line L5 and is kept by each of lines L17 to L19, for the tortoise and for the hare. The sequence $x_0, x_1, \dots$ with $x_{i+1} = f(x_i)$ lives in a finite set, so it is eventually periodic, and Floyd's lemma gives an $i \ge 1$ with $x_i = x_{2i}$, so each attempt ends. At that point $g^{a - A} = h^{B - b}$; if $h = g^{x^*}$, then $s x^* \equiv A - a \pmod n$, and when $s \ne 0$ the solutions of this congruence are exactly $y + t n/d$ for $0 \le t < d$, one of which is $x^*$. Line L15 checks each candidate, so any returned value is correct, and if $h \in \langle g \rangle$ the attempt with $s \ne 0$ and small $d$ returns $x^*$. If $h \notin \langle g \rangle$, line L1 returns NONE, since $h^n = 1$ would put $h$ in the unique subgroup of order $n$. Each attempt after the first uses fresh random choices, so the algorithm stops with probability $1$; the number of attempts is not bounded in the worst case. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Group operations, heuristic.** If $f$ behaves like a random map on a set of size $r$, the tail and the cycle of the rho each have expected length about $\sqrt{\pi r / 8}$, Floyd's method stops after the epact, which has expected value about $0.823 \sqrt{\pi r / 2}$, and each round costs three group operations. The total is $(3.093 + o(1))\sqrt r$ group operations for prime order $r$ (Galbraith, Section 14.2.2). The probability that $s = 0$ is about $1/r$, so the expected number of attempts is $1 + o(1)$ for prime $r$.
- **Proved results.** For the original three-set walk with a uniformly random partition, Miller and Venkatesan proved a collision within $O_\varepsilon(\sqrt r \log^3 r)$ operations with probability $1 - \varepsilon$, and Kim, Montenegro, Peres and Tetali improved this to $O_\varepsilon(\sqrt r)$ (Galbraith, Theorem 14.2.23 and the text after it). These results average over all partitions, which no compact selection function realizes, so no running time is proved for an implementable rho.
- **Space.** Six residues and two counters: $O(1)$ group elements, against $\Theta(\sqrt n)$ for [baby-step giant-step](/baby-step-giant-step/).
- **Bit operations.** $O(\sqrt n \, k^2)$ heuristic in a subgroup of $(\mathbb{Z}/p\mathbb{Z})^*$ with $k$-bit $p$, plus $O(\log n)$ multiplications for line L1 and $O(k^2)$ for the extended Euclidean algorithm at line L13.
- **Composite order.** The walk works modulo $n$, and line L12 handles a common factor $d$; but running rho in the whole group costs $\sqrt n$ rather than $\sqrt r$ for the largest prime $r \mid n$, so Pohlig-Hellman should come first.

## Properties

- **Randomized, Las Vegas.** Every returned value is checked, so the answer is always right; only the running time is random. The first attempt in the version above is deterministic, as in Pollard's paper.
- **Generic.** Only the group law, equality and a deterministic function of a unique representation are used, so it applies to elliptic curves, Jacobians and class groups.
- **Constant memory.** The defining advantage over baby-step giant-step, whose memory limits it to orders around $2^{50}$.
- **Not parallel as stated.** Floyd's method follows one walk. Running $m$ independent copies gives only a $\sqrt m$ speedup; [distinguished points](/distinguished-points/) give the linear speedup of [parallel collision search](/parallel-collision-search/).

## Variants and improvements

- **Better cycle finding.** [Brent's method](/brent-cycle-detection/) uses fewer group operations than Floyd's with the same memory. With distinguished points, a single walk needs about $(1 + o(1))\sqrt{\pi r / 2} \approx 1.253 \sqrt r$ operations plus a small overhead (Galbraith, Section 14.2.4).
- **More partitions.** Teske's $r$-adding walk multiplies by one of $r \approx 20$ random elements $g^{u_j} h^{v_j}$ and avoids squarings. It behaves closer to a random map, and Teske observed that Pollard's three-set walk is slower than a random map. Heuristic arguments of Brent and Pollard and of others put the expected length for $n_S$ classes above the random value by a factor that depends on $n_S / (n_S - 1)$ and tends to $1$ as $n_S$ grows (Galbraith, Section 14.2.5).
- **Equivalence classes.** On elliptic curves, walking on classes $\{P, -P\}$ halves the search space and saves a factor $\sqrt 2$; Frobenius classes on Koblitz curves save more. The walk must then avoid short "fruitless" cycles (Galbraith, Section 14.4).
- **Parallel and distributed.** [Parallel collision search](/parallel-collision-search/) runs many walks that report [distinguished points](/distinguished-points/) to a server, with linear speedup.
- **Interval problems.** The [kangaroo method](/pollard-kangaroo/), also from Pollard's 1978 paper, adapts the idea to an exponent in a known interval.

## When to use it

Use rho for the discrete logarithm in a group of large prime order where index calculus does not apply, most of all elliptic curves, once [Pohlig-Hellman](/pohlig-hellman/) has reduced to prime order. For orders below about $2^{40}$, [baby-step giant-step](/baby-step-giant-step/) is simpler and deterministic. For record computations use the distinguished point version on many machines. For $(\mathbb{Z}/p\mathbb{Z})^*$ with large $p$ and a large subgroup, [index calculus](/index-calculus/) and the [number field sieve](/number-field-sieve-discrete-logarithm/) are much faster.

## Pitfalls

- **No membership test.** Without line L1, a target outside $\langle g \rangle$ makes every collision give a candidate that line L15 rejects, and the loop of line L4 never ends. Line L1 must come first; it is valid because the group is cyclic, and for a non-cyclic ambient group the order test alone does not decide membership.
- **Dividing by a zero coefficient.** If line L13 inverts $s$ without the test $s \ne 0$ of line L12, the method crashes or returns garbage. For prime $n$ this happens with probability about $1/n$, but in small groups it is common.
- **Ignoring the gcd.** For composite $n$, computing $s^{-1} \bmod n$ fails when $d > 1$. The right lines are L13 to L15: divide by $d$, solve modulo $n/d$, and test the $d$ lifts.
- **Exponents not reduced.** Line L18 doubles $a$ and $b$; without reduction modulo $n$ they grow to $\Theta(\sqrt n)$ bits. Every update in lines L17 to L19 is modulo $n$.
- **A fixed point at the start.** With the partition by $x \bmod 3$, the identity $1$ lies in $S_1$ and the first step is $1 \cdot h$. If line L3 put $1$ in the squaring class, the walk would stay at $1$, the first collision would have $s = 0$, and every restart from $1$ with that partition would fail the same way. Line L3 must pair the start $x_0 = 1$ with a partition in which $1$ is not squared.
- **Same walk on restart.** Restarting with the same partition at line L16 and the same start reproduces the same failure. Change the partition, the start, or both.
- **Non-unique representations.** The class of an element must be computed from a unique form, such as affine coordinates on an elliptic curve; otherwise equal elements take different steps.

## Implementations

## History

John Pollard introduced the rho method for factoring in 1975 and, in his 1978 paper "Monte Carlo methods for index computation (mod p)", gave both the rho method and the kangaroo (lambda) method for discrete logarithms. The Handbook of Applied Cryptography presents the three-set walk with Floyd's cycle finding as Algorithm 3.60. Teske studied the $r$-adding walks in 1998, and van Oorschot and Wiener's parallel collision search of 1999 made distinguished points the standard way to run rho on many machines. All the records for elliptic curve discrete logarithms have been set with variants of this method.

## References
