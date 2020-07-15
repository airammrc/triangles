import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from utils import draw_triangle, reflection, halfplane2disk

def get_chain(ini_tri, W, geometry='hyperbolic', model = 'halfplane', draw=True, axes=None, **kargs):

    word = W.replace(' ', '').replace('(', '').replace(')', '')

    label = {'a': 0, 'b': 1, 'c': 2}

    tri = ini_tri[:]
    chain_v = [{'a': tri[0], 'b': tri[1], 'c': tri[2]}]

    if draw:
        if axes == None:
            ax = plt.gca()
        else: 
            ax = axes
        ax.axis('off')
        ax.set_aspect('equal')

        edges, face = draw_triangle(ax, ini_tri, geometry=geometry, model=model, **kargs)
        chain_e = [edges]
        chain_f = [face]

    for i in range(len(word)):
        x = label[word[i]]
        a = (x+1)%3
        b = (x-1)%3
        tri[x] = reflection(tri[x], tri[a], tri[b], geometry=geometry)
        chain_v.append({'a': tri[0], 'b': tri[1], 'c': tri[2]})
        if draw:
            e, face = draw_triangle(ax, [tri[a], tri[b], tri[x]], all_edges=False, geometry=geometry, model=model, **kargs)
            edges = [None]*3
            edges[a] = e['a']
            edges[b] = e['b']
            edges[x] = chain_e[-1][word[i]]
            chain_e.append({'a': edges[0], 'b': edges[1], 'c':edges[2]})
            chain_f.append(face)

    if geometry == 'hyperbolic' and model == 'disk':
        chain_v = [dict([(v, halfplane2disk(*t[v])) for v in t]) for t in chain_v]

    if draw:
        if geometry == 'hyperbolic' and model == 'disk':
            ax.add_patch(Circle((0., 0.), radius=1., fill=False, lw = 1, color='black'))

        ax.autoscale()

        if geometry == 'hyperbolic' and model == 'halfplane':
            ax.set_ylim(bottom=0.)

        return chain_v, chain_e, chain_f
    else:
        return chain_v
