clear
x = importdata('lat-rate.txt');
y = importdata('long-rate.txt');
z = importdata('rate.txt');
latmax = max(max(x))
latmin = min(min(x))
lonmax = max(max(y))
lonmin = min(min(y))

x1 = 200*(x-latmin)/(latmax-latmin)
y1 = 200-200*(y-lonmin)/(lonmax-lonmin)
%x1 = 111111.1111*(x-latmin);   %γ�Ⱦ���
%y1 = 111111.1111*cos((latmax+latmin)/2)*(y-lonmin);  %���Ⱦ���
%x2 = 111130*(latmax-latmin)   %γ��������
%y2 = 111111.1111*cos((latmax+latmin)/2)*(lonmax-lonmin)  %����������
%x3 = 40030173*(latmax-latmin)/360   %γ��������
%y3 = 40030173*cos((latmax+latmin)/2)*(lonmax-lonmin)/360 %����������
[X,Y] = meshgrid(x1,y1)
Z = griddata(x1,y1,z,X,Y,'v4')
surf(X,Y,Z)  % surf for creating surface plot
shading interp
colorbar
view(-90,90);