did_not_stole(X, money) :- does_not_love(X, money).

does_not_love(alice, money).

hate(X, herman) :- works(X, herman).

knew_where_was(carol, money).
knew_where_was(X, money) :- stole(X, money).

love(bob, money).
love(X, money) :- stole(X, money).

stole(X, money) :- hate(X, herman).

works(david, herman).
