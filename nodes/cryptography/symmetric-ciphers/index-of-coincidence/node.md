---
tag: SQVP90
kind: concept
slug: index-of-coincidence
name: Index of coincidence
aliases:
area: cryptography/symmetric-ciphers
level: intro
summary: The chance that two letters drawn from a text are equal. About 0.066 for English and 1/26 ≈ 0.038 for random letters, so it tells one alphabet from many and estimates the key length.
prereqs: [frequency-analysis]
see_also: [kasiski-examination, vigenere-cipher, columnar-transposition-cipher, substitution-cipher, shannon-entropy, birthday-paradox, cipher-breaking]
sources:
  - paper: "William F. Friedman, The Index of Coincidence and Its Applications in Cryptography, Riverbank Publication No. 22, Riverbank Laboratories, Geneva, Illinois, 1922"
    locator: the definition of the index and its use to find the number of alphabets of a cipher
  - book: isbn:9781138197015
    title: Douglas R. Stinson and Maura B. Paterson, Cryptography, Theory and Practice, fourth edition, CRC Press, 2018
    locator: Section 2.2.3 (the index of coincidence, its value for English, and the key length of the Vigenère cipher), Table 2.1 (letter probabilities)
  - book: isbn:9780684831305
    title: David Kahn, The Codebreakers, revised edition, Scribner, 1996
    locator: the chapter on Friedman and the Riverbank Laboratories (the index of coincidence)
---

The *index of coincidence* of a text is the probability that two letters drawn at random from it, at two different positions, are the same letter. For English it is about $0.066$; for letters drawn uniformly from 26 it is $1/26 \approx 0.0385$. The index does not change when the letters are renamed or moved, so it sees through a [substitution](/substitution-cipher/) or a [transposition](/columnar-transposition-cipher/), but it drops when several alphabets are mixed. William Friedman introduced it in 1922. It gives the length of a [Vigenère](/vigenere-cipher/) key from statistics, while [Kasiski examination](/kasiski-examination/) gets it from repeated pieces.

## In plain words

Pick two letters from a text, from two different places, and ask if they are the same. In English this happens about once in fifteen tries, because E, T and A are so common. In a jumble where every letter is as common as every other, it happens only once in twenty six tries.

Renaming the letters, as a simple substitution does, keeps this number, because the common letters stay common under new names. Moving letters around keeps it too. But a cipher that uses several alphabets in turn spreads each common letter over several cipher letters, and the number falls toward one in twenty six. So the number tells a code breaker how many alphabets are in use, and from that, how long the key is.

## The idea

Let a text have $n$ letters, and let $f_i$ be the number of times the $i$-th letter of the alphabet occurs. There are $n(n-1)$ ordered pairs of distinct positions, and $f_i(f_i - 1)$ of them hold the letter $i$ twice. So

$$\mathrm{IC} = \frac{\sum_{i=0}^{25} f_i (f_i - 1)}{n (n - 1)}.$$

**The expected value.** If the letters are drawn independently with probabilities $p_0, \ldots, p_{25}$, then a pair of distinct positions holds the letter $i$ twice with probability $p_i^2$. So $\mathbb{E}[f_i(f_i - 1)] = n(n-1) p_i^2$, and

$$\mathbb{E}[\mathrm{IC}] = \sum_i p_i^2 =: \kappa.$$

Drawing without replacement, with $f_i - 1$ in place of $f_i$, is what makes this exact for every $n \ge 2$. The value $\kappa$ is the [collision probability](/birthday-paradox/) of the letter distribution.

- **English.** The letter table of Beker and Piper, as printed by Stinson and Paterson (Table 2.1), gives $\kappa_p = \sum p_i^2 = 0.0656$. Its entries sum to $1.001$ because of rounding; rescaled to sum to 1, they give $0.0655$. Other letter tables give values from about $0.065$ to $0.067$, such as the often quoted $0.0667$.
- **Uniform letters.** $\kappa_r = 26 \cdot (1/26)^2 = 1/26 \approx 0.0385$. This is the smallest possible $\kappa$ for 26 letters, by the Cauchy-Schwarz inequality.

