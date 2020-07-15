import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Circle

from triangles.utils import draw_triangle, get_mobius_triangle, reflection, halfplane2disk

class vertex:

    def __init__(self, xy, type):
        self.xy = xy
        self.type = type
        self.index = 1
        self.alive = True

class triangle:

    def __init__(self, vertices, parity):
        self.vertices = vertices
        self.parity = parity

class tessellation:

    def __init__(self, triangles, model, depth):
        self.triangles = triangles
        self.model = model
        self.depth = depth

def draw_tessellation(tes, color=('blue', 'blue'), alpha=(0.8, 0.2), axes=None):

    if axes == None:
        ax = plt.gca()
    else: 
        ax = axes
    ax.axis('off')
    ax.set_aspect('equal')

    for t in tes.triangles:
        tri = [v.xy for v in t.vertices]
        draw_triangle(ax, tri, model=tes.model, edges=False, facecolor=color[t.parity], alpha=alpha[t.parity])

    if tes.model == 'halfplane':
        ax.set_xlim(tes.depth[0], tes.depth[1])
        ax.set_ylim(tes.depth[2], tes.depth[3])
    if tes.model == 'disk':
        ax.add_patch(Circle((0., 0.), radius=1., fill=False, lw = 1, color='black'))
        ax.autoscale()

def generate_tessellation(type, model='halfplane', depth=None):

    if depth == None:
        if model == 'halfplane':
            depth = [-2., 2., 0.01, 2.]
        if model == 'disk':
            depth = 0.99

    abc = ['a', 'b', 'c']

    index = dict([(abc[i], 2*type[i]) for i in range(3)])

    ini_tri = get_mobius_triangle(*type)
    ini_tri = [vertex(ini_tri[i], abc[i]) for i in range(3)]
    ini_tri = triangle(ini_tri, False)

    tes = [ini_tri]

    bound = ini_tri.vertices[:]
    intv = bound[:]
    intv.append(intv.pop(0))

    node = bound[-1]
    ndead = 0
    parity = False

    while ndead < len(bound)-1:
        node.index += 1
        parity = not parity

        if node.index == index[node.type]:

            bound[-2].xy = reflection(intv[0].xy, node.xy, bound[0].xy)
            new_tri = [bound[-2], node, bound[0]]
            par = parity

            bound[-2].index += 1
            bound.pop(-1)
            intv.pop(0)
            intv[-1] = node

            node = bound.pop(0)
            node.index += 1
            bound.append(node)

            while node.index == index[node.type]:
                if not bound.pop(-1).alive:
                    ndead -=1
                node = bound.pop(0)
                bound[-1].xy = node.xy
                parity = bool((parity+1+bound[-1].index)%2)
                node.index += bound.pop(-1).index
                bound.append(node)
                intv.pop(0)
                intv.pop(-1)

            while not node.alive:
                parity = bool((parity+1+node.index)%2)
                node = bound.pop(0)
                bound.append(node)
                intv.append(intv.pop(0))

        else:
            x = vertex(reflection(intv[-1].xy, node.xy, bound[-2].xy), intv[-1].type)

            if model == 'halfplane':
                kill = x.xy[0] < depth[0] or x.xy[0] > depth[1] or x.xy[1] < depth[2] or x.xy[1] > depth[3]
            if model == 'disk':
                p = halfplane2disk(*x.xy)
                kill = np.sqrt(np.dot(p, p)) > depth
            if kill:
                x.alive = False
                ndead += 1

            new_tri = [bound[-2], x, node]
            par = parity

            intv.pop(-1)
            intv.append(node)
            intv.append(bound[-2])

            bound[-2].index += 1

            bound.pop(-1)
            bound.append(x)
            bound.append(node)

        tes.append(triangle(new_tri, par))

    while node.index != index[node.type]:
        node.index += 1
        parity = not parity

        x = vertex(reflection(intv[-1].xy, node.xy, bound[-2].xy), intv[-1].type)

        if model == 'halfplane':
            kill = x.xy[0] < depth[0] or x.xy[0] > depth[1] or x.xy[1] < depth[2] or x.xy[1] > depth[3]
        if model == 'disk':
            p = halfplane2disk(*x.xy)
            kill = np.sqrt(np.dot(p, p)) > depth
        if kill:
            x.alive = False
            ndead += 1

        new_tri = [bound[-2], x, node]
        par = parity

        intv.pop(-1)
        intv.append(node)
        intv.append(bound[-2])

        bound[-2].index += 1

        bound.pop(-1)
        bound.append(x)
        bound.append(node)

        tes.append(triangle(new_tri, par))

    return tessellation(tes, model, depth)
