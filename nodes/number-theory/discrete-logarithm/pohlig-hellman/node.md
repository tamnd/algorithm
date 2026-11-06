---
tag: PW5NFF
kind: algorithm
slug: pohlig-hellman
name: Pohlig-Hellman algorithm
aliases:
- Silver-Pohlig-Hellman
- Pohlig-Hellman reduction
area: number-theory/discrete-logarithm
level: core
summary: Reduces a discrete logarithm in a group of order N = prod l^e to logarithms in subgroups of prime order l and joins them by the CRT. The cost is set by the largest prime factor of N.
solves: [discrete-logarithm-problem]
model: generic-group-model
complexity:
  vars:
    N: a multiple of the order of g whose factorization is known
    q: the largest prime factor of the order of g
    s: the number of prime factors of N counted with multiplicity
    k: the number of binary digits of the modulus p, when the group is (Z/pZ)^*
  time:
    worst: O(log(N)^2 + s q^(1/2))
  space:
    extra: O(q^(1/2))
  bit_operations:
    worst: O((log(N)^2 + s q^(1/2)) k^2)
properties:
  deterministic: true
  recursive: false
prereqs: [discrete-logarithm-problem, chinese-remainder-theorem, baby-step-giant-step, lagranges-theorem-group-theory]
see_also: [pollard-rho-discrete-logarithm, safe-prime, small-subgroup-attack, smooth-number, multiplicative-order, garner-algorithm, sophie-germain-prime, cyclic-group]
sources:
  - paper: doi:10.1109/TIT.1978.1055817
    title: Stephen C. Pohlig and Martin E. Hellman, An improved algorithm for computing logarithms over GF(p) and its cryptographic significance, IEEE Transactions on Information Theory 24(1), 1978
    locator: pages 106 to 110 (the reduction to the prime power factors of p - 1, digit by digit)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 3, Section 3.6.4, Pohlig-Hellman algorithm (Algorithm 3.63, Example 3.64 in Z*_251, Fact 3.65, Notes 3.66 and 3.67)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 13, Section 13.2, The Pohlig-Hellman method (Lemma 13.2.1, Algorithm 13, Example 13.2.3, Theorem 13.2.5, and footnote 1 on the other discoverers)
---

The Pohlig-Hellman algorithm solves the [discrete logarithm problem](/discrete-logarithm-problem/) in a group whose order $N$ is known and factored, by reducing it to problems in subgroups of prime order. If $N = \prod l_i^{e_i}$, it finds $x \bmod l_i^{e_i}$ one base-$l_i$ digit at a time, each digit being a logarithm in a subgroup of order $l_i$, and then combines the residues with the [Chinese remainder theorem](/chinese-remainder-theorem/). With [baby-step giant-step](/baby-step-giant-step/) for the digits it takes $O(\sum e_i (\log N + \sqrt{l_i}))$ group operations, so the difficulty of the discrete logarithm in any group is that of its largest prime order subgroup. This is why groups for cryptography are chosen with a large prime order.

## In plain words

Suppose the length of the cycle of powers factors into small pieces, say two times three times three. Instead of searching for the full step count at once, you can ask simpler questions: is the count even or odd, and what is its remainder when divided by nine? Each question can be answered by looking at a much smaller cycle, obtained by raising everything to a suitable power. The remainder by nine is found one digit at a time in base three, and each digit is a search in a cycle of only three elements.

At the end, the remainders are glued together into the one count that has all of them. The total work is set by the largest piece of the factorization, not by the length of the cycle. If one piece is huge, this trick does not help with that piece.

## The problem

**Input.** A modulus $p$ and units $g, h$ modulo $p$, or more generally elements of any finite abelian group, together with the factorization $N = \prod_{i} l_i^{e_i}$ of a multiple $N$ of $\operatorname{ord}(g)$. For a prime $p$, $N = p - 1$.

**Output.** The least $x \ge 0$ with $g^x = h$, or NONE if $h \notin \langle g \rangle$.

**Cost model.** The algorithm uses only group operations, equality tests and hashing, so it is generic. Costs are counted in group operations; in $(\mathbb{Z}/p\mathbb{Z})^*$ one operation is a multiplication modulo $p$, $O(k^2)$ bit operations for a $k$-bit $p$ with schoolbook arithmetic. The factorization of $N$ is part of the input. For $N = p - 1$ it comes from [integer factorization](/integer-factorization/), which for the sizes in use is far cheaper than the discrete logarithm itself.

