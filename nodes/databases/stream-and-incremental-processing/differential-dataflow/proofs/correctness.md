---
title: Differential reachability stores exactly the differences of every iterate at every time
proves: [correctness, termination]
status: full
---

We use the line numbers of the pseudocode on the page. Times are pairs $t = (e, i)$ of an epoch and an iteration, with the product order $(e_1, i_1) \le (e_2, i_2)$ if and only if $e_1 \le e_2$ and $i_1 \le i_2$. Any two times have a least upper bound $s \vee u = (\max(e_s, e_u), \max(i_s, i_u))$. A *trace* $\delta$ maps times to signed bags, nonzero at finitely many times, and its *accumulation* is $X(t) = \sum_{s \le t} \delta[s]$.

**The program.** The inputs after epoch $e$ are $\mathit{roots}_e$ and $\mathit{edges}_e$, bags with nonnegative weights. The iterates are $R_{e,0} = \mathrm{distinct}(\mathit{roots}_e)$ and $R_{e,i+1} = \mathrm{distinct}(\mathit{roots}_e + \mathrm{dst}(R_{e,i} \bowtie \mathit{edges}_e))$, where $\mathrm{dst}(F \bowtie E)$ has, for each node $b$, the weight $\sum_{(a, b)} F[a] \cdot E[(a, b)]$. We must show that after epoch $E$ has been processed, the trace of R has accumulation $R_{e,i}$ at every time $(e, i)$ with $e \le E$.

**Lemma 1 (uniqueness of differences).** For every function $X$ from times to signed bags with $X(e, i) = 0$ when $e < 0$ or $i < 0$, there is exactly one trace with accumulation $X$, namely

$$\delta[e, i] = X(e, i) - X(e - 1, i) - X(e, i - 1) + X(e - 1, i - 1).$$

If the values $\delta[s]$ for $s \le t$, $s \ne t$, are known, then $\delta[t] = X(t) - \sum_{s \le t,\ s \ne t} \delta[s]$.

*Proof.* The second statement is the definition of the accumulation at $t$ solved for $\delta[t]$. It fixes each $\delta[t]$ by induction along any order that lists the times below $t$ first, which gives uniqueness. The formula has accumulation $X$, because the sum over the rectangle below $(e, i)$ telescopes. $\square$

**Lemma 2 (inputs).** Line L1 adds the change of epoch $e$ at time $(e, 0)$. So the accumulations of the input traces at $(e, i)$ are $\mathit{roots}_e$ and $\mathit{edges}_e$, for every $i$.

