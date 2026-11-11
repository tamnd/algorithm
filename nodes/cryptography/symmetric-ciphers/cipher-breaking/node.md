---
tag: P8VQMG
kind: problem
slug: cipher-breaking
name: Cipher breaking
aliases:
- classical cryptanalysis
- recovering plaintext without the key
area: cryptography/symmetric-ciphers
level: intro
summary: Recover the plaintext of a classical cipher without the key. The method finds the cipher model, studies the key space, picks a score that tells right from wrong, and searches.
prereqs: [cryptanalysis, ciphertext-only-attack]
see_also: [frequency-analysis, index-of-coincidence, kasiski-examination, known-plaintext-attack, key-recovery, hill-climbing, simulated-annealing, exhaustive-key-search]
sources:
  - book: isbn:9781138197015
    title: Douglas R. Stinson and Maura B. Paterson, Cryptography, Theory and Practice, fourth edition, CRC Press, 2018
    locator: Section 2.2 (the cryptanalysis of the affine, substitution, Vigenère and Hill ciphers) and Section 3.5 (spurious keys and unicity distance)
  - book: isbn:9780486200972
    title: Helen Fouché Gaines, Cryptanalysis, a Study of Ciphers and Their Solution, Dover, 1956
    locator: the opening chapters on the identification of cipher types by letter counts, and the chapters on the solution of substitution and transposition ciphers
  - book: isbn:9783540245025
    title: Friedrich L. Bauer, Decrypted Secrets, Methods and Maxims of Cryptology, fourth edition, Springer, 2007
    locator: Part II (cryptanalysis), the chapters on exhausting combinatorial complexity, patterns and frequencies of language, periodicity, and anagramming
  - paper: doi:10.1002/j.1538-7305.1949.tb00928.x
    title: Claude E. Shannon, Communication theory of secrecy systems, Bell System Technical Journal 28(4), 1949, pp. 656-715
    locator: Part II, the unicity distance, and Part III, the discussion of the work of solving a cipher
---

Cipher breaking is the problem of recovering the plaintext of an encrypted message without being given the key. This page covers the classical ciphers, where the problem has a standard method in four steps: find the *model* (which cipher, and which parameters such as the period), study the *key space* (its size and whether it splits into parts), choose a *distinguisher* (a score that tells correct plaintext from wrong plaintext), and *search* the keys with that score. Each classical attack on this site is an instance of the method. Cipher breaking is narrower than [cryptanalysis](/cryptanalysis/), the whole field with its attack models and goals, and it is not the same as [key recovery](/key-recovery/), which is one goal: a code breaker who reads the plaintext of a two-time pad has broken the messages without learning the key.

## In plain words

A code breaker gets a page of secret text. First, the code breaker asks what kind of cipher it is. Counting letters helps: if the counts look like English, the letters were only moved; if they are flat, the cipher uses several alphabets.

Next, the code breaker asks how many keys there are, and whether the key can be found in parts. Then the code breaker needs a test that says "this looks like English" for the right answer and "this is noise" for a wrong one. Last comes the search: try all keys if there are few, solve one part at a time, or improve a guess step by step until the text reads well.

## Definition

**Input.** One or more ciphertexts $c_1, \ldots, c_q$ produced by a cipher from a known family $\{\mathrm{Enc}_k\}_{k \in \mathcal{K}}$ (or from one of a few candidate families) under one unknown key $k^*$, and a model of the plaintext source, such as letter and n-gram frequencies of English. In the [known-plaintext](/known-plaintext-attack/) version, some pairs of plaintext and ciphertext are given too.

**Output.** Plaintexts $\hat m_1, \ldots, \hat m_q$, and if possible the key $\hat k$.

**Success.** The output plaintexts equal the true ones, or agree with them on almost all letters. Because the problem is about natural text, success is measured on test messages, as the share of letters or of keys recovered.

**The four steps.**

1. *Model.* Identify the cipher family and its parameters. Letter counts that match English mean a transposition; the [index of coincidence](/index-of-coincidence/) separates one alphabet from several; the [Kasiski examination](/kasiski-examination/) and the index of coincidence give the period.
2. *Key space.* Count the keys, and look for structure: a key that splits into parts that can be tested one at a time makes the search much smaller.
3. *Distinguisher.* Choose a score $s(m)$ that is high for language and low for random text: the chi-squared statistic of the letter counts, the index of coincidence, an n-gram log likelihood, or the consistency of a crib.
4. *Search.* Find a key whose decryption maximizes the score: by [exhaustive search](/exhaustive-key-search/), by divide and conquer over the parts of the key, by [hill climbing](/hill-climbing/) or [simulated annealing](/simulated-annealing/), or by solving equations.

## Variants