## The algorithm

The key fact is that for $l^f \mid r = \operatorname{ord}(g)$, the map $y \mapsto y^{r / l^f}$ sends $\langle g \rangle$ onto its subgroup of order $l^f$, and sends $g^x$ to $g_l^{x}$ with $g_l = g^{r/l^f}$ of order exactly $l^f$. So $h_l = h^{r/l^f}$ determines $x \bmod l^f$. Write $x \bmod l^f = d_0 + d_1 l + \dots + d_{f-1} l^{f-1}$ with digits $0 \le d_k < l$. If $x_l = d_0 + \dots + d_{k-1} l^{k-1}$ is already known, then

$$\big(h_l \, g_l^{-x_l}\big)^{l^{f-1-k}} = \gamma^{d_k}, \qquad \gamma = g_l^{\,l^{f-1}},$$

and $\gamma$ has order $l$. So each digit is a logarithm in a group of prime order $l$.

```pseudo id=main
POHLIG-HELLMAN(g, h, F)             ▷ F = {(l, e)}: N = ∏ l^e is a multiple of ord(g); returns least x or NONE
L1  r ← N; for each (l, e) in F do  ▷ reduce r to the exact order of g
L2      while l | r and g^(r/l) = 1 do
L3          r ← r / l
L4  if h^r ≠ 1 then return NONE     ▷ in a cyclic group: h ∈ ⟨g⟩ iff h^r = 1
L5  residues ← empty list
L6  for each prime l dividing r do
L7      f ← the exponent of l in r
L8      g_l ← g^(r / l^f), h_l ← h^(r / l^f)    ▷ project onto the subgroup of order l^f
L9      γ ← g_l^(l^(f−1))                       ▷ an element of order l
L10     x_l ← 0
L11     for k ← 0 to f − 1 do                   ▷ find the digit d_k of x in base l
L12         δ ← (h_l · g_l^(−x_l))^(l^(f−1−k))
L13         d ← BABY-STEP-GIANT-STEP(γ, δ, l)
L14         if d = NONE then return NONE
L15         x_l ← x_l + d · l^k
L16     append (x_l, l^f) to residues
L17 x ← CRT(residues)                 ▷ the x in [0, r) with x ≡ x_l mod l^f for all l
L18 if g^x ≠ h then return NONE      ▷ needed only in a non-cyclic group
L19 return x
```

