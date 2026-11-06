---
tag: KW87TP
kind: algorithm
slug: baby-step-giant-step
name: Baby-step giant-step
aliases:
- Shanks' baby-step giant-step
- Shanks' algorithm
- BSGS
area: number-theory/discrete-logarithm
level: core
summary: Writes x = i m + j with m about n^(1/2), stores the baby steps g^j in a hash table and walks the giant steps h g^(-i m) until one hits. Deterministic, O(n^(1/2)) group operations and memory.
solves: [discrete-logarithm-problem]
model: generic-group-model
complexity:
  vars:
    n: an upper bound on the order of g
    k: the number of binary digits of the modulus p, when the group is (Z/pZ)^*
  time:
    worst: O(n^(1/2))
    average: O(n^(1/2))
  space:
    extra: O(n^(1/2))
  bit_operations:
    worst: O(n^(1/2) k^2)
properties:
  deterministic: true
  recursive: false
prereqs: [discrete-logarithm-problem, hash-table, modular-exponentiation]
see_also: [pohlig-hellman, pollard-rho-discrete-logarithm, pollard-kangaroo, interval-discrete-logarithm-problem, meet-in-the-middle-attack, shoup-generic-lower-bound, order-finding, generic-group-model]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 3, Section 3.6.2, Baby-step giant-step algorithm (Algorithm 3.56, Fact 3.57 and Example 3.58)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 13, Section 13.3, Baby-step giant-step (BSGS) method (Algorithm 14, Theorem 13.3.1, Remark 13.3.2, Exercises 13.3.3 to 13.3.12)
  - paper: "Daniel Shanks, Class number, a theory of factorization, and genera, Proceedings of Symposia in Pure Mathematics 20, American Mathematical Society, 1971"
    locator: pages 415 to 440 (the baby-step giant-step idea, introduced for class groups of quadratic forms)
  - paper: doi:10.1007/s001450010010
    title: J. M. Pollard, Kangaroos, Monopoly and discrete logarithms, Journal of Cryptology 13(4), 2000
    locator: pages 437 to 447 (the interleaved form of baby-step giant-step, with average cost (4/3) n^(1/2))
---

Baby-step giant-step is a deterministic algorithm for the [discrete logarithm problem](/discrete-logarithm-problem/): given $g$ and $h$ in a group and a bound $n$ on the order of $g$, it finds the least $x \ge 0$ with $g^x = h$, or reports that there is none. It splits the unknown exponent as $x = i m + j$ with $m = \lceil \sqrt n \rceil$, stores the $m$ "baby steps" $g^j$ in a [hash table](/hash-table/), and computes the "giant steps" $h g^{-im}$ until one of them is in the table. It uses $O(\sqrt n)$ group operations and stores $O(\sqrt n)$ elements, and it works in any group, which makes it optimal up to a constant factor among [generic algorithms](/generic-group-model/). It is usually credited to Daniel Shanks.

## In plain words

You want to know how many steps lead from the start of a cycle to a given element. Instead of walking one step at a time, take a hundred small steps from the start and write down where each one lands. Then, starting from the given element, walk backwards in jumps of a hundred small steps each. After each jump, look the position up in your notes.

As soon as a jump lands on a spot you wrote down, you know the count: so many big jumps back plus so many small steps forward. With a hundred small steps and a hundred big jumps you can reach any count below ten thousand, so ten thousand positions are covered by only two hundred moves. The price is the notebook of a hundred entries. If no jump ever lands in the notebook, the element is not on the cycle.

## The problem

**Input.** A group $G$ in which we can multiply, invert and test equality, elements $g, h \in G$, and an integer $n \ge 1$ with $\operatorname{ord}(g) \le n$. For $G = (\mathbb{Z}/p\mathbb{Z})^*$ with $p$ prime one can take $n = p - 1$; when the order of $g$ is known, $n = \operatorname{ord}(g)$ is best.

