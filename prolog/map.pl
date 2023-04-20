adjacent(serranegra, saojoao).
adjacent(serranegra, caico).
adjacent(serranegra, timbauba).
adjacent(serranegra, jardimpiranhas).

adjacent(jardimpiranhas, timbauba).
adjacent(jardimpiranhas, saofernando).
adjacent(jardimpiranhas, jucurutu).
adjacent(jardimpiranhas, serranegra).

adjacent(jucurutu, jardimpiranhas).
adjacent(jucurutu, saofernando).
adjacent(jucurutu, caico).
adjacent(jucurutu, florania).
adjacent(jucurutu, santanamatos).

adjacent(timbauba, serranegra).
adjacent(timbauba, jardimpiranhas).
adjacent(timbauba, saofernando).
adjacent(timbauba, caico).

adjacent(saofernando, timbauba).
adjacent(saofernando, jardimpiranhas).
adjacent(saofernando, jucurutu).
adjacent(saofernando, caico).

adjacent(saojoao, ipueira).
adjacent(saojoao, serranegra).
adjacent(saojoao, caico).

path(X, Y, P) :- path(X, Y, F, [X]), append([X], F, P).

path(X, Y, P, V) :- adjacent(X, Y),
                    append([Y], [], P);
                    adjacent(X, Z),
                    not(member(Z, V)),
                    append([Z], V, W),
                    path(Z, Y, F, W),
                    append([Z], F, P).
