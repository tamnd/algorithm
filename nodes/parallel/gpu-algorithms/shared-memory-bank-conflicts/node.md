---
tag: TZK1W3
kind: concept
slug: shared-memory-bank-conflicts
name: Shared memory bank conflicts
aliases:
- bank conflicts
area: parallel/gpu-algorithms
level: intro
summary: Shared memory has 32 banks of 4-byte words; a warp access that asks one bank for k distinct words takes k passes, and padding a 32 by 32 tile to 33 columns removes the column conflicts.
prereqs: [gpu-memory-hierarchy, simt-model]
see_also: [shared-memory-tiling, memory-coalescing, parallel-matrix-transpose, parallel-histogram, all-prefix-sums, blelloch-scan, euclidean-algorithm]
sources:
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 2.3.4.2 (shared memory access patterns, 32 banks, broadcast, Figure 15), Section 2.3.4.2.1 (transpose through shared memory), Section 2.3.4.2.2 (the 32-way conflict of a column and padding) and Section 5.1.3, Table 34 (32 banks for every listed compute capability)
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition
    locator: Chapter 5 (memory architecture and data locality) and Chapter 6 (performance considerations)
  - url: https://rocm.docs.amd.com/projects/HIP/en/latest/understand/hardware_implementation.html
    title: AMD, HIP documentation, Hardware implementation
    locator: the section on the local data share (LDS)
---

A **shared memory bank conflict** happens when two or more lanes of one [warp](/simt-model/) access different words in the same bank of shared memory in one instruction. Shared memory is split into 32 banks, and successive 4-byte words go to successive banks; each bank serves one word per clock, so a conflict splits the access into several passes (CUDA Programming Guide v13.5, Section 2.3.4.2). The count of 32 banks holds for every compute capability in the Guide's Table 34 (7.5 to 12.x), and the cost model is the [SIMT model](/simt-model/) with passes per warp access as the measure.

## In plain words

A room has thirty-two shelves, and the boxes go on them in turn: the first box on shelf one, the next on shelf two, and so on, then back to shelf one. Each shelf has one clerk, who hands out one box per turn. A team of thirty-two workers asks for boxes at the same moment. If every worker wants a box on a different shelf, all get their boxes in one turn. If two workers want different boxes from the same shelf, that clerk needs two turns, and the team waits. If many workers want the very same box, the clerk holds it up once and all of them read it. When workers walk down a column of a square grid of boxes, they all hit one shelf. Adding one empty box at the end of each row shifts every row by one shelf and fixes this.

## The idea

### Banks and the conflict degree

Let lane $\ell$ access the 4-byte word with word address $a_\ell$ (the byte address divided by 4). Its bank is $a_\ell \bmod 32$. The **conflict degree** of the access is

$$d = \max_{b \in \{0, \dots, 31\}} \bigl\lvert \{ a_\ell : \ell \text{ active}, \ a_\ell \bmod 32 = b \} \bigr\rvert,$$

the largest number of distinct words that one bank must deliver. The hardware serves the access in $d$ passes, so it takes $d$ times the time of a conflict-free access. A degree of 1 means no conflict.

**The broadcast rule.** Lanes that read the same word count once: the word is read once and broadcast to them. So 32 lanes reading one word have $d = 1$. For a write of the same word by several lanes, only one lane writes, and the Guide does not say which one (Section 2.3.4.2).

### Strided access

Let lane $\ell$ read word $s\ell$, for a stride $s \ge 1$, and let $g = \gcd(s, 32)$. Then

$$d(s) = \gcd(s, 32).$$

*Proof.* Lanes $\ell$ and $\ell'$ hit the same bank if and only if $32$ divides $s(\ell - \ell')$, which holds if and only if $32/g$ divides $\ell - \ell'$, because $s/g$ and $32/g$ are coprime. So the 32 lanes fall into classes of $\ell \bmod 32/g$, each class has $g$ lanes, and all lanes of a class use one bank. Their words $s\ell$ are distinct because $s \ge 1$. So each used bank delivers exactly $g$ distinct words. $\square$

