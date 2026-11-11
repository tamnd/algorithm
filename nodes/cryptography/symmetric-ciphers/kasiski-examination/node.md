---
tag: ZTGXR5
kind: algorithm
slug: kasiski-examination
name: Kasiski examination
aliases:
- Kasiski test
area: cryptography/symmetric-ciphers
level: intro
summary: Find the period of a Vigenère-type cipher from repeated ciphertext pieces. Their distances are mostly multiples of the period, so the factor that divides most of them gives it.
solves: [cipher-breaking]
model: word-ram
complexity:
  vars: {n: the number of letters of the ciphertext, P: the largest period tried}
  time: {worst: Θ(n·P), best: Θ(n + P)}
  space: {extra: Θ(n)}
properties: {deterministic: true}
prereqs: [vigenere-cipher, greatest-common-divisor]
see_also: [index-of-coincidence, frequency-analysis, longest-repeated-substring, suffix-array, ciphertext-only-attack, cipher-breaking]
sources:
  - paper: "Friedrich W. Kasiski, Die Geheimschriften und die Dechiffrir-Kunst, E. S. Mittler und Sohn, Berlin, 1863"
    locator: the method of repeated sequences for ciphers with a periodic key
  - book: isbn:9781138197015
    title: Douglas R. Stinson and Maura B. Paterson, Cryptography, Theory and Practice, fourth edition, CRC Press, 2018
    locator: Section 2.2.3 (cryptanalysis of the Vigenère cipher, the Kasiski test)
  - book: isbn:9780684831305
    title: David Kahn, The Codebreakers, revised edition, Scribner, 1996
    locator: the account of Kasiski and of his solution of the periodic polyalphabetic cipher
  - book: isbn:9780385495318
    title: Simon Singh, The Code Book, Anchor Books, 2000
    locator: Chapter 2, Le Chiffre Indéchiffrable (Babbage and Kasiski)
---

Kasiski examination finds the period $m$ of a periodic polyalphabetic cipher such as the [Vigenère cipher](/vigenere-cipher/). It looks for pieces of ciphertext, usually of three letters, that occur more than once. When the same plaintext piece meets the same position of the key, it gives the same ciphertext piece, and then the distance between the two copies is a multiple of $m$. So the period divides most of the distances. Chance matches, the *false hits*, add distances that $m$ does not divide, so the plain greatest common divisor often fails, and a count of divisors is more robust. Friedrich Kasiski published the method in 1863. It uses *repeats*; the [index of coincidence](/index-of-coincidence/) is the other classical test, and it uses *statistics*.

## In plain words

In English, words such as THE and AND appear again and again. A Vigenère cipher with a key of five letters uses the same shift on every fifth letter. So when a THE falls on the same part of the key twice, it turns into the same three cipher letters both times. The gap between the two copies is then a multiple of five.

A code breaker lists the repeated groups of three letters in the ciphertext and measures the gaps. Most gaps share the factor five, and that gives the length of the key. A few gaps come from chance, and they share nothing. So the code breaker does not ask which number divides all gaps, but which number divides most of them.

## The problem

Let $c = c_0 c_1 \ldots c_{n-1}$ be the letters of a ciphertext that a periodic cipher with an unknown period $m \ge 2$ produced from English text. A *repeat* of length $\ell$ is a pair of positions $i < j$ with $c_i \ldots c_{i+\ell-1} = c_j \ldots c_{j+\ell-1}$. The task is to estimate $m$ from the repeats. This is a step of a [ciphertext-only attack](/ciphertext-only-attack/); after it, each column of letters $m$ apart is a [Caesar cipher](/caesar-cipher/) that falls to [frequency analysis](/frequency-analysis/).

## The algorithm

