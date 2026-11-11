---
tag: X8G9S4
kind: technique
slug: linear-cryptanalysis
name: Linear cryptanalysis
area: cryptography/symmetric-ciphers
level: advanced
summary: A known-plaintext attack that uses a linear relation of plaintext, ciphertext and key bits that holds with probability far from 1/2. A count over many texts reveals key bits.
prereqs: [block-cipher, s-box, known-plaintext-attack, substitution-permutation-network]
see_also: [differential-cryptanalysis, walsh-hadamard-transform, boolean-function, data-encryption-standard, advanced-encryption-standard, central-limit-theorem, cryptanalysis]
sources:
  - paper: doi:10.1007/3-540-48285-7_33
    title: Mitsuru Matsui, Linear cryptanalysis method for DES cipher, Eurocrypt 1993, LNCS 765, Springer, 1994
    locator: pp. 386-397, Section 3 (Algorithm 1 and Algorithm 2), Lemma 2 and Table 2 (the success rate of Algorithm 1), Lemma 3 (the piling-up lemma), Lemma 5 and Table 3 (the success rate of Algorithm 2), Section 6 (the attacks on 8, 12 and 16 rounds of DES)
  - paper: doi:10.1007/3-540-48658-5_1
    title: Mitsuru Matsui, The first experimental cryptanalysis of the Data Encryption Standard, Crypto 1994, LNCS 839, Springer, 1994
    locator: pp. 1-11, the abstract and Section 1 (two approximations from the best 14-round expression, 26 key bits, 2^43 known plaintexts, the experiment of fifty days on twelve computers)
  - paper: doi:10.1007/BFb0053460
    title: Kaisa Nyberg, Linear approximation of block ciphers, Eurocrypt 1994, LNCS 950, Springer, 1995
    locator: pp. 439-444, Theorem 1 (the fundamental theorem) and Section 2 (the potential and the approximate linear hull)
  - paper: doi:10.1007/s00145-007-9013-7
    title: Ali Aydın Selçuk, On probability of success in linear and differential cryptanalysis, Journal of Cryptology 21(1), 2008
    locator: pp. 131-147, Theorem 2 (the success probability for an a-bit advantage) and Corollary 1 (the number of plaintexts)
  - paper: doi:10.1080/0161-110291890885
    title: Howard M. Heys, A tutorial on linear and differential cryptanalysis, Cryptologia 26(3), 2002
    locator: pp. 189-221, the toy SPN, its linear approximation table, the 3-round approximation with bias -1/32 and the extraction of last-round key bits
  - paper: doi:10.1007/978-3-662-04722-4
    title: Joan Daemen and Vincent Rijmen, The Design of Rijndael, Springer, 2002
    locator: the wide trail strategy and the bound on the number of active S-boxes in four rounds of Rijndael
---

Linear cryptanalysis is a [known-plaintext attack](/known-plaintext-attack/) on [block ciphers](/block-cipher/). The attacker finds a linear relation, an XOR of some plaintext bits, some ciphertext bits and some key bits, that holds with probability a little different from 1/2. With enough known plaintext and ciphertext pairs, a count shows on which side of 1/2 the relation falls, and this gives one bit of key information. Mitsuru Matsui published the method in 1993. In 1994 he broke the full 16-round [DES](/data-encryption-standard/) in an experiment with $2^{43}$ known plaintexts.

**Notation.** $E$ is the cipher with block size $n$. For a mask $a$ and a word $x$, $a \cdot x$ is the parity of the bits of $x$ where $a$ has a 1, that is, the XOR of the selected bits. A linear approximation is a relation $\alpha \cdot P \oplus \beta \cdot C = \kappa \cdot K$ with masks $\alpha$, $\beta$ and $\kappa$. It holds with probability $\frac{1}{2} + \varepsilon$ over random plaintexts, and $\varepsilon$ is its bias. For an $m$-bit S-box $S$, the linear approximation table (LAT) has entry $L[a][b]$ = (the number of $x$ with $a \cdot x = b \cdot S(x)$) $- 2^{m-1}$, so the bias of $a \cdot x \oplus b \cdot S(x) = 0$ is $L[a][b] / 2^m$. $N$ is the number of known plaintexts.

