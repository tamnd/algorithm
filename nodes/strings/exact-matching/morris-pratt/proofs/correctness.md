---
title: Morris-Pratt outputs exactly the valid shifts
proves: [correctness, termination]
status: full
---

**Claim.** For a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$ with $m \ge 1$, MP-MATCHER$(T, P)$ stops and outputs exactly the shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. For $m = 0$, line L2 outputs every shift $0, \ldots, n$, as the definition requires.

**Setup.** Assume that lines L12 to L18 compute the [prefix function](/prefix-function/) $\pi$ of $P$; the proof is on that page. For a string $x$, let $\lambda(x)$ be the length of the longest prefix of $P$ that is a suffix of $x$ and is shorter than $m$. We use the border-chain lemma: for $q \ge 1$, the lengths of the proper borders of $P[0 \ldots q-1]$ are exactly $\pi[q-1], \pi[\pi[q-1]-1], \ldots, 0$, in decreasing order.

**Lemma 1.** Let $q = \lambda(x)$. The prefixes of $P$ of length at most $q$ that are suffixes of $x$ are exactly $P[0 \ldots q-1]$ and the proper borders of $P[0 \ldots q-1]$.

*Proof.* If $k \le q$ and $P[0 \ldots k-1]$ is a suffix of $x$, then it is a suffix of the longer suffix $P[0 \ldots q-1]$ of $x$, and it is a prefix of it too, so it is a border of $P[0 \ldots q-1]$ (proper if $k < q$). Conversely, a border of $P[0 \ldots q-1]$ is a suffix of $P[0 \ldots q-1]$, hence of $x$. $\square$

**Lemma 2.** Let $q = \lambda(x)$ at line L6 and $c = T[i]$. After line L8, $q$ is the length $\ell$ of the longest prefix of $P$ that is a suffix of $xc$.

*Proof.* For $j < m$, the prefix $P[0 \ldots j]$ is a suffix of $xc$ exactly when $P[0 \ldots j-1]$ is a suffix of $x$ and $P[j] = c$. Such a $j$ is at most $\lambda(x) = q$. So by Lemma 1, $\ell - 1$ is the first value $j$ in the list $q, \pi[q-1], \pi[\pi[q-1]-1], \ldots, 0$ with $P[j] = c$, and $\ell = 0$ if there is none.

Lines L6 and L7 walk down this list, in this order, while the current value is positive and $P[q] \ne c$. Each step lowers $q$ by at least 1 and $q \ge 0$, so the loop stops. If it stops with $P[q] = c$, $q$ is the first good value and line L8 sets $q = \ell$. If it stops with $q = 0$ and $P[0] \ne c$, no value of the list is good, line L8 changes nothing, and $q = 0 = \ell$. $\square$

**Theorem.** The claim holds.

*Proof.* We prove by induction on $i$ that at the start of the iteration for $i$, and at the end for $i = n$:

> **(I)** $q = \lambda(T[0 \ldots i-1])$, and the output is the increasing list of the valid shifts $s$ with $s + m \le i$.

For $i = 0$, line L4 sets $q = 0 = \lambda$ of the empty string, and nothing is output. Assume (I) for $i$. By Lemma 2, after line L8, $q = \ell$, the length of the longest prefix of $P$ that is a suffix of $T[0 \ldots i]$. The shift $i - m + 1$ is valid exactly when $\ell = m$, and it is larger than all shifts output before, so lines L9 and L10 keep the second part of (I). If $\ell < m$, then $q = \lambda(T[0 \ldots i])$. If $\ell = m$, the longest prefix shorter than $m$ that is a suffix of $T[0 \ldots i]$ is, by Lemma 1 applied with $P$ in place of $P[0 \ldots q-1]$, the longest proper border of $P$, of length $\pi[m-1]$, which line L11 assigns. So (I) holds for $i + 1$. The loop of line L5 runs $n$ times and each inner loop stops, so the algorithm stops, and (I) for $i = n$ is the claim. $\blacksquare$
