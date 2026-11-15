---
tag: FAJN7H
kind: concept
slug: context-sensitivity
name: Context sensitivity
aliases:
- context-sensitive analysis
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: core
summary: Whether an analysis keeps the facts of different calls to the same procedure apart, by call strings, objects or summaries.
prereqs: [dataflow-analysis, monotone-dataflow-framework, call-graph]
see_also: [interprocedural-dataflow-analysis, functional-approach-interprocedural, ifds-framework, flow-sensitivity, k-cfa, object-sensitivity, function-inlining, cfl-reachability]
sources:
  - paper: "Micha Sharir and Amir Pnueli, Two approaches to interprocedural data flow analysis, in Steven S. Muchnick and Neil D. Jones (eds.), Program Flow Analysis: Theory and Applications, Prentice-Hall, 1981"
    locator: the call-string approach and the functional approach to interprocedural analysis
  - paper: "Olin Shivers, Control-flow analysis of higher-order languages, PhD thesis, Carnegie Mellon University, 1991 (report CMU-CS-91-145)"
    locator: k-CFA, which separates contexts by the last k call sites
  - paper: doi:10.1145/1044834.1044835
    title: "Ana Milanova, Atanas Rountev and Barbara G. Ryder, Parameterized object sensitivity for points-to analysis for Java, ACM Transactions on Software Engineering and Methodology 14(1), 1 to 41, 2005"
    locator: object sensitivity, with receiver objects as contexts
  - paper: doi:10.1145/996841.996859
    title: "John Whaley and Monica S. Lam, Cloning-based context-sensitive pointer alias analysis using binary decision diagrams, Proceedings of the ACM SIGPLAN 2004 Conference on Programming Language Design and Implementation (PLDI '04), 131 to 144, 2004"
    locator: one clone per acyclic call path, with the contexts stored in binary decision diagrams
  - paper: doi:10.1145/1926385.1926390
    title: "Yannis Smaragdakis, Martin Bravenboer and Ondrej Lhotak, Pick your contexts well: understanding object-sensitivity, Proceedings of the 38th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL '11), 17 to 30, 2011"
    locator: type sensitivity and the comparison of context choices for Java
  - paper: doi:10.1145/1391984.1391987
    title: "Ondrej Lhotak and Laurie Hendren, Evaluating the benefits of context-sensitive points-to analysis using a BDD-based implementation, ACM Transactions on Software Engineering and Methodology 18(1), 1 to 53, 2008"
    locator: the measured precision and cost of call-site and object-sensitive variants on Java programs
  - paper: doi:10.1145/1411204.1411243
    title: "David Van Horn and Harry G. Mairson, Deciding kCFA is complete for EXPTIME, Proceedings of the 13th ACM SIGPLAN International Conference on Functional Programming (ICFP '08), 275 to 282, 2008"
    locator: the EXPTIME-completeness of k-CFA for k of 1 or more
  - paper: doi:10.1145/199448.199462
    title: "Thomas Reps, Susan Horwitz and Mooly Sagiv, Precise interprocedural dataflow analysis via graph reachability, Proceedings of the 22nd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL '95), 49 to 61, 1995"
    locator: summary edges, which give exact context sensitivity for distributive subset problems
---

An analysis is *context-sensitive* when it keeps the facts of different calls to the same procedure apart. A *context-insensitive* analysis gives each procedure one set of facts, the meet of what all its callers pass in, and sends the result back to all callers. The facts of one caller then leak into the others. A context-sensitive analysis tags each fact with a *context*, an abstraction of the call that is active. The common choices are the last $k$ call sites (*call strings*), the receiver objects of the calls (*object sensitivity*), and the input facts themselves (*summaries*, the functional approach). It is one of the main dimensions of precision of an analysis, next to [flow sensitivity](/flow-sensitivity/).

## In plain words

A procedure that many places call is a meeting point. If the analysis keeps only one set of notes for it, every caller's notes get mixed together. A caller that passes the number 1 and a caller that passes the number 2 both get back "some number". A context-sensitive analysis keeps separate notes for separate calls. One way is to remember the last few places that made a call. Another way is to remember which object the call was made on. A third way is to work out, once, what the procedure does to any input, and to reuse that answer at each call. Remembering the last few places has a trap: if the useful difference is further back than you remember, the notes still get mixed.

## The idea

