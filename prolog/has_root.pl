has_root(N) :- has_root(N, 1).
has_root(N, R) :- is(P, *(R, R)),
                  (
                      =(N, P);
                      >(N, P),
                      is(Rn, +(R, 1)),
                      has_root(N, Rn)
                  ).
