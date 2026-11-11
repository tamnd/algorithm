---
tag: KGXAH6
kind: definition
slug: trapdoor-one-way-function
name: Trapdoor one-way function
aliases:
- trapdoor function
- trapdoor permutation
area: cryptography/public-key
level: core
summary: A family of one-way functions, each with a secret that inverts it. It is what public-key encryption needs, and no black box construction gets one from a plain one-way function.
prereqs: [one-way-function]
see_also: [public-key-encryption, rsa-problem, rabin-cryptosystem, hard-core-predicate, computational-hardness-assumption, key-encapsulation-mechanism, public-key-cryptography]
sources:
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Section 2.4.4 (the definition of a collection of trapdoor one way permutations, with the RSA and Rabin candidates as Examples)
  - paper: "Whitfield Diffie and Martin E. Hellman, New directions in cryptography, IEEE Transactions on Information Theory 22(6), pages 644 to 654, November 1976"
    locator: Section III, the part on trap doors (the object is asked for by name, with no construction given)
  - paper: "Andrew C. Yao, Theory and application of trapdoor functions, 23rd Annual Symposium on Foundations of Computer Science (FOCS), pages 80 to 91, 1982"
    locator: Sections 2 to 4 (the formal treatment of trapdoor functions, computational entropy, and the use of a hard core digit for encryption)
  - paper: doi:10.1145/73007.73012
    title: Russell Impagliazzo and Steven Rudich, Limits on the provable consequences of one-way permutations, Proceedings of the 21st ACM Symposium on Theory of Computing, STOC 1989, pages 44 to 61, 1989
    locator: Sections 1 and 2 (the black box separation, which rules out a construction of key agreement, and therefore of a trapdoor permutation, from a one way permutation alone)
  - url: "https://doi.org/10.1145/359340.359342"
    title: Ronald L. Rivest, Adi Shamir and Leonard Adleman, A method for obtaining digital signatures and public-key cryptosystems, Communications of the ACM 21(2), pages 120 to 126, 1978
    locator: Sections 1 and 2 (the first published candidate, with the factorization as the trapdoor)
  - url: "http://publications.csail.mit.edu/lcs/pubs/pdf/MIT-LCS-TR-212.pdf"
    title: Michael O. Rabin, Digitalized signatures and public-key functions as intractable as factorization, MIT/LCS/TR-212, MIT Laboratory for Computer Science, January 1979
    locator: Sections 1 and 2 (squaring modulo a Blum integer as a trapdoor permutation of the quadratic residues, with the equivalence to factoring)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2021
    locator: the chapters on public-key encryption and on theoretical constructions (the definition, and encryption from a trapdoor permutation with a hard core predicate)
---

A trapdoor one way function is a [one way function](/one-way-function/) that comes with a secret, the *trapdoor*, which makes inversion easy. The pair is generated together: the index of the function is the public key, and the trapdoor is the private key. This is the exact object that [public-key encryption](/public-key-encryption/) and signatures need, and it is the object Diffie and Hellman asked for in 1976 and could not supply. [RSA](/rsa-cryptosystem/) and [Rabin](/rabin-cryptosystem/) are the two classical candidates. The gap between a one way function and a trapdoor one is real and not just a matter of effort: Impagliazzo and Rudich proved in 1989 that no black box construction bridges it.

**Notation.** $n$ is the security parameter, $i$ an index (the public key), $t$ a trapdoor (the private key), $D_i$ the domain of the function with index $i$, $f_i : D_i \to R_i$ the function, and $\mathrm{negl}(n)$ a negligible function. "Efficient" means probabilistic polynomial time in $n$.

## Definition

**A collection of trapdoor one way functions** is a tuple of four efficient algorithms $(\mathrm{Gen}, \mathrm{Samp}, \mathrm{Eval}, \mathrm{Invert})$:

- $\mathrm{Gen}(1^n) \to (i, t)$, randomized, outputs an index and its trapdoor;
- $\mathrm{Samp}(i) \to x$, randomized, outputs an element of the domain $D_i$;
- $\mathrm{Eval}(i, x) = f_i(x)$, deterministic;
- $\mathrm{Invert}(t, y) \to x$, deterministic, with $f_i(x) = y$ for every $y$ in the range.

The requirements are

1. **Correctness of the trapdoor.** For every $(i, t)$ from $\mathrm{Gen}(1^n)$ and every $x \in D_i$, $\mathrm{Invert}(t, f_i(x)) \in f_i^{-1}(f_i(x))$.
2. **One wayness without the trapdoor.** For every efficient $\mathcal{A}$,

