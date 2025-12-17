#!/usr/bin/env python3

import json
import glob
import os
import shutil
import subprocess
from pathlib import Path
import argparse

# Image type definitions
IMG_SD = 0
IMG_NAND = 1
IMG_SPINAND = 2
IMG_SPINOR = 3
IMG_UNKNOWN = 0xFF

# Define deploy_dir as a global variable
deploy_dir = ""
def deploy_path(filename):
    return os.path.join(deploy_dir, filename)

def get_image(image) -> int:
	image = str.upper(image)
	return {
		'SD': IMG_SD,
		'NAND': IMG_NAND,
		'SPINAND': IMG_SPINAND,
		'SPINOR': IMG_SPINOR,
	}.get(image, IMG_UNKNOWN)

from datetime import datetime

SDCARD = ""
BOOT_SPACE = 32768
IMAGE_ROOTFS_ALIGNMENT = 4096
BOOT_SPACE_ALIGNED = BOOT_SPACE - 1

def main():
    parser = argparse.ArgumentParser(description="Generate image for MA35 platform.")
    parser.add_argument("--deploy_dir", type=str, help="Path to DEPLOY_DIR_IMAGE.")
    parser.add_argument("--imgdeploy_dir", type=str, help="Path to IMGDEPLOY_DIR.")
    parser.add_argument("--image_name", type=str, help="Image Name.")
    parser.add_argument("--image_basename", type=str, help="Image BaseName.")
    parser.add_argument("--machine", type=str, help="Machine.")
    parser.add_argument("--secure_boot", type=str, help="Enable secure boot encryption.")
    parser.add_argument("--aes_key", type=str, help="AES key.")
    parser.add_argument("--ecdsa_key", type=str, help="ECDSA key.")	
    parser.add_argument("--tfa_load_m4", type=str, help="Include M4 binary.")
    parser.add_argument("--tfa_m4_bin", type=str, help="Include M4 binary.")
    parser.add_argument("--tfa_load_optee", type=str, help="Include OP-TEE binary.")
    parser.add_argument("--tfa_platform", type=str, help="ATF Platform.")
    parser.add_argument("--nuwriter_dir", type=str, help="Path to nuwriter tool.")
    parser.add_argument("--image", type=str, help="Select Image.")
    parser.add_argument("--sd_rootfs_size", type=int, help="rootfs size.")
    parser.add_argument("--ubinize_args", type=str, help="ubinize args.")

    args = parser.parse_args()
    
    image_id = get_image(args.image)
    try:
        if image_id == IMG_UNKNOWN:
            raise ValueError(f"Cannot support image {str.upper(args.image[0])}")
    except ValueError as err:
            sys.exit(err)

    global deploy_dir

    deploy_dir = args.deploy_dir  # Set deploy_dir dynamically here
    os.chdir(deploy_dir)

    enc = ""
    fipdir = ""
    rtp_bin="{args.tfa_m4_bin}"
    fip_matrix = [("bl31-{args.tfa_platform}.bin","--soc-fw"), ("u-boot.bin-sdcard","--nt-fw")]
    if image_id == IMG_SD:
        global SDCARD
        SDCARD = os.path.join(args.imgdeploy_dir,f"{args.image_name}.sdcard")
        files = [f"header-${args.image_basename}-${args.machine}-enc-sdcard.bin", f"${args.image_basename}-${args.machine}-enc-sdcard.pack", f"pack-${args.image_basename}-${args.machine}-enc-sdcard.bin", f"header-${args.image_basename}-${args.machine}-sdcard.bin", f"${args.image_basename}-${args.machine}-sdcard.pack", f"pack-${args.image_basename}-${args.machine}-sdcard.bin" ]
        for file in files:
            if os.path.exists(file):
                os.remove(file)
        if args.tfa_load_optee == "yes":
            target = enc + f'fip_with_optee-{args.image_basename}-{args.machine}.bin-sdcard'
            fip_matrix.append(("tee-header_v2-optee.bin","--tos-fw"))
            fip_matrix.append(("tee-pager_v2-optee.bin","--tos-fw-extra1"))
        else:
            target = enc + f'fip_without_optee-{args.image_basename}-{args.machine}.bin-sdcard'

        if args.tfa_load_m4 == "yes":
            m4path = deploy_path(args.tfa_m4_bin)
            if os.path.isfile(m4path):
                fip_matrix.append((args.tfa_m4_bin,"--scp-fw"))

        if args.secure_boot == "yes":
            fipdir = "fip/"
            enc = "enc_"
            
            if os.path.exists(deploy_path(f"fip_with_optee-{args.image_basename}-{args.machine}.bin-sdcard")):
                os.remove(deploy_path(f"fip_with_optee-{args.image_basename}-{args.machine}.bin-sdcard"))
            if os.path.exists(deploy_path(f"fip_without_optee-{args.image_basename}-{args.machine}.bin-sdcard")):
                os.remove(deploy_path(f"fip_without_optee-{args.image_basename}-{args.machine}.bin-sdcard"))
            os.makedirs(fipdir, exist_ok=True)
            enc_config = "fip/enc_fip.json"
            enc_bin = "fip/enc.bin"
            json_cmd = f"jq '.header.secureboot = \"yes\" | .header.aeskey = \"{args.aes_key}\" | .header.ecdsakey = \"{args.ecdsa_key}\"' {args.nuwriter_dir}/enc_fip.json >{enc_config}"
            subprocess.run(json_cmd, shell=True, check=True)
            for fip_file, fip_arg in fip_matrix:
                shutil.copyfile(deploy_path(fip_file.format(args=args)), enc_bin)
                subprocess.run([deploy_path("nuwriter/nuwriter"), "-c", enc_config], stdout=subprocess.DEVNULL, check=True)
                output_path =deploy_path(f"{fipdir}{enc}{fip_file.format(args=args)}")
                with open(deploy_path("conv/enc_enc.bin"), "rb") as f1, open(deploy_path("conv/header.bin"), "rb") as f2, open(output_path, "wb") as out:
                    out.write(f1.read())
                    out.write(f2.read())
                today_prefix = datetime.now().strftime("%m%d-")
                for name in os.listdir("."):
                    if name.startswith(today_prefix):
                        if os.path.isdir(name):
                            shutil.rmtree(name, ignore_errors=True)
                        else:
                            os.remove(name)

            if args.tfa_load_m4 == "yes":
                os.rename("fip/"+"{enc}{f}", "fip/"+"{enc}"+"rtp.bin")
                rtp_bin = rtp.bin

            if os.path.exists(f"{enc_bin}"):
                os.remove(f"{enc_bin}")
            if os.path.exists(f"{enc_config}"):
                os.remove(f"{enc_config}")

        fiptool = deploy_path('fiptool')
        cmd = [fiptool, 'create']
        for fip_file, fip_arg in fip_matrix:
            file_path = deploy_path(f"{fipdir}{enc}{fip_file.format(args=args)}")
            cmd.extend([fip_arg, file_path])
        cmd.append(target)
        subprocess.run(cmd, check=True)
        if os.path.islink(f'fip.bin-sdcard') or os.path.exists(f'fip.bin-sdcard'):
            os.unlink(f'fip.bin-sdcard')
        os.symlink(target, f'fip.bin-sdcard')

        image_path = os.path.join(args.imgdeploy_dir, f"{args.image_basename}-{args.machine}.rootfs.ext4")
        if os.path.isfile(image_path):
            SDCARD_SIZE = BOOT_SPACE_ALIGNED + IMAGE_ROOTFS_ALIGNMENT + args.sd_rootfs_size + IMAGE_ROOTFS_ALIGNMENT
            dd_cmd = ["dd", "if=/dev/zero", f"of={SDCARD}", "bs=1", "count=0", f"seek={1024 * SDCARD_SIZE}"]
            subprocess.run(dd_cmd, shell=True, check=True)
            with open(SDCARD, "wb") as f:
                f.truncate(1024 * SDCARD_SIZE)
            subprocess.run(f"parted -s {SDCARD} mklabel msdos", shell=True, check=True)
            part_start = BOOT_SPACE_ALIGNED + IMAGE_ROOTFS_ALIGNMENT
            part_end = part_start + args.sd_rootfs_size
            subprocess.run(f"parted -s {SDCARD} unit KiB mkpart primary {part_start} {part_end}", shell=True, check=True)
            subprocess.run(f"parted {SDCARD} print", shell=True, check=True)
            mbr_bin = deploy_path("MBR.scdard.bin")
            subprocess.run(f"dd if=/dev/zero of={mbr_bin} bs=1 count=0 seek=512", shell=True, check=True)
            subprocess.run(f"dd if={SDCARD} of={mbr_bin} conv=notrunc seek=0 count=1 bs=512", shell=True, check=True)
            if os.path.exists(f"rootfs.ext4-sdcard"):
                os.remove(f"rootfs.ext4-sdcard")
            os.symlink(os.path.join(args.imgdeploy_dir, f"{args.image_basename}-{args.machine}.rootfs.ext4"), f"rootfs.ext4-sdcard")
            if args.secure_boot == "no":
                src_files = glob.glob(os.path.join(args.nuwriter_dir, f"*-sdcard.json"))
                for file in src_files:
                    shutil.copy(file, deploy_path("nuwriter"))
                subprocess.run([deploy_path("nuwriter/nuwriter"), "-c", f"nuwriter/header-sdcard.json"], check=True)
                shutil.copy(deploy_path("conv/header.bin"), deploy_path(f"header-{args.image_basename}-{args.machine}-sdcard.bin"))
                data = json.load(open(os.path.join(args.nuwriter_dir, f"pack-sdcard.json")))
                data["image"][8]["offset"] = str((BOOT_SPACE_ALIGNED + IMAGE_ROOTFS_ALIGNMENT) * 1024)
                with open(f"nuwriter/pack-sdcard.json", "w") as f:
                    json.dump(data, f, indent=2)
                subprocess.run([deploy_path("nuwriter/nuwriter"), "-p", f"nuwriter/pack-sdcard.json"], check=True)
                shutil.copy(os.path.join(args.deploy_dir, "pack", "pack.bin"), deploy_path(f"pack-{args.image_basename}-{args.machine}-sdcard.bin"))
                symlink_name = f"{args.image_basename}-{args.machine}-sdcard.pack"
                if os.path.exists(symlink_name):
                    os.remove(symlink_name)
                os.symlink(f"pack-{args.image_basename}-{args.machine}-sdcard.bin", symlink_name)
                if os.path.exists(f"enc_bl2-ma35d1-sdcard.dtb"):
                    os.remove(f"enc_bl2-ma35d1-sdcard.dtb")
                if os.path.exists(f"enc_bl2-ma35d1-sdcard.bin"):
                    os.remove(f"enc_bl2-ma35d1-sdcard.bin")
            else:
                with open(os.path.join(args.nuwriter_dir, f"header-sdcard.json"), "r") as f:
                    data = json.load(f)
                data["header"]["secureboot"] = "yes"
                data["header"]["aeskey"] = str(args.aes_key)
                data["header"]["ecdsakey"] = str(args.ecdsa_key)
                with open(f"nuwriter/header-sdcard.json", "w") as f:
                   json.dump(data, f, indent=4)
                subprocess.run(["nuwriter/nuwriter", "-c", f"nuwriter/header-sdcard.json"], check=True)
                shutil.copy("conv/enc_bl2-ma35d1.dtb", f"enc_bl2-ma35d1-sdcard.dtb")
                shutil.copy("conv/enc_bl2-ma35d1.bin", f"enc_bl2-ma35d1-sdcard.bin")
                lines = open(f"conv/header_key.txt").read().splitlines()
                otp = {"publicx": lines[5], "publicy": lines[6], "aeskey":  lines[1] }
                with open(f"nuwriter/otp_key-sdcard.json", "w") as f:
                    json.dump(otp, f, indent=2)
                shutil.copy("conv/header.bin", f"header-{args.image_basename}-{args.machine}-enc-sdcard.bin")
                data = json.load(open(os.path.join(args.nuwriter_dir, f"pack-sdcard.json")))
                data["image"][2]["file"]   = f"enc_bl2-ma35d1-sdcard.dtb"
                data["image"][3]["file"]   = f"enc_bl2-ma35d1-sdcard.bin"
                data["image"][8]["offset"] = str((BOOT_SPACE_ALIGNED + IMAGE_ROOTFS_ALIGNMENT) * 1024)
                with open(f"nuwriter/pack-sdcard.json", "w") as f:
                    json.dump(data, f, indent=2)
                subprocess.run(["nuwriter/nuwriter", "-p", f"nuwriter/pack-sdcard.json"], check=True)
                shutil.copy("pack/pack.bin", f"pack-{args.image_basename}-{args.machine}-enc-sdcard.bin")
                if os.path.exists(f"{args.image_basename}-{args.machine}-enc-sdcard.pack"):
                    os.remove(f"{args.image_basename}-{args.machine}-enc-sdcard.pack")
                os.symlink(f"pack-{args.image_basename}-{args.machine}-enc-sdcard.bin", f"{args.image_basename}-{args.machine}-enc-sdcard.pack")
            today_prefix = datetime.now().strftime("%m%d-")
            for name in os.listdir("."):
                if name.startswith(today_prefix):
                    if os.path.isdir(name):
                        shutil.rmtree(name, ignore_errors=True)
                    else:
                        os.remove(name)

        SDCARD_SIZE = BOOT_SPACE_ALIGNED + IMAGE_ROOTFS_ALIGNMENT + args.sd_rootfs_size + IMAGE_ROOTFS_ALIGNMENT
        if args.secure_boot == "no":
            cmd = ["dd", f"if={args.deploy_dir}/header-{args.image_basename}-{args.machine}-sdcard.bin", f"of={SDCARD}", "conv=notrunc", f"seek=2", f"bs=512"]
            subprocess.run(cmd, check=True)
            cmd = ["dd", f"if={args.deploy_dir}/bl2-ma35d1.dtb", f"of={SDCARD}", "conv=notrunc", f"seek=256", f"bs=512"]
            subprocess.run(cmd, check=True)
            cmd = ["dd", f"if={args.deploy_dir}/bl2-ma35d1.bin", f"of={SDCARD}", "conv=notrunc", f"seek=384", f"bs=512"]
            subprocess.run(cmd, check=True)
        else:
            cmd = ["dd", f"if={args.deploy_dir}/header-{args.image_basename}-{args.machine}-enc-sdcard.bin", f"of={SDCARD}", "conv=notrunc", f"seek=384", f"bs=512"]
            subprocess.run(cmd, check=True)
            cmd = ["dd", f"if={args.deploy_dir}/enc_bl2-ma35d1-sdcard.dtb", f"of={SDCARD}", "conv=notrunc", f"seek=256", f"bs=512"]
            subprocess.run(cmd, check=True)
            cmd = ["dd", f"if={args.deploy_dir}/enc_bl2-ma35d1-sdcard.bin", f"of={SDCARD}", "conv=notrunc", f"seek=384", f"bs=512"]
            subprocess.run(cmd, check=True)

        cmd = ["dd", f"if={args.deploy_dir}/u-boot-initial-env.bin-sdcard", f"of={SDCARD}", "conv=notrunc", f"seek=512", f"bs=512"]
        subprocess.run(cmd, check=True)
        cmd = ["dd", f"if={args.deploy_dir}/fip.bin-sdcard", f"of={SDCARD}", "conv=notrunc", f"seek=1536", f"bs=512"]
        subprocess.run(cmd, check=True)
        cmd = ["dd", f"if={args.deploy_dir}/Image.dtb", f"of={SDCARD}", "conv=notrunc", f"seek=5632", f"bs=512"]
        subprocess.run(cmd, check=True)
        cmd = ["dd", f"if={args.deploy_dir}/Image", f"of={SDCARD}", "conv=notrunc", f"seek=6144", f"bs=512"]
        subprocess.run(cmd, check=True)
        seek_bytes = BOOT_SPACE_ALIGNED * 1024 + IMAGE_ROOTFS_ALIGNMENT * 1024
        cmd = ["dd", f"if={args.imgdeploy_dir}/{args.image_name}.ext4", f"of={SDCARD}", "conv=notrunc,fsync", f"seek=1", f"bs={seek_bytes}"]
        subprocess.run(cmd, check=True)
    elif image_id == IMG_NAND:
        files = [f"header-${args.image_basename}-${args.machine}-enc-nand.bin", f"${args.image_basename}-${args.machine}-enc-nand.pack", f"pack-${args.image_basename}-${args.machine}-enc-nand.bin", f"header-${args.image_basename}-${args.machine}-nand.bin", f"${args.image_basename}-${args.machine}-nand.pack", f"pack-${args.image_basename}-${args.machine}-nand.bin" ]
        for file in files:
            if os.path.exists(file):
                os.remove(file)
        if args.tfa_load_optee == "yes":
            target = enc + f'fip_with_optee-{args.image_basename}-{args.machine}.bin-nand'
            fip_matrix.append(("tee-header_v2-optee.bin","--tos-fw"))
            fip_matrix.append(("tee-pager_v2-optee.bin","--tos-fw-extra1"))
        else:
            target = enc + f'fip_without_optee-{args.image_basename}-{args.machine}.bin-nand'
        if args.tfa_load_m4 == "yes":
            m4path = deploy_path(args.tfa_m4_bin)
            if os.path.isfile(m4path):
                fip_matrix.append((args.tfa_m4_bin,"--scp-fw"))
        if args.secure_boot == "yes":
            fipdir = "fip/"
            enc = "enc_"
            if os.path.exists(deploy_path(f"fip_with_optee-{args.image_basename}-{args.machine}.bin-nand")):
                os.remove(deploy_path(f"fip_with_optee-{args.image_basename}-{args.machine}.bin-nand"))
            if os.path.exists(deploy_path(f"fip_without_optee-{args.image_basename}-{args.machine}.bin-nand")):
                os.remove(deploy_path(f"fip_without_optee-{args.image_basename}-{args.machine}.bin-nand"))
            os.makedirs(fipdir, exist_ok=True)
            enc_config = "fip/enc_fip.json"
            enc_bin = "fip/enc.bin"
            json_cmd = f"jq '.header.secureboot = \"yes\" | .header.aeskey = \"{args.aes_key}\" | .header.ecdsakey = \"{args.ecdsa_key}\"' {args.nuwriter_dir}/enc_fip.json >{enc_config}"
            subprocess.run(json_cmd, shell=True, check=True)
            for fip_file, fip_arg in fip_matrix:
                shutil.copyfile(deploy_path(fip_file.format(args=args)), enc_bin)
                subprocess.run([deploy_path("nuwriter/nuwriter"), "-c", enc_config], stdout=subprocess.DEVNULL, check=True)
                output_path =deploy_path(f"{fipdir}{enc}{fip_file.format(args=args)}")
                with open(deploy_path("conv/enc_enc.bin"), "rb") as f1, open(deploy_path("conv/header.bin"), "rb") as f2, open(output_path, "wb") as out:
                    out.write(f1.read())
                    out.write(f2.read())
                today_prefix = datetime.now().strftime("%m%d-")
                for name in os.listdir("."):
                    if name.startswith(today_prefix):
                        if os.path.isdir(name):
                            shutil.rmtree(name, ignore_errors=True)
                        else:
                            os.remove(name)
            if args.tfa_load_m4 == "yes":
                os.rename("fip/"+"{enc}{f}", "fip/"+"{enc}"+"rtp.bin")
                rtp_bin = rtp.bin
            if os.path.exists(f"{enc_bin}"):
                os.remove(f"{enc_bin}")
            if os.path.exists(f"{enc_config}"):
                os.remove(f"{enc_config}")

        fiptool = deploy_path('fiptool')
        cmd = [fiptool, 'create']
        for fip_file, fip_arg in fip_matrix:
            file_path = deploy_path(f"{fipdir}{enc}{fip_file.format(args=args)}")
            cmd.extend([fip_arg, file_path])
        cmd.append(target)
        subprocess.run(cmd, check=True)
        if os.path.islink(f'fip.bin-nand') or os.path.exists(f'fip.bin-nand'):
            os.unlink(f'fip.bin-nand')
        os.symlink(target, f'fip.bin-nand')

        if isinstance(args.ubinize_args, str):
            ubinize_args = args.ubinize_args.split()
        cmd = ["ubinize"] + ubinize_args + ["-o", f"u-boot-initial-env.ubi-nand", f"u-boot-initial-env-nand-ubi.cfg"]
        subprocess.run(cmd, check=True)
        image_path = os.path.join(args.imgdeploy_dir, f"{args.image_basename}-{args.machine}.rootfs.ubi")
        if os.path.isfile(image_path):
            if os.path.exists(f"rootfs.ubi-nand"):
                os.remove(f"rootfs.ubi-nand")
            os.symlink(os.path.join(args.imgdeploy_dir, f"{args.image_basename}-{args.machine}.rootfs.ubi"), f"rootfs.ubi-nand")
            if args.secure_boot == "no":
                src_files = glob.glob(os.path.join(args.nuwriter_dir, f"*-nand.json"))
                for file in src_files:
                    shutil.copy(file, deploy_path("nuwriter"))
                subprocess.run([deploy_path("nuwriter/nuwriter"), "-c", f"nuwriter/header-nand.json"], check=True)
                shutil.copy(deploy_path("conv/header.bin"), deploy_path(f"header-{args.image_basename}-{args.machine}-nand.bin"))
                subprocess.run([deploy_path("nuwriter/nuwriter"), "-p", f"nuwriter/pack-nand.json"], check=True)
                shutil.copy(os.path.join(args.deploy_dir, "pack", "pack.bin"), deploy_path(f"pack-{args.image_basename}-{args.machine}-nand.bin"))
                symlink_name = f"{args.image_basename}-{args.machine}-nand.pack"
                if os.path.exists(symlink_name):
                    os.remove(symlink_name)
                os.symlink(f"pack-{args.image_basename}-{args.machine}-nand.bin", symlink_name)
                if os.path.exists(f"enc_bl2-ma35d1-nand.dtb"):
                    os.remove(f"enc_bl2-ma35d1-nand.dtb")
                if os.path.exists(f"enc_bl2-ma35d1-nand.bin"):
                    os.remove(f"enc_bl2-ma35d1-nand.bin")
            else:
                with open(os.path.join(args.nuwriter_dir, f"header-nand.json"), "r") as f:
                    data = json.load(f)
                data["header"]["secureboot"] = "yes"
                data["header"]["aeskey"] = str(args.aes_key)
                data["header"]["ecdsakey"] = str(args.ecdsa_key)
                with open(f"nuwriter/header-nand.json", "w") as f:
                   json.dump(data, f, indent=4)
                subprocess.run(["nuwriter/nuwriter", "-c", f"nuwriter/header-nand.json"], check=True)
                shutil.copy("conv/enc_bl2-ma35d1.dtb", f"enc_bl2-ma35d1-nand.dtb")
                shutil.copy("conv/enc_bl2-ma35d1.bin", f"enc_bl2-ma35d1-nand.bin")
                lines = open(f"conv/header_key.txt").read().splitlines()
                otp = {"publicx": lines[5], "publicy": lines[6], "aeskey":  lines[1]}
                with open(f"nuwriter/otp_key-nand.json", "w") as f:
                    json.dump(otp, f, indent=2)
                shutil.copy("conv/header.bin", f"header-{args.image_basename}-{args.machine}-enc-nand.bin")
                data = json.load(open(os.path.join(args.nuwriter_dir, f"pack-nand.json")))
                data["image"][1]["file"]   = f"enc_bl2-ma35d1-nand.dtb"
                data["image"][2]["file"]   = f"enc_bl2-ma35d1-nand.bin"
                with open(f"nuwriter/pack-nand.json", "w") as f:
                    json.dump(data, f, indent=2)
                subprocess.run(["nuwriter/nuwriter", "-p", f"nuwriter/pack-nand.json"], check=True)
                shutil.copy("pack/pack.bin", f"pack-{args.image_basename}-{args.machine}-enc-nand.bin")
                if os.path.exists(f"{args.image_basename}-{args.machine}-enc-nand.pack"):
                    os.remove(f"{args.image_basename}-{args.machine}-enc-nand.pack")
                os.symlink(f"pack-{args.image_basename}-{args.machine}-enc-nand.bin", f"{args.image_basename}-{args.machine}-enc-nand.pack")

            today_prefix = datetime.now().strftime("%m%d-")
            for name in os.listdir("."):
                if name.startswith(today_prefix):
                    if os.path.isdir(name):
                        shutil.rmtree(name, ignore_errors=True)
                    else:
                        os.remove(name)

    elif  image_id == IMG_SPINAND:
        files = [f"header-${args.image_basename}-${args.machine}-enc-spinand.bin", f"${args.image_basename}-${args.machine}-enc-spinand.pack", f"pack-${args.image_basename}-${args.machine}-enc-spinand.bin", f"header-${args.image_basename}-${args.machine}-spinand.bin", f"${args.image_basename}-${args.machine}-spinand.pack", f"pack-${args.image_basename}-${args.machine}-spinand.bin" ]
        for file in files:
            if os.path.exists(file):
                os.remove(file)
        if args.tfa_load_optee == "yes":
            target = enc + f'fip_with_optee-{args.image_basename}-{args.machine}.bin-spinand'
            fip_matrix.append(("tee-header_v2-optee.bin","--tos-fw"))
            fip_matrix.append(("tee-pager_v2-optee.bin","--tos-fw-extra1"))
        else:
            target = enc + f'fip_without_optee-{args.image_basename}-{args.machine}.bin-spinand'

        if args.tfa_load_m4 == "yes":
            m4path = deploy_path(args.tfa_m4_bin)
            if os.path.isfile(m4path):
                fip_matrix.append((args.tfa_m4_bin,"--scp-fw"))

        if args.secure_boot == "yes":
            fipdir = "fip/"
            enc = "enc_"
            if os.path.exists(deploy_path(f"fip_with_optee-{args.image_basename}-{args.machine}.bin-spinand")):
                os.remove(deploy_path(f"fip_with_optee-{args.image_basename}-{args.machine}.bin-spinand"))
            if os.path.exists(deploy_path(f"fip_without_optee-{args.image_basename}-{args.machine}.bin-spinand")):
                os.remove(deploy_path(f"fip_without_optee-{args.image_basename}-{args.machine}.bin-spinand"))

            os.makedirs(fipdir, exist_ok=True)
            enc_config = "fip/enc_fip.json"
            enc_bin = "fip/enc.bin"
            json_cmd = f"jq '.header.secureboot = \"yes\" | .header.aeskey = \"{args.aes_key}\" | .header.ecdsakey = \"{args.ecdsa_key}\"' {args.nuwriter_dir}/enc_fip.json >{enc_config}"
            subprocess.run(json_cmd, shell=True, check=True)
            for fip_file, fip_arg in fip_matrix:
                shutil.copyfile(deploy_path(fip_file.format(args=args)), enc_bin)
                subprocess.run([deploy_path("nuwriter/nuwriter"), "-c", enc_config], stdout=subprocess.DEVNULL, check=True)
                output_path =deploy_path(f"{fipdir}{enc}{fip_file.format(args=args)}")
                with open(deploy_path("conv/enc_enc.bin"), "rb") as f1, open(deploy_path("conv/header.bin"), "rb") as f2, open(output_path, "wb") as out:
                    out.write(f1.read())
                    out.write(f2.read())
                today_prefix = datetime.now().strftime("%m%d-")
                for name in os.listdir("."):
                    if name.startswith(today_prefix):
                        if os.path.isdir(name):
                            shutil.rmtree(name, ignore_errors=True)
                        else:
                            os.remove(name)

            if args.tfa_load_m4 == "yes":
                os.rename("fip/"+"{enc}{f}", "fip/"+"{enc}"+"rtp.bin")
                rtp_bin = rtp.bin
            if os.path.exists(f"{enc_bin}"):
                os.remove(f"{enc_bin}")
            if os.path.exists(f"{enc_config}"):
                os.remove(f"{enc_config}")

        fiptool = deploy_path('fiptool')
        cmd = [fiptool, 'create']
        for fip_file, fip_arg in fip_matrix:
            file_path = deploy_path(f"{fipdir}{enc}{fip_file.format(args=args)}")
            cmd.extend([fip_arg, file_path])
        cmd.append(target)
        subprocess.run(cmd, check=True)
        if os.path.islink(f'fip.bin-spinand') or os.path.exists(f'fip.bin-spinand'):
            os.unlink(f'fip.bin-spinand')
        os.symlink(target, f'fip.bin-spinand')

        if isinstance(args.ubinize_args, str):
            ubinize_args = args.ubinize_args.split()
        cmd = ["ubinize"] + ubinize_args + ["-o", f"u-boot-initial-env.ubi-spinand", f"u-boot-initial-env-spinand-ubi.cfg"]
        subprocess.run(cmd, check=True)

        image_path = os.path.join(args.imgdeploy_dir, f"{args.image_basename}-{args.machine}.rootfs.ubi")
        if os.path.isfile(image_path):
            if os.path.exists(f"rootfs.ubi-spinand"):
                os.remove(f"rootfs.ubi-spinand")
            os.symlink(os.path.join(args.imgdeploy_dir, f"{args.image_basename}-{args.machine}.rootfs.ubi"), f"rootfs.ubi-spinand")
            if args.secure_boot == "no":
                src_files = glob.glob(os.path.join(args.nuwriter_dir, f"*-spinand.json"))
                for file in src_files:
                    shutil.copy(file, deploy_path("nuwriter"))

                subprocess.run([deploy_path("nuwriter/nuwriter"), "-c", f"nuwriter/header-spinand.json"], check=True)
                shutil.copy(deploy_path("conv/header.bin"), deploy_path(f"header-{args.image_basename}-{args.machine}-spinand.bin"))
                subprocess.run([deploy_path("nuwriter/nuwriter"), "-p", f"nuwriter/pack-spinand.json"], check=True)
                shutil.copy(os.path.join(args.deploy_dir, "pack", "pack.bin"), deploy_path(f"pack-{args.image_basename}-{args.machine}-spinand.bin"))

                symlink_name = f"{args.image_basename}-{args.machine}-spinand.pack"
                if os.path.exists(symlink_name):
                    os.remove(symlink_name)
                os.symlink(f"pack-{args.image_basename}-{args.machine}-spinand.bin", symlink_name)
                if os.path.exists(f"enc_bl2-ma35d1-spinand.dtb"):
                    os.remove(f"enc_bl2-ma35d1-spinand.dtb")
                if os.path.exists(f"enc_bl2-ma35d1-spinand.bin"):
                    os.remove(f"enc_bl2-ma35d1-spinand.bin")
            else:
                with open(os.path.join(args.nuwriter_dir, f"header-spinand.json"), "r") as f:
                    data = json.load(f)
                data["header"]["secureboot"] = "yes"
                data["header"]["aeskey"] = str(args.aes_key)
                data["header"]["ecdsakey"] = str(args.ecdsa_key)
                with open(f"nuwriter/header-spinand.json", "w") as f:
                   json.dump(data, f, indent=4)
                subprocess.run(["nuwriter/nuwriter", "-c", f"nuwriter/header-spinand.json"], check=True)

                shutil.copy("conv/enc_bl2-ma35d1.dtb", f"enc_bl2-ma35d1-spinand.dtb")
                shutil.copy("conv/enc_bl2-ma35d1.bin", f"enc_bl2-ma35d1-spinand.bin")

                lines = open(f"conv/header_key.txt").read().splitlines()
                otp = {"publicx": lines[5], "publicy": lines[6], "aeskey":  lines[1]}
                with open(f"nuwriter/otp_key-spinand.json", "w") as f:
                    json.dump(otp, f, indent=2)

                shutil.copy("conv/header.bin", f"header-{args.image_basename}-{args.machine}-enc-spinand.bin")

                data = json.load(open(os.path.join(args.nuwriter_dir, f"pack-spinand.json")))
                data["image"][1]["file"]   = f"enc_bl2-ma35d1-spinand.dtb"
                data["image"][2]["file"]   = f"enc_bl2-ma35d1-spinand.bin"
                with open(f"nuwriter/pack-spinand.json", "w") as f:
                    json.dump(data, f, indent=2)

                subprocess.run(["nuwriter/nuwriter", "-p", f"nuwriter/pack-spinand.json"], check=True)

                shutil.copy("pack/pack.bin", f"pack-{args.image_basename}-{args.machine}-enc-spinand.bin")

                if os.path.exists(f"{args.image_basename}-{args.machine}-enc-spinand.pack"):
                    os.remove(f"{args.image_basename}-{args.machine}-enc-spinand.pack")
                os.symlink(f"pack-{args.image_basename}-{args.machine}-enc-spinand.bin", f"{args.image_basename}-{args.machine}-enc-spinand.pack")

            today_prefix = datetime.now().strftime("%m%d-")
            for name in os.listdir("."):
                if name.startswith(today_prefix):
                    if os.path.isdir(name):
                        shutil.rmtree(name, ignore_errors=True)
                    else:
                        os.remove(name)

    elif  image_id == IMG_SPINOR:
        files = [f"header-${args.image_basename}-${args.machine}-enc-spinor.bin", f"${args.image_basename}-${args.machine}-enc-spinor.pack", f"pack-${args.image_basename}-${args.machine}-enc-spinor.bin", f"header-${args.image_basename}-${args.machine}-spinor.bin", f"${args.image_basename}-${args.machine}-spinor.pack", f"pack-${args.image_basename}-${args.machine}-spinor.bin" ]
        for file in files:
            if os.path.exists(file):
                os.remove(file)
        if args.tfa_load_optee == "yes":
            target = enc + f'fip_with_optee-{args.image_basename}-{args.machine}.bin-spinor'
            fip_matrix.append(("tee-header_v2-optee.bin","--tos-fw"))
            fip_matrix.append(("tee-pager_v2-optee.bin","--tos-fw-extra1"))
        else:
            target = enc + f'fip_without_optee-{args.image_basename}-{args.machine}.bin-spinor'

        if args.tfa_load_m4 == "yes":
            m4path = deploy_path(args.tfa_m4_bin)
            if os.path.isfile(m4path):
                fip_matrix.append((args.tfa_m4_bin,"--scp-fw"))

        if args.secure_boot == "yes":
            fipdir = "fip/"
            enc = "enc_"
            if os.path.exists(deploy_path(f"fip_with_optee-{args.image_basename}-{args.machine}.bin-spinor")):
                os.remove(deploy_path(f"fip_with_optee-{args.image_basename}-{args.machine}.bin-spinor"))
            if os.path.exists(deploy_path(f"fip_without_optee-{args.image_basename}-{args.machine}.bin-spinor")):
                os.remove(deploy_path(f"fip_without_optee-{args.image_basename}-{args.machine}.bin-spinor"))

            os.makedirs(fipdir, exist_ok=True)
            enc_config = "fip/enc_fip.json"
            enc_bin = "fip/enc.bin"
            json_cmd = f"jq '.header.secureboot = \"yes\" | .header.aeskey = \"{args.aes_key}\" | .header.ecdsakey = \"{args.ecdsa_key}\"' {args.nuwriter_dir}/enc_fip.json >{enc_config}"
            subprocess.run(json_cmd, shell=True, check=True)
            for fip_file, fip_arg in fip_matrix:
                shutil.copyfile(deploy_path(fip_file.format(args=args)), enc_bin)
                subprocess.run([deploy_path("nuwriter/nuwriter"), "-c", enc_config], stdout=subprocess.DEVNULL, check=True)
                output_path =deploy_path(f"{fipdir}{enc}{fip_file.format(args=args)}")
                with open(deploy_path("conv/enc_enc.bin"), "rb") as f1, open(deploy_path("conv/header.bin"), "rb") as f2, open(output_path, "wb") as out:
                    out.write(f1.read())
                    out.write(f2.read())
                today_prefix = datetime.now().strftime("%m%d-")
                for name in os.listdir("."):
                    if name.startswith(today_prefix):
                        if os.path.isdir(name):
                            shutil.rmtree(name, ignore_errors=True)
                        else:
                            os.remove(name)

            if args.tfa_load_m4 == "yes":
                os.rename("fip/"+"{enc}{f}", "fip/"+"{enc}"+"rtp.bin")
                rtp_bin = rtp.bin
            if os.path.exists(f"{enc_bin}"):
                os.remove(f"{enc_bin}")
            if os.path.exists(f"{enc_config}"):
                os.remove(f"{enc_config}")

        fiptool = deploy_path('fiptool')
        cmd = [fiptool, 'create']
        for fip_file, fip_arg in fip_matrix:
            file_path = deploy_path(f"{fipdir}{enc}{fip_file.format(args=args)}")
            cmd.extend([fip_arg, file_path])
        cmd.append(target)
        subprocess.run(cmd, check=True)
        if os.path.islink(f'fip.bin-spinor') or os.path.exists(f'fip.bin-spinor'):
            os.unlink(f'fip.bin-spinor')
        os.symlink(target, f'fip.bin-spinor')

        image_path = os.path.join(args.imgdeploy_dir, f"{args.image_basename}-{args.machine}.rootfs.ubi")
        if os.path.isfile(image_path):
            if os.path.exists(f"rootfs.ubi-spinor"):
                os.remove(f"rootfs.ubi-spinor")
            os.symlink(os.path.join(args.imgdeploy_dir, f"{args.image_basename}-{args.machine}.rootfs.ubi"), f"rootfs.ubi-spinor")
            if args.secure_boot == "no":
                src_files = glob.glob(os.path.join(args.nuwriter_dir, f"*-spinor.json"))
                for file in src_files:
                    shutil.copy(file, deploy_path("nuwriter"))

                subprocess.run([deploy_path("nuwriter/nuwriter"), "-c", f"nuwriter/header-spinor.json"], check=True)
                shutil.copy(deploy_path("conv/header.bin"), deploy_path(f"header-{args.image_basename}-{args.machine}-spinor.bin"))
                subprocess.run([deploy_path("nuwriter/nuwriter"), "-p", f"nuwriter/pack-spinor.json"], check=True)
                shutil.copy(os.path.join(args.deploy_dir, "pack", "pack.bin"), deploy_path(f"pack-{args.image_basename}-{args.machine}-spinor.bin"))
                symlink_name = f"{args.image_basename}-{args.machine}-spinor.pack"
                if os.path.exists(symlink_name):
                    os.remove(symlink_name)
                os.symlink(f"pack-{args.image_basename}-{args.machine}-spinor.bin", symlink_name)
                if os.path.exists(f"enc_bl2-ma35d1-spinor.dtb"):
                    os.remove(f"enc_bl2-ma35d1-spinor.dtb")
                if os.path.exists(f"enc_bl2-ma35d1-spinor.bin"):
                    os.remove(f"enc_bl2-ma35d1-spinor.bin")
            else:
                with open(os.path.join(args.nuwriter_dir, f"header-spinor.json"), "r") as f:
                    data = json.load(f)
                data["header"]["secureboot"] = "yes"
                data["header"]["aeskey"] = str(args.aes_key)
                data["header"]["ecdsakey"] = str(args.ecdsa_key)
                with open(f"nuwriter/header-spinor.json", "w") as f:
                   json.dump(data, f, indent=4)
                subprocess.run(["nuwriter/nuwriter", "-c", f"nuwriter/header-spinor.json"], check=True)

                shutil.copy("conv/enc_bl2-ma35d1.dtb", f"enc_bl2-ma35d1-spinor.dtb")
                shutil.copy("conv/enc_bl2-ma35d1.bin", f"enc_bl2-ma35d1-spinor.bin")

                lines = open(f"conv/header_key.txt").read().splitlines()
                otp = {"publicx": lines[5], "publicy": lines[6], "aeskey":  lines[1]}
                with open(f"nuwriter/otp_key-spinor.json", "w") as f:
                    json.dump(otp, f, indent=2)

                shutil.copy("conv/header.bin", f"header-{args.image_basename}-{args.machine}-enc-spinor.bin")

                data = json.load(open(os.path.join(args.nuwriter_dir, f"pack-spinor.json")))
                data["image"][1]["file"]   = f"enc_bl2-ma35d1-spinor.dtb"
                data["image"][2]["file"]   = f"enc_bl2-ma35d1-spinor.bin"
                with open(f"nuwriter/pack-spinor.json", "w") as f:
                    json.dump(data, f, indent=2)

                subprocess.run(["nuwriter/nuwriter", "-p", f"nuwriter/pack-spinor.json"], check=True)

                shutil.copy("pack/pack.bin", f"pack-{args.image_basename}-{args.machine}-enc-spinor.bin")

                if os.path.exists(f"{args.image_basename}-{args.machine}-enc-spinor.pack"):
                    os.remove(f"{args.image_basename}-{args.machine}-enc-spinor.pack")
                os.symlink(f"pack-{args.image_basename}-{args.machine}-enc-spinor.bin", f"{args.image_basename}-{args.machine}-enc-spinor.pack")

            today_prefix = datetime.now().strftime("%m%d-")
            for name in os.listdir("."):
                if name.startswith(today_prefix):
                    if os.path.isdir(name):
                        shutil.rmtree(name, ignore_errors=True)
                    else:
                        os.remove(name)

if __name__ == "__main__":
    main()

