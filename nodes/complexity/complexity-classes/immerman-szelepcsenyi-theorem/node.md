---
tag: M3PPF9
kind: theorem
slug: immerman-szelepcsenyi-theorem
name: Immerman-Szelepcsényi theorem
aliases:
- NL equals co-NL
area: complexity/complexity-classes
level: advanced
summary: Nondeterministic space s(n) at least log n is closed under complement, so NL = coNL. The proof counts the reachable configurations by induction on the path length.
prereqs: [nondeterministic-logspace, graph-reachability, co-np]
see_also: [savitch-theorem, space-hierarchy-theorem, 2-sat, logspace, nondeterministic-turing-machine, pspace]
sources:
  - paper: doi:10.1137/0217058
    title: Neil Immerman, Nondeterministic space is closed under complementation, SIAM Journal on Computing 17(5), 935 to 938 (1988)
    locator: the main theorem and the inductive counting
  - paper: doi:10.1007/BF00299636
    title: Róbert Szelepcsényi, The method of forced enumeration for nondeterministic automata, Acta Informatica 26(3), 279 to 284 (1988)
    locator: closure under complement of nondeterministic L(n) tape-bounded languages for L(n) at least log n
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage (2013)
    locator: Section 8.6, NL Equals coNL
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 4, Space Complexity (NL = coNL)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley (1994)
    locator: Chapter 7, Relations between Complexity Classes (the reachability method and nondeterministic space)
---

The Immerman-Szelepcsényi theorem says that nondeterministic space is closed under complement: for space-constructible $s(n) \ge \log n$, a language is in $\mathsf{NSPACE}(s(n))$ if and only if its complement is. In particular $\mathsf{NL} = \mathsf{coNL}$. The heart of the proof is a nondeterministic logspace algorithm that certifies that a vertex $t$ is *not* reachable from $s$ in a directed graph. It first computes, by induction on $i$, the number of vertices reachable from $s$ in at most $i$ steps, and then it uses that number to make sure that it has seen every reachable vertex. The method is called *inductive counting*. Neil Immerman and Róbert Szelepcsényi found it independently and shared the Gödel Prize in 1995. The same question for time, whether $\mathsf{NP} = \mathsf{coNP}$, is open, and this theorem says nothing about it.

## Statement

The model is the nondeterministic multitape Turing machine with a read-only input tape; only the work tapes count; see [NL](/nondeterministic-logspace/). For a class $\mathcal{C}$, $\mathrm{co}\mathcal{C}$ is the class of complements $\{x : x \notin A\}$ of the languages $A \in \mathcal{C}$. A function $s$ is space-constructible if a deterministic machine writes $s(n)$ in binary on input $1^n$ with $O(s(n))$ work cells.

**Lemma.** The complement of directed reachability, $\overline{\mathrm{PATH}} = \{\langle G, s, t\rangle : G$ has no path from $s$ to $t\}$, is in NL.

**Theorem (Immerman 1988; Szelepcsényi 1988).** Let $s(n) \ge \log_2 n$ be space-constructible. Then

$$\mathsf{NSPACE}(s(n)) = \mathsf{coNSPACE}(s(n)).$$

In particular $\mathsf{NL} = \mathsf{coNL}$.

## In plain words

A guessing machine proves that a path exists by guessing it. To prove that no path exists is harder: it must check every route, with almost no memory.

The trick is to count. First the machine finds out how many places can be reached in at most one step, then in at most two steps, and so on. Each count comes from the one before. To check whether a place is reachable in one more step, the machine walks through all places again, guesses which of them were reachable before and proves each guess with a path. It counts the places it proved. If that number matches the earlier count, no reachable place was skipped.

At the end the machine knows the number of reachable places. It lists that many reachable places, each with a path. If the target is not among them, the target is not reachable.

## Proof

**Setup.** Let $G$ be a directed graph with vertices $1, \ldots, N$, a start vertex $s$ and a target $t$. For $i \ge 0$, let $R_i$ be the set of vertices reachable from $s$ by a path with at most $i$ edges, and let $c_i = |R_i|$. Then $R_0 = \{s\}$, $c_0 = 1$, and $R_{N-1}$ is the set of all vertices reachable from $s$.

