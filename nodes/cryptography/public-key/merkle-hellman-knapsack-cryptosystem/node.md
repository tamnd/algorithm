---
tag: FC4WWX
kind: algorithm
slug: merkle-hellman-knapsack-cryptosystem
name: Merkle-Hellman knapsack cryptosystem
aliases:
- knapsack cryptosystem
area: cryptography/public-key
level: advanced
summary: "The first public-key scheme from subset sum: a superincreasing sequence hidden by a modular multiplication. Shamir broke it in 1982, and lattice reduction reads any message."
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {n: the number of terms in the public sequence}
  time: {worst: Θ(n^2), average: Θ(n^2), best: Θ(n^2)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, randomized: false}
history:
  year: 1978
  people: [Ralph Merkle, Martin Hellman, Adi Shamir, Jeffrey Lagarias, Andrew Odlyzko]
  note: Published in 1978 as the first alternative to RSA. Shamir broke the single iteration scheme in 1982 and Lagarias and Odlyzko gave the general low density lattice attack in 1985.
prereqs: [subset-sum-problem, lll-algorithm]
see_also: [public-key-encryption, rsa-cryptosystem, shortest-vector-problem, trapdoor-one-way-function, np-complete, post-quantum-cryptography, coppersmith-method]
sources:
  - paper: "Ralph C. Merkle and Martin E. Hellman, Hiding information and signatures in trapdoor knapsacks, IEEE Transactions on Information Theory 24(5), pages 525 to 530, 1978"
    locator: Sections 2 and 3 (the superincreasing sequence, the modular disguise, the single iteration scheme and the multiple iteration scheme)
  - paper: "Adi Shamir, A polynomial-time algorithm for breaking the basic Merkle-Hellman cryptosystem, 23rd Annual Symposium on Foundations of Computer Science (FOCS), pages 145 to 152, 1982, and IEEE Transactions on Information Theory 30(5), pages 699 to 704, 1984"
    locator: the whole paper (the integer programming search for the hidden multiplier, using the small denominators of the first public terms)
  - paper: "Jeffrey C. Lagarias and Andrew M. Odlyzko, Solving low-density subset sum problems, Journal of the ACM 32(1), pages 229 to 246, 1985"
    locator: Sections 1 and 2 (the lattice, the bound on the density, and the proof that almost all subset sum problems of density below 0.6463 fall to one basis reduction)
  - paper: doi:10.1007/BF01201999
    title: Matthijs J. Coster, Antoine Joux, Brian A. LaMacchia, Andrew M. Odlyzko, Claus-Peter Schnorr and Jacques Stern, Improved low-density subset sum algorithms, Computational Complexity 2, pages 111 to 128, 1992
    locator: Section 2 (the shifted lattice that raises the density bound from 0.6463 to 0.9408)
  - url: "https://www.dtc.umn.edu/~odlyzko/doc/arch/knapsack.survey.pdf"
    title: Andrew M. Odlyzko, The rise and fall of knapsack cryptosystems, Cryptology and Computational Number Theory, Proceedings of Symposia in Applied Mathematics 42, pages 75 to 88, 1990
    locator: the whole survey (the list of knapsack schemes and the attack that broke each one)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 8, Section 8.6 (knapsack public-key encryption, the Merkle-Hellman scheme, and the notes on the attacks that broke the family)
---

The Merkle-Hellman knapsack cryptosystem is the first public-key encryption scheme that was not RSA, and the first to be broken. The private key is a *superincreasing* sequence, a sequence in which every term is larger than the sum of all the terms before it, so a subset sum over it is read back by one greedy pass. The public key is the same sequence after a modular multiplication, which is meant to destroy that structure and leave a general [subset sum](/subset-sum-problem/) instance, an NP-complete problem. Encryption adds up the public terms that the message selects. **The scheme is broken and must never be used.** Shamir recovered the private key in 1982, and the lattice attack of Lagarias and Odlyzko reads any message from the public key alone, because the Merkle-Hellman knapsack has density near 1/2.

