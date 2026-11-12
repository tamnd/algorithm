---
tag: WEYDGJ
kind: algorithm
slug: hybrid-hash-join
name: Hybrid hash join
area: systems/database-algorithms
level: advanced
summary: "Keeps the first partition of the smaller relation in memory as a hash table while it partitions the rest, so that part of both inputs is joined at once and never written to disk."
solves: [relational-join]
model: external-memory-model
complexity:
  vars: {M: the number of pages of the smaller relation R, N: the number of pages of S, B: the number of buffer pages, f: the fudge factor of the hash table, p: the number of tuples per page of R, q: the number of tuples per page of S, T: the number of output tuples, W: the number of pages written to disk partitions}
  time: {worst: Θ(p q M N), average: O(p M + q N + T), best: O(p M + q N + T)}
  space: {extra: Θ(M + N)}
  io:
    worst: "O((M + N) log_B M + M N)"
    average: "M + N + 2W"
    best: "M + N"
properties: {deterministic: true, exact: true, external: true, online: false, in_place: false, recursive: true}
history:
  year: 1984
  people: [David J. DeWitt, Randy H. Katz, Frank Olken, Leonard D. Shapiro, Michael R. Stonebraker, David Wood]
  note: "Proposed for database systems with large main memories. It combines the partitioning of the GRACE join with the in-memory hash join, so that the memory left over during partitioning does useful work."
prereqs: [grace-hash-join]
see_also: [hash-join, sort-merge-join, block-nested-loop-join, bloom-join, hash-partitioning, data-skew, map-side-join]
sources:
  - paper: doi:10.1145/602259.602261
    title: David J. DeWitt, Randy H. Katz, Frank Olken, Leonard D. Shapiro, Michael R. Stonebraker and David Wood, Implementation techniques for main memory database systems, SIGMOD 1984, pages 1 to 8
    locator: the section on join algorithms (the hybrid hash join, its memory plan and its comparison with the simple and GRACE hash joins and with sort-merge)
  - paper: doi:10.1145/6314.6315
    title: Leonard D. Shapiro, Join processing in database systems with large main memories, ACM Transactions on Database Systems 11(3), 1986, pages 239 to 264
    locator: the section on the hybrid hash join (the partition kept in memory, the number of disk partitions, and the cost as a function of memory)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Section 14.4.3, Hash Join, the part on hybrid hash join (keeping the first partition in memory, and the example with B = 300 for Sailors and Reserves)
  - paper: doi:10.1145/152610.152611
    title: Goetz Graefe, Query evaluation techniques for large databases, ACM Computing Surveys 25(2), 1993, pages 73 to 169
    locator: the section on hash join algorithms (hybrid hashing and overflow resolution)
---

The hybrid hash join computes the equi-join of two relations when the smaller relation $R$ is somewhat larger than memory. Like the [Grace hash join](/grace-hash-join/), it splits both relations into partitions with a hash function $h_1$. The difference is that it keeps the first partition $R_0$ of $R$ in memory as a [hash table](/hash-table/) while it partitions the rest. When it then reads $S$, each tuple of the matching part $S_0$ is joined at once and is never written. Only the other partitions go to disk and are joined later. The cost is $M + N + 2W$ page I/Os, where $W$ is the number of pages written to disk. This is $M + N$ when $R$ fits in memory and close to $3(M + N)$ when memory is small. DeWitt, Katz, Olken, Shapiro, Stonebraker and Wood proposed it in 1984.

## In plain words

You must match a pile of customer cards with a pile of order slips, and the cards almost fit on your desk. As in the Grace method, you sort the cards into boxes by the last digit of the customer number. But the cards for digit 0 do not go into a box: you file them on your desk.

Then you go through the slips. A slip for digit 0 is matched at once with the cards on your desk. A slip for another digit goes into its box, to be matched later. The more of your desk you use for digit 0, the fewer cards and slips you must put in boxes and take out again.

## The problem

The input is two relations $R$ and $S$ on disk and the condition $r.a = s.b$. The output is the multiset $R \bowtie S$, as on the page [relational join problem](/relational-join/). Like every hash join, the method needs an equality condition.