**Output.** The least $x \ge 0$ with $g^x = h$, which then satisfies $x < \operatorname{ord}(g)$, or NONE if $h \notin \langle g \rangle$.

**Cost model.** The algorithm uses only multiplication, inversion, equality and hashing of group elements, so it is a generic algorithm. Costs are counted in group operations and in stored elements. In $(\mathbb{Z}/p\mathbb{Z})^*$ with $p$ of $k$ binary digits, one group operation is a multiplication modulo $p$, $O(k^2)$ bit operations with schoolbook arithmetic, and a hash table operation on a $k$-bit key costs $O(k)$ bit operations in expectation. For an elliptic curve the same counts hold with one point addition per group operation, provided points are stored in a unique (affine or normalized) form so that equal points hash alike.

## The algorithm

```pseudo id=main
BABY-STEP-GIANT-STEP(g, h, n)        ▷ ord(g) ≤ n; returns least x ≥ 0 with g^x = h, or NONE
L1  m ← ⌈√n⌉
L2  T ← empty hash table             ▷ maps a group element to an exponent j < m
L3  e ← 1
L4  for j ← 0 to m − 1 do            ▷ baby steps: e = g^j
L5      if e ∉ T then T[e] ← j       ▷ keep the least j for each element
L6      e ← e · g
L7  u ← g^(−m)                       ▷ by square and multiply, O(log m) operations
L8  γ ← h
L9  for i ← 0 to m − 1 do            ▷ giant steps: γ = h · g^(−i m)
L10     if γ ∈ T then return i · m + T[γ]
L11     γ ← γ · u
L12 return NONE
```

Lines L3 to L6 compute $g^0, g^1, \dots, g^{m-1}$ and store each with its exponent. If $g$ has order less than $m$, the same element appears more than once, and line L5 keeps its first, smallest exponent. Line L7 computes $u = g^{-m}$ once, by [square and multiply](/binary-exponentiation/) applied to $g^{-1}$. Lines L8 to L11 compute $\gamma_i = h g^{-im}$ for $i = 0, 1, \dots, m-1$, and line L10 tests each against the table. A hit $\gamma_i = g^j$ means $h = g^{im + j}$.

Since $m^2 \ge n \ge \operatorname{ord}(g)$, every exponent $x < \operatorname{ord}(g)$ can be written as $x = i m + j$ with $0 \le i, j < m$, so every solution is found. Because the table keeps the least $j$ and the giant steps run in increasing $i$, the first hit gives the least solution.

## Example

Let $p = 23$, $g = 5$ (a [primitive root](/primitive-root/)), $h = 14$ and $n = 22$. Then $m = \lceil \sqrt{22} \rceil = 5$. The baby steps are

| $j$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $5^j \bmod 23$ | 1 | 5 | 2 | 10 | 4 |

and $u = 5^{-5} \bmod 23 = 15$, since $5^5 \equiv 20$ and $20 \cdot 15 = 300 = 13 \cdot 23 + 1$. The giant steps are

| $i$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $\gamma = 14 \cdot 15^i \bmod 23$ | 14 | 3 | 22 | 8 | 5 |
| in $T$? | no | no | no | no | yes, $j = 1$ |

so the algorithm returns $x = 4 \cdot 5 + 1 = 21$, and indeed $5^{21} \equiv 14 \pmod{23}$. With $h = 8$ the second giant step $8 \cdot 15 \equiv 5$ is already in the table and the answer is $1 \cdot 5 + 1 = 6$.

Now take $g = 2$, of order $11$, and $h = 5$, still with the bound $n = 22$. The baby steps are $1, 2, 4, 8, 16$, $u = 2^{-5} \bmod 23 = 18$, and the giant steps are $5, 21, 10, 19, 20$. None of them is in the table, so the algorithm returns NONE: $5$ is not a power of $2$ modulo $23$.

## Correctness

