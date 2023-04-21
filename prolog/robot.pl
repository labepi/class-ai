adjacent(a1, a2). adjacent(a1, b1).
adjacent(a2, a1). adjacent(a2, a3). adjacent(a2, b2).
adjacent(a3, a2). adjacent(a3, a4). adjacent(a3, b3).
adjacent(a4, a3). adjacent(a4, a5). adjacent(a4, b4).
adjacent(a5, a4). adjacent(a5, b5).

adjacent(b1, a1). adjacent(b1, b2). adjacent(b1, c1).
adjacent(b2, b1). adjacent(b2, a2). adjacent(b2, b3). adjacent(b2, c2).
adjacent(b3, b2). adjacent(b3, a3). adjacent(b3, b4). adjacent(b3, c3).
adjacent(b4, b3). adjacent(b4, a4). adjacent(b4, b5). adjacent(b4, c4).
adjacent(b5, b4). adjacent(b5, a5). adjacent(b5, c5).

adjacent(c1, b1). adjacent(c1, c2). adjacent(c1, d1).
adjacent(c2, c1). adjacent(c2, b2). adjacent(c2, c3). adjacent(c2, d2).
adjacent(c3, c2). adjacent(c3, b3). adjacent(c3, c4). adjacent(c3, d3).
adjacent(c4, c3). adjacent(c4, b4). adjacent(c4, c5). adjacent(c4, d4).
adjacent(c5, c4). adjacent(c5, b5). adjacent(c5, d5).

adjacent(d1, c1). adjacent(d1, d2). adjacent(d1, e1).
adjacent(d2, d1). adjacent(d2, c2). adjacent(d2, d3). adjacent(d2, e2).
adjacent(d3, d2). adjacent(d3, c3). adjacent(d3, d4). adjacent(d3, e3).
adjacent(d4, d3). adjacent(d4, c4). adjacent(d4, d5). adjacent(d4, e4).
adjacent(d5, d4). adjacent(d5, c5). adjacent(d5, e5).

adjacent(e1, d1). adjacent(e1, e2).
adjacent(e2, e1). adjacent(e2, d2). adjacent(e2, e3).
adjacent(e3, e2). adjacent(e3, d3). adjacent(e3, e4).
adjacent(e4, e3). adjacent(e4, d4). adjacent(e4, e5).
adjacent(e5, e4). adjacent(e5, d5).

path(X, Y) :- path(X, Y, P), print(P).

path(X, Y, P) :- path(X, Y, F, [X]), append([X], F, P), !.

path(X, Y, P, V) :- adjacent(X, Y),
                    append([Y], [], P);
                    adjacent(X, Z),
                    not(member(Z, V)),
                    append([Z], V, W),
                    path(Z, Y, F, W),
                    append([Z], F, P).
