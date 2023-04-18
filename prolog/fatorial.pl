factorial(0, 1).
factorial(N, R) :- >(N, 0),
                   is(N1, -(N, 1)),
                   factorial(N1, R1),
                   is(R, *(N, R1)).