## In plain words

A good cipher makes every output bit depend on the input in a complex way. But some tables in the cipher are a little biased: the sum of some input bits equals the sum of some output bits a little more often than half the time. By chaining such small biases through the rounds, the attacker finds one rule that links some bits of the message, some bits of the result and some bits of the key. The rule is right slightly more than half of the time, or slightly less.

The attacker then collects many messages with their results and counts how often the rule holds. If it holds more often than half the time, the key bits sum to one value, and if less often, to the other. A small bias needs many messages, but the attacker needs only to see them, not to choose them.

## When it applies

- **The attacker sees many plaintext and ciphertext pairs.** The plaintexts do not need to be chosen. They must be close to random, or the attacker must know their distribution.
- **An approximation with a large enough bias exists.** The attack needs about $1/\varepsilon^2$ pairs. If $1/\varepsilon^2$ is larger than $2^n$, there are not enough distinct plaintexts.
- **Key addition by XOR.** If the key enters by XOR, the key bits appear in the relation as a constant $\kappa \cdot K$, so the size of the bias does not depend on the key, only its sign does.
- **Not when the designers proved bounds.** The wide trail strategy of [AES](/advanced-encryption-standard/) gives at least 25 active S-boxes in any 4-round linear trail, which makes the bias of every trail too small to use.

## The template

**Approximations of S-boxes.** An S-box is a set of [Boolean functions](/boolean-function/). The LAT entry $L[a][b]$ measures the correlation of the Boolean function $b \cdot S$ with the linear function $a \cdot x$. A whole row of the LAT is a [Walsh-Hadamard transform](/walsh-hadamard-transform/) of $b \cdot S$. An entry far from 0 gives a useful approximation of one S-box.

**The piling-up lemma.** To chain approximations of several S-boxes into an approximation of the cipher, Matsui uses his Lemma 3. Let $X_1, \ldots, X_k$ be independent random bits with $\Pr[X_i = 0] = \frac{1}{2} + \varepsilon_i$. Then

$$\Pr[X_1 \oplus \cdots \oplus X_k = 0] = \frac{1}{2} + 2^{k-1} \prod_{i=1}^{k} \varepsilon_i.$$

*Proof.* For a bit $X$, $\mathbb{E}[(-1)^X] = \Pr[X = 0] - \Pr[X = 1] = 2\varepsilon$. The value $(-1)^{X_1 \oplus \cdots \oplus X_k}$ is the product of the values $(-1)^{X_i}$. The bits are independent, so the expectation of the product is the product of the expectations, $\prod_i 2\varepsilon_i = 2^k \prod_i \varepsilon_i$. The bias of the XOR is half of this value. $\square$

The independence is an assumption. In a real cipher, the inputs of the S-boxes in different rounds depend on each other through the key schedule and the data. The lemma gives the bias of one trail, a chain of masks through the rounds, on average over independent round keys.

**Algorithm 1.** Take an approximation $\alpha \cdot P \oplus \beta \cdot C = \kappa \cdot K$ with bias $\varepsilon$. Let $T$ be the number of pairs with $\alpha \cdot P \oplus \beta \cdot C = 0$. If $T > N/2$, guess $\kappa \cdot K = 0$ when $\varepsilon > 0$, or 1 when $\varepsilon < 0$. If $T \le N/2$, guess the other value. This gives one bit of the key.

**Algorithm 2.** Take an approximation over $r - 1$ rounds, from the plaintext to the input $U$ of the last round. Guess the bits $g$ of the last round key that enter the S-boxes where the mask $\gamma$ on $U$ is not zero. For each guess, undo the last round on these S-boxes and count. With the right guess, the relation has bias about $\varepsilon$. With a wrong guess, it looks like a random relation, with a bias close to 0.

