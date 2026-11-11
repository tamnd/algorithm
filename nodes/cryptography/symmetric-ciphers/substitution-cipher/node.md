---
tag: QQJETY
kind: algorithm
slug: substitution-cipher
name: Substitution cipher
aliases:
- monoalphabetic substitution cipher
area: cryptography/symmetric-ciphers
level: intro
summary: Replace each letter by its image under a secret permutation of the alphabet. There are 26! ≈ 2^88.4 keys, yet frequency analysis, or hill climbing with an n-gram score, breaks it.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of characters of the message}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
prereqs: [caesar-cipher, permutation]
see_also: [frequency-analysis, hill-climbing, affine-cipher, playfair-cipher, vigenere-cipher, ciphertext-only-attack, shannon-entropy, cipher-breaking]
sources:
  - paper: doi:10.1002/j.1538-7305.1949.tb00928.x
    title: Claude E. Shannon, Communication theory of secrecy systems, Bell System Technical Journal 28(4), 1949
    locator: Part II (equivocation, the unicity distance and the simple substitution example)
  - book: isbn:9781138197015
    title: Douglas R. Stinson and Maura B. Paterson, Cryptography, Theory and Practice, fourth edition, CRC Press, 2018
    locator: Section 2.1.2 (the substitution cipher), Section 2.2.2 (its cryptanalysis), Section 3.5 (spurious keys and unicity distance)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 7, Section 7.3 (simple substitution ciphers and the unicity distance)
  - paper: "Thomas Jakobsen, A fast method for cryptanalysis of substitution ciphers, Cryptologia 19(3), 1995"
    locator: the key search by swaps of two letters, scored by digram statistics
  - book: isbn:9780684831305
    title: David Kahn, The Codebreakers, revised edition, Scribner, 1996
    locator: Chapters 2 to 4 (monoalphabetic substitution and its solution by frequency counts)
---

The simple substitution cipher replaces each letter of the message by its image under a secret [permutation](/permutation/) $\pi$ of the alphabet. The key space has $26! \approx 4.03 \times 10^{26} \approx 2^{88.4}$ keys, far too many to try one by one. Yet the cipher keeps the letter statistics of the language, so [frequency analysis](/frequency-analysis/) breaks it by hand, and [hill climbing](/hill-climbing/) on an n-gram score breaks it by computer in under a second. Shannon's formula gives its unicity distance: about 28 letters of English ciphertext are enough, in principle, to fix the key.

## In plain words

Write the alphabet in a row, and under it write the same letters in a secret mixed order. To lock a message, replace each letter by the letter under it. To unlock, look the other way. The secret is the mixed row.

There are so many mixed rows that no computer can try them all. But the lock does not hide how often each letter appears. In English, E is the most common letter and T the next. In the locked text, the most common letter is almost surely E in disguise. Common pairs and triples, such as TH and THE, also show through. A code breaker guesses a few letters from these counts, sees part words appear, and fills in the rest. A program does the same: it starts from a guess, swaps two letters of the guess, and keeps the swap when the text looks more like English.

## The problem

Identify A to Z with $\mathbb{Z}_{26}$. The key space is the [symmetric group](/symmetric-group/) $S_{26}$ of all bijections $\pi : \mathbb{Z}_{26} \to \mathbb{Z}_{26}$, with $|S_{26}| = 26!$. The cipher acts letter by letter:

$$E_\pi(p_1 \ldots p_n) = \pi(p_1) \ldots \pi(p_n), \qquad D_\pi(c_1 \ldots c_n) = \pi^{-1}(c_1) \ldots \pi^{-1}(c_n).$$

The code writes a key as a string of the 26 letters: the letter at index $i$ is $\pi(i)$. It keeps the case and copies other characters. This is an instance of [symmetric encryption](/symmetric-encryption/). The attack problem is a [ciphertext-only attack](/ciphertext-only-attack/): find $\pi^{-1}$, or most of it, from $E_\pi(P)$ when $P$ is English.

## The algorithm

```pseudo id=main
SUBSTITUTION-ENCRYPT(P, π)                 ▷ π is a permutation of the 26 letters
L1  build the table T with T[x] = π(x) for each letter x
L2  for i ← 1 to n do
L3      ci ← T[pi]
L4  return C = c1 ... cn
```