**Cost model.** The conventions are those of Ramakrishnan and Gehrke, Section 14.4. $R$ is the smaller relation, with $M$ pages and $p_R$ tuples per page; $S$ has $N$ pages and $p_S$ tuples per page; memory holds $B \ge 4$ pages. A hash table on $x$ pages of tuples needs $f \cdot x$ pages, for a fudge factor $f \ge 1$. The cost is the number of page reads and writes, without the writes of the output. The front matter writes $p$ for $p_R$ and $q$ for $p_S$, and $W$ for the number of pages written to disk partitions. The [external memory model](/external-memory-model/) counts the same transfers with other letters.

## The algorithm

The memory plan comes first. If $f M \le B - 2$, the table on $R$ fits, and the method is the in-memory [hash join](/hash-join/). If not, PLAN chooses the number $k \ge 1$ of disk partitions. One frame is for input, one for output, $k$ frames are output buffers for the partitions $R_1, \dots, R_k$, and one frame is for an *overflow* partition $R_{k+1}$. The remaining $c = B - k - 3$ frames hold the table on $R_0$. PLAN takes the smallest $k$ with $c + k(B - 2) \ge \lceil f M \rceil$, so that each disk partition will fit in memory later. It then divides the hash values into $c + k d$ *slots*, with $d = \lceil (\lceil f M \rceil - c)/k \rceil$: the first $c$ slots form $R_0$, the next $d$ slots form $R_1$, and so on.

```pseudo id=main
HYBRID-HASH-JOIN(R, S, a, b, B, f)          ▷ the join r.a = s.b, B ≥ 4
L1  out ← an empty list, and push (R, S, 0) on a stack      ▷ a pair of inputs and a level
L2  while the stack is not empty do
L3      pop (R′, S′, ℓ); (k, c, d) ← PLAN(|R′|, B, f)       ▷ k disk partitions, c frames for R0
L4      if k = 0 then build a table on R′, probe it with each tuple of S′, append the matches; continue
L5      for each tuple r of R′ do                            ▷ partition R
L6          j ← h1(r.a, ℓ) mod (c + k d)
L7          if j ≥ c then write r to partition R_i, with i = 1 + ⌊(j − c)/d⌋
L8          else if R0 still fits in c frames then insert r into the table H0, with h2
L9          else write r to the overflow partition R_{k+1}
L10     for each tuple s of S′ do                            ▷ partition S and probe H0
L11         j ← h1(s.b, ℓ) mod (c + k d)
L12         if j ≥ c then write s to partition S_i, with i = 1 + ⌊(j − c)/d⌋
L13         else append the matches of s in H0 to out, and if R_{k+1} is not empty, write s to S_{k+1}
L14     for each i from 1 to k + 1 with R_i and S_i both nonempty do
L15         if R_i does not fit and (all its tuples have one key or ℓ + 1 is the depth limit) then join R_i and S_i by block nested loops, else push (R_i, S_i, ℓ + 1)
L16 return out
```

Lines L5 to L9 partition $R$. A tuple of $R_0$ goes into the table $H_0$, which uses a second hash function $h_2$, as long as $H_0$ fits in its $c$ frames. Lines L10 to L13 partition $S$: a tuple of $S_0$ probes $H_0$ at once. This is the saving: the tuples of $R_0$ and $S_0$ are read once and never written.

The overflow partition handles a bad case. If more tuples hash to $R_0$ than its frames hold, line L9 writes the rest to $R_{k+1}$. These tuples have not been joined with $S_0$, so line L13 also writes every tuple of $S_0$ to $S_{k+1}$, and the pair is joined later. Lines L14 and L15 treat each disk pair as in the Grace join: a pair that fits is pushed and joined at the next level by line L4, a pair that does not fit is partitioned again with $h_1(\cdot, \ell + 1)$, and a pair with one key, which no hash function can split, is joined by [block nested loops](/block-nested-loop-join/).

## Example

Let $R$ have the keys $[0, 1, 6, 7, 2, 3, 4, 5, 8, 9, 10, 11]$ and $S$ have the keys $[0, 6, 1, 7, 2, 3, 8, 9, 4, 5, 10, 13]$, two tuples per page, so $M = N = 6$, with $B = 6$ and $f = 1$. Here $f M = 6 > B - 2 = 4$, so PLAN gives $k = 1$, $c = 6 - 1 - 3 = 2$ and $d = 6 - 2 = 4$: there are 6 slots, and $h_1(x, 0) = x$ for the example, so the slot of a key is $x \bmod 6$.

