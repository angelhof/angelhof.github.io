---
layout: post
title: How to effectively read a systems paper
overview: true
tags: [systems, paper reading, PhD]
---

Reading a research paper takes time, and in order to get something out of it it is helpful to guide the process using a set of concrete questions about the paper and its thesis. Having a set of questions in mind can help the reader (1) better place the paper in the context of the literature, and (2) evaluate it in a more critical way.
Of course there is no one universal best way of reading a paper, but I have found that this approach works for my first reading pass.

Here is a set of questions that I have found to be relevant for many systems papers.
These questions have been inspired by the ones suggested at a graduate seminar course taught by [Benjamin C. Lee](https://www.seas.upenn.edu/~leebcc/) that I attended while in grad school.
Note that different questions apply to papers in different (sub)areas and that the questions below mostly apply to papers that propose a novel computer system, usually published in venues such as SOSP, OSDI, NSDI, EuroSys, ATC, PLDI, ASPLOS, etc.

- __Problem statement:__ 
    - What is the problem that this paper tries to address? 
    - Why is this problem important? 
    - How is it motivated? 
    - Why is the problem not solved yet? 
    - What is the state of the art?
- __Key insight:__ 
    - What is the key insight/technique of the system solution? 
    - What assumptions does it make? 
    - Are these assumptions satisfied in general or do they break in some contexts? 
    - Is this insight portable to different domains with similar assumptions?
- __Evaluation:__ 
    - What are the key claims that the paper evaluates? 
    - Do these claims relate to the problem that was phrased in the problem statement? 
    - Does satisfying these claims address the central paper problem? 
    - For each claim:
        - __Benchmarks and workloads:__
            - What is the set of benchmarks and workloads that are used?
            - Are the benchmarks realistic and representative of the stated problem?
        - __Experimental infrastructure:__
            - What is the experimental infrastructure? 
            - Do conclusions acquired using this infrastructure transfer to the problem domain?
        - __Baselines:__
            - What are the baselines used to compare the target system against?
            - Do the baselines correspond to the state of the art?
            - How does the target system compare against them?
