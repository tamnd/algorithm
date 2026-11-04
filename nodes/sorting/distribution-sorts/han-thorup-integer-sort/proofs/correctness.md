---
title: The Han-Thorup splitter recursion returns its input in sorted order, whatever its random choices
proves: [correctness, termination]
status: full
---

We prove the claim for the recursion of the pseudocode, as the model runs it: line L6 draws at most three new samples, and then it accepts the last one. The claim holds for every outcome of the random choices, so the algorithm is Las Vegas.

**Claim.** For each finite list $A$ of integers and each sequence of random choices, HAN-THORUP-SORT$(A)$ returns the keys of $A$, with their counts, in non-decreasing order.

*Proof.* Induction on $n = |A|$.

**Base.** If $n \le c$, line L1 returns the result of insertion sort.

**Step.** Let $n > c \ge 2$, and assume the claim for all lists with fewer than $n$ keys and all random choices. The loop of lines L3 to L6 runs at most four times, so it ends. Consider the sample that it accepts. It has $k = \lceil \sqrt{n} \rceil < n$ keys, all drawn from $A$, so by the hypothesis line L4 returns it sorted, and the splitters $p_1 < \cdots < p_s$, with $s \ge 1$, are keys of $A$.

*Each key goes to exactly one set.* With $p_0 = -\infty$ and $p_{s+1} = +\infty$, a key $x$ is either equal to exactly one $p_j$, and goes to $E_j$, or lies strictly between $p_j$ and $p_{j+1}$ for exactly one $j \in \{0, \ldots, s\}$, and goes to $B_j$. So the sets split the keys of $A$ with their counts.

*Each part is smaller.* No key of a part $B_j$ equals $p_1$, and $p_1$ is a key of $A$. So $|B_j| < n$, and by the hypothesis line L7 sorts each $B_j$ correctly.

*The order.* All keys of $B_{j-1}$ are less than $p_j$, all keys of $E_j$ equal $p_j$, and all keys of $B_j$ are greater than $p_j$. So in the order $B_0, E_1, B_1, \ldots, E_s, B_s$ each key of a set is less than each key of a later set. Inside $E_j$ the keys are equal, and inside $B_j$ they are sorted. So the output of line L8 is non-decreasing, and it holds the keys of $A$ with their counts.

*Termination.* Each call runs a bounded loop and then calls itself only on lists with fewer keys, so every run ends, for every sequence of random choices. $\blacksquare$
