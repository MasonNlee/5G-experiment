clear
x = importdata('lat.txt');
y = importdata('long.txt');
z = importdata('csq.txt');
latmax = max(max(x))
latmin = min(min(x))
lonmax = max(max(y))
lonmin = min(min(y))

x1 = 200*(x-latmin)/(latmax-latmin)
y1 = 200-200*(y-lonmin)/(lonmax-lonmin)
%x1 = 111111.1111*(x-latmin);   %纬度距离
%y1 = 111111.1111*cos((latmax+latmin)/2)*(y-lonmin);  %经度距离
%x2 = 111130*(latmax-latmin)   %纬度最大距离
%y2 = 111111.1111*cos((latmax+latmin)/2)*(lonmax-lonmin)  %经度最大距离
%x3 = 40030173*(latmax-latmin)/360   %纬度最大距离
%y3 = 40030173*cos((latmax+latmin)/2)*(lonmax-lonmin)/360 %经度最大距离

[X,Y] = meshgrid(x1,y1)
Z = griddata(x1,y1,z,X,Y,'v4')
surf(X,Y,Z)
shading interp
colorbar
view(-90,90);