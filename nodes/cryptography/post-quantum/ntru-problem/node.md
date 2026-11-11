---
tag: C899GW
kind: problem
slug: ntru-problem
name: NTRU problem
aliases:
- NTRU assumption
area: cryptography/post-quantum
level: advanced
summary: Given h = g / f in a polynomial ring mod q, with f and g short, find f and g, or tell h from uniform. The basis of NTRU encryption and of Falcon signatures.
prereqs: [lattice-based-cryptography, polynomial-ring, lll-algorithm]
see_also: [ntru-encrypt, ntru-prime, falcon, unique-svp, bkz-algorithm, ring-learning-with-errors, short-integer-solution, homomorphic-encryption]
sources:
  - paper: "Jeffrey Hoffstein, Jill Pipher and Joseph H. Silverman, NTRU, a ring-based public key cryptosystem, ANTS-III 1998, LNCS 1423"
    locator: the ring Z[X]/(X^N - 1), key generation with the inverses of f mod q and mod p, encryption and decryption, and the lattice attack on the key
  - paper: "Don Coppersmith and Adi Shamir, Lattice attacks on NTRU, EUROCRYPT 1997, LNCS 1233"
    locator: the lattice of dimension 2N that contains the private key, and the effect of the cyclic structure
  - paper: "Damien Stehle and Ron Steinfeld, Making NTRU as secure as worst-case problems over ideal lattices, EUROCRYPT 2011, LNCS 6632"
    locator: the result that h = g / f is statistically close to uniform when f and g are drawn from wide discrete Gaussians over Z[x]/(x^n + 1)
  - paper: "Nick Howgrave-Graham, A hybrid lattice-reduction and meet-in-the-middle attack against NTRU, CRYPTO 2007, LNCS 4622"
    locator: the hybrid attack that reduces part of the NTRU lattice and guesses the rest of the key by a meet-in-the-middle search
  - paper: "Martin Albrecht, Shi Bai and Leo Ducas, A subfield lattice attack on overstretched NTRU assumptions, CRYPTO 2016, LNCS 9814"
    locator: the norm map to a subfield, the smaller NTRU lattice, and the attacks on schemes with a very large modulus
  - paper: "Paul Kirchner and Pierre-Alain Fouque, Revisiting lattice attacks on overstretched NTRU parameters, EUROCRYPT 2017, LNCS 10210"
    locator: the dense sublattice analysis, which shows that plain lattice reduction on the full NTRU lattice works as well as the subfield attack for a large modulus
  - url: "https://falcon-sign.info/"
    title: Pierre-Alain Fouque, Jeffrey Hoffstein, Paul Kirchner, Vadim Lyubashevsky, Thomas Pornin, Thomas Prest, Thomas Ricosset, Gregor Seiler, William Whyte and Zhenfei Zhang, Falcon specification, NIST round 3 submission, 2020
    locator: the NTRU lattice over Z[x]/(x^n + 1) with q = 12289 and the NTRU equation fG - gF = q
---

The NTRU problem asks to recover two short polynomials $f$ and $g$ from their quotient $h = g/f$ in a polynomial ring modulo $q$. Hoffstein, Pipher and Silverman (HPS, 1998) built the NTRU encryption scheme on it, and it is now the hardness basis of [NTRU](/ntru-encrypt/), [NTRU Prime](/ntru-prime/) and the [Falcon](/falcon/) signature (FN-DSA). The key $(f, g)$ is a very short vector in a lattice of dimension $2n$ built from $h$, so the problem is a structured form of the unique shortest vector problem.

**Notation.** $n$ is the degree of the ring, $q$ the large modulus (not a number of queries) and $p$ the small modulus, usually 3. $R = \mathbb{Z}[x]/(\phi)$ with $\phi = x^n - 1$ (HPS) or $x^n + 1$ (Falcon), and $R_q = R/qR$. A polynomial is ternary if its coefficients are in $\{-1, 0, 1\}$. $f_q = f^{-1}$ in $R_q$ and $f_p = f^{-1}$ in $R/pR$. $H$ is the $n \times n$ matrix whose row $i$ holds the coefficients of $x^i h$. $u = 1 + x + \cdots + x^{n-1}$. $\lambda$ is the security parameter.

## In plain words

Pick two secret lists of small numbers, combine them into one long list of large numbers by a division in a special number system, and publish only the result. The problem is to get the two small lists back.