```pseudo id=main
KASISKI(c, ℓ, P)                           ▷ ℓ = the repeat length, P = the largest period tried
L1  for i ← 0 to n - ℓ do
L2      append i to the list of positions of the piece c[i .. i+ℓ-1]
L3  D ← the distances q(t+1) - q(t) between consecutive positions of each piece that occurs twice or more
L4  for m ← 2 to P do count(m) ← the number of distances in D that m divides
L5  return the m that maximizes count(m) - |D|/m
```

Line L5 is the choice that this page uses. A distance from a true repeat is a multiple of $m$. A distance from a false hit behaves like a random number, which a given $m$ divides with a chance of about $1/m$, so $|D|/m$ is the count that $m$ gets by chance. Without the correction, a small number such as 2 would win, because it divides about half of all numbers. Kasiski's own method and the textbook version take the greatest common divisor of the distances, or of most of them, and the function `gcd_of_distances` gives that as well.

The code is for study only. It attacks classical ciphers, which give no protection, and it is not constant time. To protect real data, use AES-GCM or ChaCha20-Poly1305 from libsodium, from a FIPS 140 validated module, or from the standard library of your language.

## Example

Encrypt the first two sentences of the Declaration of Independence (499 letters) with the Vigenère key LEMON. The ciphertext has 32 trigrams that occur twice or more, which give 45 distances. Some of them:

| cipher trigram | positions | distances | plaintext |
|---|---|---|---|
| XTS | 6, 186, 311, 336, 391, 456 | 180, 125, 25, 55, 65 | THE each time |
| HUP | 68, 103, 153, 223, 243, 478 | 35, 50, 70, 20, 235 | THE each time |
| HQE, QEH, EHL, HLP | 166 to 169, 381 to 384 | 215 each | DEQUAL, from "created equal" |
| SPZ | 8, 93, 354 | 85, 261 | ECO, ECO, FEV |
| ZSP | 37, 97, 353 | 60, 256 | NEC, NEC, LFE |
| TSZ | 250, 312 | 62 | ION, HEM |

The first three rows are true repeats: the same plaintext at the same key position. The last three rows hold the three false hits, 261, 256 and 62, where different plaintext gave the same ciphertext by chance. Because of them, the gcd of all 45 distances is 1. Without them, the gcd of the other 42 distances is 5.

The counts of line L4, and the score of line L5:

| $m$ | 2 | 3 | 4 | 5 | 6 | 10 | 12 | 15 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| count | 22 | 17 | 15 | 42 | 12 | 20 | 11 | 16 | 14 |
| count − 45/$m$ | −0.5 | 2.0 | 3.8 | 33.0 | 4.5 | 15.5 | 7.2 | 13.0 | 11.8 |

So the period is 5. The multiples 10, 15 and 20 come next, as they should. The index of coincidence gives 5 as well on the same ciphertext (see the [Vigenère cipher](/vigenere-cipher/) page), and the chi-squared test on each of the five columns then gives the key LEMON.

**Repeats against statistics.** The two tests use different evidence, and each one is stronger in a different case. Over 200 random keys for each line, with periods up to 25 tried:

| key length | text | Kasiski right | index of coincidence right |
|---|---|---|---|
| 2 to 6 | 499 letters | 196 | 200 |
| 7 to 12 | 499 letters | 199 | 200 |
| 13 to 20 | 499 letters | 182 | 199 |
| 3 to 8 | first 150 letters | 116 | 95 |

With long keys, few English trigrams meet the same key position twice, so Kasiski has little evidence, while the column index still works. With a short text, the columns are too short for a stable index, but a few true repeats still point to the period. In practice, code breakers use both.

## Correctness

**Lemma.** Let a periodic cipher with period $m$ encrypt each letter $p_j$ to $c_j = f_{j \bmod m}(p_j)$. If $p_i \ldots p_{i+\ell-1} = p_j \ldots p_{j+\ell-1}$ and $m$ divides $j - i$, then $c_i \ldots c_{i+\ell-1} = c_j \ldots c_{j+\ell-1}$. Indeed, $(i + t) \bmod m = (j + t) \bmod m$ for each $t$, so the same functions act on the same letters.

