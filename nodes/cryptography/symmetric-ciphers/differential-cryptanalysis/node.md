---
tag: 7PQPMV
kind: technique
slug: differential-cryptanalysis
name: Differential cryptanalysis
area: cryptography/symmetric-ciphers
level: advanced
summary: A chosen-plaintext attack that follows how an input difference spreads through the rounds. A difference that holds with high probability reveals last-round key bits.
prereqs: [block-cipher, s-box, chosen-plaintext-attack, substitution-permutation-network]
see_also: [linear-cryptanalysis, boomerang-attack, integral-cryptanalysis, related-key-attack, data-encryption-standard, advanced-encryption-standard, skipjack, cryptanalysis]
sources:
  - paper: doi:10.1007/BF00630563
    title: Eli Biham and Adi Shamir, Differential cryptanalysis of DES-like cryptosystems, Journal of Cryptology 4(1), 1991
    locator: pp. 3-72, the definitions of characteristics, right pairs and the signal-to-noise ratio, and the attacks on reduced-round DES
  - paper: doi:10.1007/978-1-4613-9314-6_5
    title: Eli Biham and Adi Shamir, Differential cryptanalysis of the full 16-round DES, chapter of Differential Cryptanalysis of the Data Encryption Standard, Springer, 1993 (book doi:10.1007/978-1-4613-9314-6)
    locator: pp. 79-88, the attack on the full 16 rounds with 2^47 chosen plaintexts
  - paper: doi:10.1007/3-540-46416-6_2
    title: Xuejia Lai, James L. Massey and Sean Murphy, Markov ciphers and differential cryptanalysis, Eurocrypt 1991, LNCS 547, Springer, 1991
    locator: the definitions of a differential and of a Markov cipher, and the hypothesis of stochastic equivalence
  - paper: doi:10.1147/rd.383.0243
    title: Don Coppersmith, The Data Encryption Standard (DES) and its strength against attacks, IBM Journal of Research and Development 38(3), 1994
    locator: the design criteria of the S-boxes and the statement that the IBM team knew the attack as the T-attack in 1974
  - paper: doi:10.1080/0161-110291890885
    title: Howard M. Heys, A tutorial on linear and differential cryptanalysis, Cryptologia 26(3), 2002
    locator: pp. 189-221, the toy SPN, its difference distribution table, the 3-round characteristic and the extraction of last-round key bits
  - paper: doi:10.1007/978-3-662-04722-4
    title: Joan Daemen and Vincent Rijmen, The Design of Rijndael, Springer, 2002
    locator: the wide trail strategy and the bound on the number of active S-boxes in four rounds of Rijndael
---

Differential cryptanalysis is a [chosen-plaintext attack](/chosen-plaintext-attack/) on [block ciphers](/block-cipher/). The attacker encrypts pairs of plaintexts with a fixed XOR difference and watches the difference of the ciphertexts. In a good cipher the output difference looks random. In a weak cipher, some input difference leads to some difference a few rounds later much more often than chance. Eli Biham and Adi Shamir published the method in 1990 and 1991, and used it to break the full 16-round [DES](/data-encryption-standard/) with $2^{47}$ chosen plaintexts, slightly faster than exhaustive search. Every new block cipher since then is designed to resist it.

**Notation.** $E$ is the cipher with $r$ rounds and block size $n$. $\alpha$ is the plaintext difference and $\beta$ the difference after $r - 1$ rounds. A pair $(P, P \oplus \alpha)$ is a right pair if its difference after $r - 1$ rounds is $\beta$. $p$ is the probability of $\alpha \to \beta$ over random plaintexts and keys. For an S-box $S$, the difference distribution table (DDT) has entry $T[a][b]$ = the number of $x$ with $S(x) \oplus S(x \oplus a) = b$. $N$ is the number of pairs.

## In plain words

Take two messages that differ in a few chosen places, and encrypt both. The key mixes in the same way into both messages, so it does not change how they differ; only the tables in the cipher do. Each table turns a given difference into some output differences more often than others. By chaining the most likely table steps, the attacker predicts how the difference looks just before the last round.

