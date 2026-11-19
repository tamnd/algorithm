---
tag: 4AXNKS
kind: technique
slug: chain-of-thought-prompting
name: Chain-of-thought prompting
aliases:
- chain of thought
- CoT prompting
area: natural-language-and-speech/language-modeling
level: research
summary: Put worked reasoning steps into the prompt so that a language model writes steps before its answer. Measured gains on multi-step problems appeared only in models of about 100B parameters.
history:
  year: 2022
  people: [Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc V. Le, Denny Zhou]
  note: "Wei and colleagues at Google measured the method on arithmetic, commonsense and symbolic tasks with LaMDA, GPT-3 and PaLM. The paper appeared at NeurIPS 2022, as did the zero-shot variant of Kojima and colleagues."
prereqs: [in-context-learning, generative-pretrained-transformer, greedy-decoding]
see_also: [self-consistency-decoding, plurality-voting, condorcet-jury-theorem, temperature-sampling, instruction-tuning, neural-scaling-law, program-synthesis, language-model]
sources:
  - url: https://arxiv.org/abs/2201.11903
    title: "Jason Wei, Xuezhi Wang, Dale Schuurmans and others, Chain-of-thought prompting elicits reasoning in large language models, NeurIPS 2022"
    locator: "Section 3.1 and Figure 1 (the eight exemplars and the tennis-ball example), Section 3.2 (gains only at about 100B parameters, the error analysis), Figure 5 (equation only, dots only and chain after answer), Section 4 (StrategyQA 75.6% against 69.4%), Section 5 and Table 5 (symbolic tasks), Table 2 (all models on five arithmetic benchmarks), Table 3 (MAWPS subsets)"
  - url: https://arxiv.org/abs/2205.11916
    title: "Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo and Yusuke Iwasawa, Large language models are zero-shot reasoners, NeurIPS 2022"
    locator: "abstract (MultiArith 17.7% to 78.7% and GSM8K 10.4% to 40.7% with text-davinci-002)"
  - url: https://arxiv.org/abs/2203.11171
    title: "Xuezhi Wang, Jason Wei, Dale Schuurmans and others, Self-consistency improves chain of thought reasoning in language models, ICLR 2023"
    locator: "abstract (sample diverse reasoning paths and take the most consistent answer; GSM8K +17.9, SVAMP +11.0, AQuA +12.2, StrategyQA +6.4, ARC-challenge +3.9)"
---

Chain-of-thought prompting is a way to write the prompt of a pretrained [language model](/language-model/). Each solved example in the prompt shows the intermediate steps, in natural language, before the final answer, so the model also writes steps before it answers a new question. The written steps are called the chain of thought. It is a form of [in-context learning](/in-context-learning/): the weights do not change. It is different from [self-consistency](/self-consistency-decoding/), which is a decoding method that samples many chains and votes on their answers, and from [instruction tuning](/instruction-tuning/), which changes the weights. The gains are measurements on particular models and benchmarks. Wei et al. (2022) found that the method helped only in models of about 100B parameters, and it made smaller models worse. No theorem says that the written steps make the answer correct, or that they are the reason the model gave it.

## In plain words

When you ask a large text model a word problem, it often answers at once and gets it wrong. If the examples you show it work through each problem step by step, and only then give the answer, the model copies that habit. It writes its own steps for the new problem, and on hard problems the final answer is right more often.

This only worked in very large models. Smaller models wrote steps that read well but did not make sense, and they did worse than with plain examples. On easy one-step problems there was little or no gain. The steps also cost time, because the model writes many more words. And a model can write correct-looking steps with a wrong answer, or wrong steps with a right answer.

## When it applies

- The task needs several steps: arithmetic word problems, questions that join several facts, or symbolic tasks such as tracking a state.
- The model is large. In the measurements below, the gains appeared at about 100B parameters.
- The final answer can be read from the output in a fixed form, for example after "The answer is".
- You can pay for longer outputs. A chain of $r$ tokens before an answer of $a$ tokens makes decoding about $(r + a)/a$ times longer.

## The template

**Sizes.** The prompt has $n$ tokens, with $n \le n_{\text{ctx}}$. The model is a [generative pretrained transformer](/generative-pretrained-transformer/) with $L$ blocks of width $d$, $h$ heads, $d_k = d / h$ and a vocabulary of size $|V|$. The chain has $r$ tokens and the answer $a$ tokens. With a key-value cache, each new token costs $O(L(d^2 + t d))$ when $t$ tokens come before it, so the whole output costs $O(L((r + a) d^2 + (r + a)(n + r + a) d))$.

1. **Write the exemplars.** Write $K$ triples (question, chain, answer). Wei et al. wrote one set of eight for all math word problem benchmarks except AQuA, where they used four (Section 3.1). End every chain with the answer in a fixed form.
2. **Build the prompt.** Join the exemplars as "Q: ... A: ..." blocks and add "Q:" with the test question and "A:".
3. **Decode.** Generate until the end of the answer. Wei et al. used [greedy decoding](/greedy-decoding/).
4. **Read the answer.** Take the text after the fixed phrase, and normalize it (for example, a number).

**What is computed.** Write $x$ for the test question, $z$ for a chain and $y$ for an answer. The model defines $p(z, y \mid P, x) = p(z \mid P, x)\, p(y \mid P, x, z)$. Greedy decoding returns one pair $(z, y)$. The answer that is most likely over all chains is $\arg\max_y \sum_z p(z, y \mid P, x)$, which greedy decoding does not compute in general. Self-consistency estimates it by sampling.