A nondeterministic machine *computes* a value if every branch either rejects or ends with the correct value, and at least one branch ends with it. The routine below computes $c_{N-1}$ in this sense and then decides $\overline{\mathrm{PATH}}$.

A *path check* for a vertex $u$ and a length $i$ guesses a path from $s$ to $u$ with at most $i$ edges, one vertex at a time, and checks each edge on the input; the branch rejects if a guessed edge does not exist or if the path does not end at $u$ within $i$ edges. It stores the current vertex and a step counter, so it uses $O(\log N)$ bits. A branch passes the check for $u$ only if $u \in R_i$, and for each $u \in R_i$ some branch passes it.

```pseudo id=count
NONREACH(G, s, t)
L1   c ← 1
L2   for i ← 0 to N - 2 do
L3       c' ← 0
L4       for each vertex v do
L5           m ← 0; found ← false
L6           for each vertex u do
L7               guess a bit b
L8               if b = 1 then
L9                   path check for u with length i, or reject
L10                  m ← m + 1
L11                  if u = v or (u, v) ∈ E then found ← true
L12          if m ≠ c then reject
L13          if found then c' ← c' + 1
L14      c ← c'
L15  m ← 0
L16  for each vertex u do
L17      guess a bit b
L18      if b = 1 then
L19          path check for u with length N - 1, or reject
L20          m ← m + 1
L21          if u = t then reject
L22  if m = c then accept else reject
```

**Claim.** At the start of round $i$ of the loop at L2, every branch that has not rejected has $c = c_i$.

*Proof by induction on $i$.* For $i = 0$, line L1 sets $c = 1 = c_0$. Suppose $c = c_i$ at the start of round $i$, and fix a vertex $v$. In the loop at L6, a branch adds 1 to $m$ only for a vertex $u$ that passed the path check, so only for $u \in R_i$, and it counts each $u$ at most once. If the branch survives line L12, it has counted $c_i = |R_i|$ such vertices, so it has counted every vertex of $R_i$. A vertex $v$ is in $R_{i+1}$ if and only if $v \in R_i$ or $v$ has an in-neighbor $u \in R_i$. So at line L13, found is true if and only if $v \in R_{i+1}$. Thus every surviving branch adds 1 to $c'$ exactly for the vertices of $R_{i+1}$, and ends the round with $c = c_{i+1}$. Some branch survives: the one that guesses $b = 1$ exactly for the vertices of $R_i$ and guesses a correct path for each. $\square$

**The last step.** After the loop, every surviving branch has $c = c_{N-1}$. In lines L15 to L22, a branch counts only vertices that passed the path check, so it reaches $m = c_{N-1}$ only if it has passed the check for every vertex of $R_{N-1}$. If $t$ is reachable, then $t \in R_{N-1}$, and every branch with $m = c$ has passed the check for $t$ and rejected at L21, so no branch accepts. If $t$ is not reachable, the branch that guesses $R_{N-1}$ correctly never meets $t$ at L21 and accepts at L22. So NONREACH accepts if and only if $t$ is not reachable from $s$.

**Space.** The machine stores $i$, $c$, $c'$, $v$, $u$, $m$, the bits $b$ and found, and the current vertex and counter of one path check. Each is at most $N$, so the space is $O(\log N)$. This proves the lemma.

**Example.** Take the vertices 0 to 5, the edges $0 \to 1$, $1 \to 2$, $0 \to 3$, $3 \to 2$, $2 \to 4$ and $5 \to 0$, with $s = 0$ and $t = 5$. Then $R_0 = \{0\}$, $R_1 = \{0, 1, 3\}$, $R_2 = \{0, 1, 2, 3\}$ and $R_3 = R_4 = R_5 = \{0, 1, 2, 3, 4\}$, so the counts are $c_0, \ldots, c_5 = 1, 3, 4, 5, 5, 5$. In the last phase, an accepting branch passes the path check for 0, 1, 2, 3 and 4, reaches $m = 5 = c_5$ and never meets $t = 5$. A branch that skips vertex 4, say, ends with $m = 4$ and rejects at L22, and a branch that claims vertex 5 cannot pass its path check, because the only edge at 5 leaves it.

