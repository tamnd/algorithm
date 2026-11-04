---
tag: CF8HNQ
kind: algorithm
slug: geohash
name: Geohash
aliases:
- geohash encoding
area: data-structures/spatial-structures
level: core
summary: Encodes latitude and longitude as an interleaved base-32 string so that nearby points share prefixes.
solves: [bit-interleaving]
model: real-ram
complexity:
  vars: {p: the number of characters of the geohash}
  time: {worst: Θ(p)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2008
  people: [Gustavo Niemeyer]
  note: Niemeyer published geohash with the geohash.org service in 2008. The bit interleaving under it is the Z-order of Morton (1966).
prereqs: [z-order-curve, binary-search]
see_also: [morton-encoding, bit-interleaving, space-filling-curve, hilbert-curve, discrete-global-grid-system, s2-cell-hierarchy, uniform-grid, b-tree]
sources:
  - url: https://en.wikipedia.org/wiki/Geohash
    title: Geohash, Wikipedia
    locator: the sections on the algorithm, the base-32 alphabet, the worked example u4pruydqqvj, the cell sizes by length, and the edge cases near the equator and the meridians
  - paper: "G. M. Morton, A computer oriented geodetic data base and a new technique in file sequencing, IBM Ltd., Ottawa, technical report, 1966"
    locator: the interleaving of the bits of two coordinates into one key for sequencing a file (the Z-order)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 1, Multidimensional Point Data, the section on one-dimensional orderings (bit interleaving and the Morton order)
---

Geohash encodes a point on the Earth, given by its latitude and longitude, as a short string over a base-32 alphabet, such as `u4pruydqqvj`. It halves the longitude range and the latitude range in turn, records one bit for each half it keeps, and writes each group of five bits as one character. Each string names a cell of a grid, and a longer string names a smaller cell inside it, so points that share a long prefix are close together. The bit order is the [Z-order curve](/z-order-curve/) on the latitude and longitude grid, and encoding with $p$ characters takes $\Theta(p)$ time.

## In plain words

Think of the game where one person picks a number and the other asks "is it in the upper half?" again and again. Each answer is one bit, and each bit halves what is left.

Geohash plays this game with a place on the map. It asks about east or west first, then about north or south, then east or west in what is left, and so on. Every five answers become one letter or digit. After a few letters you have a small box on the map that holds the place.

A longer code is a smaller box inside the box of a shorter code. So two places whose codes start with the same letters are in the same box. The reverse is not always true: two places close to each other, on the two sides of a box edge, can have codes that start differently.

## The problem

**Input.** A latitude $\varphi \in [-90, 90]$, a longitude $\lambda \in [-180, 180]$, both in degrees, and a length $p \ge 0$.

**Output.** A string $s$ of $p$ characters over the alphabet
$$\Sigma = \texttt{0123456789bcdefghjkmnpqrstuvwxyz},$$
whose character at position $c$ has the value $v \in \{0, \ldots, 31\}$ given by its index in $\Sigma$. The letters a, i, l and o are not in $\Sigma$, to avoid confusion with digits. The $5p$ bits of $s$, most significant first in each character, are the bits $b_1 b_2 \ldots b_{5p}$ of the [bit interleaving](/bit-interleaving/) of the two coordinates, longitude first: the odd positions $b_1, b_3, \ldots$ are the leading bits of $\lambda$ in $[-180, 180]$ and the even positions are the leading bits of $\varphi$ in $[-90, 90]$.

## The algorithm

```pseudo id=main
GEOHASH-ENCODE(φ, λ, p)
L1  (φlo, φhi) ← (−90, 90);  (λlo, λhi) ← (−180, 180)
L2  s ← empty string;  bits ← 0;  ch ← 0;  even ← true
L3  while |s| < p do
L4      if even then mid ← (λlo + λhi)/2;  if λ ≥ mid then ch ← 2·ch + 1, λlo ← mid else ch ← 2·ch, λhi ← mid
L5      else mid ← (φlo + φhi)/2;  if φ ≥ mid then ch ← 2·ch + 1, φlo ← mid else ch ← 2·ch, φhi ← mid
L6      even ← not even;  bits ← bits + 1
L7      if bits = 5 then append Σ[ch] to s;  bits ← 0;  ch ← 0
L8  return s
```

The procedure keeps two intervals, one for each coordinate. Line L4 cuts the longitude interval at its midpoint, keeps the half that holds $\lambda$, and shifts a 1 into $ch$ for the upper half or a 0 for the lower half. Line L5 does the same for the latitude. Line L6 switches the axis, so the axes alternate, longitude first. After five bits, line L7 turns $ch$ into one character. A value equal to the midpoint goes to the upper half, so each cell is closed at its lower ends and open at its upper ends, except at $90$ and $180$, which fall into the top cells.

**Decoding** runs the same loop on the bits of the string: each bit says which half to keep. At the end, the two intervals are the cell of the string, and its center is the usual estimate of the point. With $p$ characters the longitude gets $\lceil 5p/2 \rceil$ bits and the latitude $\lfloor 5p/2 \rfloor$ bits, so the cell is $360 / 2^{\lceil 5p/2 \rceil}$ degrees wide and $180 / 2^{\lfloor 5p/2 \rfloor}$ degrees high.

## Example

Encode $\varphi = 57.64911$, $\lambda = 10.40744$, a point in Denmark, to $p = 2$ characters.

| bit | axis | interval before | mid | bit value | kept half |
|---|---|---|---|---|---|
| 1 | lon | [−180, 180] | 0 | 1 | [0, 180] |
| 2 | lat | [−90, 90] | 0 | 1 | [0, 90] |
| 3 | lon | [0, 180] | 90 | 0 | [0, 90] |
| 4 | lat | [0, 90] | 45 | 1 | [45, 90] |
| 5 | lon | [0, 90] | 45 | 0 | [0, 45] |
| 6 | lat | [45, 90] | 67.5 | 0 | [45, 67.5] |
| 7 | lon | [0, 45] | 22.5 | 0 | [0, 22.5] |
| 8 | lat | [45, 67.5] | 56.25 | 1 | [56.25, 67.5] |
| 9 | lon | [0, 22.5] | 11.25 | 0 | [0, 11.25] |
| 10 | lat | [56.25, 67.5] | 61.875 | 0 | [56.25, 61.875] |

The first five bits are $11010_2 = 26$, which is `u`, and the next five are $00100_2 = 4$, which is `4`. So the geohash is `u4`, and its cell is $[56.25, 61.875] \times [0, 11.25]$ in latitude and longitude. With 11 characters the same point is `u4pruydqqvj`, and `u4` is its prefix.

**Cell sizes.** The height and width of a cell in degrees, and the same lengths in kilometers at the equator, with 111.32 km for one degree:

| $p$ | height (degrees) | width (degrees) | height at equator | width at equator |
|---|---|---|---|---|
| 1 | 45 | 45 | 5009 km | 5009 km |
| 2 | 5.625 | 11.25 | 626 km | 1252 km |
| 4 | 0.1758 | 0.3516 | 19.6 km | 39.1 km |
| 5 | 0.04395 | 0.04395 | 4.89 km | 4.89 km |
| 6 | 0.005493 | 0.01099 | 611 m | 1223 m |
| 7 | 0.001373 | 0.001373 | 153 m | 153 m |
| 8 | 0.0001717 | 0.0003433 | 19.1 m | 38.2 m |

Away from the equator a degree of longitude is shorter, by the factor $\cos \varphi$, so the cells are narrower in kilometers.

**A boundary.** The points $(0.0001, 10)$ and $(-0.0001, 10)$ are about 22 m apart, on the two sides of the equator. Their 6-character geohashes are `s0p058` and `kpzpgx`, with no common prefix, because the second bit, the first latitude bit, already differs.

## Correctness

Let $b_1 b_2 \ldots$ be the bits that the loop produces. The key [loop invariant](/loop-invariant/), at the test of line L3 after $t$ bits, is: the two intervals are the cell of the prefix $b_1 \ldots b_t$, that is, the longitude interval is $[-180 + 360 x / 2^{a}, -180 + 360(x+1)/2^{a}]$ where $a = \lceil t/2 \rceil$ and $x$ is the number with the bits $b_1, b_3, \ldots$, and the same holds for the latitude with $\lfloor t/2 \rfloor$ bits; and the point lies in both intervals. So each bit is the leading bit of the position of the coordinate in its range, the string is the interleaving of the problem statement, a shorter output is a prefix of a longer one, and the point lies in the cell of each prefix. The full proof is in the proofs folder.

## Complexity

Each pass of the loop of line L3 does a constant number of arithmetic operations and comparisons, on the [real RAM](/real-ram/), and produces one bit. The loop runs $5p$ times, so the time is $\Theta(p)$ in every case. Apart from the output, it keeps a constant number of numbers, so the extra space is $\Theta(1)$. Decoding also takes $\Theta(p)$ time.

On real hardware, each midpoint is $-180 + 360 x / 2^{a}$ or $-90 + 180 y / 2^{b}$, and $360 = 45 \cdot 2^3$ and $180 = 45 \cdot 2^2$, so a midpoint at depth $a$ is an integer of at most $\lg 45 + a + 1$ bits divided by a power of two. A double has a 53-bit significand, so double-precision arithmetic computes each midpoint exactly while $a \le 46$, that is, for $p \le 18$. For these lengths the floating-point encoder makes no rounding error; longer strings are below the precision of the input anyway.

## Properties

- **Hierarchical.** The geohash of length $q$ is a prefix of the geohash of length $p > q$ of the same point, and the cell of a string is the union of the 32 cells of its one-character extensions.
- **Order.** Sorting geohashes of one length as strings sorts the cells in Z-order, since the alphabet is in increasing order of value. So a [B-tree](/b-tree/) or any sorted key-value store can index points by geohash, and all points in a cell are one range scan on the prefix.
- **Not distance-preserving.** A common prefix implies the same cell, but close points may share no prefix, as in the boundary example. The Z-order also jumps: consecutive cells in the order may be far apart.
- **Not equal-area.** Cells of one length span equal angles, so their area on the sphere shrinks toward the poles by the factor $\cos \varphi$.

## Variants and improvements

- **Neighbor search.** To find the points within a radius $r$, choose the longest length whose cell is at least $r$ on each side, take the cell of the query point and its 8 neighbors, and scan the 9 prefixes. The neighbors are found by adding or subtracting 1 to the longitude or the latitude cell index, with wrap-around at $\pm 180$. This fixes the boundary problem.
- **Integer geohash.** Store the $5p$ bits as an integer instead of a string; this is the [Morton encoding](/morton-encoding/) of the two cell indices, which can use bit tricks instead of a loop.
- **Other curves.** A [Hilbert curve](/hilbert-curve/) order on the same grid has no long jumps between consecutive cells, so ranges of the order are more compact. The [S2 cell hierarchy](/s2-cell-hierarchy/) uses a Hilbert curve on the six faces of a cube projected onto the sphere.
- **Equal-area grids.** A [discrete global grid system](/discrete-global-grid-system/), such as H3 with hexagons, gives cells of about the same area everywhere.

## When to use it

Use geohash to give points a short, readable key that a sorted store, a cache or a URL can hold, and when a prefix test for "same cell" is enough. It needs no spatial index in the database, only a string column with a normal index. For exact radius queries, combine it with the 9-cell neighbor search and a distance check. For areas near the poles, for equal-area statistics, or for smooth neighborhoods, use S2 or H3.

## Pitfalls

- **The wrong axis first.** The first bit belongs to the longitude. An encoder that starts with the latitude (line L4 and line L5 swapped) gives strings that no other geohash tool reads correctly. The test of the example `u4pruydqqvj` catches this.
- **The wrong alphabet.** The alphabet has no a, i, l or o. Using the standard base-32 alphabet of RFC 4648 gives different strings.
- **Distance from prefixes.** Treating the length of the common prefix as a distance is wrong near cell edges: `s0p058` and `kpzpgx` are 22 m apart. Search the neighbors instead.
- **The midpoint rule.** A value exactly at a midpoint must go to one fixed side. With $\ge$ in lines L4 and L5, the point $(0, 0)$ is `s`, the cell north and east of it. An encoder that uses $>$ puts it in `7`, the cell south and west.
- **Width in kilometers.** The table gives sizes at the equator. At latitude 60 the cells are half as wide in kilometers, so a fixed length gives a different search radius in different places.

## Implementations

## History

G. M. Morton described the interleaving of the bits of two coordinates to order a geodetic file in an IBM report in 1966; the order is now called the Morton order or Z-order. Gustavo Niemeyer published geohash, with the base-32 alphabet and the public web service geohash.org, in 2008. The format then spread to databases and search engines as a simple geographic key.

## References