**Invariance.** If $\pi$ is a permutation of the letters, the counts of $\pi(P)$ are those of $P$ in a new order, so the index is the same. If the positions are permuted, the counts do not change at all. So the index of a substitution or transposition ciphertext equals that of its plaintext.

**Friedman's estimate of the period.** Let a periodic cipher with period $m$ encrypt $n$ letters of English, and assume that the $m$ alphabets are unrelated, so that two letters from different alphabets agree with probability $\kappa_r$. The $n$ letters fall into $m$ columns of about $n/m$ letters. Of the $\binom{n}{2}$ pairs of positions:

- $m \binom{n/m}{2} = \frac{n(n - m)}{2m}$ pairs lie in the same column, and agree with probability $\kappa_p$;
- the other $\frac{n^2 (m - 1)}{2m}$ pairs lie in different columns, and agree with probability $\kappa_r$.

So the expected index is

$$I \approx \frac{(n - m)\kappa_p + n(m - 1)\kappa_r}{m(n - 1)}.$$

Solving for $m$ gives Friedman's estimate

$$m \approx \frac{n(\kappa_p - \kappa_r)}{(n - 1) I - n\kappa_r + \kappa_p}.$$

It is a rough estimate, because the index of a real text varies, and because the alphabets of a Vigenère key are shifts of each other and not truly unrelated. A sharper test splits the text into $m$ columns for each candidate $m$ and computes the mean index of the columns: for the right $m$ each column is one alphabet, and the mean is near $\kappa_p$.

## Examples

- **Two English texts.** The first two sentences of the Declaration of Independence (499 letters) have an index of $0.0747$, and the Gettysburg Address (1,149 letters) has $0.0730$. Both are above the table value: short texts with many repeated words, such as THE and THAT, have more coincidences than a long mixed corpus.
- **A substitution ciphertext.** Any simple substitution of the Declaration text has the index $0.0747$ again, by the invariance.
- **A Vigenère ciphertext.** Under the key LEMON the same text gets the index $0.0434$. Friedman's estimate gives $m \approx 5.47$, and the mean column index is $0.0736$ for $m = 5$, $0.0719$ for $m = 10$ and below $0.045$ for every other $m \le 12$. So the key has 5 letters. The [Vigenère cipher](/vigenere-cipher/) page gives the full table and recovers the key, and the [Kasiski examination](/kasiski-examination/) page finds 5 on the same ciphertext from repeats and compares the two tests.
- **A tiny text.** The word LETTER has $f_E = 2$, $f_T = 2$, $f_L = f_R = 1$, so $\mathrm{IC} = (2 + 2)/(6 \cdot 5) = 2/15 \approx 0.133$. Short texts give very noisy values.

## Where it is used

- **The number of alphabets.** It tells a monoalphabetic cipher (index near $0.066$) from a polyalphabetic one (index lower), and estimates the period of a [Vigenère cipher](/vigenere-cipher/).
- **Transposition versus substitution.** A ciphertext with the English index and the English letter counts is likely a [transposition](/columnar-transposition-cipher/); with the English index but other counts, a [substitution](/substitution-cipher/).
- **Messages in depth.** Friedman's related kappa test writes two ciphertexts one above the other and counts the positions where they agree. If both used the same key stream at the same offset, they agree at the rate $\kappa_p$; otherwise at the rate $\kappa_r$. This finds the alignment of messages that share a key, the first step of attacks on rotor machines and on a reused [one-time pad](/one-time-pad/).
- **Language identification.** Each language has its own $\kappa$, so the index of a long plaintext or of a monoalphabetic ciphertext hints at the language.
- **Information theory.** $-\log_2 \kappa$ is the Rényi entropy of order 2 of the letter distribution, a lower bound on the [Shannon entropy](/shannon-entropy/).

## References
