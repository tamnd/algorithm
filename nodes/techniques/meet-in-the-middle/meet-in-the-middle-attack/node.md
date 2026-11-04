---
tag: ZGTKX7
kind: algorithm
slug: meet-in-the-middle-attack
name: Meet-in-the-middle attack
aliases:
- meet-in-the-middle cryptanalysis
- Diffie-Hellman double-encryption attack
area: techniques/meet-in-the-middle
level: advanced
summary: Breaks double encryption with two keys in about 2^n work and 2^n memory, instead of the naive 2^(2n).
solves: [double-encryption-key-recovery]
model: word-ram
complexity:
  vars: {K: the number of keys, N: the number of blocks, t: the number of known pairs, c: the number of key pairs that match the first pair (at most K^2)}
  time: {worst: O(K + c t), average: O(K + t K^2 / N)}
  space: {extra: Θ(K)}
properties: {deterministic: true, recursive: false, in_place: false, online: false}
history:
  year: 1977
  people: [Whitfield Diffie, Martin Hellman]
  note: Diffie and Hellman described the attack on double encryption with DES in their 1977 analysis of exhaustive search on DES.
prereqs: [block-cipher, known-plaintext-attack, exhaustive-key-search]
see_also: [double-encryption-key-recovery, triple-des, data-encryption-standard, horowitz-sahni-algorithm, schroeppel-shamir-algorithm, parallel-collision-search, hash-join, time-memory-tradeoff]
sources:
  - paper: doi:10.1109/C-M.1977.217750
    title: Whitfield Diffie and Martin E. Hellman, Exhaustive cryptanalysis of the NBS Data Encryption Standard, Computer 10(6) (1977), 74-84
    locator: the discussion of multiple encryption with DES
  - paper: doi:10.1145/358699.358718
    title: Ralph C. Merkle and Martin E. Hellman, On the security of multiple encryption, Communications of the ACM 24(7) (1981), 465-467
    locator: the attacks on double encryption and on triple encryption with two keys
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography
    locator: Chapter 7 (block ciphers), the part on multiple encryption
  - paper: doi:10.1007/PL00003816
    title: Paul C. van Oorschot and Michael J. Wiener, Parallel collision search with cryptanalytic applications, Journal of Cryptology 12(1) (1999), 1-28
    locator: the application to meet-in-the-middle attacks
---

The meet-in-the-middle attack recovers the two keys of a double encryption $C = E_{k_2}(E_{k_1}(P))$ of a [block cipher](/block-cipher/) from a few [known plaintext-ciphertext pairs](/known-plaintext-attack/). It encrypts the plaintext under each first key, decrypts the ciphertext under each second key, and looks for a value that both sides reach in the middle. With $K$ keys it uses about $2K$ cipher calls and a table of $K$ entries, where [exhaustive search](/exhaustive-key-search/) over the key pairs uses $K^2$ double encryptions. This is why double DES with two 56-bit keys gives about 57 bits of security against this attack, and not 112.

## In plain words

A message goes through two locks in a row, each with its own secret key. You know one message and the result after both locks. To try every pair of keys takes the number of keys times itself.

The attack starts from both ends. From the message side, you put the message through the first lock with every possible key, and you write down each result in a table. From the result side, you undo the second lock with every possible key. If a value from this side is in the table, the two keys of that match can be the right pair, because they lead to the same value in the middle.

Some matches are wrong by chance. A second known message removes almost all of them: you test each matching pair of keys on it, and you keep only the pairs that work.

## The problem

The input is a block cipher with keys $\{0, 1, \ldots, K-1\}$ and blocks $\{0, 1, \ldots, N-1\}$, given by an encryption function $E_k$ and its inverse $D_k$, and $t \ge 1$ known pairs $(P_1, C_1), \ldots, (P_t, C_t)$. The output is the set of all key pairs that are consistent with each pair:

$$R = \{(k_1, k_2) : E_{k_2}(E_{k_1}(P_i)) = C_i \text{ for } i = 1, \ldots, t\}.$$

This is [double-encryption key recovery](/double-encryption-key-recovery/). The pairs come from a [known-plaintext attack](/known-plaintext-attack/): the attacker does not choose the plaintexts.

## The algorithm

$T$ is a map from a block to the list of first keys that lead to that block. A [hash join](/hash-join/) of the two sides is the core of the method.

```pseudo id=main
MEET-IN-THE-MIDDLE(E, D, K, (P1, C1), ..., (Pt, Ct))
L1  T ← an empty map from blocks to lists of keys
L2  for k1 ← 0 to K − 1 do
L3      append k1 to T[E_{k1}(P1)]               ▷ keep every key, not only the last one
L4  R ← an empty list
L5  for k2 ← 0 to K − 1 do
L6      X ← D_{k2}(C1)                           ▷ the middle value seen from the ciphertext side
L7      for each k1 in T[X] do                   ▷ candidates: E_{k2}(E_{k1}(P1)) = C1
L8          if E_{k2}(E_{k1}(Pi)) = Ci for each i = 2, ..., t then
L9              append (k1, k2) to R
L10 return R
```

