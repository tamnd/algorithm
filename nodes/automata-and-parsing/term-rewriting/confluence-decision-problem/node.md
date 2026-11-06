---
tag: CJ5FME
kind: problem
slug: confluence-decision-problem
name: Deciding confluence
aliases:
- confluence problem
area: automata-and-parsing/term-rewriting
level: advanced
summary: Decide whether a given term rewriting system is confluent.
prereqs: [confluence, critical-pair-lemma, newman-lemma, combinatory-logic]
see_also: [termination-decision-problem, orthogonal-confluence-theorem, local-confluence, knuth-bendix-completion, critical-pair, halting-problem, arithmetical-hierarchy, hindley-rosen-lemma]
sources:
  - paper: doi:10.1016/j.ic.2010.09.003
    title: Jörg Endrullis, Herman Geuvers, Jakob Grue Simonsen and Hans Zantema, Levels of undecidability in rewriting, Information and Computation 209(2) (2011)
    locator: pp. 227 to 245 (confluence is complete for the level Pi-0-2 of the arithmetical hierarchy, and local confluence is complete for Sigma-0-1)
  - paper: doi:10.1016/0890-5401(90)90015-A
    title: Max Dauchet, Thierry Heuillard, Pierre Lescanne and Sophie Tison, Decidability of the confluence of finite ground term rewrite systems and of other related term rewrite systems, Information and Computation 88(2) (1990)
    locator: pp. 187 to 201 (confluence of finite ground systems is decidable, with tree automata and ground tree transducers)
  - paper: doi:10.1109/SFCS.2001.959904
    title: Hubert Comon, Guillem Godoy and Robert Nieuwenhuis, The confluence of ground term rewrite systems is decidable in polynomial time, 42nd IEEE Symposium on Foundations of Computer Science (2001)
    locator: pp. 298 to 307 (a polynomial time algorithm for finite ground systems)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 6, Confluence (undecidability in general, decidability for terminating systems by critical pairs, and orthogonal systems)
---

The **confluence decision problem** asks, for a given finite [term rewriting system](/term-rewriting-system/), whether it is [confluent](/confluence/): whether any two reduction sequences from the same term can always be continued to a common term. The problem is undecidable in general, and it is complete for the level $\Pi^0_2$ of the [arithmetical hierarchy](/arithmetical-hierarchy/). It is decidable for terminating systems, by testing the [critical pairs](/critical-pair/), and for finite ground systems, in polynomial time. In between, tools prove confluence with sufficient conditions such as orthogonality.

## In plain words

A set of rewrite rules is confluent if the order in which you apply the rules never matters in the end: whatever two paths you take from a starting expression, you can always continue both until they meet. This is what makes the result of a computation well defined.

The question is whether a program can look at any set of rules and say yes or no. It cannot, in general. If the rules always stop, it can: check the finitely many places where two rules overlap. If the rules contain no variables, it can, and fast. For other rules there are only partial methods.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure of the rewrite relation of $R$.

**Input.** A finite signature $\Sigma$ and a finite set $R$ of rules $l \to r$ over $T(\Sigma, V)$, with $l \notin V$ and $\mathrm{Var}(r) \subseteq \mathrm{Var}(l)$.

**Question.** Is $\to_R$ confluent, that is, do $s \to_R^* t_1$ and $s \to_R^* t_2$ always imply that $t_1 \to_R^* u$ and $t_2 \to_R^* u$ for some $u$?

The question is about all terms, including terms with variables. Confluence is the same as the Church-Rosser property, that $\leftrightarrow_R^*$-equal terms are joinable.

## Variants

