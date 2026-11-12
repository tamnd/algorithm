---
tag: FD46E0
kind: data-structure
slug: tree-bitmap
name: Tree bitmap
aliases:
- multibit trie with bitmaps
- tree bitmap trie
- Eatherton tree bitmap
area: systems/networking-algorithms
level: advanced
summary: "A multibit trie for longest prefix match. Each node has an internal bitmap of its prefixes and an external bitmap of its children, and a popcount finds the array slot."
solves: [longest-prefix-match]
model: word-ram
complexity:
  vars: {n: the number of prefixes, W: the address width, s: the stride of a node}
  time: {worst: O(W/s), update: O(W/s + 2^s)}
  space: {extra: O(n W / s)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [longest-prefix-match, trie, population-count]
see_also: [radix-tree, roaring-bitmap, packet-classification, bit-set, routing-problem]
sources:
  - paper: doi:10.1145/997150.997160
    title: Will Eatherton, George Varghese and Zubin Dittia, Tree bitmap, hardware/software IP lookups with incremental updates, ACM SIGCOMM Computer Communication Review 34(2), 2004
    locator: pages 97 to 122 (the node layout with internal and external bitmaps, the lookup, incremental updates and the hardware optimizations)
  - book: isbn:9780120884773
    title: George Varghese, Network Algorithmics, Morgan Kaufmann, 2005
    locator: Chapter 11, Section 11.8 (Tree bitmap) and Section 11.7 (Lulea-compressed tries, for the contrast)
  - paper: doi:10.1145/263105.263133
    title: Mikael Degermark, Andrej Brodnik, Svante Carlsson and Stephen Pink, Small forwarding tables for fast routing lookups, ACM SIGCOMM 1997
    locator: pages 3 to 14 (the Lulea scheme, with leaf pushing and bitmap compression)
  - paper: doi:10.1145/296502.296503
    title: V. Srinivasan and George Varghese, Fast address lookups using controlled prefix expansion, ACM Transactions on Computer Systems 17(1), 1999
    locator: pages 1 to 40 (multibit tries with expanded prefixes, the uncompressed baseline)
---

A tree bitmap is a multibit [trie](/trie/) for [longest prefix match](/longest-prefix-match/) in which each node of stride $s$ stores two bitmaps instead of an array of $2^s$ pointers: an *internal bitmap* of $2^s - 1$ bits for the prefixes that end inside the node, and an *external bitmap* of $2^s$ bits for the children that exist. The children of a node are stored side by side in one array, so one pointer and a [population count](/population-count/) of the bits below a position give the address of any child; the next hops are kept in a separate result array in the same way. A lookup reads one node for each $s$ bits of the address and then one result, at most $\lfloor W/s \rfloor + 2$ reads, and an insert or a delete changes only the nodes on one path. Eatherton, Varghese and Dittia published it in 2004.

## In plain words

A plain trie for addresses looks at one bit at a time, so a lookup can take more than thirty steps. A trie that looks at four bits at a time takes about eight steps, but each node needs sixteen pointers, and most of them are empty.

A tree bitmap keeps the four-bit steps and drops the empty pointers. Each node keeps a short row of yes/no marks for "which of my sixteen children exist", and one more row for "which short routes end inside me". The children of a node sit next to each other in memory. To find the fifth child that exists, count the marks before it and add that count to the one pointer. Processors count marks in one instruction. Because the node keeps its own routes, a change of one route touches only one node, not a large copied block.

## The abstract type

The structure stores a set $T$ of prefixes of $W$-bit addresses, each with a next hop, and supports:

- LOOKUP$(a)$: the next hop of the longest prefix in $T$ that matches the address $a$, or "no route";
- INSERT$(p, \ell, h)$: add the prefix $(p, \ell)$ with next hop $h$, or replace its next hop;
- DELETE$(p, \ell)$: remove the prefix $(p, \ell)$.

A prefix $(p, \ell)$ has $0 \le \ell \le W$ and $0 \le p < 2^\ell$, and it matches $a$ if the top $\ell$ bits of $a$ equal $p$. This is the dynamic version of the [longest prefix match](/longest-prefix-match/) problem. The model is a word RAM with a popcount instruction, and the cost that the design counts is memory reads per lookup.

## Representation

Fix the stride $s$. The node at depth $k$ covers the address bits $ks$ to $ks + s - 1$ of the paths that reach it. Each node holds four fields:

- `internal`: $2^s - 1$ bits. The prefix that ends in this node after $j$ more bits, with $0 \le j \le s - 1$ and value $v < 2^j$, has bit $2^j - 1 + v$. So bit 0 is the node's own string, bits 1 and 2 are its extensions `0` and `1`, bits 3 to 6 are `00` to `11`, and so on.
- `external`: $2^s$ bits. Bit $c$ is 1 if the child for the next $s$ bits $c$ exists.
- `children`: one pointer to a contiguous array of the existing children, in increasing order of $c$.
- `results`: one pointer to a contiguous array of the next hops of the internal prefixes, in increasing order of bit index.

A prefix $(p, \ell)$ lives in the node at depth $\lfloor \ell/s \rfloor$ on its path, as the in-node prefix of length $\ell \bmod s$. A prefix whose length is a multiple of $s$ is therefore bit 0 of a child node, not a bit of its parent. The position of the child $c$ in the array is

$$\mathrm{rank}(\mathit{external}, c) = \mathrm{popcount}(\mathit{external} \wedge (2^c - 1)),$$

and the same rank on `internal` gives the position of a result. With $s = 4$ a node has 15 + 16 = 31 bitmap bits and two pointers, so it fits in one wide memory word. The result array is read only once per lookup, at the end, so in hardware it can sit in slower memory.

## Operations

```pseudo id=main
TB-LOOKUP(root, a)                         ▷ rank(B, i) = popcount(B AND (2^i − 1))
L1  node ← root, k ← 0
L2  best ← none
L3  loop
L4      c ← the s bits of a from bit ks, padded with zeros past bit W − 1
L5      for j ← min(s − 1, W − ks) down to 0 do          ▷ longest in-node prefix first
L6          if bit 2^j − 1 + (the first j bits of c) of node.internal is 1 then
L7              best ← (node, rank(node.internal, that bit)); break
L8      if (k + 1)s > W or bit c of node.external is 0 then exit the loop
L9      node ← node.children[rank(node.external, c)], k ← k + 1
L10 if best = none then return no route
L11 return best.node.results[best.position]
```

The lookup keeps only a node and a position in `best` and reads the result array once, at line L11. This is the main saving in hardware: the bitmaps of each node arrive with the node, so the search of lines L5 to L7 costs no extra memory read.

**Insert.** Walk the path of the first $\lfloor \ell / s \rfloor s$ bits of $p$. At each step, if bit $c$ of `external` is 0, set it and insert a new empty node into `children` at position $\mathrm{rank}(\mathit{external}, c)$. At the last node, set the internal bit $i = 2^j - 1 + v$ with $j = \ell \bmod s$, and insert the next hop into `results` at position $\mathrm{rank}(\mathit{internal}, i)$, or overwrite it if the bit was already 1.

**Delete.** Walk the same path. Clear the internal bit and remove its result. Then, from the bottom up, free each node other than the root whose two bitmaps are both 0, and clear its bit in the parent's `external` and remove it from the parent's `children`.

In hardware, a change of a child array means: allocate a new array one slot larger or smaller, copy the other children, then switch the one parent pointer. A lookup that runs at the same time sees either the old array or the new one.

## Example

Take $W = 8$, $s = 4$, and the prefixes A = `*`, B = `1*`, C = `101*`, D = `10110*`, E = `1011011*` and F = `0110*`. A, B and C have lengths 0, 1 and 3, so they live in the root. D and E have lengths 5 and 7, so they live in the child for the first four bits `1011` (11). F has length 4, so it is bit 0 of the child for `0110` (6). The bitmaps, written in bit-index order and grouped by in-node length (0, 1, 2 and 3), are:

| node | internal (lengths 0, 1, 2, 3) | external (children 0 to 15) | results |
|---|---|---|---|
| root | 1 01 0000 00000100 | 0000001000010000 | A, B, C |
| child 6 (`0110`) | 1 00 0000 00000000 | all zero | F |
| child 11 (`1011`) | 0 10 0000 00010000 | all zero | D, E |

The root's internal bits are 0 (A), $2^1 - 1 + 1 = 2$ (B) and $2^3 - 1 + 5 = 12$ (C). In child 11, D is `0` after `1011`, bit $2^1 - 1 + 0 = 1$, and E is `011`, bit $2^3 - 1 + 3 = 10$. The root's children array is [child 6, child 11], because bit 6 comes before bit 11.

**Lookup of 10110110.** At the root, $c$ = `1011`. The in-node search tries `101` first: bit 12 is 1, so best is (root, position $\mathrm{rank} = 2$), which is C. External bit 11 is 1, and $\mathrm{rank}(\mathit{external}, 11) = 1$ because only bit 6 is below it, so the next node is children[1] = child 11. There $c$ = `0110`. The search tries `011`: bit 10 is 1, so best becomes (child 11, position 1). External bit 6 of child 11 is 0, so the loop stops. The one result read returns results[1] = E. The lookup made 3 reads: two nodes and one result.

**Other lookups.** 10110001 gives D (bit 1 of child 11), 10111111 gives C (child 11 has no prefix `111`, `11`, `1` or empty), 01100000 gives F, and 01110000 gives A after 2 reads, because the root has no child 7.

**A random IPv4 table.** On the synthetic table of the [longest prefix match](/longest-prefix-match/) page (seed 1, 1723 prefixes), with 10000 addresses drawn inside random prefixes of the table:

| stride $s$ | nodes | bitmap bits in all nodes | mean reads | most reads |
|---|---|---|---|---|
| 1 | 12919 | 38757 | 21.49 | 34 |
| 2 | 6447 | 45129 | 11.49 | 18 |
| 4 | 3213 | 99603 | 6.50 | 10 |
| 8 | 1527 | 780297 | 4.01 | 6 |

The reads include the one result read. With $s = 1$ the nodes are exactly the nodes of the binary trie. Stride 4 cuts the reads by a factor of about 3 for about 2.6 times the bitmap memory of stride 1; stride 8 costs about 20 times the memory.

## Correctness

The structure keeps one invariant: each prefix is the internal bit $2^j - 1 + v$ of the node that its first $\lfloor \ell / s \rfloor s$ bits reach; each array has one entry for each 1 bit of its bitmap, in bit order; and no node other than the root is empty. Under this invariant, the lookup visits exactly the nodes on the path of the address, finds the longest matching prefix in each, and the deepest one found is the longest match overall, because a node deeper on the path holds only longer prefixes. Rank gives the array slot because the slots before an entry are exactly the entries of the 1 bits below it. Insert and delete keep the invariant because they add or remove an entry at its rank position at the same time as they set or clear its bit. The full proof is in the proofs file.

## Complexity

Let $n$ be the number of prefixes, $W$ the address width and $s$ the stride.

- **Lookup.** At most $\lfloor W/s \rfloor + 1$ node reads and 1 result read, in the worst case. For IPv4 with $s = 4$ that is 9 node reads and 10 reads in all. The work inside a node is $O(s)$ bit tests and two popcounts on words of $2^s$ bits, which hardware does in parallel.
- **Space.** At most $n \lfloor W/s \rfloor + 1$ nodes, because every node other than the root is on the path of a stored prefix. Each node has $2^{s+1} - 1$ bitmap bits and two pointers. The result arrays have $n$ entries in all. Unlike controlled prefix expansion, no prefix is copied.
- **Update.** An insert or a delete walks at most $\lfloor W/s \rfloor$ nodes and copies the child array or result array of a constant number of nodes on the path, each of at most $2^s$ entries. So an update costs $O(W/s + 2^s)$ time in the worst case. This is the point of the design: a single route change never forces a rebuild of a large table.

These bounds are worst case and hold for every table. The memory numbers in the example above are measured on one synthetic table; real tables, with most prefixes of length 24 for IPv4, give other numbers.

## Variants

- **Initial array.** Replace the top levels by one direct table indexed by the first 8 to 16 bits, which removes several reads at the cost of a fixed block of memory.
- **Different strides by level.** The stride need not be the same at each depth. A designer picks the strides so that one node fits the width of one memory read.
- **Split and segmented bitmaps.** For a large stride the bitmaps no longer fit in one memory word. The paper splits a node so that a read fetches only the part of the bitmap that the next bits of the address need.
- **Lulea, the contrast.** The Lulea scheme of Degermark, Brodnik, Carlsson and Pink (1997) also uses bitmaps and popcounts, but it first *pushes* each prefix down to the leaves, so that each node has one bitmap of where the answer changes. Its tables are smaller, but the scheme is built for a static table: one route change can rewrite many pushed copies and the codewords after them. The tree bitmap keeps internal prefixes in the node where they end, so it needs no leaf pushing and supports incremental updates.
- **Multibit trie with controlled prefix expansion.** The uncompressed version of the same trie, with an array of $2^s$ entries in each node and each prefix expanded to the node boundary (Srinivasan and Varghese, 1999). The tree bitmap stores the same trie shape without the empty entries and without the copies.

## When to use it

Use a tree bitmap for a forwarding table that changes often, when a lookup must finish in a small fixed number of memory reads: in a router line card, or in a software router with a cache line per node. For a static table, a fully compressed scheme can be smaller. When the memory reads do not matter and only the code size does, a binary trie or a hash table per prefix length is simpler. A [roaring bitmap](/roaring-bitmap/) is a different structure: it compresses a large set of integers, not a trie node.

## Pitfalls

- **Off by one in the internal bitmap.** It has $2^s - 1$ bits, not $2^s$: the in-node lengths are $0$ to $s - 1$, and a prefix of length $ks$ belongs to bit 0 of the child, not to a length-$s$ bit of the parent. Code that puts it in the parent stores it twice or loses it.
- **The rank of the wrong bitmap.** Children use the rank in `external`, results use the rank in `internal`. Mixing them returns a wrong next hop with no error.
- **Rank must count bits strictly below.** $\mathrm{popcount}(B \wedge (2^c - 1))$, not $\mathrm{popcount}(B \wedge (2^{c+1} - 1))$. The second form counts the bit itself and is off by one.
- **Bit order.** Hardware descriptions often number bits from the left (the most significant bit first). Any order works if insert, delete and lookup use the same one.
- **Empty nodes after a delete.** A node with no prefix and no child must be freed, or the lookup still follows it and the memory grows.
- **The last partial chunk.** When $s$ does not divide $W$, the last node covers fewer than $s$ address bits. Pad the chunk and stop the in-node search at the remaining length.

## Implementations

## History

Eatherton, Varghese and Dittia described the tree bitmap in an ACM SIGCOMM Computer Communication Review article in 2004. It came after the Lulea scheme (1997) and controlled prefix expansion (1999), and it kept their multibit trie and bitmap compression while it removed leaf pushing so that updates stay local. Varghese's book Network Algorithmics (2005) gives it its own section, Section 11.8.

## References