Each pair $(e, j)$ stored in $T$ satisfies $e = g^j$ with $0 \le j < m$, and $j$ is the least such exponent for $e$. Before the test at line L10 in round $i$, $\gamma = h g^{-im}$. So a hit returns $x = im + j$ with $g^x = h$, and NONE is returned only if no $\gamma_i$ is a baby step. If $x^*$ is the least solution, then $x^* < \operatorname{ord}(g) \le n \le m^2$, so $x^* = i^* m + j^*$ with $0 \le i^*, j^* < m$, and $\gamma_{i^*} = g^{j^*}$ is in $T$: a solution is never missed. A hit at round $i < i^*$ would give a solution $im + j < i^* m \le x^*$, and the hit at $i^*$ returns a solution $i^* m + T[\gamma] \le x^*$; so the answer is $x^*$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Group operations.** Lines L4 to L6 take $m$ multiplications. Line L7 takes one inversion and at most $2 \lceil \lg m \rceil$ multiplications. Lines L9 to L11 take at most $m$ multiplications. The total is at most $2m + O(\log m) = 2\sqrt n + O(\log n)$ in the worst case, proved. If $x$ is uniform in $\{0, \dots, n-1\}$, the expected number of giant steps is about $m/2$, so about $1.5 \sqrt n$ operations on average (Galbraith, Exercise 13.3.3).
- **Table operations.** $m$ insertions and at most $m$ lookups, each $O(1)$ expected time with a hash table, or $O(\log m)$ comparisons with a sorted array or a balanced tree, which makes the method fully deterministic at a cost of $O(\sqrt n \log n)$ comparisons.
- **Space.** $m$ group elements and exponents, $O(\sqrt n \log n)$ bits for $(\mathbb{Z}/p\mathbb{Z})^*$ with $p \approx n$. This is the binding constraint in practice.
- **Bit operations.** In $(\mathbb{Z}/p\mathbb{Z})^*$ with $k$-bit $p$: $O(\sqrt n \, k^2)$ with schoolbook multiplication, the bound of Galbraith's Theorem 13.3.1.
- **Optimality.** For a group of prime order $q$, [Shoup's theorem](/shoup-generic-lower-bound/) shows that every generic algorithm needs $\Omega(\sqrt q)$ group operations to succeed with constant probability. Baby-step giant-step meets this bound up to a constant factor, deterministically. It is not optimal in groups where the encoding helps, such as $\mathbb{F}_p^*$, where [index calculus](/index-calculus/) is subexponential.

## Properties

- **Deterministic and exact.** No randomness and no heuristic. It always finds the least solution, and NONE is a proof of non-membership given that $n \ge \operatorname{ord}(g)$.
- **Generic.** Only the group law, equality and a hash of a unique representation are used. It works in $(\mathbb{Z}/p\mathbb{Z})^*$, on elliptic curves, in class groups and in any other group.
- **Time-memory tradeoff.** With $m$ baby steps and $\lceil n/m \rceil$ giant steps, the time is $m + n/m$ and the memory $m$. Any $m$ between $1$ (exhaustive search) and $n$ (a full table) is valid.
- **Reusable table.** The baby steps depend only on $g$ and $m$, so many logarithms to the same base share one table.
- **Order not needed.** Only an upper bound on the order is needed. The same structure computes the order of $g$ ([order finding](/order-finding/)): if a baby step repeats, the first repeat $g^j = 1$ gives it, and otherwise the least $i \ge 1$ with $g^{-im} = g^j$ for a baby step $g^j$ gives $\operatorname{ord}(g) = im + j$.

## Variants and improvements

- **Unbalanced steps.** If the table can hold only $M < \sqrt n$ elements, use $M$ baby steps and $n/M$ giant steps (Galbraith, Exercise 13.3.5). If the same base is used for $L$ logarithms, take $m \approx \sqrt{L n}$ baby steps once and about $\sqrt{n/L}$ giant steps per target, for $O(\sqrt{L n})$ in total (Galbraith, Exercise 13.3.12).
- **Interleaved.** Pollard's version alternates baby and giant steps, stores both in one table, and stops at the first match between the two lists. Its average cost is about $\tfrac{4}{3}\sqrt n$ operations instead of $1.5 \sqrt n$ (Galbraith, Exercise 13.3.4).
- **Interval.** If $x$ is known to lie in $[b, b + w)$, run the method on $h g^{-b}$ with $n = w$: $O(\sqrt w)$ operations, the baby-step giant-step solution of the [interval problem](/interval-discrete-logarithm-problem/). [Pollard's kangaroo](/pollard-kangaroo/) does the same with constant memory, heuristically.
- **Fast inversion.** On elliptic curves negation is free, so the baby steps $g^{\pm j}$ cover twice the range for the same work, which saves a factor of about $\sqrt 2$ (Galbraith, Exercise 13.3.7).
- **With Pohlig-Hellman.** For composite order the method is run in each prime order subgroup; [Pohlig-Hellman](/pohlig-hellman/) with baby-step giant-step costs $O(\sum e_i \sqrt{l_i})$ plus lower order terms for order $\prod l_i^{e_i}$.
- **Constant memory.** [Pollard's rho](/pollard-rho-discrete-logarithm/) replaces the table by a random walk and a collision search, with about the same time and $O(1)$ memory, at the price of a heuristic analysis.

## When to use it

Use it when the order $n$ is up to about $2^{40}$ to $2^{50}$, so that $\sqrt n$ elements fit in memory, and when a deterministic answer with a proof of non-membership is wanted. It is the standard subroutine inside [Pohlig-Hellman](/pohlig-hellman/) for the small prime factors of the group order, and inside many order computations. For larger prime orders, the memory makes it impractical; use [Pollard's rho](/pollard-rho-discrete-logarithm/) with [distinguished points](/distinguished-points/) instead. For large prime fields, [index calculus](/index-calculus/) is far faster.

## Pitfalls

- **Bound smaller than the order.** If $n < \operatorname{ord}(g)$, solutions with $x \ge m^2$ are missed and NONE is wrong. Line L1 must use a true upper bound such as $p - 1$, not a guess.
- **Rounding the square root down.** With $m = \lfloor \sqrt n \rfloor$ in line L1, $m^2$ can be less than $n$; for $n = 22$ that gives $m = 4$ and misses $x \in \{16, \dots, 21\}$. The right line is $m \leftarrow \lceil \sqrt n \rceil$, computed exactly with an integer square root, not with floating point.
- **Overwriting the table.** If line L5 stores $T[e] \leftarrow j$ unconditionally, an element of small order keeps its largest exponent below $m$, and the answer is a solution but not the least one. Keep the first exponent.
- **Wrong giant step.** Multiplying by $g^{m}$ instead of $g^{-m}$ in line L11 computes $h g^{im}$ and finds $x = j - im$, a negative or wrapped exponent. Line L7 must compute the inverse power.
- **Non-unique representations.** Projective elliptic curve points, or residues not reduced modulo $p$, hash differently even when equal. Normalize every element before line L5 and line L10 (Galbraith, Remark 13.3.2).
- **Inputs outside the group.** If $\gcd(g, p) \ne 1$, $g^{-1}$ does not exist and line L7 fails; check the input first. An $h$ that is not a unit (such as $0$) is never a power of $g$ and correctly gives NONE.

## Implementations

## History

Daniel Shanks described the baby-step giant-step idea in 1971, for computations in class groups of binary quadratic forms. Galbraith notes that Nechaev states the method was known to Gel'fond in 1962. The Handbook of Applied Cryptography gives it as the standard square root algorithm for the discrete logarithm, and Pollard's 2000 paper on kangaroos analyzed the interleaved variant with average cost about $\tfrac{4}{3}\sqrt n$.

## References
