---
tag: 199WKZ
kind: technique
slug: taint-analysis
name: Taint analysis
aliases:
- taint tracking
- information flow tracking
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: advanced
summary: Tracks data from untrusted sources through a program and reports when it reaches a sensitive sink without passing a sanitizer.
prereqs: [dataflow-analysis, data-dependence, ifds-framework]
see_also: [noninterference, self-composition, control-dependence, points-to-analysis, program-slicing, dynamic-slicing, datalog-program-analysis, symbolic-execution]
sources:
  - paper: doi:10.1145/2594291.2594299
    title: Steven Arzt, Siegfried Rasthofer, Christian Fritz, Eric Bodden, Alexandre Bartel, Jacques Klein, Yves Le Traon, Damien Octeau and Patrick McDaniel, FlowDroid, precise context, flow, field, object-sensitive and lifecycle-aware taint analysis for Android apps, Proceedings of the 35th ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI '14), 2014, pages 259-269
    locator: the taint problem as an IFDS problem over access paths, the on-demand alias search, and the model of the Android life cycle
  - paper: doi:10.1145/360051.360056
    title: Dorothy E. Denning, A lattice model of secure information flow, Communications of the ACM 19(5), 1976, pages 236-243
    locator: security classes as a lattice, explicit and implicit flows, and the certification of flows through control structures
  - paper: "V. Benjamin Livshits and Monica S. Lam, Finding security vulnerabilities in Java applications with static analysis, Proceedings of the 14th USENIX Security Symposium, 2005, pages 271-286"
    locator: sources, sinks and derivation rules for SQL injection and cross-site scripting in Java web applications, on top of a context-sensitive points-to analysis
  - paper: doi:10.1109/SP.2010.26
    title: Edward J. Schwartz, Thanassis Avgerinos and David Brumley, All you ever wanted to know about dynamic taint analysis and forward symbolic execution (but might have been afraid to ask), 2010 IEEE Symposium on Security and Privacy, 2010, pages 317-331
    locator: a formal semantics of dynamic taint analysis, taint policies, and the problems of over-tainting and under-tainting
  - paper: "James Newsome and Dawn Song, Dynamic taint analysis for automatic detection, analysis, and signature generation of exploits on commodity software, Proceedings of the Network and Distributed System Security Symposium (NDSS 2005), 2005"
    locator: TaintCheck, which tracks taint at run time in binaries and reports when tainted data is used as a jump target or a format string
---

Taint analysis checks one kind of property: data from an untrusted *source* must not reach a sensitive *sink* unless it first passes through a *sanitizer*. It marks values that come from sources as tainted, makes the result of an operation tainted when an operand is tainted, clears the mark at sanitizers, and reports each sink that can receive a tainted value. The static form is a forward [dataflow analysis](/dataflow-analysis/) whose transfer functions are distributive, so it fits the [IFDS framework](/ifds-framework/); FlowDroid (Arzt and coauthors, PLDI 2014) is built that way. The dynamic form keeps a taint bit beside each value at run time. Both forms follow explicit flows only, the data dependences of the program. A branch on a tainted value that then writes a constant is an implicit flow, and taint analysis does not see it, so a clean result does not prove [noninterference](/noninterference/).

## In plain words

Some data comes from places the program cannot trust, such as text that a user types into a web form. Some operations are dangerous if they get such data, such as a database query or a shell command. Taint analysis marks the untrusted data as tainted at the point where it enters. It then follows the data as the program copies it, joins it with other strings and passes it to functions. A value computed from tainted data is tainted too. A cleaning function, such as one that escapes quotes, removes the mark. If a tainted value reaches a dangerous operation, the analysis reports it. The analysis follows only the data itself. If the program makes a choice based on tainted data and then writes a constant, the constant is not marked, even though it tells something about the input.

## When it applies

- **Integrity.** Untrusted input must not control a sensitive operation: SQL injection, cross-site scripting, command injection, path traversal, and tainted jump targets in binaries.
- **Confidentiality, in a weak form.** Private data, such as a location or a contact list on a phone, must not reach a network or log call. Taint analysis catches the direct leaks. It does not catch leaks through branches, timing or other side channels.
- The sources, sinks and sanitizers can be listed as functions or statements. The result is only as good as that list and the models of library code.
- Data dependence is the threat that matters, or missing control dependence is acceptable. When it is not, use a check for [noninterference](/noninterference/), for example a security type system or [self-composition](/self-composition/).

## The template

**The specification.** A taint problem is a program and three sets of statements:

- *sources*, `x = src(...)`, whose result is untrusted, such as a read of a request parameter;
- *sinks*, `snk(e)`, whose argument must not be untrusted, such as the execution of a query string;
- *sanitizers*, `x = san(e)`, whose result is trusted, such as an escape function.

**The taint semantics.** Fix one run of the program. Let $T_i$ be the set of variables that hold a tainted value after step $i$, with $T_0 = \emptyset$. A step changes $T$ as follows, where $\mathrm{vars}(e)$ is the set of variables in $e$:

| statement | $T_{i+1}$ |
|---|---|
| `x = src(...)` | $T_i \cup \{x\}$ |
| `x = san(e)` | $T_i \setminus \{x\}$ |
| `x = e`, or `x = f(e)` for a library call without a model | $T_i \cup \{x\}$ if $\mathrm{vars}(e) \cap T_i \ne \emptyset$, else $T_i \setminus \{x\}$ |
| `if (e)`, `while (e)` | $T_i$ |
| `snk(e)` | $T_i$, and a violation if $\mathrm{vars}(e) \cap T_i \ne \emptyset$ |

The row for branches is the explicit-flow rule: a test on a tainted value taints nothing. The run has a *taint violation* if some sink step has a tainted argument.

