---
tag: 3G0PKX
kind: algorithm
slug: playfair-cipher
name: Playfair cipher
area: cryptography/symmetric-ciphers
level: intro
summary: Encrypt pairs of letters with a 5×5 key square (I and J merged) by the row, column and rectangle rules. Invented by Wheatstone in 1854; broken by digraph counts and known plaintext.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of letters of the message}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
prereqs: [substitution-cipher]
see_also: [frequency-analysis, known-plaintext-attack, hill-cipher, vigenere-cipher, simulated-annealing, cipher-breaking]
sources:
  - book: isbn:9780684831305
    title: David Kahn, The Codebreakers, revised edition, Scribner, 1996
    locator: the account of Wheatstone, Lord Playfair and the Playfair cipher, and of its use and solution in the Boer War and the First World War
  - book: isbn:9780486200972
    title: Helen Fouché Gaines, Cryptanalysis, a Study of Ciphers and Their Solution, Dover, 1956
    locator: the chapter on the Playfair cipher (the rules, the digraph statistics and the reconstruction of the square)
  - book: isbn:9783540245025
    title: Friedrich L. Bauer, Decrypted Secrets, Methods and Maxims of Cryptology, fourth edition, Springer, 2007
    locator: Chapter 4 (polygraphic substitution, the Playfair cipher)
---

The Playfair cipher encrypts a message two letters at a time. The key is a 5 × 5 square that holds 25 letters, with I and J in one cell, filled with a keyword and then the rest of the alphabet. Each pair of plaintext letters becomes a pair of cipher letters by one of three rules: the same row, the same column, or the corners of a rectangle. Charles Wheatstone invented it in 1854, and his friend Lyon Playfair promoted it, so it carries Playfair's name. Because it substitutes pairs, single letter counts do not break it. But it is still a fixed substitution on 600 pairs, so pair counts and a little known plaintext do.

## In plain words

Write a keyword into a five by five grid, skip letters that repeat, and fill the rest of the grid with the other letters of the alphabet. I and J share a cell. Split the message into pairs of letters. If a pair has the same letter twice, put an X between them. If one letter is left over, add an X.

Now replace each pair. If the two letters are in the same row, take the letter to the right of each one. If they are in the same column, take the letter below each one. Otherwise they are opposite corners of a rectangle; take the other two corners, each one in the row of the letter that it replaces. To decrypt, move left and up instead.

## The problem

Let $\Sigma$ be the 25 letters A to Z without J. A key is a square $S$, an arrangement of $\Sigma$ in 5 rows and 5 columns, which is a [permutation](/permutation/) of $\Sigma$. Write $S[r, c]$ for the letter in row $r$ and column $c$, with indices modulo 5.

**Preparing the plaintext.** Take the letters, write J as I, and split them into pairs $ab$ with $a \ne b$. When the next two letters are equal, emit the first one with the filler X and continue from the second one. If one letter is left at the end, add X. (After an X, the code uses Q as the filler.)

**Encrypting one pair.** Let $a = S[r_1, c_1]$ and $b = S[r_2, c_2]$ with $a \ne b$.

- Same row ($r_1 = r_2$): $E(ab) = S[r_1, c_1 + 1]\, S[r_2, c_2 + 1]$.
- Same column ($c_1 = c_2$): $E(ab) = S[r_1 + 1, c_1]\, S[r_2 + 1, c_2]$.
- Rectangle (otherwise): $E(ab) = S[r_1, c_2]\, S[r_2, c_1]$.

Decryption uses $-1$ in place of $+1$; the rectangle rule is its own inverse. This is a [substitution](/substitution-cipher/) on the 600 ordered pairs of different letters, and an instance of [symmetric encryption](/symmetric-encryption/).

## The algorithm

```pseudo id=main
PLAYFAIR-ENCRYPT(P, S)                     ▷ S is the 5 × 5 key square
L1  D ← the pairs of P, with J as I, X between equal letters, and X at an odd end
L2  for each pair ab in D do
L3      (r1, c1) ← the place of a in S, (r2, c2) ← the place of b in S
L4      if r1 = r2 then output S[r1, c1+1] S[r2, c2+1]
L5      else if c1 = c2 then output S[r1+1, c1] S[r2+1, c2]
L6      else output S[r1, c2] S[r2, c1]
L7  return the output pairs, joined
```

Decryption runs lines L3 to L7 on the cipher pairs with $-1$ in place of $+1$. It returns the prepared plaintext, with the fillers; the reader removes them by sense.

The code is for study only. It is not constant time, and the cipher gives no protection. To protect real data, use AES-GCM or ChaCha20-Poly1305 from libsodium, from a FIPS 140 validated module, or from the standard library of your language.

## Example

The keyword PLAYFAIR EXAMPLE gives the square

| | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 0 | P | L | A | Y | F |
| 1 | I | R | E | X | M |
| 2 | B | C | D | G | H |
| 3 | K | N | O | Q | S |
| 4 | T | U | V | W | Z |

