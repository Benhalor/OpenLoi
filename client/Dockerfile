FROM node:18-alpine
WORKDIR /client
RUN apk add --no-cache git
COPY . .
RUN yarn install
RUN yarn upgrade
EXPOSE 8080
CMD ["yarn", "start"]
