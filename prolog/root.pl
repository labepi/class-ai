root(N) :- root(N, 1).
root(N, R) :- is(P, *(R, R)),
              (
                  =(N, P), print(R), !;
                  >(N, P),
                  is(Rn, +(R, 1)),
                  root(N, Rn)
              ).