The published list looks random. But the two secret lists are tied to it by a simple rule, and together they form an unusually short arrow in a large grid of points that anyone can build from the public list. Finding that arrow is the attack. For the sizes used in practice, the best grid methods need too much time.

## Definition

Fix $R$, $q$ and a distribution $\mathcal{D}$ on short polynomials (for example ternary with a fixed number of nonzero coefficients). Draw $f, g$ from $\mathcal{D}$, with $f$ invertible in $R_q$, and set

$$h = g \cdot f^{-1} \bmod q.$$

**Search NTRU.** Given $h$, find $(f, g)$. Because $x^i h = (x^i g)/(x^i f)$, any rotation $\pm x^i (f, g)$ is an equally good answer. More generally, any short $(F, G)$ with $F h \equiv G \pmod q$ and $\|(F, G)\|$ close to $\|(f, g)\|$ serves as a key in most schemes.

**Decision NTRU.** Tell $h$ from a uniform element of $R_q$. It is the assumption for public keys of NTRU-based encryption and homomorphic encryption.

**The NTRU lattice.** The lattice

$$\Lambda_h = \{(F, G) \in R^2 : F h \equiv G \pmod q\}$$

has rank $2n$ and the row basis

$$B = \begin{pmatrix} I_n & H \\ 0 & q I_n \end{pmatrix}.$$

Its volume is $q^n$, and $(f, g)$ lies in it: the row combination $f \cdot (I_n \mid H)$ gives $(f, fh)$, and subtracting multiples of the rows $(0, q I_n)$ reduces $fh$ to $g$. Coppersmith and Shamir (1997) used this lattice to attack early NTRU parameters.

## Variants

- **HPS NTRU.** $R = \mathbb{Z}[x]/(x^n - 1)$ with $n$ prime, $q$ a power of 2, $p = 3$, ternary $f$ and $g$. The scheme needs $f$ invertible both mod $q$ and mod $p$. Encryption of a ternary $m$ is $e = r h + m$ for a random ternary $r$ (here the factor $p$ is placed in $h = p f_q g$; HPS put it into the encryption). Decryption computes $a = f e = p\, r g + f m \bmod q$, which is exact over the integers when its coefficients are below $q/2$, and then $m = f_p a \bmod p$.
- **Other rings.** NTRU Prime uses $x^n - x - 1$ with $q$ prime, to avoid the subrings and the factor $x - 1$. Falcon uses $x^n + 1$ with $n = 512$ or $1024$ and $q = 12289$, together with the NTRU equation $f G - g F = q$, which turns $(f, g)$ into a full trapdoor basis of $\Lambda_h$.
- **Gaussian keys.** Stehlé and Steinfeld (2011) take $f$ and $g$ from discrete Gaussians over $x^n + 1$. If the width is about $\sqrt{q}$ times a small factor, $h$ is statistically close to uniform, so decision NTRU holds without any assumption.
- **Overstretched NTRU.** Homomorphic encryption and multilinear map schemes used $q$ far larger than $\|(f, g)\|^2$. This regime is much easier; see the Known algorithms section.

## Examples

**A toy key.** Take $n = 7$, $q = 32$, $p = 3$ and

$$f = -x + x^2 + x^3 + x^5 - x^6, \qquad g = -1 - x + x^4 + x^5.$$

$f$ has three coefficients $+1$ and two $-1$, so $f(1) = 1$. Its inverses are $f_q = 4 + 2x + 26x^2 + 22x^3 + 3x^4 + 23x^5 + 17x^6$ in $R_{32}$ and $f_p = 1 + x + 2x^2$ in $R/3R$. The quotient $g/f$ has coefficients $(27, 19, 30, 24, 28, 12, 20)$, and the HPS public key $h = 3 f_q g$ has coefficients $(17, 25, 26, 8, 20, 4, 28)$. Multiplying $g/f$ by $f$ and taking coefficients in $(-16, 16]$ gives back $(-1, -1, 0, 0, 1, 1, 0)$, which is $g$.

**A short vector that is not a key.** The coefficients of $g/f$ above add up to $160 \equiv 0 \pmod{32}$. In $x^n - 1$, $u \cdot a = a(1)\, u$ for every $a$, and $g(1) = 0$, so $u \cdot (g/f) = 0$. Hence $(u, 0)$, of length $\sqrt{n}$, lies in $\Lambda_h$ and is shorter than $(f, g)$, of length 3 here. An attacker has to skip it, and lattice reduction often mixes it into the short vectors it returns.

