# Yocto Build for Nuvoton Boards
## Supported Boards:
* ``` MA35D1 (numaker-som-ma35d16a81) ```
* ``` MA35H0 (numaker-hmi-ma35h04f70) ```
* ``` MA35D0 (numaker-iot-ma35d03f80) ```
#### NOTE: There are multiple board models available for reference. For example, in the case of MA35D1, you can refer to source/meta-ma35d1/conf/machine/* for configurations.
# Downloading Source and Building Process:
## 1. For MA35D1 (numaker-som-ma35d16a81):
### 1.1. Initialize Yocto repository:
```console
repo init -u https://github.com/OpenNuvoton/MA35D1_yocto-v5.0.git -m meta-ma35d1/base/ma35d1.xml
```
```console
repo sync
```
### 1.2. Set up the environment and build:
```console
DISTRO=nvt-ma35d1-directfb MACHINE=numaker-som-ma35d16a81 source sources/init-build-env build
```
#### NOTE: Modify the device tree of arm-trusted-firmware and the kernel as per the board in source/meta-ma35d1/conf/machine/*.conf.
### 1.3. Execute bitbake to build core-image-minimal:
```console
bitbake core-image-minimal
```
## 2. For MA35H0 (numaker-hmi-ma35h04f70):
### 2.1. Initialize Yocto repository:
```console
repo init -u https://github.com/OpenNuvoton/MA35D1_yocto-v5.0.git -m meta-ma35h0/base/ma35h0.xml
```
```console
repo sync
```
### 2.2. Set up the environment and build:
```console
DISTRO=nvt-ma35h0-directfb MACHINE=numaker-hmi-ma35h04f70 source sources/init-build-env build
```
#### NOTE: Same modification note as in section 1.2.
### 2.3. Execute bitbake to build core-image-minimal:
```console
bitbake core-image-minimal
```
## 3. For MA35D0 (numaker-iot-ma35d03f80):
### 3.1. Initialize Yocto repository:
```console
repo init -u https://github.com/OpenNuvoton/MA35D1_yocto-v5.0.git -m meta-ma35d0/base/ma35d0.xml
```
```console
repo sync
```
### 3.2. Set up the environment and build:
```console
DISTRO=nvt-ma35d0 MACHINE=numaker-som-ma35d16a81 source sources/init-build-env build
```
#### NOTE: Same modification note as in section 1.2.
### 3.3. Execute bitbake to build core-image-minimal:
```console
bitbake core-image-minimal
```
