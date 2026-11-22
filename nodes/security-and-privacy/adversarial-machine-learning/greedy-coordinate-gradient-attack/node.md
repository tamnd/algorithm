---
tag: C3XD4J
kind: technique
slug: greedy-coordinate-gradient-attack
name: Greedy coordinate gradient attack
aliases:
- GCG attack
- universal jailbreak suffix
area: security-and-privacy/adversarial-machine-learning
level: research
summary: "An automated search for a token suffix that makes an aligned language model answer requests it should refuse. This page covers the threat model, the lesson for alignment and the defenses."
prereqs: [adversarial-example, language-model, reinforcement-learning-from-human-feedback]
see_also: [prompt-injection, universal-adversarial-perturbation, adversarial-transferability, perplexity, adversarial-training, randomized-smoothing, language-model-watermarking, backward-pass-differentiable-approximation]
sources:
  - url: https://arxiv.org/abs/2307.15043
    title: Andy Zou, Zifan Wang, Nicholas Carlini, Milad Nasr, J. Zico Kolter and Matt Fredrikson, Universal and transferable adversarial attacks on aligned language models, arXiv 2023
    locator: the abstract and the threat model, the claim of universality over prompts and of transfer from open models to other models
  - url: https://arxiv.org/abs/2309.00614
    title: Neel Jain, Avi Schwarzschild, Yuxin Wen, Gowthami Somepalli, John Kirchenbauer, Ping-yeh Chiang, Micah Goldblum, Aniruddha Saha, Jonas Geiping and Tom Goldstein, Baseline defenses for adversarial attacks against aligned language models, arXiv 2023
    locator: three kinds of defense (perplexity detection, input preprocessing by paraphrase and retokenization, and adversarial training) in white-box and gray-box settings
  - url: https://arxiv.org/abs/1902.06705
    title: Nicholas Carlini, Anish Athalye, Nicolas Papernot, Wieland Brendel, Jonas Rauber, Dimitris Tsipras, Ian Goodfellow, Aleksander Madry and Alexey Kurakin, On evaluating adversarial robustness, arXiv 2019
    locator: the need for adaptive attacks when a defense is evaluated
---

The greedy coordinate gradient (GCG) attack of Zou, Wang, Carlini, Nasr, Kolter and Fredrikson (2023) showed that the safety training of large language models can be defeated by an automatic search, the way image classifiers are defeated by [adversarial examples](/adversarial-example/). The search adds a short sequence of tokens to a request and changes it, by a combination of greedy and gradient-based search over discrete tokens, so that the model starts its answer in an affirmative way instead of refusing. The authors reported that one sequence found on open models for many requests at once often worked on other requests and on other models, including closed models behind public interfaces. This page describes the attack only at the level of the abstract of the paper. It gives no sequence, no request and no detail of the search, and it spends most of its length on the threat model, the conditions the attack needs and the defenses.

**Threat model.** The goal is a policy violation: the model produces content that its safety training is meant to refuse. The knowledge is white box on one or more open models (weights and gradients), and black box on the target, which is reached by transfer. The capability is to control part of the text of the request; the attacker cannot change the weights, the system instructions or the filters of the target. The defender controls the model, its training, and any filter on the input or the output.

## In plain words

A chat model is trained to refuse some requests. That training changes how the model answers, but it does not change the fact that the model is a function of the text it reads, and that this function can be searched.

The attack treats the extra tokens as a key to search for. It changes them step by step, keeps a change when the model looks more willing to answer, and repeats. The result is often nonsense to a person, but it moves the model past its refusal.

The lesson for defenders is that refusal training alone is not a security boundary. A model can be pushed by text that no person would write, so defenses must expect it.

## When it applies

- **Access for the search.** The search needs the gradient of the model with respect to its input tokens, so it runs on models whose weights the attacker has. A closed target is reached only by transfer from such models, and transfer is not guaranteed.
- **A measurable goal.** The search needs a score to raise. In the paper it is the probability of an affirmative start of the answer, which works as a stand-in for compliance.
- **Free text in the request.** The attacker must be able to place arbitrary tokens in the request. Interfaces that restrict or rewrite the input remove this condition.
- **No filter on unusual text.** The sequences found by the plain search have very low likelihood under a [language model](/language-model/), so a filter based on [perplexity](/perplexity/) can flag them; the attack applies when no such filter runs, or when the attacker adapts to it at a cost.
- **Shared weaknesses.** Transfer works best between models with similar training data and similar alignment methods, which is the case for many open models.

## The template

The shape of the attack and the points where the defender acts. The holes in angle brackets are the stages of the paper's abstract; none of them is a parameter, a string or a search rule.