**Notation.** $n$ is the number of terms, $a_1, \ldots, a_n$ the private superincreasing sequence, $m$ the private modulus with $m > \sum a_i$, $w$ the private multiplier with $\gcd(w, m) = 1$, $b_i = w a_i \bmod m$ the public terms, $x \in \{0,1\}^n$ the message and $c = \sum x_i b_i$ the ciphertext. The *density* of the public sequence is $d = n / \log_2(\max_i b_i)$.

## In plain words

A list of weights is easy to work with when each weight is heavier than all the lighter ones together. To find which weights make up a given total, take the heaviest one that fits, then the next, and so on. There is never a choice to make.

The owner keeps such a list secret and publishes a scrambled copy: every weight is multiplied by a secret number, and only the remainder after division by a second secret number is published. The scrambled list looks random, so a sender can add up the published weights that the message picks, and nobody else can take the total apart. The owner unscrambles the total and uses the easy list.

It does not work. The scrambling leaves traces that lattice methods find in seconds.

## The problem

The scheme aims at [public-key encryption](/public-key-encryption/). Its one way function is the subset sum map

$$f_b : \{0,1\}^n \to \mathbb{Z}, \qquad f_b(x) = \sum_{i=1}^n x_i b_i ,$$

and the trapdoor is the pair $(m, w)$ that turns the public sequence back into a superincreasing one. The general problem of inverting $f_b$ is [subset sum](/subset-sum-problem/), which is [NP-complete](/np-complete/), and that was the selling point: a hard problem with a hidden easy case.

The gap in the argument is that NP-completeness is a statement about the *worst* case of a problem, while a cryptosystem needs the *average* case of the particular distribution it generates. The keys this scheme generates are not average subset sum instances. They have two defects, each fatal on its own: the modular disguise leaves the multiplier recoverable (Shamir), and the entries are too small for the number of terms, so the message is a short lattice vector (Lagarias and Odlyzko).

## The algorithm

```pseudo id=main
MH-KEYGEN(n)
L1  a ← a superincreasing sequence a_1, ..., a_n, each term above the sum of the terms before it
L2  m ← a random integer with m > a_1 + ... + a_n
L3  w ← a random integer in [2, m) with gcd(w, m) = 1
L4  for i ← 1 to n: t_i ← w*a_i mod m          ▷ the modular disguise
L5  π ← a random permutation of 1..n; b_j ← t_(π(j)) for j ← 1 to n
L6  return public key b, private key (a, m, w, π)

MH-ENCRYPT(b, x)                                ▷ x is a string of n binary digits
L7  return c ← x_1*b_1 + ... + x_n*b_n

MH-DECRYPT((a, m, w, π), c)
L8  s ← w^(-1)*c mod m                          ▷ remove the disguise
L9  y ← SOLVE-SUPERINCREASING(a, s)
L10 return the message x with x_j ← y_(π(j))
```

The easy case that the trapdoor restores:

```pseudo id=greedy
SOLVE-SUPERINCREASING(a, s)
L1  for i ← n down to 1
L2      if a_i ≤ s then y_i ← 1; s ← s − a_i
L3      else y_i ← 0
L4  if s ≠ 0 then return ERROR
L5  return y
```

**The walk-through.** Line 1 builds the easy instance. The implementation of this page takes $a_i$ to be the sum of the terms so far plus a random gap below $2^n$, so the terms grow by about a factor 2 each step and $a_n$ is near $2^{2n}$. Line 2 chooses a modulus above the total, which is what makes line 8 exact: the sum $\sum y_i a_i$ never wraps around $m$, so removing the factor $w$ recovers the integer sum and not just its residue class.

Lines 4 and 5 are the disguise. Multiplying by $w$ modulo $m$ is a bijection of $\mathbb{Z}_m$ that does not respect order, so the public terms are spread over the whole range and the superincreasing property is no longer visible to the eye. The permutation hides which public term came from which private one, which matters because the smallest private terms are the ones Shamir's attack looks for.

Line 7 is the encryption: $n$ additions, no multiplication, no modular reduction. This speed, about two orders of magnitude above RSA on the hardware of 1978, was the reason for the interest in knapsack schemes.

