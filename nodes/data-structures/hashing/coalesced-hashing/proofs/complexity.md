---
title: Cost of coalesced hashing
proves: [time.worst, time.expected]
status: sketch
---

**Worst case (full proof).** A search or insert of key $k$ visits the slots of one walk from $h(k)$, and by the lemma of the correctness proof this walk has at most $n$ slots. So each search costs $O(n)$, and each insert costs $O(n)$ plus the passes of line L7. The pointer $r$ starts at $m$, only decreases, and line L7 decreases it by one at each pass, so all inserts together make at most $m + 1$ passes of line L7. For the lower bound, let all $n$ keys have the same home slot. The first key fills the home slot, and each later key is appended at the end of the one chain, so the $j$-th insert visits $j - 1$ slots of the chain, and a search for the last key visits $n$ slots. Hence the worst case of a single operation is $\Theta(n)$, plus $O(m)$ for the moves of $r$ over all inserts. $\square$

**Expected case (sketch, after Knuth, Section 6.4).** Assume that the $n$ keys have independent uniform home slots. The analysis of Algorithm C rests on two facts.

1. The chains form a set of disjoint linked lists that cover the occupied slots, and the cost of a search that fails from home slot $i$ is 1 if slot $i$ is EMPTY, and else the number of slots from $i$ to the end of the list that contains $i$.
2. A new key whose home slot lies on a list of $\ell$ slots, which happens with probability $\ell/m$, adds one slot to that list: the free slot that line L7 takes. That slot may later be the home slot of another key, and this is how two lists merge. Counting the expected number of lists of each length leads to a recurrence on $n$ that Knuth solves.

The result, as $m \to \infty$ with $n = \alpha m$, is $C'(\alpha) \approx 1 + \frac{1}{4}(e^{2\alpha} - 1 - 2\alpha)$ expected probes for a search that fails, and $C(\alpha) \approx 1 + \frac{1}{8\alpha}(e^{2\alpha} - 1 - 2\alpha) + \frac{\alpha}{4}$ for a search that succeeds. Both are at most their values at $\alpha = 1$, about 2.10 and 1.80, so the expected cost is $O(1)$ for each $\alpha \le 1$. The full derivation is in Knuth, The Art of Computer Programming, Volume 3, Section 6.4, in the analysis of Algorithm C, and the variants with a cellar are analysed in Vitter, Journal of the ACM 30(2), 1983, pages 231 to 258.
