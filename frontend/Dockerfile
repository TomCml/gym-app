# --- STAGE 1: Build ---
FROM node:22-alpine AS builder
WORKDIR /frontend
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# --- STAGE 2: Production ---
FROM nginx:alpine
COPY --from=builder /frontend/dist /usr/share/nginx/html
COPY ../nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80