**The toy attack.** The Python code with this page generates HPS keys for $n = 11$, $13$ and $17$ with $q = 128$, runs its own LLL on $B$, and looks for a vector of the public key shape among the reduced rows, their pairwise sums and differences, and these plus or minus $(u, 0)$. For these sizes it returns $\pm x^i (f, g)$ for almost every key; on a few keys it finds nothing or another key of the same shape. The search step uses the known key shape, so this is LLL plus a small search, not plain LLL. The code is for study only, is not constant time, and attacks only toy sizes. For real use take a maintained library such as liboqs, or ML-KEM from a FIPS 140 validated module.

## Known algorithms

- **Lattice reduction (primal attack).** $(f, g)$ is an unusually short vector of $\Lambda_h$. The [Gaussian heuristic](/gaussian-heuristic/) predicts a shortest length near $\sqrt{n q/(\pi e)}$ for a random lattice of this rank and volume, while $\|(f, g)\|$ is about $\sqrt{2n \cdot 2/3}$ for ternary keys of density $2/3$. [BKZ](/bkz-algorithm/) with a large enough block size finds it, as in the [unique-SVP](/unique-svp/) attack on LWE; the block size is estimated in the [core-SVP](/core-svp-hardness/) model. For $n = 17$ and $q = 128$ the ratio of the two lengths is about 3.5, small enough for LLL.
- **Rotations.** The $2n$ vectors $\pm x^i (f, g)$ all have the same length, so the attacker can stop at the first of them; this saves at most a factor near $n$.
- **Hybrid attacks.** Howgrave-Graham combined lattice reduction with a meet-in-the-middle search on part of the key; this matters for sparse ternary keys.
- **Overstretched regime.** The rotations of $(f, g)$ span a sublattice of rank $n$ whose volume is about $\|(f, g)\|^n$, much smaller than $q^{n/2}$ when $q$ is large. Albrecht, Bai and Ducas (2016) map $h$ to a subfield with the norm map, which keeps the key short relative to $q$ and gives a smaller lattice, and they broke the parameters of several homomorphic encryption and multilinear map schemes. Kirchner and Fouque (2017) showed that the subfield step is not needed: lattice reduction on the full $\Lambda_h$ finds a vector of the dense sublattice at a block size that falls quickly as $q$ grows, and does at least as well as the subfield attack. For the moduli of NTRU, NTRU Prime and Falcon this effect does not apply.

## Bounds

- **Statistical hardness for wide keys.** For Gaussian $f, g$ of width about $\sqrt{q} \cdot \mathrm{poly}(n)$ over $x^n + 1$, $h$ is statistically close to uniform (Stehlé and Steinfeld 2011), and their NTRU variant is as hard as worst-case problems on ideal lattices through Ring-LWE. Practical schemes use much shorter keys, outside this result.
- **No worst-case reduction** is known for the short ternary keys of practical NTRU. Its security comes from the cost of the attacks above.
- **Uniqueness.** When $\|(f, g)\|$ is well below the Gaussian heuristic, the rotations of $(f, g)$ are the shortest vectors of $\Lambda_h$ apart from vectors such as $(u, 0)$, which come from the factor $x - 1$.

## Reductions

- **To unique-SVP and BDD.** Search NTRU is a unique-SVP instance in $\Lambda_h$, with gap about $\sqrt{nq/(\pi e)} / \|(f, g)\|$.
- **Relation with Ring-LWE.** $h f - g \equiv 0$ is a Ring-LWE sample with secret $f$, error $-g$ and $a = h$, except that $h$ depends on the secret and is not uniform. No reduction between the two is known in either direction for practical parameters.
- **Decision from search.** A key $(F, G)$ that is short tells $h$ from uniform, because a uniform $h$ has no such pair with high probability.

## Applications

- **Encryption.** NTRU and NTRU Prime, both NIST round 3 candidates, are key encapsulation methods based on the NTRU problem; the hybrid sntrup761 key exchange is used in OpenSSH.
- **Signatures.** Falcon (FN-DSA) uses the NTRU lattice over $x^n + 1$ as a trapdoor: the private basis made of $(f, g)$ and $(F, G)$ samples short vectors by the [GPV](/gpv-signature/) method, and forging means finding short $(s_1, s_2)$ with $s_1 + s_2 h \equiv c \pmod q$ for a hashed target $c$, an inhomogeneous SIS problem over $R_q$.
- **Homomorphic encryption.** NTRU-based schemes used decision NTRU with a large modulus; the overstretched attacks broke several of their parameter sets.

## References
