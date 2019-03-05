---
layout: post
title: Discussing "An optimality theory of concurrency control for databases" by Kung & Papadimitriou 
overview: true
tags: [serialization, concurrency, weak-serialization, scheduling, paper, linearizability]
---
**TODO: Bazw ta links ths bibliografias**

**TODO: Ftiaxnw ta footnotes san tou Tim Urban**

This blog post is an intro to a (possibly long) series of posts that revolve around correctness criteria of concurrent objects and systems, most notably linearizability, sequential consistency, serializability, etc. My objective is to write those blog posts to help me better understand the above concepts, both because writting helps getting to the bottom of an issue, as well as because of occasional feedback that I might get from any reader.

I was planning to first read several important papers in this field and then organize them in a series of posts and that is why I started reading [Kung & Papadimitriou 78]. However, while reading it I was amazed by their results, and I thought that this specific paper might be a post on its own.

In this post, I will try write my thoughts while reading this paper, rephrasing and explaining their results, trying to elaborate more on them. While this post was mostly written to help me understand the paper, I think that it might be helpful to read it side by side with the original paper, to maybe get a firmer grasp of some ideas or implications that could be easily skipped if one doesn't pay too much attention (they certainly did skip me when I first read the paper). As I am far from an expert on this field (maybe not even knowledgable) I would encourage any comment or feedback on anything that is wrong, misphrased, etc of this post.

After this long (and possibly unnecessary) introduction let's get right into the paper.

## Motivation

Object systems[^1] are data systems that are shared among multiple users. An object system, usually comes with a description of what it means for the data that it stores to be consistent. It is important for the data that is stored in the object system to always satisfy those requirements. For example, imagine a banking system which contains the data about the bank accounts of the bank's clients. A consistency requirement is that an account should never contain negative amounts of money.

User interact with an object system through sequences of requests (aka transactions) that read or update values of the system. Therefore an issue that naturally arises is making sure that executing the user requests on a consistent object system, should preserve its consistency. In a single user environment, this task is relatively simple, since each transaction is executed as a contiguous block, and a transaction starts executing only when the previous has finished. In this setting, the problem reduces to verifying that each transaction preserves the consistency requirements of the object system (if executed on a consistent state of the system). In the multi-user setting however, the problem is much harder, because even if each transaction preserves consistency; arbitrarily interleaving their requests might not.

<!-- It is desirable for a (database/object system) to be time-shared among multiple users.  -->
<!-- The different steps of different requests may be interleaved in any order, and despite assuming -->
<!-- that each transaction is correct on its own (it preserves the consistency of the database), -->
<!-- when arbitrarily interleaved with other transactions it might bring a consistent database state  -->
<!-- to an inconsistent one.  -->

<!-- Interpretation: -->
<!-- When there is only one user performing requests to the object system, it is easy as a problem to -->
<!-- verify and maintain consistency, because each request is executed after the other has finished. -->

<!-- If the multi-user system was also implemented in a naive way, a user would acquire a lock for -->
<!-- each one of their requests and release it when done. Then if each request preserves the consistency of -->
<!-- the database, inductively, the database is always in a consistent states if it starts from one. -->

<!-- However, acquiring a lock, and processing every request atomically offers very low performance, -->
<!-- and doesn't scale to many users.  -->

<!-- Thus in the quest for performance, requests from different users are allowed to be interleaved in  -->
<!-- possibly arbitrary ways. However, now the task of mainting consistency is not as simple, and  -->
<!-- executing arbitrary interleaving of (consistence preserving) requests, doesn't necessarily maintain -->
<!-- consistency. -->

<hr>

**TODO:** Introduce concurrent access control mechanisms before just stating them here

It is clear that consistency preservation should be the primary objective of a concurrent "access" control mechanism. However, it can't be considered in isolation. A trivial solution to preserve consistency would be to execute all transactions of the first user until they log off, then execute the transactions of the second user until they log off, etc. This execution order clearly preserves consistency, and enforcing it requires minimal information from each transaction (just the id of the user who issued it). However, its performance is disastrous! The more users interact with the system, the more each user has to wait until its requests are processed. Imagine wanting to transfer some money between some accounts on an online banking system, and having to wait for all the users who logged in before you to log out before the system processes your request. 

Therefore, there are two necessary properties to consider when designing a concurrent "access" control mechanism (which from now on we will call scheduler). 
- **Performance:**
  Which ideally represents how long does it take for a set of transactions to complete under the scheduler. Note that there is no universal metric of performance, so even reasoning about it can be tricky.
