---
tag: TNJ165
kind: algorithm
slug: wiener-attack
name: Wiener's attack
aliases:
- small private exponent attack
area: cryptography/public-key
level: advanced
summary: If the RSA private exponent is below N^(1/4)/3, then k/d is a continued fraction convergent of e/N, so about log N tries recover d and factor the modulus.
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {b: the number of binary digits of the modulus}
  time: {worst: Θ(b^3), average: Θ(b^3), best: Θ(b^2)}
  space: {extra: Θ(b)}
properties: {deterministic: true, randomized: false}
history:
  year: 1990
  people: [Michael J. Wiener, Dan Boneh, Glenn Durfee]
  note: Wiener published the continued fraction attack in the IEEE Transactions on Information Theory in 1990. Boneh and Durfee raised the bound to d below N^0.292 with a lattice method in 1999.
prereqs: [rsa-cryptosystem, continued-fraction-convergents]
see_also: [rsa-problem, integer-factorization, coppersmith-method, lll-algorithm, continued-fraction, rsa-signature, rsa-blinding]
sources:
  - paper: "Michael J. Wiener, Cryptanalysis of short RSA secret exponents, IEEE Transactions on Information Theory 36(3), pages 553 to 558, 1990"
    locator: Sections 2 and 3 (the continued fraction method, the bound d < N^(1/4)/3, and the countermeasures with a large public exponent)
  - paper: "Dan Boneh and Glenn Durfee, Cryptanalysis of RSA with private key d less than N^0.292, EUROCRYPT 1999, LNCS 1592, pages 1 to 11"
    locator: Sections 1 and 4 (the lattice formulation of the small inverse problem and the bound N^0.292)
  - url: "https://www.ams.org/notices/199902/boneh.pdf"
    title: Dan Boneh, Twenty years of attacks on the RSA cryptosystem, Notices of the AMS 46(2), pages 203 to 213, 1999
    locator: Section 3 (low private exponent, with the statement of Wiener's theorem and the remark that the attack is no threat when e is large)
  - book: isbn:9780486696300
    title: A. Ya. Khinchin, Continued Fractions, Dover edition
    locator: Chapter II (best approximations and Legendre's criterion, which is the step that turns the bound into the list of candidates)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 8, Section 8.2.2 (the note on small decryption exponents and why d must be large)
  - url: "https://www.rfc-editor.org/rfc/rfc8017"
    title: "Kathleen Moriarty, Burt Kaliski, Jakob Jonsson and Andreas Rusch, RFC 8017, PKCS #1, RSA Cryptography Specifications Version 2.2, 2016"
    locator: Section 3.2 (the private key, where d is the full size value that this attack cannot reach)
---

Wiener's attack recovers an RSA private exponent that was made small to speed up decryption. The relation $ed = 1 + k\varphi(N)$ makes the unknown fraction $k/d$ an extremely good approximation of the public $e/N$, and Legendre's criterion says that an approximation that good must be one of the [continued fraction convergents](/continued-fraction-convergents/) of $e/N$. There are only about $\log_2 N$ of those, so the attacker lists them, and each one is tested with two multiplications and one square root. If $q < p < 2q$ and

$$d < \frac{N^{1/4}}{3} ,$$

the attack always succeeds. It is the reason no implementation chooses $d$ first; the standard choice is a small *public* exponent, $e = 65537$, which leaves $d$ of full size.

**Notation.** $N = pq$ with primes $p > q$, $\varphi(N) = (p-1)(q-1)$, $e$ the public exponent, $d$ the private exponent with $ed \equiv 1 \pmod{\varphi(N)}$, and $k = (ed - 1)/\varphi(N)$ the integer that the congruence hides. The convergents of $e/N$ are written $h_i/k_i$.

## In plain words

RSA decryption raises a number to the power of the private exponent, so a short exponent means a fast decryption. The saving is tempting, and it is fatal.

The private exponent is tied to the public one by an equation with two unknowns, and the ratio of those unknowns is very close to the ratio of two public numbers. A classic result about continued fractions says that a fraction which approximates a number that well cannot hide: it must appear in the short list of best approximations, which for a normal key has a few hundred entries.

So the attacker writes out the list and tests each entry with a check that only the right one passes. The whole attack is faster than one decryption. Make the public exponent small instead; then the private exponent is large and this attack cannot start.

## The problem

The input is a public key $(N, e)$ alone. The output is the factorization of $N$ and the private exponent $d$, so the attack [factors the modulus](/integer-factorization/) for this one weak key shape. The promise is that $d$ is small: the attack is correct for every key with $q < p < 2q$ and $d < N^{1/4}/3$, and it reports failure, never a wrong answer, when the promise does not hold.

The attacker does not get a ciphertext, a plaintext, an oracle or a signature. This is the strongest kind of attack there is, a key-only attack, and that is what makes small private exponents unusable rather than merely risky.

## The algorithm

```pseudo id=main
WIENER-ATTACK(N, e)
L1  a ← the continued fraction expansion of e / N
L2  for each convergent k / d of a, in order, do
L3      if k = 0 or d is even then continue              ▷ d is odd, k ≥ 1
L4      if (e*d - 1) mod k ≠ 0 then continue             ▷ k must divide ed - 1
L5      f ← (e*d - 1) / k                                ▷ the guess for φ(N)
L6      s ← N - f + 1                                    ▷ the guess for p + q
L7      if s < 0 or s is odd then continue
L8      D ← s*s - 4N                                     ▷ the guess for (p - q)^2
L9      if D is not a perfect square then continue
L10     p ← (s + sqrt(D)) / 2; q ← (s - sqrt(D)) / 2
L11     if p*q = N then return (p, q, d)                 ▷ the only test that can pass by luck
L12 return FAILURE
```

**The walk-through.** Line 1 runs [Euclid's algorithm](/extended-euclidean-algorithm/) on the pair $(e, N)$ and keeps the quotients; this is the continued fraction expansion of $e/N$, and it has $O(\log N)$ terms. Line 2 builds the convergents from the quotients with the usual recurrences $h_i = a_i h_{i-1} + h_{i-2}$ and $k_i = a_i k_{i-1} + k_{i-2}$; each pair is already in lowest terms, which matters because $\gcd(k, d) = 1$ holds for the true pair.

Lines 3 to 11 are the test of one candidate. Take the convergent as a guess $k/d$ for the true $k/d$. Then line 5 inverts $ed = 1 + k\varphi(N)$ to guess $\varphi(N)$. Line 6 uses $N - \varphi(N) = p + q - 1$, so the guess for the sum of the primes is $N - \varphi + 1$. Now $p$ and $q$ are the two roots of

$$x^2 - (p+q)x + pq = 0 ,$$

so line 8 forms the discriminant $(p+q)^2 - 4N = (p-q)^2$, line 9 asks whether it is a perfect square, and line 10 takes the two roots. Line 11 is the check that makes the whole attack sound: a wrong guess almost never gives a factorization of $N$, and if it does, the factorization is still correct and the attack still wins. The small filters in lines 3, 4, 7 and 9 exist only to make the loop fast; dropping them would leave the result unchanged.

The exact integer square root of line 9 is the only operation that is not a multiplication or a division. Use an integer routine, never a floating point square root: for a modulus of 2048 binary digits a double has 53 significant binary digits and will answer nonsense.

## Example

A key small enough to follow: $p = 239$, $q = 379$, so $N = 90581$ and $\varphi(N) = 238 \cdot 378 = 89964$. Choose $d = 5$. Then $e = 5^{-1} \bmod 89964 = 17993$, and indeed $5 \cdot 17993 = 89965 = 1 + 1 \cdot 89964$, so $k = 1$.

The expansion of $e/N = 17993/90581$ starts $[0; 5, 29, 4, 1, 3, \ldots]$, and its first convergents are

$$\frac{0}{1}, \quad \frac{1}{5}, \quad \frac{29}{146}, \quad \frac{117}{589}, \ldots$$

The first candidate has $k = 0$ and line 3 drops it. The second is $k/d = 1/5$, the true pair. The loop then computes $f = (17993 \cdot 5 - 1)/1 = 89964$, $s = 90581 - 89964 + 1 = 618 = p + q$, $D = 618^2 - 4 \cdot 90581 = 381924 - 362324 = 19600 = 140^2$, and the roots $(618 \pm 140)/2$, that is $379$ and $239$. Their product is $90581 = N$, so line 11 returns. Here $d = 5$ is below $N^{1/4}/3 \approx 5.78$ and $239 < 379 < 2 \cdot 239$, so the key meets the hypothesis of the theorem.

A toy key of realistic shape, from the test file. The primes have 128 binary digits each,

$$p = 273864138845241657029075268143536711069, \qquad q = 173710947069375085680776429514357002701,$$

with $q < p < 2q$ and $N$ of 255 binary digits. The generator draws a private exponent below the bound $\lfloor N^{1/4}/3 \rfloor = 4922880958527498657$ and inverts it, which gives

$$d = 3957778989932399297 \quad (62 \text{ binary digits}), \qquad k = 3830882568331697983 .$$

The expansion of $e/N$ has 150 partial quotients, and the true pair is convergent number 41. The attack finds it in a few milliseconds and returns both primes. The test file repeats this for ten random weak exponents, does the same with a 511 binary digit modulus and a private exponent of 126 binary digits, and checks that the same key with $e = 65537$, where $d$ has the full 255 binary digits, gives FAILURE.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It has three parts.

1. *Soundness.* If the attack returns $(p, q, d)$, then $pq = N$ by line 11, and $d$ satisfies $ed \equiv 1 \pmod{\varphi(N)}$ for the true $\varphi(N)$, because line 5 and line 11 together force $f = \varphi(N)$. So a returned answer is always right, whatever the key.
2. *Completeness.* If $q < p < 2q$ and $d < N^{1/4}/3$, then $|e/N - k/d| < 1/(2d^2)$, and Legendre's criterion makes $k/d$ one of the convergents, so the loop reaches it.
3. *The inequality.* From $ed - k\varphi(N) = 1$,

$$\left| \frac{e}{N} - \frac{k}{d} \right| = \frac{|ed - kN|}{Nd} = \frac{|1 - k(N - \varphi(N))|}{Nd} < \frac{k(p + q)}{Nd} < \frac{3k\sqrt{N}}{Nd} = \frac{3k}{d\sqrt{N}} ,$$

using $N - \varphi(N) = p + q - 1$ and $p + q < 3\sqrt{N}$, which is where $p < 2q$ is needed. Then $k < d$ and $d < N^{1/4}/3$ give $6kd < 6d^2 < \tfrac{2}{3}\sqrt{N} < \sqrt{N}$, which rearranges to $3k/(d\sqrt{N}) < 1/(2d^2)$.

## Complexity

Let $b$ be the number of binary digits of $N$, with schoolbook arithmetic.

| step | count | cost each | total |
|---|---|---|---|
| continued fraction expansion (line 1) | $O(b)$ divisions | $O(b^2)$ in total for Euclid | $\Theta(b^2)$ |
| convergents (line 2) | $O(b)$ | $\Theta(b)$ additions and one short multiplication | $O(b^2)$ |
| candidate test (lines 4 to 11) | $O(b)$ | $\Theta(b^2)$, the integer square root included | $\Theta(b^3)$ |

So the attack is $\Theta(b^3)$, which is the cost of a single RSA decryption, and for $b = 2048$ it is milliseconds. The space is one convergent and a few temporaries, $\Theta(b)$. The best case is $\Theta(b^2)$: the true pair can be the first convergent, as it nearly is in the example above.

The number of candidates is at most the number of partial quotients, which is $O(\log N)$ and on average about $0.72 \log_2 N$ for a random pair, by the Gauss-Kuzmin law. For the 255 binary digit example it is 150.

## Properties

- **Key only.** The attack needs the public key and nothing else. No ciphertext, no oracle, no timing.
- **Never wrong.** Line 11 is a complete test, so the attack returns either a true factorization or FAILURE.
- **Sharp in practice, not in theory.** The bound $N^{1/4}/3$ is what the proof gives. Keys with larger $d$ often fall as well, because the proof is loose in several places, and keys slightly above the bound can be caught by searching the neighbours of each convergent. Treat $N^{1/4}$ as a wall with an unknown thickness, not as a safe line.
- **The ratio hypothesis matters for the proof, not much for the attack.** The step $p + q < 3\sqrt{N}$ uses $q < p < 2q$. Primes of equal length, as every standard generator produces, satisfy it with room to spare.
- **It does not touch small public exponents.** With $e = 3$ or $e = 65537$ the private exponent is of the order of $N$, and $e/N$ has nothing to say about it. Small $e$ has its own attacks, such as the broadcast attack and [Coppersmith's method](/coppersmith-method/), and they are of a different kind.
- **It does not touch small CRT exponents directly.** A key with small $d_p$ and $d_q$ but a full size $d$ is not open to this attack; it is open to the lattice attacks of Jochemsz and May, which reach $d_p, d_q$ below about $N^{0.073}$.

## Variants and improvements

- **Boneh and Durfee (1999).** Rewrite the problem as a small inverse problem, $k(N + 1 - s) \equiv 1 \pmod e$ with the unknowns $k$ and $s = p + q$, and solve it with [Coppersmith's method](/coppersmith-method/) over a lattice reduced by [LLL](/lll-algorithm/). This reaches $d < N^{0.292}$, a real improvement over $N^{0.25}$, and it is still the record. The lattice is of dimension about 30 for useful parameters, and the analysis needs a geometrically progressive matrix argument.
- **Better continued fraction targets.** Approximating $e/(N + 1 - 2\lceil\sqrt{N}\rceil)$ instead of $e/N$ removes most of the slack in the step $p + q < 3\sqrt{N}$, and raises the reachable range by a constant factor. Dujella and others give families of extensions that search a window around each convergent.
- **Partial key exposure.** Boneh, Durfee and Frankel (1998) showed that a quarter of the bits of $d$, when $e$ is small, is enough to recover the rest with Coppersmith's method. The same lattice machinery covers partially known $p$ and partially known $d_p$.
- **Wiener's own countermeasure.** His paper notes that adding a multiple of $\varphi(N)$ to $d$, or using a large $e$, breaks the approximation. Both work: the attack needs $e < \varphi(N)$ and a small $d$ at the same time.
- **Other cryptosystems with the same shape.** Any scheme with a public relation $ed \equiv 1$ modulo a hidden value has a continued fraction attack on the small secret: this covers Rabin-like variants, the KMOV and LUC systems, and some RSA variants over elliptic curves.

## When to use it

As a check on a key you did not generate. Keys with a tiny private exponent appear in embedded devices that wanted fast decryption, in homework code, in capture-the-flag puzzles and in the odd library bug. The attack costs milliseconds, so a key audit can simply run it on every key it sees, together with a [batch gcd](/batch-gcd/) over the whole collection and a check that the exponents are standard.

As a design rule, the lesson is settled: choose $e$ small and fixed, let $d$ be whatever falls out, and never pick $d$ first. If decryption speed is the problem, use the [CRT](/chinese-remainder-theorem/) form of the private key, which is about four times faster and gives up nothing, or move to a scheme whose private operation is cheap by design.

## Pitfalls

- **Floating point square roots.** Line 9 needs an exact integer square root. A `sqrt` on a double fails above $2^{53}$ and will silently reject the right candidate.
- **Testing only the denominators.** Both parts of the convergent are used: $k$ divides $ed - 1$, and $d$ is the exponent. An implementation that forgets the $k = 0$ convergent, or that uses $h_i$ and $k_i$ the wrong way round, finds nothing.
- **Convergents of $N/e$ instead of $e/N$.** The approximation is of $e/N$ by $k/d$. Inverting the fraction inverts the roles of $k$ and $d$ and the filters then reject everything.
- **Assuming the bound is a safety line.** $d > N^{1/4}$ is not a safe condition. The safe condition is $d > N^{0.292}$ from the lattice attacks, with a margin, and the simple way to get it is a small public exponent.
- **Using $\lambda(N)$ when the proof uses $\varphi(N)$.** With $ed \equiv 1 \pmod{\lambda(N)}$ the value $f$ of line 5 is a multiple of $\lambda(N)$ that need not be $\varphi(N)$, so line 6 can fail even for a small $d$. A practical attack therefore tries $f, 2f, 3f$ and so on for the first few multiples, or works with $\gcd(p-1, q-1)$ small, which holds for random primes.
- **Reading the attack as a break of RSA.** It is a break of a key generation choice. RFC 8017 keys with $e = 65537$ are not affected at all.

**The code of this page is for study only.** It is not constant time, and the keys it attacks are toy keys built inside the test file for that purpose.

## Implementations

## History

Michael Wiener, then at Bell-Northern Research, published "Cryptanalysis of short RSA secret exponents" in the IEEE Transactions on Information Theory in May 1990. The paper came out of a practical question: RSA decryption was slow on the hardware of the day, and choosing a short secret exponent was an obvious saving that several people had proposed. Wiener showed that the saving costs the key, gave the bound $N^{1/4}/3$, and also described a special purpose hardware search for exponents a little above it.

The result closed that design door for good and opened a line of work on how small $d$ may be. In 1998 Boneh, Durfee and Frankel gave the first partial key exposure attacks. In 1999 Boneh and Durfee reached $d < N^{0.292}$ by turning the problem into a bivariate modular equation and applying the lattice method that Coppersmith had developed in 1996; Blömer and May, and later Herrmann and May, simplified and extended the analysis, and the exponent $0.292$ has stood since. Whether the true boundary is $N^{0.5}$, which is the value at which the problem has many solutions and so cannot be solved by this route, is open.

Wiener's attack also became the standard first example of a lattice-free cryptanalysis built on a classical tool: the continued fraction algorithm is older than public-key cryptography by two centuries, and it breaks a modern key in milliseconds.

## References
