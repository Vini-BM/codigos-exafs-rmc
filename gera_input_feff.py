# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 13:06:11 2023

@author: vinib
"""
#%% Imports
import numpy as np
import os
#%% Cabeçalho feff
main = 'C:\\Users\\Vinicius\\OneDrive\\Documentos\\Faculdade\\IC\\Teste_feff_evax'
os.chdir(main)
cab = 'cabecalho_feff.txt'
cab_lines = list(open(cab, 'r'))
filename = 'output_lammps\\dump.523'
outfile = 'output_lammps\\dump.523.inp'
lines = list(open(filename,'r'))
f = open(outfile, 'w')
for line in cab_lines:
    f.write(line + '\n')
#%% Posição absoluta dos átomos
NATOMS = int(lines[3].strip(''))
f.write('\n ATOMS *this list contains {} atoms \n'.format(str(NATOMS)))
f.write('* x   y   z   ipot   tag   distance \n')
x_lo, x_hi = float(lines[5].strip('').split( )[0]), float(lines[5].strip('').split( )[1]) 
y_lo, y_hi = float(lines[6].strip('').split( )[0]), float(lines[6].strip('').split( )[1]) 
z_lo, z_hi = float(lines[7].strip('').split( )[0]), float(lines[7].strip('').split( )[1])
dx = x_hi - x_lo
dy = y_hi - y_lo
dz = z_hi - z_lo
#%% Átomos
positions = []
ge_count = 0 # Para a composição Ge_x Si_(1-x)
for line in range(9, 9+NATOMS):
    at_type, xx, yy, zz = int(lines[line].strip('').split( )[1]), float(lines[line].strip('').split( )[2]), float(lines[line].strip('').split( )[3]), float(lines[line].strip('').split( )[4])
    x = (xx - x_lo) * dx
    y = (yy - y_lo) * dy
    z = (zz - z_lo) * dz
    if at_type == 1:
        tag = 'Ge'
        ge_count += 1
    elif at_type == 2:
        tag = 'Si'
    positions.append([x, y, z, at_type, tag])
xc, yc, zc = positions[0][0:3] # Posição do átomo central
for i in range(0, len(positions)):
    xi, yi, zi = positions[i][0:3]
    # Átomo central como (0,0,0):
    positions[i][0] = xi - xc
    positions[i][1] = yi - yc
    positions[i][2] = zi - zc
    dist = np.linalg.norm((positions[i][0], positions[i][1], positions[i][2]))
    positions[i].append(dist) # Adicionar distância à lista
#%% Escrever no arquivo
for line in positions:
    for text in line:
        f.write(str(text) + ' ') # Escreve x, y, z, ipot, tag, distance
        # Índice de coordenação não é escrito (ex: Ge.1, Ge.2)
    f.write('\n')
f.write('\n')
f.write('END')
f.close()
#%% Composição Ge_x Si_(1-x)
prop_ge = ge_count/NATOMS
print(prop_ge)
