---
tag: AGT6N3
kind: problem
slug: activity-selection
name: Activity selection
aliases:
- Interval scheduling
- Maximum set of non-overlapping intervals
- Minimum removals to make intervals disjoint
- interval scheduling
- interval scheduling maximization
- maximum disjoint intervals
area: techniques/greedy
level: intro
summary: Choose the maximum number of pairwise non-overlapping intervals.
prereqs: [greedy-algorithm, sorting-problem]
see_also: [earliest-finish-time-first, greedy-stays-ahead, greedy-choice-property, interval-partitioning, weighted-interval-scheduling, k-machine-interval-scheduling, online-interval-scheduling, interval-piercing-greedy]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.1, An activity-selection problem
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.1, Interval Scheduling, The Greedy Algorithm Stays Ahead; Section 6.1, Weighted Interval Scheduling
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 4, Greedy Algorithms
---

Activity selection asks for the largest set of pairwise non-overlapping intervals among $n$ given intervals on a line. It is also called interval scheduling: each interval is a request to use one resource, and the goal is to serve the most requests. The [earliest finish time first](/earliest-finish-time-first/) algorithm solves it in $O(n \log n)$ time, and it is the first example of a [greedy algorithm](/greedy-algorithm/) in most courses. Small changes, such as values on the intervals or several resources, give problems where the same greedy rule fails.

## In plain words

Many people want to book the same room. Each booking has a start time and an end time. Two bookings that overlap cannot both be accepted. You want to accept as many bookings as you can.

The answer is a number, the most bookings that fit, together with a list of bookings that reaches it. Several different lists can reach the best number.

The problem looks like it needs a search over all lists, but it does not. A short rule finds a best list: keep taking the booking that ends first among those that still fit. This page is about the problem, its versions and its relatives. The page on the rule itself gives the full proof that it is correct.

## Definition

**Input.** A finite set $S$ of $n$ activities. Activity $a \in S$ has a start time $s(a)$ and a finish time $f(a)$ from a totally ordered set, usually the integers or the reals, with $s(a) < f(a)$. Activity $a$ occupies the half-open interval $[s(a), f(a))$. Two activities with the same times are still two different items.

**Compatibility.** Two distinct activities $a, b$ are compatible when $[s(a), f(a)) \cap [s(b), f(b)) = \emptyset$, which is the case if and only if $f(a) \le s(b)$ or $f(b) \le s(a)$. A set $A \subseteq S$ is compatible when its activities are pairwise compatible. The empty set and each set of one activity are compatible.

**Output.** A compatible set $A \subseteq S$ with
$$ |A| = \mathrm{opt}(S) = \max\{\, |B| : B \subseteq S \text{ and } B \text{ is compatible} \,\}. $$

**Convention.** With half-open intervals, an activity that ends at time 7 and one that starts at time 7 are compatible. Some texts use closed intervals $[s(a), f(a)]$, and then a common end point is a conflict. All results on this page hold for both conventions, with $\le$ replaced by $<$ in the test of compatibility.

## Variants

- **Minimum removals.** Delete the fewest intervals so that the rest are pairwise disjoint. The answer is $n - \mathrm{opt}(S)$, so this is the same problem.
- **Weighted activity selection.** Each activity has a value $v(a) > 0$, and the goal is a compatible set of the largest total value. This is [weighted interval scheduling](/weighted-interval-scheduling/). It is solved by [dynamic programming](/dynamic-programming/), not by a greedy rule.
- **Several identical resources.** Choose the most activities that can be split among $k$ rooms, with no overlap inside a room. This is [k-machine interval scheduling](/k-machine-interval-scheduling/). For $k = 1$ it is activity selection.
- **Cover all activities.** Use the fewest rooms so that every activity gets a room. This is [interval partitioning](/interval-partitioning/). It asks for a partition of all of $S$, not for a subset.
- **Online.** The activities arrive one by one and each must be accepted or rejected at once. This is [online interval scheduling](/online-interval-scheduling/). No deterministic rule is optimal on every input in this setting.
- **Circular arcs.** The activities are arcs of a circle, such as daily shifts that cross midnight. Then no activity is first in time, and the plain greedy scan does not apply directly.

## Examples

**The CLRS instance.** Take the 11 activities, as (start, finish), $a_1 = (1, 4)$, $a_2 = (3, 5)$, $a_3 = (0, 6)$, $a_4 = (5, 7)$, $a_5 = (3, 9)$, $a_6 = (5, 9)$, $a_7 = (6, 10)$, $a_8 = (8, 11)$, $a_9 = (8, 12)$, $a_{10} = (2, 14)$, $a_{11} = (12, 16)$. Here $\mathrm{opt}(S) = 4$, and exactly four compatible sets have size 4: $\{a_1, a_4, a_8, a_{11}\}$, $\{a_1, a_4, a_9, a_{11}\}$, $\{a_2, a_4, a_8, a_{11}\}$ and $\{a_2, a_4, a_9, a_{11}\}$. Earliest finish time first returns the first of them. The minimum number of removals is $11 - 4 = 7$.

**Rules that fail.** Three natural rules are not optimal.

