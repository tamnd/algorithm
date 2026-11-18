---
tag: 41NFV7
kind: theorem
slug: weak-acyclicity
name: Weak acyclicity and chase termination
aliases:
- weakly acyclic dependencies
area: databases/data-integration-and-cleaning
level: advanced
summary: "If the dependency graph of the tgds has no cycle through a special edge, each chase stops in polynomially many steps, for a fixed set of dependencies, in the size of the instance (data complexity)."
prereqs: [tuple-generating-dependency, equality-generating-dependency, chase-algorithm, data-and-combined-complexity]
see_also: [data-exchange-problem, universal-solution, data-exchange-core-computation, certain-answers, schema-mapping, undecidability]
sources:
  - paper: doi:10.1016/j.tcs.2004.10.033
    title: "Ronald Fagin, Phokion G. Kolaitis, Renée J. Miller and Lucian Popa, Data exchange: semantics and query answering, Theoretical Computer Science 336(1), 2005"
    locator: weakly acyclic sets of tgds and the polynomial bound on the length of chase sequences
  - book: isbn:9781107016163
    title: "Marcelo Arenas, Pablo Barceló, Leonid Libkin and Filip Murlak, Foundations of Data Exchange, Cambridge University Press, 2014"
    locator: "Chapter 5, Existence of solutions"
---

Weak acyclicity is a syntactic condition on a set of [tuple-generating dependencies](/tuple-generating-dependency/) (tgds) that makes the chase stop. If no cycle of the dependency graph goes through a special edge, then every chase sequence with these tgds and any set of [equality-generating dependencies](/equality-generating-dependency/) (egds) has a length bounded by a polynomial in the size of the instance. The bound is in data complexity: the polynomial depends on the fixed set of dependencies. The condition is sufficient for termination but not necessary. This page proves the termination theorem; the [data exchange problem](/data-exchange-problem/) page uses it as its standard assumption on target dependencies, and the [universal solution](/universal-solution/) page uses the chase result it guarantees.

## Statement

A tgd has the form $\forall x\, \forall u\, (\varphi(x, u) \to \exists y\, \psi(x, y))$. The variables $x$ occur in the body and in the head and are the *frontier* variables. The variables $y$ are the *existential* variables. An egd has the form $\forall x\, (\varphi(x) \to x_i = x_j)$. Values are constants or labeled nulls $\bot_1, \bot_2, \ldots$, and instances are sets of facts.

**Positions and the dependency graph.** A *position* is a pair $(R, i)$ of a relation $R$ and an argument number $i$. The *dependency graph* of a set $\Sigma$ of tgds has the positions as nodes. For each tgd of $\Sigma$, each frontier variable $x$ and each position $p$ where $x$ occurs in the body:

- there is a *regular edge* from $p$ to each position where $x$ occurs in the head;
- there is a *special edge* from $p$ to each position where an existential variable occurs in the head.

$\Sigma$ is *weakly acyclic* if no cycle of the dependency graph goes through a special edge.

**Chase steps.** Let $K$ be an instance. A *tgd step* uses a tgd and a map $h$ of its body into $K$ such that no extension of $h$ maps the head into $K$. It adds the facts $\psi(h(x), N)$, with fresh nulls $N$ for the existential variables. An *egd step* uses an egd and a map $h$ of its body into $K$ with $h(x_i) \neq h(x_j)$. If both values are constants, the chase *fails*. Otherwise it replaces a null among the two by the other value everywhere in $K$. A *chase sequence* of $I$ with $\Sigma$ starts at $K_0 = I$ and makes one step at a time.

**Theorem.** Let $\Sigma$ be a finite set of tgds and egds whose tgds are weakly acyclic. There is a polynomial $p_\Sigma$ such that, for each instance $I$, each chase sequence of $I$ with $\Sigma$ has at most $p_\Sigma(|I|)$ steps. So for a fixed $\Sigma$, each chase stops, with a result or with a failure, after a number of steps polynomial in the size of $I$ (data complexity).

## In plain words

The chase repairs an instance by adding missing facts. Some rules invent new unknown values, and an invented value can trigger a rule that invents another one, and so on forever.

