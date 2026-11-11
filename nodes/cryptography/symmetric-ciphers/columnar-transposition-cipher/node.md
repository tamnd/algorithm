---
tag: G69PV9
kind: algorithm
slug: columnar-transposition-cipher
name: Columnar transposition cipher
aliases:
area: cryptography/symmetric-ciphers
level: intro
summary: Write the message in rows under a keyword and read the columns in the alphabetical order of the key letters. The letters stay the same, so letter counts reveal it.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of letters of the message, k: the number of columns}
  time: {worst: Θ(n + k·log k), average: Θ(n + k·log k), best: Θ(n + k·log k)}
  space: {extra: Θ(n + k)}
properties: {deterministic: true}
prereqs: [permutation, symmetric-encryption]
see_also: [frequency-analysis, index-of-coincidence, substitution-cipher, brute-force-search, ciphertext-only-attack, known-plaintext-attack, cipher-breaking, confusion-and-diffusion]
sources:
  - book: isbn:9780684831305
    title: David Kahn, The Codebreakers, revised edition, Scribner, 1996
    locator: the accounts of transposition ciphers, of the German double transposition ÜBCHI in 1914 and its solution by the French, and of multiple anagramming
  - book: isbn:9780486200972
    title: Helen Fouché Gaines, Cryptanalysis, a Study of Ciphers and Their Solution, Dover, 1956
    locator: the chapters on transposition ciphers (columnar transposition, the solution of messages of the same length by multiple anagramming)
  - book: isbn:9783540245025
    title: Friedrich L. Bauer, Decrypted Secrets, Methods and Maxims of Cryptology, fourth edition, Springer, 2007
    locator: Chapter 6 (encryption steps, transposition) and the chapter on anagramming in Part II
---

A columnar transposition cipher changes the order of the letters of a message and keeps the letters themselves. The sender writes the message in rows under a keyword of $k$ letters, one letter per column, and then reads the columns from top to bottom, in the alphabetical order of the key letters. The key is the order of the columns, a [permutation](/permutation/) of $k$ elements. Because no letter changes, the ciphertext has exactly the letter counts of the plaintext, so [frequency analysis](/frequency-analysis/) shows at once that the cipher is a transposition. Applying the cipher twice with two keys gives the double transposition, a field cipher of both World Wars. The classical attacks are a search over column orders and multiple anagramming of several messages of the same length.

## In plain words

Pick a keyword such as ZEBRAS. Write it across the top of a grid, and write the message below it, row by row, six letters per row. Then number the columns in the order of their key letters in the alphabet: A first, then B, E, R, S and Z. Read out the column under A from top to bottom, then the column under B, and so on.

The receiver knows the keyword. From the length of the message the receiver knows how long each column is, cuts the ciphertext into columns, puts them back under the keyword, and reads the rows.

The letters do not change, only their places. So the ciphertext has as many E letters as the message, and as many T letters. A code breaker who counts letters sees normal English counts and knows that the letters were moved, not replaced.

## The problem

Let the message be the letters $t_0 t_1 \cdots t_{n-1}$ and let the key be a word $K$ of $k$ letters. Place $t_i$ in row $\lfloor i / k \rfloor$ and column $i \bmod k$. Column $c$ then holds the letters $t_c, t_{c+k}, t_{c+2k}, \ldots$, and it has $\ell_c = \lfloor n/k \rfloor + [c < n \bmod k]$ letters. The last row may be short; the code does not pad it, which is the *irregular* form of the cipher.

The column order $\pi$ sorts the columns by their key letters, with equal letters from left to right. The ciphertext is column $\pi_0$, then column $\pi_1$, and so on. The map from plaintext positions to ciphertext positions is a [permutation](/permutation/) of $\{0, \ldots, n-1\}$ that depends only on $n$ and $\pi$. This is [symmetric encryption](/symmetric-encryption/): the same key encrypts and decrypts.

## The algorithm

```pseudo id=main
COLUMNAR-ENCRYPT(P, K)                     ▷ P has n letters, K has k letters
L1  π ← the columns 0, ..., k-1 sorted by (K[c], c)
L2  for each column c in the order π do
L3      output the letters P[c], P[c+k], P[c+2k], ... of column c
L4  return the output, joined
```

Decryption computes $\pi$ and the column lengths $\ell_c$, cuts the ciphertext into pieces of lengths $\ell_{\pi_0}, \ell_{\pi_1}, \ldots$, puts the piece of column $c$ back in column $c$, and reads the grid row by row. Double transposition runs the encryption twice, with keys $K_1$ and then $K_2$, and decryption undoes the two steps in the reverse order.

