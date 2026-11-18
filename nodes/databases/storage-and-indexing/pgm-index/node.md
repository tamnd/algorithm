---
tag: YYKWMY
kind: data-structure
slug: pgm-index
name: PGM-index
aliases:
- piecewise geometric model index
area: databases/storage-and-indexing
level: research
summary: "A learned index of recursive piecewise linear models with a guaranteed error bound, built optimally in one pass over the sorted keys."
model: word-ram
complexity:
  vars: {n: the number of keys, m: the number of segments on the bottom level, ε: the error bound of the bottom level, ε': the error bound of the upper levels (a constant)}
  time: {worst: "O(log m + log ε)", average: "O(log m + log ε)", best: "O(log ε)"}
  space: {extra: "Θ(m)"}
properties: {deterministic: true, exact: true, external: false, online: false, in_place: false, recursive: true}
history:
  year: 2020
  people: [Paolo Ferragina, Giorgio Vinciguerra]
  note: "Ferragina and Vinciguerra published the PGM-index in PVLDB in 2020. It replaced the trained models of the first learned indexes by an optimal piecewise linear approximation with a proved error bound, used at every level."
prereqs: [learned-index, binary-search]
see_also: [alex-learned-index, b-plus-tree, interpolation-search, elias-fano-encoding, helly-theorem, convex-hull, log-structured-merge-tree, fusion-tree]
sources:
  - paper: doi:10.14778/3389133.3389135
    title: "Paolo Ferragina and Giorgio Vinciguerra, The PGM-index: a fully-dynamic compressed learned index with provable worst-case bounds, PVLDB 13(8) (2020)"
    locator: pp. 1162 to 1175, the optimal piecewise linear ε-approximation and its construction (Lemma 1), the bound on the number of segments (Lemma 2), the recursive index and its query bound (Theorem 1), the dynamic version (Theorem 2), the compressed and distribution-aware versions, and the experiments
  - paper: doi:10.1145/3183713.3196909
    title: "Tim Kraska, Alex Beutel, Ed H. Chi, Jeffrey Dean and Neoklis Polyzotis, The case for learned index structures, SIGMOD 2018"
    locator: pp. 489 to 504, the index as a model of the cumulative distribution and the recursive model index, which the PGM-index compares with
---

The PGM-index (piecewise geometric model index) is a [learned index](/learned-index/) for a sorted array of keys. It replaces the nodes of a [B+ tree](/b-plus-tree/) by line segments: each segment takes a key and predicts its position in the array, and every prediction is within a fixed error $\varepsilon$ of the true position. The segments are the fewest that meet the error bound, and they are found in one pass over the keys. The first keys of the segments are indexed in the same way, level by level, until one segment remains. A lookup follows one segment per level and finishes with a [binary search](/binary-search/) over at most $2\varepsilon + 1$ positions.

## In plain words

Plot the sorted keys on a graph: the key across, its position in the array up. The points climb from left to right. Over a short stretch they lie almost on a straight line, so a line can stand in for all of them: give it a key, and it says roughly where the key is.

The PGM-index draws as few lines as it can, under one rule: no point may be more than $\varepsilon$ places away from its line. To find a key, pick the right line, read off a guess, and look only at the $2\varepsilon + 1$ places around the guess. To pick the right line, the index uses the same trick again on the first keys of the lines, so it is a short tree of lines.

## The abstract type

A static set of $n$ distinct keys, stored sorted in an array $K[0..n-1]$.

- `rank(x)`: the number of keys $\le x$. This gives predecessor search, membership and range queries.
- `lower_bound(x)`: the position of the first key $\ge x$.
- `contains(x)` and `range(lo, hi)`: membership, and the keys in $[lo, hi]$.

The keys stay in the array. The index is the extra data that finds a position, as with a sparse index over a sorted file.

## Representation

A *segment* is a triple (key, slope, intercept) and the run of positions $a..b$ that it covers. It predicts $f(x) = intercept + slope \cdot (x - key)$. A piecewise linear $\varepsilon$-approximation (PLA) of an array $A$ is a list of segments that cover the positions $0..N-1$ in runs, with $|f(A[i]) - i| \le \varepsilon$ for every covered $i$.

The index has levels. The bottom level is a PLA of $K$ with the error $\varepsilon$. The next level is a PLA, with the error $\varepsilon'$, of the array of the first keys of the bottom segments, and so on until a level has one segment, the root.

## Operations

The PLA is built greedily: a segment starts at a point and grows while some line is still within $e$ of all of its points. The set of such lines is a convex polygon in the plane of (slope, intercept). Each new point $(x_j, j)$ cuts the polygon with the two half-planes $j - e \le c + s(x_j - x_i) \le j + e$. When the polygon becomes empty, the segment ends before that point.

```pseudo id=main
BUILD-PLA(A[0..N-1], e)
L1  i ← 0
L2  while i < N do
L3      P ← the lines within e of the points (A[i], i) and (A[i+1], i+1)
L4      j ← i + 2
L5      while j < N and P cut by the strip of the point (A[j], j) is not empty do
L6          P ← that cut; j ← j + 1
L7      output a segment with key A[i], a line from P and the positions i..j-1
L8      i ← j

BUILD-PGM(K, ε, ε')
L9  A ← K; e ← ε
L10 repeat S ← BUILD-PLA(A, e); store S as a level
L11     A ← the first keys of the segments of S; e ← ε'
L12 until S has one segment
```

A query predicts a position, clamps it to the run of the segment, and searches a window of $2e + 1$ entries around it. The result names the segment of the next level down.

```pseudo id=query
RANK(x)                                       ▷ the number of keys ≤ x
L13 if x < K[0] then return 0
L14 s ← the root segment
L15 for each level, from the root down do
L16     p ← ⌊f_s(x) clamped to [s.start, s.end]⌋
L17     r ← the number of entries ≤ x of the array of this level, by binary search in the positions max(s.start, p - e) to min(s.end + 1, p + e + 1)
L18     if this is the bottom level then return r
L19     s ← the segment of the next level whose first key is entry r - 1
```

The code uses exact fractions, so the test "is the polygon empty" has no rounding error. A segment with one point gets a flat line. If the chosen line has a negative slope, the code uses the flat line at the middle of the run, which is then valid (see the proof). The paper builds the PLA in $O(N)$ time by keeping the convex hulls of the upper and lower ends of the strips (its Lemma 1, after O'Rourke 1981). The polygon of this page is easier to check and gives the same segments in count, but each cut costs time in the size of the polygon.

## Example

Take the 12 keys

$$K = [2, 3, 5, 8, 12, 13, 14, 20, 30, 31, 40, 41]$$

with $\varepsilon = \varepsilon' = 1$.

1. **Bottom level.** The greedy segment from position 0 grows over the keys 2 to 20 (positions 0 to 7). At the key 30 (position 8) no line is within 1 of all nine points, so the segment ends. The code's line is $f(x) = 19/60 + (49/120)(x - 2)$. For example, $f(13) = 577/120 \approx 4.81$ against the position 5, and $f(20) = 920/120 \approx 7.67$ against 7. The second segment covers the keys 30 to 41 (positions 8 to 11).
2. **Root.** The first keys are $[2, 30]$, and one segment covers them, with $f(x) = (x - 2)/28$. The index has 2 levels and 3 segments.
3. **rank(13).** The root predicts $11/28 \approx 0.39$, so $p = 0$. The window is the positions 0 to 1 of $[2, 30]$, and the count of entries $\le 13$ is 1, so the next segment is the first bottom segment. It predicts 4.81, so $p = 4$, and the window is the positions 3 to 5, with the keys 8, 12 and 13. The count is 6: six keys are $\le 13$.
4. **lower_bound(25).** The root again picks the first bottom segment. It predicts $f(25) \approx 9.7$, which is past the run 0 to 7, so the clamp gives $p = 7$. The window is the positions 6 and 7, with the keys 14 and 20, and the count is 8. The key 25 is not present, and it would go at position 8.

**Sizes (measurement).** On 10,000 keys in clusters (seed 5 in the test file), the bottom level has 495 segments for $\varepsilon = 4$, 117 for $\varepsilon = 16$ and 16 for $\varepsilon = 64$. With $\varepsilon' = 4$ the index has 3, 2 and 2 levels. A uniform sample of 10,000 keys from a range of 100,010 values needs 121 segments for $\varepsilon = 4$ and a single segment for $\varepsilon = 64$.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).

- **Theorem (optimal PLA).** The greedy BUILD-PLA gives the fewest segments of any PLA with the error $e$. The proof is an exchange argument: if any valid segment covers a run, then any shorter run inside it also has one, so the greedy end of the $t$-th segment is never before the $t$-th end of an optimal PLA.
- **Theorem (segment length).** Every segment but the last covers at least $2e + 1$ positions, because the flat line at height $i + e$ is within $e$ of the positions $i$ to $i + 2e$. So $m \le \lceil n / (2\varepsilon + 1) \rceil$. The paper states this as at least $2\varepsilon$ keys per segment (its Lemma 2).
- **Theorem (search).** If $x$ lies between the first key of a segment and the first key of the next one, then its rank in the array of that level is within $e$ of the clamped prediction, with one more place on the right for keys between two array entries. So the window at L17 holds the answer, and induction on the levels shows that RANK returns the number of keys $\le x$.

## Complexity

- **Query (theorem).** Each level costs one prediction and a binary search over at most $2e + 1$ entries. With $\varepsilon'$ a constant, every upper level has at most $1/(2\varepsilon' + 1)$ of the entries of the level below, so there are $O(\log m)$ levels, and a query takes $O(\log m + \log \varepsilon)$ time. This is the bound of Theorem 1 of the paper.
- **Space (theorem).** $m$ segments on the bottom level, and $O(m / \varepsilon')$ on all the levels above it together, because each level is at most $1/(2\varepsilon' + 1)$ of the one below. Each segment is a key and two numbers. The keys themselves are not counted.
- **Build.** The paper's convex-hull method builds each level in time linear in its size. The polygon method of the code takes time in the size of the polygon per point.
- **Trade-off.** A larger $\varepsilon$ gives fewer segments and a longer final search. The measurement in the Example shows how fast $m$ falls with $\varepsilon$ on clustered data.

In the word RAM model each operation on a key or a fraction costs $O(1)$; the code uses exact fractions only to make the tests exact.

## Variants

- **Dynamic PGM-index.** The paper supports inserts and deletes by the logarithmic method: a set of static PGM-indexes of sizes that grow by powers of two, merged and rebuilt when one fills (its Theorem 2). Inserts can also go to a buffer.
- **Compressed PGM-index.** The paper compresses the intercepts and the slopes of the segments, which reduces the space further at the same error.
- **Distribution-aware PGM-index.** If the frequency of queries is known, the error bound can be smaller for keys that are queried often.
- **Choosing ε from a budget.** The paper also gives a version that picks $\varepsilon$ to meet a space bound or a time bound.
- **Other learned indexes.** The recursive model index of Kraska et al. (2018) trains a fixed number of models and stores their measured errors, with no bound before training. [ALEX](/alex-learned-index/) adds gaps to its arrays to support inserts.

## When to use it

Use a PGM-index for a large sorted array that is read much more often than it changes, such as a column of a read-only table or a sorted run of an [LSM tree](/log-structured-merge-tree/), when the space of the index matters. For a workload with many updates, or for variable-length keys such as strings, a B+ tree is the simpler choice. The paper reports, as a measurement, that the PGM-index used 63.3% less space than the FITing-tree, another index of linear segments.

## Pitfalls

- **Rounding in the build.** With floating-point numbers, the test "is the polygon empty" can be wrong for large keys, and a segment can break the error bound. Store the slopes with enough precision, or check the bound after the build.
- **Keys between segments.** A key that is not in the array can be past the last key of its segment, and the line can then predict a position far outside the run. Clamp the prediction to the run before the window search.
- **Duplicate keys.** The proofs assume distinct keys. With duplicates, index the distinct keys or the first position of each key.
- **Error bound for one level only.** The upper levels need their own error $\varepsilon'$. A large $\varepsilon'$ saves little space, because the upper levels are already small, and it makes each step longer.
- **Static by design.** One insert can change the optimal segments of a whole level. Use the dynamic version, or a buffer, for updates.

## Implementations

## History

Tim Kraska, Alex Beutel, Ed Chi, Jeffrey Dean and Neoklis Polyzotis proposed learned indexes at SIGMOD 2018, with models that are trained and whose errors are measured after the training. Paolo Ferragina and Giorgio Vinciguerra presented the PGM-index in PVLDB in 2020. They used an optimal piecewise linear approximation with a fixed error, a construction known from the approximation of time series, at every level of the index. This gave a learned index with worst-case bounds on time and space, and with dynamic and compressed versions.

## References