Then the attacker guesses part of the last round key, undoes the last round on both outputs, and checks the difference. With the right guess, the predicted difference shows up a little more often than with any wrong guess. After enough pairs, the right guess stands out in a count.

## When it applies

- **The attacker can choose plaintexts**, or at least sees many pairs with a known difference. With only known plaintexts, the attack needs far more data.
- **Key addition by XOR.** If the key enters by XOR, a difference passes through the key addition unchanged, so the probability of a trail does not depend on the key. With modular addition, as in [IDEA](/idea/) or [RC5](/rc5/), the attacker uses a different notion of difference or accepts a weaker estimate.
- **Small S-boxes with an uneven DDT.** The attack needs one or more trails through the rounds with probability $p$ well above $2^{-n}$.
- **Not when the designers proved bounds.** Ciphers built with the wide trail strategy, such as [AES](/advanced-encryption-standard/), have proven bounds on the probability of any trail that make the attack need more pairs than there are plaintexts.

## The template

A characteristic is a sequence of differences, one for each round, with a probability for each round. Its probability is the product of the round probabilities. For an S-box with input difference $a$ and output difference $b$, the probability is $T[a][b] / 2^m$ for an $m$-bit S-box. A differential is the pair $(\alpha, \beta)$ only, and its probability is the sum over all characteristics with these ends.

The attack on the last round uses an $(r - 1)$-round differential $\alpha \to \beta$ and guesses the key bits that enter the S-boxes of the last round where $\beta$ is not zero.

```pseudo id=main
DIFFERENTIAL-LAST-ROUND(E, α, β, N)
L1  counts[g] ← 0 for each guess g of the target subkey bits
L2  for j ← 1 to N do
L3      choose P at random; C ← E(P); C′ ← E(P ⊕ α)
L4      if C ⊕ C′ is not zero on the S-boxes where β is zero then skip this pair
L5      for each g such that S⁻¹(C ⊕ g) ⊕ S⁻¹(C′ ⊕ g) = β on the target S-boxes do
L6          counts[g] ← counts[g] + 1
L7  return the g with the largest count
```

**Why the right guess wins.** A right pair always adds 1 to the count of the right guess $g^*$ in line L6, because undoing the last round with $g^*$ gives back the true difference $\beta$. So $g^*$ gets about $N p$ counts from right pairs. A wrong pair, or a wrong guess, behaves like random noise and adds about the same small amount to every guess. Line L4 removes most wrong pairs for free, since a right pair has no difference on the S-boxes that $\beta$ does not touch. Biham and Shamir call the ratio of the right count to the average wrong count the signal-to-noise ratio. When it is large, a few right pairs are enough.

**Data.** With $N = c / p$ pairs, the right guess gets about $c$ right pairs. Biham and Shamir report that a small constant $c$, a few right pairs, suffices when the signal-to-noise ratio is high. The time is about $2N$ encryptions plus the work of line L5.

**The Markov assumption.** The product rule for a characteristic treats the rounds as independent. Lai, Massey and Murphy defined a Markov cipher: one where the probability of a round difference does not depend on the input, when the round key is uniform. For such a cipher with independent round keys, the differences form a Markov chain, and the product rule is exact on average over the keys. Real ciphers have a key schedule, so the rule holds only as a hypothesis, which Lai, Massey and Murphy call stochastic equivalence. For one fixed key, the probability can differ from the average.

**About the code.** The Python code of this page attacks the toy cipher of Heys, a 4-round substitution-permutation network on 16 bits with five independent 16-bit round keys. It is for study only and is not constant time. Do not use any of it to protect real data. Use AES from a validated library such as OpenSSL instead.

## Classic examples

### The toy cipher of Heys

The cipher of the Heys tutorial has four 4-bit S-boxes in each round, all equal to the first row of the DES S-box S1, and a bit permutation that sends bit $4i + j$ to bit $4j + i$. Rows B, 4 and 2 of the DDT hold the large entries $T$[B][2] = 8, $T$[4][6] = 6 and $T$[2][5] = 6.

