---
tag: TTCF1W
kind: technique
slug: double-buffering
name: Double buffering
aliases:
- read-ahead buffering
- overlapped I/O
area: sorting/external-sorting
level: intro
summary: Overlap I/O on one buffer with computation on another so that merging does not stall on disk reads.
prereqs: [external-memory-model]
see_also: [external-merge-sort, k-way-merge, replacement-selection, prefetching, disk-striping, disk-scheduling, hard-disk-model]
sources:
  - paper: doi:10.1561/0400000014
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4), 2008
    locator: Section 5.2, Sorting by Merging (Figure 5.3, double buffers for each run), and Section 5.3, Prefetching, Caching, and Applications to Sorting
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition
    locator: Chapter 13, External Sorting (double buffering and blocked I/O)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.4.6, Practical Considerations for Tape Merging (buffer allocation and forecasting)
  - paper: "Roman Dementiev and Peter Sanders, Asynchronous parallel disk sorting, Proceedings of the 15th ACM Symposium on Parallel Algorithms and Architectures (SPAA 2003)"
    locator: pp. 138 to 148, the overlap of computation and I/O in a parallel disk sort
---

Double buffering gives each stream of data two buffers, so that the processor works on one buffer while the disk fills or empties the other. It hides the time of an I/O behind the time of the computation, and the other way round. The time per block drops from the sum of the I/O time and the compute time to the larger of the two. In an [external merge sort](/external-merge-sort/) it costs half of the fan-in, because each run needs two buffers instead of one.

## In plain words

You wash dishes and a friend dries them. With one rack, you wash a rack of dishes, then you wait while your friend dries them, then your friend waits while you wash the next rack. With two racks, you wash into the second rack while your friend dries the first. Both of you work all the time, and the job takes about as long as the slower of the two tasks, not the sum of both.

A program that reads a file works the same way. With one buffer, it waits for the disk, then the disk waits for the program. With two buffers, the disk reads the next block into one buffer while the program works on the block in the other. When both are done, they swap. This needs a disk that can work on its own while the processor computes.

## When it applies

- The data moves as a stream of blocks, in an order that is known before the blocks are needed.
- The disk can transfer a block while the processor computes, for example with direct memory access and an asynchronous read call.
- The I/O time and the compute time per block are of the same order. If one of them is much larger, overlap saves little, because the larger one sets the time anyway.
- There is memory for a second buffer for each stream. In a merge, this memory comes from the fan-in.

## The template

The holes are the source of blocks and the work on each block. A block $i$ takes time $t_r$ to read and time $t_p$ to process.

```pseudo id=main
DOUBLE-BUFFERED-SCAN(F, n)              ▷ F has blocks 1..n; process(·) is the hole
L1  X, Y ← two buffers of one block each
L2  start the read of block 1 into X
L3  for i ← 1 to n do
L4      wait until the read into X is complete
L5      if i < n then start the read of block i + 1 into Y
L6      process(X)                      ▷ the disk fills Y at the same time
L7      swap X and Y
```

Line L5 starts the next read before line L6 starts the work, so the read and the work run at the same time. Line L4 waits only if the read takes longer than the work of the last block. Output works the same way: the program fills one buffer while the disk writes the other.

**Why it is correct.** Each block is read into a buffer that is not in use: at line L5, $Y$ holds block $i - 1$, whose work ended in the last iteration. Line L4 makes sure that block $i$ is complete before line L6 uses it. So the work sees blocks $1, \ldots, n$ in order, each one complete, as with one buffer.

**Cost.** Let $S_i$ be the time at which the work on block $i$ starts. Then $S_1 = t_r$. The read of block $i + 1$ and the work on block $i$ both start at $S_i$, so $S_{i+1} = S_i + \max(t_r, t_p)$. The last work ends at

$$T_2 = t_r + (n - 1)\max(t_r, t_p) + t_p,$$

