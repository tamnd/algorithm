---
tag: ZZJ07J
kind: data-structure
slug: dynamic-bit-vector
name: Dynamic bit vector
aliases:
- dynamic bitvector
area: data-structures/succinct-structures
level: advanced
summary: A bit vector that supports insertions and deletions along with rank and select, usually in O(log n) time.
model: word-ram
complexity:
  vars: {n: the current length of the bit vector}
  time: {access: O(log n), rank: O(log n), select: O(log n), insert: O(log n), delete: O(log n), set: O(log n)}
  space: {total: "n + O(n / log n)"}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2001
  people: [Rajeev Raman, Venkatesh Raman, S. Srinivasa Rao]
  note: Raman, Raman and Rao studied succinct dynamic bit vectors and prefix sums in 2001; Mäkinen and Navarro used balanced trees of bit blocks for dynamic compressed sequences in 2008, and Navarro and Sadakane reached the optimal O(log n / log log n) time with insertions and deletions.
prereqs: [rank-select-problem, implicit-treap, balanced-binary-search-tree]
see_also: [rank-select-dictionary, bit-vector, order-statistic-tree, fenwick-tree, rope, partial-sums-problem, range-min-max-tree, succinct-data-structures]
sources:
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 12 (Dynamic Structures), Section 12.1 (Bitvectors), the balanced tree of blocks with counts of bits and 1s
  - paper: doi:10.1145/1367064.1367072
    title: Veli Mäkinen and Gonzalo Navarro, Dynamic entropy-compressed sequences and full-text indexes, ACM Transactions on Algorithms 4(3), Article 32, 2008
    locator: the dynamic bit vector as a balanced tree over blocks, with rank, select, insert and delete in O(lg n) time
  - paper: doi:10.1145/2601073
    title: Gonzalo Navarro and Kunihiko Sadakane, Fully functional static and dynamic succinct trees, ACM Transactions on Algorithms 10(3), Article 16, 2014
    locator: the dynamic bit vectors and parentheses with operations in O(lg n / lg lg n) time
  - paper: doi:10.1145/73007.73040
    title: Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, 21st ACM Symposium on Theory of Computing (STOC 1989), 345-354
    locator: the Omega(lg n / lg lg n) lower bound for dynamic prefix parity, which applies to rank under bit flips
  - paper: "Rajeev Raman, Venkatesh Raman and S. Srinivasa Rao, Succinct dynamic data structures, Workshop on Algorithms and Data Structures (WADS 2001), LNCS 2125, 426-437"
    locator: dynamic rank, select and prefix sums in succinct space
---

A dynamic bit vector stores a sequence of $n$ bits and supports access, [rank and select](/rank-select-problem/) together with updates: inserting a bit at any position, deleting one, and flipping one. A static [rank/select dictionary](/rank-select-dictionary/) answers queries in $O(1)$ time, but one insertion would shift every later position and force a rebuild. The standard dynamic solution cuts the bits into chunks of $\Theta(\lg^2 n)$ bits and keeps them in a balanced tree whose nodes store the number of bits and of 1s below them, so that every operation takes $O(\lg n)$ time on the [word RAM](/word-ram/) in $n + O(n / \lg n)$ bits. The optimum is $\Theta(\lg n / \lg \lg n)$: Fredman and Saks proved the lower bound in 1989, and Navarro and Sadakane matched it. Dynamic bit vectors are the base layer of dynamic succinct trees, dynamic wavelet trees and dynamic FM-indexes.

## In plain words

A long row of bits with rank and select is easy to search when it never changes. Once you can insert a bit in the middle, every count after that point moves by one, and fixing them all is slow.

So cut the row into pieces of a few hundred bits each, and keep the pieces in a balanced search tree in their left-to-right order. Each tree node remembers how many bits and how many 1s lie in its part of the tree. To find a position or a count, walk down from the top using those numbers, and finish inside one piece. To insert a bit, change one piece and fix the numbers on the way back up. A piece that grows too big is cut in two.

## The abstract type

A sequence $B[0..n-1]$ of bits with:

- `access(i)`: the bit $B[i]$;
- `rank1(i)`: the number of 1s in $B[0..i-1]$, for $0 \le i \le n$, and `rank0(i)` $= i - $ `rank1(i)`;
- `select1(j)` and `select0(j)`: the position of the $j$-th 1 or 0, for $j \ge 1$;
- `insert(i, b)`: make $b$ the new bit at position $i$, shifting $B[i..n-1]$ right;
- `delete(i)`: remove $B[i]$, shifting the rest left;
- `set(i, b)`: overwrite $B[i]$.

Positions are 0-based, as on the [rank and select problem](/rank-select-problem/) page.

## Representation

