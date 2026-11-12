---
title: SSTF serves a nearest request at each step, is not optimal, and can starve a request
proves: [correctness]
status: full
---

We use the pseudocode of the page. $A[0..n-1]$ is the sorted batch, indices run from 0, and $A[k]$ for $k < 0$ or $k \ge n$ does not exist. The *pending* requests are those not yet in `out`.

**Claim 1 (invariant).** Before each test of line L4:

1. the requests in `out` are exactly $A[i+1..j-1]$, and the pending requests are $A[0..i]$ and $A[j..n-1]$;
2. if $i \ge 0$ then $A[i] \le p$, and if $j < n$ then $p \le A[j]$.

*Proof.* At the start, `out` is empty and $j = i + 1$, so part 1 holds. Line L2 sets $i$ so that $A[i] < r$ and $A[j] \ge r$, and $p = r$, so part 2 holds. Suppose the claim holds and line L7 runs. It appends $x = A[j]$ and sets $j \leftarrow j + 1$, so part 1 holds again. The new head is $p' = A[j_{\text{old}}]$. Then $A[i] \le p \le p'$, and $p' \le A[j_{\text{old}} + 1]$ because $A$ is sorted, so part 2 holds. Line L8 is the mirror case. $\square$

**Claim 2 (greedy choice).** Each run of lines L5 to L8 serves a pending request at least distance from $p$, and among two such requests on both sides of $p$ it serves the one in the direction of the last move (at the start, of $d$).

*Proof.* By Claim 1, every pending request below or at $p$ is at most $A[i]$, so its distance to $p$ is at least $p - A[i] = dl$. Every pending request above or at $p$ is at least $A[j]$, so its distance is at least $A[j] - p = du$. So the least distance over the pending requests is $\min(dl, du)$, and it is reached at $A[i]$ or $A[j]$. Line L7 takes $A[j]$ when $du < dl$ and line L8 takes $A[i]$ when $dl < du$. When $du = dl$, line L7 takes $A[j]$ exactly when $d = +1$. Line L9 sets $d$ to the sign of each move of nonzero length, and a move of length 0 does not change the side of any other request, so $d$ is the direction of the last real move, or the start direction if there was none. $\square$

**Claim 3 (termination and output).** The loop runs $n$ times and `out` is a permutation of $R$.

*Proof.* Each run increases $j - i$ by one. It starts at 1 and the loop stops when $i < 0$ and $j \ge n$, that is, when $j - i = n + 1$. By Claim 1, `out` is then $A[0..n-1]$ in some order, which is $R$. $\square$

Claims 2 and 3 show that the output is the SSTF order, defined as: at each step serve a nearest pending request, with the tie rule above. They also give the run property: the served requests always form a contiguous run of $A$, and $p$ is one end of the run.

**Claim 4 (not optimal).** SSTF does not always give the least total head movement.

*Proof.* Let $r = 50$ and $R = \{46, 53, 58\}$. From 50 the distances are 4 and 3, so SSTF serves 53. From 53 they are 7 and 5, so it serves 58, then 46. Its movement is $3 + 5 + 12 = 20$. The order 46, 53, 58 moves $4 + 7 + 5 = 16$. This matches the formula $M_{\min} = (hi - lo) + \min(|r - lo|, |r - hi|) = 12 + 4$ of the [disk scheduling](/disk-scheduling/) page. $\square$

For a family, let $r = 10$, and let $R$ hold 8 and the chain $11, 13, \ldots, t$ with $t \ge 13$ odd. From 10, the request 11 is at distance 1 and 8 at distance 2, so SSTF goes up. From each chain element $c < t$, the next one is at distance 2 and 8 is at distance $c - 8 \ge 3$, so SSTF climbs to $t$ and then goes to 8. It moves $(t - 10) + (t - 8) = 2t - 18$. The formula gives $M_{\min} = (t - 8) + 2 = t - 6$. The ratio $(2t - 18)/(t - 6)$ tends to 2.

**Claim 5 (unbounded wait).** In the dynamic model with service time 0, for each bound $B$ there is a finite arrival stream in which some request waits more than $B$ ticks under SSTF.

*Proof.* Take $C = 200$, the head at 100, a request $q$ at cylinder 0 that arrives at tick 0, and one request at cylinder 100 that arrives at each tick $0, 1, \ldots, k - 1$, with $k = B$. We show by induction that at each tick $t \le k$ the head is at 99 or 100 and $q$ is pending. At tick 0 the head is at 100. Suppose it holds at tick $t < k$. If the head is at 100, it serves all requests at 100, and only $q$ is left, so it moves to 99 at tick $t + 1$. If the head is at 99, then $t \ge 1$ and the request that arrived at tick $t$ at cylinder 100 is pending. It is at distance 1, and $q$ is at distance 99, so the head moves to 100 at tick $t + 1$. In both cases $q$ is not served, since the head never reaches cylinder 0. At tick $k$ the head is at 99 or more, so it needs at least 99 more ticks to reach $q$. The wait of $q$ is at least $k + 99 > B$. $\square$

The tests run this stream and get the wait $k + 100$ for $k = 10, 100, 1000$. If the stream at cylinder 100 never ends, $q$ is never served.
