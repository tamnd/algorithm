---
title: Correctness of baby-step giant-step
proves: [correctness, termination, minimality]
status: full
---

Let $G$ be a group, $g, h \in G$, $r = \operatorname{ord}(g)$ and $n \ge r$. Let $m = \lceil \sqrt n \rceil$, so $m \ge 1$ and $m^2 \ge n \ge r$.

**Lemma 1 (baby steps).** After the loop of lines L4 to L6, the table $T$ contains exactly the elements $g^0, \dots, g^{m-1}$, and for each such element $e$, $T[e]$ is the least $j \in \{0, \dots, m-1\}$ with $g^j = e$.

*Proof.* By induction on $j$, at the start of round $j$ we have $e = g^j$ (line L3 gives $e = 1 = g^0$, and line L6 multiplies by $g$). Line L5 inserts $e$ with the value $j$ only if $e$ is not yet in $T$, and never changes an entry already present. So each element enters with the first, least index at which it occurs, and every $g^j$ with $j < m$ is present after round $j$. $\square$

**Lemma 2 (giant steps).** At the test of line L10 in round $i$ of the loop of lines L9 to L11, $\gamma = h g^{-im}$.

*Proof.* Line L8 gives $\gamma = h$ for $i = 0$, and line L11 multiplies by $u = g^{-m}$ from line L7. $\square$

**Soundness.** If line L10 returns $x = im + j$ with $j = T[\gamma]$, then by the lemmas $h g^{-im} = \gamma = g^j$, so $h = g^{im + j} = g^x$, and $x \ge 0$.

**Completeness.** Suppose $h \in \langle g \rangle$ and let $x^*$ be the least $x \ge 0$ with $g^x = h$. Then $x^* < r$, because $g^{x^* - r} = h$ would otherwise give a smaller solution. Write $x^* = i^* m + j^*$ with $0 \le j^* < m$. Since $x^* < r \le m^2$, also $i^* < m$, so round $i^*$ is executed unless the algorithm returned earlier. In round $i^*$, $\gamma = h g^{-i^* m} = g^{j^*}$, which is in $T$ by Lemma 1. So the algorithm returns in some round $i \le i^*$.

**Minimality.** Let the algorithm return in round $i$ with $j = T[\gamma]$. If $i < i^*$, the returned $x = im + j \le im + m - 1 < i^* m \le x^*$ is a solution by soundness, smaller than the least solution, which is impossible. So $i = i^*$. In this round $g^{j^*} = \gamma = g^{j}$ with $j$ the least exponent below $m$ for $\gamma$ (Lemma 1), so $j \le j^*$, and $x = i^* m + j \le x^*$ is a solution; by the choice of $x^*$, $x = x^*$.

**Non-membership.** If $h \notin \langle g \rangle$, no round can return, since a return gives $h = g^x$ by soundness. The loops are bounded, so the algorithm stops at line L12 with NONE. Conversely, by completeness, NONE is returned only when $h \notin \langle g \rangle$.

**Termination and cost.** Both loops run at most $m$ rounds, and line L7 uses $O(\log m)$ multiplications by square and multiply, so the algorithm stops after at most $2m + O(\log m)$ group operations, $m$ insertions and $m$ lookups. $\blacksquare$
