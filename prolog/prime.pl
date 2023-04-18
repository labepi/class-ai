prime(X) :- is(Y, -(X, 1)), prime(X, Y).
prime(X, Y) :- =(Y, 1);
               >(X, 2),
               >(mod(X, Y), 0),
               is(Z, -(Y, 1)),
               prime(X, Z).