**The static analysis.** Each transfer function above has the form $f(T) = (T \setminus K) \cup G \cup \{x : \mathrm{vars}(e) \cap T \ne \emptyset\}$ for fixed sets $K$ and $G$, and so $f(T_1 \cup T_2) = f(T_1) \cup f(T_2)$. A forward may analysis over the [control-flow graph](/control-flow-graph/) with these functions and union as the join computes, at each point, a superset of every $T_i$ that a path to that point can produce, so every violation of every run is reported. The functions are distributive over a finite set of facts, so the IFDS algorithm solves the interprocedural problem exactly over the paths on which calls and returns match: the result at a point is the union of the taint sets of all such paths to it. Spurious reports come from paths that no run takes, from the heap model, and from the library models, not from the merge.

**Heap and calls.** Real programs move data through fields and arrays. The facts become *access paths* `x.f.g`, cut at a fixed length $k$, and a store `a.f = y` with `y` tainted taints `a.f` and every access path that may alias it. The aliases come from a [points-to analysis](/points-to-analysis/), or from an on-demand backward search as in FlowDroid. Calls map the facts of the arguments to the parameters, and returns map them back, as in any interprocedural dataflow problem.

**The dynamic analysis.** A run-time version keeps a taint bit in shadow memory for each byte or word, updates it with the rules above on every instruction, and checks it at each sink. It sees only the path that runs, but it has exact addresses, so it needs no alias analysis.

## Classic examples

**SQL injection.** A request parameter flows into a query.

```
id = request.getParameter("id")           // source
q  = "SELECT * FROM users WHERE id = " + id
db.executeQuery(q)                        // sink
```

The tainted set is $\{id\}$ after the first line and $\{id, q\}$ after the second, so the sink is reported. With `q = "..." + escapeSql(id)` the call to the sanitizer gives a clean value, the concatenation of two clean strings is clean, and no report is made. Livshits and Lam (USENIX Security 2005) checked Java web applications in this way, with sources, sinks and sanitizers for the servlet API.

**Aliasing.** Here the tainted value enters through one name and leaves through another.

```
a = new Box();  b = a
a.f = src()
snk(b.f)
```

The store taints the access path `a.f`. Without alias information, `b.f` is clean and the leak is missed. With the fact that `a` and `b` point to the same object, the analysis taints `b.f` too and reports the sink.

**Context.** A helper is called twice.

```
id(x) { return x }
t1 = id(src())
t2 = id("constant")
snk(t2)
```

A context-insensitive analysis merges the two calls, finds the return value tainted, and reports a false alarm at `snk(t2)`. IFDS matches each return with its call, so `t2` stays clean.

**An implicit flow.** Taint analysis does not report this program.

```
s = src()
t = 0
if (s == 1) t = 1
snk(t)
```

No assignment copies `s`, so the tainted set at the sink is $\{s\}$ and `t` is clean on both paths. But the value of `t` at the sink equals the test `s == 1`, so the sink learns a bit of the source. The program is not noninterferent. Denning (1976) called this an implicit flow and showed how to certify it by the security class of the branch condition.

## Variations

- **Tainting the program counter.** Mark the assignments under a branch on a tainted value as tainted, using [control dependence](/control-dependence/). This catches the assignment `t = 1` above. A dynamic monitor still misses the run where the branch is not taken and `t` keeps 0, which also tells the sink something; a static analysis must taint every variable assigned in either branch.
- **Taint labels.** Keep a set of labels, or an element of a lattice, instead of one bit, to tell sources apart or to model several kinds of trust, as in Denning's lattice model. Sanitizers then remove only the labels that they clean.
- **Dynamic taint for binaries.** TaintCheck (Newsome and Song, NDSS 2005) taints input bytes and stops a run when a tainted value becomes a jump target or a format string. Schwartz, Avgerinos and Brumley give a formal semantics of such policies.
- **Taint in Datalog.** Sources, sinks and the propagation rules can be written as rules beside a points-to analysis, so that both are solved together; see [Datalog-based program analysis](/datalog-program-analysis/).
- **Slicing.** A forward [program slice](/program-slicing/) from a source contains every statement that a taint analysis with control dependence would mark. The slice is the coarser tool, and a [dynamic slice](/dynamic-slicing/) is its run-time form.

## Pitfalls

- **Implicit flows.** Taint analysis tracks explicit flows only. A clean report says that no sink gets data copied or computed from a source; it does not say that the sink is independent of the source.
- **Over-tainting.** If an address computed from a tainted index taints the value loaded from it, taint spreads through table lookups and pointer arithmetic until nearly every value is tainted. Dynamic tools must choose a policy for addresses.
- **Under-tainting.** Native code, reflection, callbacks and library methods without models move data out of the view of the analysis. Missing models cause missed reports.
- **The wrong sanitizer.** Escaping for HTML does not make a string safe for SQL. Attach each sanitizer to the kinds of sink that it protects.
- **Aliases.** Without alias information, flows through the heap are missed. A coarse alias analysis gives false alarms instead.
- **Infeasible paths.** The static analysis reports a sink that is reachable only on paths that no run takes. Each report needs a check, by hand or with [symbolic execution](/symbolic-execution/).

## Exercises

1. Give the tainted set after each line of `a = src(); b = a + 1; a = san(b); c = a + b; snk(c)`. Is the sink reported?
2. Prove that each transfer function of the template is distributive, and that the composition of two such functions is again of the same form.
3. Write a program with an implicit flow that a static analysis with control dependence finds and a dynamic monitor that taints the program counter misses on some run.
4. Show that the k-limited access paths `x.f.f.f...` with $k = 2$ can miss no flow, and say what precision is lost when the path is cut.
5. Write a program where a context-insensitive taint analysis reports a false alarm and IFDS does not, other than the one above, using a field instead of a return value.

## References
