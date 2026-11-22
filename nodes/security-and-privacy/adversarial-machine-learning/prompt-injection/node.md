---
tag: GMS0NH
kind: concept
slug: prompt-injection
name: Prompt injection
aliases:
- indirect prompt injection
area: security-and-privacy/adversarial-machine-learning
level: research
summary: "An attack that places instructions in data a language model reads, such as a web page, so that the model follows them instead of its user."
history:
  year: 2022
  people: [Fabio Perez, Ian Ribeiro, Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, Mario Fritz]
  note: Perez and Ribeiro (2022) studied text in the prompt that overrides the instructions of an application, and Greshake et al. (AISec 2023) showed the indirect form, where the text comes from data the model retrieves.
prereqs: [language-model, sql-injection, taint-analysis]
see_also: [sql-injection, cross-site-scripting, taint-analysis, noninterference, reference-monitor, principle-of-least-privilege, greedy-coordinate-gradient-attack, same-origin-policy]
sources:
  - url: https://arxiv.org/abs/2302.12173
    title: Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz and Mario Fritz, Not what you've signed up for, compromising real-world LLM-integrated applications with indirect prompt injection, ACM AISec 2023
    locator: the indirect form of the attack, the taxonomy of threats to applications that retrieve data, and the discussion of mitigations
  - url: https://arxiv.org/abs/2211.09527
    title: Fabio Perez and Ian Ribeiro, Ignore previous prompt, attack techniques for language models, ML Safety Workshop at NeurIPS 2022
    locator: the direct form, goal hijacking and prompt leaking, measured on an application model
  - paper: "Jerome H. Saltzer and Michael D. Schroeder, The protection of information in computer systems, Proceedings of the IEEE 63(9), 1975"
    locator: the principles of least privilege and complete mediation
---

Prompt injection is an attack on an application built on a language model, in which text that the attacker controls is read by the model as if it were an instruction of the application or of the user. A language model takes one sequence of tokens: the instructions of the developer, the request of the user and any data the application adds, such as a web page, an email or the output of a tool, are all joined into it. The model has no reliable way to tell which parts are instructions and which parts are only data. So text inside the data that reads as an instruction can change what the model does: what it says to the user, which tools it calls, or what it sends where. Perez and Ribeiro (2022) studied the direct form, where the attacker is the user and overrides the developer's instructions. Greshake et al. (2023) showed the indirect form, where the attacker never talks to the model but places text in data that the model will retrieve later, and so acts against a user who trusts the application. The problem has the same root as [SQL injection](/sql-injection/): code and data share one channel. Unlike SQL, the language of the model has no grammar that an escaper can enforce, so the known defenses limit what an injected instruction can do, rather than remove the possibility.

## In plain words

An assistant reads your email to make a summary. It cannot always tell the difference between your request and the words in the emails. If one email contains a sentence that looks like a request to the assistant, the assistant may obey it, as if it came from you.

This is the old mistake of mixing orders and data in one channel. A database can be protected from it by keeping the query and the values apart. A language model cannot, because it reads everything as one text.

The practical defense is to assume that the model can be misled whenever it reads text from outside, and to limit what it may do in that case: fewer tools, fewer permissions, and a person's approval for actions that matter.

## The idea

**The channel model.** An application computes its answer as $a = M(I \cdot U \cdot D)$, where $M$ is the model, $I$ the instructions of the developer, $U$ the request of the user, $D$ the data added by the application, and $\cdot$ joins texts. The intent is that $I$ and $U$ decide the task and $D$ is only material for it. The attack is a choice of the part of $D$ (or of $U$, in the direct form) that the attacker controls, such that $a$ does what neither the developer nor the user asked.

**Direct and indirect.** In the direct form the attacker types the request $U$ and wants to override $I$, for example to make the application reveal $I$ or ignore its task. In the indirect form the attacker controls only a source of $D$: a web page a search tool will fetch, a document in a shared folder, a message in an inbox. Greshake et al. showed that this turns every source of data into a way in, and that the harm grows with the tools of the application, since the attacker's text can make the model call them.

