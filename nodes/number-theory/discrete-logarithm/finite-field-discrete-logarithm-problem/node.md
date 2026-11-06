---
tag: JGA7A4
kind: problem
slug: finite-field-discrete-logarithm-problem
name: Discrete logarithm in finite fields
aliases:
- finite field DLP
- DLP in GF(p^n)
- discrete logarithm in GF(q)
area: number-theory/discrete-logarithm
level: advanced
summary: The DLP in the multiplicative group of GF(q), q = p^n. Index calculus beats generic methods; the best cost runs from quasi-polynomial (small p) to L_q[1/3] (large p).
prereqs: [discrete-logarithm-problem, irreducible-polynomial]
see_also: [index-calculus, number-field-sieve-discrete-logarithm, function-field-sieve, coppersmith-discrete-logarithm, quasi-polynomial-discrete-logarithm, menezes-okamoto-vanstone-reduction, subexponential-time, dsa]
sources:
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 15, Section 15.5 (index calculus in prime fields and in fields of small characteristic, Coppersmith's algorithm, and the number field and function field sieves)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 3, Section 3.6 (Definition 3.51 of the generalized problem, Section 3.6.5 on index calculus in Z_p^* and in F_(2^m)^*, Section 3.6.6 on subgroups of Z_p^*)
  - paper: doi:10.1007/bf01840433
    title: Don Coppersmith, Andrew M. Odlyzko and Richard Schroeppel, Discrete logarithms in GF(p), Algorithmica 1, 1986
    locator: pages 1 to 15 (heuristic L_p[1/2, 1] for prime fields)
  - paper: doi:10.1109/TIT.1984.1056941
    title: Don Coppersmith, Fast evaluation of logarithms in fields of characteristic two, IEEE Transactions on Information Theory 30(4), 1984
    locator: pages 587 to 594 (the first L[1/3] algorithm)
  - paper: doi:10.1007/11818175_19
    title: Antoine Joux, Reynald Lercier, Nigel Smart and Frederik Vercauteren, The number field sieve in the medium prime case, CRYPTO 2006, Lecture Notes in Computer Science 4117
    locator: pages 326 to 344 (L[1/3] for all finite fields, and the split into small, medium and large characteristic)
  - paper: doi:10.1007/978-3-642-55220-5_1
    title: Razvan Barbulescu, Pierrick Gaudry, Antoine Joux and Emmanuel Thomé, A heuristic quasi-polynomial algorithm for discrete logarithm in finite fields of small characteristic, EUROCRYPT 2014, Lecture Notes in Computer Science 8441
    locator: pages 1 to 16 (main theorem)
  - paper: doi:10.1090/jams/985
    title: Thorsten Kleinjung and Benjamin Wesolowski, Discrete logarithms in quasi-polynomial time in finite fields of fixed characteristic, Journal of the American Mathematical Society 35, 2022
    locator: pages 581 to 624 (a proved quasi-polynomial bound)
  - paper: doi:10.1007/978-3-030-56880-1_3
    title: Fabrice Boudot, Pierrick Gaudry, Aurore Guillevic, Nadia Heninger, Emmanuel Thomé and Paul Zimmermann, Comparing the difficulty of factorization and discrete logarithm, a 240-digit experiment, CRYPTO 2020, Lecture Notes in Computer Science 12171
    locator: pages 62 to 91 (a 795-bit prime field record)
  - paper: doi:10.1090/mcom/3669
    title: Robert Granger, Thorsten Kleinjung, Arjen K. Lenstra, Benjamin Wesolowski and Jens Zumbrägel, Computation of a 30750-bit binary field discrete logarithm, Mathematics of Computation, 2021
    locator: the main result (a record in GF(2^30750))
---

The discrete logarithm problem in a finite field asks, for a finite field $\mathbb{F}_q$ with $q = p^n$, a generator $g$ of $\mathbb{F}_q^*$ (or of a subgroup) and an element $h$, for an integer $x$ with $g^x = h$. It is the setting of the original [Diffie-Hellman](/diffie-hellman/) key exchange, of [ElGamal](/elgamal-encryption/) and of [DSA](/dsa/). Unlike the elliptic curve case, field elements have a representation that can be factored, so [index calculus](/index-calculus/) methods run in [subexponential time](/subexponential-time/), and the best known cost depends on how $p$ compares with $q$: quasi-polynomial for small characteristic, $L_q[1/3, c]$ for medium and large characteristic.

## In plain words

A finite field is a finite number system where you can add, subtract, multiply and divide, like the numbers modulo a prime. Bigger finite fields are built from polynomials whose coefficients come from a smaller one. The problem is the usual one: given a starting element and a target, find how many times you must multiply the start by itself to reach the target.

Here, unlike on elliptic curves, elements can be split into small pieces: numbers into small primes, polynomials into polynomials of small degree. Attacks collect many elements that split, solve a large system of equations for the logarithms of the pieces, and then split the target. How fast this goes depends on the shape of the field, and fields built from a very small base turned out to be much weaker than once thought.

## Definition

Let $q = p^n$ with $p$ prime. Represent $\mathbb{F}_q$ as $\mathbb{F}_p[t]/(f)$ for an [irreducible polynomial](/irreducible-polynomial/) $f$ of degree $n$; for $n = 1$ this is $\mathbb{Z}/p\mathbb{Z}$. The multiplicative group $\mathbb{F}_q^*$ is cyclic of order $q - 1$.

**Input.** The field (given by $p$ and $f$), an element $g$ of known order $N$, usually a generator ($N = q - 1$) or a generator of a subgroup of prime order $r \mid q - 1$, and an element $h \in \mathbb{F}_q^*$.

**Output.** The least $x \ge 0$ with $g^x = h$, or "no solution". Since $\mathbb{F}_q^*$ is cyclic, $h \in \langle g \rangle$ exactly when $h^N = 1$.

**Cost model.** One field multiplication costs $O(\log^2 q)$ bit operations with schoolbook arithmetic and $\tilde O(\log q)$ with fast arithmetic, and an inversion costs about the same up to a logarithmic factor. Generic algorithms are measured in field multiplications. Index calculus algorithms are measured in bit operations, as a function of $Q = q$, with

$$L_Q[\alpha, c] = \exp\big((c + o(1)) (\ln Q)^{\alpha} (\ln \ln Q)^{1 - \alpha}\big).$$

Almost all subexponential bounds below are heuristic: they assume that the numbers or polynomials that arise are smooth as often as random ones of the same size, and that the linear systems have full rank.

## Variants

The size of $p$ against $q$ decides which algorithm wins. Write $p = L_q[\alpha, c]$:

- **Small characteristic**, $\alpha < 1/3$, for example $\mathbb{F}_{2^n}$ and $\mathbb{F}_{3^n}$. The factor base is polynomials of small degree over $\mathbb{F}_p$ or over a small extension.
- **Medium characteristic**, $1/3 < \alpha < 2/3$. Typical of the fields $\mathbb{F}_{p^k}$ that hold the pairing values of pairing friendly curves.
- **Large characteristic**, $\alpha > 2/3$, including prime fields $\mathbb{F}_p$. The factor bases are rational primes and prime ideals of number fields.
- **Subgroups.** The discrete logarithm in a subgroup of prime order $r$ of $\mathbb{F}_q^*$. Generic methods cost $\sqrt r$, and index calculus works in the whole field at a cost that depends on $q$ only, so both $r$ and $q$ must be large (HAC, Section 3.6.6). DSA uses this with, for example, a $3072$-bit $p$ and a $256$-bit $r$.
- **Many targets.** After a precomputation of the logarithms of the factor base for a fixed field, each new logarithm is much cheaper; this made the reuse of a few standard primes a real weakness.

## Examples

- **A prime field.** In $\mathbb{F}_{23}^*$ with $g = 5$, the logarithm of $h = 14$ is $21$; see the [discrete logarithm problem](/discrete-logarithm-problem/) for the full power table.
- **An extension field.** Let $\mathbb{F}_{16} = \mathbb{F}_2[t]/(t^4 + t + 1)$. The class of $t$ has order $15$, so it generates $\mathbb{F}_{16}^*$. Then $t^{13} = t^3 + t^2 + 1$, $t^{7} = t^3 + t + 1$ and $t^{5} = t^2 + t$, so $\log_t(t^3 + t^2 + 1) = 13$. The elements with logarithms $0, 5, 10$ are $1$, $t^2 + t$ and $t^2 + t + 1$; with $0$ they form the subfield $\mathbb{F}_4$.
- **A subgroup.** In the same field, $t^3$ has order $5$, and $\langle t^3 \rangle = \{1, t^3, t^3 + t^2, t^3 + t, t^3 + t^2 + t + 1\}$. An element outside this set, such as $t$, has no logarithm to the base $t^3$.

## Known algorithms

- **Generic.** [Pohlig-Hellman](/pohlig-hellman/) reduces to the prime factors of $q - 1$, and [baby-step giant-step](/baby-step-giant-step/) or [Pollard's rho](/pollard-rho-discrete-logarithm/) solve each in about $\sqrt r$ multiplications.
- **Basic index calculus.** For prime fields with trial division, $L_p[1/2, 2]$ proved (Galbraith, Exercise 15.5.7); with the sieve of Coppersmith, Odlyzko and Schroeppel, $L_p[1/2, 1]$ heuristic. The same ideas apply to $\mathbb{F}_{2^n}$ with polynomials of small degree as the factor base. See [index calculus](/index-calculus/).
- **Coppersmith (1984).** [Coppersmith's algorithm](/coppersmith-discrete-logarithm/) for $\mathbb{F}_{2^n}$, heuristic $L[1/3, c]$ with $c \le 1.6$, the first $L[1/3]$ algorithm.
- **Number field sieve.** The [NFS for discrete logarithms](/number-field-sieve-discrete-logarithm/), heuristic $L_q[1/3, (64/9)^{1/3}] \approx L_q[1/3, 1.923]$ for large characteristic, and $L_q[1/3, (128/9)^{1/3}]$ for medium characteristic in the variant of Joux, Lercier, Smart and Vercauteren; later variants lower the constants.
- **Function field sieve.** The [function field sieve](/function-field-sieve/), heuristic $L_q[1/3, (32/9)^{1/3}]$ for small characteristic.
- **Quasi-polynomial algorithms.** For small characteristic, Joux (2013) reached $L_q[1/4 + o(1)]$, and Barbulescu, Gaudry, Joux and Thomé (2014) reached heuristic time $(\log q)^{O(\log \log q)}$ ([quasi-polynomial algorithm](/quasi-polynomial-discrete-logarithm/)). Kleinjung and Wesolowski (2022) proved a quasi-polynomial expected time for fields of fixed characteristic.
- **Quantum.** [Shor's algorithm](/quantum-discrete-logarithm/) runs in polynomial time.

## Bounds

No lower bound beyond $\Omega(\log q)$ is known for the finite field DLP, and the generic $\Omega(\sqrt r)$ bound of [Shoup](/shoup-generic-lower-bound/) does not apply, since index calculus is not generic. In small characteristic the problem is quasi-polynomial, which is not polynomial but is far below any $L_q[\alpha]$ with $\alpha > 0$. For prime fields the best known cost is still heuristic $L_p[1/3, 1.923]$, the same as for factoring an integer of the same size by the [general number field sieve](/general-number-field-sieve/). Records include a $795$-bit prime field (Boudot and coauthors, 2020) and the binary field $\mathbb{F}_{2^{30750}}$ (Granger and coauthors).

## Reductions

- **From elliptic curves.** The [MOV](/menezes-okamoto-vanstone-reduction/) and Frey-Rück reductions map the ECDLP for a point of order $r$ into the $r$-th roots of unity of $\mathbb{F}_{q^k}^*$, where $k$ is the embedding degree. So pairing based systems need the finite field DLP in $\mathbb{F}_{q^k}$ to be hard.
- **To subgroups.** Pohlig-Hellman reduces the problem in $\mathbb{F}_q^*$ to its subgroups of prime order.
- **From Diffie-Hellman.** The [computational Diffie-Hellman](/computational-diffie-hellman/) problem in $\mathbb{F}_q^*$ reduces to the DLP; the converse is known only in special cases.
- **To smaller fields.** An element of a subfield $\mathbb{F}_{q'} \subset \mathbb{F}_q$ has a logarithm that can be computed in $\mathbb{F}_{q'}$, and the norm maps $\mathbb{F}_q^*$ onto $\mathbb{F}_{q'}^*$; the descent steps of the quasi-polynomial algorithms use the structure of subfields heavily.

## Applications

- **Key exchange and encryption.** [Diffie-Hellman](/diffie-hellman/) and [ElGamal](/elgamal-encryption/) over $\mathbb{Z}/p\mathbb{Z}$, with standards recommending primes of $2048$ bits or more.
- **Signatures.** [DSA](/dsa/) and [Schnorr signatures](/schnorr-signature/) in a prime order subgroup of $\mathbb{Z}_p^*$.
- **Pairings.** The target groups of pairings are subgroups of $\mathbb{F}_{q^k}^*$; the progress of the number field sieve in medium characteristic after 2015 forced larger parameters for pairing friendly curves.
- **Cautionary tale.** Fields of small characteristic were once proposed for efficiency, and the quasi-polynomial algorithms ruled them out for cryptography.

## References
