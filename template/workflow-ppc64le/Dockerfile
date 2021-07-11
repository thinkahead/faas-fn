FROM --platform=${BUILDPLATFORM:-linux/ppc64le} golang:1.10-alpine3.8 as builder

ARG TARGETPLATFORM
ARG BUILDPLATFORM
ARG TARGETOS
ARG TARGETARCH

WORKDIR /go/src/handler
COPY . .

# Run a gofmt and exclude all vendored code.
RUN test -z "$(gofmt -l $(find . -type f -name '*.go' -not -path "./vendor/*" -not -path "./function/vendor/*"))" || { echo "Run \"gofmt -s -w\" on your Golang code"; exit 1; }

RUN GOOS=${TARGETOS:-linux} GOARCH=${TARGETARCH:-ppc64le} CGO_ENABLED=0 GOOS=linux \
    go build --ldflags "-s -w" -a -installsuffix cgo -o handler . && \
    go test $(go list ./... | grep -v /vendor/) -cover

FROM --platform=${TARGETPLATFORM:-linux/ppc64le} alpine:3.9
RUN apk --no-cache add ca-certificates
COPY ofwatchdog-ppc64le /usr/bin/fwatchdog

# Add non root user
RUN addgroup -S app && adduser -S -g app app
RUN mkdir -p /home/app
WORKDIR /home/app

COPY --from=builder /go/src/handler/           .
RUN chown -R app /home/app
RUN chmod -R 777 /home/app/function
USER app

ENV fprocess="./handler"

CMD ["/usr/bin/fwatchdog"]
