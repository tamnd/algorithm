---
tag: JWEWY8
kind: technique
slug: memory-partitioning-for-hls
name: Memory partitioning for high-level synthesis
aliases:
- array partitioning
- cyclic and block memory partitioning
area: eda/high-level-synthesis-and-scheduling
level: research
summary: Splits an array over several memory banks by a cyclic, block or linear mapping so that the accesses of one pipelined loop iteration hit different banks.
prereqs: [loop-unrolling, iterative-modulo-scheduling]
see_also: [polyhedral-model, sdc-modulo-scheduling, resource-binding, loop-tiling, gcd-test, chinese-remainder-theorem, interface-synthesis, pigeonhole-principle]
sources:
  - paper: doi:10.1145/1929943.1929947
    title: Jason Cong, Wei Jiang, Bin Liu and Yi Zou, Automatic memory partitioning and scheduling for throughput and power optimization, ACM Transactions on Design Automation of Electronic Systems 16(2), 2011
    locator: whole paper (cyclic partitioning of arrays for loop pipelining, with the accesses scheduled over the initiation interval; first presented at ICCAD 2009)
  - paper: "Yuxin Wang, Peng Li and Jason Cong, Theory and algorithm for generalized memory partitioning in high-level synthesis, Proceedings of the ACM/SIGDA International Symposium on Field-Programmable Gate Arrays, 2014"
    locator: whole paper (linear bank functions for multidimensional arrays and the search for the fewest banks)
---

Memory partitioning splits one array of a [high-level synthesis](/high-level-synthesis/) design over several memory banks, each a separate on-chip RAM with its own ports. A loop that is pipelined to start one iteration per cycle, or unrolled by [loop unrolling](/loop-unrolling/), may read several elements of the array in the same cycle, but one RAM has only one or two ports. The partition picks a bank function, which sends element $x$ to bank $B(x)$, and an offset function, which gives its address inside the bank, so that the accesses of one iteration fall in different banks. The two classic choices are *block* partitioning, which cuts the array into contiguous pieces, and *cyclic* partitioning, which deals the elements out to the banks in turn, $B(x) = x \bmod N$. For accesses $A[i + c_1], \ldots, A[i + c_m]$, the cyclic partition is free of conflicts in every iteration exactly when no more than $p$ offsets $c_k$ share a remainder modulo $N$, for banks with $p$ ports.

## In plain words

An on-chip memory can hand out only one or two numbers per clock tick. A fast loop may want three numbers from the same list in every tick. If the whole list sits in one memory, the loop has to wait. So we cut the list into several smaller memories that work side by side. The trick is to cut so that the numbers one tick wants always come from different memories. Cutting the list into long pieces works badly when the loop reads neighbours, since neighbours sit in the same piece. Dealing the list out like cards, one item to each memory in turn, puts neighbours in different memories, and the loop never waits.

## When it applies

- The array lives on chip, in block RAMs or SRAM macros with one or two ports each.
- A loop is pipelined with a target initiation interval, often 1, or unrolled, and its schedule needs more accesses to the array per cycle than the ports allow. The [modulo scheduler](/iterative-modulo-scheduling/) then reports a resource bound on the initiation interval set by the memory ports.
- The indices are affine functions of the loop variables, such as $i + 1$ or $2i + j$, so the bank of each access can be computed at compile time or by a small adder and a modulo. Such indices are what the [polyhedral model](/polyhedral-model/) describes.

## The template

Take a one-dimensional array $A$ of size $S$, banks with $p$ ports each, and a loop body with the references $A[i + c_1], \ldots, A[i + c_m]$ in one iteration, with integer offsets $c_k$, after unrolling.

```pseudo id=main
CYCLIC-PARTITION(S, p, c_1, ..., c_m)
L1  N ← ⌈m / p⌉
L2  while some remainder ρ modulo N has more than p of the offsets c_k with c_k ≡ ρ (mod N) do N ← N + 1
L3  for each element x: B(x) ← x mod N and F(x) ← ⌊x / N⌋
L4  make N memories of ⌈S / N⌉ words each, and store A[x] at address F(x) of bank B(x)
L5  replace each reference A[i + c_k] by bank (i + c_k) mod N at address ⌊(i + c_k) / N⌋
L6  build a multiplexer from the N banks to each of the m references, selected by (i + c_k) mod N
L7  return N, B, F
```

The holes are the bank function of L3 (cyclic, block, block-cyclic or linear), the number of ports $p$, and the routing of L6, which grows with $N \cdot m$.

**Why the test of L2 is exact.** In iteration $i$, reference $k$ goes to bank $(i + c_k) \bmod N$. Two references $k$ and $l$ go to the same bank exactly when $N$ divides $(i + c_k) - (i + c_l) = c_k - c_l$, which does not depend on $i$. So the references that hit one bank in iteration $i$ are exactly those whose offsets share one remainder modulo $N$, and they fit in one cycle exactly when there are at most $p$ of them. The same sets appear in every iteration, so the check over the remainders covers all iterations at once.

**Why L2 stops.** Once $N > \max_k c_k - \min_k c_k$, all the differences $c_k - c_l$ with $c_k \ne c_l$ lie strictly between $-N$ and $N$ and are not multiples of $N$, so distinct offsets have distinct remainders. Equal offsets read the same element, and a compiler merges them into one access. So the loop ends with $N \le \max_k c_k - \min_k c_k + 1$. It never ends below $\lceil m / p \rceil$, since $m$ accesses need at least that many banks of $p$ ports. Both bounds can be tight: offsets $0, 1, \ldots, m - 1$ with $p = 1$ need exactly $m$ banks.

