---
tag: 3GCSWG
kind: algorithm
slug: ordered-statistic-cfar
name: Ordered-statistic CFAR
aliases:
- OS-CFAR
area: communications/radar-waveforms
level: advanced
summary: "Sets the threshold from the k-th smallest reference cell, kept in a sorted sliding window. Up to N - k interfering targets in the window cannot raise the threshold."
solves: [cfar-detection]
model: real-ram
complexity:
  vars: {n: the number of cells, N: the number of reference cells}
  time: {worst: Θ(n N), average: Θ(n N), best: O(n N)}
  space: {extra: Θ(N)}
properties: {deterministic: true, online: true, scale_invariant: true, constant_false_alarm_rate_in_homogeneous_noise: true, robust_to_interfering_targets: true, exact_for_rational_input: true}
history:
  year: 1983
  people: [Hermann Rohling]
  note: "Rohling took the threshold from an order statistic of the reference cells, gave the false alarm probability in closed form and tabulated the factor and its loss."
prereqs: [cfar-detection, cell-averaging-cfar, binary-search]
see_also: [quickselect, sliding-window-median, order-statistic-tree, balanced-binary-search-tree, swerling-target-models, range-doppler-processing, signal-detection, sliding-window]
sources:
  - paper: doi:10.1109/TAES.1983.309350
    title: Radar CFAR thresholding in clutter and multiple target situations
    locator: "H. Rohling, IEEE Transactions on Aerospace and Electronic Systems 19(4), 1983, pp. 608 to 621: equations 14 and 15 (the false alarm and detection probabilities) and Tables I to IV (the factor T and the average threshold)"
  - paper: "P. P. Gandhi and S. A. Kassam, IEEE Transactions on Aerospace and Electronic Systems 24(4), 1988, pp. 427 to 445"
    title: Analysis of CFAR processors in nonhomogeneous background
    locator: "the whole paper (CA and OS processors at clutter edges and with interfering targets)"
  - book: isbn:9780071444743
    title: "Mark A. Richards, Fundamentals of Radar Signal Processing, McGraw-Hill, 2005"
    locator: "Chapter 7, Section 7.4 (interfering targets and clutter edges) and Section 7.6 (order statistic CFAR)"
---

Ordered-statistic CFAR (OS-CFAR) is a [CFAR detector](/cfar-detection/) that takes the noise estimate of each cell from the $k$-th smallest of its $N$ reference cells, in place of their sum. A strong second target in the window then cannot raise the threshold: up to $N - k$ such values only push larger values to the top of the sorted list. In homogeneous exponential noise the false alarm probability is the product $\prod_{m=0}^{k-1} (N - m)/(N - m + T)$, independent of the noise power. The price is a loss of about 1 dB against [cell-averaging CFAR](/cell-averaging-cfar/) and a sorted window, which costs $O(N)$ per cell with a list or $O(\log N)$ with a balanced tree.

## In plain words

Look at the cells around the one you test, skip the guard cells, and sort the rest. Take the value at position $k$, which is often about three quarters of the way up. Multiply it by a factor $T$ and compare the tested cell with the result. If one or two of the reference cells hold other targets, they go to the top of the sorted list and do not change the value at position $k$. To move to the next cell, take out the two values that leave the window and put in the two that enter, each at its place in the sorted order.

## The problem

The input is a list $x[0], \dots, x[n-1]$ of square-law powers, an even number $N = 2h$ of reference cells, a number $G \ge 0$ of guard cells on each side, a rank $1 \le k \le N$ and a factor $T > 0$. The reference window of cell $i$ is the lagging cells $i - G - h, \dots, i - G - 1$ and the leading cells $i + G + 1, \dots, i + G + h$. Let $X_{(k)}(i)$ be the $k$-th smallest value of this multiset. The output is the list of cells $i$, with $G + h \le i \le n - 1 - G - h$, for which $x[i] > T X_{(k)}(i)$. For a design value $P_{fa}$, $T$ is the unique root of $\prod_{m=0}^{k-1} (N - m)/(N - m + T) = P_{fa}$.

## The algorithm

```pseudo id=main
OS-CFAR(x[0..n-1], N, G, k, T)
L1  w <- sorted list of the reference cells of the first cell i = G + h, with h = N / 2
L2  for i <- G + h to n - 1 - G - h
L3      z <- w[k]                                     ▷ the k-th smallest value, counted from 1
L4      t <- T * z
L5      if x[i] > t then report i
L6      remove one copy of x[i - G - h] from w; insert x[i - G] into w in order
L7      remove one copy of x[i + G + 1] from w; insert x[i + G + h + 1] into w in order
```

Line L1 sorts the first window. Line L3 reads the order statistic in $O(1)$ time, because the list is sorted. Lines L6 and L7 move the window one cell to the right: in the lagging half the oldest cell leaves and the cell next to the guard zone enters, and in the leading half the cell next to the guard zone leaves and a new outer cell enters. Each removal and each insertion finds its position by [binary search](/binary-search/). After the last cell, lines L6 and L7 are skipped.