Decryption runs the same procedure with $\pi^{-1}$. The attack searches for the decryption key $\sigma = \pi^{-1}$ that maximizes a score $S$: the log likelihood of $\sigma(C)$ under a trigram model of English.

```pseudo id=attack
HILL-CLIMB(C, R, M)                        ▷ R restarts, M = the patience
L5  for r ← 1 to R do
L6      σ ← the key that maps the j-th most common cipher letter to the j-th most common English letter
L7      if r > 1 then apply a few random swaps to σ
L8      s ← S(σ(C)), stale ← 0
L9      while stale < M do
L10         σ′ ← σ with the images of two random letters swapped
L11         if S(σ′(C)) > s then σ ← σ′, s ← S(σ′(C)), stale ← 0
L12         else stale ← stale + 1
L13     keep σ if s is the best score so far
L14 return the best σ
```

The score $S$ sums $\log P(z \mid x y)$ over the trigrams $xyz$ of the candidate text. The trigram probabilities come from the Gettysburg Address (1,149 letters), smoothed toward bigram probabilities and toward the letter table of Beker and Piper, so that no probability is zero. The attack text is a different one: the first two sentences of the Declaration of Independence (499 letters). The code counts the trigrams of $C$ once, so each score costs one pass over the distinct trigrams.

HILL-CLIMB is a heuristic. It stops at a local maximum of $S$, and even the global maximum need not be the true key, because the model of English is only an estimate. The [local search](/local-search/) page discusses the general method, and [simulated annealing](/simulated-annealing/) is a common variant that sometimes accepts a worse key to leave a local maximum.

The code is for study only. It is not constant time, and the cipher gives no protection. To protect real data, use AES-GCM or ChaCha20-Poly1305 from libsodium, from a FIPS 140 validated module, or from the standard library of your language.

## Example

**Encryption.** With the key QWERTYUIOPASDFGHJKLZXCVBNM (the top row, middle row and bottom row of a keyboard), FLEE AT ONCE becomes YSTT QZ GFET: F is the 6th letter and the 6th key letter is Y, L becomes S, E becomes T, and so on.

**The attack.** Encrypt the 499-letter sample with the random key GTXVIBPJWSKAZHUCRDQNLMFYOE. The ciphertext starts FJIHWHNJIXULDQIUBJLZGHIMIHNQ. The sample uses 23 different letters (J, X and Z do not occur). The most common plaintext letters are E (78 times), T (59), A (42) and H (40). HILL-CLIMB with 8 restarts and a patience of 1,000 swaps returns a key that decrypts the start as

WHENINTHECOURSEOMHUGANEVENTSITBECOGESNECESSARYMORONEPEOPLETO

20 of the 23 letters are right, and 95.2% of the text is right. The three wrong letters are F, G and M, which the key permutes in a cycle (OF HUMAN reads OM HUGAN). The model gives this wrong text a higher score than the true text: $-1343.1$ against $-1355.2$. So more search would not help; a better model of English would. A reader fixes the last three letters at a glance.

Over three random keys, the attack decrypts 95.2%, 89.6% and 84.4% of the letters correctly. The tests require at least 80% of the letters, and at least 17 of the 23 letters of the key.

**Unicity distance.** Shannon's estimate of the length of ciphertext that fixes the key is $U = H(K)/D$, where $H(K)$ is the [entropy](/shannon-entropy/) of the key and $D$ is the redundancy of the language in bits per letter. For a uniform key, $H(K) = \lg 26! \approx 88.38$ bits. With $26$ letters the maximum rate is $\lg 26 \approx 4.70$ bits per letter. This page takes the rate of English as $r = 1.5$ bits per letter, the value that Menezes, van Oorschot and Vanstone use, so $D = 4.70 - 1.5 \approx 3.2$. Then

$$U \approx \frac{88.38}{3.2} \approx 27.6,$$

about 28 letters. With $r = 1.0$, $D \approx 3.7$ and $U \approx 23.9$. The estimate assumes Shannon's random cipher model, and it says only that the key is unique in principle, not that a fast algorithm finds it. In practice, hill climbing needs a few hundred letters with a weak model, and less with good quadgram statistics. The [ciphertext-only attack](/ciphertext-only-attack/) page derives the formula.

## Correctness

**Encryption.** Line L1 builds $T = \pi$, and lines L2 and L3 apply it to each letter. Because $\pi$ is a bijection, $\pi^{-1}$ exists and $D_\pi(E_\pi(P)) = P$ for each message $P$.

