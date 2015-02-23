# Copyright 1999-2014 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: /var/cvsroot/gentoo-x86/dev-python/oslo-messaging/oslo-messaging-1.3.0.ebuild,v 1.4 2014/08/10 21:14:49 slyfox Exp $

EAPI=5
PYTHON_COMPAT=( python2_7 )

inherit distutils-r1

DESCRIPTION=""
HOMEPAGE="https://pypi.python.org/pypi/oslo.serialization"
SRC_URI="mirror://pypi/${PN:0:1}/oslo.serialization/oslo.serialization-${PV}.tar.gz"
S="${WORKDIR}/oslo.serialization-${PV}"

LICENSE="Apache-2.0"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE="docs test"

DEPEND="
		>=dev-python/Babel-1.3
		>=dev-python/six-1.7.0
		>=dev-python/iso8601-0.1.9
		>=dev-python/oslo-utils-0.3.0
		test? (
			>=dev-python/hacking-0.5.6
			<dev-python/hacking-0.8
			>=dev-python/mock-1.0
			>=dev-python/netaddr-0.7.12
			>=dev-python/simplejson-2.2.0
			>=dev-python/oslo-i18n-0.3.0
			)
		docs? (
			>=dev-python/sphinx-1.1.2
			!~dev-python/sphinx-1.2.0
			<dev-python/sphinx-1.3
			>=dev-python/oslo-sphinx-2.2.0.0_alpha2
			)
	   "
RDEPENDS=${DEPENDS}

# This time half the doc files are missing; Do you want them?

python_test() {
	nosetests tests/ || die "test failed under ${EPYTHON}"
}
