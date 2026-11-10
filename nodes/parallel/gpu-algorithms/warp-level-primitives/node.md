---
tag: Z0YTVG
kind: concept
slug: warp-level-primitives
name: Warp-level primitives
aliases:
- warp shuffle
- warp vote
area: parallel/gpu-algorithms
level: core
summary: Instructions that let the lanes of a warp read each other's registers (shuffle), vote on a predicate, match equal values or reduce, so a warp sum or scan takes 5 steps without shared memory.
prereqs: [simt-model, warp-divergence]
see_also: [parallel-reduce, hillis-steele-scan, all-prefix-sums, compaction, warp-aggregated-atomics, cooperative-groups, decoupled-look-back-scan, parallel-histogram]
sources:
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 5.4.6 (warp functions), 5.4.6.1 (__activemask), 5.4.6.2 (vote), 5.4.6.3 (match), 5.4.6.4 (reduce, compute capability 8.x and later), 5.4.6.5 (shuffle, width, the rules for up, down and xor), 5.4.6.6 (mask constraints), Section 5.4.4.2 (__syncwarp) and Section 3.2.2.1.1 (independent thread scheduling)
  - url: https://developer.nvidia.com/blog/using-cuda-warp-level-primitives/
    title: Yuan Lin and Vinod Grover, Using CUDA warp-level primitives, NVIDIA Developer Blog, January 15, 2018
    locator: the reduction with __shfl_down_sync and offsets 16 to 1, and the section on implicit warp-synchronous programming being unsafe
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition
    locator: Chapter 10 (reduction) and Chapter 11 (prefix sum)
---

**Warp-level primitives** are instructions that work across the 32 lanes of one [warp](/simt-model/): a **shuffle** lets each lane read a register of another lane, a **vote** combines one predicate from each lane into a bit mask or a single answer, a **match** finds the lanes with equal values, and a **reduce** sums or combines one integer from each lane. They need no shared memory and no block barrier, and one primitive is one warp instruction. With shuffles, a sum or a scan over a warp takes $\log_2 32 = 5$ steps. Each primitive takes a member mask that names the lanes that take part (CUDA Programming Guide v13.5, Section 5.4.6).

## In plain words

Thirty-two workers sit in a row. Each has a small notepad that only they can write on. Normally, to pass a number to a neighbour, a worker must write it on a shared board and wait until everyone has done the same. Warp-level primitives give the row a faster way. At one signal, every worker can read the notepad of a chosen other worker, for example the one sixteen seats to the right. At another signal, all workers raise a hand or not, and everyone sees which hands are up. To add up all the numbers, each worker adds the number of the worker sixteen seats away, then eight, then four, then two, then one. After five signals, the first worker holds the total.

## The idea

### The primitives

All have the form `__name_sync(mask, ...)`. The 32-bit `mask` lists the lanes that take part; every lane in it must call the same primitive with the same mask, and a lane may read only from lanes in the mask (Section 5.4.6.6). From compute capability 7.0 the lanes of a warp are not in lockstep (Section 3.2.2.1.1), so the mask is what makes the exchange safe.

| Primitive | Result in lane $\ell$ |
|---|---|
| `__shfl_sync(m, v, src, w)` | $v$ of lane $\text{base} + (\text{src} \bmod w)$, where $\text{base} = \ell - (\ell \bmod w)$ |
| `__shfl_up_sync(m, v, d, w)` | $v$ of lane $\ell - d$, or its own $v$ if $(\ell \bmod w) < d$ |
| `__shfl_down_sync(m, v, d, w)` | $v$ of lane $\ell + d$, or its own $v$ if $(\ell \bmod w) + d \ge w$ |
| `__shfl_xor_sync(m, v, x, w)` | $v$ of lane $\ell \oplus x$; its own $v$ if that lane is in a later segment |
| `__ballot_sync(m, p)` | the mask of lanes in $m$ whose $p$ is true |
| `__any_sync(m, p)`, `__all_sync(m, p)` | whether some or all lanes in $m$ have $p$ true |
| `__match_any_sync(m, v)` | the mask of lanes in $m$ whose $v$ equals this lane's $v$ |
| `__match_all_sync(m, v, &pred)` | $m$ and `pred = true` if all lanes in $m$ hold the same $v$, else 0 and false |
| `__reduce_add_sync(m, v)` (also min, max, and, or, xor) | the combination over the lanes in $m$, integers only |
| `__activemask()` | the mask of lanes that are active now |
| `__syncwarp(m)` | a barrier and memory fence for the lanes in $m$ |

The width $w$ is a power of 2 up to 32 and splits the warp into segments of $w$ lanes (Section 5.4.6.5). The reduce functions need compute capability 8.x or later and work on integer types (Section 5.4.6.4). The match functions came with compute capability 7.0. AMD GPUs offer similar cross-lane operations on a wavefront of 64 or 32 lanes; code that assumes 32 lanes must be adapted there.

### Warp reduction in 5 steps

```cpp
__device__ int warpReduceSum(int v) {
    for (int offset = 16; offset > 0; offset /= 2)
        v += __shfl_down_sync(0xffffffff, v, offset);
    return v;                                  // the sum is in lane 0
}
```