**The attack.** HILL-CLIMB always returns a permutation, because a swap of two images keeps a permutation. Each restart ends: the score takes at most $26!$ values and strictly rises at each accepted swap, and each rejected swap raises the counter `stale`, which reaches $M$ after at most $M$ rejections in a row. But the returned key is only a local maximum of $S$ for single swaps. No guarantee that it is the true key exists, and the example shows a case where it is not. The full proof of the encryption claim and of the termination of the attack is in the proof file below.

## Complexity

Line L1 takes $\Theta(1)$ time (26 entries), and the loop of line L2 does one table lookup for each character. So encryption and decryption take $\Theta(n)$ time in each case on the [word RAM](/word-ram/) and $\Theta(1)$ extra space for the table.

For the attack, let $t \le n - 2$ be the number of distinct trigrams of the ciphertext. Each score costs $\Theta(t)$. A restart does at most $M$ swaps after its last improvement, and there are at most as many improvements as distinct scores that it visits. So one restart costs $\Theta(t)$ times the number of swaps it tries. On the 499-letter sample, one run of the attack takes about one second in Python.

| claim | value |
|---|---|
| encryption and decryption, each case | $\Theta(n)$ |
| extra space | $\Theta(1)$ |
| keys | $26! \approx 2^{88.4}$ |
| one score in the attack | $\Theta(t)$, $t$ distinct trigrams |

## Properties

- **Monoalphabetic.** The same plaintext letter always gives the same ciphertext letter. The multiset of letter counts is kept, only renamed. This is the leak that frequency analysis uses.
- **Repeated patterns survive.** A word with a pattern of repeated letters, such as PEOPLE (the pattern ABCABD), keeps the pattern. Codebreakers use such pattern words as cribs.
- **The key space is large but useless.** A key space of $2^{88.4}$ would resist a search of all keys. The weakness is structural, which is why the size of the key space alone never proves security.
- **Closed under composition.** Two substitutions in a row are one substitution, $\pi_2 \circ \pi_1$.

## Variants and improvements

- **Keyword alphabets.** The key is built from a keyword: write the keyword without repeated letters, then the other letters in order. This is easy to remember but has fewer keys.
- **Special cases.** The [Caesar cipher](/caesar-cipher/) (26 keys) and the [affine cipher](/affine-cipher/) (312 keys) are substitutions of a special form.
- **Homophonic substitution.** Each common letter has several cipher symbols, chosen at random, to flatten the counts. Digram statistics still leak.
- **Polyalphabetic substitution.** The [Vigenère cipher](/vigenere-cipher/) changes the alphabet from letter to letter, in a cycle.
- **Digraphic substitution.** The [Playfair cipher](/playfair-cipher/) substitutes pairs of letters, and the [Hill cipher](/hill-cipher/) substitutes blocks by a linear map.

## When to use it

Use it to teach that a large key space is not enough, and to teach frequency analysis and local search. Puzzles (cryptograms) use it. Never use it to protect data.

## Pitfalls

- **A key with a repeated letter.** Then two letters map to one and decryption fails. Check that the key is a permutation (test `test_bad_keys`).
- **Decrypting with the key instead of its inverse.** $\pi$ and $\pi^{-1}$ differ unless $\pi$ is an involution. The test `test_round_trip_and_oracle` checks that `invert_key` inverts.
- **Training and testing the score on the same text.** A model built from the attacked text recovers it too easily, so the result says nothing. Here the model comes from the Gettysburg Address and the attack runs on the Declaration of Independence.
- **Trusting the best score.** The best key found may differ from the true key in rare letters, or in letters that the model can not separate, as the F, G, M cycle of the example shows. Read the result.
- **Too little ciphertext.** Below the unicity distance many keys give English-like text. Even above it, a short text leaves the rare letters undetermined: here J, X and Z do not occur at all.

## Implementations

## History

Monoalphabetic substitution is old, and its solution by letter frequencies is first described in the 9th century treatise of al-Kindi; see [frequency analysis](/frequency-analysis/) for the sources. Kahn traces its use through the cipher secretaries of the Renaissance states. Shannon defined the unicity distance in 1949, in "Communication theory of secrecy systems", and used simple substitution as an example. Computer attacks by local search followed later; Jakobsen published a fast attack by swaps of two key letters, scored by digram statistics, in Cryptologia in 1995.

## References
