---
tag: AD0T2D
kind: concept
slug: sql-injection
name: SQL injection
aliases:
- SQLi
area: security-and-privacy/network-and-web-security
level: intro
summary: "An attack that puts SQL syntax into an input that a program pastes into a query, so that the query does what the attacker wants."
history:
  year: 2006
  people: [Zhendong Su, Gary Wassermann, William G. J. Halfond, Jeremy Viegas, Alessandro Orso, Gregory Buehrer]
  note: "Public descriptions date from the late 1990s. Buehrer et al. checked queries by their parse trees in 2005, Su and Wassermann defined injection as input that is not syntactically confined in 2006, and Halfond, Viegas and Orso classified the attacks and defenses the same year."
prereqs: [context-free-grammar, parse-tree]
see_also: [parse-tree-query-validation, cross-site-scripting, taint-analysis, context-sensitive-auto-escaping, abstract-syntax-tree, relational-algebra]
sources:
  - paper: "Zhendong Su and Gary Wassermann, The essence of command injection attacks in web applications, ACM POPL 2006, pages 372 to 382"
    locator: "the definition of a command injection attack as input that is not syntactically confined in the parse tree of the query, and the checker based on an augmented grammar"
  - url: "https://viterbi-web.usc.edu/~halfond/papers/halfond06issse.pdf"
    title: "William G. J. Halfond, Jeremy Viegas and Alessandro Orso, A classification of SQL injection attacks and countermeasures, International Symposium on Secure Software Engineering 2006"
    locator: "the injection mechanisms, the intents and types of attacks, and the table that compares the prevention and detection techniques"
  - paper: "Gregory Buehrer, Bruce W. Weide and Paolo A. G. Sivilotti, Using parse tree validation to prevent SQL injection attacks, SEM 2005, pages 106 to 113, doi:10.1145/1108473.1108496"
    locator: the comparison of the parse tree of the query with and without the input
  - url: "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"
    title: "OWASP, SQL Injection Prevention Cheat Sheet"
    locator: "prepared statements as the primary defense, safe stored procedures, allowlist validation, escaping as a last resort, and least privilege"
---

SQL injection is a class of attack on programs that build a database query by pasting input into the text of the query. If the input contains characters that are special in SQL, such as a quote, the database parses part of the input as query syntax instead of as a value. The query then has a different structure from the one the programmer wrote, and it can read, change or delete data that the program never meant to touch. Su and Wassermann (2006) gave the exact form of the flaw: an injection is an input that is not syntactically confined, that is, whose characters do not stay inside one node of the right kind in the [parse tree](/parse-tree/) of the query. The primary defense is the prepared statement, which sends the query text and the values to the database separately, so a value is never parsed as SQL. Runtime checks such as [parse tree query validation](/parse-tree-query-validation/), allowlists and least privilege add layers. This page describes the class and its defenses with benign strings only; it gives no injection strings.

## In plain words

A program that looks up a person by name may build its question to the database as one piece of text: the fixed words of the question with the name typed in the middle. The database then reads the whole text and decides what it means.

If the name has a character that the database treats as part of the question, such as a quote mark, the database reads the text in a different way. Even an honest name such as O'Brien breaks the question. Someone who knows this can type text that turns the question into a different one. The fix is to send the question and the values apart, so that the database always treats the name as a name, whatever characters it has.

## The idea

**Code and data in one string.** A query language has a [context-free grammar](/context-free-grammar/). The program intends a query with a fixed structure and holes for values. When it builds the query by joining strings, the structure is decided only when the database parses the final text, and the input takes part in that decision. In the parse tree of the final query, a well-behaved input is the text of one literal. An injected input spans several nodes, closes a literal early, or adds nodes that the programmer did not write.

**The definition of Su and Wassermann.** Let a query $q$ be built from a template and inputs, and let $T$ be the parse tree of $q$. An input occurrence is syntactically confined if some node of $T$, of a kind that the policy allows for that hole (for example a literal), has as its leaves exactly the characters of the input. A command injection attack is a query in which some input is not syntactically confined. The definition does not depend on any list of bad characters, and it covers [cross-site scripting](/cross-site-scripting/) and other injections into a language as well.

