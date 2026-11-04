---
title: Interval branch and bound encloses the global minimum and all global minimizers
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Let $X \subseteq \mathbb{R}^d$ be a box, let $f$ attain its minimum $f^*$ on $X$, and let $M = \{x \in X : f(x) = f^*\} \ne \emptyset$. The inclusion function $F$ satisfies $f(y) \in F(Y)$ for every box $Y \subseteq X$ and every $y \in Y$; so $\underline{F}(Y) \le f(y)$. Let $\varepsilon > 0$.

**Claim 1 (upper bound).** At every point, $\overline{f} = f(\bar{x})$ for some $\bar{x} \in X$, so $f^* \le \overline{f}$, and $\overline{f}$ never increases. *Proof.* Line L1 sets $\overline{f} = f(\mathrm{mid}(X))$ and line L8 sets it to a smaller value $f(\mathrm{mid}(Z))$ with $Z \subseteq X$; the center of a box lies in it. $\square$

**Claim 2 (a discarded box holds no minimizer).** If a box $Y$ has $\underline{F}(Y) > \overline{f}$ for some value $\overline{f}$ taken during the run, then $Y \cap M = \emptyset$. *Proof.* For $x \in Y \cap M$, $\underline{F}(Y) \le f(x) = f^* \le \overline{f}$ by Claim 1. $\square$

**Claim 3 (invariant).** Each entry $(\beta, Y)$ of $H$ or $R$ has $\beta = \underline{F}(Y)$, and at the start of each iteration of line L2, $M \subseteq \bigcup \{Y : (\beta, Y) \in H \cup R\}$.

*Proof.* At the start, $H = \{(\underline{F}(X), X)\}$, and $M \subseteq X$. Suppose the claim holds at the start of an iteration that takes $(\beta, Y)$ and does not break. If line L5 moves $Y$ to $R$, the union is the same. Otherwise $Y = Y_1 \cup Y_2$, and each $Y_i$ is inserted unless $\underline{F}(Y_i) > \overline{f}$ at line L9, in which case $Y_i \cap M = \emptyset$ by Claim 2. So every point of $Y \cap M$ lies in a box that is inserted, and the claim holds at the next start. $\square$

**Claim 4 (termination).** For a box made by the algorithm along a path of cuts from $X$, a side of initial length $\ell$ is cut at most $\lceil \log_2 (\ell / \varepsilon) \rceil$ times. So every path has at most $d \lceil \log_2 (w(X)/\varepsilon) \rceil$ cuts, at most finitely many boxes are made, and the loop ends.

*Proof.* Line L6 cuts a box only if its width exceeds $\varepsilon$, and it cuts a longest side, which has length equal to the width. After $k$ cuts, a side of initial length $\ell$ has length $\ell / 2^k$; it is cut again only if $\ell / 2^k > \varepsilon$, that is, $k < \log_2 (\ell / \varepsilon)$. So it is cut at most $\lceil \log_2 (\ell/\varepsilon) \rceil$ times, with $\ell \le w(X)$. Each iteration takes one box from $H$ and inserts at most two, each a child in a binary tree of finite depth, so there are finitely many iterations. $\square$

**Theorem.** INTERVAL-BB returns $(\underline{f}, \overline{f}, \bar{x}, R)$ with $\underline{f} \le f^* \le \overline{f} = f(\bar{x})$, every global minimizer in a box of $R$, and every box of $R$ of width at most $\varepsilon$.

*Proof.* By Claim 4 the loop ends, either with $H$ empty or at line L4 with $\beta > \overline{f}$. In the second case, the queue is a min-priority queue, so every box left in $H$, and the box just taken, has lower bound above $\overline{f}$, and by Claim 2 it holds no point of $M$. In both cases, Claim 3 gives $M \subseteq \bigcup \{Y : (\beta, Y) \in R\}$ before line L10. Line L10 deletes only entries with $\beta > \overline{f}$, which hold no point of $M$ by Claim 2, so $M$ is still covered by $R$ after it. As $M \ne \emptyset$, $R$ is not empty, and for $x^* \in M$ in a box $Y$ of $R$, $\underline{f} \le \beta = \underline{F}(Y) \le f(x^*) = f^*$. Claim 1 gives $f^* \le \overline{f} = f(\bar{x})$. Boxes enter $R$ only at line L5, with width at most $\varepsilon$. $\blacksquare$
