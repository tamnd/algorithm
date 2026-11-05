---
title: Decoding the WebGraph stream recovers every successor list
proves: [correctness, termination]
status: full
---

We use the pseudocode and the format of the page. The input is $n$ sorted lists $S_0, \ldots, S_{n-1}$ of distinct integers, a window $W \ge 0$ and $L_{\min} \ge 1$.

**Claim.** DECODE(ENCODE$(S, W, L_{\min})$, $L_{\min}$) returns $S_0, \ldots, S_{n-1}$.

**Step 1 (the codes).** The gamma code is prefix-free: $\gamma(k)$ is $z$ zeros followed by the $z + 1$ bits of $k + 1$, which start with 1, so a reader counts the zeros and then knows the length. So reading a field returns the value written, and the reader stops at the end of the field. The map $\nu$ is a bijection from the integers to the naturals, with inverse $\nu^{-1}(k) = k/2$ for even $k$ and $-(k+1)/2$ for odd $k$. So every field written as $\gamma(k)$ or $\gamma(\nu(z))$ is read back as $k$ or $z$, provided $k \ge 0$, which Steps 3 and 4 check.

**Step 2 (induction on $x$).** We show that after the decoder has read the part of list $x$, it holds $S_0, \ldots, S_x$ and stands at the start of the part of list $x + 1$. The base is the field $\gamma(n)$. Assume the claim for all lists before $x$. The decoder reads $d = |S_x|$; if $d = 0$ the encoder wrote nothing else (line L1), and the list is empty. Otherwise it reads $r^*$ (line L4). If $r^* > 0$, then $1 \le r^* \le x$ by line L2, and by the hypothesis the decoder holds $R = S_{x - r^*}$.

**Step 3 (copy blocks).** Let $c_0, c_1, \ldots, c_b$ be the runs of the mask of $R$, alternating 1s and 0s and starting with 1s. All runs after the first are non-empty, because a run ends only where the next bit differs. The encoder wrote $b$, then $c_0 \ge 0$ and $c_j - 1 \ge 0$ for $1 \le j < b$; it omitted $c_b$. The decoder rebuilds $c_0, \ldots, c_{b-1}$, walks through $R$ with them, keeping the elements of the runs of 1s, and gives the rest of $R$, which is exactly run $c_b$, the kind that comes next in the alternation. So it obtains the copied set $C = S_x \cap R$.

**Step 4 (intervals and residuals).** Let $E = S_x \setminus C$, sorted. Line L7 cuts $E$ into maximal runs of consecutive integers; the runs of length $\ge L_{\min}$ are the intervals $[a_1, e_1), \ldots, [a_t, e_t)$, and the other elements are the residuals $y_1 < \cdots < y_s$. Since the runs are maximal and $E$ is sorted, $a_{j+1} \ge e_j + 1$: if $a_{j+1} = e_j$, the integer $e_j$ would extend run $j$. So the fields $a_{j+1} - e_j - 1$ and $\lambda_j - L_{\min}$ are $\ge 0$, and the decoder rebuilds each interval from the previous end. Since the residuals are distinct and sorted, $y_{j+1} - y_j - 1 \ge 0$. The decoder knows $s = d - |C| - \sum_j \lambda_j$, reads $s$ residuals, the first as $x + \nu^{-1}(\cdot)$ and each next one as the previous plus $1$ plus the field.

**Step 5 (the list).** $C$, the intervals and the residuals are disjoint and their union is $S_x$, by the definitions of $C$ and $E$ and because the runs partition $E$. So sorting their union gives $S_x$, and the decoder has read exactly the fields written for $x$ and stands at the start of the part of $x + 1$. This completes the induction.

**Termination.** The encoder runs a loop over $x$ with inner loops over finite lists. The decoder reads one field per field written, and each read consumes at least one bit, so it stops after reading the whole string. $\blacksquare$