$$\Pr\left[(i, t) \leftarrow \mathrm{Gen}(1^n),\ x \leftarrow \mathrm{Samp}(i),\ x' \leftarrow \mathcal{A}(i, f_i(x)) \ : \ f_i(x') = f_i(x) \right] \le \mathrm{negl}(n) .$$

The adversary gets the index $i$ and not the trapdoor $t$. This is the whole content of the definition: the *same* public information that lets anybody evaluate the function must not let anybody invert it.

**A collection of trapdoor one way permutations** is the case where each $f_i$ is a bijection of $D_i$ onto itself and $\mathrm{Samp}(i)$ is uniform on $D_i$. Then preimages are unique, inversion is well defined, and a uniform input gives a uniform output. This is the version almost all theory uses, because the uniformity removes a pile of technical conditions.

**What the definition does not say.** Three refinements matter in use and are the source of most of the errors in this area.

- **Certification.** Nothing in the definition says that a *claimed* index really describes a permutation. An adversary who supplies the public key may supply an index for which $f_i$ is not injective, and a protocol that assumed injectivity breaks. For RSA with an index $(N, e)$, the map is a permutation exactly when $\gcd(e, \varphi(N)) = 1$, which the verifier cannot check without the factorization. A *certified* collection is one where the verifier can check the index. In practice one restricts the shape of the key, proves the property in zero knowledge, or arranges that the protocol does not need injectivity.
- **Enhanced hardness.** $\mathrm{Samp}(i)$ uses random coins $r$, and an adversary that sees $r$ knows a great deal about $x$. A collection is *enhanced* when inversion stays hard even given those coins. The plain definition is not enough for oblivious transfer and for non-interactive zero knowledge; Goldreich isolates the enhanced and doubly enhanced versions for exactly this reason. For RSA and Rabin the sampler is "pick a uniform element", so the coins are the element and the enhanced property holds trivially.
- **The domain must be samplable and recognizable.** For Rabin the natural domain is the quadratic residues modulo $N$, which nobody can recognize without the factorization. One repairs this by taking the domain to be $\mathbb{Z}_N^*$ and the function to be squaring, which is then four to one rather than a permutation, or by taking the domain to be the squares and sampling by squaring a uniform element.

**The relation to one way functions.** A trapdoor collection is in particular a collection of one way functions, so the existence of one implies the existence of the other. The converse is where the field divides.

**Theorem (Impagliazzo and Rudich, 1989).** There is no black box construction of a key agreement protocol from a one way permutation. More precisely, relative to a random permutation oracle, every two party key agreement protocol can be broken by an adversary with access to the same oracle and the power to invert on a polynomial number of points, so a proof that key agreement follows from one way permutations must use the *code* of the permutation and not only its input and output behaviour.

Since a trapdoor permutation gives key agreement at once, the theorem rules out black box constructions of trapdoor permutations from one way permutations. This is the formal boundary between Impagliazzo's worlds Minicrypt, where one way functions exist and public-key cryptography does not, and Cryptomania, where it does. Every candidate trapdoor function known today comes from number theory, from lattices or from codes, and not from a generic construction.

## Examples and non-examples

**RSA.** $\mathrm{Gen}(1^n)$ draws primes $p, q$ of $n/2$ binary digits, sets $N = pq$, picks $e$ with $\gcd(e, \varphi(N)) = 1$, and computes $d = e^{-1} \bmod \varphi(N)$. The index is $(N, e)$, the trapdoor is $d$ or the pair $(p, q)$, the domain is $\mathbb{Z}_N^*$, and

$$f_{N,e}(x) = x^e \bmod N, \qquad f^{-1}(y) = y^d \bmod N .$$

This is a permutation of $\mathbb{Z}_N^*$ and in fact of all of $\mathbb{Z}_N$. One wayness is the [RSA assumption](/rsa-problem/), which is implied by the hardness of factoring and not known to be equivalent to it. The trapdoor is not unique: $d$ modulo $\lambda(N)$ works, and so does the factorization, which also gives the four times faster [CRT](/chinese-remainder-theorem/) inversion.

**Rabin.** $\mathrm{Gen}$ draws $p \equiv q \equiv 3 \pmod 4$ and publishes $N = pq$; the trapdoor is $(p, q)$ and the function is $f_N(x) = x^2 \bmod N$. On $\mathbb{Z}_N^*$ it is four to one, and on the quadratic residues it is a *permutation*, because $-1$ is a non-residue modulo each prime. Its one wayness is *equivalent* to factoring, which no other classical candidate can claim; see [Rabin](/rabin-cryptosystem/) and the proof on that page. This is the standard trapdoor permutation of the theory literature.

