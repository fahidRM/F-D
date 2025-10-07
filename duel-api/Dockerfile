# Stage 1: Build the Go binary
FROM golang:1.25 as builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod tidy
COPY . .
RUN GOOS=linux GOARCH=amd64 go build -o main .

# Stage 2: Create the final minimal image
FROM alpine:latest
WORKDIR /duel/
RUN apk update && apk add ca-certificates
COPY --from=builder /app/main .
COPY --from=builder /app/public ./public
RUN chmod +x ./main
EXPOSE 3030
CMD ["./main"]