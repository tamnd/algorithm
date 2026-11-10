---
title: Chang-Roberts elects the largest identifier with at most n(n+1)/2 + n messages
proves: [correctness, termination, complexity]
status: full
---

**Claim.** Run CHANG-ROBERTS on an asynchronous unidirectional ring of $n \ge 1$ processes with distinct identifiers, with reliable channels that need not be FIFO. Then every run is finite. At its end the process $p_m$ with the largest identifier $u_{\max}$ has status *leader*, every other process has status *non-leader*, and every process other than $p_m$ stores $u_{\max}$ as the leader. Exactly $\sum_i h_i$ elect messages are sent, where $h_i$ is defined below, and this is at most $n(n+1)/2$. Exactly $n$ leader messages are sent. Over a uniformly random assignment of the identifiers to the processes, the expected number of elect messages is $n H_n$.

**Setup.** Indices are modulo $n$, and $p_i$ sends to $p_{i+1}$. For each $i$ let $h_i$ be the least $d \in \{1, \ldots, n-1\}$ with $u_{i+d} > u_i$, and $h_i = n$ if there is no such $d$, which happens exactly for $i = m$.

**Lemma 1 (path of an identifier).** For each $i$, the message $\langle \text{elect}, u_i \rangle$ is sent exactly $h_i$ times, once by each of $p_i, p_{i+1}, \ldots, p_{i+h_i-1}$, and it is received exactly $h_i$ times.

*Proof.* Only $p_i$ creates an elect message with value $u_i$ (line L1), because every other send of an elect message (line L4) copies the value it received. So the copies of value $u_i$ form one chain: $p_i$ sends it, and each receiver either forwards it once or does not forward it. A channel delivers each message exactly once. The receiver $p_{i+d}$ for $1 \le d \le n - 1$ forwards it if and only if $u_i > u_{i+d}$ (line L4), because identifiers are distinct and $u_i \ne u_{i+d}$. By the definition of $h_i$, the receivers $p_{i+1}, \ldots, p_{i+h_i-1}$ forward it and the receiver $p_{i+h_i}$ does not: either $h_i < n$ and $u_{i+h_i} > u_i$ (line L8), or $h_i = n$ and the receiver is $p_i$ itself (line L5). So the value is sent $h_i$ times. $\square$

**Lemma 2 (exactly one leader).** Line L6 runs exactly once, at $p_m$.

*Proof.* Line L6 runs at $p_j$ when $p_j$ receives $\langle \text{elect}, u_j \rangle$. By Lemma 1 the value $u_j$ reaches its owner only if $h_j = n$, which holds only for $j = m$. For $j = m$ we have $h_m = n$ since $u_m$ is the largest, so the value travels round and arrives at $p_m$ once. $\square$

**Lemma 3 (announcement).** Exactly $n$ leader messages are sent. Each $p_i \ne p_m$ receives $\langle \text{leader}, u_{\max} \rangle$ once, sets status *non-leader* and stores $u_{\max}$.

*Proof.* The only process that creates a leader message is $p_m$ (line L7), once by Lemma 2. A process $p_i \ne p_m$ forwards it (lines L10 and L11) because $u_{\max} \ne u_i$. The process $p_m$ drops it (line L12). So the message passes $p_{m+1}, \ldots, p_{m+n-1}$, each once, and returns to $p_m$: $n$ sends in total. No other line changes the status after line L10, and line L6 does not run at $p_i$ by Lemma 2. $\square$

**Termination.** By Lemmas 1 and 3 the run sends $\sum_i h_i + n$ messages, a finite number. Each sent message is delivered after a finite delay and causes at most one send, so after the last delivery no message is in transit and no process acts again. By Lemmas 2 and 3 the statuses at that point are as claimed.

**Worst case.** Sort the identifiers and let $u_i$ have rank $k$, so exactly $k - 1$ identifiers are smaller. The processes $p_{i+1}, \ldots, p_{i+h_i-1}$ all have identifiers smaller than $u_i$ (Lemma 1), so $h_i - 1 \le k - 1$, that is $h_i \le k$. The ranks are $1, \ldots, n$, each once, so $\sum_i h_i \le \sum_{k=1}^n k = n(n+1)/2$. Equality holds when $u_i > u_{i+1}$ for all $i \ne m$. Then the $k - 1$ processes after the process of rank $k$ hold the ranks $k - 1, \ldots, 1$, so $h_i = k$ for each $i$.

**Average case.** Assign the identifiers to the processes by a uniformly random permutation. Fix the identifier of rank $n - r + 1$, that is, the one with exactly $r - 1$ larger identifiers, $1 \le r \le n$, and let $p_i$ be its process. If $r = 1$, then $h_i = n$. If $r \ge 2$, the positions $d \in \{1, \ldots, n-1\}$ of the $r - 1$ larger identifiers, seen from $p_i$ in the direction of travel, form a uniformly random subset $S$ of size $k = r - 1$ of $\{1, \ldots, N\}$ with $N = n - 1$, and $h_i = \min S$. For $1 \le j \le N$, $\min S \ge j$ holds exactly when $S \subseteq \{j, \ldots, N\}$, so

$$\Pr[\min S \ge j] = \binom{N - j + 1}{k} \Big/ \binom{N}{k}.$$

A positive integer variable $X \le N$ has $E[X] = \sum_{j=1}^{N} \Pr[X \ge j]$. With the hockey stick identity $\sum_{t=k}^{N} \binom{t}{k} = \binom{N+1}{k+1}$,

$$E[\min S] = \binom{N+1}{k+1} \Big/ \binom{N}{k} = \frac{N+1}{k+1} = \frac{n}{r}.$$

The case $r = 1$ also gives $n/r = n$. By linearity of expectation the expected number of elect messages is $\sum_{r=1}^{n} n/r = n H_n$. $\blacksquare$
