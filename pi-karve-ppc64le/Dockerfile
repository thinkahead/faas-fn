#FROM ghcr.io/openfaas/classic-watchdog:0.1.5 as watchdog
FROM docker.io/powerlinux/classic-watchdog:latest-dev-ppc64le as watchdog

FROM alpine:3.12

RUN apk update && apk upgrade && apk add curl tar make gcc build-base wget gnupg perl

RUN mkdir -p /home/app

#COPY fwatchdog-ppc64le /usr/bin/fwatchdog
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

# Add non root user
RUN addgroup -S app && adduser app -S -G app
RUN chown app /home/app

WORKDIR /home/app

USER app

# Populate example here - i.e. "cat", "sha512sum" or "node index.js"
#ENV fprocess="cat"
ENV fprocess='perl -Mbignum=bpi -wle print(bpi(100))'
# Set to true to see request in function logs
ENV write_debug="false"

EXPOSE 8080

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
