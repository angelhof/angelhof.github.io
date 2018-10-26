---
layout: post
title: Solving Problems using Monads 1 - Reachability
overview: true
---

This is part of a series of posts on solving simple programming problems using Monads. The intention of this series is to help me (and you) learn more about Monads by solving interesting (but simple) programming problems.

Searching for a simple problem to start the series with, I stumbled upon [this kata](https://www.codewars.com/kata/53223653a191940f2b000877). It contains a reachability problem for a pair of nodes in a graph. 

## Problem Definition

Given a pair of nodes \\((s, e)\\) and a list of all edges of a unidirectional graph \\(G\\), decide whether node \\(e\\) is reachable from node \\(s\\). Any linear graph traversal algorithm can be used to solve this problem in a simple and relatively efficient manner.

## Solving the problem without the use of Monads

We will first import the Data.Set in order to keep visited nodes in an efficient data structure.

```haskell
import qualified Data.Set as S
```

The only type definitions that we need are:

```haskell
type Node = Char
type Arc  = (Node, Node)
```

The main function of our problem is:

```haskell
solveGraph :: Node -> Node -> [Arc] -> Bool
solveGraph s e arcs = S.member e visited
  where
    visited = visit arcs [s] $ S.singleton s
```

The function `solveGraph` visits all nodes that are reachable from \\(s\\) and checks if \\(e\\) is one of them. So now we have to define a function `visit :: [Arc] -> [Node] -> S.Set Node -> S.Set Node` that actually performs a Breadth First Search (or any other kind of traversal) on \\(G\\) starting from \\(s\\).

```haskell
visit :: [Arc] -> [Node] -> S.Set Node ->  S.Set Node
visit _ [] visited = visited
visit arcs (n:ns) visited = visit arcs (ns ++ newOpen) newVisited 
  where
    es = S.fromList $ expandOnce arcs n
    newVisited = S.union visited es
    newOpen = S.toList $ S.difference es visited
```

`visit` performs the classic BFS algorithm. What is now left is to define `expandOnce`.

```haskell
expandOnce :: [Arc] -> Node -> [Node]
expandOnce arcs s = [b | (a,b) <- arcs, a == s]
```

`expandOnce` given a node returns all the nodes that are one edge away from it. 

This program works as can be seen below from the interpreter output:

```haskell
Prelude> :l main.hs
[1 of 1] Compiling Graph            ( main.hs, interpreted )
Ok, modules loaded: Graph.
*Graph> let arcs = [('a','b'),('b','c'),('c','a'),('c','d'),('e','a')]
*Graph> solveGraph 'a' 'd' arcs
True
*Graph> solveGraph 'a' 'e' arcs
False
```

## Incorporating Monads in the Solution

This solution is short and solves the problem, but it does not satisfy the initial requirement to use Monads. It is easy to notice that `visit` passes around the `visited :: Set Node` resembling the State monad.

```haskell
newtype State s a = State { runState :: s -> (a,s) }
```

The above `newtype` is provided in `Control.Monad.State` and we could easily think of `visited` as the state. So in order to not pass this around we could reimplement `solveGraph` and `visit` as follows.

```haskell
solveGraph :: Node -> Node -> [Arc] -> Bool
solveGraph s e arcs = S.member e visited
  where
    visited = snd $ runState (visit arcs [s]) $ S.singleton s

visit :: [Arc] -> [Node] -> State (S.Set Node) [Node]
visit _ [] = return []
visit arcs (n:ns) = do
  visited <- get
  let es = S.fromList $ expandOnce arcs n
  let newVisited = S.union visited es
  let newBoundary = S.toList $ S.difference es visited
  put newVisited
  visit arcs $ ns ++ newBoundary
```

This implementation is by no means shorter than the other one, however it is now clear that the Set of visited nodes is used as state. If the program was much longer and more complicated, not having to pass the state around as an argument would significantly improve the code's readability.

## Conclusion

We tried to solve a simple programming problem using the help of Monads and we did it. However the resulting code is not more elegant than the original one and so we did not manage to showcase the greatness of the `State` Monad. In the next part of the series I hope that I can find a problem whose solution is greatly improved when using Monads.

Here is a [link](https://github.com/angelhof/codewars-solutions/blob/master/graphExistsPath/main.hs) for the complete code in this post.
