#coding=utf-8
from __future__ import unicode_literals, print_function, division
from visual import window, cylinder, ring, random, sphere, mag, sleep, rate, mag2, dot, norm, cross, exit
from visual.graph import display, vector, color, gdisplay, gcurve, ghistogram, arange
from math import sqrt, pi, cos, sin, exp, asin
from wx import StaticText

import config

def Simulation():

    Atoms = []  # spheres
    p = []      # momentums (vectors)
    apos = []   # positions (vectors)
    ampl = 0 #амплитуда движения
    period = 5
    k = 1.4E-23 # Boltzmann constant
    R = 8.3
    dt = 1E-5
    time = 0
    
    def checkCollisions():
        hitlist = []
        r2 = 2 * config.Ratom
        for i in range(config.Natoms):
            for j in range(i):
                dr = apos[i] - apos[j]
                if dr.mag < r2:
                    hitlist.append([i, j])
        return hitlist
    piston_mode = config.piston_mode
    period = config.period
    ampl = config.ampl
    def speed(time):
        if (piston_mode == 0):
            return 0
        if (piston_mode == 1):
            return ampl/10*3*sin(time / period * 2 * pi) * sqrt(3 * 4E-3 / 6E23 * k * 300) / (5 * 4E-3 / 6E23)/period * 100
        if (piston_mode == 2):
            if (time % period < period // 2):
                return ampl/10*1.5*sqrt(3 * 4E-3 / 6E23 * k * 300) / (5 * 4E-3 / 6E23)/period * 100
            else:
                return -1.5*ampl/10*sqrt(3 * 4E-3 / 6E23 * k * 300) / (5 * 4E-3 / 6E23)/period * 100
        if (piston_mode == 3):
            if (time % period < period // 5):
                return 5*ampl/10*sqrt(3 * 4E-3 / 6E23 * k * 300) / (5 * 4E-3 / 6E23)/period * 100
            else:
                return -5/4*ampl/10*sqrt(3 * 4E-3 / 6E23 * k * 300) / (5 * 4E-3 / 6E23)/period * 100
        if (piston_mode == 4):
            if (time % period < 4* period // 5):
                return 5/4*ampl/10*sqrt(3 * 4E-3 / 6E23 * k * 300) / (5 * 4E-3 / 6E23)/period * 100
            else:
                return -5*ampl/10*sqrt(3 * 4E-3 / 6E23 * k * 300) / (5 * 4E-3 / 6E23)/period * 100
            
    width, height = config.w.win.GetSize()
    
    offset = config.w.dheight
    deltav = 100 # histogram bar width
    
    config.disp = display(window = config.w, x = offset, y = offset, forward = vector(0,-0.3,-1),
                range = 1.5,
                width = width / 3, height = height)

    config.g1 = gdisplay(window = config.w, x = width / 3 + 2 * offset, y = offset,
                background = color.white,
                foreground = color.black,
                width = width / 3, height = height / 2 - 2 * offset)
    
    speed_text = StaticText(config.w.panel, pos = (width / 3 + 2 * offset, height / 2 - offset), label = "Средняя скорость")
    graph_text = StaticText(config.w.panel, pos = (width / 3 + 2 * offset, height - 2 * offset), label = "")

    if config.piston_mode == 0:
        config.g2 = gdisplay(window = config.w, x = width / 3 + 2 * offset, y = height / 2,
                    background = color.white,
                    foreground = color.black,
                    width = width / 3, height = height / 2 - 2 * offset,
                    xmax = 3000, ymax = config.Natoms * deltav / 1000)
        graph_text.SetLabel("Распределение скоростей частиц")
    else:
        config.g2 = gdisplay(window = config.w, x = width / 3 + 2 * offset, y = height / 2,
                    background = color.white,
                    foreground = color.black,
                    width = width / 3, height = height / 2 - 2 * offset)
        graph_text.SetLabel("Температура")
    
    L = 1 # container is a cube L on a side
    gray = color.gray(0.7) # color of edges of container
    d = L / 2 + config.Ratom # half of cylinder's height
    topborder = d

    cylindertop = cylinder(pos = (0, d, 0), axis = (0, -d / 50, 0), radius = d)
    ringtop = ring(pos = (0, d, 0), axis = (0, -d, 0), radius = d,
                thickness = 0.005)
    ringbottom = ring(pos = (0, -d, 0), axis = (0, -d, 0), radius = d,
                thickness = 0.005)
    body = cylinder(pos = (0, -d, 0), axis = (0, 2 * d, 0), radius = d,
                opacity = 0.2)

    pavg = sqrt(3 * config.mass * k * config.T)  # average kinetic energy p**2/(2config.mass) = (3/2)kT

    graph_average_speed = gcurve(gdisplay = config.g1, color=color.black)

    if config.piston_mode:
        graph_temp = gcurve(gdisplay = config.g2, color=color.black)
    else:
        theory_speed = gcurve(gdisplay = config.g2, color = color.black)
        dv = 10
        for v in range(0, 3001 + dv, dv):
            theory_speed.plot(pos=(v, (deltav / dv) * config.Natoms *
                        4 * pi * ((config.mass / (2 * pi * k * config.T)) ** 1.5) *
                        exp(-0.5 * config.mass * (v ** 2) / (k * config.T)) * (v ** 2) * dv))

        hist_speed = ghistogram(gdisplay = config.g2, bins = arange(0, 3000, 100),
                    color = color.red, accumulate = True, average = True)

        speed_data = [] # histogram data
        for i in range(config.Natoms):
            speed_data.append(pavg / config.mass)

    # uniform particle distribution
    for i in range(config.Natoms):
        qq = 2 * pi * random.random()

        x = sqrt(random.random()) * L * cos(qq) / 2
        y = L * random.random() - L / 2
        z = sqrt(random.random()) * L * sin(qq) / 2

        if i == 0:
            # particle with a trace
            Atoms.append(sphere(pos = vector(x, y, z), radius = config.Ratom,
                        color = color.cyan, make_trail = True, retain = 100,
                        trail_radius = 0.3 * config.Ratom))
        else:
            Atoms.append(sphere(pos = vector(x, y, z), radius = config.Ratom,
                        color = gray))

        apos.append(vector(x, y, z))
        

        theta = pi * random.random()
        phi = 2 * pi * random.random()

        px = pavg * sin(theta) * cos(phi)
        py = pavg * sin(theta) * sin(phi)
        pz = pavg * cos(theta)

        p.append(vector(px, py, pz))

    while config.start:

        while config.pause:
            sleep(0.1)
        
        rate(100)
        
        sp = speed(time)
        cylindertop.pos.y -= sp * dt
        time += 1
        
        for i in range(config.Natoms):
            Atoms[i].pos = apos[i] = apos[i] + (p[i] / config.mass) * dt
            if config.piston_mode == 0:
                speed_data[i] = mag(p[i]) / config.mass

        total_momentum = 0
        v_sum = 0
        for i in range(config.Natoms):
            total_momentum += mag2(p[i])
            v_sum += sqrt(mag2(p[i])) / config.mass

        graph_average_speed.plot(pos = (time, v_sum / config.Natoms))
        if config.piston_mode:
            graph_temp.plot(pos = (time, total_momentum / (3 * k * config.mass) / config.Natoms))
        else:
            hist_speed.plot(data = speed_data)

        hitlist = checkCollisions()

        for ij in hitlist:
            
            i = ij[0]
            j = ij[1]
            ptot = p[i] + p[j]
            posi = apos[i]
            posj = apos[j]
            vi = p[i] / config.mass
            vj = p[j] / config.mass
            vrel = vj - vi
            a = vrel.mag2
            if a == 0: # exactly same velocities
                continue
            rrel = posi - posj
            if rrel.mag > config.Ratom: # one atom went all the way through another
                continue

            # theta is the angle between vrel and rrel:
            dx = dot(rrel, norm(vrel))  # rrel.mag*cos(theta)
            dy = cross(rrel, norm(vrel)).mag  # rrel.mag*sin(theta)
            # alpha is the angle of the triangle composed of rrel, path of atom j, and a line
            #   from the center of atom i to the center of atom j where atome j hits atom i:
            alpha = asin(dy / (2 * config.Ratom))
            d = (2 * config.Ratom) * cos(alpha) - dx  # distance traveled into the atom from first contact
            deltat = d / vrel.mag  # time spent moving from first contact to position inside atom

            posi = posi - vi * deltat  # back up to contact configuration
            posj = posj - vj * deltat
            mtot = 2 * config.mass
            pcmi = p[i] - ptot * config.mass / mtot  # transform momenta to cm frame
            pcmj = p[j] - ptot * config.mass / mtot
            rrel = norm(rrel)
            pcmi = pcmi - 2 * pcmi.dot(rrel) * rrel  # bounce in cm frame
            pcmj = pcmj - 2 * pcmj.dot(rrel) * rrel
            p[i] = pcmi + ptot * config.mass / mtot  # transform momenta back to lab frame
            p[j] = pcmj + ptot * config.mass / mtot
            apos[i] = posi + (p[i] / config.mass) * deltat  # move forward deltat in time
            apos[j] = posj + (p[j] / config.mass) * deltat

        # collisions with walls
        for i in range(config.Natoms):

            # проекция радиус-вектора на плоскость
            loc = vector(apos[i])
            loc.y = 0

            # вылет за боковую стенку (цилиндр радиуса L / 2 + config.Ratom)
            if (mag(loc) > L / 2):

                # проекция импульса на плоскость
                proj_p = vector(p[i])
                proj_p.y = 0

                loc = norm(loc)
                # скалярное произведение нормированного радиус-вектора на импульс (все в проекции на плоскость)
                dotlp = dot(loc, proj_p) 

                if dotlp > 0:
                    p[i] -= 2 * dotlp * loc
                # dotlp < 0 - атом улетает от стенки
                # dotlp = 0 - атом летит вдоль стенки
            
            loc = apos[i]

            # вылет за торцы
            if loc.y < - L / 2:
                p[i].y = abs(p[i].y)

            if loc.y > cylindertop.pos.y - config.Ratom:
                v_otn = p[i].y / config.mass + sp
                if v_otn > 0:
                    p[i].y = (- v_otn - sp) * config.mass

    config.disp.delete()
    config.g1.display.delete()
    config.g2.display.delete()

    graph_text.Destroy()
    speed_text.Destroy()
