---
tag: 4H7SHT
kind: technique
slug: knowledge-compilation
name: Knowledge compilation
aliases:
- offline compilation of knowledge bases
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: advanced
summary: Translates a knowledge base once, offline, into a target language in which the queries asked online, such as entailment or model counting, take polynomial time in the size of the result.
prereqs: [sat, conjunctive-normal-form, ordered-binary-decision-diagram]
see_also: [knowledge-compilation-map, d-dnnf, sentential-decision-diagram, model-counting, prime-implicant, horn-sat, p-poly, bayesian-network]
sources:
  - paper: doi:10.1613/jair.989
    title: Adnan Darwiche and Pierre Marquis, A knowledge compilation map, Journal of Artificial Intelligence Research 17, 2002
    locator: Table 5 on page 239 (queries) and Table 7 on page 242 (transformations); the cited result of Selman and Kautz and of Cadoli and Donini that no compilation of polynomial size gives polynomial clause entailment unless NP is in P/poly (general locator)
  - paper: doi:10.1145/502090.502091
    title: Adnan Darwiche, Decomposable negation normal form, Journal of the ACM 48(4), 2001
    locator: pages 608 to 647 (a compiler from CNF to DNNF and the bound for CNFs of bounded treewidth)
  - paper: doi:10.1613/jair.2097
    title: Jinbo Huang and Adnan Darwiche, The language of search, Journal of Artificial Intelligence Research 29, 2007
    locator: pages 191 to 219 (the traces of exhaustive search as compiled forms, from OBDD and FBDD to decision-DNNF)
  - paper: "Bart Selman and Henry Kautz, Knowledge compilation and theory approximation, Journal of the ACM 43(2), 1996"
    locator: Horn upper and lower bounds of a clausal theory as an approximate compilation (general locator)
---

Knowledge compilation splits reasoning into two phases. Offline, a knowledge base, typically a propositional formula in [CNF](/conjunctive-normal-form/), is translated once into a *target language* in which the questions of interest are easy. Online, each question is answered from the compiled form in time polynomial in its size. The offline phase may be expensive, since it often solves an [NP-hard](/np-hard/) problem, but its cost is shared by all the questions that follow. This page is the general method and how to apply it; the [knowledge compilation map](/knowledge-compilation-map/) page compares the target languages, and the [d-DNNF](/d-dnnf/) and [SDD](/sentential-decision-diagram/) pages describe two of them in detail.

## In plain words

Some questions about a set of rules are hard every time you ask them, for example "is this fact a consequence of the rules?" If the rules stay the same and you ask many such questions, you can do the hard work once. Rewrite the rules in a special form, chosen so that each question becomes a quick walk over the rewritten form. The rewriting can be slow and the result can be large, but you do it only once, before the questions arrive. The right form depends on which questions you will ask and how the rules will change. Some forms make counting easy, some make combining two rule sets easy, and no form makes everything easy without becoming very large for some rules.

## When it applies

- The knowledge base changes rarely, and many queries are asked against it. Examples are a product configurator with fixed constraints, a diagnosis model of a fixed device, or a probabilistic model that answers many queries under different evidence.
- The queries are hard on the original form: [SAT](/sat/), clause entailment, model counting, or equivalence.
- There is a target language that supports the needed queries in polynomial time, and the knowledge base has a compiled form of manageable size in that language. The second condition depends on the structure of the input and cannot be guaranteed in general: unless NP is contained in [P/poly](/p-poly/), no target language with polynomial clause entailment has polynomial-size compiled forms for all CNFs (results of Selman and Kautz and of Cadoli and Donini, as stated by Darwiche and Marquis 2002). By the [Karp-Lipton theorem](/karp-lipton-theorem/), that inclusion would collapse the polynomial hierarchy.
- Online answers must be fast and predictable, for example in an interactive tool or an embedded device, where the cost of a SAT call per query is not acceptable.

## The template

```pseudo id=main
COMPILE-THEN-QUERY(Σ, Q)                  ▷ Σ is the knowledge base, Q the stream of queries
L1  L ← ⟨target language⟩ that supports in polynomial time the queries and transformations that Q needs
L2  C ← ⟨compiler⟩(Σ, L)                  ▷ offline, once; C is equivalent to Σ
L3  for each query q in Q do
L4      if q changes the knowledge base then C ← ⟨transformation⟩(C, q)
L5      else answer q by ⟨polynomial query⟩(C, q)
```

The holes are:

- **target language (L1).** Choose it from the tables of the [map](/knowledge-compilation-map/): the queries (consistency, validity, clause entailment, model counting, equivalence, and others) and the transformations (conditioning, conjunction, disjunction, negation, forgetting) that the application needs. Among the languages that support them, prefer the most succinct, since it has the smallest compiled forms.
- **compiler (L2).** *Top-down* compilers run an exhaustive search and record its trace; exhaustive [DPLL](/dpll/) with component splitting and caching gives a decision-DNNF (Huang and Darwiche 2007). *Bottom-up* compilers build the form of each clause and combine them with a conjunction operation, as with the [apply](/bdd-apply/) of OBDDs and SDDs.
- **transformation (L4).** Conditioning on evidence is polynomial in all the usual languages; conjunction with a new clause is polynomial for OBDDs with a fixed order but not for d-DNNF unless P = NP.
- **polynomial query (L5).** One or more passes over the compiled form, such as the bottom-up count of a smooth d-DNNF.