```pseudo id=main
GCG-THREAT-MODEL(open models M_1..M_r, target model M*, requests Q)
L1  choose ⟨a target behaviour⟩ that the safety policy forbids       ▷ defense: policy and refusal training
L2  attach ⟨an adversarial token sequence⟩ to each request of Q        ▷ defense: input rules and rewriting
L3  improve the sequence by ⟨greedy and gradient-based search⟩ on M_1..M_r
                                                                       ▷ needs open weights; defense: none at the target
L4  aggregate the objective over ⟨many requests and models⟩            ▷ for universality and transfer
L5  send the request with the sequence to M*                          ▷ defense: perplexity filter, paraphrase, retokenization
L6  observe whether M* complies                                       ▷ defense: output moderation, logging, rate limits
```

Line L3 is the only stage that needs the gradient, and it runs on models that the attacker owns, so the target sees none of it. Every defense of the target acts at lines L1, L2, L5 or L6. Lines L5 and L6 are where filters and monitors work; line L1 is where training works.

**The defense points.**
- **Detection by perplexity (line L5).** Compute the perplexity of the request, or of a window of it, under a reference model, and flag text that is far less likely than normal requests. Jain et al. (2023) found that this catches the plain attack, and that an attacker who also asks for low perplexity has a harder search and a weaker result; a strict threshold also flags some benign but unusual inputs.
- **Input preprocessing (line L5).** Paraphrase the request with another model, or change its tokenization, before the target reads it. Both break the exact token sequence the search found, at some cost in the quality of answers to benign requests.
- **Adversarial training (line L1).** Train the model on attacked requests, as in [adversarial training](/adversarial-training/) for images. In text, the inner search is expensive, which limits how far this goes.
- **Output moderation (line L6).** Classify the answer, not the request, and withhold it if it violates the policy. This does not depend on the form of the request.
- **Smoothing over perturbed inputs (line L5).** Answer several randomly perturbed copies of the request and take a vote, in the spirit of [randomized smoothing](/randomized-smoothing/); adversarial sequences tend to be brittle under small changes. There is no certificate here comparable to the one for images.

## Classic examples

- **Universal perturbations for images.** One image change that fools a classifier on most inputs, the [universal adversarial perturbation](/universal-adversarial-perturbation/), is the image counterpart of a sequence that works for many requests.
- **Transfer from surrogate models.** Black-box attacks on image classifiers by [transferability](/adversarial-transferability/) from a model the attacker trains are the counterpart of line L4.
- **Obfuscated gradients.** The history of image defenses, where many filters and preprocessing steps were broken by adaptive attacks such as [BPDA](/backward-pass-differentiable-approximation/), is the warning for text filters at line L5.
- **Prompt injection.** [Prompt injection](/prompt-injection/) is a different threat: the attacker controls data that the model reads, not the request of the user, and the goal is to change what the model does for that user.

## Variations

- **Readable sequences.** Later work searched for sequences that read as normal text, to pass perplexity filters. This is the adaptive attacker that Jain et al. anticipated; it trades search cost and success rate for lower perplexity.
- **Attacks without gradients.** Other work uses only the answers of the target, or another model that rewrites requests, so that line L3 needs no open weights.
- **Multi-model and multi-request objectives.** Summing the objective over more models and requests at line L4 aims at better transfer.
- **Defense in depth.** Deployed systems combine input filters, output classifiers, monitoring and rate limits, because no single layer is robust.

## Pitfalls

These are pitfalls for defenders and for evaluations.
- **Treating refusal training as a boundary.** Line L1 alone does not stop an automated search. Keep the model's permissions small, so that a model that complies can still do little harm, as in the [principle of least privilege](/principle-of-least-privilege/).
- **Evaluating a filter against the plain attack only.** A perplexity filter at line L5 beats the plain search but not an adaptive one; evaluate against an attacker who knows the filter, as Carlini et al. (2019) ask for image defenses.
- **Ignoring false positives.** A strict filter at line L5 blocks benign but unusual text. Report the rate on benign inputs next to the detection rate.
- **Measuring success by the first words.** An affirmative start does not always lead to harmful content, and a refusal can come later. Judge the full answer at line L6 when measuring both attacks and defenses.
- **Reporting robustness from one model.** Transfer rates differ between models and versions; a defense measured on one model may not hold on the next.

## Exercises

1. A perplexity filter flags a request if its perplexity under a reference model is above a threshold $\tau$, set as the empirical $(1 - q)$ quantile of the perplexity of $n$ benign requests. Under the assumption that new benign requests have the same distribution and that ties have probability zero, show that the probability that a new benign request is flagged is at most $q + 1/(n + 1)$.
2. An abstract model: a filter sees a sequence of $k$ symbols from a made-up alphabet $\{a_1, \dots, a_4\}$, and a reference model gives each symbol probability $1/2, 1/4, 1/8, 1/8$, independently. Compute the perplexity of the sequences $a_1 a_1 a_2 a_1$ and $a_3 a_4 a_3 a_4$, and find the smallest threshold at which the filter passes the first but flags the second.
3. Explain why the defense points at lines L5 and L6 still act when the attacker has full white-box access to an open model at line L3 but only query access to the target.

## References