| rule | input | rule gives | optimum |
| --- | --- | --- | --- |
| earliest start first | $[0, 10)$, $[1, 2)$, $[3, 4)$ | 1 | 2 |
| shortest interval first | $[0, 5)$, $[4, 7)$, $[6, 10)$ | 1 | 2 |
| fewest conflicts first | $[0, 3)$, $[3, 6)$, $[6, 9)$, $[9, 12)$, $[5, 7)$, three copies of $[2, 4)$, three copies of $[8, 10)$ | 3 | 4 |

In the third row, $[5, 7)$ has 2 conflicts and every other interval has at least 3, so the rule takes $[5, 7)$ first. That removes $[3, 6)$ and $[6, 9)$, and every way to go on reaches only 3 intervals, while the four intervals of the top row give 4. Kleinberg and Tardos, Section 4.1, draw an instance of the same shape. Of the rules in this section, only "earliest finish first" is optimal on all inputs.

**Equal intervals.** For $n$ copies of $[0, 1)$, $\mathrm{opt}(S) = 1$. For $[0, 1), [1, 2), \ldots, [n-1, n)$, $\mathrm{opt}(S) = n$ with half-open intervals, but only $\lceil n/2 \rceil$ with closed intervals, because then neighbours touch.

**Weighted case.** For $[0, 2)$ with value 1 and $[1, 10)$ with value 100, the unweighted optimum takes either one, and the weighted optimum is 100. The earliest finish rule takes $[0, 2)$ and reaches only 1.

## Known algorithms

- **[Earliest finish time first](/earliest-finish-time-first/).** Sort by finish time, then take each activity that starts at or after the finish of the last one taken. $O(n \log n)$ time, or $\Theta(n)$ after the sort. Its correctness proof is the model of the [greedy stays ahead](/greedy-stays-ahead/) method; CLRS proves it with the [greedy-choice property](/greedy-choice-property/) and an [exchange argument](/exchange-argument/) instead.
- **Latest start time first.** The mirror image: sort by start time and scan from the latest start. Same cost, also optimal.
- **Dynamic programming.** Sort by finish time and compute $\mathrm{opt}$ of each prefix with the recurrence $M[j] = \max(M[j-1], 1 + M[p(j)])$, where $p(j)$ is the last activity that finishes at or before $s(a_j)$. This is the algorithm of [weighted interval scheduling](/weighted-interval-scheduling/) with all values 1. It costs $O(n \log n)$ with binary search for $p(j)$. It is slower to write than the greedy rule, but it also solves the weighted variant.
- **Brute force.** Test all $2^n$ subsets. Only useful as a test oracle for small $n$.

## Bounds

- **Upper bound.** $O(n \log n)$ time in the [comparison model](/comparison-model/) on any input, by sorting and one scan. If the activities are given sorted by finish time, $\Theta(n)$ time, which is optimal because every activity must be read.
- **Lower bound for an ordered output.** If the output must list the chosen activities in time order, $\Omega(n \log n)$ comparisons are necessary in the worst case: for distinct integers $x_1, \ldots, x_n$, the intervals $[2x_i, 2x_i + 1)$ are pairwise compatible, all of them are in the answer, and listing them in order sorts the $x_i$.
- **Size of the answer.** $1 \le \mathrm{opt}(S) \le n$ for $n \ge 1$. Both ends are reached: by $n$ copies of one interval and by $n$ disjoint intervals.

## Reductions

- **To maximum independent set.** Build the interval graph: one vertex for each activity and an edge between each pair of incompatible activities. A compatible set is an [independent set](/independent-set/) of this graph, so activity selection is [maximum independent set](/maximum-independent-set/) on interval graphs. Interval graphs are [chordal graphs](/chordal-graph/), and on them the problem is easy, while it is NP-hard on general graphs.
- **Duality with piercing.** For closed intervals, the largest number of pairwise disjoint intervals equals the smallest number of points that meet every interval. Proof: $k$ disjoint intervals need $k$ distinct points, so $\max \le \min$. Run earliest finish first with the test $s > last$ and let $p_1, \ldots, p_k$ be the finish times of the chosen intervals. Each interval $a$ is either chosen, and then it contains its own finish time, or rejected, and then $s(a) \le last = f(i) \le f(a)$ for a chosen $i$, so it contains $f(i)$. So $k$ points meet every interval, and $\min \le k = \max$. The greedy algorithm for the piercing side is [interval piercing](/interval-piercing-greedy/).
- **From weighted to longest path.** Weighted activity selection is a longest path problem in a DAG whose vertices are the activities in order of finish time. With all values 1 it is this problem.

## Applications

- **Booking one resource.** Rooms, machines, a telescope, a satellite antenna: when each accepted request counts the same, the most requests are served by the greedy rule.
- **Removing overlaps.** Making a set of intervals pairwise disjoint with the fewest deletions, for example to clean overlapping annotations in a genome or a text.
- **Teaching.** CLRS uses the problem to introduce the greedy-choice property and optimal substructure. Kleinberg and Tardos use it to introduce the stays-ahead argument, and its weighted version to introduce dynamic programming.

## References
