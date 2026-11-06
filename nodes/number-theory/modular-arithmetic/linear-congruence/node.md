---
tag: E0PRD3
kind: problem
slug: linear-congruence
name: Linear congruence
aliases:
- solving a·x ≡ b (mod n)
area: number-theory/modular-arithmetic
level: core
summary: Find all x with a·x ≡ b (mod n), solvable exactly when gcd(a, n) divides b.
prereqs: [congruence, greatest-common-divisor, bezouts-identity]
see_also: [modular-linear-equation, modular-linear-equation-solver, modular-inverse, linear-diophantine-equation, chinese-remainder-theorem, extended-euclidean-algorithm, gaussian-elimination-modular, euclids-lemma]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.4, Solving modular linear equations
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 5, Section 5.4, Linear congruences
  - book: isbn:9780471625469
    title: Ivan Niven, Herbert S. Zuckerman and Hugh L. Montgomery, An Introduction to the Theory of Numbers, fifth edition
    locator: Section 2.2, Solutions of congruences, and Section 2.3, The Chinese remainder theorem
  - book: isbn:9780387973296
    title: Kenneth Ireland and Michael Rosen, A Classical Introduction to Modern Number Theory, second edition
    locator: Chapter 3, Congruence (the congruence ax ≡ b (m) and the Chinese remainder theorem)
---

A linear congruence is a condition $ax \equiv b \pmod n$ on an unknown integer $x$, where $a$, $b$ and the modulus $n \ge 1$ are given; the problem is to find all its solutions or to show there are none. It has a solution exactly when $d = \gcd(a, n)$ [divides](/divisibility/) $b$, and then its solutions form one residue class modulo $n/d$, which is $d$ classes modulo $n$. One run of the [extended Euclidean algorithm](/extended-euclidean-algorithm/) finds them all. It is the modular form of the [linear Diophantine equation](/linear-diophantine-equation/) $ax - ny = b$, and the building block of the [Chinese remainder theorem](/chinese-remainder-theorem/).

## In plain words

You want a number that, multiplied by a given number, leaves a given remainder on a clock of a given size. Sometimes there is exactly one answer on the clock, sometimes none, and sometimes several. It depends on the largest number that divides both the multiplier and the clock size. If that common factor does not also divide the wanted remainder, no answer exists, because every multiple lands on a multiple of the factor. If it does divide, you can cancel it everywhere, solve the smaller problem with an inverse, and then get as many answers on the big clock as the size of the common factor, spread out evenly.

## Definition

**Input.** Integers $a$ and $b$, and a modulus $n \ge 1$. Only the residues of $a$ and $b$ modulo $n$ matter, so one may assume $0 \le a, b < n$.

**Output.** The set $S = \{ x \in \mathbb{Z} : ax \equiv b \pmod n \}$. It is a union of residue classes modulo $n$, so it is described by the residues in $\{0, \ldots, n - 1\}$ that it contains, or more compactly by one class $x_0 \bmod n'$ as in the theorem.

**Theorem.** Let $n \ge 1$ and $d = \gcd(a, n)$.

1. $S$ is non-empty if and only if $d \mid b$.
2. If $d \mid b$, let $x'$ be an integer with $ax' \equiv d \pmod n$, for example the first [Bézout coefficient](/bezouts-identity/) in $ax' + ny' = d$. Then $x_0 = x' \cdot (b/d)$ is a solution.
3. If $x_0 \in S$, then $S = \{ x : x \equiv x_0 \pmod{n/d} \}$. So $S$ contains exactly $d$ residues modulo $n$: $x_0 + i \cdot n/d$ for $i = 0, 1, \ldots, d - 1$, reduced modulo $n$.

*Proof.* (1, only if) If $ax \equiv b \pmod n$, then $b = ax - nk$ for some integer $k$. The integer $d$ divides $a$ and $n$, so it divides $b$.

(2, and the if part of 1) Bézout's identity gives $ax' + ny' = d$, so $ax' \equiv d \pmod n$. Multiply by the integer $b/d$: $a \cdot x'(b/d) \equiv b \pmod n$.