*Proof.* The times $(e', 0)$ below $(e, i)$ are those with $e' \le e$, and the changes of epochs $0$ to $e$ add up to the inputs after epoch $e$. $\square$

**Lemma 3 (join).** Let $F$ and $E$ be traces with accumulations $F(t)$ and $E(t)$. The trace $J[r] = \sum_{s \vee u = r} \mathrm{dst}(F[s] \bowtie E[u])$ of line L4 has accumulation $\mathrm{dst}(F(t) \bowtie E(t))$.

*Proof.* $\mathrm{dst}(\cdot \bowtie \cdot)$ is bilinear, so $\mathrm{dst}(F(t) \bowtie E(t)) = \sum_{s \le t} \sum_{u \le t} \mathrm{dst}(F[s] \bowtie E[u])$. And $s \le t$ and $u \le t$ hold together exactly when $s \vee u \le t$. Grouping the pairs by $r = s \vee u$ gives $\sum_{r \le t} J[r]$. $\square$

**Lemma 4 (feedback).** Line L3 sets $\mathit{fed}[(e, i)] = R[(e, i - 1)]$ for $i \ge 1$ and leaves $\mathit{fed}[(e, 0)] = 0$. If $R$ has accumulation $R(e, i)$, then $\mathit{fed}$ has accumulation $R(e, i - 1)$ at $(e, i)$, and 0 at $(e, 0)$.

*Proof.* The times $(e', i')$ below $(e, i)$ with $i' \ge 1$ correspond one to one to the times $(e', i' - 1)$ below $(e, i - 1)$. $\square$

**Lemma 5 (closure).** Let $U$ be a trace, $C$ the closure of its support under $\vee$, and $f$ any function on signed bags with $f(0) = 0$. The unique trace $\rho$ with accumulation $f(U(t))$ is 0 outside $C$.

*Proof.* Let $t = (e, i) \notin C$, and let $P$ be the support times below $t$. If $P$ is empty, $U$ is 0 at $t$ and at the three times below it in Lemma 1, so $\rho[t] = 0$. Otherwise let $t^* = \bigvee P \in C$. Then $t^* \le t$ and $t^* \neq t$. If $t^*$ has iteration below $i$, every support time below $t$ is also below $(e, i - 1)$, and every support time below $(e - 1, i)$ is below $(e - 1, i - 1)$. So $U(e, i) = U(e, i - 1)$ and $U(e - 1, i) = U(e - 1, i - 1)$, and the four terms of Lemma 1 for $f \circ U$ cancel. If $t^*$ has iteration $i$, its epoch is below $e$, and the same argument with the roles of the coordinates exchanged applies. $\square$

**Lemma 6 (distinct).** Lines L6 to L8 store, at every processed time $t$, the value $\rho[t]$ of the unique trace with accumulation $\mathrm{distinct}(U(t))$, provided that the traces are already correct at all times $s \le t$ with $s \ne t$.

*Proof.* Line L6 keeps the closure $C$ of the support of $U$: adding a time $t$ to a set closed under $\vee$ and adding $t \vee c$ for every $c$ in it gives a closed set again, because $(t \vee c_1) \vee (t \vee c_2) = t \vee (c_1 \vee c_2)$. Every time added is $\ge t$, so it is processed later or now. If $t \in C$, line L8 computes $\mathrm{distinct}(U(t)) - \sum_{s \le t,\ s \ne t} R[s]$, which is $\rho[t]$ by Lemma 1. If $t \notin C$, nothing is stored, and $\rho[t] = 0$ by Lemma 5. $\square$

**Lemma 7 (stopping).** Let $i_{\max}$ be the largest iteration of a time with a nonzero difference before epoch $e$. If, in epoch $e$, $i > i_{\max}$ and $R[(e, i - 1)] = 0$, then every trace is 0 at every time $(e, j)$ with $j \ge i$, so line L2 may stop.

*Proof.* By induction on $j$. At $(e, j)$, line L3 adds $R[(e, j - 1)]$, which is 0. A join pair with $s \vee u = (e, j)$ needs $s$ with iteration $j$, because the edge differences have iteration 0; a time of an earlier epoch has iteration at most $i_{\max} < j$, and $\mathit{fed}[(e, j)] = 0$. So the join and the union are 0 at $(e, j)$. A time of $C$ with iteration $j$ would be a least upper bound of support times of $U$, one of which has iteration $j$; there is none. So $R[(e, j)] = 0$ by Lemma 6. $\square$

**Theorem 1 (correctness).** After epoch $E$ is processed, each trace holds its unique differences at every time $(e, i)$ with $e \le E$, and the accumulation of the trace of R at $(e, i)$ is $R_{e,i}$.

*Proof.* The times are processed in lexicographic order, epoch first, which lists every $s \le t$ with $s \ne t$ before $t$. The times that are skipped after the stop of an epoch hold 0 in every trace, by Lemma 7. So, by induction along this order, Lemmas 2, 3, 4 and 6 apply at every time with all earlier times correct. Then the union at $(e, i)$ accumulates to $\mathit{roots}_e + \mathrm{dst}(R(e, i - 1) \bowtie \mathit{edges}_e)$, or to $\mathit{roots}_e$ for $i = 0$, and R accumulates to its distinct, which is the definition of $R_{e,i}$. $\blacksquare$

**Termination.** For a fixed epoch, $R_{e,0} \subseteq R_{e,1}$, and the step from $R_{e,i}$ to $R_{e,i+1}$ is monotone, so $R_{e,i} \subseteq R_{e,i+1}$. With $n$ nodes, the iterates of every epoch are constant from $i = n$ on. Then the four terms of Lemma 1 cancel for every time $(e, i)$ with $i > n$, and the condition of Lemma 7 holds for some $i \le \max(i_{\max}, n) + 2$. Each time costs a finite scan of the traces.
