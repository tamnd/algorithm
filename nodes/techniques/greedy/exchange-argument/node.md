---
tag: HF5WPF
kind: technique
slug: exchange-argument
name: Exchange argument
aliases:
- Cut-and-paste exchange
- Interchange argument
- exchange proof
area: techniques/greedy
level: intro
summary: Proof method that transforms an optimal solution into the greedy one without losing optimality.
prereqs: [greedy-algorithm]
see_also: [greedy-stays-ahead, greedy-choice-property, smith-rule, minimizing-maximum-lateness, huffman-coding, cut-property, inversion, belady-algorithm]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.2, Scheduling to Minimize Lateness, An Exchange Argument; Section 4.3, Optimal Caching
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 15, Greedy Algorithms (proofs of the greedy-choice property)
  - paper: doi:10.1002/nav.3800030106
    title: Wayne E. Smith, Various optimizers for single-stage production, Naval Research Logistics Quarterly 3(1-2), 1956
    locator: pages 59 to 66
---

An exchange argument proves a greedy algorithm optimal by taking an arbitrary optimal solution and changing it, one exchange at a time, into the greedy solution, while showing that no exchange makes it worse. When the changes end, the greedy solution has a value at least as good as the optimum, so it is optimal. The method is also called an interchange argument, and in CLRS the single-step form is the cut-and-paste proof of the [greedy-choice property](/greedy-choice-property/). It is the standard proof for scheduling rules such as [Smith's rule](/smith-rule/) and [earliest due date](/minimizing-maximum-lateness/), and for [Huffman codes](/huffman-coding/) and the [cut property](/cut-property/) of spanning trees.

## In plain words

You want to show that the greedy answer is a best answer. You do not know what the best answer looks like, but you know that one exists.

So take a best answer and compare it with the greedy one. Where they differ, change the best answer a little, so that it agrees more with the greedy one. Then check two things: the changed answer is still allowed, and it is not worse.

Repeat. Each change makes the two answers more alike, so after a finite number of changes the best answer has become the greedy answer, and it never got worse on the way. So the greedy answer is as good as the best one.

## When it applies

- The greedy solution and any other solution can be compared piece by piece: as orders of the same jobs, as sets of the same size, or as trees with the same leaves.
- A small local change, such as swapping two adjacent jobs, replacing one element by another or exchanging two leaves, has an effect on the cost that can be computed from the two pieces alone.
- There is a measure of disagreement with the greedy solution, such as the number of [inversions](/inversion/) or the first position of difference, that each change reduces.

Exchange arguments fit objectives that are sums or maxima over pieces, where a local change touches only a few terms. They are less natural when the greedy solution and the optimum have different numbers of pieces; there, [greedy stays ahead](/greedy-stays-ahead/) is often easier.

## The template

```pseudo id=main
EXCHANGE-PROOF(G, cost)                 ▷ G: the greedy solution
L1  let O be an optimal solution                           ▷ exists for finite problems
L2  while O ≠ G do
L3      find a difference d between O and G                ▷ hole: what a difference is
L4      let O' be O with one exchange that removes d       ▷ hole: the exchange
L5      show O' is feasible                                ▷ hole: feasibility
L6      show cost(O') ≤ cost(O)                            ▷ hole: the local cost change
L7      show disagree(O') < disagree(O)                    ▷ hole: a measure that decreases
L8      O ← O'
L9  conclude cost(G) ≤ cost of the first O, so G is optimal
```

**The holes.** Line L3 is often "an adjacent pair in the wrong order" or "the first position where $O$ and $G$ differ". Line L4 swaps the pair, or replaces the element of $O$ at that position by the element of $G$. Line L6 is the core: a short computation of how the cost changes, using only the pieces that moved. Line L7 guarantees that the loop ends; with adjacent swaps of inverted pairs the number of inversions drops by exactly one.

**Two endings.** If the greedy rule has ties, the loop may reach a different solution with the same greedy key rather than $G$ itself. Then add one more step: all solutions that satisfy the greedy rule have the same cost. The [minimizing maximum lateness](/minimizing-maximum-lateness/) proof has this step, because jobs with equal due dates can be in any order.

**Single-step form.** To prove the greedy-choice property, run the loop body once: from an optimal $O$ that does not contain the greedy choice, build an optimal $O'$ that does. Optimal substructure and induction then finish the proof.

## Classic examples

- **[Smith's rule](/smith-rule/) for $1 \| \sum w_j C_j$.** Difference: an adjacent pair $a, b$ with $w_a / p_a < w_b / p_b$. Exchange: swap them. Cost change: exactly $w_a p_b - w_b p_a < 0$. Measure: inversions.
- **[Earliest due date](/minimizing-maximum-lateness/) for $1 \| L_{\max}$.** Difference: an adjacent pair with $d_a > d_b$. After the swap, $b$ finishes earlier and $a$ finishes when $b$ used to, with a later due date, so the maximum lateness does not grow.
- **[Optimal tape storage](/optimal-tape-storage/).** The same adjacent swap with lengths and access frequencies.
- **[Huffman coding](/huffman-coding/).** Difference: the two least frequent symbols are not siblings at the deepest level. Exchange: swap them with two deepest siblings. Cost change: each swap moves a smaller frequency down and a larger one up, which does not increase the total.
- **[Fractional knapsack](/fractional-knapsack/).** Difference: some weight is given to a lower-ratio item while a higher-ratio item is not full. Exchange: move that weight. Cost change: the value does not decrease.
- **[Cut property](/cut-property/) of minimum spanning trees.** Difference: a tree $T$ does not contain the lightest edge $e$ across a cut. Exchange: add $e$ to $T$, which closes a cycle that crosses the cut at another edge $f$, and remove $f$. Cost change: $w(e) - w(f) \le 0$.
- **[Optimal caching](/belady-algorithm/).** Kleinberg and Tardos prove that evicting the item requested farthest in the future is optimal by an exchange argument on eviction schedules, changing an optimal schedule to agree with the greedy one for one more step at a time.

## Variations

- **Adjacent swaps and inversions.** For orderings, exchange only adjacent elements; the number of inversions is the measure, and at most $\binom{n}{2}$ swaps are needed.
- **First difference.** For sets or sequences built step by step, take the first step where $O$ and $G$ differ and make $O$ agree there. The measure is the length of the common prefix.
- **Continuous exchange.** For fractional problems, move an amount $\varepsilon$ from one variable to another. The fractional knapsack proof by a dual value $r$ is a compact form of this.
- **Matroid exchange.** The exchange property of a [matroid](/matroid/) supplies the exchange in line L4 for all problems of this kind at once; the [matroid greedy theorem](/matroid-greedy-theorem/) is an exchange argument done once in general.
- **Normal forms.** An exchange argument can also show that some optimal solution has a simple form, for example no idle time, before the main greedy argument. Removing idle time from a schedule is such an exchange.

## Pitfalls

- **An exchange that breaks feasibility.** In problems with deadlines, release dates or precedence, a swap can create a late job or violate an order. Line L5 must be checked, not assumed.
- **No decreasing measure.** Without line L7, the changes can cycle. State what gets smaller.
- **Proving the wrong direction.** The argument must start from an arbitrary optimal solution, not from the greedy one. Starting from $G$ and showing that changes make it worse proves only local optimality.
- **Ties.** If $\mathrm{cost}(O') = \mathrm{cost}(O)$ is allowed, as it must be, the proof shows that some solution with the greedy key is optimal. If several orders share the key, show that they all have the same cost.
- **Local change with global effect.** Swapping two non-adjacent jobs moves every job between them. Use adjacent swaps, whose effect is local.

## Exercises

1. Prove by an adjacent exchange that shortest processing time first minimizes $\sum_j C_j$ on one machine.
2. Show by an exchange that some minimum spanning tree contains a lightest edge of the whole graph.
3. With release dates, show that the earliest due date order can be worse than another order for the maximum lateness. Which line of the template fails?
4. Jobs have lengths $p_j$ and must all run on one machine; the cost of job $j$ is $w_j$ times its start time. Find the optimal order and prove it by an exchange.

## References
