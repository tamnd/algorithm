---
tag: BZ6XVD
kind: concept
slug: isogeny-based-cryptography
name: Isogeny-based cryptography
aliases:
- supersingular isogeny cryptography
- isogeny cryptography
area: cryptography/post-quantum
level: advanced
summary: "Cryptography whose hard problem is to find an isogeny, a structure-preserving map, between two elliptic curves, mostly by walks in supersingular isogeny graphs."
prereqs: [post-quantum-cryptography, elliptic-curve-cryptography]
see_also: [supersingular-isogeny-problem, sidh, castryck-decru-attack, csidh, nist-pqc-standardization, elliptic-curve-discrete-logarithm-problem, expander-walk-sampler, shor-algorithm]
sources:
  - paper: doi:10.1007/s00145-007-9002-x
    title: "Denis X. Charles, Eyal Z. Goren and Kristin E. Lauter, Cryptographic hash functions from expander graphs, Journal of Cryptology 22(1), 2009"
    locator: Section 4 (the hash from the supersingular 2-isogeny graph) and Section 5 (collision and preimage resistance as cycle and path finding)
  - paper: "Jacques Velu, Isogenies entre courbes elliptiques, Comptes Rendus de l'Academie des Sciences de Paris, Serie A, 273, 1971, pages 238 to 241"
    locator: the formulas for the isogeny with a given finite kernel
  - book: isbn:9781420071467
    title: "Lawrence C. Washington, Elliptic Curves: Number Theory and Cryptography, second edition, CRC Press, 2008"
    locator: Chapter 12 on isogenies, Theorem 12.16 (Velu's formulas), and the dual isogeny
  - paper: "Arnold K. Pizer, Ramanujan graphs and Hecke operators, Bulletin of the American Mathematical Society 23(1), 1990"
    locator: the result that the supersingular l-isogeny graphs are Ramanujan graphs
  - paper: "David Jao and Luca De Feo, Towards quantum-resistant cryptosystems from supersingular elliptic curve isogenies, PQCrypto 2011, LNCS 7071"
    locator: the SIDH key exchange
  - paper: "Wouter Castryck, Tanja Lange, Chloe Martindale, Lorenz Panny and Joost Renes, CSIDH: an efficient post-quantum commutative group action, ASIACRYPT 2018, LNCS 11274"
    locator: Sections 1 and 3 (the class group action on supersingular curves over F_p)
  - paper: "Luca De Feo, David Kohel, Antonin Leroux, Christophe Petit and Benjamin Wesolowski, SQISign: compact post-quantum signatures from quaternions and isogenies, ASIACRYPT 2020, LNCS 12491"
    locator: Section 1 (the identification protocol and the signature) and the comparison of sizes
  - paper: "Wouter Castryck and Thomas Decru, An efficient key recovery attack on SIDH, EUROCRYPT 2023, LNCS 14008 (IACR ePrint 2022/975)"
    locator: the abstract and Section 1 (the attack with Kani's criterion and the end of SIKE)
  - paper: "Luca De Feo, Mathematics of isogeny based cryptography, lecture notes, arXiv:1711.04062, 2017"
    locator: Sections 2 to 6 (isogenies, Velu's formulas, supersingular curves, isogeny graphs and the protocols)
---

Isogeny-based cryptography builds public-key schemes whose security rests on the difficulty of finding an isogeny, a map between two elliptic curves that respects their group law, when only the two curves are given. The usual setting is the graph of supersingular elliptic curves over $\mathbb{F}_{p^2}$, where each curve is joined to its $\ell$-isogenous neighbours; this graph is an excellent expander, so short random walks reach every curve almost uniformly. The field gave a hash function (Charles, Goren and Lauter, 2009), the key exchange SIDH, which a 2022 attack broke completely, the group action CSIDH, and the signature SQIsign, which is in the third round of NIST's additional signatures process. Its schemes have the smallest keys of all post-quantum families, and they are slower than lattice schemes.

## In plain words

Think of a huge map of cities, where each city is an elliptic curve and each road is a special map between two curves. Every city has the same small number of roads, and the road network is so well connected that a short random trip can end almost anywhere.

Walking a route is easy: from a city, it is cheap to find its neighbours. But if someone shows you a start city and an end city, finding any route between them is believed to be hard, even for a quantum computer.

A secret key is a route, and a public key is the end city. A hash function turns each bit of a message into a choice of road. Key exchange lets two people walk secret routes that end at the same city.

## The idea

**Curves and isogenies.** An elliptic curve over a finite field $\mathbb{F}_q$ is given here in short Weierstrass form $y^2 = x^3 + ax + b$, with a point at infinity as the identity of its group. Two curves are isomorphic over the algebraic closure exactly when they have the same $j$-invariant $j = 1728 \cdot 4a^3/(4a^3 + 27b^2)$. An **isogeny** $\varphi : E \to E'$ is a nonconstant map given by rational functions that sends the identity to the identity; it is then a group homomorphism with a finite kernel. A separable isogeny has degree equal to the size of its kernel, and every isogeny $\varphi$ of degree $d$ has a dual $\hat\varphi : E' \to E$ with $\hat\varphi \circ \varphi = [d]$.

**Velu's formulas.** For every finite subgroup $K \subset E$ there is a separable isogeny with kernel $K$, unique up to an isomorphism of the codomain, and Velu (1971) gave explicit formulas for it, with $O(|K|)$ field operations (see Washington, Theorem 12.16). So an isogeny of small prime degree $\ell$ is cheap if a point of order $\ell$ is known, and an isogeny of degree $\ell^e$ is cheap as a chain of $e$ steps of degree $\ell$. The kernels of the $\ell$-isogenies from $E$ are the $\ell + 1$ cyclic subgroups of order $\ell$ in $E[\ell] \cong (\mathbb{Z}/\ell)^2$, so every curve has $\ell + 1$ outgoing $\ell$-isogenies.

**Supersingular curves and their graph.** A curve over a field of characteristic $p$ is supersingular when it has no point of order $p$ over the algebraic closure. All supersingular $j$-invariants lie in $\mathbb{F}_{p^2}$, and there are about $p/12$ of them (exactly $\lfloor p/12 \rfloor + 2$ when $p \equiv 11 \pmod{12}$). For a prime $\ell \ne p$, the supersingular $\ell$-isogeny graph has these $j$-invariants as vertices and one edge for each $\ell$-isogeny. It is connected, $(\ell+1)$-regular (apart from small irregularities at $j = 0$ and $j = 1728$), and it is a Ramanujan graph (Pizer, 1990): every eigenvalue other than $\ell + 1$ has absolute value at most $2\sqrt{\ell}$. So a random walk of length $O(\log p)$ ends at an almost uniform vertex.

**The hard problem.** Given two supersingular curves $E$ and $E'$, find an isogeny between them, for example as a path in the $\ell$-isogeny graph. This is the [supersingular isogeny problem](/supersingular-isogeny-problem/). The best classical algorithms take time $\tilde O(p^{1/2})$ and the best quantum ones $\tilde O(p^{1/4})$; no polynomial-time quantum algorithm is known, because the problem has no obvious abelian hidden subgroup for [Shor's algorithm](/shor-algorithm/) to find. It is equivalent to computing the endomorphism ring of a supersingular curve.

**The CGL hash.** Charles, Goren and Lauter (2009) proposed the first scheme: start at a fixed curve, and for each message bit take one of the two edges of the 2-isogeny graph that do not go back. The last $j$-invariant is the hash. A collision gives a cycle in the graph, and a preimage gives a path between two given curves, so both are instances of the hard problem. The start curve must have an unknown endomorphism ring: for a start curve such as $j = 1728$, whose endomorphisms are known, Eisentrager, Hallgren, Lauter, Morrison and Petit (2018) showed how to find cycles. Producing a supersingular curve with no known endomorphism ring, without a trusted setup, is still an open problem.

**The main schemes.**

| scheme | year | idea | status |
|---|---|---|---|
| CRS (Couveignes; Rostovtsev and Stolbunov) | 1997, 2006 | class group action on ordinary curves | slow; subexponential quantum attack (Childs, Jao and Soukharev, 2014) |
| CGL hash | 2009 | walk in the supersingular 2-isogeny graph | secure only with a start curve of unknown endomorphism ring |
| [SIDH](/sidh/) and SIKE | 2011 | secret walks of degree $2^{e_A}$ and $3^{e_B}$, with images of torsion points | broken in polynomial time in 2022 by the [Castryck-Decru attack](/castryck-decru-attack/) |
| [CSIDH](/csidh/) | 2018 | commutative class group action on supersingular curves over $\mathbb{F}_p$ | unbroken; quantum subexponential attack forces large $p$ |
| SQIsign | 2020 | signature from the correspondence between curves and quaternion orders | in round 3 of the NIST additional signatures process |

**After 2022.** The attack on SIDH used Kani's theorem to embed an isogeny between elliptic curves into an isogeny between products of curves, of dimension 2 or more. Robert showed that this gives an efficient representation of any isogeny of known degree. This turned an attack into a tool: SQIsignHD (Dartois, Leroux, Robert and Wesolowski, 2024) and the "2D" versions of SQIsign, on which the round 2 submission is built, use higher-dimensional isogenies to make signing much faster and simpler. Schemes that publish images of torsion points under a secret isogeny, as SIDH did, are now designed with masked torsion or not at all.

## Examples

**A toy supersingular 2-isogeny graph.** The code with this page takes $p = 431$, starts from $E_0 : y^2 = x^3 + x$ with $j = 1728 \equiv 4 \pmod{431}$, and finds every 2-isogenous neighbour with Velu's formulas, breadth first. It finds $\lfloor 431/12 \rfloor + 2 = 37$ supersingular $j$-invariants: 21 in $\mathbb{F}_{431}$ and 16 in $\mathbb{F}_{431^2} \setminus \mathbb{F}_{431}$. Each edge $(j, j')$ satisfies the modular polynomial $\Phi_2(j, j') = 0$, which the code checks.

- From $j = 4$ (that is, 1728) the three 2-isogenies go to $19$, $19$ and $4$ itself. The loop is the isogeny with kernel $\langle(0,0)\rangle$: Velu's formulas give $y^2 = x^3 - 4x$, which again has $j = 1728$.
- From $j = 0$ all three 2-isogenies go to $125$.
- From $j = 19$ they go to $4$, $234$ and $241$.

**A CGL walk.** Start at $j = 19$, as if the walk came from $j = 4$. At each step, drop the edge back, sort the two other neighbours by their representation $a + 431b$ of $a + bi$, and take the first for bit 0 and the second for bit 1. The message 1011001 gives:

| step | bit | forward choices | next $j$ |
|---|---|---|---|
| 1 | 1 | 234, 241 | 241 |
| 2 | 0 | $118+209i$, $118+222i$ | $118+209i$ |
| 3 | 1 | $65+81i$, $315+299i$ | $315+299i$ |
| 4 | 1 | 381, $426+125i$ | $426+125i$ |
| 5 | 0 | $141+42i$, $379+325i$ | $141+42i$ |
| 6 | 0 | 419, $65+81i$ | 419 |
| 7 | 1 | 422, $141+389i$ | $141+389i$ |

So the hash of 1011001 is $141 + 389i$. Changing only the last bit gives 422, and the message 0011001 also gives 422, a collision. With 37 vertices collisions are certain; this toy shows only the mechanism. In the test, random 16-bit messages reach all 37 vertices, which shows the fast mixing. Real proposals need $p$ of 256 bits or more, and a start curve with unknown endomorphism ring. The code is for study only and not constant time; use SHA-2 or SHA-3 from a standard library to hash.

**Key sizes.** SIKEp434 had a public key of 330 bytes (197 compressed) and CSIDH-512 a public key of 64 bytes, far smaller than lattice KEMs, but each operation took tens of milliseconds where ML-KEM takes tens of microseconds.

## Where it is used

- **Research and the NIST signature process.** SQIsign is the only isogeny scheme in round 3 of NIST's additional signatures (NIST IR 8610). Its main asset is that its public key plus signature is the smallest of all post-quantum signatures, a few hundred bytes.
- **Non-interactive key exchange.** [CSIDH](/csidh/) is the main post-quantum candidate for a key exchange in which both parties publish a key once and never interact, like static Diffie-Hellman.
- **A lesson in cryptanalysis.** SIKE was a NIST round 4 candidate, studied for over ten years, when the Castryck-Decru attack broke it in 2022 with mathematics from 1997 (Kani). See [NIST post-quantum standardization](/nist-pqc-standardization/).
- **Number theory tools.** Computing endomorphism rings, isogenies of large degree and higher-dimensional isogenies are now active research areas because of these schemes.

## References
