---
tag: GBSWZP
kind: theorem
slug: haken-resolution-lower-bound
name: Haken's resolution lower bound
aliases:
- pigeonhole resolution lower bound
- Haken's theorem
- PHP lower bound for resolution
area: logic-and-constraints/sat-solving
level: advanced
summary: Every resolution refutation of the pigeonhole formula with n + 1 pigeons and n holes has 2^Ω(n) clauses, so CDCL solvers need exponential time on it.
prereqs: [refutation, resolvent, pigeonhole-principle, conjunctive-normal-form]
see_also: [cdcl-simulates-resolution, drat-proof, pseudo-boolean-sat, symmetry-breaking, perfect-matching, cdcl]
sources:
  - paper: doi:10.1016/0304-3975(85)90144-6
    title: Armin Haken, The intractability of resolution, Theoretical Computer Science 39, 1985, 297-308
    locator: the main theorem, an exponential lower bound for resolution refutations of the pigeonhole formulas, proved by bottleneck counting
  - paper: "Paul Beame and Toniann Pitassi, Simplified and improved resolution lower bounds, FOCS 1996, pages 274 to 282"
    title: Simplified and improved resolution lower bounds
    locator: the proof by critical assignments, monotone clauses and random restrictions that this page follows
  - paper: doi:10.1145/375827.375835
    title: Eli Ben-Sasson and Avi Wigderson, Short proofs are narrow, resolution made simple, Journal of the ACM 48(2), 2001, 149-169
    locator: the size-width relation for general and tree-like resolution, and its use for the pigeonhole principle on bipartite expanders
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 7 (Buss and Nordström, Proof Complexity and SAT Solving), the sections on resolution lower bounds and the pigeonhole principle
---

Haken's theorem says that the pigeonhole formula $\mathrm{PHP}^{n+1}_n$, which states that $n + 1$ pigeons sit in $n$ holes with no two in the same hole, has no short resolution [refutation](/refutation/): every refutation has $2^{\Omega(n)}$ clauses. Armin Haken proved it in 1985. It was the first exponential lower bound for general resolution, the proof system behind [DPLL](/dpll/) and [CDCL](/cdcl/). Because the clauses learned by a CDCL solver form a resolution refutation, the theorem means that every CDCL solver, with any heuristics, needs exponential time on these small formulas. The formula has only $n(n+1)$ variables and $O(n^3)$ clauses, and the [pigeonhole principle](/pigeonhole-principle/) it encodes is obvious to a human. Stronger proof systems, such as cutting planes, extended resolution and [DRAT](/drat-proof/), have polynomial proofs of it.

## Statement

**The formula.** For $n \ge 1$, the variables are $p_{i,j}$ for pigeons $i \in [n+1]$ and holes $j \in [n]$, meaning "pigeon $i$ sits in hole $j$". The clauses are

- the pigeon clauses $P_i = (p_{i,1} \vee \cdots \vee p_{i,n})$ for each $i$, which say that every pigeon sits somewhere;
- the hole clauses $H_{i,i',j} = (\neg p_{i,j} \vee \neg p_{i',j})$ for $i < i'$ and each $j$, which say that no two pigeons share a hole.

So $\mathrm{PHP}^{n+1}_n$ has $N = n(n+1)$ variables and $m = (n + 1) + n\binom{n+1}{2}$ clauses, and it is unsatisfiable. For $n = 3$ it has 12 variables and 22 clauses.

**Resolution.** A refutation is a list of clauses ending with the empty clause, where each clause is a clause of the formula, the resolvent of two earlier clauses, or a superset of an earlier clause (weakening). Its size $S$ is the number of clauses. Weakening never helps, so the bound holds with or without it. Proofs may be dag-like: a clause can be used many times.

**Theorem (Haken 1985).** There is a constant $c > 0$ such that every resolution refutation of $\mathrm{PHP}^{n+1}_n$ has size at least $2^{cn}$. The proof below gives, for $n \ge 16$,
$$S \ \ge\ \left(\tfrac{16}{15}\right)^{\lfloor n/16 \rfloor}.$$

