---
tag: 008RPY
kind: technique
slug: boomerang-attack
name: Boomerang attack
aliases:
area: cryptography/symmetric-ciphers
level: research
summary: A differential attack that joins two short differentials, one for each half of the cipher, with quartets of texts. It can work when no good differential exists for the whole cipher.
prereqs: [differential-cryptanalysis, block-cipher, chosen-ciphertext-attack]
see_also: [linear-cryptanalysis, integral-cryptanalysis, related-key-attack, serpent, chosen-plaintext-attack, birthday-paradox, cryptanalysis]
sources:
  - paper: doi:10.1007/3-540-48519-8_12
    title: David Wagner, The boomerang attack, Fast Software Encryption 1999, LNCS 1636, Springer, 1999
    locator: pp. 156-170, the abstract and Section 1 (the folk theorem and the O(q^-4) texts), Section 2 (the quartet, Figure 1 and the identity at the middle), Section 4 (the sum over the middle differences) and the table of results (COCONUT98 with 2^16 adaptive chosen texts and 2^38 work)
  - paper: doi:10.1007/3-540-44706-7_6
    title: John Kelsey, Tadayoshi Kohno and Bruce Schneier, Amplified boomerang attacks against reduced-round MARS and Serpent, Fast Software Encryption 2000, LNCS 1978, Springer, 2001
    locator: pp. 75-93, the abstract and Section 2.4 (the boomerang as an attack with chosen plaintexts only)
  - paper: doi:10.1007/3-540-44987-6_21
    title: Eli Biham, Orr Dunkelman and Nathan Keller, The rectangle attack, rectangling the Serpent, Eurocrypt 2001, LNCS 2045, Springer, 2001
    locator: pp. 340-357, the abstract and Section 2 (the count of right quartets with the sums over all middle differences)
  - paper: doi:10.1109/TIT.2011.2111091
    title: Sean Murphy, The return of the cryptographic boomerang, IEEE Transactions on Information Theory 57(4), 2011
    locator: pp. 2517-2521, the dependence between the two differentials of a boomerang
  - paper: doi:10.1007/978-3-319-78375-8_22
    title: Carlos Cid, Tao Huang, Thomas Peyrin, Yu Sasaki and Ling Song, Boomerang connectivity table, a new cryptanalysis tool, Eurocrypt 2018, LNCS 10821, Springer, 2018
    locator: pp. 683-714, the boomerang connectivity table of an S-box at the switch between the two halves
  - paper: doi:10.1080/0161-110291890885
    title: Howard M. Heys, A tutorial on linear and differential cryptanalysis, Cryptologia 26(3), 2002
    locator: pp. 189-221, the toy SPN used in the example
---

The boomerang attack is a form of [differential cryptanalysis](/differential-cryptanalysis/) that David Wagner published in 1999. It cuts the cipher into two halves and uses one short differential for each half. Four texts, two encryptions and two decryptions, form a quartet. If both differentials hold on the right pairs, the last difference comes back to the first, like a boomerang. Wagner used it to disprove a common belief: that a cipher is safe from differential attacks if no differential over the whole cipher has a high probability.

**Notation.** $E$ is a [block cipher](/block-cipher/) on $n$-bit blocks, written as $E = E_1 \circ E_0$. The differential $\alpha \to \beta$ holds for $E_0$ with probability $p$, and the differential $\gamma \to \delta$ holds for $E_1$ with probability $q$. A quartet is four plaintexts $P, P', Q, Q'$ and their ciphertexts $C, C', D, D'$. $N$ is the number of quartets.

## In plain words

Long differentials are weak: the longer the path, the smaller its chance. The boomerang uses two short paths instead. The attacker takes two messages with a chosen difference and encrypts them. The difference runs through the first half of the cipher. Then the attacker changes both results by a second chosen difference and decrypts the two new texts. This second difference runs back through the second half.

If all four short paths work, the two decrypted messages again differ by the first difference. For a random permutation, this happens almost never. So a count of returns tells the cipher apart from a random permutation, and further steps can find key bits.

## When it applies

