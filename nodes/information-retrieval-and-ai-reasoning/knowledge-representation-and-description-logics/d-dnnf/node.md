---
tag: FSRAPA
kind: data-structure
slug: d-dnnf
name: Deterministic decomposable negation normal form
aliases:
- d-DNNF
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: advanced
summary: A circuit of and, or and literals whose ands have disjoint variables and whose ors have disjoint models. It gives linear-time consistency, clause entailment and model counting.
model: word-ram
complexity:
  vars: {s: the number of edges of the circuit, n: the number of variables}
  time: {consistency: O(s), condition: O(s), clause_entailment: O(s), smooth: O(s n), count_smooth: O(s)}
  space: {circuit: O(s), smoothed_circuit: O(s n)}
properties: {persistent: true, concurrent: false, external: false}
history:
  year: 2001
  people: [Adnan Darwiche]
  note: Darwiche added determinism to decomposable negation normal form and showed that the result supports model counting in linear time. Darwiche and Marquis (2002) placed d-DNNF in their knowledge compilation map.
prereqs: [knowledge-compilation, conjunctive-normal-form, boolean-circuit, dpll]
see_also: [knowledge-compilation-map, sentential-decision-diagram, model-counting, ordered-binary-decision-diagram, free-binary-decision-diagram, shannon-expansion, hash-consing, bayesian-network]
sources:
  - paper: doi:10.1613/jair.989
    title: Adnan Darwiche and Pierre Marquis, A knowledge compilation map, Journal of Artificial Intelligence Research 17, 2002
    locator: Section 2 (decomposability, determinism, smoothness and the language d-DNNF), Table 5 on page 239 (queries), Table 7 on page 242 (transformations), Appendix A, Lemma A.1 (smoothing in polynomial time) and Lemma A.4 (consistency and conditioning give clause entailment)
  - paper: "Adnan Darwiche, On the tractable counting of theory models and its application to truth maintenance and belief revision, Journal of Applied Non-Classical Logics 11(1-2), 2001, pages 11 to 34"
    locator: deterministic DNNF and model counting in time linear in the size of the circuit (general locator)
  - paper: doi:10.1145/502090.502091
    title: Adnan Darwiche, Decomposable negation normal form, Journal of the ACM 48(4), 2001
    locator: pages 608 to 647 (DNNF, its linear-time consistency test, and a compiler from CNF to DNNF)
  - paper: doi:10.1613/jair.2097
    title: Jinbo Huang and Adnan Darwiche, The language of search, Journal of Artificial Intelligence Research 29, 2007
    locator: pages 191 to 219 (the trace of exhaustive DPLL with decomposition is a decision-DNNF, a subset of d-DNNF)
  - paper: "Adnan Darwiche, A compiler for deterministic, decomposable negation normal form, Proceedings of the Eighteenth National Conference on Artificial Intelligence (AAAI), 2002"
    locator: the c2d compiler from CNF to d-DNNF (general locator)
---

A d-DNNF is a [Boolean circuit](/boolean-circuit/) in negation normal form, built from literals, constants, and-gates and or-gates, with two properties: the inputs of each and-gate share no variable (*decomposability*), and the inputs of each or-gate have no common model (*determinism*). Darwiche (2001) introduced it as a target language for [knowledge compilation](/knowledge-compilation/): a [CNF](/conjunctive-normal-form/) is compiled once, and then consistency, clause entailment and [model counting](/model-counting/) take time linear in the size of the circuit. The model counting page gives the counting problem and its place among counting problems; this page is the data structure, its compiler and its queries, and the [knowledge compilation map](/knowledge-compilation-map/) compares it with the other languages.

## In plain words

A formula can be written as a network of "and" and "or" gates over the variables and their negations. In general such a network is hard to ask questions about: even "can this ever be true?" is hard. Add two rules. Under an "and", the parts must talk about different variables, so each part can be solved on its own. Under an "or", the parts must never be true at the same time, so the ways to make them true never overlap. With these rules, you can count the ways to make the whole thing true by one pass from the bottom: multiply under "and", add under "or". The hard work moves to the step that builds the network. A search that tries a variable both ways, and splits the problem into independent parts when it can, builds such a network as a record of its work.

## The abstract type

An **NNF circuit** over the variables $X$ is a rooted [DAG](/directed-acyclic-graph/) whose leaves are labelled $\mathit{true}$, $\mathit{false}$, $x$ or $\neg x$ for $x \in X$, and whose inner nodes are labelled $\wedge$ or $\vee$. Each node $u$ denotes a Boolean function $f_u$ in the usual way, and $\mathrm{vars}(u)$ is the set of variables at the leaves below $u$. Following Darwiche and Marquis (2002, Section 2), the circuit is

