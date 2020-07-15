# coding: utf-8

import matplotlib.pyplot as plt

from triangles.utils  import get_mobius_triangle
from triangles.chains import get_chain

triangle_type = (2, 3, 7)
W = 'ab'

ini_tri = get_mobius_triangle(*triangle_type)

v, e, f = get_chain(ini_tri, W) #%* Se genera la cadena y se guardan los vértices,*)
                                #%* lados y caras.*)

e[0]['a'].set_ls('dashed') #%* Se cambia el estilo del lado 'a' del primer triángulo.*)
f[1].set_fc('red')         #%* Se cambia el color de la cara del segundo triángulo.*)
plt.scatter(*v[2]['b'], s=100, color='blue') #%* Se pinta un punto azul sobre el*)
                                             #%* vértice 'B' del tercer triángulo.*)

plt.savefig('ejemplo2.pdf')
plt.show()