The hypotheses matter. The bound is for resolution, and it holds for every order of steps and every reuse of clauses. It is stated for the formula above. Adding the clauses that say that each pigeon has at most one hole, or that each hole is full, does not help, because the proof only uses assignments that satisfy them. In terms of the number of variables $N$, the bound is $2^{\Omega(\sqrt{N})}$.

## In plain words

Resolution can only combine clauses two at a time and never introduces a new idea, such as counting. To show that $n + 1$ pigeons do not fit into $n$ holes, it must, in effect, look at many different groups of pigeons and holes separately.

The proof measures how many pigeons a clause "talks about". The empty clause at the end talks about all of them, and every starting clause about at most one. So somewhere in the middle there is a clause that talks about roughly a third of the pigeons. Such a clause must be very long when written in a suitable form. Then a random partial seating of pigeons destroys each long clause with high probability, so there must be very many of them, or one would survive.

## Proof

This is the proof of Beame and Pitassi (1996), with explicit constants. It is shorter than Haken's original bottleneck-counting argument.

**Critical assignments.** For a pigeon $i$, an $i$-critical assignment $\alpha$ puts the other $n$ pigeons into the $n$ holes one to one and puts pigeon $i$ nowhere: $\alpha(p_{i',j}) = 1$ exactly for the matched pairs. It satisfies every clause of $\mathrm{PHP}^{n+1}_n$ except $P_i$. In a critical assignment every hole holds exactly one pigeon.

**Monotone form.** For a clause $C$, let $C^M$ be $C$ with each negative literal $\neg p_{i,j}$ replaced by $\bigvee_{i' \ne i} p_{i',j}$. $C^M$ has only positive literals. Under a critical assignment, hole $j$ is full, so $\neg p_{i,j}$ holds exactly when some other pigeon is in hole $j$. So $\alpha(C) = \alpha(C^M)$ for every critical $\alpha$.

**Pigeon measure.** For a clause $C$ let $\mathrm{Bad}(C)$ be the set of pigeons $i$ such that some $i$-critical assignment makes $C$ false, and let $\mu(C) = |\mathrm{Bad}(C)|$. Then:

- $\mu(P_i) = 1$, $\mu(H_{i,i',j}) = 0$, and $\mu(\emptyset) = n + 1$;
- if $C$ is the resolvent of $A$ and $B$, then $\mathrm{Bad}(C) \subseteq \mathrm{Bad}(A) \cup \mathrm{Bad}(B)$, because an assignment that makes $C$ false makes $A$ or $B$ false; so $\mu(C) \le \mu(A) + \mu(B)$;
- if $C \supseteq A$ (weakening), then $\mu(C) \le \mu(A)$.

**Lemma 1 (a middle clause).** If $n \ge 3$, every refutation contains a clause $C$ with $n/3 < \mu(C) \le 2n/3$.

*Proof.* Start at the empty clause, where $\mu = n + 1 > 2n/3$. While the current clause has $\mu > 2n/3$, move to a parent with the larger $\mu$. That parent has $\mu$ at least half of the current value, so more than $n/3$. Clauses of the formula have $\mu \le 1 \le n/3$, so the walk reaches a clause with $\mu \le 2n/3$ before it reaches one of them. That clause has $\mu > n/3$. $\square$

**Lemma 2 (middle clauses are wide).** If $n/3 < \mu(C) \le 2n/3$, then $C^M$ has more than $2n^2/9$ variables.

*Proof.* Let $s = \mu(C)$. Take $i \in \mathrm{Bad}(C)$ and an $i$-critical $\alpha$ that makes $C$, and so $C^M$, false. Take a pigeon $i' \notin \mathrm{Bad}(C)$, and let $j$ be its hole under $\alpha$. Let $\alpha'$ be $\alpha$ with pigeon $i'$ taken out of hole $j$ and pigeon $i$ put into it. Then $\alpha'$ is $i'$-critical, and $i' \notin \mathrm{Bad}(C)$, so $\alpha'$ satisfies $C$ and $C^M$. The only variable that is 0 under $\alpha$ and 1 under $\alpha'$ is $p_{i,j}$, and $C^M$ has only positive literals, so $p_{i,j}$ is a variable of $C^M$. The $n + 1 - s$ pigeons $i'$ outside $\mathrm{Bad}(C)$ sit in different holes under $\alpha$, so this gives $n + 1 - s$ variables $p_{i,\cdot}$ in $C^M$. Doing this for each of the $s$ pigeons $i \in \mathrm{Bad}(C)$ gives $s(n + 1 - s)$ different variables. The function $s(n + 1 - s)$ is concave, so on $n/3 < s \le 2n/3$ it is at least its value at the ends, and both $\frac{n}{3}(\frac{2n}{3} + 1)$ and $\frac{2n}{3}(\frac{n}{3} + 1)$ exceed $2n^2/9$. $\square$

**Random restrictions.** A restriction $\rho$ seats $t$ pigeons: it matches $t$ pigeons with $t$ holes, sets $p_{i,j} = 1$ for the matched pairs, and sets to 0 every other variable of a matched pigeon or a matched hole. Under $\rho$, the clauses of the matched pigeons and holes become true, and the rest is $\mathrm{PHP}^{n'+1}_{n'}$ on the other pigeons and holes, with $n' = n - t$. Applying $\rho$ to every clause of a refutation and dropping the true clauses gives a refutation of $\mathrm{PHP}^{n'+1}_{n'}$ that is no larger: if $C$ is the resolvent of $A$ and $B$ on a variable that $\rho$ sets, then $C|_\rho$ contains $A|_\rho$ or $B|_\rho$ (a weakening), and otherwise $C|_\rho$ is the resolvent of $A|_\rho$ and $B|_\rho$.

If $\rho$ sets to 1 some variable $p_{i,j}$ of $C^M$, then $\rho$ makes $C$ true. Either $p_{i,j}$ is a literal of $C$, or $\neg p_{i',j}$ is a literal of $C$ for some $i' \ne i$, and $\rho$ sets $p_{i',j} = 0$ because hole $j$ is taken. Also, for $D = C|_\rho$, every variable of the monotone form $D^M$ in the smaller instance is a variable of $C^M$.

**Proof of the theorem.** Let $n \ge 16$, $t = \lfloor n/16 \rfloor$, $n' = n - t$ and $W = 2n'^2/9$. Call a clause $C$ of the refutation *fat* if $C^M$ has at least $W$ variables. Build $\rho$ in $t$ steps. In each step choose a free pigeon and a free hole, each uniformly at random, and seat the pigeon there. Fix a fat clause $C$ that is not yet true. Each earlier step removed one pigeon, with at most $n$ variables of $C^M$, and one hole, with at most $n + 1$. So at step $k \le t$ at least $W - t(2n + 1)$ variables of $C^M$ belong to free pairs, out of at most $n(n+1)$ free pairs. With $n' \ge 15n/16$ and $t \le n/16$,
$$\frac{W - t(2n+1)}{n(n+1)} \ \ge\ \frac{\frac{2}{9} \cdot \frac{225}{256} n^2 - \frac{n^2}{8} - \frac{n}{16}}{n(n+1)} \ =\ \frac{\frac{9}{128} n - \frac{1}{16}}{n + 1} \ \ge\ \frac{1}{16},$$
where the last step holds for $n \ge 16$ (with equality at $n = 16$). So each step makes $C$ true with probability at least $1/16$, whatever happened before, and $C$ survives all $t$ steps with probability at most $(15/16)^t$.

Suppose the refutation has $S < (16/15)^t$ clauses. Then the expected number of fat clauses that survive is less than 1, so some $\rho$ makes every fat clause true. The restricted refutation of $\mathrm{PHP}^{n'+1}_{n'}$ has, by Lemmas 1 and 2 ($n' \ge 15 \ge 3$), a clause $D = C|_\rho$ with more than $2n'^2/9 = W$ variables in $D^M$. These are variables of $C^M$, so $C$ is fat, but $\rho$ makes $C$ true, so $D$ is not in the restricted refutation. This is a contradiction. Hence $S \ge (16/15)^{\lfloor n/16 \rfloor} = 2^{\Omega(n)}$. $\blacksquare$

**The width proof of Ben-Sasson and Wigderson, in outline.** They prove that a refutation of size $S$ of a formula with $N$ variables and clauses of width at most $w_0$ can be turned into one of width at most $w_0 + O(\sqrt{N \log S})$, so
$$S \ \ge\ \exp\!\left(\Omega\!\left(\frac{(w - w_0)^2}{N}\right)\right),$$
where $w$ is the smallest width of a refutation. For $\mathrm{PHP}^{n+1}_n$ this is useless, because $w_0 = n$ and $N \approx n^2$. Instead, take a bipartite graph $G$ between pigeons and holes with constant degree that is an expander, and set $p_{i,j} = 0$ for every non-edge. This restriction maps a refutation of $\mathrm{PHP}^{n+1}_n$ to one of the graph formula $G\text{-}\mathrm{PHP}$ of no larger size. The graph formula has $N = O(n)$ variables and $w_0 = O(1)$, and the expansion gives $w = \Omega(n)$ by an argument with a measure like $\mu$ above. So $S \ge \exp(\Omega(n^2/n)) = 2^{\Omega(n)}$.

## Consequences

- **CDCL needs exponential time on pigeonhole formulas.** A CDCL run with $c$ conflicts gives a resolution refutation with at most about $c \cdot N$ clauses, so every run, with any heuristics, restarts and deletion policy, has $2^{\Omega(n)}$ conflicts. See [CDCL simulates resolution](/cdcl-simulates-resolution/) for the converse direction.
- **Resolution is not polynomially bounded.** Cook and Reckhow showed that NP $\ne$ coNP exactly when no proof system has polynomial proofs for all unsatisfiable formulas. This theorem settles the question for resolution: it has no polynomial proofs for a simple family. It was the first such result for general resolution, after Tseitin's 1968 bound for regular resolution.
- **Encodings matter.** Problems with a counting core, such as scheduling with more jobs than slots or [pseudo-Boolean](/pseudo-boolean-sat/) constraints, can be hard for CNF solvers for this reason. [Symmetry breaking](/symmetry-breaking/) or reasoning in cutting planes avoids the blow-up.
- **Stronger systems.** Cook (1976) gave polynomial extended resolution proofs of the pigeonhole principle, cutting planes has polynomial proofs, and DRAT and PR proofs can be short too. These separations show that resolution is strictly weaker than these systems.

## Tightness

The bound is tight up to the constant in the exponent: $\mathrm{PHP}^{n+1}_n$ has resolution refutations with $n(n+3)2^{n-2}$ resolution steps. For a set $H$ of $k - 1$ holes, let $Q(k, H)$ be the clause $\bigvee_{i \le k} \bigvee_{j \notin H} p_{i,j}$, which says that pigeons $1, \ldots, k$ do not all fit into $H$. Then $Q(1, \emptyset) = P_1$ and $Q(n + 1, [n])$ is empty. To derive $Q(k + 1, H')$ for $|H'| = k$, start with $P_{k+1}$. For each $j \in H'$, resolve $Q(k, H' \setminus \{j\})$ with the $k$ hole clauses $H_{i,k+1,j}$, $i \le k$, which replaces each $p_{i,j}$ with $\neg p_{k+1,j}$, and resolve the result with the current clause on $p_{k+1,j}$. This takes $k(k + 1)$ steps for each of the $\binom{n}{k}$ sets $H'$, and $\sum_k \binom{n}{k} k(k+1) = n(n+3)2^{n-2}$. A script that builds and checks these refutations finds 10, 36, 112, 320, 864 and 2240 steps for $n = 2, \ldots, 7$.

The constant in the proof above, $\log_2(16/15)/16 \approx 0.0058$, was chosen for short arithmetic, not to be optimal. Both bounds are of the form $2^{\Theta(n)}$, so the theorem is tight up to the constant in the exponent.

## History

Tseitin (1968) proved exponential lower bounds for regular resolution on formulas built from graphs. Haken (1985) proved the first exponential lower bound for general resolution, for the pigeonhole formulas, with a bottleneck-counting argument over critical assignments. Urquhart (1987) extended the method to Tseitin formulas on expanders, and Chvátal and Szemerédi (1988) to random $k$-CNF. Beame and Pitassi (1996) gave the short proof by monotone clauses and random restrictions used above. Ben-Sasson and Wigderson (1999, journal version 2001) explained most of these bounds by the size-width relation.

## References