- **decomposable** if for each and-node $u$ with children $c_1, \ldots, c_k$, $\mathrm{vars}(c_i) \cap \mathrm{vars}(c_j) = \emptyset$ for all $i \ne j$;
- **deterministic** if for each or-node $u$ with children $c_1, \ldots, c_k$, $f_{c_i} \wedge f_{c_j} \equiv \mathit{false}$ for all $i \ne j$;
- **smooth** if for each or-node $u$, $\mathrm{vars}(c_i) = \mathrm{vars}(u)$ for every child $c_i$.

A **DNNF** is a decomposable NNF circuit, a **d-DNNF** is a deterministic DNNF, and an **sd-DNNF** is a smooth d-DNNF. Decomposability and smoothness are syntactic and can be checked in linear time. Determinism is semantic. A **decision node** is an or-node of the form $(x \wedge \alpha) \vee (\neg x \wedge \beta)$, and a circuit whose or-nodes are all decision nodes is a **decision-DNNF**. It is deterministic by its shape, since the two children disagree on $x$. The compiler on this page outputs decision-DNNF, which is a proper subset of d-DNNF; it never builds or-nodes whose children are contradictory for a deeper reason.

The operations are COMPILE (from CNF), CO (consistency), CONDITION, CE (clause entailment), SMOOTH and CT (model count).

## Representation

The nodes live in one array. Node 0 is $\mathit{false}$, node 1 is $\mathit{true}$, and every other node is a literal or a tuple of an operator and the sorted ids of its children. A hash table maps each such key to its id ([hash-consing](/hash-consing/)), so a subcircuit built twice is stored once. A child always has a smaller id than its parent, so a loop over the ids below the root in increasing order visits children first; every query is one such loop. The constructors AND and OR fold constants: an and-node with a $\mathit{false}$ child is $\mathit{false}$, $\mathit{true}$ children are dropped, and a gate with one child is that child. Folding keeps both properties, because it only removes children or replaces a gate by one of its children.

## Operations

The compiler is exhaustive [DPLL](/dpll/) with [unit propagation](/unit-propagation/), a split into connected components, and a cache of compiled sub-problems. For a set of clauses $\Delta$ and a literal $l$, $\Delta|l$ removes the clauses that contain $l$ and deletes $\neg l$ from the others.

```pseudo id=main
COMPILE(Δ)                               ▷ Δ is a set of clauses; returns a node
L1  if Δ = ∅ then return true
L2  if Δ contains the empty clause then return false
L3  if Δ is in the cache C then return C[Δ]
L4  if Δ has a unit clause {l} then
L5      r ← AND(l, COMPILE(Δ|l))
L6  else if the clauses of Δ split into groups Δ_1, ..., Δ_k, k ≥ 2, that share no variable then
L7      r ← AND(COMPILE(Δ_1), ..., COMPILE(Δ_k))
L8  else
L9      x ← a variable with the most occurrences in Δ
L10     r ← OR(AND(x, COMPILE(Δ|x)), AND(¬x, COMPILE(Δ|¬x)))
L11 C[Δ] ← r; return r
```

The queries walk the circuit once, children first.

```pseudo id=queries
CO(N)                                    ▷ N is decomposable
L12 for each node u below N, children first do
L13     if u is a literal or true then c[u] ← 1; if u is false then c[u] ← 0
L14     if u is an and-node then c[u] ← 1 if c[v] = 1 for every child v, else 0
L15     if u is an or-node then c[u] ← 1 if c[v] = 1 for some child v, else 0
L16 return c[N] = 1

CONDITION(N, γ)                          ▷ γ is a set of literals with no complementary pair
L17 for each node u below N, children first: a literal in γ becomes true, a literal whose negation is in γ becomes false, and each gate is rebuilt with AND or OR

CE(N, δ)                                 ▷ does N entail the clause δ?
L18 if δ contains a literal and its negation then return true
L19 return not CO(CONDITION(N, {¬l : l ∈ δ}))

SMOOTH(N, X)                             ▷ X ⊇ vars(N)
L20 for each node u below N, children first, rebuild u; if u is an or-node then
L21     replace each child v by AND(v, (y ∨ ¬y) for each y ∈ vars(u) \ vars(v))
L22 return AND(N', (y ∨ ¬y) for each y ∈ X \ vars(N))      ▷ N' is the rebuilt root

CT(N)                                    ▷ N is a smooth d-DNNF with vars(N) = X
L23 for each node u below N, children first: literal 1, true 1, false 0, and-node the product of its children, or-node the sum
L24 return the value at N
```