- **The attacker can encrypt and decrypt.** The basic attack needs chosen plaintexts and adaptive chosen ciphertexts, as in a [chosen-ciphertext attack](/chosen-ciphertext-attack/). The amplified and rectangle variants need only chosen plaintexts, at the cost of more data.
- **Good short differentials, no good long one.** The attack helps when $p^2 q^2$ is much larger than the probability of any differential over all of $E$.
- **The halves are not too dependent.** The estimate $p^2 q^2$ assumes that the four differentials hold independently. At the switch between the halves, this can be far from true.

## The template

The basic attack sends each quartet as follows.

```pseudo id=main
BOOMERANG(E, E⁻¹, α, δ, N)
L1  count ← 0
L2  for j ← 1 to N do
L3      choose P at random; P′ ← P ⊕ α
L4      C ← E(P); C′ ← E(P′)
L5      D ← C ⊕ δ; D′ ← C′ ⊕ δ
L6      Q ← E⁻¹(D); Q′ ← E⁻¹(D′)
L7      if Q ⊕ Q′ = α then count ← count + 1
L8  return count / N
```

**Why the boomerang returns.** Suppose that $E_0(P) \oplus E_0(P') = \beta$, that $E_1^{-1}(C) \oplus E_1^{-1}(D) = \gamma$ and that $E_1^{-1}(C') \oplus E_1^{-1}(D') = \gamma$. Since $E_1^{-1}(C) = E_0(P)$ and $E_1^{-1}(D) = E_0(Q)$, and the same with primes,

$$E_0(Q) \oplus E_0(Q') = \big(E_0(P) \oplus E_0(P')\big) \oplus \big(E_0(P) \oplus E_0(Q)\big) \oplus \big(E_0(P') \oplus E_0(Q')\big) = \beta \oplus \gamma \oplus \gamma = \beta.$$

So the pair $(Q, Q')$ has difference $\beta$ in the middle. If the differential $\alpha \to \beta$ also holds backwards through $E_0$ for this pair, line L7 finds $Q \oplus Q' = \alpha$. This is Section 2 of Wagner's paper. The differential of the pair $(P, P')$ holds with probability $p$, the two backward differentials through $E_1$ with probability $q$ each, and the last one with about $p$. If these events are independent, a quartet returns with probability about $p^2 q^2$. For a random permutation, the chance is about $2^{-n}$.

**Many middle differences.** The identity above does not need a fixed $\beta$ or $\gamma$. It needs only that both pairs on each side have the same difference. Wagner noted in Section 4 that this gives the better estimate

$$\hat{p}^2 \hat{q}^2, \qquad \hat{p}^2 = \sum_{\beta} \Pr[\alpha \to \beta]^2, \qquad \hat{q}^2 = \sum_{\gamma} \Pr[\gamma \to \delta]^2.$$

**Cost.** With $N$ quartets, the right count is about $N p^2 q^2$, and the attack uses $4N$ queries. So a distinguisher needs $N$ of order $1/(p^2 q^2)$, that is, of order $q^{-4}$ texts when $p = q$, as Wagner states. Key recovery adds a guess of the key bits of an outer round, as in a [differential attack](/differential-cryptanalysis/) on the last round, and counts the returns for each guess.

**About the code.** The Python code of this page runs the distinguisher on the toy cipher of Heys, a 4-round substitution-permutation network on 16 bits with five independent 16-bit round keys. The block is small, so the code also computes the return rate exactly over all plaintexts. It is for study only and is not constant time. Do not use any of it to protect real data. Use AES from a validated library such as OpenSSL instead.

## Classic examples

### The toy cipher of Heys

Let $E_0$ be rounds 1 and 2 of the toy cipher and $E_1$ be rounds 3 and 4, with $\alpha$ = 00B0 and $\delta$ = 0008. Take the round keys 1234, 9ABC, 5A5A, 0F0F and 7777. An exact count over all $2^{16}$ inputs gives:

| quantity | value | about |
|---|---|---|
| best $\beta$ for $E_0$ and its $p$ | 0202, 0.1875 | $2^{-2.4}$ |
| best $\gamma$ for $E_1$ and its $q$ | 5050, 0.0234 | $2^{-5.4}$ |
| $p^2 q^2$ | $1.9 \cdot 10^{-5}$ | $2^{-15.7}$ |
| $\hat{p}^2 \hat{q}^2$ | $3.64 \cdot 10^{-4}$ | $2^{-11.4}$ |
| best differential from $\alpha$ over all 4 rounds | 0.00229 | $2^{-8.8}$ |
| quartets that return | 1572 of 65536, 0.0240 | $2^{-5.4}$ |
| random permutation | | $2^{-16}$ |

