# The base qt5-env.sh is shared between nvt-ma35d1-directfb and every
# GC520 2D stack distro. For those distros, QT_QPA_PLATFORM must
# be etnaviv2d. The unconditional XDG_RUNTIME_DIR export must be
# dropped, since pam_systemd already sets it correctly under them.
do_install:append() {
    if ${@bb.utils.contains('DISTRO_FEATURES', 'gc520-kms', 'true', 'false', d)}; then
        sed -i \
            -e 's|^export QT_QPA_PLATFORM=.*|export QT_QPA_PLATFORM="etnaviv2d"|' \
            -e '/^export XDG_RUNTIME_DIR=/d' \
            ${D}${sysconfdir}/profile.d/qt5-env.sh
    fi
}
