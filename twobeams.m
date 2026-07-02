
nx = 1024;
ny = nx;
xm = 1;
ym = xm;
lz = 1;
dz = 0.03;
nz = round(lz/dz);
ww = 1;



x = linspace(-xm, xm, nx+1); x = x(1:nx);
dx = x(2) - x(1);
y = linspace(-ym, ym, ny+1); y = y(1:ny);
dy = y(2) - y(1);
[x, y] = meshgrid(x, y);
[phi, r] = cart2pol(x, y);

xif=0.5;

x_shift = -xif; 
x_beam1 = linspace(-xm + x_shift, xm + x_shift, nx + 1);
x_beam1 = x_beam1(1:nx);
dx_beam1 = x_beam1(2) - x_beam1(1);
y_beam1 = linspace(-ym, ym, ny + 1);
y_beam1 = y_beam1(1:ny);
dy_beam1 = y_beam1(2) - y_beam1(1);
[x_beam1, y_beam1] = meshgrid(x_beam1, y_beam1);
[phi_beam1, r_beam1] = cart2pol(x_beam1, y_beam1);
U1 = besselj(0, 2.6.*7.35.*r_beam1);

x_shift = xif;
x_beam2 = linspace(-xm + x_shift, xm + x_shift, nx + 1);
x_beam2 = x_beam2(1:nx);
dx_beam2 = x_beam2(2) - x_beam2(1);
y_beam2 = linspace(-ym, ym, ny + 1);
y_beam2 = y_beam2(1:ny);
dy_beam2 = y_beam2(2) - y_beam2(1);
[x_beam2, y_beam2] = meshgrid(x_beam2, y_beam2);
[phi_beam2, r_beam2] = cart2pol(x_beam2, y_beam2);
U2 = besselj(0, 2.6.*7.35.*r_beam2);
fx = (-nx/2:nx/2-1)*2*pi/(2*xm);
fy = (-ny/2:ny/2-1)*2*pi/(2*ym);
[fx, fy] = meshgrid(fx, fy);
tf = fftshift(exp(-1i*dz*sqrt(fx.^2 + fy.^2)/4));


Ux1 = zeros(nx, nz+1);
Ux2 = zeros(nx, nz+1);
for ii = 1:nz
    U1 = ifft2(tf .* fft2(U1));
    U2 = ifft2(tf .* fft2(U2));
    Ux1(:, ii+1) = U1(:, nx/2);
    Ux2(:, ii+1) = U2(:, nx/2);
    imagesc(abs(U1).^2 + abs(U2).^2); axis square; colorbar;
    drawnow;
end

figure(1);
mesh(x, y, abs(U1).^2 + abs(U2).^2);
shading flat;


figure(2);
waterfall(x(1,1:nx), (0:nz)*dz, ((abs(Ux1)').^2 + (abs(Ux2)').^2));
axis([-ym ym 0 lz 0 2]);
colormap([0 0 0]);

figure(3);
plot(x(1,:)./2, abs(Ux1(:, 1)).^2, x(1,:)./2, abs(Ux2(:, 1)).^2, 'r');
hold on;
plot(x(1,:)./2, abs(Ux1(:, end)).^2, (x(1,:)./2), abs(Ux2(:, end)).^2, 'b');
hold off;
legend('Haz inicial 1', 'Haz inicial 2', 'Haz final 1', 'Haz final 2');
title('Perfil de intensidades');