## Example

Take $x = (2, 1, 3, 1, 2, 1, 2, 30, 1, 2, 24, 2, 1, 3, 1, 2, 1, 2)$, so $n = 18$, with two targets of 30 and 24 at cells 7 and 10. Use $N = 8$, $G = 1$, $k = 6$ and $P_{fa} = 10^{-2}$. The root of $\prod_{m=0}^{5} (8 - m)/(8 - m + T) = 10^{-2}$ is $T = 5.8696$. Cells 5 to 12 have a full window. The last column gives the threshold of [cell-averaging CFAR](/cell-averaging-cfar/) with the same window and $P_{fa}$, which is $0.7783$ times the sum.

| $i$ | lagging | leading | sorted window | $X_{(6)}$ | $T X_{(6)}$ | $x[i]$ | OS | CA threshold |
|---|---|---|---|---|---|---|---|---|
| 5 | 2, 1, 3, 1 | 30, 1, 2, 24 | 1, 1, 1, 2, 2, 3, 24, 30 | 3 | 17.61 | 1 | no | 49.81 |
| 6 | 1, 3, 1, 2 | 1, 2, 24, 2 | 1, 1, 1, 2, 2, 2, 3, 24 | 2 | 11.74 | 2 | no | 28.02 |
| 7 | 3, 1, 2, 1 | 2, 24, 2, 1 | 1, 1, 1, 2, 2, 2, 3, 24 | 2 | 11.74 | 30 | target | 28.02 |
| 8 | 1, 2, 1, 2 | 24, 2, 1, 3 | 1, 1, 1, 2, 2, 2, 3, 24 | 2 | 11.74 | 1 | no | 28.02 |
| 9 | 2, 1, 2, 30 | 2, 1, 3, 1 | 1, 1, 1, 2, 2, 2, 3, 30 | 2 | 11.74 | 2 | no | 32.69 |
| 10 | 1, 2, 30, 1 | 1, 3, 1, 2 | 1, 1, 1, 1, 2, 2, 3, 30 | 2 | 11.74 | 24 | target | 31.91 |
| 11 | 2, 30, 1, 2 | 3, 1, 2, 1 | 1, 1, 1, 2, 2, 2, 3, 30 | 2 | 11.74 | 2 | no | 32.69 |
| 12 | 30, 1, 2, 24 | 1, 2, 1, 2 | 1, 1, 1, 2, 2, 2, 24, 30 | 2 | 11.74 | 1 | no | 49.03 |

OS-CFAR reports cells 7 and 10. The other target is always in the top two places of the sorted window, so the sixth value stays at 2 or 3. CA-CFAR detects the 30 but misses the 24, because the 30 in the window of cell 10 raises the CA threshold to 31.91.

## Correctness

The invariant of the loop is that at the start of the iteration for cell $i$, $w$ is the sorted list of the multiset of the reference values of cell $i$. Line L1 sets it. The windows of $i$ and $i + 1$ differ by exactly the two cells removed and the two cells inserted in lines L6 and L7, and removing one copy of a value and inserting a value in order keeps a sorted list sorted. So line L3 reads $X_{(k)}(i)$, and the output is the definition. The [correctness proof](proofs/correctness.md) gives the details. It also proves the false alarm probability, through the exponential spacings of order statistics, the detection probability $P_d = P_{fa}(T/(1+S))$ of a Swerling 1 target, and the bound on interferers: if at most $N - k$ reference cells hold interference, $X_{(k)}(i)$ is at most the $k$-th smallest of the clean cells, with equality when the interferers are at least that large.

## Complexity

**Time.** Line L1 sorts $N$ values in $\Theta(N \log N)$. In each of the $n - 2G - N$ iterations, the four searches of lines L6 and L7 take $O(\log N)$ comparisons, but each insertion or deletion in an array list moves the elements after its position, up to $N$ of them. On random input the average move is about $N/2$. So the loop costs $\Theta(nN)$ in the worst and the average case, and $O(nN)$ in all cases. The tests compare the sliding window with a fresh sort of each window, which costs $\Theta(nN \log N)$. With a [balanced binary search tree](/balanced-binary-search-tree/) or an [order statistic tree](/order-statistic-tree/) that stores subtree sizes, each step is $O(\log N)$ and the total is $O(n \log N)$. Computing $X_{(k)}$ from scratch with [quickselect](/quickselect/) costs $O(N)$ expected per cell.

**Space.** $\Theta(N)$ for the sorted window, beyond the input and the output.

## Properties