*Correctness.* Write $x_j$ for the input of lane $j$ and $v_\ell$ for the value of lane $\ell$. Claim: after the step with offset $o$, every lane $\ell < o$ holds $\sum_{j < 32, \ j \equiv \ell \ (\mathrm{mod}\ o)} x_j$. Before the first step, take $o = 32$: lane $\ell$ holds $x_\ell$. Assume the claim for $2o$. In the step with offset $o$, lane $\ell < o$ adds $v_{\ell + o}$, and $\ell + o < 2o$, so by the claim for $2o$ it adds the sum over $j \equiv \ell + o \pmod{2o}$ to its own sum over $j \equiv \ell \pmod{2o}$; the two classes together are $j \equiv \ell \pmod{o}$. After the step with $o = 1$, lane 0 holds $\sum_j x_j$. The lanes $\ell \ge o$ compute values that no later step reads. $\square$ The proof needs only that the operator is [associative](/associative-operator/) and commutative, so the same code computes a maximum or a minimum.

With `__shfl_xor_sync` and masks 16, 8, 4, 2, 1 (the butterfly), each step combines lane $\ell$ with lane $\ell \oplus x$, and after 5 steps every lane holds the total, so no broadcast is needed afterwards.

### Warp scan in 5 steps

```cpp
__device__ int warpInclusiveScan(int v) {
    int lane = threadIdx.x & 31;
    for (int offset = 1; offset < 32; offset *= 2) {
        int y = __shfl_up_sync(0xffffffff, v, offset);
        if (lane >= offset) v += y;
    }
    return v;                                  // lane l holds x[0] + ... + x[l]
}
```

This is the [Hillis and Steele scan](/hillis-steele-scan/) on 32 lanes. After the step with offset $o$, lane $\ell$ holds $\sum_{j = \max(0, \ell - 2o + 1)}^{\ell} x_j$, by induction on the steps; after $o = 16$ the window covers all $j \le \ell$. It does $5 \cdot 32 - 31 = 129$ adds against 31 for a sequential scan, but on a warp the extra lanes are free, because every step is one instruction for all 32 lanes. An exclusive scan follows by one more `__shfl_up_sync` by 1 with lane 0 set to the identity.

### Ballot and counting

A ballot turns 32 predicates into one 32-bit word. With `__popc` (population count), lane $\ell$ finds how many lanes below it have a true predicate: `__popc(ballot & ((1u << lane) - 1))`. That count is the output slot of lane $\ell$ in a warp-level [compaction](/compaction/), and `__popc(ballot)` is the number of outputs, all in two instructions.

## Examples

- **Block sum.** Each warp of a 256-thread block reduces its 32 values with `warpReduceSum`. Lane 0 of each warp writes its sum to `shared[warp]`, the block waits at one `__syncthreads()`, and warp 0 reduces the 8 partial sums. The block uses 8 words of shared memory and 1 barrier, against 256 words and a barrier after the initial write and after each of the 8 levels for a tree in shared memory, see [parallel reduction](/parallel-reduce/).
- **Shuffle with width 8.** `__shfl_sync(m, v, 3, 8)` gives each lane the value of lane 3 of its group of 8: lanes 0 to 7 get lane 3, lanes 8 to 15 get lane 11, and so on.
- **Ballot.** For the predicate "lane is a multiple of 3", the ballot has bits 0, 3, 6, ..., 30 set, 11 bits in all; `__any_sync` is true and `__all_sync` is false.
- **Match.** With the keys $\ell \bmod 4$, `__match_any_sync` gives lane 1 the mask of lanes 1, 5, 9, ..., 29. This finds the lanes that update the same bin of a [histogram](/parallel-histogram/), so one lane can do the update for all of them, as in [warp-aggregated atomics](/warp-aggregated-atomics/).

The Python code of this page models one warp as a list of 32 lane values and implements each primitive with its mask and width rules. The tests check the shuffle rules for every variant and width, that reading from a lane outside the mask is an error, the vote and match results, and, on 200 seeded inputs, that the shuffle reduction and the butterfly give `sum`, that the scan gives `itertools.accumulate`, the same for `max`, and that each takes exactly 5 steps. They also check the ballot compaction slots. The CUDA code on this page is for the reader; the tests do not run it.

### A pitfall

Old code did warp reductions in shared memory with no barrier, on the assumption that the 32 lanes run in lockstep. From compute capability 7.0 this is a data race, because the scheduler can interleave the lanes (Guide Section 3.2.2.1.1; Lin and Grover's section on implicit warp-synchronous programming). Use the `_sync` primitives or `__syncwarp()`. Also, a mask must not name a lane that does not reach the call: `__shfl_sync(0xffffffff, ...)` inside `if (lane < 16)` is undefined. Use `__activemask()` or a mask that matches the branch.

## Where it is used

Warp primitives are the innermost level of most GPU [reductions](/parallel-reduce/), [scans](/all-prefix-sums/) and [stream compactions](/compaction/): a block reduces or scans per warp with shuffles, combines the warp results through shared memory, and only then goes to global memory. The single-pass [decoupled look-back scan](/decoupled-look-back-scan/) uses them inside each tile. Ballots drive [warp-aggregated atomics](/warp-aggregated-atomics/) and per-warp work queues, and the match functions group equal keys for [histograms](/parallel-histogram/). [Cooperative groups](/cooperative-groups/) wrap the same instructions as methods of a tile object, such as `tile.shfl_down(v, 1)` and `cg::reduce(tile, v, cg::plus<int>())`.

## References