against $T_1 = n(t_r + t_p)$ with one buffer. Because $t_r + t_p \le 2\max(t_r, t_p)$, the gain $T_1/T_2$ is less than 2 for $n \ge 2$, and it is close to 2 only when $t_r$ and $t_p$ are about equal. The number of I/Os does not change. For example, with $n = 1000$ blocks, $t_r = 8$ ms and $t_p = 5$ ms, one buffer takes 13000 ms and two buffers take 8005 ms.

## Classic examples

**The merge of an external merge sort.** A [k-way merge](/k-way-merge/) of runs on disk holds one block of each run. With one buffer per run, the merge stops each time a block of a run is used up and waits for the next block. With two buffers per run and two output buffers, memory holds $2kB + 2B$ items, so the fan-in is $k = M/(2B) - 1$ instead of $M/B - 1$. For $M/B = 100$, the fan-in drops from 99 to 49. The number of passes is $\lceil \log_k r \rceil$, so for $r = 10^4$ runs both choices need 3 passes, and the merge with double buffers runs faster. Vitter's survey shows this design in its Figure 5.3.

**Run formation.** [Replacement selection](/replacement-selection/) reads one stream and writes one stream. Two input buffers and two output buffers let the heap work without a stop for the disk, at the cost of four blocks of memory.

**A sequential scan.** A scan for a filter, a sum or a copy is a template with a trivial process step. Operating systems do the same with read-ahead: when a program reads a file in order, the system starts the read of the next blocks before the program asks for them.

**Graphics.** A display shows one frame buffer while the program draws the next frame into the second one, and the two swap at the end of each frame. The idea is the same: the consumer never sees a buffer that is not complete.

## Variations

- **More than two buffers.** With $b$ buffers for a stream, up to $b - 1$ reads can be in progress. This helps when the I/O time varies, for example with several disks or with seeks of different lengths.
- **Forecasting.** In a merge, the runs do not use their blocks at the same rate. The run whose buffer will be empty first is the run whose buffered block has the smallest last key. Forecasting reads the next block of that run, so a merge needs only a few spare buffers in a shared pool instead of a second buffer for each run. See [prefetching](/prefetching/) and Knuth's Section 5.4.6.
- **Several disks.** With $D$ disks, a merge must read the blocks it needs next from different disks at the same time. Simple [disk striping](/disk-striping/) does this with logical blocks of $DB$ items. Better methods choose which blocks to prefetch from each disk.
- **Asynchronous threads.** A separate I/O thread, or a pipeline of stages with queues between them, does the same as the template with more than two buffers.

## Pitfalls

- **Starting the read too late.** If line L5 comes after line L6, the read of the next block starts only after the work, and there is no overlap.
- **Reading into the buffer in use.** If the program swaps the buffers before the work on the old block ends, the read of line L5 overwrites data that is still needed.
- **Counting the buffers twice.** In a merge, double buffers halve the fan-in. If $k$ is computed for one buffer per run, memory overflows.
- **Expecting more than a factor of 2.** Overlap cannot make the job faster than the larger of the total I/O time and the total compute time. If the disk is the bottleneck, fewer passes or larger blocks help more.
- **The wrong run in a merge.** With a fixed second buffer for each run, the merge can still stop when two runs empty their buffers one after the other. Forecasting, or a pool of buffers, prevents this.

## Exercises

1. With $n = 500$ blocks, $t_r = 4$ ms and $t_p = 4$ ms, compute the time with one buffer and with two buffers.
2. Show that $T_1/T_2 \le 2$ for all $n \ge 1$, $t_r > 0$ and $t_p > 0$, and find when the ratio tends to 2 as $n$ grows.
3. A merge has memory for $M = 4096$ items, blocks of $B = 64$ items, and two buffers per run and for the output. Compute the fan-in, and the number of passes for 3000 runs. Compare with one buffer per run.
4. A merge holds one block of each of three runs. The last keys in the buffers are 40, 17 and 63. Which run must get its next block first, and why?

## References
