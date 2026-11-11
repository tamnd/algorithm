---
tag: QB9T1W
kind: algorithm
slug: csidh
name: CSIDH
aliases:
- Commutative SIDH
- CSIDH-512
area: cryptography/post-quantum
level: research
summary: "Isogeny key exchange (Castryck et al., 2018) where a class group acts on supersingular curves over F_p, p = 4·l1⋯ln − 1. It gives a post-quantum NIKE, but quantum sieves force large p."
model: word-ram
complexity:
  vars: {m: "the bound on the secret exponents |e_i|", n: "the number of small primes l_i", L: "the largest l_i", p: "the prime; time is the expected count of operations in F_p"}
  time: {worst: O(m n (log p + L)), average: O(m n (log p + L)), best: O(m n (log p + L))}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true}
history:
  year: 2018
  people: [Wouter Castryck, Tanja Lange, Chloe Martindale, Lorenz Panny, Joost Renes]
  note: Presented at ASIACRYPT 2018. It moved the group action idea of Couveignes, Rostovtsev and Stolbunov from ordinary to supersingular curves, which made it fast enough to use.
prereqs: [supersingular-isogeny-problem, isogeny-based-cryptography, diffie-hellman, ideal-class-group]
see_also: [sidh, castryck-decru-attack, quantum-class-group-algorithm, shor-algorithm, nist-security-levels, crystals-kyber, hybrid-key-exchange, euler-criterion]
sources:
  - paper: "Wouter Castryck, Tanja Lange, Chloe Martindale, Lorenz Panny and Joost Renes, CSIDH: an efficient post-quantum commutative group action, ASIACRYPT 2018, LNCS 11274"
    locator: the free and transitive class group action, the uniqueness of the Montgomery coefficient for p = 3 mod 8, Algorithm 2 for the action, the public key check, and the CSIDH-512 parameters
  - url: "https://eprint.iacr.org/2006/291"
    title: Jean-Marc Couveignes, Hard homogeneous spaces, IACR ePrint 2006/291 (written in 1997)
    locator: the Diffie-Hellman protocol on a principal homogeneous space of a commutative group, with the class group acting on ordinary curves
  - url: "https://eprint.iacr.org/2006/145"
    title: Alexander Rostovtsev and Anton Stolbunov, Public-key cryptosystem based on isogenies, IACR ePrint 2006/145
    locator: key exchange from isogeny walks on ordinary curves
  - paper: "Craig Costello and Huseyin Hisil, A simple and compact algorithm for SIDH with arbitrary degree isogenies, ASIACRYPT 2017, LNCS 10625"
    locator: the x-only formulas for an isogeny of odd degree on a Montgomery curve, used by the code here
  - paper: "Andrew M. Childs, David Jao and Vladimir Soukharev, Constructing elliptic curve isogenies in quantum subexponential time, Journal of Mathematical Cryptology 8(1), 2014"
    locator: the reduction from the group action inverse problem to the abelian hidden shift problem, solved with Kuperberg's algorithm
  - paper: "Greg Kuperberg, A subexponential-time quantum algorithm for the dihedral hidden subgroup problem, SIAM Journal on Computing 35(1), 2005"
    locator: the sieve that solves the hidden shift problem in an abelian group of size N with 2^O(sqrt(log N)) quantum queries
  - paper: "Chris Peikert, He gives C-sieves on the CSIDH, EUROCRYPT 2020, LNCS 12106"
    locator: the collimation sieve with classical memory and the estimate that CSIDH-512 falls short of NIST category 1
  - paper: "Xavier Bonnetain and Andre Schrottenloher, Quantum security analysis of CSIDH, EUROCRYPT 2020, LNCS 12106"
    locator: the cost of the Kuperberg-type attacks on CSIDH and the larger primes they propose
  - paper: "Daniel J. Bernstein, Tanja Lange, Chloe Martindale and Lorenz Panny, Quantum circuits for the CSIDH: optimizing quantum evaluation of isogenies, EUROCRYPT 2019, LNCS 11477"
    locator: the cost of one quantum evaluation of the CSIDH-512 action, the oracle inside the sieve
  - paper: "Ward Beullens, Thorsten Kleinjung and Frederik Vercauteren, CSI-FiSh: efficient isogeny based signatures through class group computations, ASIACRYPT 2019, LNCS 11921"
    locator: the computation of the class group of CSIDH-512 and its relation lattice, and the signature built on it
