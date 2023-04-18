did_not_stole(X, money) :- does_not_love(X, money).

does_not_love(alice, money).

has(herman, money).

hate(X, herman) :- works(X, herman).

knew_where_was(carol, money).
knew_where_was(X, money) :- stole(X, money).

love(X, money) :- stole(X, money).
love(bob, money).

object(money).
object(safe).

opened(herman, safe).
opened(X, Y) :- person(X), object(Y), object(Z), stole(X, Z), was_inside(Z, Y).

person(alice).
person(bob).
person(carol).
person(david).
person(herman).

stole(X, money) :- hate(X, herman).
stole(X, Z) :- person(X), person(Z), object(Y), has(Z, Y), stole(X, Y).

was_inside(money, safe).

works(david, herman).
