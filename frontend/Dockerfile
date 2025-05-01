# Stage 1: build
FROM node:18-alpine AS builder
WORKDIR /app

# Copiamos deps y caché de instalación
COPY package.json package-lock.json ./
RUN npm ci

# Copiamos código y generamos el build de Vite
COPY . .
RUN npm run build

# Stage 2: servidor estático con Nginx
FROM nginx:stable-alpine
# Copiamos el build al directorio de HTML de Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Opcional: si quieres un config custom de Nginx,
# crea nginx.conf junto al Dockerfile y descomenta la línea:
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