**The theorem.** Let a nondeterministic machine $M$ decide $A$ in space $s(n) \ge \log_2 n$, with $s$ space-constructible. As in the proof of [Savitch's theorem](/savitch-theorem/), assume that $M$ has a single accepting configuration $C_{\mathrm{acc}}$, and that every branch halts. A configuration of $M$ on an input of length $n$ is a string of $d \cdot s(n)$ bits for a constant $d$; this uses $s(n) \ge \log_2 n$ for the input head position. So the configuration graph $G_{M,x}$ has $N \le 2^{d\, s(n)}$ vertices, and $x \notin A$ if and only if $C_{\mathrm{acc}}$ is not reachable from the start configuration $C_0$.

A nondeterministic machine for the complement of $A$ first computes $s(n)$, which it can do because $s$ is space-constructible. Then it runs NONREACH on $G_{M,x}$, $C_0$ and $C_{\mathrm{acc}}$ without writing the graph down: it goes through the vertices as all strings of $d \cdot s(n)$ bits, and it tests an edge by reading the input symbol under the input head and checking the transition table of $M$. Its counters are at most $N$, so they take $O(\log N) = O(s(n))$ bits. So the complement of $A$ is in $\mathsf{NSPACE}(s(n))$. This gives $\mathsf{coNSPACE}(s) \subseteq \mathsf{NSPACE}(s)$. Applying it to the complements gives the other inclusion. $\blacksquare$

## Consequences

- $\mathsf{NL} = \mathsf{coNL}$. A problem that asks whether something does *not* exist in a graph, such as acyclicity of a directed graph or the absence of a path, is in NL whenever the existence version is.
- 2-SAT is NL-complete under logspace reductions. Jones, Lien and Laaser showed that the unsatisfiability of 2-CNF formulas is NL-complete; its complement 2-SAT is coNL-complete, and coNL = NL. See [2-SAT](/2-sat/) and [NL](/nondeterministic-logspace/).
- The context-sensitive languages, which are $\mathsf{NSPACE}(n)$, are closed under complement. This answered the second LBA problem, which Kuroda posed in 1964.
- The nondeterministic space hierarchy: $\mathsf{NSPACE}(f) \subsetneq \mathsf{NSPACE}(g)$ for space-constructible $g \ge \log n$ and $f = o(g)$, by the diagonal proof of the [space hierarchy theorem](/space-hierarchy-theorem/) with NONREACH used to flip the answer.
- The logspace alternation hierarchy collapses to NL. Each extra alternation adds one complement, and NL is closed under complement.

## Tightness

- **Time.** The theorem does not give $\mathsf{NP} = \mathsf{coNP}$, and that question is open. The proof goes through all vertices of the configuration graph at each of its $N$ rounds. In space this costs nothing, because the vertices are enumerated with a counter. In time it would cost $2^{O(t)}$ steps for a machine with time $t$, since the configuration graph has that many vertices.
- **The bound $s(n) \ge \log n$.** The counts $c_i$ can be as large as the number of configurations, which is at least $n + 2$ because of the input head position. A machine with space $o(\log n)$ cannot store such a count, so the proof does not apply below $\log n$.
- **Deterministic space.** The theorem says nothing about L against NL. The deterministic simulation of NL in [Savitch's theorem](/savitch-theorem/) still costs a square.

## History

The question whether $\mathsf{NSPACE}(n)$ is closed under complement goes back to Kuroda's 1964 paper on linear bounded automata, and it stayed open for more than twenty years. Neil Immerman and Róbert Szelepcsényi solved it independently. Szelepcsényi's short version appeared in the Bulletin of the EATCS in 1987 and his paper in Acta Informatica in 1988; Immerman's paper appeared at the Structure in Complexity Theory conference in 1988 and in the SIAM Journal on Computing in the same year. Immerman came to the result from descriptive complexity, where NL is the class of properties expressible in first-order logic with a transitive closure operator. The two shared the Gödel Prize in 1995.

## References
