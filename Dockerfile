FROM ubuntu:latest
LABEL authors="gosha"

ENTRYPOINT ["top", "-b"]