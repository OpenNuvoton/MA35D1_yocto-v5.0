SUMMARY = "OP-TEE Trusted OS"
DESCRIPTION = "Open Portable Trusted Execution Environment - Trusted side of the TEE"
HOMEPAGE = "https://www.op-tee.org/"

LICENSE = "BSD-2-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=c1f21c4f72f372ef38a5a4aee55ec173"

inherit deploy python3native
require optee.inc

CVE_PRODUCT = "linaro:op-tee op-tee:op-tee_os"

DEPENDS = "python3-pyelftools-native python3-cryptography-native"

DEPENDS:append:toolchain-clang = " compiler-rt"

OPTEEMACHINE ?= "${MACHINE}"
OPTEEOUTPUTMACHINE ?= "${MACHINE}"

SRC_URI = "git://github.com/OpenNuvoton/optee_os_ma35.git;protocol=https;branch=master"

PV = "4.2.0+git${SRCPV}"
S = "${WORKDIR}/git"
B = "${WORKDIR}/build"

EXTRA_OEMAKE += " \
    CFG_${OPTEE_CORE}_core=y \
    CROSS_COMPILE_core=${HOST_PREFIX} \
    CROSS_COMPILE_ta_${OPTEE_ARCH}=${HOST_PREFIX} \
    NOWERROR=1 \
    ta-targets=ta_${OPTEE_ARCH} \
    O=${B} \
"
EXTRA_OEMAKE += " HOST_PREFIX=${HOST_PREFIX}"
EXTRA_OEMAKE += " CROSS_COMPILE64=${HOST_PREFIX}"

LDFLAGS[unexport] = "1"
CPPFLAGS[unexport] = "1"
AS[unexport] = "1"
LD[unexport] = "1"

export PLATFORM = "${OPTEE_PLATFORM}"
export PLATFORM_FLAVOR = "${OPTEE_PLATFORM_FLAVOR}"

do_compile:prepend() {
	PLAT_LIBGCC_PATH=$(${CC} -print-libgcc-file-name)
}

do_compile() {
	if echo ${TFA_DTB} | grep -q "128"; then
            oe_runmake CFG_TZDRAM_START=0x87900000 CFG_SHMEM_START=0x87800000 -C ${S} O=${B}
	elif echo ${TFA_DTB} | grep -q "512"; then
            oe_runmake CFG_TZDRAM_START=0x9F900000 CFG_SHMEM_START=0x9F800000 -C ${S} O=${B}
	elif echo ${TFA_DTB} | grep -q "1g"; then
            oe_runmake CFG_TZDRAM_START=0xBF900000 CFG_SHMEM_START=0xBF800000 -C ${S} O=${B}
	elif echo ${TFA_DTB} | grep -q "2g"; then
            oe_runmake CFG_TZDRAM_START=0xEF900000 CFG_SHMEM_START=0xEF800000 -C ${S} O=${B}
	else
            oe_runmake -C ${S} O=${B}
	fi
}
do_compile[cleandirs] = "${B}"

do_install() {
    #install core in firmware
    install -d ${D}${nonarch_base_libdir}/firmware/
    install -m 644 ${B}/core/*.bin ${B}/core/tee.elf ${D}${nonarch_base_libdir}/firmware/

    #install tas in optee_armtz
    install -d ${D}${nonarch_base_libdir}/optee_armtz/
    install -m 444 ${B}/ta/*/*.ta ${D}${nonarch_base_libdir}/optee_armtz
}

PACKAGE_ARCH = "${MACHINE_ARCH}"

do_deploy() {
    install -d ${DEPLOYDIR}/${MLPREFIX}optee
    install -m 644 ${D}${nonarch_base_libdir}/firmware/* ${DEPLOYDIR}/${MLPREFIX}optee

    install -d ${DEPLOYDIR}/${MLPREFIX}optee/ta
    install -m 644 ${B}/ta/*/*.elf ${DEPLOYDIR}/${MLPREFIX}optee/ta
}

addtask deploy before do_build after do_install

SYSROOT_DIRS += "${nonarch_base_libdir}/firmware"

PACKAGES += "${PN}-ta"
FILES:${PN} = "${nonarch_base_libdir}/firmware/"
FILES:${PN}-ta = "${nonarch_base_libdir}/optee_armtz/*"


# note: "textrel" is not triggered on all archs
INSANE_SKIP:${PN} = "textrel"
# Build paths are currently embedded
INSANE_SKIP:${PN} += "buildpaths"
INSANE_SKIP:${PN}-dev = "staticdev"
INHIBIT_PACKAGE_STRIP = "1"

