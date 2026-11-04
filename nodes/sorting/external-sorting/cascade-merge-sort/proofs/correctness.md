---
title: Cascade merge sort sorts in l passes
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode. Let $P = T - 1 \ge 2$. The cascade distributions are $a^{(0)} = (1, 0, \ldots, 0)$ and, for $a^{(\ell)} = (a_1, \ldots, a_P)$,

$$a^{(\ell+1)} = \big(a_1 + \cdots + a_P,\ a_1 + \cdots + a_{P-1},\ \ldots,\ a_1 + a_2,\ a_1\big).$$

Let $t_\ell$ be the sum of the entries of $a^{(\ell)}$.

**Lemma 1 (shape).** $a^{(1)} = (1, \ldots, 1)$. For $\ell \ge 2$, the entries of $a^{(\ell)}$ are positive and strictly decreasing. For all $\ell$, $t_{\ell+1} > t_\ell$.

*Proof.* The first claim is the rule applied to $a^{(0)}$. If all entries of $a^{(\ell)}$ are positive, the entries of $a^{(\ell+1)}$ are sums of $P, P - 1, \ldots, 1$ leading entries, so they are positive and strictly decreasing. Also $t_{\ell+1} = \sum_{i=1}^{P} (P - i + 1) a_i \ge t_\ell + (P - 1)a_1 > t_\ell$, since $a_1 \ge 1$ and $P \ge 2$. $\blacksquare$

Lines L2 to L4 put $a_d$ runs on tape $d$, real or dummy, as on the proof page of the [polyphase merge sort](/polyphase-merge-sort/).

**Lemma 2 (one pass).** Suppose that at line L7 the output tape is empty and the other $P$ tapes hold the counts of $a^{(j)}$, $j \ge 1$, in some order. Then after the loop of line L8, one tape is empty and the other $P$ tapes hold the counts of $a^{(j-1)}$, in some order, and the next pass uses the empty tape as its output.

*Proof.* Let $a^{(j-1)} = (b_1, \ldots, b_P)$. The input tapes hold $c_i = b_1 + \cdots + b_{P-i+1}$ for $i = 1, \ldots, P$. Call the input tape with $c_i$ runs tape $i$.

If $j = 1$, all $c_i = 1$. Line L10 merges once, all input tapes become empty, and the old output holds 1 run. All other tapes are empty, so the counts are those of $a^{(0)}$ up to order. The loop of line L8 stops because no tape is active.

If $j \ge 2$, the $b_i$ are positive by Lemma 1. We show by induction on $r = 1, \ldots, P - 1$: before step $r$ of the loop of line L8, the active tapes are tapes $1, \ldots, P - r + 1$ and tape $i$ holds $c_i - (b_1 + \cdots + b_{r-1}) = b_r + \cdots + b_{P-i+1}$ runs. The smallest count is that of tape $P - r + 1$, namely $b_r$, and it is the only one equal to $b_r$, because $b_{r+1}, \ldots$ are positive. Line L10 merges $b_r$ times onto the current output, and tape $P - r + 1$ alone becomes empty. Line L12 removes it from the active tapes and makes it the next output. This proves the claim for $r + 1$.

After step $P - 1$, only tape 1 is active, with $b_P$ runs, and the loop stops. The outputs of the steps $r = 1, \ldots, P - 1$ received $b_1, \ldots, b_{P-1}$ runs. So the tapes hold $b_1, \ldots, b_P$, and the last tape that became empty, tape 2, is empty and is the output of the next pass. $\blacksquare$

**Lemma 3 (contents).** At each test of line L6, each run on a tape is sorted, and the multiset union of the runs is the multiset of the items of $F$.

*Proof.* Line L1 makes sorted runs whose union is $F$, and dummy runs are empty. Line L11 replaces some runs by their merge, which is sorted and has the same items. $\blacksquare$

**Theorem.** If $S \ge 2$, the loop of line L6 runs exactly $\ell$ times, and line L14 returns the items of $F$ in non-decreasing order.

*Proof.* By Lemma 2 and induction, after $q$ passes the tapes hold the counts of $a^{(\ell - q)}$, with one tape empty. By Lemma 1, $t_{\ell - q} > t_0 = 1$ for $q < \ell$. So the loop runs exactly $\ell$ times and ends with one run, which by Lemma 3 is sorted and holds all items of $F$. $\blacksquare$
