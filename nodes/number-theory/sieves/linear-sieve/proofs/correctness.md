---
title: The linear sieve computes the primes and the least prime factors up to n, writing each composite once
proves: [correctness]
status: full
---

For $m \ge 2$ let $\mathrm{lp}(m)$ be the least prime factor of $m$. If $n < 2$, the loop of line L2 does not run, and the output is the empty list with $\mathrm{lp}[m] = 0$ for $m \le n$, which is correct. Let $n \ge 2$.

**Lemma 1 (unique form).** Let $m \ge 2$ be composite. Among all ways to write $m = p \cdot i$ with $p$ prime and $i \ge 2$, exactly one has $p \le \mathrm{lp}(i)$, namely $p = \mathrm{lp}(m)$ and $i = m / \mathrm{lp}(m)$. Moreover, for every prime $p$ and every $i \ge 2$ with $p \le \mathrm{lp}(i)$, we have $\mathrm{lp}(p i) = p$.

*Proof.* Take $i \ge 2$ and a prime $p \le \mathrm{lp}(i)$. Every prime factor of $p i$ is $p$ or a prime factor of $i$, which is at least $\mathrm{lp}(i) \ge p$; so $\mathrm{lp}(p i) = p$. This is the second statement. For the first, if $m = p i$ with $p \le \mathrm{lp}(i)$, then $p = \mathrm{lp}(m)$ by the second statement and $i = m/p$, so there is at most one such form. And the form exists: with $p = \mathrm{lp}(m)$ and $i = m/p$, we have $i \ge 2$ because $m$ is composite, and every prime factor of $i$ divides $m$, so it is at least $p$; thus $p \le \mathrm{lp}(i)$. $\square$

**Invariant.** When the loop of line L2 starts the round of $i$ (with $2 \le i \le n + 1$, the value $n + 1$ meaning the end):

> **(A)** for $2 \le j < i$, $\mathrm{lp}[j] = \mathrm{lp}(j)$, and the list holds exactly the primes less than $i$, in increasing order;
>
> **(B)** for $i \le m \le n$, $\mathrm{lp}[m] \ne 0$ if and only if $m$ is composite and $m / \mathrm{lp}(m) < i$, and then $\mathrm{lp}[m] = \mathrm{lp}(m)$;
>
> **(C)** every write of line L7 so far went to a different index.

*Initialization.* At $i = 2$, the list is empty and every entry is 0. No composite $m$ has $m/\mathrm{lp}(m) < 2$. No write has happened. So (A), (B) and (C) hold.

*Maintenance.* Assume the invariant at the start of the round of $i \le n$.

First, lines L3 and L4. By (B) with $m = i$: if $i$ is composite, then $i / \mathrm{lp}(i) < i$, so $\mathrm{lp}[i] = \mathrm{lp}(i) \ne 0$ and line L3 fails. If $i$ is prime, then $\mathrm{lp}[i] = 0$, and line L4 sets $\mathrm{lp}[i] = i = \mathrm{lp}(i)$ and appends $i$, which is larger than every prime in the list. Either way, after line L4, $\mathrm{lp}[i] = \mathrm{lp}(i)$ and the list holds exactly the primes up to $i$, in increasing order.

Next, the loop of lines L5 to L7. Every prime $p \le \mathrm{lp}(i)$ satisfies $p \le i$, so it is in the list. The loop takes the primes of the list in increasing order and stops at the first one with $p > \mathrm{lp}(i)$ or $p i > n$. So it runs line L7 exactly for the primes $p$ with $p \le \mathrm{lp}(i)$ and $p i \le n$. By Lemma 1, line L7 sets $\mathrm{lp}[p i] = p = \mathrm{lp}(p i)$, and $(p i) / \mathrm{lp}(p i) = i$.

Now check the invariant at $i + 1$. (A): the entry $\mathrm{lp}[i]$ is correct, as shown, and entries below $i$ do not change, because each write goes to $p i \ge 2i > i$. (B): let $i + 1 \le m \le n$. If $m$ is composite with $m / \mathrm{lp}(m) < i$, then $\mathrm{lp}[m] = \mathrm{lp}(m)$ already by (B), and a write in this round would go to $m = p i$ with $m / \mathrm{lp}(m) = i$, which is not the case, so the entry stays. If $m$ is composite with $m / \mathrm{lp}(m) = i$, then $p = \mathrm{lp}(m) \le \mathrm{lp}(i)$ by Lemma 1, and $p i = m \le n$, so this round writes $\mathrm{lp}[m] = \mathrm{lp}(m)$. In every other case, $m$ is prime or $m / \mathrm{lp}(m) > i$; then $\mathrm{lp}[m] = 0$ by (B), and this round does not write $m$, since each write goes to an $m$ with $m / \mathrm{lp}(m) = i$. (C): the writes of this round go to the indices $p i$ for distinct $p$, which are distinct, and each has $m / \mathrm{lp}(m) = i$. A write of an earlier round $i' < i$ went to an index with $m / \mathrm{lp}(m) = i' \ne i$. So no index is written twice.

*Termination.* The outer loop runs $n - 1$ times, and each inner loop runs at most $\pi(n) + 1$ times.

*Conclusion.* At the end, $i = n + 1$, and (A) says that $\mathrm{lp}[j] = \mathrm{lp}(j)$ for all $2 \le j \le n$ and that the list holds exactly the primes up to $n$, in increasing order. Indices 0 and 1 are never written, since each write goes to $p i \ge 4$ and line L4 writes $i \ge 2$. $\blacksquare$

**The count of writes.** By (C) and (B), line L7 writes each composite $m \le n$ exactly once, in the round of $i = m / \mathrm{lp}(m)$, and writes nothing else. So it runs exactly $n - 1 - \pi(n)$ times. In each round, the inner loop makes one test of line L6 per write, plus at most one test that breaks or the end of the list, so lines L5 and L6 run at most $(n - 1 - \pi(n)) + (n - 1)$ times in total. This gives the $\Theta(n)$ bound.
