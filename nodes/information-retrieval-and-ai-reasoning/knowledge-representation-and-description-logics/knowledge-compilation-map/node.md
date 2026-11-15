---
tag: Z585AH
kind: concept
slug: knowledge-compilation-map
name: Knowledge compilation map
aliases:
- Darwiche-Marquis map
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: research
summary: Compares target languages such as OBDD, DNNF and d-DNNF by succinctness and by the queries and transformations that each supports in polynomial time.
prereqs: [knowledge-compilation, d-dnnf, ordered-binary-decision-diagram]
see_also: [sentential-decision-diagram, free-binary-decision-diagram, prime-implicant, model-counting, conjunctive-normal-form, np-complete, p-poly, polynomial-hierarchy]
sources:
  - paper: doi:10.1613/jair.989
    title: Adnan Darwiche and Pierre Marquis, A knowledge compilation map, Journal of Artificial Intelligence Research 17, 2002, pages 229 to 264
    locator: Section 2, pages 231 to 235 (the languages), Definition 3.1 (succinctness), Table 3 and Figure 5 on page 237 (the succinctness relations), Definitions 4.1 to 4.6 on page 238 (queries), Table 5 on page 239, Definitions 5.1 to 5.7 on pages 240 to 242 (transformations), Table 7 on page 242, footnote 3 (equivalence of FBDDs and d-DNNFs), Appendix A, Lemmas A.1, A.3, A.4 and A.7
---

The knowledge compilation map of Darwiche and Marquis (2002) is a comparison of the target languages of [knowledge compilation](/knowledge-compilation/). It places sixteen propositional languages, from general negation normal form down to explicit lists of models, along three axes: how succinct each language is, which queries it answers in polynomial time, and which transformations it supports in polynomial time. The knowledge compilation page describes the method of compiling once and querying many times; this page is the table that tells which language to compile to. The pages on [d-DNNF](/d-dnnf/), [OBDDs](/ordered-binary-decision-diagram/) and [SDDs](/sentential-decision-diagram/) describe single rows in detail.

## In plain words

There are many ways to write down the same set of rules. Some ways are short but make questions hard to answer. Other ways make questions easy but can be very long. The map is a table that lists the common ways, and for each one it says three things. First, how short it can be compared to the others. Second, which questions, such as "can these rules ever be true?" or "how many ways can they be true?", it answers quickly. Third, which changes, such as adding a rule or fixing a value, it allows quickly without growing out of control. The table shows a trade-off: the more questions a form answers quickly, the longer it tends to be. You read the table to pick the shortest form that still answers your questions.

## The idea

**Languages.** All the languages are subsets of NNF, the rooted DAGs of and-nodes and or-nodes over literals and the constants $\mathit{true}$ and $\mathit{false}$ (Section 2). They are defined by properties of the DAG:

- **decomposable** (D): the children of an and-node share no variable; **deterministic** (d): the children of an or-node have no common model; **smooth** (s): the children of an or-node mention the same variables; **flat** (f): the height is at most 2;
- **decision**: every or-node has the form $(x \wedge \alpha) \vee (\neg x \wedge \beta)$; this gives BDDs; with decomposability, FBDDs (free BDDs: each variable at most once on each path); with one variable order on all paths, OBDDs; and with one fixed order $<$ for all sentences of the language, OBDD$_<$;
- **CNF** and **DNF** are the flat languages whose clauses or terms are simple; **PI** is the CNFs that list all prime implicates, **IP** the DNFs that list all [prime implicants](/prime-implicant/), and **MODS** the DNFs whose terms are the models.

So the rows are NNF, DNNF, d-NNF, s-NNF, f-NNF, d-DNNF, sd-DNNF, BDD, [FBDD](/free-binary-decision-diagram/), OBDD, OBDD$_<$, DNF, [CNF](/conjunctive-normal-form/), PI, IP and MODS.