The first attack tries every column order for a guessed number of columns, and keeps the order whose decryption looks most like English under a trigram score.

```pseudo id=break
BREAK-COLUMNAR(C, k)
L5  best ← none
L6  for each order π of the k columns do
L7      P' ← the decryption of C with the order π
L8      if score(P') > score(best decryption so far) then best ← π
L9  return best
```

The second attack needs no grid at all. It takes $r$ messages of the same length $n$, all encrypted with the same key. The same key moves plaintext position $p$ to the same ciphertext position in every message, so if the ciphertexts are written one below the other, each column of letters belongs to one plaintext position. The attack finds which column follows which.

```pseudo id=anagram
MULTIPLE-ANAGRAM(C1, ..., Cr)              ▷ r ciphertexts of length n
L10 for each pair of positions i ≠ j: w(i, j) ← Σ over t of PMI(Ct[i], Ct[j])
L11 for each pair (i, j) in the order of decreasing w(i, j) do
L12     if i has no successor, j has no predecessor, and i → j closes no cycle then link i → j
L13 return the chain of links, from the position with no predecessor
```

Here $\mathrm{PMI}(a, b) = \log \bigl(P(b \mid a) / P(b)\bigr)$ measures how much more often the letter $b$ follows $a$ in English than chance predicts. The bigram probabilities come from a training text that the tests do not attack.

The code is for study only. It is not constant time, and the cipher gives no protection. To protect real data, use AES-GCM or ChaCha20-Poly1305 from libsodium, from a FIPS 140 validated module, or from the standard library of your language.

## Example

Encrypt WE ARE DISCOVERED FLEE AT ONCE with the key ZEBRAS. The 25 letters fill four full rows and one letter of a fifth row.

| Z | E | B | R | A | S |
|---|---|---|---|---|---|
| W | E | A | R | E | D |
| I | S | C | O | V | E |
| R | E | D | F | L | E |
| E | A | T | O | N | C |
| E | | | | | |

The key letters in alphabetical order are A, B, E, R, S, Z, in the columns 4, 2, 1, 3, 5, 0. So $\pi = (4, 2, 1, 3, 5, 0)$, and the columns are read as EVLN, ACDT, ESEA, ROFO, DEEC and WIREE. The ciphertext is

EVLNACDTESEAROFODEECWIREE.

To decrypt, the receiver computes $\ell_0 = 5$ and $\ell_c = 4$ for the other columns, so the first four letters go to column 4, the next four to column 2, and the last five to column 0.

**Frequencies are kept.** With the key GERMAN, the 499 letters of the sample text (the start of the Declaration of Independence) give a ciphertext that starts IOFEIMEFPTOEINCCTMNASMESEHRDSNCAANTOTMNE. It has the same letter counts as the plaintext, so its [index of coincidence](/index-of-coincidence/) is 0.0747 and its chi-squared statistic against English letter frequencies is 39.3, both the values of English text. A substitution cipher would give the same index of coincidence but a large chi-squared value.

**Search.** With $k = 6$, BREAK-COLUMNAR tries $6! = 720$ orders on the whole ciphertext and finds $\pi = (4, 1, 0, 3, 5, 2)$, the order of GERMAN, in under a second. Short messages are harder. For pieces of the sample text that start every 40 letters, the search finds the key for all 11 pieces of 60 letters, for 7 of 12 pieces of 30 letters, and for only 4 of 12 pieces of 20 letters. On short texts the trigram score of a wrong order is often higher.

**Multiple anagramming.** Cut the sample text into messages of the same length, and move the letters of every message with the same random permutation. MULTIPLE-ANAGRAM then gives the share of correct links below.

| length $n$ | messages $r$ | correct links |
|---|---|---|
| 15 | 33 | 100% |
| 20 | 24 | 100% |
| 25 | 19 | 96% |
| 30 | 16 | 79% |
| 40 | 12 | 62% |

More messages give more evidence for each link. The attack does not use the grid, so it breaks any fixed transposition of messages of the same length, including double transposition.

## Correctness

Line L3 outputs exactly the $\ell_c$ letters of column $c$, so the ciphertext is the columns in the order $\pi$, each one complete. Decryption knows $n$ and $\pi$, so it knows the lengths $\ell_c$, cuts the ciphertext at the same places, and puts each piece back in its column. Reading the grid row by row then gives the letters in their first order. Every letter of the plaintext is output once, so the cipher is a permutation of the positions and keeps the letter counts. For MULTIPLE-ANAGRAM, each kept link joins the end of one chain to the start of another, so the links always form disjoint chains, and while two chains remain, the link from the end of one to the start of the other is still allowed. So the result is one chain through all $n$ positions. The full proof is in the proof file below.

