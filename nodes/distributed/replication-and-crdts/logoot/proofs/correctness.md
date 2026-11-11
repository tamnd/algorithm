---
title: Logoot allocation returns a fresh position between its arguments, and replicas converge
proves: [correctness, invariant, termination]
status: full
---

**Setting.** A position is a finite list of triples $(d, s, c)$ with $0 \le d < \mathit{base}$ and $\mathit{base} \ge 2$. Triples are ordered as tuples, and positions in lexicographic order, where a proper prefix is smaller. $\top$ is above every position. Write $x[i]$ for the triple at level $i$, counting from 0, and $x[0..i)$ for the prefix of length $i$. Call a position *good* if it is not empty and its last digit is at least 1. Each site has a distinct id and a clock that it increases before each ALLOC. Operations are delivered once at every replica in a causal order.

**Claim 1 (ALLOC).** Let $p$ be the empty list or a good position, let $q$ be $\top$ or a good position, and let $p < q$. Then ALLOC$(p, q)$ stops and returns a good position $x$ with $p < x < q$, $|x| \le \max(|p|, |q|) + 1$, digits in $[0, \mathit{base})$, and the site and clock of the caller in its last triple.

*Proof.* We show that at the start of each round $i$ the following hold.

- (a) $\mathit{out}$ has length $i$, and $\mathit{out} = p[0..i)$ if $i \le |p|$, while $p$ is a prefix of $\mathit{out}$ if $i \ge |p|$.
- (b) If $\mathit{bound}$ is true, then $q \ne \top$, $\mathit{out} = q[0..i)$ and $i < |q|$.
- (c) If $\mathit{bound}$ is false and $q \ne \top$, then $\mathit{out}[j] < q[j]$ for some $j < i$ with $\mathit{out}[0..j) = q[0..j)$.

At round 0, $\mathit{out}$ is empty, $\mathit{bound}$ is $q \ne \top$, and $|q| \ge 1$ because $q$ is good. So (a) to (c) hold.

*Return at line L5.* Here $qd - pd \ge 2$, and the new digit $d = pd + r$ with $1 \le r \le \mathit{step} \le qd - pd - 1$ has $pd < d < qd \le \mathit{base}$ and $d \ge 1$. Let $t = (d, \mathit{site}, \mathit{clock})$ and $x = \mathit{out} + [t]$. Then $x$ is good. If $i < |p|$, (a) gives $\mathit{out} = p[0..i)$, and $t > p[i]$ because $d > pd$, so $x > p$. If $i \ge |p|$, then $p$ is a prefix of $\mathit{out}$, so a proper prefix of $x$, and $x > p$. If $\mathit{bound}$ is true, (b) gives $\mathit{out} = q[0..i)$ and $t < q[i]$ because $d < qd$, so $x < q$. If $\mathit{bound}$ is false, (c) gives $x < q$, or $q = \top$.

*Line L6* ($i < |p|$). The triple $p[i]$ is appended, so (a) holds at round $i + 1$. Suppose $\mathit{bound}$ was true. By (a) and (b), $p[0..i) = q[0..i)$. If $p[i] = q[i]$, then $\mathit{out} = q[0..i+1)$, and $|q| > i + 1$: otherwise $q$ would be a prefix of $p$, so $q \le p$. Then (b) holds. If $p[i] \ne q[i]$, then $p[i] < q[i]$ because $p < q$ and the prefixes are equal, so (c) holds with $j = i$. If $\mathit{bound}$ was false, (c) carries over.

*Line L7* ($i \ge |p|$, $qd = 0$). Then $\mathit{bound}$ is true, because otherwise $qd = \mathit{base} \ge 2$ and $pd = 0$, and line L3 would have returned. The triple $q[i]$ is appended, so $\mathit{out} = q[0..i+1)$, and $p$ is still a prefix. The digit of $q[i]$ is 0 and $q$ is good, so $|q| > i + 1$, and (b) holds.

*Line L8* ($i \ge |p|$, $qd \ne 0$, no room). As for line L7, $\mathit{bound}$ is true, so $qd = q[i]$'s digit, and with $pd = 0$ and no room, $qd = 1$. The appended triple has digit 0, so it is less than $q[i]$, and (c) holds with $j = i$. Also $p$ is still a prefix of $\mathit{out}$.

*Termination and length.* At a round $i \ge |p|$ with $\mathit{bound}$ false, $pd = 0$ and $qd = \mathit{base} \ge 2$, so line L5 returns. While $\mathit{bound}$ is true and $i \ge |p|$, line L7 runs only while $i + 1 < |q|$, by (b) at the next round, and line L8 sets $\mathit{bound}$ to false. So ALLOC returns at the latest in round $\max(|p|, |q|)$, and $|x| \le \max(|p|, |q|) + 1$. Copied triples come from $p$ or $q$, and the new digit is below $\mathit{base}$, so all digits are in range. $\square$

**Claim 2 (unique positions).** Two different inserts make different positions.

*Proof.* By Claim 1, the last triple of a position holds the site of the insert that made it and the clock value it took. A site never takes the same clock value twice, and site ids are distinct, so two different inserts have different last triples, and their positions differ. $\square$

**Claim 3 (the state).** Let $E$ be a set of operations closed under causal predecessors. A replica that has run exactly $E$, in any causal order, holds the pairs $(x, v)$ such that the insert of $(x, v)$ is in $E$ and no delete of $x$ is in $E$.

*Proof.* By induction on the number of operations run. An insert of $(x, v)$ adds the pair; by Claim 2 no other insert uses $x$, and a delete of $x$ is causally after its insert, so it has not run yet. A delete of $x$ removes the pair, which is present since the insert ran before it. Since $x$ is made by one insert only and deleted at most by deletes after it, the result is the set stated. $\square$

**Theorem 1 (convergence).** Two replicas that have run the same set of operations show the same list.

*Proof.* By Claim 3 they hold the same set of pairs, and READ lists them in increasing position, which is a total order on distinct positions. $\square$

**Theorem 2 (local intent and stable order).** A local INSERT$(i, v)$ makes $v$ the $i$-th element at its source, and a local DELETE$(i)$ removes the $i$-th element. Two elements present at a replica are in the same relative order at every replica and every time.

*Proof.* For an insert, $p$ is the position of element $i - 1$ or the empty list, and $q$ that of element $i$ or $\top$. All positions in the document are good: the empty start is never stored, and Claim 1 makes every new position good. So Claim 1 applies, and $p < x < q$ puts the new pair between the two neighbours, at index $i$. A delete removes the pair at index $i$. The relative order of two elements is the order of their positions, which never change. $\square$

**Termination.** By Claim 1, ALLOC runs at most $\max(|p|, |q|) + 1$ rounds. $\blacksquare$
