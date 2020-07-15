# coding: utf-8

import matplotlib.pyplot as plt

from triangles.utils  import get_mobius_triangle
from triangles.tessellations import generate_tessellation, draw_tessellation

triangle_type = (2, 3, 7) #%* Tipo de teselación triangular.*)
model = 'disk'            #%* Modelo del espacio hiperbólico utilizado para*)
                          #%* representar la teselación.*)

#%* Se genera la teselación.*)
tes = generate_tessellation(triangle_type, model)

#%* Se dibuja la teselación con los colores rojo y azul y diferentes grados de transparencia.*)
draw_tessellation(tes, color=('red', 'blue'), alpha=(1., 0.5))

plt.title('Disco')
plt.savefig('ejemplo3_disk.png')

#%* Aunque la teselación ha sido generada para el modelo de disco, también puede ser representada en el modelo de semiplano ejecutando los siguientes comandos.*)
tes.model = 'halfplane'
tes.depth = [-1., 1., 0.01, 2.] #%* Ajusta la región que se representa.*)
draw_tessellation(tes, color=('black', 'white'), alpha=(1., 1.))

plt.title('Semiplano')
plt.savefig('ejemplo3_halfplane.png')
