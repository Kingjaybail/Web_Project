# Frontend Dockerfile (React)
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy frontend code
COPY . .

# Expose React dev server port
EXPOSE 5173

# Run the React development server
CMD ["npm", "run", "dev", "--", "--host"]