---

CSIDH (Commutative Supersingular Isogeny Diffie-Hellman, said "seaside") is a key exchange in which a commutative group acts on a set of elliptic curves, and the two parties use this action as [Diffie-Hellman](/diffie-hellman/) uses exponentiation. Castryck, Lange, Martindale, Panny and Renes introduced it in 2018. Its public keys are one number mod $p$, 64 bytes at the original size, and a party can check a public key cheaply. So CSIDH gives a non-interactive key exchange (NIKE) with static keys, which no other post-quantum scheme gives at this size. It is not broken, but subexponential quantum attacks mean that the prime must be much larger than first proposed. It is not a NIST standard and it was not submitted to the [NIST process](/nist-pqc-standardization/).

**Notation.** $\ell_1 < \cdots < \ell_n$ are small odd primes and $p = 4 \ell_1 \cdots \ell_n - 1$ is prime, so $p \equiv 3 \pmod 8$. For $A \in \mathbb{F}_p$, $E_A$ is the Montgomery curve $y^2 = x^3 + A x^2 + x$. $\pi$ is the Frobenius map $(x, y) \mapsto (x^p, y^p)$, and for a supersingular $E_A$ it satisfies $\pi^2 = -p$. $\mathcal{O} = \mathbb{Z}[\sqrt{-p}]$ is an order in an imaginary quadratic field, and $\mathrm{Cl}(\mathcal{O})$ is its [ideal class group](/ideal-class-group/). $\mathfrak{l}_i = (\ell_i, \pi - 1)$ and $\overline{\mathfrak{l}}_i = (\ell_i, \pi + 1)$. For a class $[\mathfrak{a}]$, $[\mathfrak{a}] \star E$ is the action defined below.

## In plain words

There is a large set of special curves, each named by one number. There is also a group of moves, and a move takes any curve in the set to another curve in the set. The important thing is that the moves commute: doing move one and then move two lands on the same curve as doing move two and then move one.

Alice picks a secret move, applies it to a fixed public starting curve, and publishes the number of the curve she reaches. Bob does the same with his own secret move. Then each applies their own secret move to the other's published curve. Because the moves commute, both reach the same curve, and its number is the shared secret.

Finding the secret move from the start and the end is believed hard. A quantum computer helps more here than first thought, so the numbers must be large.

## The problem