```pseudo id=main
MATSUI-ALGORITHM-2(pairs (P₁, C₁) .. (P_N, C_N), masks α and γ)
L1  for each pair (P, C), count it by α·P and the bits of C under the target S-boxes
L2  for each guess g of the target subkey bits do
L3      T_g ← 0
L4      for each pair (P, C) do
L5          U ← S⁻¹(C ⊕ g) on the target S-boxes
L6          if α·P ⊕ γ·U = 0 then T_g ← T_g + 1
L7      ε_g ← T_g / N − 1/2
L8  return the g with the largest |ε_g|
```

Line L1 is an optimization from the DES attack: pairs that agree on $\alpha \cdot P$ and on the target ciphertext bits give the same answer for every guess, so the loop of line L4 can run over the cells of the count instead of over all pairs. The sign of $\varepsilon_g$ for the best guess then gives the key bit $\kappa \cdot K$, as in Algorithm 1.

**Cost.** By the [central limit theorem](/central-limit-theorem/), $T$ is about normal with mean $N(\frac{1}{2} + \varepsilon)$ and standard deviation about $\sqrt{N}/2$. Algorithm 1 is wrong when $T$ falls on the wrong side of $N/2$, so its success rate is about $\Phi(2\sqrt{N}\,|\varepsilon|)$, where $\Phi$ is the standard normal distribution function. This is Lemma 2 of Matsui 1993. His Table 2 gives the values for $N = c / \varepsilon^2$:

| $c$ | 1/4 | 1/2 | 1 | 2 |
|---|---|---|---|---|
| success rate of Algorithm 1 | 84.1% | 92.1% | 97.7% | 99.8% |

Algorithm 2 must also separate the right guess from all wrong guesses, so it needs a larger constant. Table 3 of Matsui 1993 gives 48.6%, 78.5%, 96.7% and 99.9% for $c$ = 2, 4, 8 and 16, for one active S-box of DES in the last round. Selçuk gave a general formula. If the right guess must rank among the best $2^{m-a}$ of the $2^m$ guesses, and every wrong guess has bias 0, then the success probability is $\Phi(2\sqrt{N}\,|\varepsilon| - \Phi^{-1}(1 - 2^{-a-1}))$. The time is $N$ steps to fill the count, and $2^m$ times the number of cells for line L2 to line L7.

**About the code.** The Python code of this page attacks the toy cipher of Heys, a 4-round substitution-permutation network on 16 bits with five independent 16-bit round keys. It is for study only and is not constant time. Do not use any of it to protect real data. Use AES from a validated library such as OpenSSL instead.

## Classic examples

### The toy cipher of Heys

The toy cipher is a [substitution-permutation network](/substitution-permutation-network/) with four 4-bit [S-boxes](/s-box/) in each round, all equal to E 4 D 1 2 F B 8 3 A 6 C 5 9 0 7, and a bit permutation that sends bit $4i + j$ to bit $4j + i$. The LAT has $L$[B][4] = +4 and $L$[4][5] = $-4$, so these two approximations have biases $+1/4$ and $-1/4$.

| round | S-box | input mask | output mask | bias |
|---|---|---|---|---|
| 1 | $S_{12}$ | B | 4 | $+1/4$ |
| 2 | $S_{22}$ | 4 | 5 | $-1/4$ |
| 3 | $S_{32}$ | 4 | 5 | $-1/4$ |
| 3 | $S_{34}$ | 4 | 5 | $-1/4$ |

The four approximations chain into a relation between the plaintext mask $\alpha$ = 0B00 and the mask $\gamma$ = 0505 on the input $U$ of the round-4 S-boxes. The piling-up lemma gives the bias $2^3 \cdot \frac{1}{4} \cdot \left(-\frac{1}{4}\right)^3 = -\frac{1}{32}$. For the three key sets in the tests, an exact count over all $2^{16}$ plaintexts of three rounds gives a bias of exactly $-1/32$, key bits included.

With Algorithm 1 and $N = 1/\varepsilon^2 = 1024$ known plaintexts, Lemma 2 predicts the success rate $\Phi(2) \approx 0.977$, and the tests require success for at least 36 of 40 random keys.