**Block partitioning.** Here $B(x) = \lfloor x / \lceil S / N \rceil \rfloor$ and $F(x) = x \bmod \lceil S / N \rceil$. Neighbouring elements share a bank, so it suits loops whose parallel accesses are far apart, such as two halves of an array processed at once.

## Classic examples

**Least banks for common access patterns.** For the cyclic partition, the least $N$ found by L1 and L2:

| offsets $c_k$ | one port | two ports |
|---|---|---|
| $0, 1, 2$ | 3 | 2 |
| $-1, 0, 1$ | 3 | 2 |
| $0, 1, 3$ | 4 | 2 |
| $0, 2, 4$ | 3 | 3 |
| $0, 4$ | 3 | 1 |
| $0, 1, 2, 3$ | 4 | 2 |
| $0, 1, 4, 5$ | 6 | 2 |

For $0, 2, 4$ with two ports, $N = 2$ puts all three offsets in bank 0, so $N = 3$ is the least, above the bound $\lceil 3/2 \rceil = 2$. For $0, 1, 4, 5$ with one port, $N = 4$ and $N = 5$ both put two offsets together ($0 \equiv 4$ and $0 \equiv 5$), so 6 banks are needed.

**Block against cyclic.** A 12-element array is read by the loop $i = 0, \ldots, 9$ with the references $A[i], A[i + 1], A[i + 2]$, and each bank has one port. With 3 blocks of 4 elements, iteration 0 reads elements 0, 1 and 2, all in bank 0, so it takes 3 cycles. Over the 10 iterations, the block partition takes $3 + 3 + 2 + 2 + 3 + 3 + 2 + 2 + 3 + 3 = 26$ cycles. The cyclic partition into 3 banks reads the three elements from three different banks in every iteration, and takes 10 cycles, one per iteration.

**A two-dimensional stencil.** A 5-point stencil reads $A[i][j]$, $A[i \pm 1][j]$ and $A[i][j \pm 1]$. Cyclic partitioning along one dimension leaves two of the five references in the same bank for any number of banks, since $A[i][j - 1]$, $A[i][j]$ and $A[i][j + 1]$ differ in $j$ only and the two references $A[i \pm 1][j]$ have the same $j$ as $A[i][j]$. The linear bank function $B(x, y) = (x + 2y) \bmod 5$ maps the five offsets $(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)$ to $0, 1, 4, 2, 3$, all different, so 5 single-port banks suffice, and fewer is impossible with 5 accesses. Wang, Li and Cong (2014) search such linear functions for general patterns.

## Variations

- **Block-cyclic.** Deal out blocks of $k$ elements in turn, $B(x) = \lfloor x / k \rfloor \bmod N$. It covers loops that read groups of $k$ neighbours.
- **Linear partitioning for several dimensions.** Use $B(\mathbf{x}) = (\boldsymbol\alpha \cdot \mathbf{x}) \bmod N$ with an integer vector $\boldsymbol\alpha$. The test of L2 becomes a test on the values $\boldsymbol\alpha \cdot \mathbf{c}_k$ modulo $N$.
- **Scheduling with the partition.** Cong, Jiang, Liu and Zou (2009, 2011) let the accesses of one iteration spread over the $II$ cycles of the initiation interval, so a bank may serve $p \cdot II$ of them, and choose the schedule and the partition together.
- **Padding.** When the offset function needs a division by an awkward $N$, pad each row or round $N$ up to a power of two, so that $B$ and $F$ are bit fields. This costs memory and may raise $N$.
- **Duplication.** A read-only array can be copied into several memories, one per reference, at the cost of memory and of keeping the copies equal when written.
- **Reshaping.** Packing several elements into one wide word lets one port read them all, which helps when the accesses are neighbours.

## Pitfalls

- **Non-affine or data-dependent indices.** For $A[f(i)]$ with an unknown $f$, no static bank function avoids conflicts, and the tool must keep a conservative schedule or add arbitration.
- **The routing cost.** Each of the $m$ references needs a multiplexer over the $N$ banks, so a large $N$ adds wide multiplexers that may lengthen the clock period, see [resource binding](/resource-binding/) for the same trade-off with units.
- **Division and modulo hardware.** With a general $N$, the address $\lfloor (i + c_k) / N \rfloor$ needs a divider unless it is computed by counters that step with $i$.
- **Size not divisible by $N$.** The last bank is shorter, or every bank gets $\lceil S / N \rceil$ words and some stay unused.
- **Accesses across loops.** A partition chosen for one loop may cause conflicts in another loop that reads the same array in a different pattern.

## Exercises

1. Find the least number of single-port banks for the cyclic partition of the offsets $0, 3, 6, 9$, and explain why $N = 3$ fails.
2. Prove that for offsets $0, 1, \ldots, m - 1$ and banks with $p$ ports, the least cyclic $N$ is $\lceil m / p \rceil$.
3. For the 5-point stencil, find every $\beta \in \{0, 1, 2, 3, 4\}$ for which $B(x, y) = (x + \beta y) \bmod 5$ sends the five offsets to five different banks.
4. A loop reads $A[2i]$ and $A[2i + 1]$ in each iteration. Compare the block partition into 2 banks with the cyclic one, and say which needs a wider multiplexer.

## References