Line 8 undoes the disguise with one modular multiplication by $w^{-1}$, and lines 9 and the greedy block read the message. The greedy pass is forced at every step: if $a_i \le s$ then $a_i$ must be in the subset, because without it the remaining terms $a_1, \ldots, a_{i-1}$ sum to less than $a_i \le s$ and cannot reach $s$.

## Example

Take the private sequence $a = (2, 3, 6, 13, 27, 52)$, which is superincreasing since $2 < 3$, $2 + 3 = 5 < 6$, $2+3+6 = 11 < 13$, $2+3+6+13 = 24 < 27$ and $2+3+6+13+27 = 51 < 52$. Its total is 103, so take $m = 105$ and $w = 31$, with $\gcd(31, 105) = 1$. The disguise gives

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $a_i$ | 2 | 3 | 6 | 13 | 27 | 52 |
| $b_i = 31 a_i \bmod 105$ | 62 | 93 | 81 | 88 | 102 | 37 |

The public key is $(62, 93, 81, 88, 102, 37)$, with the identity permutation to keep the example readable. Encrypt the message $x = 011001$:

$$c = 93 + 81 + 37 = 211 .$$

To decrypt, note $31 \cdot 61 = 1891 = 18 \cdot 105 + 1$, so $w^{-1} = 61$, and

$$s = 61 \cdot 211 \bmod 105 = 12871 \bmod 105 = 61 .$$

The greedy pass on $a$: $52 \le 61$ so take it and leave 9; $27 > 9$ and $13 > 9$, skip both; $6 \le 9$, take it and leave 3; $3 \le 3$, take it and leave 0; $2 > 0$, skip. The subset is $\{3, 6, 52\}$, which is $x = 011001$ again.

**The break on the same key.** The attack of the next block builds a lattice of 7 rows from the public key and the ciphertext, reduces it once, and finds the row $(0,1,1,0,0,1,0)$. The first six entries are the message. The private sequence, the modulus and the multiplier were never used.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The parts are:

1. **The greedy pass is exact.** For a superincreasing sequence, a target has at most one subset that sums to it, and the greedy pass finds it or reports failure.
2. **The disguise is reversible.** Because $m$ exceeds the total of the sequence, the integer $\sum y_i a_i$ is below $m$, so line 8 recovers it exactly and not merely modulo $m$.
3. **Decryption inverts encryption** for every message, with no failure probability. The scheme is deterministic in both directions.
4. **The lattice attack is sound and, for low density, complete.** The message is a lattice vector of length at most $\sqrt{n}$ in a lattice whose other short vectors are ruled out when the density is below the Lagarias-Odlyzko bound 0.6463. The Merkle-Hellman construction has density near 1/2, which is inside the broken range by construction.

## Complexity

| step | cost in arithmetic operations on $O(n)$ digit integers | binary digit operations |
|---|---|---|
| key generation | $\Theta(n)$ draws and $n$ modular multiplications | $\Theta(n^3)$ |
| encryption | $n$ additions | $\Theta(n^2)$ |
| decryption | one modular multiplication and $n$ subtractions | $\Theta(n^2)$ |
| public key size | $n$ terms of about $2n$ binary digits | $\Theta(n^2)$ |
| the lattice attack | one LLL reduction in dimension $n+1$ with entries of $O(n)$ binary digits | polynomial in $n$ |

Encryption is the cheapest part of any public-key scheme ever proposed: additions only. The public key is the expensive part, about $2n^2$ binary digits, which is 128 kilobytes for the $n = 200$ or so that was once thought safe, against 256 octets for RSA at the same claimed security.

The rational arithmetic LLL of this page reduces the attack lattice in about 0.5 s for $n = 20$, 1.3 s for $n = 24$ and 2.2 s for $n = 28$ in Python. A floating point implementation with the $L^2$ algorithm handles $n$ in the hundreds in about the same time, which is why the historical parameters offer no protection.

## Properties

