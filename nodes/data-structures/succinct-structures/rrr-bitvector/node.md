---
tag: 5SBQH9
kind: data-structure
slug: rrr-bitvector
name: RRR bit vector
aliases:
- RRR
- Raman-Raman-Rao bit vector
area: data-structures/succinct-structures
level: advanced
summary: An entropy-compressed bit vector with rank and select, using nH0 + o(n) bits.
model: word-ram
complexity:
  vars: {n: the length of the bit vector, m: the number of 1s, b: the block length in bits}
  time: {access: O(1), rank: O(1), select: O(log n), build: O(n)}
  space: {total: "m log(n / m) + O(m + n log log n / log n)"}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2002
  people: [Rajeev Raman, Venkatesh Raman, S. Srinivasa Rao]
  note: The class and offset encoding of blocks appeared in the SODA 2002 paper on succinct indexable dictionaries; Claude and Navarro made it practical in 2008.
prereqs: [fully-indexable-dictionary, enumerative-coding, combinatorial-number-system]
see_also: [jacobson-rank, rank-select-dictionary, sd-array, elias-fano-encoding, compressed-data-structure, wavelet-tree, shannon-entropy, binomial-coefficient]
sources:
  - paper: doi:10.1145/1290672.1290680
    title: Rajeev Raman, Venkatesh Raman and S. Srinivasa Rao, Succinct indexable dictionaries with applications to encoding k-ary trees, prefix sums and multisets, ACM Transactions on Algorithms 3(4), Article 43, 2007
    locator: the construction of the fully indexable dictionary from blocks stored as a class and an offset, with the space bound lg C(n, m) + O(n lg lg n / lg n)
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 4, Sections 4.1.1 (Zero-Order Compression) and 4.2.3 (Rank on Compressed Bitvectors)
  - paper: doi:10.1007/978-3-540-89097-3_18
    title: Francisco Claude and Gonzalo Navarro, Practical rank/select queries over arbitrary sequences, String Processing and Information Retrieval (SPIRE 2008), LNCS 5280, 176-187
    locator: the implementation of the Raman, Raman and Rao bit vector with sampled ranks and pointers
---

The RRR bit vector stores a static bit vector $B$ of $n$ bits with $m$ ones in $\lg \binom{n}{m} + O(n \lg \lg n / \lg n)$ bits, which is at most $n H_0(B) + o(n)$, and answers access and rank in $O(1)$ time on the [word RAM](/word-ram/). It cuts $B$ into blocks of $b$ bits and stores each block as a pair: its *class*, the number of 1s in it, and its *offset*, the index of the block among all blocks of that class. A block with few or many 1s has a short offset, so a vector with few 1s, or few 0s, shrinks. Raman, Raman and Rao introduced it in 2002 as the base of their [fully indexable dictionary](/fully-indexable-dictionary/). This page is about the block encoding and its proof of space; the set interface and the reductions are on the dictionary page.

## In plain words

Cut a long row of bits into short pieces. Instead of writing each piece as it is, first write how many 1s it has. Once that count is known, the piece is one of a short list of possible pieces with that count, so it is enough to write its number in that list.

If the count is 0 or equal to the length, the list has one entry and nothing more needs to be written. If the count is small, the list is short and its numbers are short. So a row with few 1s takes far fewer bits than its length.

To answer a question about a position, keep a running count of 1s and a pointer into the written pieces every few pieces. Jump to the right piece, rebuild it from its count and its number, and look inside.

## The abstract type

The structure answers the queries of the [rank and select problem](/rank-select-problem/) on a static bit vector: `build(B)`, `access(i)` for $0 \le i < n$, `rank1(i)` and `rank0(i)` for $0 \le i \le n$, `select1(j)` for $1 \le j \le m$ and `select0(j)` for $1 \le j \le n - m$. The rank counts the bits before position $i$, and select returns a 0-based position. Bit $j$ of a block is $B[t b + j]$ for block $t$, so the lowest bit of the block word is the leftmost bit of the block.

## Representation

Fix a block length $b$ and a superblock of $k$ blocks. The vector is cut into $\lceil n/b \rceil$ blocks; the last one has $b' = n - (\lceil n/b \rceil - 1) b$ bits. For block $t$, with $c_t$ ones at the positions $p_1 < p_2 < \cdots < p_{c_t}$ inside the block:

- **Class.** $K[t] = c_t$, stored in $\lceil \lg(b+1) \rceil$ bits.
- **Offset.** $O[t] = \sum_{i=1}^{c_t} \binom{p_i}{i}$, the rank of the block among the $\binom{b}{c_t}$ blocks of class $c_t$ in the [combinatorial number system](/combinatorial-number-system/). It is stored in $L[c_t] = \lceil \lg \binom{b}{c_t} \rceil$ bits, or $\lceil \lg \binom{b'}{c_t} \rceil$ bits for the last block, and the offsets of all blocks are written one after another in a bit stream $O$.
- **Samples.** For each superblock $q$, $R[q]$ is the number of 1s before it and $P[q]$ is the position in $O$ where its first offset starts. For each block $t$, $RB[t]$ and $PB[t]$ are the same counts measured from the start of its superblock.

A table of $\binom{j}{c}$ for $0 \le j, c \le b$ and the table $L$ are shared. The invariant is that each field holds the value that its definition gives; the structure is static.

## Operations

```pseudo id=main
ENCODE(x)                                    ▷ x: a block of b bits
L1  c ← 0, o ← 0
L2  for j ← 0 to b − 1 do
L3      if bit j of x is 1 then c ← c + 1, o ← o + C(j, c)
L4  return (c, o)

DECODE(c, o)                                 ▷ the block of class c and offset o
L5  x ← 0
L6  for j ← b − 1 downto 0 do
L7      if c > 0 and o ≥ C(j, c) then
L8          x ← x or 2^j, o ← o − C(j, c), c ← c − 1
L9  return x

ACCESS(i)                                    ▷ 0 ≤ i < n
L10 t ← ⌊i / b⌋, q ← ⌊t / k⌋
L11 return bit (i mod b) of DECODE(K[t], READ(P[q] + PB[t], L[K[t]]))

RANK1(i)                                     ▷ 0 ≤ i ≤ n
L12 t ← ⌊i / b⌋, q ← ⌊t / k⌋
L13 if i mod b = 0 then return R[q] + RB[t]
L14 x ← DECODE(K[t], READ(P[q] + PB[t], L[K[t]]))
L15 return R[q] + RB[t] + POPCOUNT(x and (2^(i mod b) − 1))

SELECT1(j)                                   ▷ 1 ≤ j ≤ m
L16 q ← the last superblock with R[q] < j          ▷ binary search
L17 t ← the last block of superblock q with R[q] + RB[t] < j
L18 x ← DECODE(K[t], READ(P[q] + PB[t], L[K[t]]))
L19 return t·b + the position of the (j − R[q] − RB[t])-th 1 of x
```

READ$(p, \ell)$ returns the $\ell$ bits of the stream $O$ that start at position $p$, as an integer; it reads at most two words when $\ell \le w$. $C(j, c)$ is the binomial coefficient, read from the table, and it is 0 when $c > j$. For the last block, $L[K[t]]$ stands for $\lceil \lg \binom{b'}{K[t]} \rceil$.

**Build.** One pass over the blocks computes $K[t]$ and $O[t]$ by ENCODE, appends $O[t]$ to the stream and fills the samples. The time is $O(n)$ with a table for ENCODE, or $O(n)$ bit steps with the loop.

**Access and rank.** Lines L10 and L12 find the block and its superblock. The pointer $P[q] + PB[t]$ is where the offset of block $t$ starts, so line L14 rebuilds the block, and line L15 adds the 1s of the block before position $i$. Line L13 skips the decode when $i$ is at a block boundary, which also covers $i = n$. Then $\text{rank}_0(i) = i - \text{rank}_1(i)$.

**Select.** Lines L16 and L17 find, by two binary searches, the block that holds the $j$-th 1, and line L19 finds the 1 inside the decoded block. $\text{select}_0$ is the same with $q k b - R[q]$ and the class $b - K[t]$ in place of the counts of 1s.

**Constant time.** With $b = \lfloor \frac12 \lg n \rfloor$, there are at most $2^b = \sqrt{n}$ blocks, so ENCODE and DECODE become reads of a table of $O(\sqrt{n} \lg n)$ bits, as in the [method of Four Russians](/four-russians-method/). Access and rank are then $O(1)$. Select is $O(\lg n)$ with the binary searches above; Raman, Raman and Rao make it $O(1)$ with a select index in the style of [Clark](/rank-select-dictionary/) built on the same blocks.

## Example

Take $B = 1011\,0010\,1100\,0111$, with $n = 16$ and $m = 9$, blocks of $b = 4$ bits and superblocks of $k = 2$ blocks. The table $L$ is $L[0..4] = [0, 2, 3, 2, 0]$, from $\binom{4}{c} = 1, 4, 6, 4, 1$.

| block $t$ | bits | positions of the 1s | class $K[t]$ | offset $O[t]$ | $L[K[t]]$ | $RB[t]$ | $PB[t]$ |
|---|---|---|---|---|---|---|---|
| 0 | 1011 | 0, 2, 3 | 3 | $\binom01 + \binom22 + \binom33 = 2$ | 2 | 0 | 0 |
| 1 | 0010 | 2 | 1 | $\binom21 = 2$ | 2 | 3 | 2 |
| 2 | 1100 | 0, 1 | 2 | $\binom01 + \binom12 = 0$ | 3 | 0 | 0 |
| 3 | 0111 | 1, 2, 3 | 3 | $\binom11 + \binom22 + \binom33 = 3$ | 2 | 2 | 3 |

The superblock samples are $R = [0, 4]$ and $P = [0, 4]$. The offset stream has $2 + 2 + 3 + 2 = 9$ bits, while $\lg \binom{16}{9} = \lg 11440 \approx 13.5$; the classes take $4 \cdot 3 = 12$ bits more, which is why real blocks are longer.

- RANK1$(13)$: $t = 3$, $q = 1$, so the count so far is $R[1] + RB[3] = 6$, and the offset starts at $P[1] + PB[3] = 7$. DECODE$(3, 3)$ tests $j = 3, 2, 1$ against $\binom33 = 1$, $\binom22 = 1$, $\binom11 = 1$ and sets all three bits, so the block has 1s at 1, 2 and 3. No 1 is below position $13 \bmod 4 = 1$, so the answer is 6.
- RANK1$(10)$: $t = 2$, $q = 1$, count $4 + 0 = 4$. DECODE$(2, 0)$ fails the tests at $j = 3$ and $j = 2$, since $\binom32 = 3$ and $\binom22 = 1$ are larger than 0, and then sets bits 1 and 0. Two 1s are below position $2$, so the answer is 6.
- SELECT1$(5)$: $R = [0, 4]$ gives $q = 1$. In superblock 1, block 2 has $4 + 0 < 5$ and block 3 has $4 + 2 \ge 5$, so $t = 2$. The 1st 1 of block 2 is at 0, and the answer is $2 \cdot 4 + 0 = 8$.

## Correctness

ENCODE and DECODE are inverse bijections between the blocks of class $c$ and the integers $0 \le o < \binom{b}{c}$, by the combinatorial number system; the proof shows that the greedy choice in line L7 picks the largest position first. The offset stream holds the offsets of the blocks in order, and $P[q] + PB[t]$ is the sum of $L[K[t']]$ over the blocks $t' < t$, which is where offset $t$ starts. So line L14 rebuilds block $t$, and rank and select follow from the counts. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

| operation | time, worst case |
|---|---|
| build | $O(n)$ |
| access, rank | $O(1)$ with the decode table, $O(b)$ with the loop |
| select | $O(\lg n)$ by binary search; $O(1)$ with an extra select index |

**Space of the offsets.** Let $b_t$ be the length of block $t$, which is $b$ except for the last block. The number of bit vectors of length $n$ whose blocks have the classes $c_0, c_1, \ldots$ is $\prod_t \binom{b_t}{c_t}$, and these are among the $\binom{n}{m}$ vectors with $m$ ones, so $\prod_t \binom{b_t}{c_t} \le \binom{n}{m}$. Hence

$$\sum_t L_t \le \sum_t \left( \lg \binom{b_t}{c_t} + 1 \right) \le \lg \binom{n}{m} + \frac{n}{b} + 1.$$

**Space of the rest.** The classes take $\lceil n/b \rceil \lceil \lg(b+1) \rceil$ bits. With superblocks of $k b = \Theta(\lg^2 n)$ bits, $R$ and $P$ take $O(n / \lg n)$ bits, and $RB$ and $PB$ take $O(\lg \lg n)$ bits for each block. With $b = \Theta(\lg n)$, all of this is $O(n \lg \lg n / \lg n)$ bits, and the total is $\lg \binom{n}{m} + O(n \lg \lg n / \lg n)$. Since $\lg \binom{n}{m} \le n H_0(B)$, where $H_0$ is the [zero-order entropy](/shannon-entropy/) of the bits, this is $n H_0(B) + o(n)$.

## Variants

- **Sampled scan.** Claude and Navarro drop $RB$ and $PB$ and keep only $R$ and $P$ every $k$ blocks, then scan the classes of up to $k - 1$ blocks, adding their counts and their offset lengths. Rank is $O(k)$, and $k$ trades space for time.
- **Long blocks.** Navarro and Providel decode offsets with the loop of lines L5 to L9 and no table, which allows $b = 63$ and makes the class overhead $\lg 64 / 63$ bits for each bit.
- **Multisets.** Raman, Raman and Rao also store a multiset of $n$ elements from $[0, u)$ in $\lg \binom{u + n}{n} + o(n)$ bits by the same method on a vector with $u + n$ positions.
- **Very sparse vectors.** When $m$ is much smaller than $n / \lg n$, the term $n \lg \lg n / \lg n$ is larger than $\lg \binom{n}{m}$; the [SD-array](/sd-array/) or [Elias-Fano](/elias-fano-encoding/) is then smaller.
- **Compressed sequences.** The bit vectors of a [wavelet tree](/wavelet-tree/) stored as RRR give a sequence in $n H_0 + o(n \lg \sigma)$ bits.

## When to use it

Use the RRR bit vector when a static vector has a skewed or clustered distribution of 1s and space matters more than a few nanoseconds: the bit vectors of a compressed [wavelet tree](/wavelet-tree/) in an [FM-index](/fm-index/), or a sparse [characteristic vector](/fully-indexable-dictionary/). For dense random vectors it saves nothing and is slower than a plain [rank/select dictionary](/rank-select-dictionary/). For a vector with very few 1s, the [SD-array](/sd-array/) has a better redundancy.

## Pitfalls

- **Offset order.** ENCODE and DECODE must use the same order. With $O = \sum \binom{p_i}{i}$, the positions are 0-based and the indices $i$ start at 1. Mixing 0-based and 1-based indices gives offsets that collide.
- **Lengths come from the class.** The length of an offset is $L[c]$ for the class of the block, not a fixed width. A reader that uses a fixed width reads the wrong bits after the first short offset.
- **Class 0 and class $b$.** These blocks have $L = 0$; READ must return 0 without reading. A pointer that is not advanced for them is correct; one that is advanced by 1 is not.
- **The short last block.** The last block has $b' \le b$ bits. Its offset must get $\lceil \lg \binom{b'}{c} \rceil$ bits, not $L[c]$: padding it to $b$ bits wastes up to $b$ bits, and the space bound fails, for example for a vector of all 1s. $\text{select}_0$ must not count the missing bits as 0s, which is safe as long as $j \le n - m$.
- **Small $b$.** The class field costs $\lg(b+1)$ bits for each block. For $b = 4$, as in the example, the classes alone cost $3/4$ of a bit for each bit, so the structure is larger than the plain vector.

## Implementations

## History

Raman, Raman and Rao presented the fully indexable dictionary in $\lg \binom{n}{m} + O(n \lg \lg n / \lg n)$ bits at SODA 2002, with the journal version in ACM Transactions on Algorithms in 2007. Its core is the encoding of each short block by its class and its offset, an instance of [enumerative coding](/enumerative-coding/). Claude and Navarro gave a practical implementation in 2008 with sampled pointers, and later work by Navarro and Providel replaced the decode table with on-the-fly decoding to allow longer blocks.

## References
