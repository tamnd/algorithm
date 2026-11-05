---
title: Sample sort is correct, and its buckets are small with high probability
proves: [correctness]
status: full
---

Let the keys be distinct. If they are not, pair each key with its input index and order the pairs by key and then by index. The pairs are distinct and sorting them sorts the keys stably, so this case reduces to distinct keys.

## Lemma 1. The output is sorted

*Proof.* Let $y_0 = -\infty$ and $y_p = +\infty$. By line L4, a key $x$ is in bucket $j = b(x)$ exactly when $y_j < x \le y_{j+1}$, because the splitters $y_1 \le \cdots \le y_{p-1}$ are sorted. So if $x$ is in bucket $j$ and $x'$ is in bucket $j' > j$, then $x \le y_{j+1} \le y_{j'} < x'$. Each bucket is sorted on line L6, so the concatenation on line L7 is sorted. Each key goes to exactly one bucket, so the output is a permutation of the input. This holds for every sample. $\square$

## Lemma 2. A large bucket leaves a run of keys with few draws

Let $g \ge 1$. Call a set of $g$ keys that are consecutive in sorted order a *run*. If some bucket has more than $g$ keys, then some run gets at most $s$ of the $ps$ draws of line L1.

*Proof.* Let bucket $j$ have more than $g$ keys, and let $W$ be its $g$ smallest keys. They are consecutive in sorted order, because the bucket holds all the keys of an interval, so $W$ is a run. Every key of $W$ is greater than $y_j$ and, since the bucket has a larger key, less than $y_{j+1}$.

Let a draw have its key in $W$. In the sorted sample $S$, its position $i$ satisfies $S[i] > y_j = S[js]$, so $i > js$ when $j \ge 1$, and $S[i] < y_{j+1} = S[(j+1)s]$, so $i < (j+1)s$ when $j \le p - 2$. For $j = 0$ the positions are less than $s$, and for $j = p - 1$ they are greater than $(p-1)s$ and less than $ps$. In each case the positions lie in a set of at most $s$ integers, so at most $s$ draws have their key in $W$. $\square$

## Theorem. Bucket bound

Let $p \ge 2$ and $g = \lceil 2n/p \rceil \le n$. With probability at least $1 - n e^{-s/4}$, every bucket has at most $g$ keys. For $s \ge 12 \ln n$, the probability is at least $1 - n^{-2}$.

*Proof.* Fix one run $W$ of $g$ keys. Each draw falls in $W$ with probability $g/n \ge 2/p$, independently of the other draws. So the number $X$ of draws in $W$ is a binomial variable with mean $\mu = psg/n \ge 2s$. By the Chernoff bound $\Pr[X \le (1 - \delta)\mu] \le e^{-\delta^2 \mu/2}$ with $\delta = 1/2$,

$$\Pr[X \le s] \le \Pr[X \le \mu/2] \le e^{-\mu/8} \le e^{-s/4}.$$

There are $n - g + 1 \le n$ runs. By Lemma 2 and a union bound, the probability that some bucket has more than $g$ keys is at most $n e^{-s/4}$. For $s \ge 12 \ln n$ this is at most $n \cdot n^{-3} = n^{-2}$. $\square$

## Running time

On the CREW PRAM with $p$ processors, lines L1 to L3 take time $O(ps \log(ps))$ with the sample sorted on one processor. Line L4 takes time $O(\lceil n/p \rceil \log p)$, line L5 takes time $O(n/p + p + \log p)$, and on the event of the theorem, line L6 takes time $O((n/p + 1) \log n)$. Line L7 is free when the buckets were placed in order on line L5. So with probability at least $1 - n^{-2}$ the time is $O((n/p) \log n + ps \log(ps))$.
