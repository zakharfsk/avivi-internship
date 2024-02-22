#!/bin/bash

autossh -M 0 \
    -oServerAliveInterval=30 \
    -oServerAliveCountMax=3 \
    -oStrictHostKeyChecking=no \
    -oUserKnownHostsFile=/dev/null \
    -oExitOnForwardFailure=yes \
    -R avivi-internship:80:nginx:80 \
    serveo.net