## Complexity

Line L1 sorts $k$ key letters in $\Theta(k \log k)$ time, and lines L2 to L4 output each of the $n$ letters once, so encryption and decryption take $\Theta(n + k \log k)$ time and $\Theta(n + k)$ space for the output and the column table.

| claim | value |
|---|---|
| encryption and decryption | $\Theta(n + k \log k)$ |
| column orders for $k$ columns | $k!$, for example $6! = 720$ and $10! = 3628800$ |
| double transposition with $k_1$ and $k_2$ columns | at most $k_1! \cdot k_2!$ keys |
| BREAK-COLUMNAR | $\Theta(k! \cdot n)$ |
| MULTIPLE-ANAGRAM | $\Theta(r n^2 + n^2 \log n)$ |

The key space is small for short keywords. A search over $k!$ orders is fast for $k$ up to about 9; for longer keys, [hill climbing](/hill-climbing/) over orders with an n-gram score replaces the exhaustive search.

## Properties

- **The letters are kept.** The ciphertext is a rearrangement of the plaintext, so the letter counts, the index of coincidence and the chi-squared value do not change.
- **Pairs are broken up.** Two neighbouring plaintext letters $t_i, t_{i+1}$ go to two different columns (when $k \ge 2$), so the common pairs of English such as TH and HE mostly disappear from the ciphertext.
- **Columns stay together.** The letters of one column stay in their order and next to each other. A code breaker who guesses where the columns start can put two columns side by side and test the pairs that they form.
- **One key for each length.** For a fixed $n$, the key gives one fixed permutation of positions. Two messages of the same length with the same key are moved in the same way, which multiple anagramming uses.

## Variants and improvements

- **Rail fence cipher.** The message is written in a zigzag over a few rows and read row by row. It is a different and weaker transposition with a key of one number, the number of rows; the alias on this page refers to the wider family of transposition ciphers.
- **Regular and irregular grids.** Padding the last row with nulls gives full columns, which makes the column lengths easy to guess. The irregular form, used here, leaves the last row short.
- **Double transposition.** Encrypting the result again with a second key, or the same key, spreads each letter much further. With long keys and irregular grids it resists the search attack well. It is still a single fixed permutation for each length, so multiple anagramming breaks it.
- **Route and grille ciphers.** Other transpositions read the grid along a spiral or another route, or use a grille, a card with holes, to choose the cells.
- **With substitution.** A transposition combined with a substitution hides both the letter counts and the positions. ADFGVX, a German cipher of 1918, did this. In modern block ciphers, permutation steps give diffusion and substitution steps give [confusion](/confusion-and-diffusion/).

## When to use it

Use it to teach the difference between substitution and transposition, the use of letter counts to tell them apart, and attacks that search over permutations. Never use it to protect data.

## Pitfalls

- **Ties in the key.** A keyword with repeated letters, such as LETTER with two E letters and two T letters, needs a rule for ties. The usual rule, used here, takes equal letters from left to right. Sender and receiver must use the same rule.
- **Short last row.** Decryption must give the first $n \bmod k$ columns one letter more. Treating all columns as equal in length cuts the ciphertext in the wrong places.
- **Reusing the key.** Many messages of the same length under the same key fall to multiple anagramming, even under double transposition.
- **Short messages and search.** A trigram score needs enough text. On 20 letters of the example the best scoring order is wrong in most cases; a search that returns one answer can return a wrong answer with confidence.

## Implementations

## History

Transposition is one of the oldest ways to hide a message. Greek writers describe the scytale of Sparta, a staff around which a strip was wound, but some historians doubt that it served as a cipher. Columnar transposition with a keyword was a common field cipher in the nineteenth and twentieth centuries. At the start of the First World War, the German army used a double columnar transposition that the French called ÜBCHI. According to Kahn, French cryptanalysts solved it, and after the German press reported the fact, the Germans replaced it in late 1914. Double transposition was used again in the Second World War, for example by agents of resistance groups and secret services, often with keys taken from poems; this use is described in memoirs of the period rather than in the sources above. The general solution of all transpositions is multiple anagramming: with two or more messages of the same length under the same key, the code breaker puts the messages one below the other and moves the columns of letters together until all rows read as language. This removes the need to know the shape of the grid. Gaines and Bauer give worked examples. In the code, 24 messages of 20 letters each are enough to recover every link of an arbitrary permutation of 20 positions.

## References
