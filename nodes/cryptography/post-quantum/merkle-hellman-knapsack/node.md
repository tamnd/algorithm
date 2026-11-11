---
tag: TC99QJ
kind: algorithm
slug: merkle-hellman-knapsack
name: Knapsack cryptosystems after Merkle-Hellman
aliases:
- CJLOSS attack
- low-density subset sum attack
area: cryptography/post-quantum
level: intro
summary: "The knapsack schemes after Merkle-Hellman (iterated, Chor-Rivest, OTU) and the lattice attacks that broke them: Lagarias-Odlyzko below density 0.6463 and CJLOSS below 0.9408."
model: word-ram
complexity:
  vars: {n: "the number of weights a_i", b: "the number of bits of the largest a_i; time counts arithmetic operations of LLL, on integers of O(n b) bits"}
  time: {worst: O(n^4 b), average: O(n^4 b), best: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, randomized: false}
history:
  year: 1992
  people: [Matthijs J. Coster, Antoine Joux, Brian A. LaMacchia, Andrew M. Odlyzko, Claus-Peter Schnorr, Jacques Stern]
  note: The CJLOSS paper in Computational Complexity raised the density bound of the Lagarias-Odlyzko attack from 0.6463 to 0.9408. Knapsack schemes were proposed and broken from 1978 to the 2000s.
prereqs: [merkle-hellman-knapsack-cryptosystem, lll-algorithm, subset-sum-problem]
see_also: [lattice-based-cryptography, unique-svp, shortest-vector-problem, lattice-basis-reduction, post-quantum-cryptography, shor-algorithm, knapsack-problem, schroeppel-shamir-algorithm]
sources:
  - paper: "Matthijs J. Coster, Antoine Joux, Brian A. LaMacchia, Andrew M. Odlyzko, Claus-Peter Schnorr and Jacques Stern, Improved low-density subset sum algorithms, Computational Complexity 2(2), 1992"
    locator: the lattice with the row (1/2, ..., 1/2, N s), and the theorem that almost all subset sum problems of density below 0.9408 reduce to one call of a shortest vector oracle
  - paper: "Jeffrey C. Lagarias and Andrew M. Odlyzko, Solving low-density subset sum problems, Journal of the ACM 32(1), 1985"
    locator: the lattice with rows (e_i, N a_i) and (0, ..., 0, N s), the definition of density, and the bound 0.6463
  - paper: "Ernest F. Brickell, Breaking iterated knapsacks, CRYPTO '84, LNCS 196, 1985"
    locator: the attack on the iterated Merkle-Hellman scheme, which finds the chain of modular multiplications with lattice reduction
  - paper: "Benny Chor and Ronald L. Rivest, A knapsack-type public key cryptosystem based on arithmetic in finite fields, IEEE Transactions on Information Theory 34(5), 1988"
    locator: the weights from discrete logarithms in GF(p^h), the messages of weight h, and the density above 1
  - paper: "Serge Vaudenay, Cryptanalysis of the Chor-Rivest cryptosystem, CRYPTO '98, LNCS 1462, 1998; journal version in Journal of Cryptology 14(2), 2001"
    locator: the key recovery that uses the subfields of GF(p^h) for the proposed parameters
  - paper: "Tatsuaki Okamoto, Keisuke Tanaka and Shigenori Uchiyama, Quantum public-key cryptosystems, CRYPTO 2000, LNCS 1880"
    locator: the knapsack scheme whose key generation needs discrete logarithms computed by a quantum computer, with low-weight messages
  - paper: "Phong Q. Nguyen and Jacques Stern, Adapting density attacks to low-weight knapsacks, ASIACRYPT 2005, LNCS 3788"
    locator: the pseudo-density of a knapsack with messages of low Hamming weight, the reductions to SVP and CVP, and the application to Chor-Rivest and OTU
  - paper: "Andrew M. Odlyzko, The rise and fall of knapsack cryptosystems, in Cryptology and Computational Number Theory, Proceedings of Symposia in Applied Mathematics 42, AMS, 1990"
    locator: the survey of the knapsack schemes and the attacks on each
  - paper: "Miklos Ajtai, Generating hard instances of lattice problems, STOC 1996"
    locator: the modular knapsack function x -> A x mod q with small x and its worst-case to average-case reduction
