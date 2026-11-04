---
tag: WNB66Y
kind: theorem
slug: lovasz-local-lemma
name: Lovász local lemma
aliases:
- Lovasz local lemma
area: foundations/probabilistic-analysis
level: advanced
summary: If each bad event has small probability and depends on few others, then with positive probability no bad event happens, and the Moser-Tardos algorithm finds such an outcome.
prereqs: [probability-space, conditional-probability, independence-of-events, union-bound, probabilistic-method]
see_also: [k-sat, 3-sat, hypergraph, graph-coloring, las-vegas-algorithm, method-of-conditional-expectations, independent-random-variables, linearity-of-expectation]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Section 6.7, The Lovász Local Lemma (6.7.2, Application, Satisfiability); Section 6.9, Lovász Local Lemma, The General Case; Section 6.10, The Algorithmic Lovász Local Lemma
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition, Wiley, 2016
    locator: Chapter 5, The Local Lemma (the lemma, property B, lower bounds for Ramsey numbers, and Section 5.7, Moser's fix-it algorithm)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 5, The Probabilistic Method (the Lovász local lemma)
  - paper: doi:10.1145/1667053.1667060
    title: Robin A. Moser and Gábor Tardos, A constructive proof of the general Lovász local lemma, Journal of the ACM 57(2), 2010
    locator: Algorithm 1.1, Theorem 1.2, Lemma 2.1 (witness trees) and Lemma 3.1 (the Galton-Watson process)
  - paper: doi:10.1007/BF02579368
    title: James B. Shearer, On a problem of Spencer, Combinatorica 5(3), 1985
    locator: pp. 241 to 245; f(1) = 1/2 and f(d) = (d-1)^(d-1)/d^d for d >= 2
  - paper: "Paul Erdős and László Lovász, Problems and results on 3-chromatic hypergraphs and some related questions, in Infinite and Finite Sets, Colloquia Mathematica Societatis János Bolyai 10, North-Holland, 1975"
    locator: the original statement of the lemma
  - paper: doi:10.1002/rsa.3240020402
    title: József Beck, An algorithmic approach to the Lovász local lemma I, Random Structures and Algorithms 2(4), 1991
    locator: pp. 343 to 365; abstract (2-coloring of n-uniform hypergraphs where each edge meets at most 2^(n/48) others)
  - paper: doi:10.1145/1536414.1536462
    title: Robin A. Moser, A constructive proof of the Lovász local lemma, STOC 2009
    locator: pp. 343 to 350
  - paper: doi:10.1145/2975386
    title: Heidi Gebauer, Tibor Szabó and Gábor Tardos, The local lemma is asymptotically tight for SAT, Journal of the ACM 63(5), 2016
    locator: abstract and main theorem (unsatisfiable k-CNF formulas with each variable in at most (2/e + o(1)) 2^k/k clauses)
---

The Lovász local lemma says that a finite family of "bad" events in a [probability space](/probability-space/) has a positive probability that none of them happens, if each event has small probability and is independent of all but a few of the others. It is a tool of the [probabilistic method](/probabilistic-method/): it proves that a satisfying assignment of a [k-SAT](/k-sat/) formula or a proper coloring of a [hypergraph](/hypergraph/) exists in cases where the [union bound](/union-bound/) proves nothing, because the number of events has no limit. The Moser-Tardos algorithm makes the lemma constructive: when the events are defined by independent variables, resampling the variables of a bad event until none is left takes, under the symmetric condition, at most the number of events in expected resampling steps.

## Statement

**Dependency graph.** Let $A_1, \ldots, A_n$ be events in a probability space, and $\bar A_i$ the complement of $A_i$. An event $A$ is *mutually independent* of a family $B_1, \ldots, B_r$ if $\Pr[A \cap C] = \Pr[A]\Pr[C]$ for each event $C = \bigcap_{j \in J} C_j$ with $J \subseteq \{1, \ldots, r\}$ and each $C_j \in \{B_j, \bar B_j\}$ (the empty intersection is the whole space). A graph $G$ on the vertex set $\{1, \ldots, n\}$ is a *dependency graph* of the events if, for each $i$, the event $A_i$ is mutually independent of the family $\{A_j : j \ne i,\ j \notin \Gamma(i)\}$, where $\Gamma(i)$ is the set of neighbors of $i$ in $G$. The vertex $i$ itself is not in $\Gamma(i)$.

**Theorem 1 (general form).** Let $G$ be a dependency graph of $A_1, \ldots, A_n$. If there are real numbers $x_1, \ldots, x_n \in [0, 1)$ with
$$ \Pr[A_i] \le x_i \prod_{j \in \Gamma(i)} (1 - x_j) \qquad \text{for each } i, $$
then
$$ \Pr\Bigl[\,\bigcap_{i=1}^{n} \bar A_i\Bigr] \ \ge\ \prod_{i=1}^{n} (1 - x_i) \ >\ 0. $$

**Theorem 2 (symmetric form).** Assume that $\Pr[A_i] \le p$ for each $i$ and that each vertex of a dependency graph has at most $d$ neighbors. If
$$ e\,p\,(d+1) \le 1, $$
then $\Pr[\bigcap_i \bar A_i] > 0$. For $d \ge 1$ the probability is at least $\bigl(d/(d+1)\bigr)^n$.

### The variable setting and the Moser-Tardos algorithm

Let $\mathcal P$ be a finite set of mutually [independent random variables](/independent-random-variables/), and let each event $A$ of a finite family $\mathcal A$ be determined by the values of a set $\mathrm{vbl}(A) \subseteq \mathcal P$. Join two distinct events by an edge when their variable sets intersect. This graph is a dependency graph: the events not adjacent to $A$ are determined by variables outside $\mathrm{vbl}(A)$, and these are independent of the variables of $A$. The algorithm below needs only a way to draw a sample of each variable and a way to test whether an event holds.

```pseudo id=main
MOSER-TARDOS(𝒫, 𝒜)                    ▷ each event A is determined by the variables vbl(A)
L1  for each variable P in 𝒫 do v_P ← a random sample of P
L2  while some event of 𝒜 holds under the assignment v do
L3      A ← an event of 𝒜 that holds under v      ▷ any rule that does not look at future samples
L4      for each P in vbl(A) do v_P ← a new independent sample of P
L5  return v
```

**Theorem 3 (Moser and Tardos).** In the variable setting, let $\Gamma(A)$ be the set of events $B \ne A$ with $\mathrm{vbl}(A) \cap \mathrm{vbl}(B) \ne \emptyset$. If there are numbers $x(A) \in (0,1)$ with $\Pr[A] \le x(A) \prod_{B \in \Gamma(A)} (1 - x(B))$ for each $A \in \mathcal A$, then MOSER-TARDOS stops with probability 1, it returns an assignment under which no event of $\mathcal A$ holds, and the expected number of times line L4 resamples the event $A$ is at most $x(A)/(1 - x(A))$. So the expected total number of resampling steps is at most
$$ \sum_{A \in \mathcal A} \frac{x(A)}{1 - x(A)}. $$
Under the symmetric condition $e\,p\,(d+1) \le 1$ with $d \ge 1$, the choice $x(A) = 1/(d+1)$ gives at most $|\mathcal A|/d$ expected resampling steps.

## In plain words

Suppose you pick a random outcome and some things can go wrong. If each problem is rare and the problems are fully independent, then with some chance none of them happens, however many problems there are. The local lemma keeps this conclusion when each problem is linked to only a few others. The condition is local: it compares the chance of each problem with the number of its neighbors, and it never looks at the total number of problems. The chance that everything goes well can be tiny, but it is above zero, so a good outcome exists.

The algorithm of Moser and Tardos finds one. It picks random values. While some problem occurs, it takes one such problem and picks new random values for only the inputs of that problem. Under the same condition, the expected number of repairs for each problem is a small constant.

## Proof

### Theorem 1

For $S \subseteq \{1, \ldots, n\}$ write $B_S = \bigcap_{j \in S} \bar A_j$, with $B_\emptyset$ the whole space.

**Claim.** For each $S$ and each $i \notin S$ with $\Pr[B_S] > 0$, we have $\Pr[A_i \mid B_S] \le x_i$.

*Proof of the claim,* by strong induction on $|S|$. Fix $S$ and $i \notin S$ with $\Pr[B_S] > 0$, and assume the claim for all smaller sets. Split $S$ into $S_1 = S \cap \Gamma(i)$ and $S_2 = S \setminus S_1$. Since $B_S \subseteq B_{S_2}$, we have $\Pr[B_{S_2}] > 0$.

1. *Numerator.* Every $j \in S_2$ satisfies $j \ne i$ and $j \notin \Gamma(i)$. By the definition of the dependency graph, $A_i$ is mutually independent of $\{A_j : j \in S_2\}$, and $B_{S_2}$ is an intersection of complements of these events, so $\Pr[A_i \mid B_{S_2}] = \Pr[A_i]$. Hence $\Pr[A_i \cap B_{S_1} \mid B_{S_2}] \le \Pr[A_i \mid B_{S_2}] = \Pr[A_i] \le x_i \prod_{j \in \Gamma(i)} (1 - x_j)$ by the hypothesis.
2. *Case $S_1 = \emptyset$.* Then $B_S = B_{S_2}$ and step 1 gives $\Pr[A_i \mid B_S] = \Pr[A_i] \le x_i$, because each factor $1 - x_j$ is at most 1.
3. *Case $S_1 = \{j_1, \ldots, j_r\}$ with $r \ge 1$.* By the definition of conditional probability, $\Pr[A_i \mid B_S] = \Pr[A_i \cap B_{S_1} \mid B_{S_2}] \,/\, \Pr[B_{S_1} \mid B_{S_2}]$. Write $T_t = S_2 \cup \{j_1, \ldots, j_{t-1}\}$. The chain rule gives
$$ \Pr[B_{S_1} \mid B_{S_2}] = \prod_{t=1}^{r} \bigl(1 - \Pr[A_{j_t} \mid B_{T_t}]\bigr). $$
Each set $T_t$ is a subset of $S$ that does not contain $j_t$, so it has fewer than $|S|$ elements, and $B_{T_t} \supseteq B_S$ has positive probability. So the induction hypothesis gives $\Pr[A_{j_t} \mid B_{T_t}] \le x_{j_t}$, and
$$ \Pr[B_{S_1} \mid B_{S_2}] \ge \prod_{j \in S_1} (1 - x_j) \ge \prod_{j \in \Gamma(i)} (1 - x_j), $$
where the last step uses $S_1 \subseteq \Gamma(i)$ and $0 < 1 - x_j \le 1$.
4. Divide the bound of step 1 by the bound of step 3: $\Pr[A_i \mid B_S] \le x_i$. This proves the claim.

*Proof of Theorem 1.* Let $S_k = \{1, \ldots, k\}$. We show $\Pr[B_{S_k}] \ge \prod_{i \le k}(1 - x_i)$ by induction on $k$. For $k = 0$ both sides are 1. If it holds for $k - 1$, then $\Pr[B_{S_{k-1}}] > 0$ because each $x_i < 1$, so the claim applies with $S = S_{k-1}$ and $i = k$:
$$ \Pr[B_{S_k}] = \Pr[B_{S_{k-1}}]\,\bigl(1 - \Pr[A_k \mid B_{S_{k-1}}]\bigr) \ge \Pr[B_{S_{k-1}}]\,(1 - x_k) \ge \prod_{i \le k} (1 - x_i). $$
For $k = n$ this is the theorem. $\square$

### Theorem 2

*Case $d = 0$.* The graph has no edges, so each $A_i$ is mutually independent of all the others, and $\Pr[\bigcap_i \bar A_i] = \prod_i (1 - \Pr[A_i]) \ge (1 - p)^n$. The condition gives $p \le 1/e < 1$, so this is positive.

*Case $d \ge 1$.* Put $x_i = 1/(d+1)$ for each $i$, which lies in $[0, 1)$. Each $\Gamma(i)$ has at most $d$ elements, and each factor is less than 1, so
$$ x_i \prod_{j \in \Gamma(i)} (1 - x_j) \ \ge\ \frac{1}{d+1}\Bigl(\frac{d}{d+1}\Bigr)^{d} = \frac{1}{d+1} \cdot \frac{1}{(1 + 1/d)^{d}} \ \ge\ \frac{1}{e\,(d+1)} \ \ge\ p \ \ge\ \Pr[A_i]. $$
The second inequality uses $1 + y \le e^y$ with $y = 1/d$, so $(1 + 1/d)^d \le e$. The third is the hypothesis $e\,p\,(d+1) \le 1$. Theorem 1 applies and gives $\Pr[\bigcap_i \bar A_i] \ge (1 - 1/(d+1))^n = (d/(d+1))^n$. $\square$

### Theorem 3

The full proof is in [the Moser-Tardos analysis](proofs/moser-tardos.md). Its plan is as follows.

1. Draw all randomness from a table: for each variable, an infinite list of independent samples, used in order. This does not change the distribution of the run.
2. Write the *log* $C(1), C(2), \ldots$ of resampled events. For a step $t$, build a *witness tree* $\tau(t)$: the root has label $C(t)$; going back over the steps $s = t-1, \ldots, 1$, attach a vertex with label $C(s)$ below the deepest vertex whose label shares a variable with $C(s)$, and skip $s$ if there is none.
3. In such a tree, two vertices whose labels share a variable lie at different depths, and the one from the earlier step is deeper. So the children of each vertex have distinct labels (the tree is *proper*), and each step that touched a variable of a vertex label before that vertex is in the tree.
4. Fix a proper tree $\tau$. Visit its vertices from the deepest level up, and test each label on fresh entries of the table. This test passes with probability $\prod_{v} \Pr[[v]]$. By step 3, if $\tau$ occurs in the log, the test reads exactly the values that the run had when it resampled each label, so it passes. Hence $\Pr[\tau \text{ occurs}] \le \prod_v \Pr[[v]]$.
5. The $k$-th resampling of $A$ gives a tree with root $A$ and exactly $k$ vertices with label $A$, so distinct resamplings give distinct trees. So $\mathbb E[N_A] \le \sum_{\tau} \prod_v \Pr[[v]]$, over the proper trees $\tau$ with root $A$.
6. A random branching process, in which each vertex with label $B$ gets a child with label $C$ with probability $x(C)$ for each $C$ equal to $B$ or adjacent to it, yields each such tree $\tau$ with probability $\frac{1 - x(A)}{x(A)} \prod_v x([v]) \prod_{C \in \Gamma([v])} (1 - x(C))$. These probabilities add up to at most 1. With the hypothesis, the sum of step 5 is at most $x(A)/(1-x(A))$.

The algorithm stops only when no event holds. So Theorem 3 also proves Theorem 1 in the variable setting, without the bound on the probability.

## Consequences

### k-SAT

Let $F$ be a [k-SAT](/k-sat/) formula in [conjunctive normal form](/conjunctive-normal-form/) where each clause has exactly $k$ literals on $k$ distinct variables. Give each variable the value true or false with probability $\frac12$ each, independently. Let $A_C$ be the event that clause $C$ is false. Then $\Pr[A_C] = 2^{-k}$, the event depends only on the variables of $C$, and two clauses are adjacent when they share a variable.

**Corollary.** If each clause shares a variable with at most $d$ other clauses and $d \le 2^k/e - 1$, then $F$ is satisfiable, and MOSER-TARDOS finds a satisfying assignment after at most $m/d$ expected resampling steps, where $m$ is the number of clauses ($d \ge 1$). If each variable is in at most $L$ clauses, then $d \le k(L - 1)$.

This is Theorem 2 and Theorem 3 with $p = 2^{-k}$. The union bound gives a different condition: $\Pr[\text{some clause is false}] \le m\,2^{-k}$, so $F$ is satisfiable if $m \le 2^k - 1$. The union bound limits the number of clauses; the local lemma limits only the overlap of each clause, and $m$ can be as large as you like.

| $k$ | $2^k/e - 1$ | largest $d$ | largest $L$ from $d \le k(L-1)$ | union bound: largest $m$ | resamplings per clause, $1/d$ |
|---|---|---|---|---|---|
| 3 | 1.94 | 1 | 1 | 7 | 1 |
| 4 | 4.89 | 4 | 2 | 15 | 0.25 |
| 5 | 10.77 | 10 | 3 | 31 | 0.1 |
| 6 | 22.54 | 22 | 4 | 63 | 0.0455 |
| 7 | 46.09 | 46 | 7 | 127 | 0.0217 |
| 8 | 93.18 | 93 | 12 | 255 | 0.0108 |
| 9 | 187.35 | 187 | 21 | 511 | 0.0053 |
| 10 | 375.71 | 375 | 38 | 1023 | 0.0027 |

The formula that has all $2^k$ clauses on the same $k$ variables is unsatisfiable, and each of its clauses meets $d = 2^k - 1$ others. So the threshold of the corollary is within a factor of about $e$ of a real obstruction: the ratio $2^k / (d_{\max} + 1)$ of this formula to the corollary is 2.723 for $k = 7$ to $10$.

### The bound against the exact probability

The general form can succeed where the symmetric form fails. Take $2m$ variables $y_1, \ldots, y_{2m}$ with $y_{2m+1} = y_1$, and the $m$ clauses
$$ C_j = y_{2j-1} \vee y_{2j} \vee y_{2j+1}, \qquad j = 1, \ldots, m. $$
For $m \ge 3$ each clause shares one variable with $C_{j-1}$ and one with $C_{j+1}$ (indices mod $m$), so $d = 2$ and $p = 1/8$. The symmetric condition fails: $e \cdot \frac18 \cdot 3 = 1.019 > 1$. The general form with all $x_j = x$ needs $\frac18 \le x(1-x)^2$. The identity $x(1-x)^2 - \frac18 = (x - \frac12)(x^2 - \frac32 x + \frac14)$ shows that the least solution is $x^* = (3 - \sqrt5)/4 = 0.1910$. So Theorem 1 gives $\Pr[F \text{ true}] \ge ((1 + \sqrt5)/4)^m = 0.8090^m$. With the natural choice $x = 1/(d+1) = 1/3$, the condition holds too ($4/27 = 0.1481 \ge 0.125$), and the bound is $(2/3)^m$.

The exact probability follows from a transfer matrix. Given the values of $y_{2j-1}$ and $y_{2j+1}$, the number of values of $y_{2j}$ that make $C_j$ true is 1 if both are false and 2 otherwise. So $\Pr[F \text{ true}] = \mathrm{tr}(M^m)/4^m$ with $M = \begin{pmatrix} 1 & 2 \\ 2 & 2 \end{pmatrix}$, whose larger eigenvalue is $(3 + \sqrt{17})/2$. The exact probability decays like $0.8904^m$.

| $m$ | exact $\Pr[F \text{ true}]$ | LLL bound, $x^* = 0.1910$ | LLL bound, $x = 1/3$ | union bound $1 - m/8$ |
|---|---|---|---|---|
| 4 | 161/256 = 0.6289 | 0.4284 | 0.1975 | 0.5 |
| 8 | 0.3950 | 0.1835 | 0.03902 | 0 (no conclusion) |
| 16 | 0.1561 | 0.03368 | 0.001522 | negative |
| 32 | 0.02435 | 0.001134 | 2.318e-6 | negative |
| 64 | 5.930e-4 | 1.286e-6 | 5.372e-12 | negative |

The union bound stops working at $m = 8$. The local lemma gives a positive bound for every $m$, and its rate $0.8090$ per clause is close to the true rate $0.8904$.

For MOSER-TARDOS on the same formula, with the rule "resample the false clause of least index" in line L3, the expected number of resampling steps is the solution of a linear system over the $4^m$ assignments. Theorem 3 with $x^*$ bounds it by $m\,x^*/(1-x^*) = m(\sqrt5 - 2) = 0.2361\,m$.

| $m$ | exact expected resamplings | bound $m(\sqrt5 - 2)$ | expected false clauses at the start, $m/8$ |
|---|---|---|---|
| 3 | 0.3761 | 0.7082 | 0.375 |
| 4 | 0.4973 | 0.9443 | 0.5 |
| 5 | 0.6228 | 1.1803 | 0.625 |
| 6 | 0.7478 | 1.4164 | 0.75 |

### Hypergraph 2-coloring

A [hypergraph](/hypergraph/) has *property B* if its vertices can be colored with two colors so that no edge is monochromatic. Let $H$ be $k$-uniform, and color each vertex red or blue with probability $\frac12$ each, independently. An edge is monochromatic with probability $2 \cdot 2^{-k} = 2^{1-k}$, and this event depends only on the colors of its own vertices. So if each edge meets at most $d$ other edges and $e\,(d+1) \le 2^{k-1}$, then $H$ is 2-colorable, and MOSER-TARDOS finds a coloring. For $k = 4$ to $10$ the largest such $d$ is 1, 4, 10, 22, 46, 93 and 187. The union bound needs fewer than $2^{k-1}$ edges in total. This is the question that led Erdős and Lovász to the lemma. A bound on the degree of the vertices does not by itself help the union bound, but it does here: if each vertex is in at most $\Delta$ edges, each edge meets at most $k(\Delta - 1)$ others.

### Ramsey numbers

Color the edges of the complete graph on $N$ vertices at random, and let the bad events be the monochromatic copies of $K_k$. Two copies are adjacent when they share an edge. The local lemma gives a lower bound for the diagonal Ramsey numbers of [Ramsey's theorem](/ramsey-theorem/), $R(k,k) > (1 + o(1)) \frac{\sqrt2}{e}\, k\, 2^{k/2}$, twice the bound of the plain union bound argument (Alon and Spencer, Chapter 5).

## Tightness

**The constant $e$ (Shearer 1985).** For $d \ge 1$, let $f(d)$ be the supremum of the numbers $p$ such that, for all events with probabilities at most $p$ and a dependency graph of maximum degree at most $d$, the probability that none happens is positive. Shearer proved $f(1) = \frac12$ and $f(d) = (d-1)^{d-1}/d^d$ for $d \ge 2$, so $d\,f(d) \to 1/e$. So for each $p > f(d)$ there are events with probabilities at most $p$ and a dependency graph of maximum degree at most $d$ such that, with probability 1, at least one of the events happens.

| $d$ | Shearer $f(d)$ | symmetric LLL, $1/(e(d+1))$ | ratio $f(d) \cdot e(d+1)$ |
|---|---|---|---|
| 1 | 0.5 | 0.1839 | 2.718 |
| 2 | 0.25 | 0.1226 | 2.039 |
| 3 | 0.1481 | 0.09197 | 1.611 |
| 10 | 0.03874 | 0.03344 | 1.158 |
| 100 | 0.003697 | 0.003642 | 1.015 |
| 1000 | 3.681e-4 | 3.675e-4 | 1.0015 |

So the condition $c\,p\,(d+1) \le 1$ does not suffice for all $d$ when $c < e$: for large $d$, $1/(c(d+1)) > f(d)$. In the other direction, Shearer's value gives a slightly stronger sufficient condition, $e\,p\,d \le 1$ for $d \ge 1$. For $d \ge 2$, $f(d) = \frac1d (1 - \frac1d)^{d-1}$, and $(1 - \frac1d)^{d-1} > 1/e$ because $\ln\frac{d}{d-1} < \frac{1}{d-1}$ (from $\ln(1+y) < y$ for $y > 0$). So $1/(ed) < f(d)$, and for $d = 1$, $1/e < \frac12$.

**For k-SAT.** The all-clauses formula above shows that the k-SAT corollary is within a factor of about $e$. In terms of variable occurrences, Gebauer, Szabó and Tardos (2016) built unsatisfiable k-CNF formulas in which each variable is in at most $(2/e + o(1))\,2^k/k$ clauses, and they showed with a lopsided form of the lemma that this number is asymptotically the threshold.

### Pitfalls

- **Pairwise independence is not enough.** Let $u, w$ be independent fair bits, and $A_1 = \{u = 0\}$, $A_2 = \{w = 0\}$, $A_3 = \{u = w\}$. Each event has probability $\frac12$ and each pair is independent. But $\bar A_1 \cap \bar A_2 \cap \bar A_3 = \{u = 1, w = 1, u \ne w\}$ is empty. The empty graph is not a dependency graph here, because $A_3$ is not mutually independent of $\{A_1, A_2\}$: $\Pr[A_3 \mid A_1 \cap A_2] = 1$. With the empty graph and $x_i = \frac12$, Theorem 1 would wrongly give the bound $(\frac12)^3 > 0$.
- **$d$ counts the other events.** The degree does not count the event itself, and the condition is $e\,p\,(d+1) \le 1$. In the cyclic example, $d = 2$ and the symmetric form fails, but the general form with a good choice of $x_i$ works.
- **Positive, not large.** The guaranteed probability $\prod_i (1 - x_i)$ is exponentially small in $n$. For the cyclic formula with $m = 64$ the bound is $1.286 \times 10^{-6}$ and the truth is $5.930 \times 10^{-4}$: drawing fresh random assignments until one works takes $1/(5.930 \times 10^{-4}) = 1686.2$ draws on average, while MOSER-TARDOS needs at most $64(\sqrt5 - 2) = 15.11$ expected resamplings.
- **The algorithm needs the variable setting.** Theorem 3 needs events that are functions of independent variables, with the graph of shared variables. Theorem 1 in its abstract form, for example for events on a random permutation, does not give an algorithm by itself.
- **The weights must be below 1.** With $x_i = 1$ the factor $1 - x_i$ is 0 and the bound says nothing. The proof divides by $\Pr[B_{S_1} \mid B_{S_2}]$, which needs each $x_j < 1$.

## History

Erdős and Lovász introduced the lemma in 1975, in a paper on 3-chromatic hypergraphs, that is, hypergraphs without property B. Shearer (1985) found the exact threshold $f(d)$ of the symmetric case, which shows that the constant $e$ is asymptotically best. Beck (1991) gave polynomial-time algorithms for some applications, with a weaker constant: for example, a 2-coloring of an $n$-uniform hypergraph in which each edge meets at most $2^{n/48}$ others. Moser (2009) gave a resampling algorithm for k-SAT formulas whose clauses overlap few others, and Moser and Tardos (2010) proved Theorem 3 for the general form in the variable setting, with the witness tree argument. Gebauer, Szabó and Tardos (2016) showed that the lemma is asymptotically tight for k-SAT with bounded variable occurrences.

## References
