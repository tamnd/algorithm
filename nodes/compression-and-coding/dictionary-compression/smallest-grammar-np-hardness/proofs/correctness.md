---
title: The reduction from vertex cover to the smallest grammar problem
proves: [statement]
status: full
---

We follow the reduction of Charikar et al. (2005, Section V-A), which they base on arguments of Storer and Szymanski. The lower bound below is our own argument by phrase sets; it gives the exact value of the smallest grammar and needs no bound on the degree. The degree bound is used only for the constant $8569/8568$.

Throughout, the size $|G|$ of a grammar is the total length of its right-hand sides, and $g^{*}(w)$ is the smallest size of a grammar that derives $w$.

## The construction

Let $H = (V, E)$ be a simple graph with $V = \{v_1, \ldots, v_p\}$. Write each edge once, as $(v_i, v_j)$ with $i < j$. The alphabet has one symbol $\#$, one symbol $v_i$ for each vertex, and one fresh separator symbol for each place where $\mid$ appears below; each separator occurs exactly once in the string. Let

$$\sigma_H = \prod_{i=1}^{p} \big( \#v_i \mid v_i\# \mid \big)^{2} \;\cdot\; \prod_{i=1}^{p} \big( \#v_i\# \mid \big) \;\cdot\; \prod_{(v_i, v_j) \in E} \big( \#v_i\#v_j\# \mid \big).$$

Its length is $12|V| + 4|V| + 6|E|$, and it has $5|V| + |E|$ separators. The map $H \mapsto \sigma_H$ takes polynomial time. Let $\tau(H)$ be the size of a minimum [vertex cover](/vertex-cover/) of $H$.

**Theorem.** $g^{*}(\sigma_H) = 15|V| + 3|E| + \tau(H)$. Moreover, from any grammar $G$ for $\sigma_H$ one can compute in polynomial time a vertex cover of $H$ of size at most $|G| - 15|V| - 3|E|$.

## Upper bound

Let $C$ be a vertex cover. Use the rules $A_i \to \#v_i$ and $B_i \to v_i\#$ for each $i$, and $D_i \to A_i \#$ for each $v_i \in C$. In the start rule, write:

- each block $\#v_i$ and $v_i\#$ of the first product as $A_i$ or $B_i$: 4 symbols for each vertex;
- the block $\#v_i\#$ as $D_i$ if $v_i \in C$ (1 symbol), and as $A_i \#$ otherwise (2 symbols);
- the block $\#v_i\#v_j\#$ as $D_i B_j$ if $v_i \in C$, and as $A_i D_j$ otherwise, which is possible because $C$ covers the edge (2 symbols);
- each separator as itself: $5|V| + |E|$ symbols.

So the start rule has length $(5|V| + |E|) + 4|V| + (2|V| - |C|) + 2|E|$. The rules $A_i$ and $B_i$ cost $4|V|$, and the rules $D_i$ cost $2|C|$. The total is

$$(5|V| + |E|) + 4|V| + (2|V| - |C|) + 2|E| + 4|V| + 2|C| \;=\; 15|V| + 3|E| + |C|.$$

With $|C| = \tau(H)$, this gives $g^{*}(\sigma_H) \le 15|V| + 3|E| + \tau(H)$.

## Lower bound

**Step 1: a normal form.** Let $G$ be any grammar for $\sigma_H$. Apply these changes while one applies, and apply change 4 only when none of changes 1 to 3 applies. Each one keeps the derived string and lowers $|G|$ by at least 1, so at most $|G|$ changes happen, and each takes polynomial time.

1. A nonterminal that is not reachable from the start symbol: delete its rule.
2. A rule $A \to x$ with a right-hand side of length 1: replace each use of $A$ by $x$ and delete the rule. The size drops by 1.
3. A nonterminal $A$ other than the start symbol, used exactly once in all right-hand sides: put its right-hand side $\alpha$ in place of the use and delete the rule. The size drops from $|\alpha| + 1$ to $|\alpha|$.
4. Two nonterminals $A \ne B$ with the same expansion: replace each use of $B$ by $A$ and delete the rule of $B$. The size drops by the length of that rule. The result has no cycle, because no nonterminal in the derivation of $A$ has an expansion as long as that of $A$ (by rule 2, each right-hand side has length at least 2, so each proper part of a derivation is shorter).

At the end, every rule other than the start rule has length at least 2, every nonterminal other than the start symbol is used at least twice, and distinct nonterminals have distinct expansions. Call such a grammar *normal*. Since $|G|$ did not grow, it is enough to bound the size of normal grammars.

**Step 2: the possible phrases.** Let $G$ be normal and let $D$ be the set of expansions of its nonterminals other than the start symbol. Take $p \in D$, the expansion of $A$. Then $|p| \ge 2$. $A$ is used at least twice in reachable rules, so it labels at least two nodes of the derivation tree. Two such nodes start at different positions of $\sigma_H$: if they started at the same position, one would be a proper ancestor of the other (two nodes with the same start position lie on one root path), and a proper descendant has a shorter expansion. So $p$ occurs at least twice in $\sigma_H$, and $p$ contains no separator, because each separator occurs once. A string with no separator lies inside one block $\#v_i$, $v_i\#$, $\#v_i\#$ or $\#v_i\#v_j\#$. Each string of length at least 2 inside an edge block that contains both $v_i$ and $v_j$ contains $v_i\#v_j$, and this string occurs only in the block of the edge $(v_i, v_j)$, which appears once because $H$ is simple. The string $\#\#$ never occurs. Hence

$$D \subseteq \{\#v_i,\ v_i\#,\ \#v_i\# : 1 \le i \le p\}.$$

**Step 3: size of a grammar with phrase set $D$.** For a string $u$ and a set $D'$ of strings, let $P(u, D')$ be the least number of pieces in a cut of $u$ into single symbols and strings of $D'$. Each symbol in the start rule of $G$ is a terminal or a nonterminal with expansion in $D$, so the start rule has length at least $P(\sigma_H, D)$. For a rule $A \to \alpha$ with expansion $p$, each symbol of $\alpha$ expands to a single symbol or to a string of $D$ that is shorter than $p$ (because $|\alpha| \ge 2$), so $|\alpha| \ge P(p, D \setminus \{p\})$. Therefore

$$|G| \ \ge\ P(\sigma_H, D) + \sum_{p \in D} P(p, D \setminus \{p\}).$$

No string of $D$ contains a separator, so a cut of $\sigma_H$ is a cut of each block between separators, and $P(\sigma_H, D)$ is $5|V| + |E|$ (the separators) plus the sum of $P(\beta, D)$ over the blocks $\beta$.

**Step 4: counting.** Let $a_i, b_i, c_i \in \{0, 1\}$ tell whether $\#v_i$, $v_i\#$, $\#v_i\#$ lie in $D$, and let $C = \{v_i : c_i = 1\}$.

- *The strings $\#v_i$ and $v_i\#$.* The two blocks $\#v_i$ cost $2(2 - a_i)$, and the rule for $\#v_i$, if present, costs $2 a_i$. Together they cost exactly 4, for each value of $a_i$. The same holds for $v_i\#$. This gives $8|V|$.
- *The string $\#v_i\#$.* If $c_i = 1$, the block costs 1 and its rule costs at least 2, so at least 3. If $c_i = 0$, the block has length 3, and no string of $D$ has length 3 except the $\#v_k\#$, which differ from it, so it costs at least 2. In both cases the cost is at least $2 + c_i$, which gives $2|V| + |C|$.
- *The edge block $\#v_i\#v_j\#$.* It has length 5 and the strings of $D$ have length at most 3, so it costs at least 2. If it costs exactly 2, its two pieces have lengths 3 and 2, and the piece of length 3 is $\#v_i\#$ or $\#v_j\#$, so $v_i \in C$ or $v_j \in C$. So an edge with no end in $C$ costs at least 3. This gives $2|E| + u$, where $u$ is the number of edges with no end in $C$.

Adding up,

$$|G| \ \ge\ (5|V| + |E|) + 8|V| + 2|V| + |C| + 2|E| + u \;=\; 15|V| + 3|E| + |C| + u.$$

Let $C'$ be $C$ plus one end of each edge with no end in $C$. Then $C'$ is a vertex cover with $|C'| \le |C| + u \le |G| - 15|V| - 3|E|$, and $C'$ is computed in polynomial time from the normal form of $G$. Since $\tau(H) \le |C'|$, every grammar has size at least $15|V| + 3|E| + \tau(H)$. With the upper bound, this proves the theorem. $\square$

## NP-hardness

Vertex cover is NP-complete, also on graphs of maximum degree 3 (Garey and Johnson, problem GT1). By the theorem, $H$ has a vertex cover of size at most $t$ if and only if $g^{*}(\sigma_H) \le 15|V| + 3|E| + t$. So the decision version of the smallest grammar problem is NP-hard. It is in NP (see the [problem page](/smallest-grammar-problem/)), so it is NP-complete. $\square$

## The constant 8569/8568

Berman and Karpinski (1998) show that, unless P = NP, no polynomial-time algorithm approximates the minimum vertex cover within a ratio below $145/144$ on graphs of maximum degree 3; Charikar et al. use this result for graphs with $|E| \ge |V|$.

Suppose an algorithm $\mathcal{A}$ finds, in polynomial time, a grammar of size at most $\rho \cdot g^{*}(w)$ for each string $w$, with $\rho < 8569/8568$. Given such a graph $H$, build $\sigma_H$, run $\mathcal{A}$, and turn its grammar $G$ into the cover $C'$ of the theorem. Write $k = \tau(H)$ and $s = 15|V| + 3|E|$. Then

$$|C'| \ \le\ |G| - s \ \le\ \rho (s + k) - s \ =\ k + (\rho - 1)(s + k).$$

Each vertex covers at most 3 edges, so $k \ge |E|/3 \ge |V|/3$, and $|E| \le 3|V|/2$. Hence $s \le 15|V| + 4.5|V| = 19.5|V| \le 58.5\, k$, and $s + k \le 59.5\, k$. So

$$|C'| \ \le\ k\big(1 + 59.5(\rho - 1)\big) \ <\ k \Big(1 + \frac{59.5}{8568}\Big) \ =\ \frac{145}{144}\, k,$$

because $59.5 \cdot 144 = 8568$. This approximates the minimum vertex cover within a ratio below $145/144$ in polynomial time, so P = NP. Hence no polynomial-time algorithm for the smallest grammar problem has ratio below $8569/8568$ unless P = NP. $\blacksquare$
