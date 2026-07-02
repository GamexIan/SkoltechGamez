lambda0 = 533e-9;        
n0 = 1.5;                
k0 = 2*pi / lambda0;     
k = n0 * k0;             
w0 = 70e-6;              
P = 80e-3;               
I0 = (2*P) / (pi * w0^2); 
L_medio = 1e-3;          
fase = -3;               
n2 = -fase * 2*pi / (k0 * I0 * L_medio); 
s = 0;                   
sigma_nl = 25e-6;      
zray = (pi * w0^2) / lambda0;     
xvalor= -1.3;
z_position =xvalor*zray;        
d = 10*zray;              


if z_position == 0
    w_z = w0;
    R_z = Inf;
    guoy_phase = 0;
else
    w_z = w0 * sqrt(1 + (z_position/zray)^2);
    R_z = z_position * (1 + (zray/z_position)^2);
    guoy_phase = atan(z_position/zray);
end

Lx = 90*w_z;        
Ly = Lx;                 
N = 900;           
%dz = 1e-3;               
%Nz = round(L_medio / dz); 
Nz = 500;               
dz = L_medio / Nz;       


dx = Lx / N;
dy = Ly / N;
x = (-Lx/2:dx:Lx/2-dx);
y = (-Ly/2:dy:Ly/2-dy);
[X, Y] = meshgrid(x, y);
r = sqrt(X.^2 + Y.^2);


if z_position == 0
    A = sqrt(I0) * exp(-r.^2 / w0^2);
else
    A = sqrt(I0) * (w0/w_z) .* exp(-r.^2 / w_z^2) .* ...
        exp(-1i * k0 * r.^2 / (2 * R_z)) .* exp(-1i * guoy_phase);
end

I_in = abs(A).^2;


kx = 2*pi * [0:N/2-1, -N/2:-1] / Lx;
ky = 2*pi * [0:N/2-1, -N/2:-1] / Ly;
[KX, KY] = meshgrid(kx, ky);
K2 = KX.^2 + KY.^2;


linear_prop_exact = exp(1i * dz * (K2 ./ (sqrt(k^2 - K2) + k)));


linear_prop_exact(K2 >= k^2) = 0;


if s ~= 0
    R1 = exp(-(X.^2 + Y.^2) / (2 * sigma_nl^2));
    R = R1 / (sum(R1(:)) * dx * dy);
else
    R = 0;
end

fprintf('Iniciando propagación...\n');
fprintf('Parámetros: w0 = %.1f μm, L_medio = %.1f mm, n2 = %.2e m²/W\n', ...
        w0*1e6, L_medio*1e3, n2);

A_out = A; 

for iz = 1:Nz
    if mod(iz, round(Nz/10)) == 0
        fprintf('Progreso: %.0f%%\n', 100*iz/Nz);
    end
    
  
    I = abs(A).^2;
    
  
    if s ~= 0
        nonlocal_term = s * conv2(I, R, 'same') * dx * dy;
    else
        nonlocal_term = 0;
    end
    
    delta_n = n2 * I + nonlocal_term;
    A = A .* exp(1i * k0 * delta_n * dz/2);
    
   
    A_fft = fft2(A);
    A_fft = A_fft .* linear_prop_exact; 
    A = ifft2(A_fft);
    

    I = abs(A).^2;
    
    if s ~= 0
        nonlocal_term = s * conv2(I, R, 'same') * dx * dy;
    else
        nonlocal_term = 0;
    end
    
    delta_n = n2 * I + nonlocal_term;
    A = A .* exp(1i * k0 * delta_n * dz/2);
    
   
    if iz == Nz
        A_out = A;
    end
end

I_out = abs(A_out).^2;


A_far = fftshift(fft2(ifftshift(A_out)));
I_far = abs(A_far).^2;


kx_fft = 2*pi * (-N/2:N/2-1) / Lx;  
ky_fft = 2*pi * (-N/2:N/2-1) / Ly;
u = (d * lambda0) * kx_fft / (2*pi);
v = (d * lambda0) * ky_fft / (2*pi);
u_mm = u * 1000;
v_mm = v * 1000;
[U_mm, V_mm] = meshgrid(u_mm, v_mm);



figure('Name', 'Haz Gaussiano a la Entrada', 'Position', [100 100 1200 500]);

subplot(1,2,1);
imagesc(x*1e6, y*1e6, I_in);
xlabel('x (\mum)'); ylabel('y (\mum)');
title('Intensidad a la Entrada (2D)');
axis square; colorbar; colormap('hot');
set(gca, 'FontSize', 12);

subplot(1,2,2);
profile_x = I_in(N/2+1, :);
plot(x*1e6, profile_x/max(profile_x), 'LineWidth', 2);
xlabel('x (\mum)'); ylabel('Intensidad Normalizada');
title('Perfil de Intensidad a la Entrada');
grid on;
set(gca, 'FontSize', 12);

figure('Name', 'Haz a la Salida del Medio', 'Position', [100 100 1200 500]);

subplot(1,2,1);
imagesc(x*1e6, y*1e6, I_out);
xlabel('x (\mum)'); ylabel('y (\mum)');
title('Intensidad a la Salida del Medio (2D)');
axis square; colorbar; colormap('hot');
set(gca, 'FontSize', 12);

subplot(1,2,2);
profile_x_out = I_out(N/2+1, :);
plot(x*1e6, profile_x_out/max(profile_x_out), 'LineWidth', 2);
xlabel('x (\mum)'); ylabel('Intensidad Normalizada');
title('Perfil de Intensidad a la Salida');
grid on;
set(gca, 'FontSize', 12);




nombreFigura = string(xvalor) + "zraycl" + string(fase);
figure('Name', nombreFigura, 'Position', [100 100 1200 500]);



subplot(1,2,1);
pcolor(U_mm, V_mm, I_far);
shading interp;         
axis square;
axis off;
%xlabel('x [mm]'); ylabel('y [mm]');
%title(sprintf('Patrón de Difracción (d = %.2f m)', d));
%colorbar;
colormap('hot');
set(gca, 'FontSize', 12);

subplot(1,2,2);
profile_x_far = I_far(N/2+1, :);
plot(u_mm, profile_x_far/max(profile_x_far), 'LineWidth', 2);
xlabel('p/mm'); ylabel('Intensidad Normalizada');
%title('Perfil de Intensidad en Campo Lejano');
%grid on;
set(gca, 'FontSize', 12);


nombreFigura2 = string(xvalor) + "zraycp" + string(fase);
figure('Name', nombreFigura2, 'Position', [100 100 1000 600]);
plot(x*1e6, profile_x/max(profile_x), 'LineWidth', 2, 'DisplayName', 'Entrada');
hold on;
plot(x*1e6, profile_x_out/max(profile_x_out), 'LineWidth', 2, 'DisplayName', 'Salida Medio');
xlabel('Posición (\mum)'); ylabel('Intensidad Normalizada');
%title('Comparación de Perfiles de Intensidad');
legend('show');
grid on;
set(gca, 'FontSize', 12);



