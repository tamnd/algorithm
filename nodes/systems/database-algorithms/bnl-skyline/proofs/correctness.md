---
title: BNL outputs each skyline tuple exactly once, stops, and tests each pair of tuples at most once
proves: [correctness, termination, complexity]
status: full
---

Setting. The input is a finite sequence of $n$ tuples in $\mathbb{R}^d$, told apart by position, so equal tuples are different items. Tuple $p$ *dominates* $q$, written $p \prec q$, if $p_i \le q_i$ for all $i$ and $p_i < q_i$ for some $i$. This relation is irreflexive and transitive. The skyline is the set of tuples that no tuple dominates. The window holds at most $w \ge 1$ tuples. A global clock gives each insertion into the window (line L8) and each write to the temporary file a distinct, increasing timestamp; tuples of the original input have timestamp $-1$. *Pass* $j$ scans the source $F_j$ ($F_1$ is the input, $F_{j+1}$ is the temporary file $T_j$ written in pass $j$) in order. Let $f_j$ be the timestamp of the first write in pass $j$, or $\infty$ if there is none.

We say that $p$ is *scanned against* $q$ if $p$ is processed at lines L6 and L7 while $q$ is in the window.

**Lemma 1 (window).** The window is always an antichain: no window tuple dominates another. A tuple is dropped at line L6 or removed at line L7 only if some tuple dominates it.

*Proof.* A tuple $p$ enters the window only if the loop of line L6 ran to the end, so no window tuple dominates $p$, and line L7 removed each window tuple that $p$ dominates. The second claim is the text of lines L6 and L7. $\square$

**Lemma 2 (a scan decides the pair).** If $p$ is scanned against $q$ and both $p$ and $q$ are output, then neither dominates the other.

*Proof.* If $q \prec p$, the loop either stops at an earlier window tuple, which also dominates $p$, or reaches $q$; in both cases $p$ is dropped and is never output. If $p \prec q$, the loop either reaches $q$ and removes it, or stops earlier at a window tuple $u \prec p$; then $u \prec q$ by transitivity, and $u$ and $q$ are both in the window, against Lemma 1. A removed tuple is never output. $\square$

**Lemma 3 (when a window tuple leaves).** Let $q$ enter the window in pass $j$ at time $t_q$. During pass $j$, $q$ is not output. If $f_j > t_q$, $q$ is output at the end of pass $j$ unless removed. Otherwise, $q$ stays in the window into pass $j + 1$ and is output, unless removed, at line L5 just before the first source tuple with timestamp larger than $t_q$, or at the end of pass $j + 1$.

*Proof.* Source tuples of pass $j$ were written in pass $j - 1$ (or are input tuples) and so have timestamps less than $t_q$; line L5 outputs only window tuples with a smaller timestamp than the scanned tuple. Line L9 outputs $q$ exactly when $t_q < f_j$. In pass $j + 1$, line L5 outputs $q$ at the first source tuple with a larger timestamp. At the end of pass $j + 1$, every write of that pass is later than $t_q$, so line L9 outputs $q$ if it is still there. $\square$

**Lemma 4 (output tuples meet).** If $q$ and $s$ are both output and $q \ne s$, then one of them is scanned against the other.

*Proof.* Let $s$ enter the window at time $t_s$ in pass $j_s$, and $q$ at time $t_q > t_s$ in pass $j_q \ge j_s$. In pass $j_s$, $q$ is processed either after time $t_s$ or before it.

If after, $s$ is in the window then, by Lemma 3 (it is not output during pass $j_s$, and it is not removed since it is output later). So $q$ is scanned against $s$.

If before, $q$ did not enter the window then (it enters at $t_q > t_s$), and it was not dropped, so it was written to $T_{j_s}$ at a time $u < t_s$. Then $f_{j_s} \le u < t_s$, so by Lemma 3 $s$ stays in the window into pass $j_s + 1$ and leaves only at a source tuple with timestamp larger than $t_s$, or at the end. The source of pass $j_s + 1$ is $T_{j_s}$ in order of timestamps, and $q$ has timestamp $u < t_s$, so $q$ is processed in pass $j_s + 1$ while $s$ is still in the window. $\blacksquare$

**Lemma 5 (termination).** Each pass removes at least one tuple for good (by output or by drop or removal), so BNL stops after at most $n$ passes, and every tuple that is never dropped or removed is output exactly once.

*Proof.* Call a tuple *live* at the start of pass $j + 1$ if it is in $F_{j+1}$ or in the window. The window tuples carried into pass $j + 1$ all leave during that pass, by Lemma 3. If none are carried, the window is empty at the start of pass $j + 1$, so the first source tuple enters it before any write of that pass; by Lemma 3 it leaves during pass $j + 1$. Every other source tuple is dropped, enters the window, or is written to $T_{j+1}$. So the number of live tuples drops in every pass that has a nonempty source. When the source is empty the loop stops, and the last pass had no writes, so line L9 empties the window. A tuple leaves the window only once, so it is output at most once. $\square$

**Theorem 1 (correctness).** BNL outputs each skyline tuple exactly once and no other tuple.

*Proof.* A skyline tuple is never dropped or removed (Lemma 1), so it is output exactly once (Lemma 5). Suppose an output tuple $q$ is dominated. The set of tuples that dominate $q$ is finite and nonempty; let $s$ be a minimal one under $\prec$. If some $u \prec s$, then $u \prec q$, against minimality, so $s$ is in the skyline and is output. By Lemma 4, one of $q$ and $s$ is scanned against the other, and by Lemma 2 neither dominates the other, a contradiction. $\blacksquare$

**Theorem 2 (cost).** Each unordered pair of tuples is tested for dominance at most once, so BNL makes at most $n(n - 1)/2$ dominance tests, each in $O(d)$ time: $O(d n^2)$ time in total. Each pass reads its source once and writes at most that many tuples, so the I/O is at most $n$ tuples read and $n$ written per pass.

*Proof.* A test of $p$ against $q$ happens when $p$ is scanned against $q$. Suppose $p$ is scanned against $q$ in pass $j$. If $q$ entered the window in pass $j$, then $p$ is processed after $q$ in pass $j$; if $p$ is written, its timestamp is larger than $t_q$, so in pass $j + 1$ the tuple $q$ leaves (Lemma 3) before $p$ is processed. If $q$ entered in pass $j - 1$, then $q$ leaves the window before the end of pass $j$. Either way $p$ is scanned against $q$ at most once. And $q$ cannot also be scanned against $p$: whichever of the two entered the window first was processed for the last time before the other entered. $\blacksquare$