The bits are split into consecutive *chunks*, each of at most $2\beta$ bits, where $\beta = \Theta(\lg^2 n)$ bits in theory and a few hundred to a few thousand bits in practice. The chunks are the nodes of a [balanced binary search tree](/balanced-binary-search-tree/) ordered by position, here an [implicit treap](/implicit-treap/), so that an in-order walk lists the chunks from left to right. Each node $x$ stores:

- its chunk, packed in words;
- $\text{size}(x)$, the number of bits in its subtree, and $\text{ones}(x)$, the number of 1s in its subtree.

The invariant is that every node's counts equal the sums over its left subtree, its chunk and its right subtree, and that the in-order concatenation of the chunks is $B$. Positions are never stored; they are derived from the sizes on the way down, which is what makes insertion cheap. This is the same idea as an [order-statistic tree](/order-statistic-tree/) or a [rope](/rope/), applied to blocks of bits.

## Operations

```pseudo id=main
RANK1(i)
L1  x ← root;  r ← 0
L2  while x ≠ nil do
L3      if i < size(left(x)) then x ← left(x)
L4      else if i ≤ size(left(x)) + |chunk(x)| then return r + ones(left(x)) + POPCOUNT(chunk(x)[0 .. i − size(left(x)) − 1])
L5      else r ← r + ones(left(x)) + ones in chunk(x);  i ← i − size(left(x)) − |chunk(x)|;  x ← right(x)
L6  return r

SELECT1(j)
L7  x ← root;  base ← 0
L8  while x ≠ nil do
L9      if j ≤ ones(left(x)) then x ← left(x)
L10     else if j ≤ ones(left(x)) + ones in chunk(x) then return base + size(left(x)) + SELECT-IN-CHUNK(chunk(x), j − ones(left(x)))
L11     else j ← j − ones(left(x)) − ones in chunk(x);  base ← base + size(left(x)) + |chunk(x)|;  x ← right(x)

INSERT(i, b)
L12 find, as in RANK1, the node x whose chunk holds position i, its offset o and the path to it
L13 insert b at offset o of chunk(x)
L14 add 1 to size, and b to ones, of every node on the path
L15 if |chunk(x)| > 2β then split chunk(x) into two halves and insert the second half as a new node right after x

DELETE(i)
L16 find the node x holding position i, its offset o and the path to it
L17 remove the bit at offset o of chunk(x)
L18 subtract 1 from size, and the removed bit from ones, of every node on the path
L19 if chunk(x) is empty then remove the node x from the tree
```

**Queries.** RANK1 and SELECT1 walk down one path, so they take time proportional to the height plus the work inside one chunk. Inside a chunk of $2\beta$ bits, rank is a popcount over $O(\beta / w)$ words, and select is a scan of word popcounts followed by a select in one word. `access` is the same walk as rank. `select0` is the same walk as SELECT1 with $\text{size} - \text{ones}$ in place of ones; this page's implementation uses a binary search over `rank0` instead.

**Updates.** An insertion shifts the bits of one chunk, $O(\beta / w)$ word operations, and fixes $O(\lg n)$ counts. Splitting a full chunk creates one tree node, inserted by the tree's usual method with rebalancing in $O(\lg n)$ time. `set` changes one bit and the ones counts on the path.

**Keeping chunks full.** For the space bound, chunks must stay at least about half full. A real implementation merges a chunk that falls below $\beta/2$ bits with a neighbor, splitting again if the merge exceeds $2\beta$. This page's implementation only removes empty chunks.

## Example

Take $B = 01101001$ with chunk parameter $\beta = 2$, so chunks hold at most 4 bits, and suppose the tree has the chunk `10` (positions 2-3) at the root, `01` (positions 0-1) as its left child, `10` (positions 4-5) as its right child, and `01` (positions 6-7) as the right child of that.

| node | chunk | size | ones |
|---|---|---|---|
| root | `10` | 8 | 4 |
| left | `01` | 2 | 1 |
| right | `10` | 4 | 2 |
| right's right | `01` | 2 | 1 |

- RANK1$(5)$: at the root, $\text{size}(\text{left}) = 2$ and $5 > 2 + 2$, so add $1 + 1 = 2$, set $i = 1$ and go right. There $\text{size}(\text{left}) = 0$ and $1 \le 2$, so the answer is $2 + 0 + \text{popcount}(1) = 3$. Indeed $01101$ has three 1s.
- SELECT1$(3)$: at the root, $3 > 1 + 1$, so $j = 1$, base $= 4$, go right; there $j \le 0 + 1$, and the first 1 of `10` is at offset 0, so the answer is position 4.
- INSERT$(2, 1)$: position 2 is offset 0 of the root's chunk, which becomes `110`; the root's counts become 9 and 5. The vector is now $011101001$, and RANK1$(5) = 3$, SELECT1$(4) = 5$.
- Inserting two more bits into the root's chunk would make it 5 bits long, more than $2\beta = 4$, and it would be split into two chunks of 2 and 3 bits.
- DELETE$(0)$ then removes the 0 from the left chunk, which becomes `1`, and the vector is $11101001$, with SELECT1$(4) = 4$ and SELECT0$(1) = 3$.