## Example

Let $\Delta = (x_1 \vee x_2) \wedge (\neg x_1 \vee x_3) \wedge (x_4 \vee x_5) \wedge (\neg x_4 \vee \neg x_5)$ over $x_1, \ldots, x_5$.

| call | rule | result |
|---|---|---|
| $\Delta$ | L6: groups $\{x_1, x_2, x_3\}$ and $\{x_4, x_5\}$ | AND of the two results |
| first group | L9: $x_1$ occurs twice | OR of the two branches |
| $\Delta|x_1 = \{x_3\}$ | L5 | $x_3$ |
| $\Delta|\neg x_1 = \{x_2\}$ | L5 | $x_2$ |
| second group | L9: $x_4$ (a tie with $x_5$, broken by the index) | OR of the two branches |
| $\{\neg x_5\}$ and $\{x_5\}$ | L5 | $\neg x_5$ and $x_5$ |

The circuit is

$$\big((x_1 \wedge x_3) \vee (\neg x_1 \wedge x_2)\big) \wedge \big((x_4 \wedge \neg x_5) \vee (\neg x_4 \wedge x_5)\big),$$

with 15 nodes, 14 edges and 2 decisions. SMOOTH adds $(x_2 \vee \neg x_2)$ under $x_1 \wedge x_3$ and $(x_3 \vee \neg x_3)$ under $\neg x_1 \wedge x_2$; the second or-node is already smooth. CT then gives $1 \cdot 1 \cdot 2 = 2$ for each branch of the first or-node, $2 + 2 = 4$ for the first group, $1 + 1 = 2$ for the second, and $4 \cdot 2 = 8$ at the root, which is the number of models of $\Delta$. For CE with $\delta = x_2 \vee x_3$, CONDITION with $\{\neg x_2, \neg x_3\}$ turns both branches of the first or-node into $\mathit{false}$, so the root is $\mathit{false}$ and $\Delta \models x_2 \vee x_3$. With $\delta = x_2$, the branch $x_1 \wedge x_3$ survives, so $\Delta \not\models x_2$.

## Correctness

The proofs are in the [correctness proof](proofs/correctness.md). In short:

- **COMPILE is equivalent to $\Delta$.** Line L5 uses $\Delta \equiv l \wedge \Delta|l$ when $\{l\} \in \Delta$, line L7 uses that $\Delta$ is the conjunction of its groups, and line L10 is the [Shannon expansion](/shannon-expansion/) $\Delta \equiv (x \wedge \Delta|x) \vee (\neg x \wedge \Delta|\neg x)$.
- **The output is a decision-DNNF.** $\mathrm{vars}(\mathrm{COMPILE}(\Delta')) \subseteq \mathrm{vars}(\Delta')$, so line L5 is decomposable because $\Delta|l$ does not mention the variable of $l$, line L7 because the groups share no variable, and line L10 for the same reason as L5. The or-node of line L10 is a decision node on $x$.
- **CO on a DNNF.** An and-node is satisfiable if and only if each child is, because the children have disjoint variables and their models combine. This fails without decomposability: $x \wedge \neg x$ has two satisfiable children.
- **CE.** $\Sigma \models \delta$ if and only if $\Sigma \wedge \neg \delta$ is unsatisfiable, if and only if $\Sigma|\neg\delta$ is unsatisfiable, and CONDITION keeps decomposability because it only removes variables (Darwiche and Marquis 2002, Lemma A.4).
- **CT on an sd-DNNF.** Count the models of $f_u$ over $\mathrm{vars}(u)$. For an and-node the models are the tuples of models of the children, by decomposability, so the counts multiply. For an or-node the children have the same variables, by smoothness, and no common model, by determinism, so the counts add. SMOOTH keeps the function, decomposability and determinism, because each added factor $y \vee \neg y$ is valid and mentions a variable that the child does not.

## Complexity

| operation | time | needs |
|---|---|---|
| CO | $O(s)$ | decomposability |
| CONDITION | $O(s)$ expected | nothing |
| CE | $O(s)$ expected | decomposability |
| SMOOTH | $O(s n)$, and the output has $O(s n)$ edges | decomposability |
| CT | $O(s)$ additions and multiplications of numbers of at most $n$ bits | smoothness, decomposability, determinism |
| COMPILE | exponential in $n$ in the worst case | nothing |

Darwiche and Marquis (2002, Table 5) also list validity, implicant checking and model enumeration as polynomial for d-DNNF. They leave equivalence of two d-DNNFs open, with a probabilistic polynomial test, and they show that sentential entailment is not polynomial unless P = NP. Their Table 7 shows that d-DNNF supports conditioning, but not forgetting, conjunction or disjunction of two circuits in polynomial time unless P = NP; whether negation is polynomial is open.

The compiler cannot be polynomial on all inputs unless P = [NP](/np-complete/): its output answers CO in linear time, and CO of the output decides [SAT](/sat/) of the input. Without the cache, the recursion has at most $2^n$ leaves, since a decision on one variable doubles the branches and a split into groups divides the variables; the cache can only shorten this. Much better bounds hold for structured inputs: Darwiche (2001, JACM) shows that a CNF of bounded [treewidth](/treewidth/) has a DNNF of linear size.

## Variants

- **DNNF** drops determinism. It still supports CO, CE and model enumeration, but not counting: in the DNNF $x \vee y$ the two children share the model $x = y = 1$, so after smoothing the sum is $2 + 2 = 4$, but the function has 3 models.
- **Decision-DNNF** is the output of this compiler and of other search-based compilers (Huang and Darwiche 2007).
- **[FBDD](/free-binary-decision-diagram/) and [OBDD](/ordered-binary-decision-diagram/).** Read as an NNF circuit, a free BDD is a decision-DNNF in which every and-node is the $x \wedge \alpha$ part of a decision node. Huang and Darwiche (2007) show that the trace of exhaustive DPLL without the component split of line L7 is an FBDD, and an OBDD when the variable order is fixed.
- **[Sentential decision diagram](/sentential-decision-diagram/).** A d-DNNF with structured decomposability and a canonical form for a fixed vtree. Its apply operation conjoins or disjoins two SDDs for the same vtree in polynomial time when the result need not be compressed.
- **Weighted counting.** Give each literal a weight and use the same pass with the weight in place of 1 at the leaves. With weights taken from the parameters of a [Bayesian network](/bayesian-network/), this pass computes probabilities.

## When to use it

Use a d-DNNF when one knowledge base receives many counting or probability queries, possibly under different evidence, so that the cost of compiling is paid once. Each query is then one linear pass, and evidence is a CONDITION. Do not use it when the knowledge base changes often by conjunction with new clauses: d-DNNF does not support conjunction of two circuits in polynomial time, and an [OBDD](/ordered-binary-decision-diagram/) or an SDD fits that use better.

## Pitfalls

- **Counting without smoothing.** On $x_1 \vee (\neg x_1 \wedge x_2)$ the bottom-up sum gives $1 + 1 = 2$, but the function has 3 models over $\{x_1, x_2\}$, because the child $x_1$ does not mention $x_2$. Smooth first, or multiply each child count by $2$ to the power of the number of missing variables. The root also needs smoothing to all the variables of the problem: a variable that the CNF mentions but the circuit does not doubles the count.
- **Checking determinism.** For a general NNF circuit, deciding whether two children of an or-node are contradictory is coNP-hard, since it includes unsatisfiability of an NNF formula. A compiler must make determinism hold by construction, for example with decision nodes. A d-DNNF that comes from elsewhere cannot be checked cheaply.
- **Consistency needs decomposability.** CONDITION keeps decomposability, but a conjunction of two d-DNNFs under one and-node is not decomposable in general. CO on it can then answer "satisfiable" for $x \wedge \neg x$.
- **Cache keys.** The cache of line L3 must use the residual clause set itself (or a canonical encoding of it), not only the set of free variables, or two different sub-problems share one result.

## Implementations

## History

Darwiche published the full account of DNNF, with a compiler and the treewidth bound, in the Journal of the ACM in 2001. In a 2001 paper on tractable model counting he added determinism, showed that counting is linear on smooth d-DNNF, and applied it to truth maintenance and belief revision. The compiler c2d (Darwiche 2002) builds d-DNNF from CNF. Darwiche and Marquis (2002) placed d-DNNF in the knowledge compilation map, with the succinctness relations and the polynomial queries and transformations. Huang and Darwiche (2007) showed that the trace of exhaustive DPLL with component decomposition is a decision-DNNF.

## References