The message "Hide the gold in the tree stump" gives the pairs HI DE TH EG OL DI NT HE TR EX ES TU MP. The double E of TREE gets the filler X (TR EX ES), and the last pair MP needs no filler.

- HI: H is at (2, 4) and I at (1, 0), a rectangle, so H becomes the letter at (2, 0), B, and I becomes the letter at (1, 4), M. HI becomes BM.
- DE: D at (2, 2) and E at (1, 2) share column 2, so each moves down one row: D becomes O and E becomes D. DE becomes OD.
- EX: E at (1, 2) and X at (1, 3) share row 1, so each moves right: EX becomes XM.

The whole ciphertext is BMODZBXDNABEKUDMUIXMMOUVIF, which matches the published example of this key. Decryption gives HIDETHEGOLDINTHETREXESTUMP, with the filler X still in TREXES.

## Correctness

Each rule maps a pair of different letters to a pair of different letters, and the decryption rule undoes it: a step right and a step left cancel within a row, a step down and a step up cancel within a column, and the rectangle rule applied twice returns the original corners. The case of a pair is the same before and after encryption: the two cipher letters lie in the same row exactly when the two plaintext letters do, and the same holds for columns. So decryption picks the right rule, and it returns the prepared plaintext. The full proof is in the proof file below.

## Complexity

Preparing the message and each of the at most $n$ pairs take constant time with a table of the 25 places, so encryption and decryption take $\Theta(n)$ time in each case. The square takes $\Theta(1)$ space.

| claim | value |
|---|---|
| encryption and decryption, each case | $\Theta(n)$ |
| squares | $25! \approx 1.55 \times 10^{25} \approx 2^{83.7}$ |
| different ciphers | at most $25!/25 = 24! \approx 6.2 \times 10^{23} \approx 2^{79.0}$ |

**Equivalent squares.** Shifting all rows of the square down by one, cyclically, does not change any of the three rules, because they only use positions modulo 5. The same holds for a cyclic shift of the columns. So each square has 25 equivalent squares, and there are at most $24!$ different ciphers. Transposing the square is not an equivalence: it swaps the rows and the columns, which keeps the row and column rules but reverses the output of the rectangle rule.

## Properties

The properties below are the starting points of the classical attacks.

- **No letter stays in place.** In each rule, the first cipher letter differs from the first plaintext letter, and the second from the second.
- **No doubled pairs.** A cipher pair never has two equal letters, and the ciphertext has an even length.
- **Reversal.** If $E(ab) = cd$, then $E(ba) = dc$. So the common English pairs ER and RE give reversed cipher pairs.
- **Rectangle symmetry.** If $E(ab) = cd$ by the rectangle rule, then $E(cd) = ab$.
- **Neighbours.** In the row and column rules, each cipher letter is a neighbour of its plaintext letter in the square.

## Variants and improvements

- **Two squares and four squares.** Delastelle's four-square cipher and the two-square cipher use separate squares for the two letters of a pair, which removes some of the symmetries.
- **Other alphabets.** A 6 × 6 square holds the letters and digits, so I and J need not share a cell.
- **Double Playfair.** The German army used a double Playfair cipher with two squares in the Second World War, according to Kahn.

## When to use it

Use it to teach digraph substitution, the leak of pair statistics, and how symmetries help a code breaker. In the First World War and later, armies used it as a field cipher, for messages that only had to stay secret for hours. Never use it to protect data.

## Pitfalls

- **Forgetting the fillers.** The double letter rule applies to pairs as they are formed, from left to right, not to all double letters: in BALLOON the pairs are BA LX LO ON. The filler splits LL, and the pairing itself then splits OO, which needs no filler.
- **Mixing up the rectangle rule.** The first cipher letter is in the row of the first plaintext letter. Taking the column instead gives the transposed rule, which is a different cipher.
- **Treating I and J as different.** The square has 25 cells; J must be written as I before encryption.
- **Expecting the fillers to vanish.** Decryption returns them. A filler X inside a word, as in TREXES, must be removed by the reader.

## Implementations

## History

Charles Wheatstone, the physicist known for the Wheatstone bridge, described the cipher in 1854. His friend Lyon Playfair, later Baron Playfair, showed it to British officials and promoted its use, and the cipher came to be known by his name. The British army used it in the Second Boer War and in the First World War as a tactical field cipher. Joseph Mauborgne, later the Chief Signal Officer of the US Army, published a solution in 1914, according to Kahn. The classical attacks work from digraph counts and from the properties above: a code breaker guesses common pairs such as TH, HE, ER and RE, uses the reversal property to place more pairs, and rebuilds the square from the row, column and rectangle relations that the pairs imply. Known plaintext speeds this up a great deal. Each known pair is an entry of the table of 600 pairs, and with the reversal property each one gives two entries. In the code, the 13 known pairs of the example message give 26 entries, and they read five of the seven pairs of a second message, "the gold is here", without the key. Today computer searches, such as simulated annealing over squares with an n-gram score, break Playfair ciphertexts of a few hundred letters.

## References
