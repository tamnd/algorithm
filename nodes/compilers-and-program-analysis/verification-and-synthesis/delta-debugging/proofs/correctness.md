---
title: ddmin returns a 1-minimal failing input after O(N^2) tests
proves: [correctness]
status: full
---

**Setting.** $c_0$ is a list of $N \ge 1$ elements and $\mathit{test}$ is any function from sub-lists of $c_0$ to $\{\mathrm{FAIL}, \mathrm{PASS}, \mathrm{UNRESOLVED}\}$ with $\mathit{test}(c_0) = \mathrm{FAIL}$ and $\mathit{test}([\,]) = \mathrm{PASS}$. Nothing else is assumed: the test need not be monotone. A sub-list keeps the original order; for a part $d$ of a list $c$, $c - d$ is $c$ without the elements of $d$. A failing list $c$ is *1-minimal* when $\mathit{test}(c - \delta) \ne \mathrm{FAIL}$ for every element $\delta$ of $c$. SPLIT$(c, n)$, for $1 \le n \le |c|$, returns $n$ contiguous parts whose sizes differ by at most 1, so each has at least $\lfloor |c| / n \rfloor \ge 1$ element and their concatenation is $c$.

## Lemma 1: the loop invariant

**Claim.** Each time the test of line L2 is evaluated, $c$ is a sub-list of $c_0$, $\mathit{test}(c) = \mathrm{FAIL}$, and $2 \le n \le \max(|c|, 2)$.

**Proof.** At the start, $c = c_0$ fails and $n = 2$. Assume the claim at the top of an iteration with $|c| \ge 2$; then $2 \le n \le |c|$, so SPLIT is defined and gives $n$ non-empty parts.

- Line L5: $c$ becomes a part $d_i$ with $\mathit{test}(d_i) = \mathrm{FAIL}$, and $n = 2$.
- Line L7: $c$ becomes $c - d_i$ with $\mathit{test}(c - d_i) = \mathrm{FAIL}$. It is the union of the other $n - 1$ parts, each non-empty, so $|c - d_i| \ge n - 1$. The new $n$ is $\max(n - 1, 2)$; if $n - 1 \ge 2$ it is at most $|c - d_i|$, and otherwise it is $2 \le \max(|c - d_i|, 2)$.
- Line L9: $c$ is unchanged and the new $n$ is $\min(2n, |c|)$, which lies between $n + 1$ and $|c|$ because $n < |c|$.

A sub-list of a sub-list is a sub-list, so the claim holds again. $\square$

## Theorem 1: termination and 1-minimality

**Claim.** DDMIN stops and returns a sub-list of $c_0$ that fails and is 1-minimal.

**Proof.** *Termination.* Consider the pair $(|c|, -n)$ in lexicographic order. Lines L5 and L7 make $|c|$ smaller: a part $d_i$ with $n \ge 2$ non-empty parts misses at least one element, and so does $c - d_i$ because $d_i$ is not empty. Line L9 keeps $|c|$ and makes $n$ larger. Both $|c| \ge 0$ and $n \le |c|$ are bounded, so only finitely many iterations happen before line L11 or the test of line L2 ends the loop.

*The result fails* by Lemma 1, and it is a sub-list of $c_0$.

*1-minimality.* There are two ways to leave the loop.

- $|c| \le 1$. $|c| = 0$ is impossible, because $c$ fails and the empty list passes. So $|c| = 1$, and removing its element gives the empty list, which passes.
- Line L11, in an iteration where no subset and no complement failed and $n \ge |c|$. With Lemma 1, $n = |c|$, so every part is one element, and the parts are all the elements of $c$. If $n > 2$, line L6 tested $c - d_i = c - \delta$ for every element $\delta$ and none failed. If $n = 2$, then $|c| = 2$, and $c - d_1 = d_2$ and $c - d_2 = d_1$; both parts were tested on line L4 and did not fail.

