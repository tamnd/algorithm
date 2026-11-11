---
tag: XT3DYK
kind: technique
slug: frequency-analysis
name: Frequency analysis
aliases:
- letter frequency analysis
area: cryptography/symmetric-ciphers
level: intro
summary: Count the letters, pairs and triples of a ciphertext and match them to the statistics of the language. Chi-squared scores rank the guesses. It breaks every monoalphabetic cipher.
prereqs: [substitution-cipher]
see_also: [index-of-coincidence, caesar-cipher, affine-cipher, vigenere-cipher, kasiski-examination, hill-climbing, ciphertext-only-attack, cipher-breaking]
sources:
  - paper: "Ibrahim A. Al-Kadi, Origins of cryptology: the Arab contributions, Cryptologia 16(2), 1992, pages 97 to 126"
    locator: the account of al-Kindi's treatise on deciphering cryptographic messages and its method of letter frequencies
  - book: isbn:9781138197015
    title: Douglas R. Stinson and Maura B. Paterson, Cryptography, Theory and Practice, fourth edition, CRC Press, 2018
    locator: Section 2.2 (cryptanalysis of the classical ciphers), Table 2.1 (the letter probabilities of Beker and Piper) and Section 2.2.2 (the substitution cipher)
  - book: isbn:9780684831305
    title: David Kahn, The Codebreakers, revised edition, Scribner, 1996
    locator: the chapter on the Arab contributions to cryptology, and the chapters on the solution of monoalphabetic ciphers
  - book: isbn:9780385495318
    title: Simon Singh, The Code Book, Anchor Books, 2000
    locator: Chapter 1, The Cipher of Mary Queen of Scots (al-Kindi and frequency analysis)
---

*Frequency analysis* breaks a cipher by comparing how often letters, pairs of letters and triples of letters occur in the ciphertext with how often they occur in the language of the plaintext. A monoalphabetic cipher renames letters but keeps their counts, so the most common cipher letter is most likely E, the most common pair is likely TH, and so on. A score such as Pearson's chi-squared statistic turns the comparison into a number, which lets a program rank all keys of a small key space, or guide a search in a large one. It underlies almost every attack on a classical cipher.

The oldest known description is in a 9th century Arabic treatise of the philosopher al-Kindi, known in English as "On deciphering cryptographic messages". Its manuscript was found in Istanbul in the 1980s; Al-Kadi described it for readers of Cryptologia in 1992, and Kahn and Singh tell the story. Al-Kindi counts the letters of a long sample text, then matches the most common letter of the ciphertext to the most common letter of the language, and so on.

## In plain words

In English some letters are much more common than others. E makes up about one letter in eight, while Q, X and Z are very rare. A cipher that always swaps each letter for the same other letter keeps this pattern: the letter that stands for E is still the most common one.

So a code breaker counts the letters of the secret text, guesses that the most common one is E, the next T, and so on. Pairs and triples help too: TH, HE and THE are very common, and Q is nearly always followed by U. The first guesses are often a bit wrong, but they show part words, and the part words show how to fix the guesses. A computer does the same with a score that says how much a text looks like English.

## When it applies

- The cipher is **monoalphabetic**: each plaintext letter always becomes the same cipher letter ([Caesar](/caesar-cipher/), [affine](/affine-cipher/), [simple substitution](/substitution-cipher/)). Then the counts of the ciphertext are the counts of the plaintext with the letters renamed.
- The cipher is **periodic polyalphabetic** with a known or found period ([Vigenère](/vigenere-cipher/)). Then each column of letters one period apart is monoalphabetic. The period comes from the [index of coincidence](/index-of-coincidence/) or from [Kasiski examination](/kasiski-examination/).
- The cipher **substitutes blocks** of a small size, such as the pairs of the [Playfair cipher](/playfair-cipher/). Then the counts of the blocks leak, though more text is needed.
- The cipher **moves letters** but does not change them ([columnar transposition](/columnar-transposition-cipher/)). Then the single letter counts are those of English, which identifies the type of cipher, and pair counts guide the search for the order.
- The plaintext is long enough. The counts of a short text vary a lot, and the method needs at least some tens of letters per alphabet.

It does not apply to modern ciphers: a good [block cipher](/block-cipher/) or [stream cipher](/stream-cipher/) gives output whose counts are close to uniform for every input.

## The template

