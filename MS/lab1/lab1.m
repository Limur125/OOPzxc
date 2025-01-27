% Вариант 13

X = [-10.82,-9.27,-9.65,-9.36,-9.27,-11.25,-9.89,-9.26,-11.15,-8.90,-11.02,-8.28,-9.18,-10.16,-10.59,-10.82,-9.05,-9.47,-10.98,-11.50,-8.64,-10.86,-10.76,-11.49,-11.09,-9.33,-9.32,-9.66,-8.79,-10.54,-9.12,-10.40,-8.59,-10.22,-9.06,-10.59,-10.60,-10.25,-9.35,-11.44,-9.81,-9.32,-9.95,-9.33,-10.64,-9.45,-10.99,-10.15,-10.39,-10.36,-10.49,-11.67,-10.00,-10.87,-11.11,-9.68,-10.77,-9.13,-8.62,-10.33,-11.36,-10.24,-9.41,-11.05,-10.15,-9.35,-11.45,-9.87,-10.41,-10.11,-10.84,-11.48,-7.77,-10.79,-9.88,-10.70,-9.07,-9.47,-10.15,-9.93,-11.52,-9.04,-10.93,-10.13,-9.56,-11.39,-9.79,-9.19,-11.09,-9.86,-10.67,-10.26,-9.07,-10.53,-11.24,-10.16,-11.33,-8.76,-8.88,-10.53,-10.12,-8.98,-9.84,-9.90,-10.13,-9.32,-9.31,-9.99,-8.55,-11.64,-11.32,-10.51,-11.71,-10.50,-10.50,-12.20,-11.68,-10.45,-7.88,-10.84];
n = length(X);

% a
X_max = max(X);
X_min = min(X);
fprintf("max = %f\n", X_max)
fprintf("min = %f\n", X_min)

% б
R = X_max - X_min;
fprintf("R = %f\n", R)

% в
MX = mean(X);
DX = var(X);
fprintf("MX = %f   DX = %f\n", MX, DX)

% г
m = floor(log2(n)) + 2;
delta = R / m;
fprintf('m = %i  delta = %f\n', m, delta);

% д
h = histogram(X, m);

sigma = sqrt(DX);
x = (X_min - 1):(sigma / 100):(X_max + 1);
% Функция плотности вероятности нормального распределения.
f = normpdf(x, MX, sigma);

figure;
delta = h.BinWidth;
heights = h.Values / (n * delta); % Массив значений эмпирической плотности.
centers = [];
for i = 1:m
    centers = [centers, (h.BinEdges(i + 1) + h.BinEdges(i)) / 2];
end
hold on; % Чтобы было два графика на одном полотне.
% Принимает центры и высоту столбцов.
% Рисует гистограмму (график эмпирической плотности).
bar(centers, heights, 1); 
plot(x, f, 'LineWidth', 2);

% е 
% Функция расределения нормальной СВ 
F = normcdf(x, MX, sigma); % x~N(MX,sigma)
figure;
hold on;
% Эмпиричиеская ф-ия распределения
ecdf(X);
plot(x, F, 'r');