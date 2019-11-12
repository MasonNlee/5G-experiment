clear
x = importdata('lat.txt')
y = importdata('long.txt')
z = importdata('csq.txt')
[X,Y]=meshgrid(x,y)
Z = griddata(x,y,z,X,Y,'v4')
surf(X,Y,Z)
shading interp
colorbar