- **Terminating systems.** The input is promised to be terminating. Then the problem is decidable (see below). Checking the promise is itself undecidable, see the [termination decision problem](/termination-decision-problem/).
- **Local confluence.** Is every peak $t_1 \leftarrow s \to t_2$ of single steps joinable? By the [critical pair lemma](/critical-pair-lemma/) this holds iff the finitely many critical pairs are joinable, so the problem is recursively enumerable: search for the joins. It is still undecidable, by the reduction below, and complete for $\Sigma^0_1$. For terminating systems it is the same as confluence, by [Newman's lemma](/newman-lemma/).
- **Ground confluence.** Confluence restricted to terms without variables. It can differ from confluence: $\{ f(a) \to a,\ f(b) \to b,\ g(x) \to f(x),\ g(x) \to x \}$ over the constants $a$ and $b$ is confluent on ground terms, since both rules for $g$ end in the argument, but $f(x) \leftarrow g(x) \to x$ is a peak of two normal forms. Ground confluence is undecidable even for terminating systems, since the critical pair test does not apply to it.
- **Ground systems.** The rules contain no variables. Then confluence on all terms is decidable.
- **Commutation and other properties.** Related questions, such as whether two systems commute (as in the [Hindley-Rosen lemma](/hindley-rosen-lemma/)) or whether every term has at most one normal form, have the same kind of answers: undecidable in general, decidable for ground systems.

## Examples

**A terminating system, not confluent.** $R = \{ f(f(x)) \to g(x) \}$ terminates, since each step removes a symbol. Its one critical pair comes from $f(f(f(x)))$, which rewrites to $f(g(x))$ and to $g(f(x))$. Both are normal forms and they differ, so $R$ is not confluent. Adding the rule $f(g(x)) \to g(f(x))$, as [Knuth-Bendix completion](/knuth-bendix-completion/) does, gives a terminating system whose two critical pairs $\langle f(g(x)), g(f(x)) \rangle$ and $\langle f(g(f(x))), g(g(x)) \rangle$ are joinable, so the new system is confluent.

**An orthogonal system.** [Combinatory logic](/combinatory-logic/) has the rules $K\,x\,y \to x$ and $S\,x\,y\,z \to x\,z\,(y\,z)$, with application as a binary symbol. The left sides are linear and do not overlap, so the system is confluent by the [orthogonal confluence theorem](/orthogonal-confluence-theorem/), although it does not terminate.

**Joinable critical pairs are not enough.** Huet's system $f(x, x) \to a$, $f(x, g(x)) \to b$, $c \to g(c)$ has no critical pairs, since $x$ and $g(x)$ do not unify, so it is locally confluent. It is not terminating, and not confluent: $f(c, c) \to a$ and $f(c, c) \to f(c, g(c)) \to b$ with distinct normal forms $a$ and $b$.

**The reduction in action.** With $M = S\,K\,K\,K$, the system $\mathrm{CL} \cup \{ c \to K,\ c \to M \}$ is confluent, because $M \to K\,K\,(K\,K) \to K$. With $M = S$, the term $c$ has the two normal forms $K$ and $S$, so the system is not confluent.

## Known algorithms

- **Critical pair test for terminating systems.** Compute all critical pairs $\langle u, v \rangle$ of $R$, finitely many, normalize both sides with any strategy, and answer yes iff $u{\downarrow} = v{\downarrow}$ for all of them. Correct by the critical pair lemma and Newman's lemma. It is the final check of Knuth-Bendix completion. The cost is the number of critical pairs, at most quadratic in the size of $R$, times the cost of normalization, which is not bounded by a primitive recursive function of the term size for some terminating systems.
- **Tree automata for ground systems.** Dauchet, Heuillard, Lescanne and Tison (1987, journal version 1990) decided confluence of finite ground systems with ground tree transducers, which represent $\to_R^*$ as a relation recognizable by tree automata. Their method also covers left-linear right-ground systems. Comon, Godoy and Nieuwenhuis (2001) gave the first polynomial time algorithm for ground systems.
- **Sufficient conditions.** For systems that are not terminating, confluence is proved by a syntactic criterion: orthogonality, or weak orthogonality, by the orthogonal confluence theorem; parallel closed and development closed critical pairs (Huet 1980, van Oostrom 1997); decreasing diagrams, which label the steps; and splitting the system into parts that commute. Non-confluence is shown by a peak whose two ends cannot be joined, often found by searching for two distinct normal forms of one term. Confluence tools combine these methods and compete in the yearly Confluence Competition.

## Bounds

**Undecidable, by a reduction from combinatory logic.** It is undecidable whether a closed term $M$ of combinatory logic reduces to $K$, because combinatory logic is [Turing-complete](/turing-completeness/): a term can simulate any [Turing machine](/turing-machine/) and reach $K$ exactly when the machine halts, and the [halting problem](/halting-problem/) is undecidable. Let $c$ be a new constant and

$$R_M = \mathrm{CL} \cup \{ c \to K,\ c \to M \}.$$

**Claim.** $R_M$ is confluent iff $M \to_{\mathrm{CL}}^* K$.

*Proof.* Suppose $R_M$ is confluent. From the peak $K \leftarrow c \to M$ there is a $w$ with $K \to_{R_M}^* w$ and $M \to_{R_M}^* w$. No rule has the left side $K$, so $K$ is a normal form and $w = K$. The term $M$ does not contain $c$, and no rule introduces $c$, so every step from $M$ is a step of CL. So $M \to_{\mathrm{CL}}^* K$.

Conversely, suppose $M \to_{\mathrm{CL}}^* K$. For a term $u$, let $\varphi(u)$ be $u$ with every $c$ replaced by $M$. A step $u \to v$ of CL gives $\varphi(u) \to_{\mathrm{CL}} \varphi(v)$, since the rules of CL do not contain $c$ and $\varphi$ only changes subterms that are constants. A step with $c \to M$ gives $\varphi(u) = \varphi(v)$, and a step with $c \to K$ gives $\varphi(u) \to_{\mathrm{CL}}^* \varphi(v)$, because $M \to_{\mathrm{CL}}^* K$ at that occurrence. So $u \to_{R_M}^* v$ implies $\varphi(u) \to_{\mathrm{CL}}^* \varphi(v)$. Also $u \to_{R_M}^* \varphi(u)$, by the rule $c \to M$ at each $c$. Now let $v_1 \leftarrow_{R_M}^* u \to_{R_M}^* v_2$. Then $\varphi(v_1) \leftarrow_{\mathrm{CL}}^* \varphi(u) \to_{\mathrm{CL}}^* \varphi(v_2)$. CL is confluent, so there is $w$ with $\varphi(v_1) \to_{\mathrm{CL}}^* w$ and $\varphi(v_2) \to_{\mathrm{CL}}^* w$. With $v_i \to_{R_M}^* \varphi(v_i)$, both $v_1$ and $v_2$ reduce to $w$. $\blacksquare$

So no algorithm decides confluence of finite systems, even for systems that are orthogonal except for two ground rules. The only critical pairs of $R_M$ are $\langle K, M \rangle$ and $\langle M, K \rangle$, so the same claim holds for local confluence, which is therefore undecidable too.

**Exact level.** Confluence is $\Pi^0_2$-complete (Endrullis, Geuvers, Simonsen and Zantema 2011): it says "for all peaks there exists a join", and every $\Pi^0_2$ set reduces to it. Local confluence of open terms is $\Sigma^0_1$-complete, so it is strictly easier: it is recursively enumerable, and confluence is not even that.

**Decidable cases.** For terminating finite systems the critical pair test decides confluence. For finite ground systems confluence is decidable in polynomial time.

## Reductions

- **From the halting problem**, through combinatory logic, as above. Any Turing-complete confluent system can take the place of CL.
- **From the termination promise.** For terminating systems, confluence reduces to finitely many normal form comparisons. This is why [Knuth-Bendix completion](/knuth-bendix-completion/) keeps its rules inside a reduction order: the result is terminating by construction, and its confluence is then decidable.
- **To unique normal forms.** A confluent system gives each term at most one normal form. The converse fails, so a yes for unique normal forms does not answer the confluence question.

## Applications

- **Well-defined results.** A confluent and terminating system defines a function: each term has exactly one normal form, so it decides the [word problem](/word-problem/) of its equations. Proving confluence is the main step in building such a system.
- **Programming languages and calculi.** Confluence of a calculus, such as the [Church-Rosser theorem](/church-rosser-theorem/) for the lambda calculus, shows that the order of evaluation does not change results. For rules with variables and no termination guarantee, this needs a proof by a sufficient condition, since no algorithm decides it.
- **Theorem provers.** Rewriting engines in proof assistants and equational provers check confluence of user rules, so that simplification gives the same answer in any order.

## References
