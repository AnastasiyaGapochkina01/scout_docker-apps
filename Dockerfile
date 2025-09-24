# Stage 1: Build React app
FROM node:18 AS builder
WORKDIR /app

# Устанавливаем зависимости отдельно, чтобы кешировалось
COPY package.json ./
RUN npm install

# Копируем исходники и билдим
COPY . .
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