Algorithm 2 runs on the full 4 rounds with $N = 8/\varepsilon^2 = 8192$ known plaintexts and guesses the 8 bits of the last round key on S-boxes 2 and 4. Take the round keys 1234, 9ABC, 5A5A, 0F0F and 7777, so the target is 77. In one run, the guess 77 gets $|\varepsilon_g| = 0.024$, and the next guesses 97 and C7 get 0.0223 and 0.0216. Over 100 random keys, the right guess ranks first 81 times and in the top four 96 times. The formula of Selçuk predicts 0.997 for $a = m = 8$, so the toy does worse than the model. The reason is that the wrong guesses do not have bias 0: with all $2^{16}$ plaintexts, guess 76 has bias 0.0234, close to the bias 1/32 of the right guess.

### DES

Matsui found the best linear approximations of DES rounds with a computer search. In 1993 he broke 8-round DES with $2^{21}$ known plaintexts in 40 seconds and 12-round DES with $2^{33}$ known plaintexts in 50 hours. For 16 rounds, Lemma 4 gave an estimate of $2^{47}$ known plaintexts. He also showed that the method can work with ciphertexts only, if the plaintexts are English text in ASCII, for 8-round DES. In 1994 he used two approximations from the best 14-round expression, each of which gives 13 key bits, and found the rest of the 56-bit key by search. With $2^{43}$ known plaintexts, twelve computers found the key in fifty days: forty days to make the plaintexts and ciphertexts, and ten days for the key search.

### AES and the wide trail strategy

In Rijndael, any linear trail over four rounds has at least 25 active S-boxes. The largest LAT entry of the AES S-box gives a bias of $2^{-4}$ for one S-box. The piling-up lemma then bounds the bias of a 4-round trail by $2^{24} \cdot 2^{-100} = 2^{-76}$, so a trail would need about $2^{152}$ plaintexts, far more than the $2^{128}$ that exist.

## Variations

- **Linear hulls.** Nyberg showed that the average over the keys of $\varepsilon^2$ for an approximation equals the sum of the squared biases of all the trails with the same input and output masks. She called this set the approximate linear hull. One trail can underestimate the true bias, and she showed that Matsui underestimated the success of Algorithm 2.
- **Multiple linear cryptanalysis** uses several approximations at once to reduce the data.
- **Differential-linear attacks** join a short differential from [differential cryptanalysis](/differential-cryptanalysis/) with a linear approximation.
- **Zero-correlation attacks** use approximations with bias exactly 0, the linear version of an impossible differential.
- **Ciphertext-only attacks.** If the plaintexts are not uniform, for example ASCII text, a relation on ciphertext bits alone can have a bias.

## Pitfalls

- **One trail is not the hull.** Many trails can connect the same masks. Their biases add with signs that depend on the key, so for one fixed key the true bias can be larger or smaller than the bias of the best trail.
- **The independence assumption.** The piling-up lemma needs independent inputs. In a real cipher it gives only an estimate.
- **Wrong keys are not random.** The success formulas assume that every wrong guess has bias 0. In small ciphers, a wrong guess that differs from the right one in a few bits can keep a large part of the bias, as the toy example shows.
- **Too few pairs.** With much less than $1/\varepsilon^2$ pairs, the count is noise. The constant grows with the number of guessed key bits.
- **Real ciphers.** Run such experiments only on toy ciphers or reduced rounds that you are allowed to attack.

## Exercises

1. Compute the LAT of a 3-bit S-box that is a permutation. Show that every entry is even and that, for each $b \ne 0$, the sum of the squares of the entries in column $b$ is $2^{2m-2}$, by Parseval's theorem.
2. Use the piling-up lemma to show that if one of the $\varepsilon_i$ is 0, the XOR has bias 0.
3. Find two dependent bits, each with bias $1/4$, whose XOR has a bias different from the value of the piling-up lemma.
4. In the toy example, derive the masks 0400, 0404 and 0505 at the inputs of rounds 2, 3 and 4 from the table of the four approximations.
5. Run Algorithm 2 on the toy cipher with $N = 2/\varepsilon^2$, $4/\varepsilon^2$ and $8/\varepsilon^2$ over many random keys, and compare the success rates with the formula of Selçuk.

## References
