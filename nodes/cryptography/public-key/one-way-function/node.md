---
tag: 624RQR
kind: definition
slug: one-way-function
name: One-way function
aliases:
- OWF
area: cryptography/public-key
level: intro
summary: A function that is easy to compute and hard to invert on a uniform input. It is the minimal assumption of cryptography, and most of symmetric cryptography follows from it alone.
prereqs: [computational-hardness-assumption]
see_also: [trapdoor-one-way-function, hard-core-predicate, pseudorandom-generator, pseudorandom-function, p-versus-np-problem, integer-factorization, hill-prg-from-one-way-functions]
sources:
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Sections 2.1 to 2.3 (the strong and weak definitions, the collections of one way functions, the candidates, and Theorem 2.3.2 with the full proof of Yao's amplification)
  - paper: "Whitfield Diffie and Martin E. Hellman, New directions in cryptography, IEEE Transactions on Information Theory 22(6), pages 644 to 654, November 1976"
    locator: Section III (the one way function and the one way authentication idea, where the notion first appears in print in this form)
  - paper: doi:10.1007/BF02579323
    title: Leonid A. Levin, One way functions and pseudorandom generators, Combinatorica 7(4), pages 357 to 363, 1987
    locator: the whole paper (the universal one way function, a single explicit function that is one way if any one way function exists)
  - paper: doi:10.1137/S0097539793244708
    title: Johan Hastad, Russell Impagliazzo, Leonid A. Levin and Michael Luby, A pseudorandom generator from any one-way function, SIAM Journal on Computing 28(4), pages 1364 to 1396, 1999
    locator: Sections 1 and 4 (the construction of a pseudorandom generator from an arbitrary one way function, through the false entropy generator)
  - paper: doi:10.1145/6490.6503
    title: Oded Goldreich, Shafi Goldwasser and Silvio Micali, How to construct random functions, Journal of the ACM 33(4), pages 792 to 807, 1986
    locator: Sections 2 and 3 (the tree construction of a pseudorandom function family from a length doubling pseudorandom generator)
  - paper: doi:10.1145/100216.100269
    title: John Rompel, One-way functions are necessary and sufficient for secure signatures, Proceedings of the 22nd ACM Symposium on Theory of Computing, STOC 1990, pages 387 to 394, 1990
    locator: Sections 1 and 4 (universal one way hash functions from any one way function, and signatures from those)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: the chapter on theoretical constructions (the definition, the hard core predicate, and the chain from one way functions to pseudorandom permutations)
---

A one way function is easy to compute and hard to invert. It is the weakest assumption from which anything in cryptography follows, and it is implied by every other assumption used in the field, so it sits at the bottom of the order of [hardness assumptions](/computational-hardness-assumption/). From a one way function alone one gets [pseudorandom generators](/pseudorandom-generator/), [pseudorandom functions](/pseudorandom-function/), message authentication codes, commitments, zero knowledge proofs for every NP statement, and [digital signatures](/digital-signature/). What does not follow, as far as anybody can prove, is public-key encryption, which needs the [trapdoor](/trapdoor-one-way-function/) version.

**Notation.** $n$ is the input length, $x \leftarrow \{0,1\}^n$ a uniform input, $\mathrm{negl}(n)$ a function below $1/n^t$ for every $t$ and all large $n$, and $f^{-1}(y) = \{x : f(x) = y\}$ the preimage set. "Efficient" means probabilistic time polynomial in the length of the first input. The notation $1^n$ is the length $n$ written in unary, which is given to the adversary so that it may use time polynomial in $n$ even when $f$ shrinks its input.

## Definition

**Strong one way function.** A function $f : \{0,1\}^* \to \{0,1\}^*$ is *one way* when both hold.

1. **Easy to compute.** There is a deterministic polynomial time algorithm that computes $f(x)$ for every $x$.
2. **Hard to invert.** For every efficient algorithm $\mathcal{A}$,

$$\Pr_{x \leftarrow \{0,1\}^n} \left[ \mathcal{A}(f(x), 1^n) \in f^{-1}(f(x)) \right] \le \mathrm{negl}(n) .$$

Three details decide the meaning. The probability is over a *uniform* input, so hardness on a sparse set of inputs is not enough. The adversary wins with *any* preimage, not only with $x$ itself, so a function that maps many inputs to one output is not thereby safer. And the adversary is given $1^n$, so a function that compresses its input a great deal is not one way by accident of the output length.

**Weak one way function.** $f$ is *weakly* one way when it is easy to compute and there is a polynomial $p$ such that for every efficient $\mathcal{A}$ and all large $n$,

$$\Pr_{x \leftarrow \{0,1\}^n} \left[ \mathcal{A}(f(x), 1^n) \in f^{-1}(f(x)) \right] \le 1 - \frac{1}{p(n)} .$$

So an adversary may succeed on almost every input, as long as a noticeable fraction of inputs resists. The two definitions look far apart, and they are not.

**Theorem (Yao, 1982; amplification).** If a weak one way function exists then a strong one exists. Concretely, let $f$ be weakly one way with the polynomial $p$, and set $m = 2 n\, p(n)$ and

$$g(x_1, \ldots, x_m) = \left( f(x_1), \ldots, f(x_m) \right) \qquad \text{with each } |x_i| = n .$$

Then $g$ is strongly one way. The proof is in Goldreich, Volume 1, Section 2.3, Theorem 2.3.2.

*The idea.* Inverting $g$ means inverting $f$ on all $m$ blocks at once, and intuitively the failure probabilities multiply: $(1 - 1/p)^m \approx e^{-2n}$. The intuition is not a proof, because the blocks are not independent from the point of view of an adversary that may spend its effort where it likes. The real argument is a reduction in the other direction: from an algorithm $\mathcal{B}$ that inverts $g$ with probability $1/\mathrm{poly}$, build $\mathcal{A}$ that inverts $f$ on all but a $1/p$ fraction of inputs. Given $y = f(x)$, the algorithm $\mathcal{A}$ repeatedly builds a random instance of $g$ with $y$ planted in a random block and the other blocks sampled by $\mathcal{A}$ itself, so that $\mathcal{A}$ knows their preimages, and calls $\mathcal{B}$. A counting argument over the "hard" inputs, those on which $\mathcal{B}$'s success probability conditioned on the planted block is small, shows that the set of hard inputs must be smaller than $1/p$, contradicting the weak one wayness of $f$. The number of repetitions is polynomial, which is where the factor $n\,p(n)$ in $m$ comes from.

The theorem matters for two reasons. It means a candidate needs only a noticeable hard fraction to be useful, which is a much easier thing to believe and to check. And the amplified function is far larger than the original, which is why no practical scheme is built this way.

**One way permutation.** A length preserving $f$ that is a bijection on $\{0,1\}^n$ for each $n$. Then the preimage is unique and $f^{-1}(f(x)) = \{x\}$. Permutations are the convenient case for the theory, because a uniform input gives a uniform output.

**Collections of one way functions.** Most candidates are not single functions on all strings but families indexed by a key, with three algorithms: a sampler $I(1^n)$ that outputs an index $i$, a domain sampler $D(i)$ that outputs an $x$ in the domain $D_i$, and the evaluation $f_i(x)$. The hardness condition is that no efficient algorithm inverts $f_i$ on $f_i(x)$ for $i \leftarrow I(1^n)$ and $x \leftarrow D(i)$. This is the form that RSA and the discrete logarithm take, since the modulus or the group has to be sampled. Goldreich, Section 2.4, shows that collections and single functions give the same theory.

**The existence question.** A one way function exists only if $\mathrm{P} \ne \mathrm{NP}$. The reason is that the inversion problem is in NP: the relation "$x$ is a preimage of $y$" is checkable in polynomial time, so with $\mathrm{P} = \mathrm{NP}$ one decides whether a preimage with a given prefix exists, and then builds a preimage one digit at a time with $n$ queries. The converse is open and is not expected to be provable with current techniques. $\mathrm{P} \ne \mathrm{NP}$ is a statement about the *worst* case, while a one way function must be hard on *average*, and Impagliazzo's five worlds name the possibilities: a world where NP is easy, a world where NP is hard in the worst case but easy on average, a world with average case hardness and no one way functions, a world with one way functions and no public-key encryption, and a world with public-key encryption. Nothing known rules out any of the five.

**Levin's universal one way function.** There is a single explicit function $f_U$ that is one way if any one way function exists. Levin's construction splits the input, uses the first part to describe a machine, runs the first $\log n$ machines in an enumeration for $n^2$ steps each on pieces of the rest, and concatenates the outputs. If some machine $M$ computes a one way function, then $M$ appears in the enumeration for all large $n$, and inverting $f_U$ requires inverting that block. So the existence question has one concrete witness, and the hunt for "the" one way function is, in principle, over. The function is useless in practice: its description is an interpreter, and its security parameter has to be astronomically large before the relevant machine appears.

## Examples and non-examples

**Candidates.** Each is believed one way, none is proved.

- **Multiplication of primes.** $f(p, q) = pq$ on pairs of primes of $n$ binary digits each, as a collection with the sampler drawing two random primes. Inverting it is [integer factorization](/integer-factorization/). This is the oldest candidate and the one with the longest attack record; the best known algorithm is the number field sieve at $\exp(O(n^{1/3} \log^{2/3} n))$.
- **Modular exponentiation.** $f_{p,g}(x) = g^x \bmod p$ on $x \in \{1, \ldots, p-1\}$, a permutation of the group when $g$ generates it. Inverting it is the [discrete logarithm problem](/discrete-logarithm-problem/). The elliptic curve version is the one in use, because the best attack there is generic and costs $\sqrt{q}$ group operations.
- **Subset sum.** $f(a_1, \ldots, a_n, S) = \left(a_1, \ldots, a_n, \sum_{i \in S} a_i \right)$ with each $a_i$ of $n$ binary digits and $S \subseteq \{1, \ldots, n\}$. Inverting it is [subset sum](/subset-sum-problem/) at density 1, which is the hardest density and is not touched by the lattice attacks that broke the [knapsack cryptosystems](/merkle-hellman-knapsack-cryptosystem/) at density 1/2. Note how the parameters decide everything: the same problem at a different density is easy.
- **RSA and Rabin.** $f_{N,e}(x) = x^e \bmod N$ and $f_N(x) = x^2 \bmod N$. These are the candidates with a *trapdoor*, which is a strictly stronger property; see [trapdoor one way function](/trapdoor-one-way-function/).
- **Block ciphers and hash functions.** $f(k) = \mathrm{AES}_k(0)$ and $f(x) = \mathrm{SHA\text{-}256}(x)$ are the candidates in practice. They have no algebraic structure to attack and no proof of anything, and they are many orders of magnitude faster than the number theoretic ones.

**Non-examples.**

- $f(x) = x$, and any function with an efficient inverse. Easy to compute, easy to invert.
- $f(x) = 0^n$. Inverting is trivial, since *any* string is a preimage. A function is not one way because its output carries no information; it is one way because preimages are hard to *find*.
- $f(x) = $ the first half of $x$. Any completion of the known half is a valid preimage.
- **Multiplication on all integers**, $f(x, y) = x \cdot y$ with $x, y$ uniform of $n$ binary digits. This is *not* one way, although factoring is believed hard. Half the time the product is even, so $(2, z/2)$ is a preimage, and about 86 percent of random integers have a factor below 1000. The candidate has to sample *primes*, and this is the clearest illustration that the sampler belongs to the assumption.
- **A function hard to invert only on a sparse set.** If $f$ is easy to invert on all but $2^{n/2}$ of the inputs, it fails even the weak definition, since the hard fraction must be at least $1/\mathrm{poly}$.
- **A permutation with a hard core digit but an easy inverse.** No such thing exists, which is the point of the [hard core predicate](/hard-core-predicate/) theorem in the other direction: hardness of one digit follows from hardness of the whole.

**What a one way function gives.** This is the world called Minicrypt.

| target | construction | cost |
|---|---|---|
| [pseudorandom generator](/pseudorandom-generator/) | from any one way function (HILL 1999); from a one way *permutation* it is the simple Blum-Micali-Yao chain with a [hard core predicate](/hard-core-predicate/) | the general construction is polynomial but very large; see [HILL](/hill-prg-from-one-way-functions/) |
| [pseudorandom function](/pseudorandom-function/) | the GGM tree from a length doubling generator (1986) | $n$ generator calls per evaluation |
| pseudorandom permutation | the Luby-Rackoff Feistel construction from a pseudorandom function | 3 or 4 rounds |
| [message authentication code](/message-authentication-code/) | a pseudorandom function applied to the message | one pass |
| commitment and zero knowledge for NP | from a generator, through a bit commitment | polynomial |
| [digital signature](/digital-signature/) | universal one way hash functions and a tree (Rompel 1990) | polynomial, impractical |

**What a one way function is not known to give.** Public-key encryption and key agreement. Impagliazzo and Rudich proved in 1989 that no *black box* construction of a key agreement protocol from a one way permutation exists, which is the formal statement of the gap between Minicrypt and Cryptomania. So the extra structure of a [trapdoor](/trapdoor-one-way-function/), or of a group with a commuting operation as in [Diffie-Hellman](/diffie-hellman/), is not a convenience; it is the thing that makes public-key cryptography possible.

## Related definitions

- [Trapdoor one way function](/trapdoor-one-way-function/): a collection of one way functions each of which has a secret that inverts it. This is the assumption behind [public-key encryption](/public-key-encryption/).
- [Hard core predicate](/hard-core-predicate/): a single digit of the input that is as hard to predict as the whole input is to find. The Goldreich-Levin theorem gives one for every one way function.
- [One way permutation](/trapdoor-one-way-function/): the bijective case, used in the clean constructions.
- A **universal one way hash function**, or UOWHF, is the collision style relative: given a key *after* choosing a first input, finding a second input with the same image is hard. Rompel built these from one way functions, and signatures from these.
- [Computational hardness assumption](/computational-hardness-assumption/): the general shape, of which "a one way function exists" is the weakest useful instance.
- [Pseudorandom generator](/pseudorandom-generator/) and [pseudorandom function](/pseudorandom-function/): the two objects that a one way function yields and that most of symmetric cryptography is built from.
- [P versus NP](/p-versus-np-problem/): the worst case question. One way functions need the average case version, and the two are not known to be related.
- [Cryptographic hash function](/cryptographic-hash-function/): the practical object. Collision resistance is a different and incomparable requirement, since a one way function may be easy to find collisions for and a collision resistant function is one way only if it also compresses.

## References
