FROM python:3-alpine

# Set working directory
WORKDIR /app/pawnshop

# Set environment variables
ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=True
ENV TIMEZONE=${TIMEZONE}
ENV ALLOWED_HOSTS=${ALLOWED_HOSTS:-127.0.0.1,localhost}
ENV PATH_TO_NPM=${PATH_TO_NPM}

# Copy requirements file
COPY ./requirements.txt .

# Install system dependencies and Node.js
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

ENV NPM_BIN_PATH=/usr/bin/npm

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Install DaisyUI and Tailwind via npm
WORKDIR /app/theme/static_src
COPY theme/static_src/package.json theme/static_src/package-lock.json ./theme/static_src/
# Install Node.js dependencies (DaisyUI, Tailwind, etc.)
RUN npm install --legacy-peer-deps

# Build Tailwind and DaisyUI assets (This will create your final CSS file)
RUN npm run build  # Assumes you have a build script in package.json
COPY . /app/

# Setup Django
WORKDIR /app/
RUN python manage.py tailwind install
RUN python manage.py tailwind build
RUN python manage.py collectstatic --noinput
RUN chmod +x /app/entrypoint.sh
# Expose the application port
EXPOSE 8000

# Command to run the application
CMD [ "./entrypoint.sh" ]
