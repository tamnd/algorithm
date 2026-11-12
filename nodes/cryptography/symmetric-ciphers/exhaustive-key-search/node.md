---
tag: BSXCZ6
kind: algorithm
slug: exhaustive-key-search
name: Exhaustive key search
aliases:
- brute-force attack
- brute-force key search
area: cryptography/symmetric-ciphers
level: intro
summary: Try every key on a few known plaintext and ciphertext pairs and keep the keys that fit. It costs 2^k cipher calls, about half that on average, and sets the bar for every other attack.
solves: [key-recovery]
model: query-model
complexity:
  vars: {k: the key length, n: the block length, s: the number of known pairs}
  time: {worst: O(2^k s), average: Θ(2^k)}
  space: {extra: Θ(s)}
properties: {deterministic: true}
history:
  year: 1977
  people: [Whitfield Diffie, Martin Hellman]
  note: Diffie and Hellman estimated the cost of a parallel machine that would search the 56-bit DES key space, and argued that the key was too short.
prereqs: [key-recovery]
see_also: [hellman-time-memory-tradeoff, rainbow-table, grover-search, data-encryption-standard, meet-in-the-middle-attack, distinguished-points, brute-force-search, triple-des]
sources:
  - paper: "Whitfield Diffie and Martin E. Hellman, Exhaustive cryptanalysis of the NBS Data Encryption Standard, Computer 10(6), 1977"
    locator: the design and cost estimate of a parallel DES key search machine
  - paper: doi:10.1109/TIT.1980.1056220
    title: Martin E. Hellman, A cryptanalytic time-memory trade-off, IEEE Transactions on Information Theory 26(4), 1980
    locator: the chain construction and the tradeoff T = M = N^(2/3)
  - paper: "Philippe Oechslin, Making a faster cryptanalytic time-memory trade-off, Advances in Cryptology, CRYPTO 2003, LNCS 2729, Springer, 2003"
    locator: rainbow tables, one reduction function per column
  - url: "https://www.eff.org/press/releases/eff-des-cracker-machine-brings-honesty-crypto-debate"
    title: Electronic Frontier Foundation, EFF DES cracker machine brings honesty to crypto debate, press release, July 1998
    locator: the 56-hour search that won the RSA DES Challenge II-2
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 7, Section 7.2 (exhaustive key search, the number of pairs needed, and time-memory tradeoffs)
  - paper: "Lov K. Grover, A fast quantum mechanical algorithm for database search, Proceedings of the 28th ACM Symposium on Theory of Computing (STOC), 1996"
    locator: quantum search in about the square root of the number of candidates
---

Exhaustive key search is the generic attack on a cipher: given a few known plaintext and ciphertext pairs, it tries every key and keeps the keys that map each plaintext to its ciphertext. It solves [key recovery](/key-recovery/) for each cipher with $k$-bit keys in at most $2^k$ cipher calls, and in about $2^{k-1}$ calls on average if it stops at the first fit. Every other attack is measured against this cost, and a cipher is called broken when an attack does much better. It broke [DES](/data-encryption-standard/) in practice: the EFF machine found a 56-bit key in 56 hours in July 1998.

## In plain words

You have a locked box, a message, and the same message in its locked form. You also have a key ring with every possible key. Take the keys one at a time. Lock the message with each key and compare the result with the locked form you have. When they match, you may have the right key.

A wrong key can match by chance. To rule it out, keep a second message and its locked form, and test the key on it too. A wrong key almost never matches twice.

The work grows with the number of keys. Each extra digit of key length doubles the work. On average you find the key halfway through the ring. This is why modern keys are long enough that no machine on Earth can try them all.

## The problem

The input is a cipher $E : \{0,1\}^k \times \{0,1\}^n \to \{0,1\}^n$ and $s \ge 1$ pairs $(x_1, y_1), \ldots, (x_s, y_s)$ with $y_i = E_K(x_i)$ for an unknown key $K$. The output is the set of *consistent* keys

$$C = \{K' \in \{0,1\}^k : E_{K'}(x_i) = y_i \text{ for } i = 1, \ldots, s\}.$$

The true key $K$ is in $C$. The other members of $C$ are *false positives*. The cost is counted in calls of $E$, as in the [query model](/query-model/). This is the known-plaintext form of [key recovery](/key-recovery/).

## The algorithm