**Setting.** The program is a set of procedures with a [call graph](/call-graph/). Use the meet convention of Kildall for a [monotone framework](/monotone-dataflow-framework/): $\top$ is the start value, the analysis computes the greatest solution, and lower values are less precise. (The join convention of Cousot flips the order, and every statement below holds with the order reversed.) Inside a procedure, the edges carry transfer functions $f_e$. At a call site $s$ that calls $q$, a function $\mathit{call}_s$ maps the fact before the call to the fact at the entry of $q$, and a function $\mathit{ret}_s(a, b)$ combines the fact $a$ before the call with the fact $b$ at the exit of $q$ into the fact after the call. Both are monotone. The [interprocedural dataflow analysis](/interprocedural-dataflow-analysis/) page gives the graph and the valid paths.

**Contexts.** A context abstraction gives each procedure a set of contexts and, for each call site $s$, a function that maps the context $c$ of the caller to the context $\mathit{push}(c, s)$ of the callee. The analysis keeps one value $x(c, n)$ for each point $n$ and each context $c$ of its procedure. It is the greatest solution of

$$x(c_0, \mathit{entry}_{main}) \sqsubseteq \iota, \qquad x(c, n) \sqsubseteq f_e(x(c, m)) \text{ for each edge } e = (m, n) \text{ inside a procedure},$$

$$x(\mathit{push}(c, s), \mathit{entry}_q) \sqsubseteq \mathit{call}_s(x(c, s)), \qquad x(c, r_s) \sqsubseteq \mathit{ret}_s\big(x(c, s), x(\mathit{push}(c, s), \mathit{exit}_q)\big),$$

where $r_s$ is the return point of the call site $s$. The return reads the callee's exit in the context that this call created, so a fact comes back only to the callers that share that context.

| choice | context | $\mathit{push}(c, s)$ | number of contexts |
|---|---|---|---|
| context-insensitive | one context $\epsilon$ | $\epsilon$ | 1 |
| $k$-limited call strings | the last $k$ call sites | the last $k$ sites of $c \cdot s$ | up to $S^k$ for $S$ call sites |
| full call strings | the whole stack of call sites | $c \cdot s$ | unbounded with recursion |
| object sensitivity | the last $k$ allocation sites of receivers | the receiver's site, after the receiver's own context; it reads the receiver, not only $c$ and $s$ | up to $H^k$ for $H$ allocation sites |
| summaries (functional approach) | the input fact at the entry | $\mathit{call}_s(x(c, s))$ | the size of the lattice, in the worst case |

With $k = 0$, call strings are the context-insensitive analysis. With full call strings and no recursion, the analysis is the analysis of the program with every call [inlined](/function-inlining/).

**Proposition 1 (more context, more precision).** Let $k \le k'$, and let $x_k$ and $x_{k'}$ be the solutions with $k$-limited and $k'$-limited call strings. Write $\lceil c \rceil_k$ for the last $k$ sites of $c$. Then $x_k(\lceil c' \rceil_k, n) \sqsubseteq x_{k'}(c', n)$ for every point $n$ and every $k'$-context $c'$. In particular ($k = 0$), every call-string analysis is at least as precise as the context-insensitive one.

