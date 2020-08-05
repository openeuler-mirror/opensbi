# The obs worker of RISC-V runs in cross-arch qemu virt, which support 
# multi-thread maxmium of 8.
%global _smp_mflags -j8
%global debug_package %{nil}

Name:	 opensbi
Version: 0.6
Release: 1
Summary: RISC-V Open Source Supervisor Binary Interface
URL:	 https://github.com/riscv/opensbi
License: BSD

Source0: https://github.com/riscv/opensbi/archive/v0.6.zip

Patch0: 0001-Enable-build-id-for-elf-files.patch

BuildRequires: kernel-riscv64
BuildRequires: gcc, binutils, findutils, coreutils, gzip, file

Provides: opensbi-%{_target_cpu}-image = %{version}-%{release}

ExclusiveArch: riscv64
ExclusiveOS: Linux

%ifarch riscv64
%define hd_arch riscv
%endif

%description
The RISC-V openSBI with flattened kernel image as payload. 
Currently this packages only provides booting image for RISC-V QEMU virt.

%package devel
Summary: OpenSBI Generic Headers and library

%description devel
The opensbi static lib for developing applications of interaction with RISC-V opensbi.

%package devel-qemu
Summary: OpenSBI Static library for QEMU

%description devel-qemu
The opensbi lib for developing applications of interaction with RISC-V firmware.

%prep
%autosetup -n opensbi-%{version}

%build
mkdir -p build-oe/qemu-virt

# QEMU/virt build: use flatten Linux kernel Image as QEMU virt payload
make O=build-oe/qemu-virt PLATFORM=qemu/virt FW_PAYLOAD=y FW_PAYLOAD_PATH=/boot/Image 

# TODO: build opensbi Image for SiFive hardware

%install 
# QEMU/virt Install
make I=%{buildroot} PLATFORM=qemu/virt O=build-oe/qemu-virt install
mkdir -p %{buildroot}/boot
cp %{buildroot}/platform/qemu/virt/firmware/fw_payload.elf \
	 %{buildroot}/boot/fw_payload_oe_qemuvirt.elf

%files
%license COPYING.BSD
%doc README.md
/boot/fw_payload_oe_qemuvirt.elf

%files devel
/include/*
/lib/*

%files devel-qemu
/platform/qemu/virt/*

%changelog
* Mon Aug 03 2020 whoisxxx <zhangxuzhou4@huawei.com> - 0.6-1-riscv64
- Init version of QEMU/virt with flattened Image as payload