KEY-SEARCH tests each key on the first pair, and runs the other pairs only on the keys that pass it.

```pseudo id=main
KEY-SEARCH(E, P, k)                        ▷ P = [(x1, y1), ..., (xs, ys)]
    C ← empty list
L1  for K' ← 0 to 2^k − 1 do
L2      if E(K', x1) ≠ y1 then continue
L3      if E(K', xi) = yi for each i = 2, ..., s then
L4          append K' to C
L5  return C
```

The variant that returns at the first key in $C$ is the one used in practice. It returns a false positive if one comes before $K$ in the order, so it is run with enough pairs that $C = \{K\}$ with high probability.

The Python code for this page searches a toy cipher with a 16-bit key and a 16-bit block. It is for study only, it is not constant time, and it must not be used to protect real data. To encrypt real data, use AES from a FIPS 140 validated module or from libsodium.

## Example

The toy cipher has 6 rounds on a 16-bit block. Each round XORs a round key, applies the 4-bit S-box of Heys's tutorial to each nibble, and applies the linear map $x \mapsto x \oplus \mathrm{rotl}(x, 5) \oplus \mathrm{rotl}(x, 9)$. A last round key is XORed at the end. Round key $i$ is $\mathrm{rotl}(K, (3i + 1) \bmod 16)$ XOR a round constant.

**One pair can be enough.** For $K$ = 0xBEEF, $E_K$(0x0000) = 0xFE6A. KEY-SEARCH with this one pair returns $C = \{\texttt{0xBEEF}\}$.

**One pair can be too few.** The keys 0x0004 and 0x88CB both map 0x0000 to 0xB88A. With the pair (0x0000, 0xB88A) alone, $C$ has both. A second pair with plaintext 0xFFFF gives 0xBA52 under 0x0004 and 0xB5DC under 0x88CB, so it keeps only the true key.

**How often.** Over all $2^{16}$ keys with the plaintext 0x0000, the number of keys that share each output value is distributed as follows.

| keys per output | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| outputs | 24390 | 12031 | 4018 | 938 | 199 | 39 | 7 |

So 37.2% of the keys are unique with one pair, and a key has 0.990 false positives on average. A random cipher gives $e^{-1} \approx 0.368$ and $(2^{16} - 1)/2^{16} \approx 1.000$ for these two numbers.

**Work.** With the early stop, two pairs and the keys tried in the order $0, 1, 2, \ldots$, the search for key $K$ tries exactly $K + 1$ keys, and the average over uniform keys is $(2^{16} + 1)/2$.

## Correctness

The invariant of the loop of line L1 is: after the keys $0, \ldots, j - 1$ have been tried, $C$ holds exactly the consistent keys below $j$, in increasing order. Line L2 rejects a key that fails pair 1, and line L3 rejects a key that fails another pair, so each key in $C$ is consistent. A consistent key passes both tests and is appended at line L4. The loop ends after $2^k$ steps, and then $C$ is the full set of consistent keys, which contains $K$. The full proof, with the count of cipher calls, is below.

## Complexity

Let $C_1$ be the set of keys that pass line L2. Each key costs one call at line L2, and each key in $C_1$ costs at most $s - 1$ more calls at line L3. So the number of calls is at most

$$2^k + (s - 1)\,|C_1|.$$

If each wrong key acts like an independent random permutation, then $\mathbb{E}|C_1| = 1 + (2^k - 1)/2^n$, so the expected cost is about $2^k + (s - 1)(1 + 2^{k-n})$. For DES, $2^{56 - 64} = 2^{-8}$, and line L3 is almost never reached.

- **Pairs needed.** Under the same model, the expected number of false positives with $s$ pairs is $(2^k - 1)/(2^n (2^n - 1) \cdots (2^n - s + 1)) \approx 2^{k - sn}$. So $s = \lceil k/n \rceil + 1$ pairs make $C = \{K\}$ with high probability: 1 or 2 for DES, 2 for AES-128 and 3 for AES-256.
- **Average with the early stop.** If $K$ is uniform and $C = \{K\}$, the number of keys tried is uniform on $1, \ldots, 2^k$, with mean $(2^k + 1)/2$.
- **Success with partial work.** A search of $t$ keys succeeds with probability $t/2^k$.
- **Space.** The pairs and the output, so $\Theta(s)$ apart from $C$.
- **Parallel time.** The key space splits into $p$ equal parts with no communication, so $p$ machines take $2^k/p$ calls each.