So every odd stride is conflict free, stride 2 is a 2-way conflict, and stride 32 is a 32-way conflict. This matches Figure 15 of Section 2.3.4.2, where strides 1 and 3 have no conflict and stride 2 has a two-way conflict. The proof uses the [greatest common divisor](/euclidean-algorithm/) only through the fact that $s/g$ and $32/g$ are coprime.

### The 32 by 32 tile and padding

A tile `float tile[32][32]` puts element $(r, c)$ at word $32r + c$, in bank $c$. A warp that reads row $r$ (lanes $c = 0, \dots, 31$) hits 32 banks. A warp that reads column $c$ (lanes $r = 0, \dots, 31$) hits only bank $c$, with 32 distinct words, so $d = 32$ (Section 2.3.4.2.2).

Pad the tile to 33 columns: `float tile[32][33]`. Element $(r, c)$ is at word $33r + c$, in bank $(33r + c) \bmod 32 = (r + c) \bmod 32$. For a fixed $c$, the map $r \mapsto (r + c) \bmod 32$ is a bijection of $\{0, \dots, 31\}$, so a column read hits 32 different banks and $d = 1$. Rows stay conflict free for the same reason. The cost is 32 unused words, 3% of the tile. In general, a row width $w$ gives column degree $\gcd(w, 32)$ by the stride result, so any odd width works.

```cpp
#define TILE 32
__global__ void transpose(const float* in, float* out, int n) {
    __shared__ float tile[TILE][TILE + 1];          // +1 removes the column conflict
    int x = blockIdx.x * TILE + threadIdx.x;
    int y = blockIdx.y * TILE + threadIdx.y;        // block of 32 x 32 threads
    if (x < n && y < n) tile[threadIdx.y][threadIdx.x] = in[y * n + x];   // row write
    __syncthreads();
    x = blockIdx.y * TILE + threadIdx.x;
    y = blockIdx.x * TILE + threadIdx.y;
    if (x < n && y < n) out[y * n + x] = tile[threadIdx.x][threadIdx.y];  // column read
}
```

Both global accesses are [coalesced](/memory-coalescing/), because `threadIdx.x` moves along a row of `in` and of `out`. The transpose happens in shared memory, where the read `tile[threadIdx.x][threadIdx.y]` walks down a column. Without the padding, that read is a 32-way conflict in every warp.

## Examples

| Access by lane $\ell$ (4-byte words) | Degree |
|---|---|
| `s[l]` | 1 |
| `s[2*l]` | 2 |
| `s[3*l]` | 1 |
| `s[8*l]` | 8 |
| `s[32*l]`, a column of `float[32][32]` | 32 |
| `s[33*l]`, a column of `float[32][33]` | 1 |
| `s[0]` in every lane | 1 (broadcast) |
| `s[l/2]` (pairs share a word) | 1 |
| lanes 0 to 15 read word 0, lanes 16 to 31 read word 32 | 2 |

The Python code of this page computes the degree of a warp access from its 32 word addresses. The tests check $d(s) = \gcd(s, 32)$ for strides 1 to 129, the column degree $\gcd(w, 32)$ for row widths 1 to 79, the broadcast cases, and a full $32 \times 32$ transpose through shared memory: it is correct with and without padding, its column reads have degree 32 without padding and 1 with it. The CUDA code on this page is for the reader; the tests do not run it.

## Where it is used

Bank conflicts matter wherever a kernel accesses shared memory with a stride. [Parallel matrix transpose](/parallel-matrix-transpose/) uses the padded tile above. The tree-shaped [Blelloch scan](/blelloch-scan/) in shared memory accesses words at strides $2, 4, 8, \dots$, so its deep levels have conflicts of degree up to 32 unless the indices are padded, for example with one extra word after every 32. [Shared memory tiling](/shared-memory-tiling/) for matrix multiplication is conflict free in its inner loop: a warp reads one element of the tile of $A$, which is a broadcast, and one row of the tile of $B$, which hits 32 banks. A layout in which a warp reads a column of a tile instead has a 32-way conflict. A [histogram](/parallel-histogram/) in shared memory has data-dependent conflicts when many lanes update bins in the same bank. AMD GPUs have a banked local data share (LDS) as well; the bank count and width there are given in the vendor documentation.

## References
