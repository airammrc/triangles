import numpy as np

from matplotlib.lines import Line2D
from matplotlib.patches import Polygon

def get_hyperline_halfplane(p1, p2, angles=False):

    if abs(p1[0]-p2[0]) > 1e10*np.finfo(float).eps:
        c = (np.dot(p1,p1)-np.dot(p2,p2))/(p1[0]-p2[0])/2.
        r = p1-np.array([c, 0.])
        r = np.sqrt(np.dot(r,r))
    else:
        r = np.inf
        c = p1[0]

    if angles:
        if r ==np.inf:
            theta1 = p1[1]
            theta2 = p2[1]
        else:
            theta1 = np.arccos((p1[0]-c)/r)
            theta2 = np.arccos((p2[0]-c)/r)

        return np.array([c, 0.]), r, theta1, theta2
    else:
        return np.array([c, 0.]), r

def get_hyperline_disk(p1, p2, angles=False):

    if abs(p1[1]-p2[1]) > 1e10*np.finfo(float).eps:

        d = (p1[1]*p2[0]-p1[0]*p2[1])

        if abs(d) > 1e10*np.finfo(float).eps:
            x = (p1[1]*(1.+np.dot(p2, p2))-p2[1]*(1.+np.dot(p1, p1)))/d/2.
            y = -(p1[0]-p2[0])/(p1[1]-p2[1])*(x-(p1[0]+p2[0])/2.)+(p1[1]+p2[1])/2.
            r = np.sqrt(x**2.+y**2-1.)
        else:
            if abs(p1[0]) > 1e10*np.finfo(float).eps:
                m = p1[1]/p1[0]
                x, y = np.array([1., m])/np.sqrt(1.+m**2.)
                r = np.inf
            else:
                x, y = 0., 1.
                r = np.inf
    else:

        if abs(p1[1]) > 1e10*np.finfo(float).eps:
            x = (p1[0]+p2[0])/2.
            y = (1.-p1[0]*p2[0]+p1[1]**2.)/p1[1]/2.
            r = np.sqrt(x**2.+y**2-1.)
        else:
            x, y = 1., 0.
            r = np.inf

    if angles:
        if r == np.inf:
            theta1 = p1[0]*x+p1[1]*y
            theta2 = p2[0]*x+p2[1]*y
        else:
            theta1 = np.arctan2(p1[1]-y, p1[0]-x)
            theta2 = np.arctan2(p2[1]-y, p2[0]-x)

        return np.array([x, y]), r, theta1, theta2
    else:
        return np.array([x, y]), r

def get_hyperline(p1, p2, angles=False, model='halfplane'):
    if model == 'halfplane':
        return get_hyperline_halfplane(p1, p2, angles=angles)
    if model == 'disk':
        return get_hyperline_disk(p1, p2, angles=angles)

def halfplane2disk(x, y):

    r2 = x**2.+y**2.

    d = x**2.+(y+1.)**2.

    u = (r2-1.)/d
    v = -2.*x/d

    return np.array([u, v])

def get_edge(p1, p2, geometry='hyperbolic', model='halfplane', **kargs):

    if geometry == 'hyperbolic':
        if model == 'halfplane':
            q1, q2 = p1.copy(), p2.copy()
        if model == 'disk':
            q1, q2 = halfplane2disk(*p1), halfplane2disk(*p2)
        c, r, th1, th2 = get_hyperline(q1, q2, angles=True, model=model)

        if r == np.inf:
            x, y = np.array([q1[0], q2[0]]), np.array([q1[1], q2[1]])
        else:
            w = abs(th1-th2)
            if w >= np.pi:
                w = 2.*np.pi-w
                s = -np.sign(th2-th1)
            else:
                s = np.sign(th2-th1)
            th = th1+s*np.linspace(0., w, int(w*r/0.001))
            x, y = c[0]+r*np.cos(th), c[1]+r*np.sin(th)

    if geometry == 'euclidean':
        x, y = np.array([p1[0], p2[0]]), np.array([p1[1], p2[1]])

    edge = Line2D(x, y, **kargs)

    return edge

def draw_triangle(ax, vertices, edges=True, all_edges=True, geometry='hyperbolic', model='halfplane', **kargs):

    keywords_edge = {'edgestyle': ('linestyle', 'solid'), 'edgecolor': ('color', 'black'), 'edgewidth': ('linewidth', 2.)}
    kargs_edge = []
    for k in keywords_edge.keys():
        try:
            kargs_edge.append((keywords_edge[k][0], kargs[k]))
        except KeyError:
            kargs_edge.append(keywords_edge[k])
    kargs_edge = dict(kargs_edge)

    keywords_face = {'fill': ('fill', True), 'facecolor': ('color', 'darkgrey'), 'alpha': ('alpha', 1.)}
    kargs_face = []
    for k in keywords_face.keys():
        try:
            kargs_face.append((keywords_face[k][0], kargs[k]))
        except KeyError:
            kargs_face.append(keywords_face[k])
    kargs_face = dict(kargs_face)

    bx, by = [], []

    sides = [None]*3

    for i in range(3):
        edge = get_edge(vertices[i], vertices[(i+1)%3], geometry=geometry, model=model, **kargs_edge)
        sides[(i-1)%3] = edge
        x, y = edge.get_data()
        bx, by = np.append(bx, x[:-1]), np.append(by, y[:-1])
    
    face = Polygon(np.array([bx, by]).T, lw=0, **kargs_face)
    ax.add_patch(face)

    if edges:
        for i in range(2+all_edges):
            ax.add_line(sides[i])
        return {'a': sides[0], 'b': sides[1], 'c': sides[2]}, face
    else:
        return face

def reflection(x, a, b, geometry='hyperbolic'):

    if geometry == 'hyperbolic':
        c, r = get_hyperline(a, b)
        if r == np.inf:
            z = np.copy(x)
            z[0] = 2.*c[0]-z[0]
        else:
            z = x-c
            z = z*r**2./np.dot(z,z)+c

    if geometry == 'euclidean':
        r = b-a
        r2 = np.dot(r,r)
        xp = np.dot(x-a,r)/r2*r
        z = 2.*(xp+a)-x

    return z

def get_mobius_triangle(n1, n2, n3):

    if (n1*n2+n2*n3+n3*n1)/(n1*n2*n3) >= 1 or np.any(np.array([n1, n2 ,n3]) < 2):
        print 'Invalid hiperbolic triangle'
        return None

    th1 = np.pi/float(n1)
    th2 = np.pi/float(n2)
    th3 = np.pi/float(n3)

    if n1 == 2:
        c1 = 0.
        r1 = 1.
    else:
        c1 = 1./np.tan(th1)
        r1 = 1./np.sin(th1)

    if n2 == 2:
        c2 = 0.
        r2 = 1.
    else:
        c2 = 1./np.tan(th2)
        r2 = 1./np.sin(th2)

    cth3 = np.cos(th3)

    b = r1*r2*cth3+c1*c2

    y2 = b+np.sqrt(b**2.-1.)
    x3 = (y2**2.-1.)/(c1+c2*y2)/2.
    y3 = np.sqrt(r1**2.-(x3-c1)**2.)

    return [np.array([0., 1.]), np.array([0., y2]), np.array([x3, y3])]
