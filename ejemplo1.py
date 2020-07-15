# coding: utf-8

import matplotlib.pyplot as plt

from triangles.utils  import get_mobius_triangle
from triangles.chains import get_chain

triangle_type = (2, 3, 7) #%* Tipo de triángulo de Mobius que se toma como triángulo*)
                          #%* inicial de la cadena.*)

W = 'abcabababcac'        #%* Palabra que genera la cadena.*)

ini_tri = get_mobius_triangle(*triangle_type) #%* Triángulo inicial.*)

get_chain(ini_tri, W) #%* Generar la cadena.*)

plt.savefig('ejemplo1.pdf')
plt.show()