---

After Merkle and Hellman proposed the [knapsack cryptosystem](/merkle-hellman-knapsack-cryptosystem/) in 1978, many other schemes tried to hide a trapdoor in a [subset sum problem](/subset-sum-problem/). All the main ones fell. Some fell to attacks on their particular trapdoor. Most fell to one general method: write the subset sum as a short vector in a lattice and find it with the [LLL algorithm](/lll-algorithm/). This page describes the later schemes, the density measure that decides when the lattice attack works, and the CJLOSS attack (Coster, Joux, LaMacchia, Odlyzko, Schnorr and Stern, 1992), which is the strongest form of the general method. The history is a lesson for today's lattice-based cryptography.

**Notation.** The public weights are positive integers $a_1, \ldots, a_n$, the message is $x \in \{0, 1\}^n$, and the ciphertext is $s = \sum_i x_i a_i$. The density is $d = n / \log_2 \max_i a_i$. $e_i$ is the $i$-th unit vector of length $n$, and $\|v\|$ is the Euclidean length.

## In plain words

A knapsack cipher publishes a list of numbers. To send a message, you add up the numbers that your message picks and send the total. Only the owner has a hidden shortcut to find which numbers were picked.

The attack ignores the shortcut. It builds a grid of points in many dimensions in which the picked numbers form one very short arrow. A standard method for finding short arrows then reads off the message.

This works best when the numbers are large compared with how many there are. Designers tried to escape it with small numbers, with special messages, or with deeper hidden shortcuts, and each attempt failed in its own way.

## The problem

**The schemes after Merkle-Hellman.** The basic scheme was broken by Shamir in 1982. Designers then tried several ways out.

