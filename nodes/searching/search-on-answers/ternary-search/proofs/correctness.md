---
title: Ternary search keeps the mode in its interval and shrinks the interval by a factor of at least 2/3
proves: [correctness]
status: full
---

We use the pseudocode of the page. Let $f$ be strictly unimodal for a maximum on its domain, with mode $m$, as defined on the page [unimodal function](/unimodal-function/). We use its comparison lemma: for $x_1 < x_2$, $f(x_1) < f(x_2)$ implies $m > x_1$; $f(x_1) > f(x_2)$ implies $m < x_2$; and $f(x_1) = f(x_2)$ implies $x_1 < m < x_2$.

**Claim 1 (real version).** If $m \in [lo, hi]$ before the call of TERNARY-MAX$(f, lo, hi, steps)$, then after the loop $m \in [lo, hi]$ and $hi - lo = (2/3)^{steps}$ times the initial length. The returned point is within half of that length of $m$.

*Proof.* Invariant: before each iteration, $m \in [lo, hi]$. It holds at the start by assumption. In an iteration, lines L2 and L3 give $lo < m_1 < m_2 < hi$ when $lo < hi$, with $m_1 - lo = hi - m_2 = (hi - lo)/3$.

- If $f(m_1) < f(m_2)$ (line L4), then $m > m_1$, so $m \in (m_1, hi] \subseteq [m_1, hi]$, the new interval.
- Else $f(m_1) \ge f(m_2)$. If the inequality is strict, $m < m_2$. If the values are equal, $m_1 < m < m_2$. In both cases $m \in [lo, m_2)$, the new interval of line L5.

So the invariant holds after the iteration. In both branches the new length is $(hi - lo) - (hi - lo)/3 = \tfrac23 (hi - lo)$. After $steps$ iterations the length is $(2/3)^{steps}$ times the initial one. Line L6 returns the midpoint of an interval that holds $m$, so its distance to $m$ is at most half the length. If $lo = hi$ at some point, then $m = lo$ and every later iteration keeps $lo = hi$. $\square$

The proof uses exact arithmetic. In floating point the computed $m_1$ and $m_2$ can be equal when the interval holds few doubles; the case analysis then still keeps $m$ in the interval, but the length stops shrinking.

**Claim 2 (integer version).** For integers $lo \le hi$ with $m \in \{lo, \ldots, hi\}$, TERNARY-INT$(f, lo, hi)$ returns $m$. With $n = hi - lo + 1 \ge 2$ candidates it makes at most $\lceil \log_{3/2} n \rceil$ iterations and $2 \lceil \log_{3/2} n \rceil$ evaluations of $f$.

*Proof.* Invariant: $lo \le m \le hi$ before each test of line L7. It holds at the start. In an iteration $lo < hi$; let $\ell = hi - lo \ge 1$ and $d = \lfloor \ell/3 \rfloor \ge 0$ (line L8). Line L9 sets $m_1 = lo + d$ and $m_2 = hi - d$, so $m_2 - m_1 = \ell - 2d \ge \ell/3 > 0$ and $lo \le m_1 < m_2 \le hi$.

- If $f(m_1) < f(m_2)$, then $m > m_1$, so $m \ge m_1 + 1$, the new $lo$ of line L10. The bound $m \le hi$ is unchanged.
- Else, as in Claim 1, $m < m_2$, so $m \le m_2 - 1$, the new $hi$ of line L11.

So the invariant holds. When the loop stops, $lo \ge hi$; together with $lo \le m \le hi$ this gives $lo = m = hi$, and line L12 returns $m$.

*Termination and count.* Let $s = hi - lo + 1$ be the number of candidates. One iteration removes at least $d + 1$ of them, so the new count is at most $s - 1 - \lfloor (s - 1)/3 \rfloor = \lceil 2(s-1)/3 \rceil \le \tfrac{2(s-1) + 2}{3} = \tfrac{2s}{3}$. The count drops by at least 1 per iteration, so the loop ends. After $t$ iterations $s \le (2/3)^t n$. The loop runs only while $s \ge 2$, so if it makes $t \ge 1$ iterations then $2 \le (2/3)^{t-1} n$, that is $t \le 1 + \log_{3/2}(n/2) < \log_{3/2} n$, because $\log_{3/2} 2 > 1$. Hence $t \le \lceil \log_{3/2} n \rceil$. Each iteration evaluates $f$ twice and nothing else does, which gives the bound on evaluations. $\square$