## Correctness

The proof keeps two invariants: the in-order concatenation of the chunks is the vector, and each node's size and ones are the sums over its subtree. Under them, the walk of RANK1 keeps the loop invariant that the answer is $r$ plus the number of 1s before the current offset $i$ in the subtree of $x$, and SELECT1 the matching invariant for $j$. Each update changes one chunk and fixes exactly the nodes whose subtrees contain it, and splitting or removing a chunk keeps the order. See [the proof of correctness](proofs/correctness.md).

## Complexity

| operation | time, chunks of $\Theta(\lg^2 n)$ bits | this page's implementation |
|---|---|---|
| access, rank, select | $O(\lg n)$ | $O(\lg n + \beta)$ expected |
| insert, delete, set | $O(\lg n)$ | $O(\lg n + \beta)$ expected |
| build from $n$ bits | $O(n / w)$ | $O(n)$ expected |

With chunks of $\Theta(\lg^2 n)$ bits there are $O(n / \lg^2 n)$ nodes, each with a few counters and pointers of $O(\lg n)$ bits, so the tree adds $O(n / \lg n)$ bits to the $n$ bits of the chunks, provided chunks are kept at least half full and allocated tightly. A chunk of $\Theta(\lg^2 n)$ bits is $\Theta(\lg n)$ words, so work inside it is $O(\lg n)$ with popcount, matching the height. The implementation here stores bits as Python list items, for clarity, and uses a treap, whose height is $O(\lg n)$ in expectation.

**Lower bound.** Fredman and Saks showed that maintaining prefix parity under bit flips needs $\Omega(\lg n / \lg \lg n)$ time per operation in the [cell-probe model](/cell-probe-model/), and rank parity is prefix parity, so $O(\lg n / \lg \lg n)$ is the best possible for rank with updates. Trees of large fan-out, with $\Theta(\lg^\varepsilon n)$ children per node and small in-node prefix-sum structures, achieve it.

## Variants

- **B-tree of blocks.** In practice a [B-tree](/b-tree/)-like tree with fan-out 16 to 64 and leaves of 512 to 4096 bits is fastest; the height is 3 or 4 for billions of bits.
- **Flips only.** If only `set` is needed, the length is fixed, and a [Fenwick tree](/fenwick-tree/) of block counts gives rank in $O(\lg n)$ time with a simpler layout.
- **Compressed dynamic bit vectors.** Storing each chunk with gap or run-length codes, or as an RRR block sequence, gives $n H_0 + o(n)$ bits with the same tree (Mäkinen and Navarro).
- **Dynamic sequences.** A dynamic wavelet tree over dynamic bit vectors gives a dynamic [static sequence](/static-sequence/) interface with $O(\lg n \lg \sigma)$ time, and dynamic FM-indexes build on it.
- **Dynamic parentheses.** Adding the minimum and maximum excess to each node gives the dynamic [range min-max tree](/range-min-max-tree/) and dynamic succinct trees.

## When to use it

Use a dynamic bit vector when a rank/select structure must accept insertions and deletions in the middle: dynamic succinct trees and tries, dynamic text indexes that accept new documents, and compressed sets with arbitrary insertion. When the vector changes rarely, a static [rank/select dictionary](/rank-select-dictionary/) rebuilt in batches is faster for queries by a factor of 5 to 20 in practice. When only appends happen, a static structure extended block by block suffices.

## Pitfalls

- **Positions are not stored.** Storing positions or global ranks in nodes makes every insertion $O(n)$; store only subtree counts.
- **Rank at the end.** RANK1$(n)$ must reach the last chunk and use its full length; the condition on line L4 uses $\le$ for this reason.
- **Insertion at position $n$.** The node holding "position $n$" is the last chunk, at offset equal to its length; a search that looks for a chunk strictly containing $i$ fails there.
- **Underfull chunks.** Without merging, many deletions can leave chunks of one bit each and the space grows to $\Theta(n \lg n)$ bits. This page's implementation has this weakness on purpose, to stay short.
- **Count overflow.** The counts at the root are up to $n$; use full words, not the small counters of static structures.

## Implementations

## History

Fredman and Saks proved the $\Omega(\lg n / \lg \lg n)$ lower bound for dynamic prefix parity in 1989. Raman, Raman and Rao studied succinct dynamic bit vectors, prefix sums and select in 2001. Mäkinen and Navarro used balanced trees over blocks for dynamic entropy-compressed sequences and full-text indexes in 2008, and Navarro and Sadakane reached $O(\lg n / \lg \lg n)$ time for insertion, deletion, rank and select in succinct space as part of their dynamic succinct trees in 2014. Libraries such as DYNAMIC and the dynamic structures of sdsl and succinct use B-trees of bit blocks.

## References