*Proof.* Put $z(c', n) = x_k(\lceil c' \rceil_k, n)$. For $k \le k'$, $\lceil \lceil c' \cdot s \rceil_{k'} \rceil_k = \lceil \lceil c' \rceil_k \cdot s \rceil_k$: both are the last $k$ sites of $c' \cdot s$. So each inequation of the $k'$ system, written for $z$, is an inequation of the $k$ system for the context $\lceil c' \rceil_k$, and it holds because $x_k$ is a solution. So $z$ is a solution of the $k'$ system, and $x_{k'}$ is the greatest one. $\square$

The proof uses only monotonicity, not distributivity. The same argument works for any pair of abstractions where the coarse context is a function of the fine one that commutes with $\mathit{push}$.

**Proposition 2 (exact without recursion).** If the call graph has no cycles, every transfer function is distributive, and $\mathit{ret}_s(a, b)$ depends only on $b$ (the state at the exit carries everything the caller needs), the analysis with full call strings computes the meet over all valid paths: paths on which each return goes back to the call site that made the call.

*Proof.* Without recursion, the full call strings of a procedure are the paths to it in the acyclic call graph, and the equations are those of the program with every call inlined, one copy per call string. The paths of the inlined program are exactly the valid paths of the original one, so the [coincidence theorem](/mop-mfp-coincidence-theorem/) for distributive frameworks gives the claim. $\square$

With recursion, the set of call strings is infinite. The usual exact method is then the functional approach, which uses the input fact as the context ([functional approach](/functional-approach-interprocedural/), and its graph form, the [IFDS framework](/ifds-framework/)). Valid paths are paths in a [Dyck language](/dyck-language/) of matched calls and returns, which is why [CFL-reachability](/cfl-reachability/) is the natural language for exact context sensitivity.

**The trap: $k$ too small.** A $k$-limited analysis forgets everything but the last $k$ call sites. When two calls differ only in a site further back, the analysis gives them the same context, and their facts merge. A wrapper procedure is the common case: each layer of wrappers needs one more site in the string. The analysis stays sound; it just loses precision without a warning. Larger $k$ is more precise (Proposition 1), but the number of contexts can grow as $S^k$, and for higher-order programs, deciding $k$-CFA is already EXPTIME-complete for $k = 1$ (Van Horn and Mairson 2008). Summaries do not have this trap, since they do not limit the depth.

**Cost.** For a procedure with $C$ contexts, the analysis does the work of $C$ copies of its body. Call strings and objects bound $C$ by the choice of $k$. Summaries bound it by the number of distinct input facts that reach the procedure. For distributive subset problems, the IFDS framework makes summaries cheap: it keeps one summary edge per pair of single facts, and the whole analysis takes $O(E D^3)$ time.

## Examples

Take constant propagation with one value per variable, where $\bot$ means "not a constant". The functions return their argument through a chain of wrappers. Call sites are labeled.

```text
id(a):    return a
wrap(b):  s3: r = id(b)
          return r
main():   s1: x = wrap(1)
          s2: y = wrap(2)
          s4: u = id(3)
          s5: v = id(4)
```

| analysis | contexts of `wrap` | contexts of `id` | x | y | u | v |
|---|---|---|---|---|---|---|
| context-insensitive | one | one: $a = 1 \sqcap 2 \sqcap 3 \sqcap 4 = \bot$ | $\bot$ | $\bot$ | $\bot$ | $\bot$ |
| call strings, $k = 1$ | [s1], [s2] | [s3], [s4], [s5]: $a = 1 \sqcap 2 = \bot$ in [s3] | $\bot$ | $\bot$ | 3 | 4 |
| call strings, $k = 2$ | [s1], [s2] | [s1 s3], [s2 s3], [s4], [s5] | 1 | 2 | 3 | 4 |
| summaries | $b = 1$, $b = 2$ | $a = 1, 2, 3, 4$; each summary returns its input | 1 | 2 | 3 | 4 |

With $k = 1$, the two direct calls of `id` are kept apart, so `u` and `v` are found. The calls through `wrap` both reach `id` from the same site `s3`, and the last site is all that $k = 1$ keeps. The context `[s3]` gets $a = 1 \sqcap 2 = \bot$, and that value goes back to both contexts of `wrap`. A second wrapper layer around `wrap` would need $k = 3$. The summary of `id` says "returns its argument", which is right in every context and at every depth.

**Objects.** In object-oriented code, many calls go through a few library methods, such as the `add` and `get` methods of a list class. If the program builds two lists, one of strings and one of files, a context-insensitive pointer analysis lets both lists hold both kinds of objects. Using the allocation site of the receiver as the context keeps the two lists apart, however deep the call chain that reaches `add` (Milanova, Rountev and Ryder 2005).

## Where it is used

- **Pointer analysis for Java.** Object sensitivity and its relative, type sensitivity, are the common choices for Java points-to analysis ([object sensitivity](/object-sensitivity/)). Smaragdakis, Bravenboer and Lhotak (2011) compare the choices, and Lhotak and Hendren (2008) measure call-site and object sensitivity on Java programs.
- **Control flow analysis of functional programs.** [k-CFA](/k-cfa/) separates the bindings of a closure by the last $k$ call sites. [0-CFA](/zero-cfa/) is the context-insensitive case.
- **Cloning.** Whaley and Lam (2004) give each acyclic call path its own clone and store the huge number of contexts compactly in [binary decision diagrams](/binary-decision-diagram/).
- **Exact interprocedural dataflow.** The [functional approach](/functional-approach-interprocedural/), [IFDS](/ifds-framework/) and [IDE](/ide-framework/) compute procedure summaries, which give exact results over valid paths for distributive problems.
- **Inlining.** A compiler that [inlines](/function-inlining/) a call gets a context-sensitive analysis of the inlined body for free, at the price of code size.
- **Types.** Let-polymorphism gives each use of a polymorphic function its own instance of its type, which is a form of context sensitivity in a type system ([let-polymorphism](/let-polymorphism/)).

## References
