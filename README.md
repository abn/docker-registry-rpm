# Docker Registry (v2): RPM Packaging

RPM packaging for [docker registry (v2)](https://github.com/docker/distribution). This package is built and hosted using [Travis CI](https://travis-ci.com) and [Fedora Copr](https://copr.fedorainfracloud.org/) as described in the [RPM Build Flow](https://gist.github.com/abn/daf262e7e454509df1429c87068923d1).

You can use this package by enabling the copr repository at [abn/docker-registry](https://copr.fedorainfracloud.org/coprs/abn/docker-registry/) as described [here](https://gist.github.com/abn/daf262e7e454509df1429c87068923d1#using-packages-in-copr-repository).

## Basic usage
Once installed, `docker-registry` can be used as follows.

```sh
# simple Usage
/usr/bin/docker-registry serve /etc/docker-registry.yml

# systemd start
systemctl start docker-registry

# enable on boot
systmectl enable docker-registry
```