Lines L1 to L3 compute the exact order $r$ of $g$: a prime $l$ is removed from $r$ while $g^{r/l} = 1$. Line L4 is the membership test of a cyclic group: the elements with $h^r = 1$ form the unique subgroup of order $r$, which is $\langle g \rangle$. Lines L6 to L16 handle one prime power at a time. Line L8 maps the problem into the subgroup of order $l^f$, line L9 builds the base $\gamma$ of order $l$, and lines L11 to L15 extract the digits from the lowest up: line L12 removes the digits found so far and raises to the power that kills all higher digits. Line L17 combines the residues with the [Chinese remainder theorem](/chinese-remainder-theorem/), for example by [Garner's algorithm](/garner-algorithm/). In a group that is not cyclic, such as $(\mathbb{Z}/15\mathbb{Z})^*$, an element with $h^r = 1$ need not be a power of $g$, and the check of line L18 catches this.

## Example

This is Galbraith's Example 13.2.3. Let $p = 19$, $g = 2$, $h = 5$ and $N = p - 1 = 18 = 2 \cdot 3^2$. Since $2^9 \equiv 18$ and $2^6 \equiv 7$ are not $1$, the order is $r = 18$, and $5^{18} \equiv 1$.

| step | computation | result |
|---|---|---|
| $l = 2$, $f = 1$ | $g_2 = 2^9 = 18$, $h_2 = 5^9 = 1$, $\gamma = 18$ | |
| digit $d_0$ | $\delta = 1 = \gamma^0$ | $x \equiv 0 \pmod 2$ |
| $l = 3$, $f = 2$ | $g_3 = 2^2 = 4$, $h_3 = 5^2 = 6$, $\gamma = 4^3 = 7$ | |
| digit $d_0$ | $\delta = 6^3 = 216 \equiv 7 = \gamma^1$ | $d_0 = 1$ |
| digit $d_1$ | $\delta = 6 \cdot 4^{-1} = 6 \cdot 5 \equiv 11 = 7^2$ | $d_1 = 2$, $x \equiv 1 + 2 \cdot 3 = 7 \pmod 9$ |
| CRT | $x \equiv 0 \pmod 2$, $x \equiv 7 \pmod 9$ | $x = 16$ |

Indeed $2^{16} = 2^{-2} = 4^{-1} \equiv 5 \pmod{19}$. Each digit was a logarithm in a group of order $2$ or $3$; the largest search was over three elements.

For an input with no solution, take $g = 4$ and $h = 2$. Lines L1 to L3 give $r = 9$, since $4^9 = 2^{18} \equiv 1$ but $4^3 \equiv 7$. Line L4 computes $2^9 \equiv 18 \ne 1$, so the algorithm returns NONE: $2$ has order $18$ and cannot lie in the subgroup of order $9$.

The Handbook of Applied Cryptography works a larger case, Example 3.64: $p = 251$, $g = 71$, $h = 210$, $p - 1 = 2 \cdot 5^3$, with answer $197$.

## Correctness

The invariant of the digit loop is: before round $k$ of lines L11 to L15, $x_l \equiv x \pmod{l^k}$ for every solution $x$, and $0 \le x_l < l^k$. In round $k$, $h_l g_l^{-x_l} = g_l^{x - x_l}$, and $x - x_l \equiv d_k l^k \pmod{l^{k+1}}$; raising to $l^{f-1-k}$ kills every multiple of $l^{f}$ in the exponent and leaves $\gamma^{d_k}$, so baby-step giant-step returns $d_k$. After the loop, $x_l \equiv x \pmod{l^f}$ for each prime, the CRT gives $x \bmod r$, and since $r$ is the exact order, the value in $[0, r)$ is the least solution. If $h \notin \langle g \rangle$, either line L4, line L14 or line L18 returns NONE. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $N = \prod l_i^{e_i}$, $s = \sum e_i \le \lg N$, and $q = \max l_i$ over the primes dividing $\operatorname{ord}(g)$. All bounds are proved and deterministic (with a sorted table in place of hashing).

- **Exact order (L1 to L3).** At most $s$ exponentiations of $O(\log N)$ multiplications each: $O(\log^2 N)$. When $N$ is already the order, this can be skipped.
- **Projections (L8, L9).** Three exponentiations per prime: $O(\omega \log N)$, where $\omega \le \lg N$ is the number of distinct primes.
- **Digits (L12).** For a prime power $l^f$, round $k$ computes $g_l^{-x_l}$ and one power with exponent $l^{f-1-k}$, $O(f \log l)$ multiplications, so $O(f^2 \log l)$ per prime and $O(\log^2 N)$ in total.
- **Small logarithms (L13).** $f$ calls of baby-step giant-step in a group of order $l$, each $O(\sqrt l)$ operations and $O(\sqrt l)$ storage.
- **Total.** $O(\log^2 N + \sum e_i \sqrt{l_i}) = O(\log^2 N + s \sqrt q)$ group operations and $O(\sqrt q)$ stored elements. This matches HAC's Fact 3.65, $O(\sum e_i (\lg N + \sqrt{l_i}))$, and Galbraith's Theorem 13.2.5, which states $O(\log^2 N + B \log N)$ for $B$-smooth $N$ with exhaustive search for the digits. A product tree for the projections improves the first terms to $O(\log N \log \log N)$ (Galbraith, Section 13.2).
- **Bit operations.** In $(\mathbb{Z}/p\mathbb{Z})^*$ with $k$-bit $p$: $O((\log^2 N + s \sqrt q) k^2)$.
- **Lower bound.** [Shoup's theorem](/shoup-generic-lower-bound/) gives $\Omega(\sqrt q)$ for every generic algorithm, so Pohlig-Hellman with baby-step giant-step is optimal for generic algorithms up to the factor $s$ and the polynomial terms.

## Properties

- **A reduction, not only an algorithm.** Any method for prime order groups can replace line L13: [Pollard's rho](/pollard-rho-discrete-logarithm/) for large $l$, a precomputed table for tiny $l$, or [index calculus](/index-calculus/) in a subgroup of a finite field.
- **Deterministic.** With baby-step giant-step for the digits, there is no randomness, and NONE is exact.
- **Least solution.** The CRT result lies in $[0, \operatorname{ord}(g))$, so it is the least non-negative solution.
- **Generic.** It uses only the group operations, so it works in $(\mathbb{Z}/p\mathbb{Z})^*$, on elliptic curves and in any abelian group with known order.
- **Needs the factorization.** The order and its factorization must be known; for $\mathbb{F}_p^*$ that means factoring $p - 1$, which is usually easy for the sizes in use because $p - 1$ has many small factors.

## Variants and improvements

- **Digits by rho.** For a large prime $l$, solve each digit with Pollard's rho in $O(\sqrt l)$ operations and constant memory, heuristically.
- **All digits at once.** If $l^f$ is small, solve the logarithm in the subgroup of order $l^f$ directly by baby-step giant-step in $O(l^{f/2})$, which beats $f \sqrt l$ only for tiny $l^f$.
- **Square roots.** [Tonelli-Shanks](/tonelli-shanks/) is the Pohlig-Hellman idea in the Sylow $2$-subgroup of $\mathbb{F}_p^*$: it finds the digits of a logarithm in base $2$, and the Adleman-Manders-Miller method does the same for $r$-th roots ([discrete root](/discrete-root/)).
- **Interval plus smooth order.** If $x$ is known to lie in an interval of width $w$ and $N = m q$ with $m$ smooth, Pohlig-Hellman gives $x \bmod m$ and an interval method finishes in $O(\sqrt{w/m})$ (Galbraith, Exercise 13.3.9).
- **Faster projections.** A tree of partial products computes all $g^{N/l_i^{e_i}}$ in $O(\log N \log \log N)$ operations instead of $O(\omega \log N)$.

## When to use it

Use it as the first step of every discrete logarithm computation in a group of known order: it reduces the problem to the prime order subgroups, and nothing is lost by doing so. It solves the whole problem when every prime factor of the order is small, which is what makes groups with a smooth order insecure. In a well chosen cryptographic group, such as a prime order subgroup of an elliptic curve or a [safe prime](/safe-prime/) field, the remaining prime order part is large, and the work moves to rho or to index calculus.

## Pitfalls

- **Using the group order when the element has smaller order.** If line L1 used $N$ itself as the order and $g$ has smaller order, the projections $g^{N/l^e}$ can be $1$ and the digit loop meets a base $\gamma = 1$, for which baby-step giant-step returns $0$ for $\delta = 1$ and NONE otherwise, rejecting valid inputs. Reduce $N$ to the exact order first (lines L1 to L3), or skip primes for which $g_l = 1$.
- **Projecting by the wrong exponent.** The projection must raise to $r / l^f$, the cofactor of the prime power, as in line L8, not to $r / l$; raising to $r / l$ throws away all but the lowest digit.
- **Forgetting to remove found digits.** Line L12 must multiply by $g_l^{-x_l}$ before raising to $l^{f-1-k}$. Without it, every round recovers $d_0$ again.
- **Skipping the membership check.** Without line L4 (or line L18 in non-cyclic groups), an $h$ outside $\langle g \rangle$ may produce a wrong $x$ from the CRT. For the units modulo $15$, $g = 4$ has order $2$ and $h = 11$ satisfies $h^2 = 1$, but $11 \notin \{1, 4\}$; only line L18 detects it.
- **Small subgroup attacks.** In protocols, an attacker who sends an element of small order learns the secret exponent modulo that order through this method. Check that received elements lie in the prime order subgroup ([small subgroup attack](/small-subgroup-attack/)).

## Implementations

## History

Stephen Pohlig and Martin Hellman published the method in 1978, in a paper whose title stresses its cryptographic consequence: logarithms modulo $p$ are easy when $p - 1$ has only small prime factors. Galbraith notes that R. Silver, R. Schroeppel, H. Block and V. Nechaev also discovered it, which is why it is sometimes called the Silver-Pohlig-Hellman algorithm. The paper led to the advice that $p - 1$ must have a large prime factor, and later to the use of prime order subgroups and [safe primes](/safe-prime/).

## References
