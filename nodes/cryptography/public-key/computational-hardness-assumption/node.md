---
tag: HNP3EM
kind: definition
slug: computational-hardness-assumption
name: Computational hardness assumption
aliases:
- cryptographic assumption
area: cryptography/public-key
level: intro
summary: A statement that some problem cannot be solved by any efficient algorithm on a stated distribution of instances. Every security proof in use rests on one, and none of them is proved.
prereqs: [computational-indistinguishability, polynomial-time]
see_also: [one-way-function, rsa-problem, decisional-diffie-hellman, learning-with-errors, integer-factorization, p-versus-np-problem, shor-algorithm]
sources:
  - paper: doi:10.1007/978-3-540-45146-4_6
    title: Moni Naor, On cryptographic assumptions and challenges, Advances in Cryptology, CRYPTO 2003, LNCS 2729, pages 96 to 109, 2003
    locator: Sections 1 and 2 (the classification of assumptions by how a claimed break can be demonstrated, and the definition of an efficiently falsifiable assumption)
  - paper: doi:10.1007/978-3-662-49096-9_21
    title: Shafi Goldwasser and Yael Tauman Kalai, Cryptographic assumptions, a position paper, Theory of Cryptography, TCC 2016-A, LNCS 9562, pages 505 to 522, 2016
    locator: Sections 1 and 3 (complexity assumptions against hardness assumptions, and the criteria proposed for accepting a new one)
  - paper: doi:10.1137/S0097539795293172
    title: Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5), pages 1484 to 1509, 1997
    locator: Sections 4 and 5 (the factoring algorithm and the discrete logarithm algorithm, which falsify every assumption of the first group of the table on this page for a quantum adversary)
  - paper: doi:10.1145/1568318.1568324
    title: Oded Regev, On lattices, learning with errors, random linear codes, and cryptography, Journal of the ACM 56(6), article 34, 2009
    locator: Sections 1 and 3 (the learning with errors assumption and the quantum reduction from worst case lattice problems to it)
  - paper: doi:10.1007/BFb0054851
    title: Dan Boneh, The decision Diffie-Hellman problem, Algorithmic Number Theory, ANTS 1998, LNCS 1423, pages 48 to 63, 1998
    locator: Sections 2 to 4 (the statement of DDH, its relation to CDH and to the discrete logarithm, and the groups in which each is believed hard)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2021
    locator: the chapter on number theoretic assumptions (factoring, RSA, the discrete logarithm family, and how a scheme's proof uses an assumption)
---

A computational hardness assumption is a statement of the form "no efficient algorithm solves this problem on these instances". It is an assumption and not a theorem: nobody can prove that any of the problems used in cryptography is hard, because that would separate complexity classes that remain open. A security proof is therefore always conditional. It says that breaking the scheme is at least as hard as solving the stated problem, so the assumption is where the trust actually sits. This page defines what an assumption is, lists the ones in use, and gives the two ways of sorting them that matter: standard against non-standard, and falsifiable against not.

**Notation.** $k$ is the security parameter, $\mathrm{negl}(k)$ a function below $1/k^t$ for every $t$ and all large $k$, and "efficient" means probabilistic time polynomial in $k$. $N = pq$ is a product of two primes of $k/2$ binary digits, $\mathbb{G}$ a cyclic group of prime order $q$ with generator $g$, and $\mathbb{Z}_N^*$ the units modulo $N$.

## Definition

**A search assumption.** Let $\mathrm{Gen}(1^k)$ be an efficient sampler that outputs an instance $x$, and let $R$ be an efficiently checkable relation that says which strings are solutions of $x$. The assumption is

$$\Pr\left[ x \leftarrow \mathrm{Gen}(1^k),\ w \leftarrow \mathcal{A}(1^k, x) \ : \ R(x, w) \right] \le \mathrm{negl}(k) \quad \text{for every efficient } \mathcal{A} .$$

Three parts must be stated and all three carry weight: the *sampler*, because a problem can be hard for one distribution of instances and easy for another; the *relation*, because finding a full solution and finding one digit of it are different problems; and the *threshold*, because an assumption with a constant success probability is a different statement from one with a negligible threshold.

**A decision assumption.** Let $\mathrm{Gen}_0$ and $\mathrm{Gen}_1$ be two efficient samplers. The assumption is that the two ensembles are [computationally indistinguishable](/computational-indistinguishability/):

$$\left| \Pr[\mathcal{A}(1^k, \mathrm{Gen}_0(1^k)) = 1] - \Pr[\mathcal{A}(1^k, \mathrm{Gen}_1(1^k)) = 1] \right| \le \mathrm{negl}(k) \quad \text{for every efficient } \mathcal{A} .$$

A decision assumption is formally stronger than the matching search assumption, since an algorithm that finds the solution can decide. [DDH](/decisional-diffie-hellman/) implies [CDH](/computational-diffie-hellman/) and the converse is open, and in a group with a [bilinear pairing](/bilinear-pairing/) the converse is *false*: the pairing decides DDH while CDH is still believed hard.

**What makes an assumption usable.** Four properties are asked of a new one.

1. **It must be falsifiable.** There must be a way to demonstrate a break. Naor's classification turns on this: an assumption is *efficiently falsifiable* when a challenger can sample a public challenge and check a claimed solution in polynomial time, so that a break is a public event that settles the question. Factoring is the extreme case: a factor of a published number is checked by one multiplication, and the RSA challenge numbers made this concrete.
2. **It should be simple to state**, with no reference to the scheme it supports. An assumption of the form "this scheme is secure" proves nothing.
3. **It should have survived study**, which in practice means it has a name, a literature, and a best known attack whose cost is understood well enough to set parameters.
4. **It should be as weak as possible.** Of two assumptions that both do the job, the one implied by the other is the better choice, because it is harder to be wrong about.

**Not falsifiable, and why that is a problem.** A *knowledge* assumption says that an algorithm which produces a certain output must "know" a related value, formally that an extractor exists. There is no challenge that can be published and no solution that can be checked, so a doubter has nothing to attack and a claim of a break has nothing to exhibit. The knowledge of exponent assumption, used in some succinct proof systems, is of this kind, as is any assumption quantified over all efficient adversaries with an existential extractor. These are not useless, but they are a different kind of evidence, and Goldwasser and Kalai argue for keeping the two kinds apart in any security claim.

**Models are not assumptions.** The [random oracle model](/random-oracle-model/) and the [generic group model](/generic-group-model/) replace an object by an idealized one. A proof in such a model is a proof about a different world, and there are schemes secure in the random oracle model whose every instantiation is insecure. The models are evidence, not assumptions, and a page that says "secure in the ROM under the RSA assumption" is making one assumption and one idealization.

## Examples and non-examples

The catalogue in use. "Shor" means [Shor's algorithm](/shor-algorithm/) solves the problem in polynomial time on a quantum computer, so the assumption is false against a quantum adversary.

| assumption | the problem | kind | quantum | used by |
|---|---|---|---|---|
| factoring | given $N = pq$, find $p$ | search | Shor | [Rabin](/rabin-cryptosystem/), [Blum-Goldwasser](/blum-goldwasser-cryptosystem/), key generation everywhere |
| [RSA](/rsa-problem/) | given $(N, e, y)$, find $x$ with $x^e = y \bmod N$ | search | Shor | [RSA](/rsa-cryptosystem/), [OAEP](/rsa-oaep/), [RSA-PSS](/rsa-pss/) |
| strong RSA | given $(N, y)$, find any $(x, e)$ with $e > 1$ and $x^e = y \bmod N$ | search | Shor | accumulators, Cramer-Shoup signatures, anonymous credentials |
| [QR](/quadratic-residuosity-problem/) | decide whether $y$ with Jacobi symbol 1 is a square modulo $N$ | decision | Shor | [Goldwasser-Micali](/goldwasser-micali-cryptosystem/), Cocks identity based encryption |
| [DCR](/decisional-composite-residuosity/) | decide whether $y$ is an $N$-th power modulo $N^2$ | decision | Shor | [Paillier](/paillier-cryptosystem/), [Okamoto-Uchiyama](/okamoto-uchiyama-cryptosystem/) |
| [DL](/discrete-logarithm-problem/) | given $g^a$ in $\mathbb{G}$, find $a$ | search | Shor | the base of the whole group family |
| [CDH](/computational-diffie-hellman/) | given $g^a, g^b$, compute $g^{ab}$ | search | Shor | [Diffie-Hellman](/diffie-hellman/), [ECDH](/ecdh/), hashed ElGamal |
| [DDH](/decisional-diffie-hellman/) | tell $(g^a, g^b, g^{ab})$ from $(g^a, g^b, g^c)$ | decision | Shor | [ElGamal](/elgamal-encryption/), [Cramer-Shoup](/cramer-shoup-cryptosystem/) |
| gap-DH | CDH is hard even with an oracle that decides DDH | search | Shor | pairing groups, where DDH is easy and CDH is not |
| BDH and decisional BDH | compute or recognize $e(g,g)^{abc}$ from $g^a, g^b, g^c$ | both | Shor | [Boneh-Franklin IBE](/boneh-franklin-ibe/), short signatures |
| $q$-type, for example $q$-SDH | given $g, g^x, g^{x^2}, \ldots, g^{x^q}$, produce a new power relation | search | Shor | pairing based signatures and succinct proofs |
| [LWE](/learning-with-errors/) | tell $(A, As + e)$ from uniform, with $e$ small | decision | open | [ML-KEM](/crystals-kyber/), [ML-DSA](/crystals-dilithium/), fully homomorphic encryption |
| [SIS](/short-integer-solution/) | given $A$, find a short nonzero $z$ with $Az = 0 \bmod q$ | search | open | lattice signatures, hash functions |
| [NTRU](/ntru-problem/) | distinguish a ratio of small polynomials from uniform | decision | open | [NTRU](/ntru-encrypt/), Falcon |
| decoding | decode a random linear code at a given distance | search | open | [McEliece](/mceliece-cryptosystem/), [Niederreiter](/niederreiter-cryptosystem/) |

**Standard against non-standard.** The first six rows and the two lattice rows are *standard*: each is a single short statement about a natural problem, each predates the schemes that use it, and each has a literature of attack papers that fix the parameters. The $q$-type family is *non-standard* in a specific sense: the assumption is a family indexed by $q$, the adversary gets more data as $q$ grows, and Cheon's attack shows that the security degrades with $q$, so the choice of $q$ is part of the assumption. The *uber assumption* framework collects such families into one statement, which makes them easier to compare and no easier to believe.

**Examples of assumptions that were falsified.**

- The subset sum assumption *with a Merkle-Hellman trapdoor*, falsified by Shamir in 1982 and by the lattice attacks of 1985; see [Merkle-Hellman](/merkle-hellman-knapsack-cryptosystem/). The lesson is that the sampler is part of the assumption, since the general problem is NP-complete and only the generated instances were easy.
- The hardness of the Chor-Rivest knapsack, broken in 2001.
- SIDH, the isogeny assumption behind SIKE, which reached the final round of the NIST process and was broken in 2022 by the [Castryck-Decru attack](/castryck-decru-attack/).
- Small subgroup and small exponent variants of discrete logarithm assumptions, repeatedly weakened by attacks that use the structure the variant added.

**Non-examples.**

- **"The problem is NP-complete."** This is a statement about the worst case of a problem. Cryptography needs the *average* case of the particular sampler a key generator uses, and the two are unrelated in general. [P versus NP](/p-versus-np-problem/) is also the wrong question in another way: $\mathrm{P} \ne \mathrm{NP}$ is necessary for one way functions to exist but is not known to be sufficient.
- **"The scheme has no known attack."** An absence of attacks is evidence, not a statement that can be assumed, and it gives no parameters.
- **Perfect secrecy.** [The one time pad](/one-time-pad/) needs no assumption, which is exactly why it also needs a key as long as the message. Information theoretic security is the one kind that assumes nothing; see [perfect secrecy](/perfect-secrecy/).
- **"Nobody can factor a 2048 digit number."** A claim about today's machines, not an asymptotic statement. It is the claim that actually matters for a deployment, and it is derived from an assumption plus a cost estimate for the best known algorithm, not assumed on its own.

**Relations between them.** Assumptions form a partial order by implication, and the weaker an assumption is the better. Known implications include: factoring is hard if RSA is hard, and the converse is open; DL hard if CDH hard; CDH hard if DDH hard; strong RSA hard implies RSA hard; LWE is hard if worst case lattice problems are hard, by Regev's quantum reduction, which is the only row of the table with a worst case to average case reduction behind it. That reduction is the strongest form of evidence any assumption in use has, and it is a large part of the reason the post-quantum standards are lattice based.

## Related definitions

- [One way function](/one-way-function/) is the minimal assumption of the field. Its existence is implied by every assumption in the table, and almost all of symmetric cryptography follows from it.
- [Trapdoor one way function](/trapdoor-one-way-function/) is strictly more than a one way function as far as anybody can prove, and it is what public-key encryption needs.
- [Hard core predicate](/hard-core-predicate/) turns a hardness assumption about full inversion into one about a single digit, with no extra assumption.
- [Computational indistinguishability](/computational-indistinguishability/) is the shape every decision assumption takes.
- [Semantic security](/semantic-security/), [IND-CPA](/ind-cpa-security/) and [IND-CCA](/ind-cca-security/) are the security goals that proofs connect to these assumptions by a [reduction](/reduction/).
- [Integer factorization](/integer-factorization/), the [RSA problem](/rsa-problem/), the [quadratic residuosity problem](/quadratic-residuosity-problem/), the [discrete logarithm problem](/discrete-logarithm-problem/), [learning with errors](/learning-with-errors/) and [short integer solution](/short-integer-solution/) are the problem pages behind the rows of the table, with the best known algorithms and the key sizes they imply.
- [Post-quantum cryptography](/post-quantum-cryptography/) is the response to the quantum column of the table.

## References
