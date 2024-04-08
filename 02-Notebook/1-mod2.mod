
# Parâmetros
param np; # numero de produtos
param nm; # numero de maquinas
set P = 1..np; # conjunto de produtos
set M = 1..nm; # conjunto de maquinas
param preco{P}; # preco de venda dos produtos
param custo{M}; # custo/hora das maquinas
param disp{M}; # disponibilidade das maquinas
param tempo{M,P}; # tempo gasto pelo produto j na maquina i

#Variáveis de decisão
var x{P} integer >= 0; # quantidade de produtos a produzir
var venda = sum{j in P} preco[j]*x[j];
var gasto = sum{i in M} custo[i]*(sum{j in P} tempo[i,j]*x[j])/60;

#Função-objetivo
maximize L: venda - gasto;
s.t. R1 {i in M}: sum{j in P} (tempo[i,j]*x[j])/60 <= disp[i];