- **Ciphertext only** or **known plaintext**, as in the attack models of [cryptanalysis](/cryptanalysis/).
- **Unknown cipher type.** The model step comes first, with statistics that do not depend on the key.
- **Several messages under one key.** More text helps the score, and some methods, such as multiple anagramming of transpositions, need several messages of the same length.
- **Plaintext only.** Some attacks, such as crib dragging on a reused [one-time pad](/one-time-pad/), recover the plaintexts without the key.
- **Partial breaks.** Reading part of the message, or narrowing the key to a small set, is often enough in practice.

## Examples

| cipher | model step | key space | distinguisher | search |
|---|---|---|---|---|
| [Caesar cipher](/caesar-cipher/) | letter counts are shifted English | 26 keys | chi-squared of the counts | all 26 keys |
| [affine cipher](/affine-cipher/) | as Caesar | 312 keys | chi-squared | all keys, or two known pairs and algebra |
| [substitution cipher](/substitution-cipher/) | one alphabet, by the index of coincidence | $26! \approx 2^{88}$ | n-gram score | hill climbing from the frequency order |
| [Vigenère cipher](/vigenere-cipher/) | period by [Kasiski](/kasiski-examination/) and the [index of coincidence](/index-of-coincidence/) | $26^m$, splits into $m$ shifts | chi-squared for each column | 26 shifts for each of $m$ columns |
| [Playfair cipher](/playfair-cipher/) | even length, no doubled pairs | at most $24!$ squares | n-gram score | simulated annealing, or known pairs |
| [Hill cipher](/hill-cipher/) | flat counts, block structure | 157,248 keys for $n = 2$ | known plaintext | linear algebra modulo 26 |
| [columnar transposition](/columnar-transposition-cipher/) | English letter counts | $k!$ orders | n-gram score | all orders, or multiple anagramming |
| [Enigma machine](/enigma-machine/) | rotor machine | about $10^{23}$ settings, split into rotors and plugboard | crib consistency, cycle structure | the bombe over rotor settings |

## Known algorithms

- **Exhaustive search** with a statistical score, for key spaces up to about $2^{40}$ on a computer, and for 26 keys by hand.
- **Divide and conquer.** A key with independent parts is found one part at a time: the [Vigenère cipher](/vigenere-cipher/) splits into $m$ shift ciphers once the period is known, so the work is $26 m$ trials instead of $26^m$. The bombe found the rotor settings of Enigma first, and the plugboard came out of the consistent settings.
- **Local search.** [Hill climbing](/hill-climbing/) and [simulated annealing](/simulated-annealing/) improve a key by small changes, such as swapping two letters of a substitution key, and keep the change if the n-gram score improves. They break substitution and Playfair ciphers of a few hundred letters.
- **Algebra.** Linear ciphers give linear equations from known plaintext: the affine and Hill ciphers fall to [Gaussian elimination](/gaussian-elimination/) modulo 26, using the [Chinese remainder theorem](/chinese-remainder-theorem/) to work modulo 2 and 13.
- **Pattern and structure attacks.** Repeated pieces (Kasiski), letter patterns of words, cribs, and the cycle structure of permutations (Rejewski) use the structure of the cipher directly.

## Bounds

- **Unicity distance.** Below about $H(K)/D$ letters of ciphertext, where $D$ is the redundancy of the language per letter, many keys give meaningful text, and no method can decide among them. For simple substitution this is about 28 letters. See the [ciphertext-only attack](/ciphertext-only-attack/).
- **Perfect secrecy.** For a scheme with [perfect secrecy](/perfect-secrecy/), such as the one-time pad used correctly, no amount of computing breaks a single message: every plaintext of the right length is equally likely.
- **Search cost.** Without structure to exploit, the cost is the size of the key space. Practical methods need much more text than the unicity distance, because they cannot search the whole space and their scores are noisy on short texts.

## Reductions

- Breaking a Vigenère cipher with a known period reduces to breaking $m$ shift ciphers on the columns.
- Breaking a Hill cipher with known plaintext reduces to solving a linear system modulo 26, and by the Chinese remainder theorem to two systems modulo 2 and 13.
- Breaking a transposition cipher reduces to ordering the columns, a search over [permutations](/permutation/); with several messages of the same length it becomes the assembly of a chain of positions from pair scores.
- Breaking a reused one-time pad reduces to splitting the XOR of two texts into two texts that both read as language.

## Applications

- Military and diplomatic code breaking, from the field ciphers of the nineteenth century to the World Wars.
- The reading of historical documents and private ciphers whose keys are lost.
- Teaching: classical ciphers show the attack models, the role of redundancy in language, and the use of search and statistics, at a scale where every step can be checked by hand.
- Puzzles and competitions built on classical ciphers.

## References