**Succinctness.** A language $L_1$ is *at least as succinct as* $L_2$, written $L_1 \le L_2$, if there is a polynomial $p$ such that every sentence $\alpha$ of $L_2$ has an equivalent sentence $\beta$ of $L_1$ with $|\beta| \le p(|\alpha|)$ (Definition 3.1). Table 3 and Figure 5 give the relations. One chain in them is

$$\text{DNNF} < \text{d-DNNF} < \text{FBDD} < \text{OBDD} < \text{OBDD}_< < \text{MODS},$$

where $<$ means strictly more succinct. Smoothing a d-DNNF takes polynomial time (Lemma A.1), so sd-DNNF and d-DNNF are equally succinct.

**Queries** (Definitions 4.1 to 4.6). For sentences $\Sigma, \Sigma'$ of the language, a clause $\gamma$ and a term $\tau$:

| query | question |
|---|---|
| CO | is $\Sigma$ consistent? |
| VA | is $\Sigma$ valid? |
| CE | does $\Sigma \models \gamma$ hold? |
| IM | does $\tau \models \Sigma$ hold? |
| EQ | is $\Sigma \equiv \Sigma'$? |
| SE | does $\Sigma \models \Sigma'$ hold? |
| CT | how many models does $\Sigma$ have? |
| ME | list the models of $\Sigma$, in time polynomial in the size of $\Sigma$ and in the number of models |

**Transformations** (Definitions 5.1 to 5.7). A language supports a transformation if the result can be computed in polynomial time *and stays in the language*:

| transformation | result |
|---|---|
| CD | conditioning: replace each variable of a consistent term $\rho$ by its value in $\rho$ |
| FO | forgetting: $\exists X.\, \Sigma$ for a set of variables $X$ |
| SFO | singleton forgetting: $\exists x.\, \Sigma$ for one variable |
| $\wedge$C, $\vee$C | conjunction, disjunction of any number of sentences |
| $\wedge$BC, $\vee$BC | conjunction, disjunction of two sentences |
| $\neg$C | negation |

**Table 5, queries** (page 239). √ means that the language satisfies the query, ◦ that it does not unless P = NP, and ? that the question is open.

| L | CO | VA | CE | IM | EQ | SE | CT | ME |
|---|---|---|---|---|---|---|---|---|
| NNF | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ |
| DNNF | √ | ◦ | √ | ◦ | ◦ | ◦ | ◦ | √ |
| d-NNF | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ |
| s-NNF | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ |
| f-NNF | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ |
| d-DNNF | √ | √ | √ | √ | ? | ◦ | √ | √ |
| sd-DNNF | √ | √ | √ | √ | ? | ◦ | √ | √ |
| BDD | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ |
| FBDD | √ | √ | √ | √ | ? | ◦ | √ | √ |
| OBDD | √ | √ | √ | √ | √ | ◦ | √ | √ |
| OBDD$_<$ | √ | √ | √ | √ | √ | √ | √ | √ |
| DNF | √ | ◦ | √ | ◦ | ◦ | ◦ | ◦ | √ |
| CNF | ◦ | √ | ◦ | √ | ◦ | ◦ | ◦ | ◦ |
| PI | √ | √ | √ | √ | √ | √ | ◦ | √ |
| IP | √ | √ | √ | √ | √ | √ | ◦ | √ |
| MODS | √ | √ | √ | √ | √ | √ | √ | √ |

**Table 7, transformations** (page 242). √ means that the language satisfies the transformation, • that it does not, ◦ that it does not unless P = NP, and ? that the question is open.