Lines L1 to L3 build the forward table: one encryption of $P_1$ under each key. Lines L5 and L6 compute the backward values: one decryption of $C_1$ under each key. A key $k_1$ in the list $T[X]$ gives $E_{k_1}(P_1) = X = D_{k_2}(C_1)$, so the pair $(k_1, k_2)$ maps $P_1$ to $C_1$. Line L8 filters these candidates with the other known pairs.

## Example

The toy cipher has 8-bit blocks ($N = 256$) and 4-bit keys ($K = 16$). For a key $k$, let $\kappa = 17k$, so $\kappa$ is the byte with the digit $k$ in both hexadecimal places. Then

$$E_k(x) = (\mathrm{rotl}_3(x \oplus \kappa) + \kappa) \bmod 256, \qquad D_k(y) = \mathrm{rotr}_3((y - \kappa) \bmod 256) \oplus \kappa,$$

where $\oplus$ is bitwise exclusive or and $\mathrm{rotl}_3$ and $\mathrm{rotr}_3$ rotate a byte by 3 bits to the left and to the right. Each $E_k$ is a permutation of the 256 bytes, and the 256 double ciphers $E_{k_2} \circ E_{k_1}$ are 256 different permutations.

The secret keys are $k_1 = 3$ and $k_2 = 10$. The known pairs are $(P_1, C_1) = (42, 52)$ and $(P_2, C_2) = (100, 228)$. The table gives, for each key $k$, the forward value $E_k(P_1)$ (lines L2 and L3), the backward value $D_k(C_1)$ (line L6) and the list $T[D_k(C_1)]$ (line L7).

| $k$ | $E_k(42)$ | $D_k(52)$ | $T[D_k(52)]$ |
|---|---|---|---|
| 0 | 81 | 134 | empty |
| 1 | 234 | 117 | empty |
| 2 | 98 | 96 | empty |
| 3 | 251 | 19 | empty |
| 4 | 183 | 90 | empty |
| 5 | 80 | 174 | [10] |
| 6 | 200 | 191 | empty |
| 7 | 97 | 192 | empty |
| 8 | 157 | 29 | empty |
| 9 | 54 | 234 | [1] |
| 10 | 174 | 251 | [3] |
| 11 | 71 | 148 | empty |
| 12 | 3 | 193 | empty |
| 13 | 156 | 55 | empty |
| 14 | 20 | 38 | empty |
| 15 | 173 | 89 | empty |

The first pair leaves three candidates, $(k_1, k_2) = (10, 5)$, $(1, 9)$ and $(3, 10)$. For example, $D_9(52) = 234 = E_1(42)$. Line L8 encrypts $P_2 = 100$ under each candidate. The results are 0, 194 and 228. Only $(3, 10)$ gives $C_2 = 228$, so $R = [(3, 10)]$.

The attack used 16 encryptions, 16 decryptions and 3 double encryptions for the filter: 38 cipher calls. Exhaustive search over the 256 key pairs uses 512 cipher calls on the first pair alone.

## Correctness

After the loop of line L2, the table has this property: for each block $x$, $T[x]$ is the list of all keys $k_1$ with $E_{k_1}(P_1) = x$. Since $D_{k_2}$ is the inverse of the permutation $E_{k_2}$, the test $E_{k_1}(P_1) = D_{k_2}(C_1)$ of line L7 holds exactly when $E_{k_2}(E_{k_1}(P_1)) = C_1$. Line L8 checks the other pairs, so $R$ is exactly the set of consistent key pairs, and each pair is in it once. The [full proof](proofs/correctness/) gives the steps.

## Complexity

The cost is counted in cipher calls (one $E$ or one $D$) and in map operations, in the [word RAM](/word-ram/) with a block and a key in one word each.

- **Table.** Lines L2 and L3 make $K$ encryptions and $K$ insertions.
- **Lookups.** Lines L5 and L6 make $K$ decryptions and $K$ lookups.
- **Filter.** Let $c$ be the number of key pairs that map $P_1$ to $C_1$. Line L8 runs once for each of them and costs at most $2(t - 1)$ cipher calls. So the filter costs at most $2c(t-1)$ cipher calls.

The total is $2K + 2c(t-1)$ cipher calls and $O(K + c)$ map operations, with $c \le K^2$ in the worst case. With a hash map, each map operation takes $O(1)$ expected time.