So each true repeat gives a distance that is a multiple of $m$. The converse is false: equal ciphertext pieces can come from different plaintext pieces, and those distances carry no information. For a ciphertext whose trigrams were uniform, about $\binom{n}{2} / 26^3$ pairs of positions match by chance; for $n = 499$ this is about 7, of which the example shows 3 between consecutive positions. If all distances come from true repeats, their gcd is a multiple of $m$ (it can be a proper multiple, for example when all repeats happen to be $2m$ apart). So the method finds a multiple of the period in the clean case, and it is a heuristic when false hits occur. Lines L1 to L3 compute exactly the distances between consecutive occurrences; the full proof is in the proof file below.

## Complexity

With a hash map keyed by the piece, lines L1 and L2 take $\Theta(n)$ expected time for a fixed $\ell$. Line L3 gives fewer than $n$ distances, because each position starts at most one piece. Line L4 tests each distance against each $m \le P$, so it takes $\Theta(|D| \cdot P)$ time, which is $\Theta(nP)$ in the worst case (a text of one repeated letter) and $\Theta(P)$ when there is no repeat. So the whole method takes between $\Theta(n + P)$ and $\Theta(nP)$ time. A [suffix array](/suffix-array/) finds all repeats of every length in $O(n \log n)$ time, which helps when longer repeats are wanted.

| claim | value |
|---|---|
| finding the repeats of length $\ell$ | $\Theta(n)$ expected |
| the counts for $m \le P$ | $\Theta(\lvert D \rvert \cdot P)$, at most $\Theta(nP)$ |
| space | $\Theta(n)$ |

## Properties

- **Repeats, not statistics.** The method uses equal pieces of ciphertext. It needs no table of English frequencies, only the fact that the plaintext repeats itself.
- **It finds a multiple.** True repeats give multiples of the period, so the period found can be a multiple or a divisor of a number that fits. Line L5 favours the right one, but no rule is safe.
- **Sensitive to false hits.** The plain gcd fails with one false hit. Longer repeats, of four or five letters, give fewer false hits but also fewer true ones.
- **Useless for non-periodic keys.** With an autokey, a running key or a [one-time pad](/one-time-pad/), there is no period to find.

## Variants and improvements

- **The plain gcd.** Take the gcd of the distances of the longest or most frequent repeats only. This is the textbook form, and it works well by hand when long repeats exist.
- **Factor tallies.** Count how many distances each small number divides, as here.
- **Repeats in columns.** After a guess $m$, the [index of coincidence](/index-of-coincidence/) of the columns confirms it.
- **Longer repeats.** Use $\ell = 4$ or $5$ when the text is long. A repeat of length $\ell$ by chance has a probability of about $26^{-\ell}$ per pair of positions.

## When to use it

Use it as the first step against a cipher that you suspect is periodic polyalphabetic, together with the index of coincidence. It works best on texts of moderate length with short keys, and it works by hand.

## Pitfalls

- **Taking the gcd of all distances.** A single false hit gives the answer 1, as in the example.
- **Choosing the most common factor without a correction.** The number 2 divides about half of all distances, so it wins too often.
- **Overlapping repeats.** A long repeat gives several overlapping trigram repeats with the same distance (HQE, QEH, EHL, HLP in the example). They are one piece of evidence, not four. Here the score counts them separately, which is a known bias.
- **Treating Kasiski as proof.** It gives a guess for $m$; confirm it with the index of coincidence or by breaking the columns.

## Implementations

## History

Friedrich Wilhelm Kasiski, a Prussian infantry officer, published the method in 1863 in "Die Geheimschriften und die Dechiffrir-Kunst" (Secret writing and the art of deciphering). It was the first published general solution of the periodic polyalphabetic cipher, which had resisted attack since the 16th century. According to Kahn and Singh, Charles Babbage had found a similar solution in the 1850s, but he did not publish it. In 1922 William Friedman gave the statistical test by the index of coincidence, which complements the method.

## References