(3) Let $x_0 \in S$. For an integer $x$, $ax \equiv b \pmod n$ holds if and only if $ax \equiv ax_0 \pmod n$, that is, $n \mid a(x - x_0)$. Write $a = d a'$ and $n = d n'$. Since $d \ge 1$ (as $n \ge 1$), this is equivalent to $n' \mid a'(x - x_0)$. Now $\gcd(a', n') = 1$, because a common divisor $c > 1$ would make $cd$ a common divisor of $a$ and $n$ larger than $d$. By [Euclid's lemma](/euclids-lemma/) in Gauss's form, $n' \mid a'(x - x_0)$ holds if and only if $n' \mid x - x_0$. So $S$ is the class of $x_0$ modulo $n' = n/d$. That class meets $\{0, \ldots, n-1\}$ in the $d$ numbers $x_0 \bmod n' + i n'$ for $i = 0, \ldots, d - 1$, which are distinct modulo $n$ because they differ by less than $n$. $\square$

**Special cases.**

- If $\gcd(a, n) = 1$, there is exactly one solution modulo $n$, namely $x \equiv a^{-1} b$, with the [modular inverse](/modular-inverse/) $a^{-1}$.
- If $a \equiv 0 \pmod n$, then $d = n$: every $x$ is a solution when $n \mid b$, and none is when $n \nmid b$.
- The homogeneous congruence $ax \equiv 0 \pmod n$ always has the $d$ solutions $i \cdot n/d$, for $i = 0, \ldots, d - 1$.

**Cost models.** For word-sized $n$ on the [word RAM](/word-ram/), each division with remainder costs one unit. For $n$ of $k$ binary digits in arbitrary precision, cost is counted in bit operations.

## Variants

- **Listing every solution.** Output the $d$ residues explicitly. This is the [modular linear equation](/modular-linear-equation/) problem in the form of CLRS, solved by the [modular linear equation solver](/modular-linear-equation-solver/). The output can be as large as $n$ itself.
- **Several unknowns.** $a_1 x_1 + \cdots + a_k x_k \equiv b \pmod n$. Let $d = \gcd(a_1, \ldots, a_k, n)$. The map $(x_1, \ldots, x_k) \mapsto \sum a_i x_i \bmod n$ is a homomorphism of additive groups from $(\mathbb{Z}/n\mathbb{Z})^k$ onto the subgroup of multiples of $d$, which has $n/d$ elements. So the congruence is solvable if and only if $d \mid b$, and then it has exactly $d \cdot n^{k-1}$ solutions modulo $n$, the size of each fiber.
- **Simultaneous congruences in one unknown.** $a_i x \equiv b_i \pmod{n_i}$ for $i = 1, \ldots, t$. Solve each one into $x \equiv c_i \pmod{m_i}$, then combine with the [Chinese remainder theorem](/chinese-remainder-theorem/). For moduli that are not pairwise coprime, $x \equiv c_i \pmod{m_i}$ and $x \equiv c_j \pmod{m_j}$ are compatible if and only if $c_i \equiv c_j \pmod{\gcd(m_i, m_j)}$; see the [Chinese remainder problem](/chinese-remainder-problem/).
- **Linear systems.** $Ax \equiv b \pmod n$ for a matrix $A$. Modulo a prime this is [Gaussian elimination modulo p](/gaussian-elimination-modular/); modulo a composite $n$ it needs the Hermite or Smith normal form, since not every nonzero pivot is invertible.
- **Solutions in a range.** Count or list the solutions in an interval $[L, R]$. Since $S$ is an arithmetic progression with step $n/d$, this is a few divisions; see [linear Diophantine solutions in an interval](/linear-diophantine-solutions-in-interval/).

## Examples

| congruence | $d = \gcd(a, n)$ | solutions modulo $n$ |
| --- | --- | --- |
| $14x \equiv 30 \pmod{100}$ | 2 | 45, 95 |
| $3x \equiv 5 \pmod 7$ | 1 | 4 |
| $6x \equiv 4 \pmod 9$ | 3 | none, since $3 \nmid 4$ |
| $6x \equiv 3 \pmod 9$ | 3 | 2, 5, 8 |
| $12x \equiv 8 \pmod{20}$ | 4 | 4, 9, 14, 19 |
| $35x \equiv 10 \pmod{50}$ | 5 | 6, 16, 26, 36, 46 |
| $0x \equiv 0 \pmod 5$ | 5 | 0, 1, 2, 3, 4 |
| $-3x \equiv 4 \pmod{10}$ | 1 | 2 |

**Worked example.** For $14x \equiv 30 \pmod{100}$, $d = 2$ divides 30. Cancel $d$ to get $7x \equiv 15 \pmod{50}$. The inverse of 7 modulo 50 is 43, since $7 \cdot 43 = 301 = 6 \cdot 50 + 1$. So $x \equiv 15 \cdot 43 = 645 \equiv 45 \pmod{50}$, and the solutions modulo 100 are $45$ and $95$. Check: $14 \cdot 45 = 630 \equiv 30$ and $14 \cdot 95 = 1330 \equiv 30 \pmod{100}$.

**Several unknowns.** $6x + 10y \equiv 4 \pmod{15}$ has $d = \gcd(6, 10, 15) = 1$, so it has $1 \cdot 15 = 15$ solution pairs modulo 15. And $6x + 9y \equiv 3 \pmod{15}$ has $d = 3$, so $3 \cdot 15 = 45$ pairs.

## Known algorithms

- [Extended Euclidean algorithm](/extended-euclidean-algorithm/): gives $d$ and $x'$ with $ax' \equiv d \pmod n$, hence $x_0$ by part 2 of the theorem, in $O(\log n)$ division steps.
- [Modular linear equation solver](/modular-linear-equation-solver/): the procedure of CLRS Section 31.4, which also lists the $d$ solutions.
- [Modular inverse](/modular-inverse/) after cancelling $d$: $x \equiv (b/d)(a/d)^{-1} \pmod{n/d}$. Any inverse method works, including [Fermat's little theorem](/fermat-little-theorem/) when $n/d$ is prime.
- [Linear Diophantine solution](/linear-diophantine-solution/): solving $ax - ny = b$ in integers gives the same $x$.

## Bounds

**Word-sized modulus.** Finding $d$ and one solution takes $O(\log n)$ time in the worst case, by the bound on the Euclidean algorithm ([Lamé's theorem](/lames-theorem/)), and $O(1)$ extra words. The compact answer $(x_0 \bmod n/d, \; n/d)$ has constant size. Listing all residues modulo $n$ takes $\Theta(d)$ more time, which is needed just to write them.

**Arbitrary precision.** For $n$ of $k$ binary digits, the extended gcd costs $O(k^2)$ bit operations with classical arithmetic and $O(M(k) \log k)$ with the [half-GCD](/half-gcd/), where $M(k)$ is the cost of a product. The final product $x'(b/d)$ and its reduction cost $O(M(k))$.

**Lower bound.** Deciding solvability already decides whether $\gcd(a, n) = 1$ (take $b = 1$), so the problem is at least as hard as testing [coprimality](/coprime-integers/). No lower bound above the input size is known for that.

## Reductions

- **Equivalent to a linear Diophantine equation.** $ax \equiv b \pmod n$ holds if and only if $ax - ny = b$ for some integer $y$. So the two problems have the same solvability condition and the same $x$-solutions, and each reduces to the other in $O(1)$ operations; see [linear Diophantine equation](/linear-diophantine-equation/).
- **To a modular inverse.** After cancelling $d$, a solvable congruence has a unit coefficient, so one inverse modulo $n/d$ and one product solve it.
- **The modular inverse is a special case.** $a^{-1} \bmod n$ is the solution of $ax \equiv 1 \pmod n$.
- **Building block of the Chinese remainder theorem.** Combining $x \equiv r_1 \pmod{m_1}$ with $x \equiv r_2 \pmod{m_2}$ means solving $m_1 t \equiv r_2 - r_1 \pmod{m_2}$ for $t$ and setting $x = r_1 + m_1 t$.

## Applications

- **The Chinese remainder theorem and Garner's algorithm.** Each combining step solves one linear congruence ([Garner's algorithm](/garner-algorithm/)).
- **Periodic events.** Two events that repeat with periods $p_1$ and $p_2$ and offsets $r_1$ and $r_2$ meet at the times $t$ with $t \equiv r_1 \pmod{p_1}$ and $t \equiv r_2 \pmod{p_2}$, which reduces to one linear congruence.
- **Affine ciphers and linear congruential generators.** Undoing $y = ax + c \bmod n$ is a linear congruence in $x$. For a [linear congruential generator](/linear-congruential-generator/) with a known multiplier, the previous state follows from the current one in the same way.
- **Stepping through a table.** A probe sequence $h, h + s, h + 2s, \ldots$ modulo $m$ visits each slot exactly when $\gcd(s, m) = 1$, by part 3 of the theorem with $d = 1$; this is why double hashing chooses the step coprime to the table size.

## References
