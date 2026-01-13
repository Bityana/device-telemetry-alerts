FROM node:20-alpine

WORKDIR /web
COPY web/package.json /web/package.json
COPY web/tsconfig.json /web/tsconfig.json
COPY web/vite.config.ts /web/vite.config.ts
COPY web/index.html /web/index.html
COPY web/src /web/src

RUN npm install

EXPOSE 5173
CMD ["npm", "run", "dev"]
