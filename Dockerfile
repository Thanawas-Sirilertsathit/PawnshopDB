# Stage 1: Node.js for Tailwind and npm dependencies
FROM node:16-alpine as node-stage

# Set working directory
WORKDIR /app/theme/static_src

# Copy only the Tailwind package files
COPY theme/static_src/package.json theme/static_src/package-lock.json ./

# Install npm dependencies
RUN npm install --legacy-peer-deps

# Build Tailwind CSS
COPY theme/static_src .
RUN npm run build


# Stage 2: Python for Django application
FROM python:3-alpine as python-stage

# Set working directory
WORKDIR /app/pawnshop

# Install system dependencies and Node.js (required for Tailwind)
RUN apk add --no-cache \
    build-base \
    python3 \
    python3-dev \
    mariadb-dev \
    bash \
    curl \
    nodejs \
    npm \
    pkgconfig

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy Tailwind assets from the Node.js stage
COPY --from=node-stage /app/theme/static_src /app/theme/static_src

# Add NPM_BIN_PATH to settings.py
ENV NPM_BIN_PATH="/usr/bin/npm"

# Run Django setup commands
RUN python manage.py tailwind install
RUN python manage.py tailwind build
RUN python manage.py collectstatic --noinput

# Expose the application port
EXPOSE 8000
CMD ["sh", "-c", "python /app/pawnshop/manage.py migrate --noinput && python /app/pawnshop/manage.py runserver 0.0.0.0:8000"]