| round | active S-box | input difference | output difference | probability |
|---|---|---|---|---|
| 1 | $S_{12}$ | B | 2 | 8/16 |
| 2 | $S_{23}$ | 4 | 6 | 6/16 |
| 3 | $S_{32}$ | 2 | 5 | 6/16 |
| 3 | $S_{33}$ | 2 | 5 | 6/16 |

So the plaintext difference $\alpha$ = 0B00 reaches the input of the round-4 S-boxes as $\beta$ = 0606 with probability $\frac{8}{16} \cdot \left(\frac{6}{16}\right)^3 = 27/1024 \approx 2^{-5.25}$. The attack guesses the 8 bits of the last round key on S-boxes 2 and 4. For one fixed key, an exact count over all $2^{16}$ pairs gives 1752 right pairs, a probability of 0.0267, a little above 27/1024 because other characteristics add to the same differential.

With $N = 8/p \approx 303$ pairs, about 19 pairs pass the filter of line L4 in a typical run, and the right guess gets 5 counts while the next best guesses get 3. The tests run the attack on 50 random keys and require success for at least 45; with $N = 16/p$ pairs it succeeds for all 30 test keys.

### DES

Biham and Shamir found iterative characteristics of DES: a difference that returns to itself after two rounds, with probability about $1/234$ per two rounds. The 1991 paper breaks DES reduced to fewer rounds. The full 16-round attack, in their 1993 book, needs $2^{47}$ chosen plaintexts. In 1994, Don Coppersmith of IBM published the design criteria of the DES S-boxes. He stated that the IBM team knew the method in 1974, called it the T-attack, and chose the S-boxes to resist it. The design criteria stayed secret after discussions with the NSA.

### AES and the wide trail strategy

Daemen and Rijmen designed Rijndael so that any trail over four rounds has at least 25 active S-boxes. Each S-box passes a difference with probability at most $2^{-6}$, so any 4-round characteristic has probability at most $2^{-150}$, far below $2^{-128}$. This is the wide trail strategy, described in The Design of Rijndael.

## Variations

- **Truncated differentials** fix the difference only on some words, for example zero or nonzero bytes.
- **Impossible differentials** use a difference that never occurs. Biham, Biryukov and Shamir used one to attack [Skipjack](/skipjack/) reduced to 31 rounds.
- **Higher-order differentials** take differences of differences. [Integral cryptanalysis](/integral-cryptanalysis/) is close to this idea.
- **[Boomerang attacks](/boomerang-attack/)** join two short differentials instead of one long one.
- **Related-key differentials** put a difference in the key as well. See the [related-key attack](/related-key-attack/).
- **Differential-linear attacks** join a differential with a linear approximation from [linear cryptanalysis](/linear-cryptanalysis/).

## Pitfalls

- **One characteristic is not the differential.** The probability of the differential is the sum over all characteristics with the same ends. Using one characteristic often underestimates it, as the toy example shows.
- **The average over keys.** The Markov assumption gives the average over independent round keys. For a fixed key schedule, some keys can be much better or much worse.
- **Too few pairs.** With fewer than about $1/p$ pairs, the right guess may get no right pair at all, and the count shows noise.
- **The filter.** Without line L4, every wrong pair adds noise to many guesses, and the attack needs more data.
- **Real ciphers.** Run such experiments only on toy ciphers or reduced rounds that you are allowed to attack.

## Exercises

1. Compute the DDT of a 3-bit S-box of your choice, and show that each row sums to 8 and that all entries are even.
2. Show that if the key enters by XOR, the difference after the key addition does not depend on the key.
3. In the toy example, explain why a right pair has ciphertext difference zero on S-boxes 1 and 3.
4. Prove that for a Markov cipher with independent uniform round keys, the average probability of a characteristic is the product of the round probabilities.
5. Run the toy attack with $N = 2/p$, $4/p$ and $8/p$ pairs over many random keys, and plot the success rate against $N$.

## References
