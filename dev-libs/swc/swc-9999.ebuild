# Copyright 1999-2014 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI=5
inherit eutils git-2

DESCRIPTION="Wayland"
HOMEPAGE="https://github.com/michaelforney/swc"
EGIT_REPO_URI="https://github.com/michaelforney/swc.git"

EGIT_BRANCH="master"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="~amd64"
IUSE=""

DEPEND="dev-libs/wayland
		dev-libs/wld"
RDEPEND="${DEPEND}"

src_install() {
echo DESTDIR: ${D}
	emake DESTDIR="${D}" PREFIX=/usr install
}
