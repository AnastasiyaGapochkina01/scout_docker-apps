FROM golang:1.21-alpine
RUN apk add --no-cache curl bash
RUN mkdir /app
WORKDIR /app
COPY main.go /app/
RUN go mod init example.com/metricsapp || true
RUN go mod tidy || true
RUN go build -o metricsapp main.go
COPY start.sh /app/
RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]
