---
title: The banker's queue takes O(1) amortized time per operation, also under persistent use
proves: [time.amortized]
status: full
---

We count one unit for each step of $O(1)$ work. The *unshared cost* of an operation is the work it does outside the forcing of suspensions: it is $O(1)$ for each of EMPTY, SNOC, HEAD, TAIL and CHECK, since line L9 only builds two suspensions. The *shared cost* is the work done when a suspension runs for the first time. Memoization means that each suspension runs at most once in the whole execution, whatever the number of versions that force it.

**Costs of the suspensions.** A rotation of a front $F$ of length $m$ and a rear $R$ of length $m + 1$ makes the stream $F ⧺ \text{REVERSE}(R)$. Its cells are suspensions made one by one: the cell of index $j < m$ does $O(1)$ own work (it forces cell $j$ of $F$, which is a suspension of an older stream with its own debits, and builds the next suspension of the concatenation). The cell of index $m$ forces the end of $F$, then runs REVERSE$(R)$, which does $m + 1$ steps, and returns its first cell. The cells after index $m$ were built by REVERSE and cost nothing more. We give each suspension *debits* equal to its own work, in units: the cell $j < m$ gets 1 debit and the cell $m$ gets $m + 2$ debits (one for its own step and $m + 1$ for REVERSE). All debits of a stream are attached to it when the rotation creates it, even to cells that are built later.

**The accounting rule.** Each operation may *discharge* some debits of the version it acts on. The record of discharged debits belongs to a version: the new version inherits the record of its argument and adds the debits that the operation discharges. The rule is that a suspension may be forced by an operation on a version $Q$ only when, in the record of $Q$, all debits of that suspension are discharged. The *amortized cost* of an operation is its unshared cost plus the number of debits it discharges.

**Lemma 1 (the rule bounds the total).** If the rule holds in an execution, the total actual cost of the execution is at most the sum of the amortized costs of its operations.

*Proof.* The total actual cost is the sum of the unshared costs plus, for each suspension $s$ that runs, its own work $c(s)$. Take a suspension $s$ that runs, and the operation that first forces it, on a version $Q$. By the rule, all $c(s)$ debits of $s$ are discharged in the record of $Q$. Each entry of that record was added by one operation in the history of $Q$, and that operation counted it in its amortized cost. Distinct suspensions have distinct debits, so these discharge events are distinct for distinct $s$. So $\sum_s c(s)$ is at most the total number of discharges, and the total actual cost is at most the sum of the amortized costs. The same debit may be discharged in several histories; that only makes the bound larger, not wrong. $\square$

**The debit invariant.** For a version with front $F$ of length $\ell_f$ and rear length $\ell_r$, let $d(j)$ be the number of debits on cell $j$ of $F$ that are not yet discharged in its record, and $D(i) = \sum_{j=0}^{i} d(j)$. The invariant is

$$ \text{(D)} \qquad D(i) \le \min(2i,\ \ell_f - \ell_r) \quad \text{for each } 0 \le i < \ell_f. $$

Each operation discharges the earliest debits first: to discharge $k$ debits, take them from the cell of least index with a debit left, then the next one, and so on. If $k$ is more than the debits left, all of them are discharged. After discharging $k$ debits in this way, the new prefix sums are $D'(i) = \max(0, D(i) - k)$.

**Lemma 2.** SNOC discharges 1 debit, or 2 if it makes a rotation, and TAIL discharges 2 debits. Then (D) holds for every version.

*Proof.* EMPTY has no cells, so (D) holds. Assume (D) for the argument $Q$.

*Snoc without a rotation.* The front is the same and $\ell_r$ grows by 1, so the bound $\ell_f - \ell_r$ falls by 1 and $2i$ does not change. After the discharge of 1 debit, $D'(i) = \max(0, D(i) - 1)$. If $D(i) \ge 1$ then $D'(i) \le \min(2i, \ell_f - \ell_r) - 1 \le \min(2i, \ell_f - \ell_r - 1)$. If $D(i) = 0$ then $D'(i) = 0$, and $0 \le 2i$ and $0 \le \ell_f - (\ell_r + 1)$ because no rotation means $\ell_r + 1 \le \ell_f$.

*Tail without a rotation.* The new front is $F$ without cell 0, so the new cell $i$ is the old cell $i + 1$, and $d(0) = 0$ by (D) at $i = 0$. The new prefix sums before the discharge are $E(i) = D(i + 1)$, and $D(i + 1) \le \min(2i + 2, \ell_f - \ell_r)$. The new bound is $\min(2i, (\ell_f - 1) - \ell_r)$, which is at least $\min(2i + 2, \ell_f - \ell_r) - 2$. After the discharge of 2 debits, if $E(i) \ge 2$ then $E(i) - 2$ is within the new bound; if $E(i) < 2$ then the new prefix sum is 0, and $0 \le \min(2i, \ell_f - 1 - \ell_r)$ because no rotation means $\ell_r \le \ell_f - 1$.

*An operation with a rotation.* A rotation happens when, after the update of the lengths, $\ell_r = \ell_f + 1$. For a snoc this means $\ell_r = \ell_f$ in $Q$; for a tail it means $\ell_r = \ell_f$ in $Q$ as well, since the tail lowers $\ell_f$ by 1. In both cases (D) for $Q$ gives $D(i) \le \ell_f - \ell_r = 0$ for every $i$, so every cell of the front of $Q$ is free of debits, and so is every cell of the shorter front after a tail. The new version has the new stream of length $2m + 1$, where $m$ is the length of the old front after the operation, and $\ell_r = 0$. Its only debits are those of the rotation: $D(i) = i + 1$ for $i < m$ and $D(i) = 2m + 2$ for $m \le i \le 2m$. After the discharge of 2 debits, $D'(i) = \max(0, i - 1) \le 2i$ for $i < m$, and $D'(i) \le 2m + 1 = \ell_f - \ell_r$ for all $i$. For $i \ge m$, $D'(i) = 2m \le 2i$. So (D) holds. (When $m = 0$ the stream has one cell with 2 debits, and both are discharged.)

HEAD does not change the version, so (D) still holds for it. $\square$

**Lemma 3.** The accounting rule holds.

*Proof.* HEAD and TAIL force only the first cell of the front of their argument. By (D) at $i = 0$, $D(0) \le 0$, so that cell has no debits left. Forcing cell 0 of a rotated stream forces cell 0 of its inner front $F$, which had no debits at the rotation (proof of Lemma 2), and the cell $m$ forces the end of $F$ and REVERSE, whose debits are on cell $m$ itself. A cell of index $j > 0$ of a stream is forced only when it has become cell 0 of the front of some version, after the $j$ tails that removed the cells before it; then (D) for that version applies to it. No other operation forces a suspension. $\square$

**Theorem.** Any sequence of $k$ operations on a banker's queue, applied to any versions in any order, takes $O(k)$ time in total. So each operation takes $O(1)$ amortized time, also under persistent use.

*Proof.* Each operation has $O(1)$ unshared cost and discharges at most 2 debits, so its amortized cost is $O(1)$. By Lemma 3 the accounting rule holds, and by Lemma 1 the total actual cost is at most the sum of the amortized costs, which is $O(k)$. $\blacksquare$