**Why it pays.** Let compilation take time $T_c$, a query on the compiled form take time $t_q$, and the same query on $\Sigma$ take time $t_s$. Answering $m$ queries costs $T_c + m t_q$ with compilation and $m t_s$ without, so compilation pays off once $m > T_c / (t_s - t_q)$. For hard queries $t_s$ is exponential in the worst case and $t_q$ is linear in $|C|$, so the break-even point is small when $|C|$ is.

**Why correctness is easy to state.** A compiler must return a form $C$ that is equivalent to $\Sigma$, or for counting, has the same models over the same variables. Every query then has the same answer on $C$ as on $\Sigma$. A compiler that drops this requirement and returns a weaker or stronger theory gives approximate answers, as in the Horn approximations below.

## Classic examples

- **CNF to d-DNNF for counting and probabilities.** A CNF, or the encoding of a [Bayesian network](/bayesian-network/) as a CNF with weights, is compiled by exhaustive search into a [d-DNNF](/d-dnnf/). Then [model counting](/model-counting/), weighted counting under any evidence and clause entailment are each one linear pass. The compiler bears the #P-hard part once.
- **Circuits to OBDDs for verification.** A combinational circuit, or the transition relation of a system, is compiled into an [OBDD](/ordered-binary-decision-diagram/) for a fixed variable order. Equivalence of two circuits is then a comparison of two roots, and [symbolic model checking](/symbolic-model-checking/) applies conjunction and existential quantification to OBDDs again and again. Here the transformations matter as much as the queries.
- **Prime implicates for entailment.** The set of prime implicates of a CNF supports clause entailment by a subset test: a clause is entailed if and only if it contains some prime implicate. The dual form uses [prime implicants](/prime-implicant/). Both can be exponentially larger than the input, and conjoining a set of prime implicates with a new clause is not polynomial (Darwiche and Marquis 2002, Table 7).
- **Incremental compilation with SDDs.** When the knowledge base grows by conjunction with new constraints, a [sentential decision diagram](/sentential-decision-diagram/) for a vtree chosen from the structure of the problem keeps the canonical form and an apply operation, and for some functions it is exponentially smaller than every OBDD, as the SDD page explains.

## Variations

- **Approximate compilation.** Selman and Kautz (1996) compute a [Horn](/horn-sat/) theory $\Sigma_{lb}$ that entails $\Sigma$ and a Horn theory $\Sigma_{ub}$ that $\Sigma$ entails, and entailment from a Horn theory takes linear time. If $\Sigma_{ub} \models \alpha$ then $\Sigma \models \alpha$, and if $\Sigma_{lb} \not\models \alpha$ then $\Sigma \not\models \alpha$; only the queries between the two need the full theory.
- **Compilation that uses structure.** Darwiche (2001) compiles a CNF of [treewidth](/treewidth/) $w$ into a DNNF of size linear in the number of variables and exponential only in $w$. SDDs have a similar bound for their vtrees. These bounds explain why compilation works for many structured inputs despite the general lower bound.
- **Compiling to a query, not a language.** When only one kind of query will be asked, for example a fixed set of variables to count over, the compiler can drop the parts of the knowledge base that the query cannot see, such as by forgetting the other variables first in a language that supports forgetting.
- **Choosing the language by the map.** The [map](/knowledge-compilation-map/) gives, for each language, its polynomial queries and transformations and its place in the succinctness order, and so turns the choice in L1 into a lookup.

## Pitfalls

- **Size blowup.** The compiled form can be exponential in the input, and for some inputs every equivalent form in a given language is. Measure the size on real inputs before you commit to compilation; the time and size of a compiler are measurements on benchmarks, not guarantees.
- **The wrong transformations.** d-DNNF supports conditioning but not conjunction of two compiled forms in polynomial time unless P = NP. An application that adds clauses after compilation must recompile or pick a language with polynomial conjunction, such as OBDD with a fixed order.
- **Variable order and vtree.** The size of an OBDD or SDD depends strongly on the variable order or the vtree, from linear to exponential for the same function. A poor choice can make compilation fail on inputs that a good choice handles easily.
- **Counting over the wrong variables.** A compiled form that does not mention a variable of the original problem still counts it as free; the model count must be taken over all the variables of the input, which may need smoothing.
- **Unsound shortcuts.** A compiler that is not exactly equivalent to $\Sigma$, for example one that drops clauses it considers redundant without proof, gives wrong answers to every later query.

## Exercises

1. Show that the CNF $(x_1 \vee y_1) \wedge (x_2 \vee y_2) \wedge \cdots \wedge (x_n \vee y_n)$ has $2^n$ prime implicants, so its smallest DNF has $2^n$ terms, while it has an OBDD with $2n$ inner nodes for the order $x_1, y_1, \ldots, x_n, y_n$.
2. Show that a language that supports consistency and conditioning in polynomial time also supports clause entailment in polynomial time.
3. A SAT call on a knowledge base takes 2 seconds, compilation takes 600 seconds, and a query on the compiled form takes 1 millisecond. After how many queries does compilation pay off?
4. Give a CNF with $n$ variables whose d-DNNF from the compiler of the d-DNNF page has size linear in $n$, but which is not a Horn formula and has no Horn equivalent.

## References