| phase | tuples | action | I/Os |
|---|---|---|---|
| L5 to L9 | keys 0, 1, 6, 7 (slots 0 and 1) | into $H_0$: 2 pages, which fits in $c = 2$ frames | read 6 |
| L5 to L9 | keys 2, 3, 4, 5, 8, 9, 10, 11 | to $R_1$: 4 pages | write 4 |
| L10 to L13 | keys 0, 6, 1, 7, 13 (slots 0 and 1) | probe $H_0$: 4 matches, key 13 has none | read 6 |
| L10 to L13 | keys 2, 3, 8, 9, 4, 5, 10 | to $S_1$: 4 pages, the last one half full | write 4 |
| L4 | $R_1$ and $S_1$ | $R_1$ has 4 pages, which fits: 7 matches | read 8 |

The output has $4 + 7 = 11$ tuples. The cost is $6 + 6 + 2 \cdot (4 + 4) = 28$ I/Os, against $3(M + N) = 36$ for a Grace hash join that writes only full pages.

**The textbook sizes.** For Sailors ($M = 500$) and Reserves ($N = 1000$) with $B = 300$, Ramakrishnan and Gehrke make two partitions of Sailors, keep one in memory and get 3000 I/Os, against 4500 for Grace. The memory plan of this page gives $k = 1$ and $c = 296$, so $R_0$ takes 296 slots of 500. With an even hash function, $R_1$ has 204 pages and $S_1$ has 408, and the cost is $1500 + 2 \cdot (204 + 408) = 2724$, which the tests check.

**A range of memory sizes.** The table gives the I/O count of the implementation, with the default hash function, for $M = 500$, $N = 1000$, two tuples per page and distinct keys, next to the Grace hash join on the same input.

| $B$ | $k$ | $c$ | hybrid | Grace |
|---|---|---|---|---|
| 25 | 22 | 0 | 5386 | 4524 |
| 50 | 10 | 37 | 4496 | 4548 |
| 100 | 5 | 92 | 4322 | 4598 |
| 200 | 2 | 195 | 4112 | 4708 |
| 300 | 1 | 296 | 2730 | 4703 |
| 400 | 1 | 396 | 3710 | 4828 |
| 502 | 0 | 500 | 1500 | 4859 |

The hybrid join wins when $B$ is large compared with $\sqrt{M}$, because then $c$ is a large share of $M$. At $B = 25$ it loses: the plan leaves no frames for $R_0$ ($c = 0$) and sizes each of its 22 partitions at the memory limit, so uneven partitions must be split again, while Grace has 24 partitions with room to spare. At $B = 100$, $200$ and $400$, more tuples hashed to $R_0$ than its frames hold (for $B = 400$, 404 pages for 396 frames), so all of $S_0$ was written as well. This is why the cost at $B = 400$ is above the cost at $B = 300$.

## Correctness

Each tuple of $R'$ goes to exactly one of $H_0$, $R_1, \dots, R_k$ and $R_{k+1}$, and each tuple of $S'$ goes to one $S_i$ with $i \le k$ or to the probe of line L13. Two matching tuples have the same slot. If the slot is at least $c$, they meet in one disk pair $(R_i, S_i)$. If it is below $c$, the tuple $r$ is in $H_0$ or in $R_{k+1}$. In the first case line L13 finds the pair. In the second case $R_{k+1}$ is not empty, so line L13 writes $s$ to $S_{k+1}$ and the pair is found when $(R_{k+1}, S_{k+1})$ is joined. No pair is found twice, because each tuple of $R'$ is in exactly one place. The full proof, with an invariant over the stack, is in [the proof page](proofs/correctness.md).

## Complexity