## Properties

- **Generic.** It uses $E$ as a black box. It works for every cipher, and its cost depends only on $k$.
- **Known plaintext.** It needs no chosen inputs. With ciphertext only, the test at line L2 becomes "the decryption looks like valid plaintext", for example ASCII text, and needs enough ciphertext that a wrong key fails this test.
- **No memory.** It stores almost nothing, unlike the time-memory tradeoffs below.
- **Deterministic.** The order of keys is fixed, but a random order gives the same average.

## Variants and improvements

- **Complementation of DES.** DES has $E_{\bar K}(\bar x) = \overline{E_K(x)}$. With the encryptions of $x$ and $\bar x$, one trial of $K'$ also tests $\bar K'$, so the search needs $2^{55}$ trials in the worst case. See [DES](/data-encryption-standard/).
- **Multi-target search.** With $T$ keys that each encrypt the same plaintext $x$, compute $E_{K'}(x)$ for each $K'$ and look it up in a table of the $T$ ciphertexts. One of the keys is found after about $2^k/T$ trials. In the test code, 64 targets on the 16-bit toy cipher are found after fewer than $2^{13}$ trials.
- **[Hellman time-memory tradeoff](/hellman-time-memory-tradeoff/).** For a fixed chosen plaintext $x_0$, let $f(K') = R(E_{K'}(x_0))$, where $R$ reduces a block to a key. Precompute chains $K', f(K'), f^2(K'), \ldots$ of length $t$ and store only the start and end of each. Online, apply $f$ to the target until an end point appears, then rebuild the chain from its start. With $N = 2^k$, precomputation costs about $N$, and the online time $T$ and memory $M$ satisfy $T M^2 \approx N^2$, for example $T = M = N^{2/3}$ (Hellman 1980). On the 16-bit toy cipher, 4 tables of 256 chains of length 64 keep 914 distinct end points, cover 19205 keys and find a key for 95 of 200 random targets.
- **[Rainbow tables](/rainbow-table/).** Use a different reduction function in each column, so that two chains merge only if they meet in the same column (Oechslin 2003). On the toy cipher, one table of 1024 chains of length 64 keeps 689 end points, covers 32213 keys and finds a key for 136 of 200 targets.
- **[Distinguished points](/distinguished-points/).** End each chain at a point with a fixed pattern, so that a lookup is needed only at those points.
- **[Grover search](/grover-search/).** A quantum computer can find the key in about $2^{k/2}$ evaluations of $E$ (Grover 1996). This is one reason to prefer 256-bit keys for long-term use.

## When to use it

Use exhaustive search as the reference cost for each claim about a cipher with $k$-bit keys. Run it in practice only when $k$ is small: a 40-bit export key, the 56-bit DES key, a toy cipher, or a key derived from a short password, where the search runs over the password space. For $k \ge 112$, no machine can run it.

## Pitfalls

- **One pair is not proof.** With $k \ge n$, one pair leaves about $2^{k-n}$ false positives. For AES-128, one pair leaves about one wrong key on average. Use $\lceil k/n \rceil + 1$ pairs.
- **The real key space is smaller than the key length.** DES keys have 64 bits, but 8 are parity bits, so the search is over $2^{56}$ keys. A 128-bit key derived from a 6-letter password has only about $2^{28}$ values.
- **Counting the average.** The expected cost is about $2^{k-1}$, not $2^k$. The worst case is $2^k$.
- **Multi-target attacks.** A system with many keys gives the attacker a factor equal to the number of targets. A 64-bit key used by a million users is found after about $2^{44}$ trials.
- **Precomputation is not free.** A time-memory tradeoff costs about $2^k$ work once. It pays off only for many targets with the same fixed plaintext. A random salt or IV defeats it.

## Implementations

## History

Diffie and Hellman argued in 1977 that a parallel machine of special chips could search the 56-bit DES key space in about a day, and that the key was too short. Hellman published the time-memory tradeoff in 1980. In July 1998 the Electronic Frontier Foundation built a DES search machine for less than 250,000 US dollars. It found the key of the RSA DES Challenge II-2 in 56 hours, at about 88 billion keys per second on average, after searching 24.8% of the key space. Oechslin introduced rainbow tables in 2003.

## References