**Why it is hard to fix.**
- **No separator.** A model is trained to follow instructions wherever they appear. Delimiters, and warnings in $I$ that the data is only data, are themselves text, and a model can ignore them. They lower the rate of success but do not bound it.
- **No grammar.** For [SQL injection](/sql-injection/) and [cross-site scripting](/cross-site-scripting/), a parser defines exactly where data ends, so escaping or parameterized queries remove the attack. For natural language there is no such parser.
- **Adaptive attackers.** Like other filters in adversarial machine learning, a classifier that detects injected text can be evaded by an attacker who knows it; automated searches such as the [GCG attack](/greedy-coordinate-gradient-attack/) show that unusual text can steer models.

**Defenses by design.** These defenses do not try to make the model perfect; they limit what a misled model can do.
- **Treat retrieved text as data with a label.** Track which parts of the context come from untrusted sources, as [taint analysis](/taint-analysis/) does for program variables, and forbid sensitive actions whose arguments depend on tainted text. The ideal is a form of [noninterference](/noninterference/): untrusted data must not influence privileged actions.
- **Privilege separation.** Let a model that reads untrusted data have no tools, and let a model that has tools never read untrusted data, only symbols or results that a program checks. A [reference monitor](/reference-monitor/) outside the model checks every tool call against a policy.
- **Least privilege.** Give the application only the tools and permissions its task needs, the [principle of least privilege](/principle-of-least-privilege/), and ask a person to confirm actions that are hard to undo, such as sending money or messages.
- **Input marking.** Mark the data part of the context, for example by special tokens or by a transformation of the data, and train or instruct the model to treat marked text as data. This lowers success rates in measurements, but it is a heuristic, not a guarantee.
- **Output and action checks.** Check the answer and each proposed action against the task of the user, for example that an email is sent only to an address the user typed.

## Examples

The examples are abstract. They use placeholders in angle brackets, never real instructions.

**A summarizer with no tools.** The instructions $I$ ask for ⟨a summary of the document⟩, and $D$ is a document that contains ⟨a sentence addressed to the assistant⟩. The worst case is a wrong summary. The harm is small because the application can do nothing but write text, so least privilege already bounds the attack.

**An assistant with tools.** The application can read the inbox and send emails. A message from an unknown sender contains ⟨a sentence that asks the assistant to forward data⟩. If the model may call the send tool with arguments derived from that message, the attacker can cause data to leave without the user's consent. The design defense is a label check:

| part of the context | source | label |
|---|---|---|
| $I$ | developer | trusted |
| $U$ | user | trusted |
| message from an unknown sender | email | untrusted |
| result of a search | web | untrusted |

| proposed action | arguments depend on | allowed by the policy |
|---|---|---|
| show a summary to the user | any part | yes |
| send an email to an address typed by the user | $U$ only | yes, after confirmation |
| send an email to an address found in a message | untrusted part | no |

The check runs outside the model, as a program, so it holds whatever the model was led to propose. The cost is that some useful actions need a confirmation by the user.

**The SQL analogy, made exact.** In a query built by joining text, a value with a quote character can end the string and start code; a parameterized query sends the value in a separate field, so the database never parses it as code. A prompt has no separate field for data that the model is bound to respect, which is the difference between the two attacks.

## Where it is used

- **Threat models of LLM applications.** Every application that adds retrieved or tool data to the context of a model, such as browsing assistants, email agents and coding agents, must assume indirect injection from each source of data.
- **Security evaluations.** Benchmarks place made-up injected tasks in synthetic data and measure how often an agent performs them, with and without defenses. Such numbers are measurements for one model and one attack set.
- **System design.** Privilege separation, label tracking and confirmation steps for agents come from the design of secure systems, such as reference monitors and information flow control, applied to models.
- **Research on robustness.** Training models to give priority to the instructions of the developer over text in the data is an active line of work; it lowers success rates but gives no guarantee against adaptive attackers.

## References
