---
tag: 61GKS9
kind: algorithm
slug: marzullo-algorithm
name: Marzullo's algorithm
aliases:
- interval intersection for clock sources
- Marzullo intersection
area: distributed/clocks-and-ordering
level: core
summary: Given k intervals that should each hold the true time, a sweep over the sorted endpoints finds the region that the most intervals share, in O(k log k) time.
solves: [clock-synchronization]
model: real-ram
complexity:
  vars: {k: the number of intervals}
  time: {worst: O(k log k)}
  space: {extra: O(k)}
properties: {deterministic: true, recursive: false}
history:
  year: 1984
  people: [Keith Marzullo]
  note: Marzullo gave the method in his 1984 Stanford PhD thesis on maintaining the time in a distributed system, after a 1983 PODC paper with Susan Owicki.
prereqs: [clock-synchronization]
see_also: [ntp, interval-stabbing-query, interval-tree, cristian-algorithm, berkeley-algorithm, truetime, clock-synchronization]
sources:
  - paper: "Keith Marzullo, Maintaining the time in a distributed system, PhD thesis, Stanford University, 1984"
    title: Keith Marzullo, Maintaining the time in a distributed system, PhD thesis, Department of Electrical Engineering, Stanford University, 1984
    locator: the chapter on the intersection of time intervals
  - paper: doi:10.1145/800221.806730
    title: Keith Marzullo and Susan Owicki, Maintaining the time in a distributed system, Proceedings of the 2nd ACM Symposium on Principles of Distributed Computing (PODC), 1983
    locator: pages 295 to 305
  - url: https://www.rfc-editor.org/rfc/rfc5905
    title: David Mills, Jim Martin, Jack Burbank and William Kasch, RFC 5905, Network Time Protocol Version 4, 2010
    locator: Section 11.2.1 (the selection algorithm) and Appendix A.5.5.1 (its C code)
---

*Marzullo's algorithm* takes $k$ intervals, each from one time source that claims that the true time lies in its interval, and finds the region that the largest number of intervals share. It sorts the $2k$ endpoints and sweeps over them with a counter, so it takes $O(k \log k)$ time. If at most $f$ sources are wrong, the true time lies in at least $k - f$ intervals, so a point where fewer meet cannot be the true time. [NTP](/ntp/) uses a variant of it to separate good servers from bad ones.

## In plain words

You ask several people for the time. Each one gives an answer with a margin, for example "between 10:10 and 10:14". Most of them are right, but a few may be badly wrong. You want the time span that the most people agree with.

Draw each answer as a bar on a time line. Walk along the line from left to right. Each time you reach the start of a bar, one more person agrees with this point; each time you pass the end of a bar, one fewer agrees. Keep the place where the most people agree. If only a few people can be wrong, the true time must be in a place where nearly all bars meet, so this place is a good answer, and people whose bars are far from it are probably wrong.

## The problem

**Input.** $k$ closed intervals $[l_1, h_1], \dots, [l_k, h_k]$ with $l_i \le h_i$. In clock synchronization, source $i$ reads offset $\theta_i$ with error bound $\lambda_i$ and gives $[\theta_i - \lambda_i, \theta_i + \lambda_i]$, for example from [Cristian's algorithm](/cristian-algorithm/). A source is *correct* when its interval holds the true value.

**Output.** The largest *depth* $c^* = \max_x |\{ i : l_i \le x \le h_i \}|$, and a region $[a, b]$ where every point has depth $c^*$. If at most $f$ sources are wrong and $c^* \ge k - f$, the caller uses $[a, b]$ as the estimate. This is the *interval stabbing* question of finding a point that the most intervals contain (see [interval stabbing query](/interval-stabbing-query/)). The computation is local, so the model is a [real RAM](/real-ram/) that compares real numbers.

## The algorithm

```pseudo id=main
MARZULLO(intervals)
L1  table ← for each [l, h]: the entries (l, START) and (h, END)
L2  sort table by position; at equal positions START comes before END
L3  best ← 0, count ← 0
L4  for each entry (x, kind) of table, at index j, in order do
        if kind = START then
L5          count ← count + 1
L6          if count > best then
L7              best ← count, a ← x, b ← the position of entry j + 1
        else
L8          count ← count − 1
    return (best, a, b)
```

Putting START first at equal positions makes closed intervals that only touch count as meeting. The pair $[a, b]$ is the leftmost region of largest depth: the scan sets it at the first point where the depth reaches its maximum, and entry $j + 1$ always exists, since the END of an interval that has started comes later.

**With $f$ wrong sources.** Return $[a, b]$ when $best \ge k - f$, and report failure otherwise.

## Example

Four sources give $[10, 14]$, $[11, 15]$, $[9, 12]$ and $[16, 18]$.

| entry | 9 S | 10 S | 11 S | 12 E | 14 E | 15 E | 16 S | 18 E |
|---|---|---|---|---|---|---|---|---|
| count after it | 1 | 2 | 3 | 2 | 1 | 0 | 1 | 0 |
| best | 1 | 2 | 3 | 3 | 3 | 3 | 3 | 3 |

The count first reaches 3 at the entry 11, and the next entry is 12, so the result is $(3, 11, 12)$. Three intervals meet in $[11, 12]$, and the source $[16, 18]$ is not part of it. With $f = 1$, $3 \ge 4 - 1$, so the estimate is $[11, 12]$. With $f = 0$, all four would have to meet, which they do not, so the call fails.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). After line L5 handles every START at a position $p$, the counter equals the depth of $p$: the intervals with $l_i \le p$, less those with $h_i < p$. Some interval endpoint $l_i$ has the largest depth, because if $x$ has the largest depth, the largest left end among the intervals that hold $x$ lies in all of them. So the largest counter value is $c^*$. When line L7 fires at entry $j$, every open interval ends at entry $j+1$ or later, so each of the $best$ intervals holds all of $[a, b]$, and no point holds more. If at most $f$ sources are wrong and the true value $t$ lies in all correct intervals, then $t$ has depth at least $k - f$, so $c^* \ge k - f$.