**Example.** The first exemplar of Wei et al. (Figure 1) is:

```
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
   Each can has 3 tennis balls. How many tennis balls does he have now?
A: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6 tennis balls.
   5 + 6 = 11. The answer is 11.
```

With standard prompting, the exemplar answer is only "The answer is 11." Both prompts end with the same test question and "A:".

## Classic examples

All results are accuracies in percent, measured by the papers cited, with their exemplars.

**GSM8K and model size (Wei et al., Table 2).** Standard prompting against chain-of-thought prompting:

| Model | Standard | Chain of thought |
|---|---|---|
| PaLM 8B | 4.9 | 4.1 |
| PaLM 62B | 9.6 | 29.9 |
| PaLM 540B | 17.9 | 56.9 |
| GPT-3 6.7B | 4.0 | 2.4 |
| GPT-3 175B | 15.6 | 46.9 |
| LaMDA 420M | 2.6 | 0.4 |
| LaMDA 137B | 6.5 | 14.3 |

The authors (Section 3.2) describe the gain as appearing only at about 100B parameters, with smaller models writing fluent but illogical chains. With an external calculator for the arithmetic, PaLM 540B reached 58.6.

- **Easy problems (Table 3).** On SingleOp, the one-step subset of MAWPS, the change was negative or very small.
- **Commonsense (Section 4).** PaLM 540B reached 75.6% on StrategyQA, against 69.4% for the earlier best result.
- **Symbolic tasks (Section 5, Table 5).** For joining the last letters of the words of a name, PaLM 540B went from 7.6 to 99.4 on two-word names, the length of the exemplars. On four-word names, a length it had not seen in the exemplars, it went from 0.0 to 63.0.
- **Ablations (Figure 5, LaMDA 137B and PaLM 540B).** Writing only the equation before the answer helped little on GSM8K. Writing a row of dots as long as the equation, to give extra tokens with no content, scored about as the baseline. Writing the chain after the answer also scored about as the baseline. The authors read this as evidence that the steps in words matter, not only the extra tokens. That reading is a heuristic.
- **Error analysis (Section 3.2).** In 50 wrong answers of LaMDA 137B on GSM8K, 46% of the chains were almost correct, with small errors such as a calculator error or one missing step, and 54% had major errors.
- **No exemplars (Kojima et al.).** Adding "Let's think step by step" before each answer, with no solved examples, raised the accuracy of text-davinci-002 from 17.7% to 78.7% on MultiArith and from 10.4% to 40.7% on GSM8K.

## Variations

- **Zero-shot.** Use a trigger phrase instead of exemplars, as Kojima et al. did. A second prompt then reads the answer from the generated chain.
- **Self-consistency.** Sample several chains with [temperature sampling](/temperature-sampling/) and return the answer that occurs most often, a [plurality vote](/plurality-voting/). Wang et al. report gains over greedy chain-of-thought decoding of 17.9 points on GSM8K, 11.0 on SVAMP, 12.2 on AQuA, 6.4 on StrategyQA and 3.9 on ARC-challenge.
- **External tools.** Let a calculator or an interpreter do the arithmetic that the chain writes down. Wei et al. measured this with a calculator (58.6 against 56.9 on GSM8K). Writing the steps as a program and running it is related to [program synthesis](/program-synthesis/).
- **Training on chains.** Fine-tuning a model on examples with chains, as part of instruction tuning, is another way to get steps without exemplars in the prompt.

## Pitfalls

- **Small models.** In Table 2, models below about 100B parameters often did worse with chains. Measure the method on your model before you use it.
- **Easy tasks.** On one-step problems the chain costs tokens and gives little or nothing.
- **Steps are not an explanation.** The chain is text that the model wrote. A correct chain does not prove that the model used it, and Wei et al. note chains that reached the correct answer by chance. Do not treat the chain as a faithful record of how the answer was found.
- **Parsing the answer.** If the output does not end in the fixed form, the answer can be read wrongly. Count unparsed outputs as wrong, and report how many there were.
- **Voting is not free accuracy.** The [Condorcet jury theorem](/condorcet-jury-theorem/) says that a majority of independent voters, each right with probability $p > 1/2$, is right more often as the number grows. Samples from one model and one prompt are not independent, so the theorem does not apply to self-consistency. Its gains are measured.
- **Cost.** A chain of 100 tokens before an answer of 3 tokens means about 34 times more decoding steps, and self-consistency with $m$ samples multiplies that by $m$.

## Exercises

1. Assume $k$ independent samples, each with the correct answer with probability 0.6, and two possible answers. Show that the majority of $k = 3$ is right with probability 0.648 and the majority of $k = 5$ with probability 0.68256.
2. Repeat Exercise 1 with $p = 0.4$ and $k = 5$, and show the result is 0.31744. Now let the wrong answers be spread over three values with probability 0.2 each, while the correct one has 0.4. Explain why a plurality vote can still help.
3. From the GSM8K table above, compute the change from standard prompting for each model. Which models get worse? Why is "appears only at about 100B parameters" a measurement and not a law?
4. A prompt has $n = 800$ tokens. The model writes a chain of $r = 120$ tokens and an answer of $a = 4$ tokens. How many decoding steps does it take with and without the chain? With self-consistency over 40 samples, how many in total?
5. Write two exemplars with chains for the task "Is the number of letters in this word even?" Then explain what the "chain after answer" ablation of Wei et al. would look like for your prompt, and what it is meant to test.

## References