**Mechanisms.** Halfond, Viegas and Orso (2006) list the ways an input reaches a query: form fields and URL parameters, cookies, server variables such as request headers, and second-order injection, where data stored earlier is later pasted into a query. A defense that checks only form fields misses the others. They also sort attacks by intent, for example to learn the schema, to read or change data, or to get past a login check, and they compare the defenses by the types of attack each one stops.

**The defenses.**

1. **Prepared statements.** The program sends the query text with placeholders, and then the values as parameters. The database parses the text once, without the values, so the structure is fixed before any input is seen. This removes the class for values. Stored procedures give the same protection only if they do not build dynamic SQL inside.
2. **Allowlists for what cannot be a parameter.** Table names, column names and sort directions cannot be placeholders in most databases. Map each allowed choice to a fixed string in the program, and reject every other input.
3. **Escaping as a last resort.** An escaper for the exact dialect and character encoding, such as one that doubles each quote inside a string literal, can keep a value inside its literal. It is easy to get wrong: one missed call, a numeric context with no quotes, or a different character set breaks it.
4. **Least privilege.** The database account of the program gets only the rights it needs, so an injection that does happen can do less.
5. **Runtime checks.** [Parse tree query validation](/parse-tree-query-validation/) (Buehrer et al. 2005) parses the query with and without the input and rejects it if the structure changes. SQLCheck of Su and Wassermann marks the input in the query and parses with an augmented grammar. [Taint analysis](/taint-analysis/) tracks input to the query call and checks that it passed through a safe path.

Filters that look for keywords or symbols in the input are not a defense on their own: the same characters are often in honest data, and the parser accepts more forms than the filter knows.

## Examples

**A toy query language.** To keep the example free of real attack strings, take a small grammar with a query $Q \to$ `find` $A$ `where` $A$ `=` $L$, an attribute $A$ that is a word, and a literal $L$ that is either digits or text between single quotes, where a quote inside the text is written as two quotes. A program fills the literal from an input $x$ with the template `find name where last = '`$x$`'`. The table shows benign inputs.

| input $x$ | query built by pasting | parse | is $x$ confined? |
| --- | --- | --- | --- |
| `Smith` | `... last = 'Smith'` | one literal `'Smith'` | yes |
| `O'Brien` | `... last = 'O'Brien'` | the literal ends after `O`, and `Brien'` is left over, so the parse fails | no: the quote of the input ended the literal |
| `O'Brien`, escaped to `O''Brien` | `... last = 'O''Brien'` | one literal whose value is `O'Brien` | yes |
| `O'Brien`, as a parameter | `... last = ?` with the value sent apart | one placeholder; the value is never parsed | yes, by construction |

The second row is not an attack. It is an honest name that the program cannot handle, and it shows the mechanism: a character of the input changed the parse. A program that fails on `O'Brien` will also accept some input that parses into a query of a different shape.

**A numeric hole.** The template `find name where id = `$x$, with no quotes, expects digits. The input `42` is one literal. The input `4 2` gives two tokens where the grammar expects one literal, so the parse fails and the input is not confined. Here an escaper for quotes does nothing, because the hole has no quotes; only a parameter or a check that $x$ is a number keeps the structure fixed.

**What the parse tree check sees.** For the first row, the tree with the input and the tree with a placeholder have the same shape, and the input is the full text of the literal node. For the second row, there is no tree. The [parse tree validation](/parse-tree-query-validation/) page runs this check with code on benign strings.

## Where it is used

- **Database interfaces.** Every common database API has prepared statements or parameter binding, and object-relational mappers use them by default. Code that builds query text by hand, for names that cannot be parameters or for dynamic filters, is where most remaining flaws are.
- **Program analysis.** Static [taint analysis](/taint-analysis/) of web applications reports paths from request data to query calls without a parameter or an escaper. Most such tools track explicit flows only.
- **Runtime protection.** Parse tree checks, model-based checks and database proxies compare each query with the structure that the program is expected to send.
- **Security reviews.** SQL injection is a standard class in reviews and in the OWASP Top 10, where it is counted under injection with [cross-site scripting](/cross-site-scripting/).
- **Other languages.** The same flaw and the same defense apply to shell commands, LDAP filters, XPath queries and template languages: keep the structure fixed and pass values apart.

## References