## Complexity

Line L1 makes $2k$ entries and line L2 sorts them in $O(k \log k)$ time. The scan of lines L4 to L8 takes $O(k)$ time. The table needs $O(k)$ space. This is optimal in the algebraic decision tree model: with the intervals $[x_i, x_i]$, the largest depth is 1 exactly when the $x_i$ are distinct, and [element distinctness](/element-distinctness/) needs $\Omega(k \log k)$ time.

## Properties

- **Exact.** The counter is the depth, so the result is the true maximum, not an approximation.
- **Works with any widths.** A precise source gives a narrow interval, so it constrains the result more.
- **Faults are detected, not assumed.** The caller compares $best$ with $k - f$ and learns whether enough sources agree.
- **Not a value but a region.** The output is an interval; a caller who needs one value takes its midpoint.

## Variants and improvements

**The NTP variant (RFC 5905, Section 11.2.1).** NTP calls a correct source a *truechimer* and a wrong one a *falseticker*. Each candidate gives its offset $\theta$ and its root distance $\lambda$, and three entries: $\theta - \lambda$ (low), $\theta$ (mid) and $\theta + \lambda$ (high). The algorithm tries $f = 0, 1, \dots$ while $2f < m$, for $m$ candidates.

1. Scan the sorted entries upward with a counter $c$ (plus 1 for a low, minus 1 for a high). The first position where $c \ge m - f$ is $l$. Count the mid entries passed on the way in $d$.
2. Scan downward in the same way to find $u$, and add the mid entries passed to $d$.
3. If $d \le f$ and $l < u$, return $[l, u]$ and $f$. Else try $f + 1$.
4. If no $f$ with $2f < m$ works, there is no majority of truechimers, and NTP selects no source.

The mid count rejects a region at the very edge of many intervals, where most offsets lie outside. The text of RFC 5905 says "d = f" in the last step, but its C code in Appendix A.5.5.1 tries again only when $d > f$. The code of this page follows the C code. With the candidates $(\theta, \lambda) = (10, 4), (12, 3), (11, 5), (50, 2)$ in ms, $f = 0$ fails, and $f = 1$ gives $l = 9$, $u = 14$ with $d = 1$, so the source at 50 ms is a falseticker.

**Fault-tolerant intervals.** If at most $f$ of $k$ sources are wrong, the smallest region that is sure to hold the true time is the smallest interval that holds all points of depth at least $k - f$, since the true time has at least that depth. The same sweep finds its two ends. [TrueTime](/truetime/) in Spanner uses a variant to reject liars among its time masters.

**Online use.** With a balanced tree over the endpoints and a stored maximum depth, intervals can be added and removed in $O(\log k)$ time each, as in an [interval tree](/interval-tree/).

## When to use it

Use it when a client reads several time sources, each with an error bound, and some sources may be wrong. It is the selection step between per-server readings and the final clock adjustment in NTP. The same sweep finds the busiest moment of a set of time spans, such as the most meetings at the same time.

## Pitfalls

- **The order at ties.** If END sorts before START at the same position, two closed intervals that touch do not meet, and the result changes.
- **Wrong error bounds.** The method trusts each $\lambda_i$. A correct server with too small a bound looks like a falseticker.
- **Many wrong sources that agree.** If $f$ or more wrong sources agree with each other and the correct ones are fewer, the largest region is the wrong one. The guarantee needs $f < k/2$ at least.
- **An empty region.** With $c^* < k - f$, do not use $[a, b]$; report that the sources disagree.

## Implementations

## History

Keith Marzullo developed the method for his PhD thesis at Stanford University in 1984, under Susan Owicki, after their 1983 PODC paper on maintaining the time in a distributed system. The method entered the Network Time Protocol through David Mills, and RFC 5905 (2010) gives the form that NTP version 4 uses. Corbett et al. (2012) report that the TrueTime daemons of Spanner use a variant of it.

## References