| L | CD | FO | SFO | $\wedge$C | $\wedge$BC | $\vee$C | $\vee$BC | $\neg$C |
|---|---|---|---|---|---|---|---|---|
| NNF | √ | ◦ | √ | √ | √ | √ | √ | √ |
| DNNF | √ | √ | √ | ◦ | ◦ | √ | √ | ◦ |
| d-NNF | √ | ◦ | √ | √ | √ | √ | √ | √ |
| s-NNF | √ | ◦ | √ | √ | √ | √ | √ | √ |
| f-NNF | √ | ◦ | √ | • | • | • | • | √ |
| d-DNNF | √ | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ | ? |
| sd-DNNF | √ | ◦ | ◦ | ◦ | ◦ | ◦ | ◦ | ? |
| BDD | √ | ◦ | √ | √ | √ | √ | √ | √ |
| FBDD | √ | • | ◦ | • | ◦ | • | ◦ | √ |
| OBDD | √ | • | √ | • | ◦ | • | ◦ | √ |
| OBDD$_<$ | √ | • | √ | • | √ | • | √ | √ |
| DNF | √ | √ | √ | • | √ | √ | √ | • |
| CNF | √ | ◦ | √ | √ | √ | • | √ | • |
| PI | √ | √ | √ | • | • | • | √ | • |
| IP | √ | • | • | • | √ | • | • | • |
| MODS | √ | √ | √ | • | √ | • | • | • |

**How the cells are proved.** Many √ cells follow from a few general lemmas: a language with CO and CD in polynomial time also has CE (Lemma A.4) and ME (Lemma A.3), and a language with VA and CD has IM (Lemma A.7). Many ◦ cells come from a reduction from SAT or its complement: a language that contains all CNFs, or into which CNFs translate in polynomial time while keeping the query, cannot answer CO, or VA, in polynomial time unless P = NP. The • cells are unconditional: for some inputs, every sentence of the language that is equivalent to the result is exponentially larger than the input. The ? cells for EQ on d-DNNF and FBDD are open; footnote 3 notes that these problems are in [coNP](/co-np/) and have polynomial probabilistic tests.

## Examples

- **Counting under evidence.** An application conditions on evidence and counts models many times. It needs CD and CT. The rows with both are d-DNNF, sd-DNNF, FBDD, OBDD, OBDD$_<$ and MODS. The most succinct of these is d-DNNF, and compilers for probabilistic inference target it.
- **A knowledge base that grows.** An application adds clauses one at a time and tests equivalence with a specification. It needs $\wedge$BC and EQ. Only OBDD$_<$ and MODS have both, and OBDD$_<$ is far more succinct. Plain OBDD, where different sentences may use different orders, has EQ but not $\wedge$BC: conjoining two OBDDs with different orders is not polynomial unless P = NP.
- **The two classical normal forms.** CNF answers VA and IM at once, since a CNF is valid only if each clause is, but not CO, which is SAT. DNF is the mirror image: CO is easy, since a DNF is consistent if some term is, and VA is hard. Neither supports CT, and the map shows that compiling either one into d-DNNF or OBDD gains the queries it lacks, at a possible cost in size.
- **The price of determinism.** DNNF has CO, CE and ME, and supports forgetting, but not VA or CT. Adding determinism gives d-DNNF, which gains VA, IM and CT but loses forgetting and both forms of disjunction. The map shows such trade-offs for every step in the succinctness order.
- **Why MODS is not the answer.** MODS satisfies every query and many transformations, but its size grows with the number of models, which can be exponential in the number of variables. It is the least succinct row of the chain above.

## Where it is used

- **Choosing a target language.** Designers of compilers and applications read the tables to find the most succinct language that has the queries and transformations they need, as in the examples above.
- **Placing new languages.** Later languages are described by their position in the same framework. The [SDD](/sentential-decision-diagram/) is a subset of d-DNNF; its page explains how it adds canonical forms for a fixed vtree and a polynomial apply when compression is dropped.
- **Lower bounds.** The • cells and the strict succinctness relations are statements that a family of functions has no small representation in a language; they connect knowledge compilation with circuit complexity and with the question whether NP is in [P/poly](/p-poly/), on which the general limit of compilation depends.
- **Teaching the area.** The definitions of the properties (decomposable, deterministic, smooth, decision, ordered) and the queries are the common vocabulary of later work on compilation and on tractable circuits for counting and probabilistic inference.

## References
