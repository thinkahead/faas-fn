#FROM ghcr.io/openfaas/classic-watchdog:0.1.5 as watchdog

FROM alpine:3.12

RUN apk update && apk upgrade && apk add curl tar make gcc build-base wget gnupg

RUN mkdir -p /usr/src/perl

WORKDIR /usr/src/perl

## from perl; `true make test_harness` because 3 tests fail
## some flags from http://git.alpinelinux.org/cgit/aports/tree/main/perl/APKBUILD?id=19b23f225d6e4f25330e13144c7bf6c01e624656
RUN curl -SLO https://www.cpan.org/src/5.0/perl-5.32.0.tar.gz \
    && echo 'ddecb3117c016418b19ed3a8827e4b521b47d6bb *perl-5.32.0.tar.gz' | sha1sum -c - \
    && tar --strip-components=1 -xzf perl-5.32.0.tar.gz -C /usr/src/perl \
    && rm perl-5.32.0.tar.gz \
    && ./Configure -des \
        -Duse64bitall \
        -Dcccdlflags='-fPIC' \
        -Dcccdlflags='-fPIC' \
        -Dccdlflags='-rdynamic' \
        -Dlocincpth=' ' \
        -Duselargefiles \
        -Dusethreads \
        -Duseshrplib \
        -Dd_semctl_semun \
        -Dusenm \
    && make libperl.so \
    && make -j$(nproc) \
    && TEST_JOBS=$(nproc) make test_harness \
    && make install \
    && curl -LO https://raw.githubusercontent.com/miyagawa/cpanminus/master/cpanm \
    && chmod +x cpanm \
    && ./cpanm App::cpanminus \
    && rm -fr ./cpanm /root/.cpanm /usr/src/perl

## from tianon/perl
ENV PERL_CPANM_OPT --verbose --mirror https://cpan.metacpan.org --mirror-only
RUN cpanm Digest::SHA Module::Signature && rm -rf ~/.cpanm
ENV PERL_CPANM_OPT $PERL_CPANM_OPT --verify

RUN mkdir -p /home/app

COPY fwatchdog-ppc64le /usr/bin/fwatchdog
#COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

# Add non root user
RUN addgroup -S app && adduser app -S -G app
RUN chown app /home/app
WORKDIR /home/app

USER app

# Populate example here - i.e. "cat", "sha512sum" or "node index.js"
COPY runme.pl /home/app/runme.pl
ENV fprocess="/home/app/runme.pl"
#ENV fprocess="cat"
#ENV fprocess='perl -Mbignum=bpi -wle print(bpi(100))'
#'foreach my $line ( <STDIN> ) { chomp($line);if ($line=~/^$/) { last; } print(bpi($line)); }'
#"foreach my \$line ( <STDIN> ) { chomp(\$line);if (\$line=~/^\$/) { last; } print(bpi(\$line)); }"
# Set to true to see request in function logs
ENV write_debug="true"

EXPOSE 8080

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