- **Constant false alarm rate (theorem, homogeneous exponential noise).** $P_{fa} = \prod_{m=0}^{k-1} (N - m)/(N - m + T)$, independent of the noise power. For integer $T$ it equals Rohling's form $k \binom{N}{k} (k-1)!\, (T + N - k)!/(T + N)!$, and the tests check the two forms exactly for all $N \le 12$, $k \le N$ and $T \le 14$.
- **The factor (closed form).** At $P_{fa} = 10^{-6}$: $T = 46.70$ for $N = 8$, $k = 6$; $T = 20.95$ for $N = 16$, $k = 12$; $T = 16.29$ for $N = 24$, $k = 18$. These match Rohling's Table II to the printed decimal.
- **The loss.** The average threshold $T\, E[X_{(k)}]/\mu$ is 27.19 for $N = 16$, $k = 12$, against 21.94 for CA-CFAR: 0.93 dB more. For a Swerling 1 target at $P_d = 0.9$, OS needs 24.08 dB and CA needs 23.15 dB.
- **Robust to interfering targets (theorem).** Up to $N - k$ reference cells can hold any values, and the threshold is still at most $T$ times the $k$-th smallest clean value. For CA-CFAR one interferer of power $A$ adds $A$ to the sum, with no limit.
- **Scale invariant (theorem).** Multiplying all cells by $c > 0$ multiplies $X_{(k)}$ by $c$, so no decision changes.

## Variants and improvements

- **The choice of $k$.** Rohling's average threshold table uses $k = 3N/4$, a common choice. A larger $k$ lowers the loss in homogeneous noise but tolerates fewer interferers. A smaller $k$ tolerates more interferers but has a larger loss and more false alarms at a clutter edge.
- **OS on each half.** Take an order statistic of each half and use the larger (OSGO) or the smaller (OSSO), which mixes the clutter edge behavior of GO and SO with the robustness of OS.
- **Trimmed mean (TM-CFAR).** Sort the window, drop the $r_1$ smallest and $r_2$ largest values and sum the rest. With $r_1 = 0$ and $r_2 = 0$ it is CA, and with $r_1 = k - 1$ and $r_2 = N - k$ it is OS.
- **Censored mean.** Drop the $N - k$ largest values and average the $k$ smallest.
- **Two dimensions.** On the output of [range-Doppler processing](/range-doppler-processing/), the window is a ring of cells in range and Doppler. Automotive radar often uses OS on the range axis of each Doppler bin, because targets at the same range are common there.
- **A faster window.** A sliding median structure (see [sliding window median](/sliding-window-median/)) generalizes to any rank $k$ with two heaps or an order statistic tree.

## When to use it

Use OS-CFAR when targets come in groups, so that a second target is often in the window of the first: road traffic, formations of aircraft, or ships in a harbor. Also use it when clutter is spiky and a few reference cells are much larger than the rest. In thermal noise with sparse targets, [cell-averaging CFAR](/cell-averaging-cfar/) has a smaller loss and a lower cost.

## Pitfalls

- **An index off by one in line L3.** The pseudocode counts from 1. In a language that counts from 0, line L3 must read `w[k - 1]`. Reading `w[k]` takes the $(k+1)$-th value, raises the threshold, and gives a false alarm rate below the design value, with a larger loss.
- **Removing every copy of a value in lines L6 and L7.** Powers from integer counts or quantized samples repeat. Line L6 must remove exactly one copy of $x[i - G - h]$. A removal that deletes all equal values shrinks the window and makes line L3 read the wrong rank, or an index that does not exist. The tests use small integer values, with many repeats, on 600 random inputs and compare the result with a fresh sort of each window.
- **The factor of CA-CFAR in line L4.** $T$ comes from the product $\prod_{m<k} (N - m)/(N - m + T)$, not from $(1 + \tau)^{-N}$, and it multiplies one cell, not a sum. For $N = 16$ and $P_{fa} = 10^{-6}$, $T = 20.95$ for $k = 12$, while the CA factor on the sum is 1.37 and on the mean is 21.94.
- **More interferers than $N - k$.** With $k = N$, line L3 takes the maximum, and one interferer sets the threshold. In the tests, $N - k + 1$ interferers of $10^6$ make the threshold $T \cdot 10^6$.
- **Clutter edges.** If the clutter fills more than $N - k$ reference cells on one side and the cell under test is in the quiet region, the threshold comes from the clutter and the cell is masked. If the cell is in the clutter and more than $k$ cells are quiet, the threshold is too low and false alarms follow.

## Implementations

## History

Hermann Rohling published OS-CFAR in 1983 in the IEEE Transactions on Aerospace and Electronic Systems. He gave the false alarm probability in closed form, tabulated the factor $T$ and the average threshold for several $N$ and $k$, and studied the detector in clutter and with several targets. P. P. Gandhi and S. A. Kassam compared CA, GO, SO and OS processors at clutter edges and with interfering targets in 1988. OS-CFAR is now common in automotive radar.

## References
