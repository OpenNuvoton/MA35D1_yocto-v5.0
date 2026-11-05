FILESEXTRAPATHS:prepend := "${THISDIR}/6.18.y:"

PATCHTOOL = "git"

SRC_URI += "file://0001-net-stmmac-add-Nuvoton-platform-support.patch \
            file://0002-rpmsg-char-fix-TOCTOU-race-in-rpmsg_eptdev_poll.patch \
            "
