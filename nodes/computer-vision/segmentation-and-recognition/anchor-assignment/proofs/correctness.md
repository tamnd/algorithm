---
title: ASSIGN labels each anchor by the stated rule, gives every overlapped true box a positive anchor at its best IoU, and SAMPLE keeps the stated counts
proves: [correctness]
status: full
---

Let $M[i][j] = \operatorname{IoU}(A_i, G_j)$ for $n$ anchors and $m \ge 1$ true boxes, let $m_i = \max_j M[i][j]$, and let $b_j = \max_i M[i][j]$. Fix thresholds $0 \le \tau_{neg} \le \tau_{pos}$. Call anchor $i$ *best* when $M[i][j] = b_j > 0$ for some $j$.

**Claim 1 (the rule).** After ASSIGN, $\text{label}_i = 1$ exactly when $m_i \ge \tau_{pos}$ or $i$ is best. For any other anchor, $\text{label}_i = 0$ when $m_i < \tau_{neg}$ and $\text{label}_i = -1$ when $\tau_{neg} \le m_i < \tau_{pos}$. The matched box $g_i$ satisfies $M[i][g_i] = m_i$.

*Proof.* Line L3 sets every label to 0 or $-1$ by the test $m_i < \tau_{neg}$. After that, lines L5 and L6 only write the value 1. Line L5 writes it for anchor $i$ exactly when some $j$ with $b_j > 0$ has $M[i][j] = b_j$, that is, when $i$ is best. Line L6 writes it exactly when $m_i \ge \tau_{pos}$. So a label is 1 exactly when one of the two conditions holds, and any other label keeps its value from line L3. Line L2 picks $g_i$ among the $j$ with $M[i][j] = m_i$. $\square$

**Claim 2 (coverage).** Every true box $j$ with $b_j > 0$ has an anchor $i$ with $\text{label}_i = 1$ and $M[i][j] = b_j$. A true box with $b_j = 0$ makes no anchor positive through line L5.

*Proof.* Since $b_j$ is a maximum over a finite set, some anchor $i$ has $M[i][j] = b_j$, and line L5 sets its label to 1. By Claim 1 no later line sets a label to anything but 1. Line L4 skips every $j$ with $b_j = 0$. $\square$

Claim 2 does not say that $g_i = j$ for that anchor. If $M[i][k] > M[i][j]$ for another box $k$, then $g_i = k$, and box $j$ can end with no anchor whose matched box is $j$. This is the behaviour of the reference code, and the page lists it as a pitfall.

**Claim 3 (no ignored anchors without a gap).** If $\tau_{neg} = \tau_{pos}$, no anchor is ignored.

*Proof.* By Claim 1 an ignored anchor has $\tau_{neg} \le m_i < \tau_{pos}$, which is empty when the two are equal. $\square$

**Claim 4 (sampling).** Let $P$ and $N$ be the numbers of positive and negative labels before SAMPLE. After SAMPLE there are $\min(P, \lfloor fB \rfloor)$ positives and $\min(N, B - \min(P, \lfloor fB \rfloor))$ negatives, every kept label equals its old value, and every other label is $-1$.

*Proof.* Line L8 draws $\min(P, \lfloor fB \rfloor)$ distinct positives without replacement, then $\min(N, B - p)$ distinct negatives, where $p$ is the number of positives drawn. Every label that is not drawn becomes $-1$, and a drawn label is copied. So the batch has at most $B$ labels, and at most $\lfloor fB \rfloor$ of them are positive. $\square$

**SSD matching.** The SSD rule first sets every anchor to positive when $m_i$ is above its threshold, else negative, and then, for each true box $j$ in order, sets its best anchor (the first index of largest IoU) to positive and matched to $j$. So every true box whose best anchor is not taken by a later box has an anchor matched to it, and when the best anchors of all boxes are distinct, every true box has one. There is no label $-1$.

**ATSS.** For each true box, the candidates are at most $k$ anchors per level, and an anchor becomes positive for the box only if its IoU is at least the mean plus the standard deviation of the candidate IoUs and its center lies strictly inside the box. When an anchor passes for several boxes, the code keeps the box with the strictly highest IoU, and the first one on a tie. So every positive anchor has its center inside its matched box, and each box has at most $kL$ positives for $L$ levels. ATSS does not promise a positive for every box: for the candidate IoUs $1, 1, 0$ the mean plus the sample standard deviation is $2/3 + 1/\sqrt 3 \approx 1.244$, and no IoU reaches it.
