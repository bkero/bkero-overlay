# Copyright 1999-2014 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: /var/cvsroot/gentoo-x86/dev-python/oslo-messaging/oslo-messaging-1.3.0.ebuild,v 1.4 2014/08/10 21:14:49 slyfox Exp $

EAPI=5
PYTHON_COMPAT=( python2_7 )

inherit distutils-r1

DESCRIPTION=""
HOMEPAGE="https://pypi.python.org/pypi/oslo.i18n"
SRC_URI="mirror://pypi/${PN:0:1}/oslo.config/oslo.i18n-${PV}.tar.gz"
S="${WORKDIR}/oslo.i18n-${PV}"

LICENSE="Apache-2.0"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE="docs test"

DEPEND="
		>=dev-python/Babel-1.3
		>=dev-python/six-1.7.0
	    test? (
		>=dev-python/hacking-0.9.2
		<dev-python/hacking-0.10
		>=dev-python/oslosphinx-2.2.0_alpha2
		>=dev-python/oslotest-1.1.0.0_alpha1 )"

RDEPENDS=${DEPENDS}

# This time half the doc files are missing; Do you want them?

python_test() {
	nosetests tests/ || die "test failed under ${EPYTHON}"
}