- **One level.** Lines L5 and L10 read $M + N$ pages. The disk partitions get $W$ pages in total, and line L4 reads each of them once at the next level, so the cost is $M + N + 2W$ when each disk pair fits and has two nonempty sides.
- **The share kept in memory.** With an even hash function and no overflow, $R_0$ and $S_0$ receive a share $\rho = c/(c + k d) \approx c/(f M)$ of the tuples of each relation, and $W \approx (1 - \rho)(M + N)$. So the cost is about $(3 - 2\rho)(M + N)$. It is $M + N$ for $\rho = 1$, the in-memory hash join, and $3(M + N)$ for $\rho = 0$, the Grace hash join.
- **When it beats Grace.** The share $\rho$ is large when $B$ is large compared with $\sqrt{f M}$, which is the condition for one level of partitioning. Close to that condition, $k$ is large and $c = B - k - 3$ is small, so the hybrid join is no better than Grace, and the table above shows it can be worse.
- **Recursion and skew.** As for Grace, each further level reads and writes its pairs once more, so the worst case without heavy duplicates is $O((M + N) \log_B M)$. A single heavy key forces block nested loops on its pair, and the output alone can then have $|R| \cdot |S|$ tuples.
- **Work in memory.** With good hash functions the expected work is $O(p_R M + p_S N + T)$ per level.

## Properties

- **Smooth in memory.** The cost moves from $3(M + N)$ toward $M + N$ as $B$ grows from about $\sqrt{f M}$ to $f M$, while Grace stays at $3(M + N)$ until $R$ fits.
- **Early output.** The matches of $S_0$ come out during the partitioning of $S$, before any partition is read back.
- **Memory on the smaller input.** Only the size of $R$ decides the plan.
- **Sensitive to the size estimate.** The plan depends on $M$, which an optimizer often knows only as an estimate.

## Variants and improvements

- **Grace hash join.** The [Grace hash join](/grace-hash-join/) is the case $c = 0$. It uses $B - 1$ partitions and costs $3(M + N)$.
- **In-memory hash join.** The [hash join](/hash-join/) is the case $k = 0$, at $M + N$.
- **Bit-vector filtering.** While partitioning $R$, set a bit for the hash value of each key. While partitioning $S$, drop each tuple whose bit is clear, so fewer tuples of $S$ are written. This is the filter of the [Bloom join](/bloom-join/).
- **Dynamic hybrid hashing.** Later systems choose which partitions stay in memory while the build input is read, and spill a partition to disk when memory runs out. This adapts to a bad size estimate and to [data skew](/data-skew/).
- **Role reversal.** At the next level, build on the smaller side of each pair.

## When to use it

Use it for an equi-join when the smaller input is larger than memory but not by much, for example up to a few times $B$. Then it costs much less than $3(M + N)$. When $R$ fits in memory, the plain [hash join](/hash-join/) is the same algorithm. When memory is close to $\sqrt{f M}$, the Grace hash join is as good and simpler. When sorted output is needed, or the keys are heavily skewed, a [sort-merge join](/sort-merge-join/) can be better.

## Pitfalls

- **No slack for $R_0$.** The plan of this page gives $R_0$ exactly the number of slots that its frames can hold. With a real hash function, $R_0$ gets more tuples about as often as fewer, and then line L9 spills tuples and line L13 writes all of $S_0$. A real system plans $R_0$ smaller than its frames, or uses the fudge factor for this margin.
- **Forgetting the overflow tuples of $S_0$.** If line L9 spills some tuples of $R_0$, line L13 must write $S_0$ to disk as well. Probing only $H_0$ loses the matches with the spilled tuples.
- **Too many partitions.** Each disk partition takes an output frame from the table on $R_0$. A plan with more partitions than needed makes $c$ small and the cost close to Grace.
- **The same hash function at every level.** As in Grace, the next level must use a new function $h_1(\cdot, \ell + 1)$ and the table must use $h_2$.

## Implementations

## History

DeWitt, Katz, Olken, Shapiro, Stonebraker and Wood (1984) proposed the hybrid hash join in a study of database systems with large main memories. It combines the partitioning of the GRACE join of Kitsuregawa, Tanaka and Moto-Oka (1983) with the in-memory hash join, and they found it the best of the joins they compared over a wide range of memory sizes. Shapiro (1986) gave a detailed analysis of its cost as a function of memory. Graefe's survey (1993) describes overflow resolution and the dynamic variants. Ramakrishnan and Gehrke, Section 14.4.3, present it as an improvement of the Grace hash join when memory is large.

## References