**Expected number of candidates.** In the [ideal cipher model](/ideal-cipher-model/), each wrong key pair acts on $P_1$ as a random permutation, so it maps $P_1$ to $C_1$ with probability $1/N$. The true pair always matches. By linearity of expectation,

$$\mathbb{E}[c] = 1 + \frac{K^2 - 1}{N}.$$

With $t$ pairs with distinct plaintexts, a wrong pair passes all of them with probability $\frac{1}{N(N-1)\cdots(N-t+1)}$, which is about $N^{-t}$. For DES, $K = 2^{56}$ and $N = 2^{64}$. One pair leaves about $2^{48}$ wrong candidates, and two pairs leave about $2^{-16}$ in expectation. So the attack needs two or three known pairs, and its time is about $2^{57}$ cipher calls.

**Memory.** The table has $K$ entries. For DES, this is $2^{56}$ entries of a 64-bit block and a 56-bit key, about $10^{18}$ bytes.

**Sort instead of hash.** Sort the $K$ forward pairs $(E_{k_1}(P_1), k_1)$ by block, then look up each backward value with [binary search](/binary-search/). This takes $O(K \log K)$ comparisons and needs no hashing. A third way sorts both lists and merges them, as in a [sort-merge join](/sort-merge-join/).

## Properties

- **Exact.** The output is the full set of consistent key pairs, not a probable one. If several key pairs encrypt the known plaintexts in the same way, all of them are in $R$.
- **Known plaintext only.** The attack needs no chosen plaintexts.
- **Generic.** It uses $E$ and $D$ only as black boxes, so it works for each block cipher. It does not need a weakness in the cipher.
- **Memory bound.** The time is close to two exhaustive searches, but the memory is a table with one entry for each key. In practice the memory, not the time, is the limit.

## Variants and improvements

- **Triple encryption with three keys.** Put the table at one end and search the two other keys on the other side. This takes about $K^2$ cipher calls and $K$ memory, so three-key [triple DES](/triple-des/) has about 112 bits of security against this attack.
- **Triple encryption with two keys.** Merkle and Hellman give a chosen-plaintext attack on the form $E_{k_1} D_{k_2} E_{k_1}$ with about $K$ operations, $K$ words of memory and about $K$ chosen plaintexts.
- **Less memory.** van Oorschot and Wiener apply [parallel collision search](/parallel-collision-search/) to meet-in-the-middle problems such as double encryption. It needs less memory than the full table and pays with more cipher calls.
- **Partial tables.** Store the forward values for only a fraction $1/r$ of the first keys at a time, and repeat the backward pass $r$ times. The memory drops to $K/r$ and the backward work grows to $rK$.
- **Subset sum.** The same split solves [subset sum](/subset-sum-problem/) in the [Horowitz-Sahni algorithm](/horowitz-sahni-algorithm/), and the [Schroeppel-Shamir algorithm](/schroeppel-shamir-algorithm/) reduces its memory.

## When to use it

Use it when the secret is a composition of two parts that you can compute from opposite ends: an encryption followed by a second encryption, a first half and a second half of a sum, or two halves of a path. If memory for $K$ entries is available, it uses about $2K$ cipher calls, where exhaustive search uses $K^2$. If the memory is too small, use the partial-table variant or parallel collision search. For a single encryption, there is no middle, and [exhaustive key search](/exhaustive-key-search/) is the generic attack.

## Pitfalls

- **One key for each table entry.** A map that stores one key for each block in line L3 (`T[x] ← k1`) loses keys when two first keys give the same middle value. Line L3 must append to a list.
- **No filter.** A program that returns the first match of line L7 returns a wrong pair with high probability when $K^2 > N$. For DES there are about $2^{48}$ wrong matches with one pair. Line L8 must check at least one more pair.
- **The wrong direction.** Line L6 must decrypt the ciphertext with the second key, $D_{k_2}(C_1)$. Encrypting it, or decrypting with the first key, meets in no middle.
- **Mixing up the key order.** The pair is $(k_1, k_2)$ with $k_1$ applied first. A program that returns $(k_2, k_1)$ gives keys that fail on new data.
- **The other MITM.** A meet-in-the-middle attack is a key search. It is not the man-in-the-middle attack on a protocol, which has the same initials.

## Implementations

## History

Diffie and Hellman described the attack in 1977, in their analysis of exhaustive search on the NBS Data Encryption Standard. They showed that double encryption with two DES keys does not give the square of the key space as the cost of an attack, if the attacker has a large memory. Merkle and Hellman in 1981 studied multiple encryption further. They gave the analysis of double encryption and a chosen-plaintext attack on triple encryption with two keys, which shows that this form is weaker than its 112-bit key suggests. In 1999, van Oorschot and Wiener applied parallel collision search to meet-in-the-middle attacks, to reduce their memory.

## References