Draw a graph whose nodes are the columns of the relations. Draw an arrow when a rule copies a value from one column to another, and a marked arrow when a rule invents a value in a column because of a value in another column. If no loop of arrows contains a marked arrow, invented values cannot keep making new invented values: the depth of invention has a limit. So the number of invented values is bounded by a polynomial in the size of the data, and the chase must stop. The rules that make two values equal only remove values, so they do not break this.

## Proof

Let $n$ be the number of values of $I$, let $P$ be the number of positions, let $k$ be the largest number of frontier variables and $w$ the largest number of existential variables of a tgd of $\Sigma$.

**Rank.** The *rank* of a position $p$ is the largest number of special edges on a walk that ends at $p$. If a walk had $P + 1$ special edges, two of their end positions would be equal. The part of the walk between them is a closed walk that contains a special edge $u \to v$. The rest of that closed walk goes from $v$ back to $u$ and contains a simple path from $v$ to $u$, so the edge and the path form a cycle through a special edge. This is false for a weakly acyclic set, so each rank is at most $P$. A regular edge $q \to p$ gives $\mathrm{rank}(q) \le \mathrm{rank}(p)$, and a special edge $q \to p$ gives $\mathrm{rank}(q) < \mathrm{rank}(p)$. Let $P_{\le j}$ be the set of positions of rank at most $j$.

**Three facts about steps.**

1. A tgd step puts at a head position $p$ either a value $h(x)$ of a frontier variable, which already occurs at a body position $q$ with a regular edge $q \to p$, so $q \in P_{\le \mathrm{rank}(p)}$; or a fresh null. In the second case each frontier variable occurs only at body positions with a special edge to $p$, so all frontier values come from $P_{\le \mathrm{rank}(p) - 1}$.
2. An egd step that does not fail replaces one null $a$ by a value $b$ everywhere. After it, $a$ never occurs again, because each later null is fresh.
3. For times $t < t'$, let $s_{t,t'}$ be the composition of the replacements of the egd steps between $t$ and $t'$. Then $s_{t,t'}(K_t) \subseteq K_{t'}$, because a tgd step only adds facts and an egd step applies its replacement to all facts.

**Tokens.** Fix $j$. We hand out *tokens* to the values that occur at positions of $P_{\le j}$. At time 0, each such value of $I$ gets a new token. When a tgd step puts a fresh null at a position of $P_{\le j}$, the null gets a new token. When an egd step replaces $a$ by $b$, and $a$ holds a token and $b$ holds none, then $b$ takes the token of $a$; otherwise the token of $a$, if any, is dropped. By induction on the steps, using fact 1 for copied values and fact 2 for egd steps, two statements hold at each time $t$.

- (T1) Each value that occurs at a position of $P_{\le j}$ holds exactly one token, and no two values hold the same token.
- (T2) If a token is held by $u$ at time $t$ and by $u'$ at a later time $t'$, then $u' = s_{t,t'}(u)$.

Let $N_j$ be the number of tokens created at level $j$ over the whole sequence. Then $N_j \le n + (\text{the number of fresh nulls placed at positions of } P_{\le j})$.

**One tgd fires a bounded number of times.** Let $d$ be a tgd whose frontier variables $x_1, \ldots, x_k$ all occur at body positions of $P_{\le i}$. Map each step that applies $d$ at time $t$, with the map $h$, to the tuple of tokens at level $i$ held by $h(x_1), \ldots, h(x_k)$ at time $t$. Assume that two steps at times $t < t'$, with maps $h$ and $h'$, give the same tuple. The step at $t$ adds $\psi(h(x), N)$, so by fact 3, $K_{t'}$ contains $\psi(s(h(x)), s(N))$ for $s = s_{t+1,t'}$. By (T1) and (T2), $h'(x_l) = s(h(x_l))$ for each $l$. Then $h'$ extends to the head by $y \mapsto s(N)$, so the step at $t'$ is not a tgd step, which is a contradiction. So $d$ fires at most $N_i^k$ times if $k \ge 1$, and at most once if $k = 0$, as its head then holds forever. In both cases the count is at most $(N_i + 1)^k$.

