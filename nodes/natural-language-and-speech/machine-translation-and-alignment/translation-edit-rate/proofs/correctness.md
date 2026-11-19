---
title: Greedy TER terminates and returns the cost of a valid edit sequence, between the fewest edits and the plain edit distance
proves: [correctness]
status: full
---

Fix a hypothesis $h$ and a reference $r$, lists of words. The edits are the insertion, the deletion and the substitution of one word, and the shift of a block: a run of consecutive words of $h$ moved to another place. Each costs 1. Let $\mathrm{ED}(a, b)$ be the word edit distance (insertions, deletions and substitutions only), and let $\mathrm{OPT}(h, r)$ be the least cost of a sequence of edits of the four kinds that turns $h$ into $r$. Let $d_0 = \mathrm{ED}(h, r)$.

**Lemma 1 (the edit distance).** EDIT-DISTANCE of lines L4, L7 and L11 returns $\mathrm{ED}(a, b)$, and the words it flags as correct form a common subsequence of $a$ and $b$ that is matched in order.

*Proof.* The table is the one of the [Wagner-Fischer algorithm](/wagner-fischer-algorithm/), whose correctness gives $d[n][m] = \mathrm{ED}(a, b)$. The traceback moves from $(n, m)$ to $(0, 0)$, and every step goes to a cell whose value plus the cost of the step equals the current value, so the steps form an optimal alignment. A word pair is flagged correct only on a diagonal step with equal words. The diagonal steps of a path from $(n, m)$ to $(0, 0)$ have strictly decreasing $i$ and $j$, so the flagged words are matched in order. $\square$

**Lemma 2 (termination).** Let $d_t$ be the edit distance after $t$ shifts. Every round that applies a shift has $d_t \le d_{t-1} - 1$. Hence the loop of lines L5 to L11 ends after at most $d_0$ shifts.

*Proof.* Line L9 leaves the loop unless the chosen shift has a gain $d_{t-1} - d_t \ge 1$, and line L10 applies only that shift. The values $d_t$ are non-negative integers that drop by at least 1 per applied shift, so at most $d_0$ shifts are applied. Each round itself is finite: there are finitely many blocks $(i, k)$ and destinations $p$. $\square$

**Theorem.** For one reference, let $s$ be the number of shifts applied, $h'$ the final hypothesis and $e = s + \mathrm{ED}(h', r)$ the value used at line L12. Then

$$\mathrm{OPT}(h, r) \le e \le \mathrm{ED}(h, r).$$

With several references, line L12 keeps the least $e$, and lines L13 to L15 divide it by the mean reference length (with the stated rule for a length of 0).

*Proof.* The lower bound: applying the $s$ shifts in order turns $h$ into $h'$, and an optimal alignment of $h'$ and $r$ gives $\mathrm{ED}(h', r)$ word edits that turn $h'$ into $r$. Together these are a sequence of $e$ edits of the allowed kinds from $h$ to $r$, so $\mathrm{OPT}(h, r) \le e$.

The upper bound: by Lemma 2, $d_s \le d_0 - s$ by induction on the number of shifts. So $e = s + d_s \le s + d_0 - s = d_0$.

The rest of lines L1 to L15 takes a minimum over the references and divides by a positive number, or returns the fixed value of line L14. $\square$

**Remark (the bound is not tight).** For $h$ = "a a b b" and $r$ = "b c c a", $\mathrm{ED}(h, r) = 4$. One shift of the block "b b" to the front gives "b b a a", at edit distance 2 from $r$, so $\mathrm{OPT} \le 3$. The greedy search may shift only blocks that occur in $r$, and "b b" and "a a" do not. It shifts "a" to the end and then "b" to the front, and returns $e = 2 + 2 = 4$. The tests find $\mathrm{OPT} = 3$ by trying all sequences of shifts. In general no polynomial algorithm for $\mathrm{OPT}$ is known: Shapira and Storer (2002) showed that edit distance with block moves is NP-complete.

**Remark (complexity).** Let $n$ be the larger of $|h|$ and $|r|$. A round tries $O(n^2)$ blocks, and for each block $O(n)$ destinations, and each try computes an edit distance in $O(n^2)$ time. So a round takes $O(n^5)$ time, and by Lemma 2 there are at most $d_0 \le n$ rounds with a shift plus one final round. The total is $O(n^6)$ time per reference and $O(n^2)$ space. Bounds on the block size and on the distance of a move, as in tercom, cut the number of tries per round.