- **Iterated Merkle-Hellman.** Apply the modular multiplication of the basic scheme several times, with different moduli, to hide the superincreasing sequence better. Brickell broke it at CRYPTO '84 (published 1985), and the low-density attack below also applies, because each iteration makes the weights larger and the density lower.
- **Chor-Rivest (1984; journal version 1988).** The weights are discrete logarithms in $GF(p^h)$, and messages have exactly $h$ ones. The density can exceed 1, so the lattice attacks of the time did not apply. Schnorr and Horner (1995) broke smaller parameters with improved lattice reduction, and Vaudenay (CRYPTO '98; Journal of Cryptology, 2001) recovered the keys of the proposed parameters with the subfield structure of $GF(p^h)$.
- **Okamoto-Tanaka-Uchiyama (OTU, CRYPTO 2000).** A knapsack whose key generation needs discrete logarithms, computed with [Shor's algorithm](/shor-algorithm/) on a quantum computer, so it was offered as a quantum public-key scheme. The density is high and messages have low weight. Nguyen and Stern (ASIACRYPT 2005) showed that low-weight knapsacks still fall to lattice attacks when a measure they call pseudo-density is low, which counts the bits in a message of low weight rather than $n$. Their bounds put the OTU parameters in doubt.

**The attack problem.** Given $a_1, \ldots, a_n$ and $s$, find $x \in \{0, 1\}^n$ with $\sum_i x_i a_i = s$, without the private key. The subset sum problem is NP-hard in general, but the instances of a cryptosystem are random-looking instances of low density, and those are easy.

**Density.** If $d > 1$, there are more messages than possible sums, so many $s$ have several solutions and the system cannot decrypt uniquely without extra structure. If $d$ is small, the weights are large, the solution is almost surely unique, and the lattice that encodes the problem has an unusually short vector. Merkle-Hellman with $n = 100$ used weights of about 200 bits, a density of about $0.5$.

## The algorithm

Lagarias and Odlyzko (1985) took the lattice spanned by the rows $(e_i, N a_i)$ for $i = 1, \ldots, n$ and $(0, \ldots, 0, N s)$. The vector $(x, 0)$ lies in it and has length at most $\sqrt{n}$, about $\sqrt{n/2}$ for a message of weight $n/2$. With an oracle for the shortest vector, this finds $x$ for almost all instances with $d < 0.6463$. CJLOSS change the last row to $(\frac{1}{2}, \ldots, \frac{1}{2}, N s)$. The target becomes $(x_1 - \frac{1}{2}, \ldots, x_n - \frac{1}{2}, 0)$, of length exactly $\sqrt{n}/2$ for every $x$, and the bound rises to $d < 0.9408$. The code scales by 2 to keep integers.

```pseudo id=main
CJLOSS(a_1, …, a_n, s)
L1  N ← ⌊√n⌋ + 1                                ▷ N > √n, so a vector with last entry ≠ 0 is longer than the target
L2  for i ← 1 to n do b_i ← (2 e_i, N a_i)
L3  b_{n+1} ← (1, …, 1, N s)
L4  B ← LLL(b_1, …, b_{n+1})
L5  for each row v of B, and its negative −v do
L6      if v_{n+1} = 0 and every v_i ∈ {−1, +1} for i ≤ n then
L7          x ← ((v_1 + 1)/2, …, (v_n + 1)/2)
L8          if Σ x_i a_i = s then return x
L9  return FAIL
```

The target is $\sum_i x_i b_i - b_{n+1} = (2x_1 - 1, \ldots, 2x_n - 1, 0)$, of length $\sqrt{n}$. LLL only approximates the shortest vector, within a factor $2^{n/2}$ in the worst case, but on these lattices it finds the target far more often than the bound suggests. The Lagarias-Odlyzko attack is the same with the rows $(e_i, N a_i)$ and $(0, \ldots, 0, N s)$, and with $v_i \in \{0, 1\}$ at line L6.

## Example

Take $n = 10$, the weights $a = (1327, 3883, 618, 1618, 2667, 198, 297, 3364, 2195, 386)$ and $s = 5635$. The largest weight has 11.9 bits, so $d = 10 / \log_2 3883 \approx 0.839$, above the Lagarias-Odlyzko bound. Line L1 gives $N = 4$. After LLL, the first row of the reduced basis is

$$(-1, 1, 1, -1, 1, -1, -1, 1, -1, 1, 0).$$

Its last entry is 0 and the others are $\pm 1$, so line L5 takes its negative and line L7 gives $x = (1, 0, 0, 1, 0, 1, 1, 0, 1, 0)$. The check at line L8 holds: $1327 + 1618 + 198 + 297 + 2195 = 5635$. The next rows of the reduced basis, such as $(0, -2, 2, 0, 0, 2, -2, 2, 0, 0, 0)$, are other short vectors, of length $\sqrt{20} \approx 4.47$ against $\sqrt{10} \approx 3.16$ for the target.

The code also breaks a basic Merkle-Hellman key with $n = 10$ ($q = 7253$, density 0.78) from the public key alone. It recovers the message of a ciphertext without the multiplier $r$. In a run of 24 weights of 30 bits ($d \approx 0.80$), CJLOSS with LLL recovered 10 of 10 messages, and Lagarias-Odlyzko with LLL only 3 of 10. At 24 weights of 24 bits ($d \approx 1.00$), CJLOSS still recovered 9 of 10, because LLL works very well at this small dimension. The tests check a smaller version of each of these runs. The code is for study only, on toy instances, and is not constant time.

## Correctness

The returned $x$ is always a solution, because line L8 checks it. The question is when the attack returns. The target vector lies in the lattice and has length $\sqrt{n}$. Any vector with a nonzero last entry has length at least $N > \sqrt{n}$. So if the target is, up to sign, the only vector of length at most $\sqrt{n}$ with last entry 0, it is the shortest vector of the lattice, and an exact shortest vector oracle returns it. CJLOSS show that this holds for almost all instances with $d < 0.9408$, by counting the integer points in a ball of radius $\sqrt{n}/2$ that could satisfy the one linear relation $\sum y_i a_i = y_{n+1} s$. The [full proof](proofs/correctness.md) proves the deterministic part and states the counting theorem.

## Complexity

Lattice reduction dominates. The lattice has rank $n + 1$ and entries of $O(b + \log n)$ bits, so LLL uses $O(n^4 b)$ arithmetic operations on integers of $O(n b)$ bits. Lines L5 to L8 then cost $O(n^2)$. In practice, LLL succeeds on these lattices up to a few dozen dimensions, and BKZ with larger blocks goes further. The theoretical density bounds assume an exact shortest vector oracle, which costs exponential time in $n$. So for large $n$ the attack is heuristic: it is not proved to work, but it works much better than the worst-case bounds suggest.

## Properties

- **Ignores the trapdoor.** The attack uses only the public weights and the ciphertext, so it breaks every knapsack scheme of low enough density, whatever the trapdoor.
- **Deterministic.** LLL and the scan are deterministic; the probabilistic part is over the random instance.
- **Density threshold.** With an exact SVP oracle, the attack works for almost all instances below $d = 0.9408$. Above $d = 1$, solutions are not unique, and the scheme needs extra structure, such as low-weight messages, which brings its own attacks.
- **Same target length for all messages.** In the CJLOSS lattice the target has length $\sqrt{n}/2$ (before the scaling by 2) whatever the weight of $x$; in the Lagarias-Odlyzko lattice its length depends on the weight.

## Variants and improvements

- **Lagarias-Odlyzko (1985).** The first low-density attack, with bound 0.6463. Frieze (1986) gave a simpler proof.
- **Low-weight knapsacks.** Nguyen and Stern (2005) adapted the attack to messages of Hamming weight $k$ and showed that pseudo-density, not density, decides its success.
- **Better reduction.** BKZ and its successors find shorter vectors than LLL, which pushes the practical limit to larger $n$. The same embedding of a closest vector problem in a lattice with one extra row is the "primal attack" on LWE today, which reduces to the [unique shortest vector problem](/unique-svp/).
- **Combinatorial algorithms.** [Schroeppel-Shamir](/schroeppel-shamir-algorithm/) and the later algorithms of Howgrave-Graham and Joux, and of Becker, Coron and Joux, solve subset sums of density near 1 in time about $2^{0.29 n}$, which the lattice attacks do not reach.

## When to use it

Use the CJLOSS attack to test whether a scheme or a protocol leaks a subset sum of low density: weights much larger than $2^n$. In teaching, use it to show how lattice reduction breaks a scheme based on an NP-hard problem. Do not use any knapsack cryptosystem of this family to protect data; none has survived.

## Pitfalls

- **NP-hard is not hard on average.** Subset sum is NP-hard in the worst case, but the instances of a cryptosystem are random-looking instances of a special shape, and most of these are easy. A hard worst case says nothing about the instances that a key generator produces.
- **Hidden structure leaks.** Every trapdoor puts structure into the weights. Shamir's attack used the small multipliers of the basic scheme, Brickell's attack the chain of iterations, and Vaudenay's the subfields of Chor-Rivest.
- **Reduction beats its bounds.** The theoretical guarantee of LLL is weak, but in practice it finds short vectors far beyond it. Parameters must follow the best experimental and heuristic estimates, not the proven worst case.
- **Quantum key generation is not quantum security.** OTU needed a quantum computer to build keys, but this did not make it resist lattice attacks, classical or quantum.

**The lesson for lattice cryptography.** Modern [lattice-based cryptography](/lattice-based-cryptography/) is in a sense the knapsack idea done right. Ajtai's function $x \mapsto A x \bmod q$ (1996), the basis of the SIS problem, is a modular knapsack with vector weights. The difference is that its average case is proved as hard as worst-case lattice problems, so a random instance is safe if any is, and no trapdoor is hidden in the public instance itself: in LWE-based schemes the public key is a random instance plus small noise. The parameters are set by the cost of the lattice attacks that broke the knapsacks, now with BKZ cost models.

## Implementations

## History

Merkle and Hellman published their scheme in 1978, and Shamir broke the basic version in 1982. Brickell broke the iterated version at CRYPTO '84. Lagarias and Odlyzko gave the general low-density attack in 1985, and Coster, Joux, LaMacchia, Odlyzko, Schnorr and Stern raised its bound to 0.9408 in 1992. Chor and Rivest proposed a high-density scheme at CRYPTO '84 (journal version 1988), which Schnorr and Horner attacked for small parameters in 1995 and Vaudenay broke at CRYPTO '98. Okamoto, Tanaka and Uchiyama proposed a quantum public-key knapsack at CRYPTO 2000, and Nguyen and Stern showed in 2005 that its low-weight messages do not stop lattice attacks. Odlyzko's 1990 survey, "The rise and fall of knapsack cryptosystems", gave the field its epitaph.

## References