- **Information:**
  Which represents the information that the scheduler needs to make its decision. This typically includes syntactic and semantic information for the transactions as well as the integrity constraints.
  
Our objective as the designers of a scheduler is for it preserve the consistency requirements of the database, while striking a balance between performance and information needed. In this paper, the authors formalize this tradeoff between performance and needed information, and present upper bounds for several information granularities. They show that given only syntactic information, **serialization** [Bernstein et al 1978, Papadimitriou 1979]
is the best one can hope for and when also given semantic information, **serialization** can be relaxed to a weaker form.

<!-- Consistency is the primary objective of concurrent "access" control. However, it is not the only -->
<!-- one. Trivial solutions exist for concurrent consistency, but they offer disastrous performance. -->
<!-- A trivial one would be to only execute user1's requests until they log off, then execute user2's... -->
<!-- This clearly lacks regarding performance, however it has a serious benefit. The concurrency control  -->
<!-- mechanism only needs to know about the User ID associated with each transaction to make its decisions. -->

<!-- Therefore, there are two necessary properties to consider for the design of a scheduler. -->
<!-- - **Its performance** -->
<!--   They measure performance as the set of request sequences which the scheduler can pass without  -->
<!--   any delay. So in the sense it is some form of latency. They call this set the __fixpoint set__ of  -->
<!--   a scheduler and they argue that if a scheduler has a strictly larger fixpoint set, it performs better -->
<!--   when regarding average delays (this seems a bit not believable). -->
  