1. **Count.** For the ciphertext $c$ of $n$ letters, count the single letters $f_x$, and if needed the digrams $f_{xy}$ and the trigrams $f_{xyz}$.
2. **Compare with the language.** Use a table of the probabilities $p_x$ of the letters of the language, made from a text that is not the ciphertext. For a candidate decryption $d$ with counts $f_x$, Pearson's chi-squared statistic is

   $$\chi^2(d) = \sum_{x} \frac{(f_x - n p_x)^2}{n p_x}.$$

   A small value means that the counts look like the language. For larger blocks, the log likelihood $\sum \log P(z \mid x y)$ of the trigrams under a model of the language is a stronger score.
3. **Search.** If the key space is small, decrypt with every key and rank the keys by the score; this is a [brute-force search](/brute-force-search/) with a statistical test. If it is large, start from the key that matches the ranks of the counts, and improve it by local changes, by hand or by [hill climbing](/hill-climbing/).
4. **Read and fix.** Look at the best candidates. Part words, common short words and patterns of repeated letters confirm or correct the guesses. The score only ranks; a human or a dictionary check decides.

## Classic examples

**English counts.** The first two sentences of the Declaration of Independence have 499 letters. The most common ones are E (78), T (59), A (42), H (40), N and O (33 each), S (30) and I (27). The most common digrams are TH (27), HE (20), ES (12), AT and RE (11 each), and the most common trigrams are THE (19), AND, THA and ESE (5 each). The Gettysburg Address gives a similar picture: E, T, A, O, H, R, N, I for the letters, TH, AT, HE, RE for the digrams, and THE, THA, HAT, HER for the trigrams.

**A Caesar cipher by chi-squared.** Shift the Declaration text by each of the 26 shifts and compute $\chi^2$ against the table of Beker and Piper. The plaintext scores $39.3$. The next best shift scores $1641.4$. So the right key is plain from the score alone. The [Caesar cipher](/caesar-cipher/) page shows the same ranking on a 40-letter text, where the margin is smaller.

**The affine cipher by two guesses.** Guess that the two most common cipher letters stand for E and T. Two equations in $\mathbb{Z}_{26}$ give the key, as the [affine cipher](/affine-cipher/) page proves.

**Simple substitution.** The key that matches the ranks of the counts is only a start. On the Declaration text, its decryption has 53% of the letters right but starts FOEIHITOECNURSE for WHENINTHECOURSE, because letters with close counts (N and O, both 33) swap places and the table order differs from the order in this text. Hill climbing on a trigram score from that start recovers about 95% of the text; see the [substitution cipher](/substitution-cipher/) page.

**Vigenère columns.** With the key LEMON, each of the five columns of the Declaration ciphertext is a Caesar cipher of about 100 letters. The chi-squared test picks the right shift in each column, and the second best shift scores at least six times higher; see the [Vigenère cipher](/vigenere-cipher/) page.

## Variations

- **The chi-squared test against a table**, as above, or the **dot product** $\sum_x f_x p_x$ of the counts with the table, which Stinson and Paterson use for the Vigenère columns: the right shift tends to maximize it.
- **The index of coincidence** uses the counts without knowing which letter is which. It tells how many alphabets are mixed, not which letter is E. See the [index of coincidence](/index-of-coincidence/).
- **Log likelihood scores** with digram, trigram or quadgram models are the standard score for computer attacks on substitution, Playfair and transposition ciphers.
- **Vowel and consonant tests.** Vowels tend to alternate with consonants, and a letter that has contact with many different letters is likely a vowel. Older manual methods use such contact tables.
- **Word patterns.** Repeated letters inside words, such as the pattern of PEOPLE, point to words from a dictionary.

## Pitfalls

- **Treating chi-squared as a formal test.** The letters of a text are not independent draws, so the statistic does not follow the chi-squared distribution exactly. The Declaration plaintext scores $39.3$, above the 5% critical value of about $37.7$ for 25 degrees of freedom, yet it is English. Use the statistic to rank candidates.
- **Short texts.** In a short text the rank of the letters can differ a lot from the table. Do not fix more than the top few letters from the counts alone.
- **The wrong language or style.** Military messages, lists of names and texts written to avoid the letter E have other counts. The table must fit the plaintext.
- **Rare letters.** Letters that do not occur in the ciphertext can not be decided. In the Declaration text, J, X and Z do not occur.
- **Training on the text that you attack.** A score built from the ciphertext's own plaintext makes the attack look better than it is.

## Exercises

1. Show that the chi-squared statistic of a Caesar decryption depends on the shift only through a cyclic rotation of the counts, and that computing it for all 26 shifts takes $\Theta(n + 26^2)$ time.
2. A ciphertext has an index of coincidence of $0.066$, but its most common letters are X, K and Q. Which classical ciphers could have made it? What changes if its most common letters are E, T and A?
3. Explain why a homophonic cipher, which gives E several cipher symbols, flattens the single letter counts but not the digram counts.

## References