**Paillier and the residuosity family.** $f(x, r) = (1 + N)^x r^N \bmod N^2$ with the trapdoor $\lambda(N)$. It is a bijection from $\mathbb{Z}_N \times \mathbb{Z}_N^*$ to $\mathbb{Z}_{N^2}^*$, so it is a trapdoor permutation in the loose sense and additively homomorphic; see [Paillier](/paillier-cryptosystem/).

**Lattice trapdoors.** $f_A(x) = Ax \bmod q$ for a wide matrix $A$, with a short basis of the lattice as the trapdoor. This is *not* a permutation. It is a surjective, many to one trapdoor function with a *preimage sampler*: the trapdoor does not invert the function but samples a short preimage from the right distribution. The change of definition is substantial and it is the one the post-quantum signature schemes use; see [short integer solution](/short-integer-solution/) and [ML-DSA](/crystals-dilithium/).

**McEliece.** $f(m, e) = mG' + e$ for a scrambled generator matrix $G'$ and a low weight error $e$, with the scrambling as the trapdoor. A trapdoor function, not a permutation, and the index cannot be certified: nobody can tell a scrambled Goppa code from a random code, which is the assumption, and that means nobody can check that a claimed public key is a valid one. See [McEliece](/mceliece-cryptosystem/).

**Non-examples.**

- **Modular exponentiation.** $f_{p,g}(x) = g^x \bmod p$ is a one way permutation candidate with *no trapdoor at all*: knowing $p$ and $g$ better than anybody else does not help, because there is no secret to know. The discrete logarithm family builds public-key cryptography by a different route, through the commuting structure of [Diffie-Hellman](/diffie-hellman/), and [ElGamal](/elgamal-encryption/) is not an instance of the trapdoor paradigm.
- **A cryptographic hash function.** $\mathrm{SHA\text{-}256}$ is a fine one way candidate and compresses, so it has no inverse, let alone a trapdoor.
- **A function with a public trapdoor.** If the trapdoor is computable from the index in polynomial time, condition 2 fails. This is what the attacks do: [Wiener's attack](/wiener-attack/) computes $d$ from $(N, e)$ when $d$ is small, which turns the RSA collection into a non-example for that part of the key space.
- **The Merkle-Hellman knapsack.** It has the right shape, an easy instance hidden behind a disguise, and the disguise does not hold. See [Merkle-Hellman](/merkle-hellman-knapsack-cryptosystem/) for the two attacks. A trapdoor is an assumption about the *sampler*, and that is what failed.
- **A permutation whose trapdoor inverts only some of the range.** The definition asks for inversion on every image. A partial trapdoor gives a weaker object and usually a broken scheme, since the inputs it fails on are the ones an adversary will choose.

**What a trapdoor permutation gives.** With a [hard core predicate](/hard-core-predicate/) $b$, the scheme

$$\mathrm{Enc}(i, m) = \left( f_i(r),\ b(r) \oplus m \right) \quad \text{for a uniform } r \in D_i$$

encrypts one digit and is [IND-CPA](/ind-cpa-security/) secure. Iterating gives many digits, [full domain hash](/rsa-fdh/) gives signatures in the random oracle model, and [OAEP](/rsa-oaep/) gives [IND-CCA2](/ind-cca-security/) there as well. These are the constructions that make the object the central one of public-key cryptography. Note the direction of use: the *sender* evaluates the public function on a random value, and the owner of the trapdoor recovers that value. The message is never the input of $f_i$ in a modern scheme, which is the lesson of textbook RSA.

## Related definitions

- [One way function](/one-way-function/): the same object without the trapdoor. The gap between the two is the Impagliazzo-Rudich separation.
- [Hard core predicate](/hard-core-predicate/): what turns a trapdoor permutation into an encryption scheme for one digit. The Goldreich-Levin theorem supplies one for any candidate.
- **Trapdoor predicate**, from Goldwasser and Micali: a public key fixes two distributions on ciphertexts, one per digit, which the trapdoor tells apart. This is the direct abstraction of [Goldwasser-Micali](/goldwasser-micali-cryptosystem/) encryption, and it is a different and incomparable primitive: it implies encryption more directly, while a trapdoor permutation needs the hard core theorem first.
- **Lossy trapdoor function**, from Peikert and Waters: the index can be sampled in two modes, an injective one with a trapdoor and a lossy one whose image is small, and the two are indistinguishable. This gives [IND-CCA](/ind-cca-security/) security without random oracles and is the modern generic route.
- [Key encapsulation mechanism](/key-encapsulation-mechanism/): the practical interface that the construction above describes, with the message digit replaced by a derived key.
- [Public-key encryption](/public-key-encryption/) and [digital signature](/digital-signature/): the two problems that this definition exists to solve.
- [Computational hardness assumption](/computational-hardness-assumption/): "a trapdoor permutation family exists" is one, and it is strictly stronger than "a one way function exists" in the black box world.

## References