Two parties want a shared secret over a public channel, from a problem that [Shor's algorithm](/shor-algorithm/) does not solve. Diffie-Hellman needs a group in which $(g^a)^b = (g^b)^a$; CSIDH needs only a commutative group $G$ acting on a set $X$, with $g \star (h \star x) = h \star (g \star x)$. The hoped hard problem is the group action inverse problem: given $E$ and $[\mathfrak{a}] \star E$, find $[\mathfrak{a}]$. It is a commutative special case of the [supersingular isogeny problem](/supersingular-isogeny-problem/), and its commutativity is what gives quantum attacks a hold.

**The action.** Let $X$ be the set of supersingular curves $E_A$ over $\mathbb{F}_p$. For $p \equiv 3 \pmod 8$, every such curve has $\mathbb{F}_p$-rational endomorphism ring $\mathcal{O}$, and different $A$ give curves that are not isomorphic over $\mathbb{F}_p$. The group $\mathrm{Cl}(\mathcal{O})$ acts freely and transitively on $X$: an ideal $\mathfrak{a}$ maps $E$ to $E / E[\mathfrak{a}]$, where $E[\mathfrak{a}]$ is the set of points killed by every element of $\mathfrak{a}$. This is a theorem of Deuring's theory, stated in the CSIDH paper as the reason the scheme works.

Because $\ell_i$ divides $p + 1$, we have $-p \equiv 1 \pmod{\ell_i}$, so $(\ell_i)$ splits as $\mathfrak{l}_i \overline{\mathfrak{l}}_i$, and $[\overline{\mathfrak{l}}_i] = [\mathfrak{l}_i]^{-1}$. These classes have very simple kernels:

- $E[\mathfrak{l}_i]$ is the set of points $P$ of order $\ell_i$ with $\pi(P) = P$: the points of order $\ell_i$ in $E(\mathbb{F}_p)$.
- $E[\overline{\mathfrak{l}}_i]$ is the set of points of order $\ell_i$ with $\pi(P) = -P$: those with $x \in \mathbb{F}_p$ and $y \notin \mathbb{F}_p$, which are $\mathbb{F}_p$-points of the quadratic twist.

Since $\#E(\mathbb{F}_p) = p + 1 = 4 \ell_1 \cdots \ell_n$, each of these kernels is easy to find with a scalar multiplication. A secret is an exponent vector $(e_1, \ldots, e_n)$ with $|e_i| \le m$, standing for the class $[\mathfrak{l}_1^{e_1} \cdots \mathfrak{l}_n^{e_n}]$.

## The algorithm

The protocol is Diffie-Hellman with the action in place of exponentiation, from $E_0 : y^2 = x^3 + x$.

- **Key generation.** Alice picks $e \in [-m, m]^n$ uniformly. Her public key is $A = \text{GROUP-ACTION}(0, e)$.
- **Shared key.** On Bob's public key $B$, Alice first checks that $E_B$ is supersingular and stops if not. Her shared key is $\text{GROUP-ACTION}(B, e)$. Bob does the same with his secret and $A$.

GROUP-ACTION is Algorithm 2 of the CSIDH paper. It uses $x$-only Montgomery arithmetic, so a point is given by its $x$-coordinate, and one random $x$ gives a point on $E_A$ or on its twist. [Euler's criterion](/euler-criterion/) tells which.

```pseudo id=main
GROUP-ACTION(A, (e_1, …, e_n))             ▷ returns [l_1^e_1 ⋯ l_n^e_n] ⋆ E_A
L1  while some e_i ≠ 0 do
L2      x ← uniform in F_p \ {0}
L3      s ← +1 if x³ + Ax² + x is a square in F_p, else −1    ▷ s = +1: P on E_A; s = −1: P on the twist
L4      S ← {i : s · e_i > 0}; if S = ∅ then go to L1
L5      k ← ∏_{i ∈ S} ℓ_i
L6      Q ← [(p + 1)/k] P                     ▷ x-only Montgomery ladder; Q has order dividing k
L7      for i ∈ S do
L8          K ← [k/ℓ_i] Q                     ▷ K has order 1 or ℓ_i
L9          if K = ∞ then continue
L10         A, Q ← codomain of the ℓ_i-isogeny with kernel ⟨K⟩, and the image of Q
L11         k ← k/ℓ_i; e_i ← e_i − s
L12 return A
```

Line L10 uses the $x$-only formulas of Costello and Hisil (2017). For $\ell = 2d + 1$, let $x_j = x([j] K)$ for $j = 1, \ldots, d$. The isogeny maps $x \mapsto x \prod_j \left( \frac{x x_j - 1}{x - x_j} \right)^2$, and the codomain is $E_{A'}$ with

$$A' = \Bigl(\prod_{j=1}^{d} x_j\Bigr)^2 \Bigl(A - 6 \sum_{j=1}^{d} \bigl(x_j - x_j^{-1}\bigr)\Bigr).$$

## Example

The code with this page uses the toy prime $p = 4 \cdot 3 \cdot 5 \cdot 7 - 1 = 419$. **It is a toy.** It has only 27 curves, so every key falls to a table of 27 entries. Write $[a, b, c]$ for the exponent vector of $\mathfrak{l}_3^a \mathfrak{l}_5^b \mathfrak{l}_7^c$.

1. One step from $E_0$: $[1, 0, 0] \star E_0 = E_{158}$, $[0, 1, 0] \star E_0 = E_{199}$ and $[0, 0, 1] \star E_0 = E_{75}$. The inverse step gives $[-1, 0, 0] \star E_0 = E_{261}$, and $261 = -158 \bmod 419$: the action of $\mathfrak{a}^{-1}$ on $E_0$ gives the quadratic twist $E_{-A}$ of $\mathfrak{a} \star E_0 = E_A$. So the inverse of a public key is free to compute.
2. The orbit of $E_0$ under the three steps has 27 curves, with $A$ in $\{0, 6, 9, 15, 29, 40, 51, 75, 124, 144, 158, 174, 191, 199, 220, 228, 245, 261, 275, 295, 344, 368, 379, 390, 404, 410, 413\}$. These are all the supersingular $E_A$ over $\mathbb{F}_{419}$, as the theory says. The class group has 27 elements and is cyclic: $[\mathfrak{l}_3]$ and $[\mathfrak{l}_7]$ have order 27, and $[\mathfrak{l}_5]$ has order 9.
3. With seed 2024 and $m = 2$, Alice's secret is $[1, -1, 2]$ and her public key is $A = 261$. Bob's secret is $[0, 2, -1]$ and his public key is $B = 245$. Alice computes $[1, -1, 2] \star E_{245}$ and Bob computes $[0, 2, -1] \star E_{261}$. Both get $E_6$, so the shared key is $6$.

Alice's public key is the same as that of the secret $[-1, 0, 0]$. Different exponent vectors often give the same class; only the class matters. In CSIDH-512 the box $[-5, 5]^{74}$ has $11^{74} \approx 2^{256}$ vectors, close to the class number of about $\sqrt{p} \approx 2^{256}$, and the CSIDH paper assumes that the vectors cover the group nearly uniformly.

The tests check the steps above, check that 20 random pairs of keys agree, check that an ordinary curve is rejected, and break toy keys with the table of 27 entries. The code is for study only and is not constant time: the number of rounds and the isogeny degrees depend on the secret. For a real key exchange use ML-KEM ([CRYSTALS-Kyber](/crystals-kyber/)) from a FIPS 140 validated module, alone or in a [hybrid](/hybrid-key-exchange/) with X25519 from libsodium.

## Correctness

Two facts carry the proof. First, the class group is abelian, so $[\mathfrak{a}] \star ([\mathfrak{b}] \star E_0) = [\mathfrak{a}\mathfrak{b}] \star E_0 = [\mathfrak{b}] \star ([\mathfrak{a}] \star E_0)$, and since $A$ fixes the curve up to $\mathbb{F}_p$-isomorphism, both parties get the same $A$. Second, GROUP-ACTION computes the action. The point from line L3 lies in $\ker(\pi - s)$, and multiplication by a scalar keeps it there. So the point $K$ from line L8, if it is not $\infty$, generates $E[\mathfrak{l}_i]$ when $s = 1$ or $E[\overline{\mathfrak{l}}_i]$ when $s = -1$. The isogeny of line L10 then applies $[\mathfrak{l}_i]^s$, which matches the update $e_i \leftarrow e_i - s$. The image of $Q$ keeps the order needed for the next prime in $S$. The [full proof](proofs/correctness.md) gives the details.

## Complexity

Count operations in $\mathbb{F}_p$. Line L6 and each run of line L8 are Montgomery ladders of $O(\log p)$ steps. Each isogeny of line L10 costs $O(\ell_i)$ to find the $x_j$ and to push one point. So a round costs $O(n \log p + n L)$. In a round, each $i$ with the right sign succeeds unless the random point has no $\ell_i$ part, which happens with probability $1/\ell_i$. A sign matches about half the time, so about $2m$ rounds suffice on average, and the expected total is $O(m n (\log p + L))$. The loop has no fixed bound, but more rounds become exponentially unlikely. The square root Velu formulas of Bernstein, De Feo, Leroux and Smith (2020) cut the isogeny cost to $\tilde{O}(\sqrt{\ell})$, which helps for large $\ell$.

In practice, one action for CSIDH-512 takes tens of milliseconds, many times slower than X25519 or ML-KEM. The larger primes needed against quantum attacks make it slower again.

## Properties

- **Commutative.** The action of an abelian group makes the protocol a direct analogue of Diffie-Hellman. [SIDH](/sidh/) lacked this and had to publish torsion images, which the [Castryck-Decru attack](/castryck-decru-attack/) used. CSIDH publishes no torsion images, so that attack does not apply.
- **Non-interactive.** A party checks a public key by testing that $E_B$ is supersingular, which is cheap. So keys can be static and reused, and two parties who know each other's public keys share a key without sending a message.
- **Small keys.** A public key is one element of $\mathbb{F}_p$: 64 bytes for CSIDH-512.
- **Randomized, variable time.** The algorithm uses random points. The plain form leaks the secret through timing.
- **Free inverse.** The inverse class acts on $E_0$ as the twist, $A \mapsto -A$.

## Variants and improvements

- **Constant-time forms.** Meyer, Campos and Reith (2019) and Onuki and others (2019) add dummy isogenies and fixed loop counts. Cervantes-Vazquez and others (2019) remove the dummy operations to resist fault attacks. CTIDH (Banegas and others, 2021) groups the primes in batches and is the fastest constant-time form.
- **Faster isogenies.** The square root Velu formulas of Bernstein, De Feo, Leroux and Smith (ANTS 2020) for large degrees; strategies for the order of the steps.
- **CSI-FiSh.** Beullens, Kleinjung and Vercauteren (2019) computed the class group of CSIDH-512 and a reduced basis of its relation lattice. With them, any class can be written as a short exponent vector, which gives a uniform action and a Fiat-Shamir signature. The [quantum class group algorithm](/quantum-class-group-algorithm/) does this in polynomial time on a quantum computer; classically it costs subexponential time and has been done only for small parameters.
- **Larger parameters.** After the quantum analyses below, later papers propose primes of thousands of bits for [NIST category 1](/nist-security-levels/), often with few primes and small exponents, as in SQALE (Chavez-Saab, Chi-Dominguez, Jaques and Rodriguez-Henriquez, 2022).
- **The ancestor.** Couveignes (1997, published 2006) and Rostovtsev and Stolbunov (2006) used ordinary curves, where the steps need large field extensions; their scheme was very slow. CSIDH gets all kernels over $\mathbb{F}_p$ by the choice of $p$.

## When to use it

Use CSIDH for research, or where a post-quantum NIKE with static keys and small keys is the requirement and the cost is acceptable, and then only with conservative parameters and a constant-time implementation. Do not use CSIDH-512 as a stand-alone post-quantum scheme: the quantum attacks below put it under NIST category 1. For ordinary key exchange, a KEM such as ML-KEM is faster, standardized and better studied.

## Pitfalls

- **Quantum attacks are subexponential.** The action is a commutative group action, so the inverse problem reduces to an abelian hidden shift problem: $f_0(\mathfrak{x}) = \mathfrak{x} \star E_0$ and $f_1(\mathfrak{x}) = \mathfrak{x} \star E_A$ differ by the shift $\mathfrak{a}$. Childs, Jao and Soukharev (2014) applied Kuperberg's algorithm to this problem, which runs in time $2^{O(\sqrt{\log N})}$ for a group of size $N$. In 2020, Peikert (He gives C-sieves on the CSIDH) and Bonnetain and Schrottenloher gave concrete costs with Kuperberg's later sieves. Both concluded that CSIDH-512 falls short of category 1 and that $p$ must be much larger, with the exact size depending on the cost of the quantum oracle (Bernstein, Lange, Martindale and Panny, 2019). Shor's algorithm itself does not apply, because a group action has no group law on the curves.
- **Classical security.** The best classical attack is a meet-in-the-middle or collision search in the class group, about $\sqrt{\#\mathrm{Cl}(\mathcal{O})} \approx p^{1/4}$ steps, so $2^{128}$ for CSIDH-512.
- **Skipped key check.** Without the supersingularity check, an attacker can send an ordinary curve and learn about a static secret from the result. The check is cheap; never skip it with static keys.
- **Timing.** The plain algorithm leaks the exponents through its running time. Use a constant-time form.
- **Equal $A$, not equal $j$.** The shared key is $A$. Curves with $A$ and $-A$ have the same $j$-invariant but are different points of the set, so do not compare by $j$.

## Implementations

## History

Couveignes described Diffie-Hellman on hard homogeneous spaces in 1997, with the class group acting on ordinary curves; his paper appeared on ePrint in 2006. Rostovtsev and Stolbunov proposed a similar scheme independently in 2006. Childs, Jao and Soukharev gave a subexponential quantum attack on it in 2010 (journal version 2014). That attack and the slowness of the ordinary scheme led Jao and De Feo to the non-commutative SIDH in 2011. In 2018, Castryck, Lange, Martindale, Panny and Renes moved the action to supersingular curves over $\mathbb{F}_p$, with $p + 1$ chosen so that all kernels are rational, and called the result CSIDH; it appeared at ASIACRYPT 2018. Beullens, Kleinjung and Vercauteren computed the CSIDH-512 class group in 2019. Peikert and Bonnetain and Schrottenloher published the quantum analyses at EUROCRYPT 2020. CSIDH survived the 2022 attacks on SIDH.

## References
