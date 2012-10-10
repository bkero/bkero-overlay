# Copyright 1999-2012 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI=4
RESTRICT_PYTHON_ABIS="3.*"

inherit distutils

DESCRIPTION="Fluidsynth bindings"
HOMEPAGE="http://pypi.python.org/pypi/fluidsynth"
SRC_URI="mirror://pypi/${PN:0:1}/${PN}/${P}.tar.gz"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="~amd64"
IUSE=""

DEPEND="media-sound/fluidsynth"
RDEPEND="${DEPEND}"

src_install() {
	distutils_src_install
}