**The recursion.** By fact 1, a fresh null at a position of rank at most $j$ comes from a tgd whose frontier variables all occur at positions of rank at most $j - 1$. Each step makes at most $w$ nulls. So, with $N_{-1} = 0$,

$$N_j \le n + |\Sigma| \, w \, (N_{j-1} + 1)^k.$$

By induction on $j$, $N_j$ is at most a polynomial in $n$ of degree at most $\max(1, k)^j$, with coefficients that depend only on $\Sigma$. Each position has rank at most $P$, so $N_P$ bounds the number of all values that ever occur.

**The length.** Each tgd has its frontier variables at positions of rank at most $P$, so by the bound above there are at most $|\Sigma| (N_P + 1)^k$ tgd steps. By fact 2, each egd step that does not fail removes a null for good, so there are at most $N_P$ of them, and at most one step fails. So each chase sequence has at most

$$p_\Sigma = |\Sigma| (N_P + 1)^k + N_P + 1$$

steps. Since $n$ is at most the largest arity times $|I|$, this is a polynomial in $|I|$ for a fixed $\Sigma$. $\blacksquare$

## Consequences

- **Existence of solutions.** Let a [schema mapping](/schema-mapping/) have source-to-target tgds and target dependencies that are egds and weakly acyclic tgds. Then run a chase. If it fails, no solution exists. If it succeeds, the result is a [universal solution](/universal-solution/). So the existence of a solution is decidable in polynomial time in data complexity. Without a condition of this kind the problem is undecidable in general.
- **Query answering.** The [certain answers](/certain-answers/) of a union of conjunctive queries are the null-free answers of naive evaluation on the chase result, so they take polynomial time in data complexity.
- **The core.** Gottlob and Nash showed that the core of the universal solutions can then also be computed in polynomial time in data complexity (see [core computation for data exchange](/data-exchange-core-computation/)).
- **Any order of steps.** The bound holds for each chase sequence, so an implementation may choose the order of the steps freely.

## Tightness

- **Sufficient, not necessary.** Take the single tgd $\forall x, y\, (R(x, y) \wedge S(y) \to \exists z\, R(y, z))$. The variable $y$ occurs at $(R, 2)$ in the body and $z$ occurs at $(R, 2)$ in the head, so there is a special edge from $(R, 2)$ to itself, and the set is not weakly acyclic. But each chase stops: a step needs $S(y)$, no step adds to $S$, and after one step with a given $y$ the head holds for $y$. So there are at most $|S^I|$ steps.
- **Without the condition, the chase may not stop.** With $\forall x, y\, (E(x, y) \to \exists z\, E(y, z))$ and $I = \{E(a, b)\}$, each step adds a fact $E(\bot_i, \bot_{i+1})$ whose new null starts a new step. The special edge from $(E, 2)$ to itself is a cycle.
- **The bound is not polynomial in combined complexity.** Take the tgds $R(x) \wedge R(y) \to \exists z\, S_1(x, y, z)$ and, for $1 \le i < r$, $S_i(x, y, z) \wedge S_i(x', y', z') \to \exists v\, S_{i+1}(z, z', v)$, each with all its variables universally quantified. All edges go from $S_i$ to $S_{i+1}$, so the set is weakly acyclic, and $(S_i, 3)$ has rank $i$. Each pair of nulls of $S_i$ gives a new fact, so $|S_i| = n^{2^i}$ for $n$ values in $R$. With $n = 2$ and $r = 3$, the chase makes facts in the counts 4, 16 and 256. The number of steps is doubly exponential in the number of tgds, so the degree of $p_\Sigma$ must grow with $\Sigma$.

## History

Fagin, Kolaitis, Miller and Popa defined weakly acyclic sets of tgds and proved the polynomial bound on chase sequences in their paper on data exchange, presented at ICDT 2003 and published in Theoretical Computer Science in 2005. Before that, the chase was mostly used with full dependencies, which make no new values and so always stop. Weak acyclicity became the usual assumption on target dependencies in data exchange, and later work found larger classes of tgds with a terminating chase.

## References
