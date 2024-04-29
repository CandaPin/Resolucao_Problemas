param n;
param cv;
param cp;
param np;
param r;

suffix master IN, binary;
suffix block IN, integer;

set I = 1..n ordered;
set K = 1..r ordered;
param w {I,K} >= 0;
param v {I,K} >= 0;
param inner{I,K} >= 0;
param d {I,K} >= 0;
param maxVal := max {i in I, k in K} w[i,k];
param soma := sum{i in I, k in K} d[i, k];
param maxbins := ceil(soma / floor(cp / maxVal));

set J = 1..maxbins ordered;

var e {I,J,K} integer >= 0;
var y {J,K} binary;

minimize FO:  sum {j in J, k in K} y[j,k];

s.t. R1_capacidade_mochila_peso {j in J, k in K}:
   sum {i in I} w[i,k] * e[i,j,k] * inner[i,k] <= cp * y[j,k];

s.t. R2_capacidade_mochila_volume {j in J, k in K}:
   sum {i in I} v[i,k] * e[i,j,k] * inner[i,k] <= cv * y[j,k];

s.t. R3_capacidade_mochila_pecas {j in J, k in K}:
   sum {i in I} e[i,j,k] * inner[i,k] <= np * y[j,k];

s.t. R4_quantidade_demanda {i in I, k in K}:
   sum {j in J} e[i,j,k]* inner[i,k] = d[i,k];
