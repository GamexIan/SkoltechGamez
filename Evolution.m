lambda0 = 533e-9;       
n0 = 1.5;                % index
k0 = 2*pi / lambda0;     
k = n0 * k0;             
w0 = 70e-6;              % Waist
P = 80e-3;               
I0 = (2*P) / (pi * w0^2); 
L_medio = 5e-2 ;    
fase = 0.15 ;               
n2 = -fase * 2*pi / (k0 * I0 * L_medio); 
s = 0;                   
sigma_nl = 25e-6;        % NO LOCAL RESONSE
zray = (pi * w0^2) / lambda0; 

xvalor = 0;
z_position = xvalor * zray;        
d = 75e-2;              

if z_position == 0
    w_z = w0;
    R_z = Inf;
    guoy_phase = 0;
else
    w_z = w0 * sqrt(1 + (z_position/zray)^2);
    R_z = z_position * (1 + (zray/z_position)^2);
    guoy_phase = atan(z_position/zray);
end

Lx = 10*w_z;        
Ly = Lx;                 
N = 900;           
Nz = 400;               
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


z_positions = (1:Nz) * dz;  % Z
I_evolution = zeros(N, Nz);  

A_current = A;

for iz = 1:Nz
    if mod(iz, round(Nz/10)) == 0
        fprintf('Progreso: %.0f%%\n', 100*iz/Nz);
    end
    
    
    I = abs(A_current).^2;
    
    if s ~= 0
        nonlocal_term = s * conv2(I, R, 'same') * dx * dy;
    else
        nonlocal_term = 0;
    end
    
    delta_n = n2 * I + nonlocal_term;
    A_current = A_current .* exp(1i * k0 * delta_n * dz/2);
    
    
    A_fft = fft2(A_current);
    A_fft = A_fft .* linear_prop_exact; 
    A_current = ifft2(A_fft);
    
    
    I = abs(A_current).^2;
    
    if s ~= 0
        nonlocal_term = s * conv2(I, R, 'same') * dx * dy;
    else
        nonlocal_term = 0;
    end
    
    delta_n = n2 * I + nonlocal_term;
    A_current = A_current .* exp(1i * k0 * delta_n * dz/2);
    
    
    I_evolution(:, iz) = I(N/2+1, :);
end

I_out = abs(A_current).^2;


figure('Position', [100, 100, 1400, 1000]);

% UPPer view
subplot(2,2,[1,2]); 
z_mm = z_positions * 1000;  
x_mm = x * 1000;           

h = imagesc(z_mm, x_mm, I_evolution);
xlabel('Z position(mm)', 'FontSize', 14, 'FontWeight', 'bold');
ylabel('X position (mm)', 'FontSize', 14, 'FontWeight', 'bold');
title('Evolution', ...
      'FontSize', 16, 'FontWeight', 'bold');
%colorbar;
%c = colorbar;
%c.Label.String = 'Intensidad (W/m²)';
%c.Label.FontSize = 12;
axis xy;  % Asegurar que el eje y esté en la dirección correcta
colormap('hot');
grid off;
set(gca, 'FontSize', 12, 'GridAlpha', 0.3);

%{
subplot(2,2,3);
plot(x_mm, I_evolution(:, 1)/max(I_evolution(:, 1)), 'b-', 'LineWidth', 3, 'DisplayName', 'Entrada (z=0)');
hold on;
plot(x_mm, I_evolution(:, end)/max(I_evolution(:, end)), 'r-', 'LineWidth', 3, 'DisplayName', 'Salida (z=L)');
xlabel('Posición x (mm)', 'FontSize', 12);
ylabel('Intensidad Normalizada', 'FontSize', 12);
title('Comparación Entrada/Salida', 'FontSize', 14, 'FontWeight', 'bold');
legend('show', 'FontSize', 11);
grid on;
set(gca, 'FontSize', 11);
%}

%{ 
subplot(2,2,4);
plot(x_mm, I_evolution(:, end), 'k-', 'LineWidth', 3);
xlabel('Posición x (mm)', 'FontSize', 12);
ylabel('Intensidad (W/m²)', 'FontSize', 12);
title('Perfil de Intensidad a la Salida (z=L)', 'FontSize', 14, 'FontWeight', 'bold');
grid on;
set(gca, 'FontSize', 11);
%}


figure('Position', [100, 50, 1000, 400]);
A_far = fftshift(fft2(ifftshift(A_current)));
I_far = abs(A_far).^2;

kx_fft = 2*pi * (-N/2:N/2-1) / Lx;  
ky_fft = 2*pi * (-N/2:N/2-1) / Ly;
u = (d * lambda0) * kx_fft / (2*pi);
v = (d * lambda0) * ky_fft / (2*pi);
u_mm = u * 1000;
v_mm = v * 1000;
[U_mm, V_mm] = meshgrid(u_mm, v_mm);

subplot(1,2,1);
pcolor(U_mm, V_mm, I_far);
shading interp;         
axis square;
axis off;
xlabel('x (mm)', 'FontSize', 12); 
ylabel('y (mm)', 'FontSize', 12);
title('Patrón de Difracción - Campo Lejano', 'FontSize', 14, 'FontWeight', 'bold');
colorbar;
colormap('hot');

subplot(1,2,2);
profile_x_far = I_far(N/2+1, :);
plot(u_mm, profile_x_far/max(profile_x_far), 'LineWidth', 2);
xlabel('x (mm)', 'FontSize', 12); 
ylabel('Intensidad Normalizada', 'FontSize', 12);
title('Far Fiel', 'FontSize', 14, 'FontWeight', 'bold');
grid on;

fprintf('\nAnálisis completado:\n');
fprintf('- Longitud del medio: %.3f mm\n', L_medio*1000);
fprintf('- Número de pasos de propagación: %d\n', Nz);
fprintf('- Tamaño de paso dz: %.2f μm\n', dz*1e6);
fprintf('- Intensidad máxima inicial: %.2e W/m²\n', max(I_in(:)));
fprintf('- Intensidad máxima final: %.2e W/m²\n', max(I_out(:)));