<!-- - **The information that it needs/uses in order to schedule requests** -->
<!--   Typical information can be: -->
<!--   + syntactic information about the transactions -->
<!--   + semantic information about the meaning of the data and the operations performed -->
<!--   + integrity constraints, or the consistency requirements that the data must satisfy -->
<!--   However,they claim that excessive information might be distracting and make the  -->
<!--   scheduler less efficient. (Examined in detail in [Papadimitriou 1979]). -->
<!--   In addition, some information might not be available (like the integrity constraints -->
<!--   and if the semantics are expressed in a powerful enough language, then the scheduler  -->
<!--   may be faced with undecidable problems. -->
  
<!-- Intepretation: -->

<!-- We clearly want consistency as our main objective, when designing the concurrent access controller. -->
<!-- However, we have to somehow balance between performance and the information that the scheduler  -->
<!-- needs in order to make its decisions, because by designing it poorly we might end up with horrific -->
<!-- performance, or with undecidable decisions.  -->

<!-- -------------------------------------------------------------------------------------------------- -->
  
<!-- They examine the literature about concurrency control andy give a uniform (__uniform in what sense__) -->
<!-- framework to evaluate different solutions. They point out that there is a tradeoff between performance -->
<!-- of a scheduler and the information that it uses. Their approach allows them to formally show, that -->
<!-- when only syntactic information is available, **serialization** [Bernstein et al 1978, Papadimitriou 1979] -->
<!-- is the best one can hope for (__what does best mean?__). In case of semantic information, other approaches -->
<!-- [Lamport 1993] could be used. -->

<!-- -------------------------------------------------------------------------------------------------- -->

## Transaction Systems

> WARNING: The point of this post is to be self-contained, and so below follow some necessary definitions that will allow us to formalize the notions and results discussed in the paper. If you don't want to realy understand the results of this paper formally, skip ahead to [this section](#optimal-schedulers) where the results are presented and explained in a more informal manner.

### Syntax

**LEFT HERE**

**Syntax**

By a transaction system, they mean a database (data and integrity constraints) together with a set of prespecified transaction programs. In a sense a database is an object, with private data, invariants or integrity constraints that must always hold for this data, and a set of methods that are used to access and modify the private data.

They define transactions to be *finite* sequences of steps, where each step reads from a global variable to a local one and writes to the global variable, based on the values of the local variables in all previous steps. Note that each step is indivisible (atomic) and that transactions are straight line programs in this simplified model. (They claim that in Section 6 they extend those to transactions defined by more general programs.
  
**Semantics**

They assume that each transaction is executed only once and that a state of the transaction system T is a triple (J, L, G) where J is a product of program counters which show the next step of each transaction, L is a product of the values of all local variables, and G is a product of the values of all global variables. 

Integrity constraints can be given as a subset of all possible value products of the global variables. A sequence of transaction steps is said to be **correct** if a serial execution of the steps in the sequence will map any consistent state of the transaction system into a consistent state.

**The basic assumption that they follow (and most other papers in the literature) is that all transactions in a transaction system are correct, so their sequential executions are correct. Verifying that a sequential transaction is correct is a different task, which is supposed to be much easier and orthogonal to the task that all those papers try to solve. All of those papers reason about the subset of interleavings of possible transactions that are correct, given that the transactions themselves are correct.**

At the end of section 2 they give an example of the system that might be useful to use as a guiding example.

--------------------------------------------------------------------------------------------------

**Schedules**

They define a schedule π of a transaction system to be a permutation of the set of steps in $$T$$ such that the
steps in each specific transaction are kept in order. In practice a schedule is an interleaving of all the transaction steps. The set of all schedules of $$T$$ is denoted by $$H(T)$$. A schedule is said to be **correct** if its execution preserves the consistency of the database. The set of all correct schedules of $$T$$ is denoted by $$C(T)$$. The set $$C(T)$$ is always non empty as it at least contains all serial schedules (the ones that execute one transaction after the other).

Interpretation:

In this paper they don't really deal with what linearizability deals. There are several main differences to what I think of as linearizability. First of all, transaction steps are strictly atomic. Second, each transaction doesn't return any output, so our observation is always the state of the object. In addition, we have a set of invariants (integrity constraints) that have to always hold during the system execution.

**NOTE: It seems that a very important difference in many of those papers, is what they consider as observable. Is it the outputs of the requests to the system? Is it the system state? Is there a global observable time of requests? All those slight differences in the model, make for (possibly) interesting changes in the different approaches, and I would like to understand whether those different assumptions make a real difference. At least I want to mention this and ensure that I explicitly claim what do I think is observable**

NOTE: Another important note is that in this work they assume **FIFO communication channels** between each client and the database, so a schedule is always an interleaving where each individual client's requests are not reordered. This is very similar to sequential consistency, so here they already assume that schedules are sequentially consistent. _This makes some sense, because reordering individual client's requests might only need to happen in a distributed object system. **IS THAT CORRECT?**_

--------------------------------------------------------------------------------------------------

**Scheduler**

A scheduler has to transform any schedule to a correct schedule. So it is a mapping S from H to C(T). A scheduler is correct when all its schedules are correct. They measure the **performance** of a scheduler by its fixpoint set P, which is defined to be the largest subset of H satisfying the following:

$$
S(h) = h \forall h \in P
$$

In a sense, a scheduler's fixpoint set, is the set of execution request sequences (schedules) that the scheduler keeps intact, without changing (it grants requests in the same order that they arrive). **NOTE: This is clearly not a universal performance metric but they explain in Section 6 why it is good enough**

Except for the performance of the scheduler (aka how long do requests have to wait until they are released), we must also think about the cost of the scheduler making decisions. This is either the information or the time thata scheduler requires to make a decision. In this work they derive upper bounds on the performance of schedulers based solely on the **information** that they use (the time that a scheduler needs to make its decisions is addressed in [Papadimitriou 78]).

Ideally we would want P to be equal to C(T), so that the scheduler lets all correct schedules pass intact. However, this is not always possible nor desirable because of the need for a lot of information. Below, they capture this in a formal theorem. What is a formal model of the information abailable to a scheduler S.

--------------------------------------------------------------------------------------------------

## Information Levels

**A format theory**

A **level of information** available to a scheduler about a transaction system T is a set I of transaction systems that contains T. Intuitively, if S keeps this level of information, it know that T is among I, but doesn't know exactly which. 


**SIDE NOTE: Abstractions, Operations, and the properties that they have to satisfy**
NOTE: _I_ represents in a sense the abstraction that the scheduler does. The granularity to which it can distringuish amond different systems using the information that it gets. The more information (observables) the scheduler has, the finer distinctions it can make between different transaction systems, and thus the smaller the set I will be. This is a general phenomenon, when trying to reason about a system (If I am not wrong, it is also the idea behind abstract interpretation). Reasoning about the system itself is undecidable or requires an extreme amount of information, so the system is thought of as a set of systems, that are all equivalent to its other based on the amount of information that we get. Thus any operation or transition that the system does has to be lifted to the set of systems, and that is where imprecision can lead to very bad results. In a sense we want well behaving approximations, abstractions, that is abstractions that are size preserving when we apply to them operations that we would normally only apply to the system itself. For example, an range abstraction on integers, is not well behaving when the operation that we apply on our states/systems is multiplication with numbers larger than one. Because, when we multiply a number in the range [1, 10] with 2, we can only get [2, 4, .., 20], but our range abstraction will return [2, 20]. A point to be made here is that abstractions have to be chosen together with the operations that are to be applied on the abstracted object, and applying the operations on the abstractions must have some nice properties.

Alternatively we could define I as a projection that maps any transaction system to an object I(T). Then two transaction systems T T', can not be distinguished with level information I, if they map to the same I(T) = I(T').

**Theorem 1:** 
For any scheduler using information I, its fixpoint set P must satisfy:

$$
P \subseteq \bigcap_{(T' \in I)} C(T')
$$

The scheduler cannot distinguish between the different transaction systems in I, and because of that, all the schedules that it allows intact, have to be in the correct sets of schedules of all the indistinguishable transaction systems in I. Otherwise the scheduler might end up allowing a non correct schedule to pass, which should certainly not be allowed. Thus this upper bound on P shows what is the largest P we can hope to achieve with a specific amount/level of information. The proof of this theorem uses an adversary argument.

**SIDE NOTE: It seems like in general when we want to prove something for all, we can assume for contradiction that one of the forall doesn't hold, and then use an adversary to somehow expose that one that doesn't work and create a contradiction.**

As a corollary, an optimal scheduler (in regards to this metric of performance, has a fixpoint set P equal to this upper bound. 

Using the above definitions of levels of information and performance, we can partially order schedulers based on sophistication (A scheduler S is more sophisticated than S', if I \subseteq I') and we can also partially order them in respect to performance (S performs better than S', if P' \subseteq P). Then the mapping from any level of information I to the fixpoint set of the optimal scheduler for I:

I -> P (= \bugcap ...) is a natural *isomorphism* between these two partially ordered sets. This capture the fundamental trade-off between scheduler information and performance. If I \subseteq I', then P' \subseteq P, for the optimal schedulers.

--------------------------------------------------------------------------------------------------

## Optimal Schedulers

**Maximum and Minimum Information Optimal Schedulers**

The optimal **maximum information** scheduler has I = {T} and because of that P = C(T).

The optimal **minimum information** scheduler produces only serial schedules, and thus only has serial schedules in its P. The proof is clear, by just constructing a contradiction when a scheduler with minimum information produces any non serial schedule interleaving.

--------------------------------------------------------------------------------------------------

**Optimal Schedulers for Complete Syntactic Information** (WOW)

Suppose that all syntactic information is available, so I is the set of all transaction systems with the same syntax. (**NOTE(That might be wrong): From what I understand knowing the syntax of the program, means that we know all the names of functions and the arguments that they are given but not the the semantics of the calls themselves. So we don't know what might happen after a call. TODO: Make sure I understand this correctly**) 

A schedule is **serializable** if its execution results (**QUESTION: FINAL OR ALSO INTERMEDIATE RESULTS??**) are the same as the execution results of some serial schedule under the _Herbrand semantics_ (**Read side note below**). 

(**NOTE: A serializable schedule is one that cannot be distinguished (by looking at the execution results) by a serial schedule, which we said that is correct by definition. Because of the Herbrand semantics, two final results are equal, when exactly the same function calls and arguments where used to compute them. So "same execution results" means syntactic equality.**) 

(**NOTE 2: A schedule is serializable if we can reorder its steps to a serial one, while keeping the exact same syntactic results. For example the assignment x := f1(x) might sometimes preserve the value of variable x (based on some branching in f1). However, because we only have knowledge of syntax, we can only reorder the assignment x := f1(x) with the assignment x := f1(x) and not with x := f2(x) despite knowing that for x f1 and f2 return the same value.**) 

By SR(T) we denote the set of all serializable histories of T. A **serialization scheduler** is defined to be a scheduler S whose P = SR(T) and S(H) = P for any T. So it is the scheduler that allows all serializable schedules to pass without an issue, and that maps every other schedule to a serializable one. In a sense, a serialization scheduler, is "faster" than a serial scheduler because it allows all serializable schedules to pass by intact, and ensures correctness for H by making sure that there exists a reordering of it that gives syntactically equivalent results (under Herbrand semantics) to a serial schedule (which is always correct no matter what). In a sense, the way they make schedulers, is that they build them on top of the simple serial schedulers (which are correct by definition) by allowing them to do equivalent reorderings to schedules to bring them to a serial one. The other approach would be to make sure that the schedule preserves the integrity constraints, but that requires syntactic, semantic, and integrity information, making the problem undecidable(**is it correct that it becomes undecidable?**)

**Side Note on Herbrand Semantics:**
Herbrand semantics is a way to give semantic meaning to syntax, while not losing any information. What it does essentially is to interpret a function call, using the function call syntax itself. It is in a sense like lazy computation, where we keep every function call unintepreted, but we know that it was called. So the semantics of a final assignment migh be f1(x, f2(y,z)).


**Theorem 3:** WOW
The serialization scheduler is:
1. Correct
2. Optimal among all schedulers using complete syntactic information.

**Proof:**
1. To prove correctness (SR(T') \subseteq C(T') for any T' \in I), (so the fact that all serializable schedules are correct), they use Herbrand's theorem [Manna 74] which states that if two sequences of steps are equivalent under the Herbrand interpretation, they are equivalent under any interpretation. 

(Of course this assumes that functions are pure and don't introduce any side effect, so the interpretation of a function call f1(a1, a2, ..., an) only depends on f1, a1, a2, ..., an and nothing else.)

Thus if h \in SR(T') then the execution results of h are the same as those of some serial schedule for T'. This implies that for any h \in SR(T'), the execution of h preserves the consistency of T', as serial schedules all preserve the consistency of T', and thus h \in C(T').

2. To prove optimality, given a history h not \in SR(T), they want to define a transaction system T' \in I(T) such that h not in C(T'). The semantics of T' are the Herbrand interpretation to simplify things. Now they give the stricter possible integrity constraints, that is (a1, a2, ..., ak) \in IC iff there exists a possibly empty sequence S of steps that is a concatenation of serial executions of transactions such that the initial values (v1, v2, ...vk) of the global variables are transformed by S to (a1, a2, ..., ak). By this definition, all transactions are individually correct, and the basic assumption holds. Now it is easy to see that, if h is any history, not in SR(T'), then it transforms the initial values (v1, ..., vk) to a set of values not in IC, so h not in C(T').

**NOTE:** The optimality proof is based on the idea that a scheduler has to produce correct schedules for any transaction system, under any semantics, and with any integrity constraints. They use that in their favor, to construct a very strict transaction system, using the Herbrand semantics, and the integrity constraints that only serial executions of transactions lead the transaction system to a state that satisfies the IC. 
To get a better intuition of the construction of a transaction system T' done in the proof, below follows an example (inspired by the Figure1 in section 4.3 of the paper, but slightly different) of a transaction system T' where:

A system with one global variable x with initial value x0, and two transactions
T1: x := f1(x); x := f2(x)
T2: x := f3(x)

The set of acceptable final states IC = {x0, x1, x2, x12, x21} 
where x1 is the value of x after executing T1 so x1 = f2(f1(x0)), similarly x2 = f3(x0)
and x12 is x after executing T1; T2 so x1 = f3(x1) and similarly x21 = f2(f1(x2)).

Note that for this specific transaction system, the set of serializable schedules is the set of serial schedules, as there is no way to reorder any non serial schedule to give the same results (under Herbarnd semantics) with any serial schedule.

The above theorem shows that given complete syntactic information of the transactions, one can hope to create a scheduler whose P is at most equal to SR(T), because anything more than that wouldn't be correct for some interpretation and integrity constraints. That is why, most approaches to concurrency control (at the time) had serialization as their goal [citations].

**QUESTION: How do we find a serializable schedule in the first place???**

In [Papadimitriou 78] it is shown that for some transaction systems of restricted syntax, although serialization is intractable (**I guess because all the different serial orderings are exponentially many**), it can be **approximated** by more restrictive schedulers. (See also [Papadimitriou 77]). So in practice, we cannot even expect to get a scheduler with performance P = SR(T).

--------------------------------------------------------------------------------------------------

**Optimal Scheduler for Complete semantic information, without integrity constraints**

In the example above, the history h = (T11, T21, T12) is not serializable since its final Herbrand value is not in IC. However, given an interpretation of the functions as f1(x) = x + 1, f2(x) = 2 * x, and f3(x) = 3 * x the history T11, T21, T12 returns the same value for x as the T1;T2 history. This shows, that given semantic information, a serialization scheduler, is not optimal, as we can do better. 

Therefore, they define a generalized notion of serialization as follows:

A schedule h is said to be weakly serializable, if starting from any state E, the execution of the schedule will end with a state that is achievable by some concatenation of transactions, possibly with repetitions and omissions of transactions also starting from state E. This way we extend P to be the set of schedules that lead to a semantically equivalent final state, instead of a syntactically equivalent one (which is semantic equivalence under Herbrand interpretation).

Denote by WSR(T) the set of all weakly serializable schedules of T. It is clear that SR(T) \subseteq WSR(T). The weak serialization scheduler is defined to be S that satisfies: P = WSR(T) and S(H) = P for any T. Similarly to above, it holds that the weak serialization scheduler is optimal among all schedulers using all information (syntactic and semantic) but the integrity constraints. 

## Discussion

<hr>

{% comment %}
Footnote Section
{% endcomment %}

[^1]: A standard instance of an object system is a database.