- **Broken, completely and in two independent ways.** Shamir's attack recovers the private key for the single iteration scheme in polynomial time. The lattice attack does not recover the key at all; it reads each message directly, and it does not care how the public sequence was built.
- **Deterministic, so not semantically secure** even if the subset sum were hard. Equal messages give equal ciphertexts, so the scheme fails [IND-CPA](/ind-cpa-security/) for the same reason textbook RSA does.
- **Additively malleable.** The ciphertexts of two messages with disjoint supports add to the ciphertext of the union, and a ciphertext minus a public term $b_i$ is the ciphertext of the message with the digit $i$ cleared. This leaks digits even without the attacks.
- **Low density by construction.** A superincreasing sequence of $n$ terms needs its largest term above $2^{n-1}$, so $\log_2 \max_i b_i \ge n$ and the density is at most about 1. The construction that makes the gaps random puts it near 1/2, deep inside the range that one lattice reduction solves.
- **NP-completeness gave no protection.** The hardness of the worst case of subset sum says nothing about the instances a key generator produces. This is the standard lesson of the knapsack family, and the reason modern lattice schemes argue from *average case* problems such as [learning with errors](/learning-with-errors/) with a worst case to average case reduction.
- **Fast encryption, no modular arithmetic in the sender.** The one real advantage, and not enough to save anything.

## Variants and improvements

Every variant below was broken. The list is the history of a dead family.

- **Multiple iteration Merkle-Hellman (1978).** Apply several modular disguises with different pairs $(m_j, w_j)$. Merkle and Hellman proposed this as the strong version and offered a prize for breaking it. Brickell broke it in 1984, and the lattice attacks do not care how many iterations were applied, since they work from the density alone.
- **Graham-Shamir knapsacks.** Hide the superincreasing structure in the high order digits instead of using a modular multiplication. Broken by the same lattice methods.
- **Lu-Lee, Goodman-McAuley, Pieprzyk and the Chor-Rivest scheme.** A long series of attempts to find a trapdoor in subset sum that leaves the public instance looking random. Odlyzko's survey lists them with the attack that killed each one. The Chor-Rivest scheme, which has high density and resisted lattice attacks, fell in 2001 to Vaudenay's algebraic attack.
- **Shamir's attack (1982).** Searches for the hidden multiplier $w^{-1}/m$ as a real number. The points $b_i \cdot w^{-1}/m$ must all land in short intervals near the bottom of $[0,1)$, because the private terms $a_i$ are small for small $i$, and that condition is an integer program in a fixed number of variables, which Lenstra's algorithm solves in polynomial time. The permutation of line 5 costs the attacker only a factor $\binom{n}{k}$ for the few terms it needs.
- **The Lagarias-Odlyzko attack (1985), in the block below.** No key recovery, just one basis reduction per ciphertext.
- **The CJLOSS improvement (1992).** Shift the lattice so that the target vector has entries $\pm 1/2$ instead of 0 and 1. The target gets shorter by a factor near $\sqrt{2}$, and the density bound rises from 0.6463 to 0.9408. Almost every knapsack with a trapdoor is below that.

```pseudo id=attack
LOW-DENSITY-ATTACK(b, c)
L1  K ← an integer above sqrt(n)/2
L2  build the basis with rows (e_i, K*b_i) for i ← 1 to n, and the row (0, K*c)
L3  R ← LLL-REDUCE(basis)
L4  for each row r of R with last entry 0
L5      if ±r has all entries in {0, 1} and b·(±r) = c then return that vector
L6  return FAILURE
```

The lattice vector $\sum_i x_i (e_i, K b_i) - 1 \cdot (0, Kc)$ is $(x, 0)$, of length at most $\sqrt{n}$, while the determinant of the lattice is $K c$, which is about $2^{n/d}$ with $d$ the density. When $d < 0.6463$, a counting argument shows that almost no other lattice vector is that short, so the reduced basis must contain the message.

## When to use it

Never. There is no setting in which this scheme is the right tool, and no parameter size that repairs it. It is on this site for three reasons:

- **As history.** It is the second public-key scheme ever published, and the first to show that a public-key proposal can be destroyed within four years.
- **As the standard example of a failed hardness argument.** The claim "it is based on an NP-complete problem" is still made for new schemes. Merkle-Hellman is the counterexample to keep ready: the trapdoor was what made the instances easy.
- **As an exercise in lattice reduction.** The attack is the simplest real application of [LLL](/lll-algorithm/): write the secret as a short vector, reduce once, read it off. The same shape appears in [Coppersmith's method](/coppersmith-method/) and in the attacks on early lattice schemes.

For public-key encryption today use [RSA-OAEP](/rsa-oaep/), [ECIES](/ecies/) or a post-quantum [KEM](/key-encapsulation-mechanism/) such as [ML-KEM](/crystals-kyber/). Note that the modern lattice schemes are not a rehabilitation of knapsacks: they argue from average case hardness with a reduction from a worst case lattice problem, which is exactly what Merkle-Hellman lacked.

## Pitfalls

- **Believing that NP-hardness of a problem makes a cryptosystem.** The key generator defines a distribution, and only the hardness of *that* distribution matters. No modern scheme claims security from NP-completeness alone.
- **Adding iterations to repair a broken disguise.** Several modular multiplications give an attacker more structure to work with, not less, and change the density not at all.
- **Choosing $m$ below the total of the sequence.** Then the sum wraps around and line 8 gives the wrong integer, so decryption fails for about half of the messages. This is a correctness bug, not a security repair.
- **Reading the permutation as a defence.** It costs the key recovery attack a small factor and costs the lattice attack nothing, because the attack recovers the message in the public order.
- **Using the scheme for signatures.** Merkle and Hellman also proposed a knapsack signature, by inverting the map on a hash. It is broken by the same attacks, and it was broken earlier, since a signature forgery needs only one lucky subset sum.
- **Reusing the "fast encryption" argument.** Any scheme that is cheap because its public operation is linear is in danger from lattices, since linear relations are what lattice reduction finds.

**The code of this page is for study only.** The key sizes are toy sizes, the arithmetic is not constant time, and the attack runs against a key made in the same process. The scheme itself is broken at every size, so no implementation of it is safe.

## Implementations

## History

Diffie and Hellman described public-key cryptography in 1976 without a concrete trapdoor. Two answers appeared in 1978: [RSA](/rsa-cryptosystem/) in February, and in the September issue of the IEEE Transactions on Information Theory, "Hiding information and signatures in trapdoor knapsacks" by Ralph Merkle and Martin Hellman. The knapsack scheme looked the stronger candidate at the time. Its underlying problem was NP-complete, while factoring was not known to be NP-hard and still is not, and its encryption was about a hundred times faster than a modular exponentiation. Merkle offered 100 dollars for a break of the single iteration scheme and 1000 dollars for the multiple iteration version.

Adi Shamir collected the first prize in 1982, with an attack presented at FOCS that recovers the private multiplier by integer programming in a fixed dimension. Ernest Brickell collected the second in 1984 by breaking the iterated scheme. Then Lagarias and Odlyzko changed the terms of the discussion in 1985: their lattice attack ignores the trapdoor entirely and solves *almost every* subset sum problem of density below 0.6463, which covers nearly every knapsack scheme anybody had proposed, including ones with no known key recovery attack. Coster, Joux, LaMacchia, Odlyzko, Schnorr and Stern raised the bound to 0.9408 in 1992.

Attempts continued for a decade. Odlyzko's 1990 survey, "The rise and fall of knapsack cryptosystems", lists a dozen proposals and the attack that broke each one, and its conclusion has held: no knapsack scheme has survived. The Chor-Rivest scheme lasted the longest, from 1988 to Vaudenay's break in 2001.

The episode left two permanent marks on the field. First, the modern standard of evidence for a new assumption, which asks for an average case problem and, where possible, a reduction from a worst case one. Second, the recognition of lattice reduction as a basic tool of cryptanalysis. [LLL](/lll-algorithm/) was published in 1982, the same year as Shamir's attack, and the knapsack problem was its first large scale application.

## References