In both cases no removal of one element gives FAIL. $\square$

## Theorem 2: the number of tests

**Claim.** DDMIN calls $\mathit{test}$ at most $(3N - 2)(N - 1)$ times for $N \ge 2$, and never for $N = 1$. So the number of tests is $O(N^2)$.

**Proof.** An iteration at granularity $n$ tests at most $n$ parts on line L4 and, only when $n > 2$, at most $n$ complements on line L6. So it makes at most $2n$ tests.

Group the iterations into *phases*: a phase is a maximal run of consecutive iterations with the same $c$. Inside a phase, every iteration but the last one ends on line L9, and the last one ends on line L5, L7 or L11. Let the phase have size $m = |c| \ge 2$ and let its iterations have the granularities $n_0 < n_1 < \dots < n_r$.

- For $j < r$, $n_{j+1} = \min(2 n_j, m)$, and the iteration at $n_j$ did not stop, so $n_j < m$. All $n_j$ with $j < r$ satisfy $n_{j+1} = 2 n_j$ except possibly the last of them, so $n_0, \dots, n_{r-1}$ is a doubling sequence with $n_0 \ge 2$ and $n_{r-1} \le m - 1$. Its sum is $2 n_{r-1} - n_0 \le 2(m - 1) - 2 = 2m - 4$. The tests of these iterations number at most $2(2m - 4) = 4m - 8$, and none happen when $r = 0$.
- The last iteration has $n_r \le m$ by Lemma 1, so it makes at most $2m$ tests.

A phase of size $m$ makes at most $2m$ tests if $r = 0$, and at most $6m - 8$ tests if $r \ge 1$. In the second case $n_0 < m$ forces $m \ge 3$, where $6m - 8 \ge 2m$; for $m = 2$, the bound $2m = 4 = 6m - 8$. So every phase of size $m \ge 2$ makes at most $6m - 8$ tests.

Each phase but the last ends on line L5 or L7, which makes $c$ strictly shorter, as in Theorem 1. The phases therefore have pairwise different sizes, all between 2 and $N$, and the total is at most

$$\sum_{m=2}^{N} (6m - 8) = 3N(N + 1) - 6 - 8(N - 1) = 3N^2 - 5N + 2 = (3N - 2)(N - 1).$$

For $N = 1$ the loop does not run. $\square$

**Remarks.** The bound is not tight. Zeller and Hildebrandt state $N^2 + 3N$ tests in the worst case for their version (Proposition 12), from a scenario in which every test is UNRESOLVED until $n = N$ and then only the last complement fails, one element at a time. The tests of the page check the bound $(3N - 2)(N - 1)$ on every test function for $N \le 4$ and on random ones up to $N = 12$.

In the best case of the paper, one element $\delta$ makes every list that contains it fail and every other list pass. Then at $n = 2$ one of the two halves fails, so every iteration replaces $c$ by a part of size $\lceil |c| / 2 \rceil$ or less with at most 2 tests. After $\lceil \log_2 N \rceil$ iterations one element is left, and the total is at most $2 \lceil \log_2 N \rceil$; the paper states $2 \log_2 N$ (Proposition 13).

## A 1-minimal result need not be a minimum

Let the elements be $0, \dots, 7$ and let a list fail exactly when it contains both 0 and 1, or contains 6. DDMIN tests $[0, 1, 2, 3]$ (FAIL), then $[0, 1]$ (FAIL), then $[0]$ and $[1]$ (both PASS), and returns $[0, 1]$, which is 1-minimal by Theorem 1. The list $[6]$ fails and has one element, so the result is not a minimum. More generally, deciding that a failing list of size $s$ is a minimum, with the test as a black box, needs the outcome of every non-empty list of size less than $s$: an adversary that answers PASS can make any untested one of them FAIL. When $s = N$ that is $2^N - 2$ tests, so no algorithm can match the $O(N^2)$ bound of Theorem 2 for minimum results.