One quartet that returns: $P$ = 002B and $P'$ = 009B encrypt to $C$ = 6DD9 and $C'$ = AED8. Then $D$ = 6DD1 and $D'$ = AED0 decrypt to $Q$ = 2301 and $Q'$ = 23B1, and $Q \oplus Q'$ = 00B0 = $\alpha$. In the middle, both pairs $(P, P')$ and $(Q, Q')$ have difference 0202, and both cross pairs have difference C090.

So the boomerang returns ten times as often as the best long differential holds. Here it returns far more often than even $\hat{p}^2 \hat{q}^2$ predicts, because the halves are not independent: the quartets meet in the S-boxes of round 3, right after the switch. The tests check, for five random keys, that the return rate is more than five times the best 4-round differential.

### COCONUT98

Serge Vaudenay designed COCONUT98 with a decorrelation module, which gives a proof that no differential over the whole cipher has a high probability. Wagner broke it with a boomerang that uses about $2^{16}$ adaptive chosen plaintexts and ciphertexts and about $2^{38}$ work. The proof stays true, but it does not cover quartets. In the same paper he gave boomerang attacks on 16 rounds of Khufu, on 6 rounds of FEAL and on 16 rounds of CAST-256.

### Serpent and MARS

Kelsey, Kohno and Schneier attacked 8 rounds of [Serpent](/serpent/) and 11 rounds of the MARS core with the amplified boomerang. Biham, Dunkelman and Keller then reached 10 rounds of Serpent with 256-bit keys with the rectangle attack.

## Variations

- **Amplified boomerang.** Kelsey, Kohno and Schneier send many pairs $(P, P \oplus \alpha)$ and wait for two pairs whose middle values differ by $\gamma$, a chance of $2^{-n}$ for each pair of pairs. Like the [birthday paradox](/birthday-paradox/), many pairs give many pairs of pairs. The attack needs only chosen plaintexts.
- **Rectangle attack.** Biham, Dunkelman and Keller count over all $\beta$ and $\gamma$ in the amplified setting. With $m$ pairs, the number of right quartets is about $m^2 \, 2^{-n} \, \hat{p}^2 \hat{q}^2$.
- **The switch.** Murphy showed that the two differentials of a boomerang can depend on each other, so that the product estimate fails. Cid, Huang, Peyrin, Sasaki and Song defined the boomerang connectivity table (BCT) of an S-box. It gives the exact chance that a quartet passes one S-box layer at the switch.
- **Related-key boomerangs** use different keys for the different texts of a quartet. See the [related-key attack](/related-key-attack/).

## Pitfalls

- **Independence.** The estimate $p^2 q^2$ multiplies four probabilities as if the events were independent. The toy example shows a rate far above the estimate, and Murphy showed that the estimate can fail in general. Measure the rate on reduced versions when you can.
- **Fixed or summed middle differences.** With fixed $\beta$ and $\gamma$, the estimate is often too low. Sum over all middle differences.
- **Queries.** The basic attack needs a decryption oracle. Without one, use the amplified or rectangle form. It needs about $2^{n/2} / (pq)$ pairs instead of about $1/(p^2 q^2)$ quartets, because a right quartet needs a chance meeting of $2^{-n}$ in the middle.
- **Real ciphers.** Run such experiments only on toy ciphers or reduced rounds that you are allowed to attack.

## Exercises

1. Prove that in any quartet, $(P \oplus P') \oplus (P \oplus Q) \oplus (P' \oplus Q') \oplus (Q \oplus Q') = 0$, and use it to explain why three differences in the middle fix the fourth.
2. Show that for a random permutation, a quartet returns with probability close to $2^{-n}$.
3. Show that $\hat{p}^2 \ge p^2$ for any choice of $\beta$, and give a case where $\hat{p}^2$ is much larger.
4. Run the toy distinguisher with a random permutation in place of the cipher, and find how many quartets you need to tell the two apart.
5. Change the split of the toy cipher to one round and three rounds, and compare the return rates.

## References
