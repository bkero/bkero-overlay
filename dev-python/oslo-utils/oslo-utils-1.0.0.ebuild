# Copyright 1999-2014 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: /var/cvsroot/gentoo-x86/dev-python/oslo-messaging/oslo-messaging-1.3.0.ebuild,v 1.4 2014/08/10 21:14:49 slyfox Exp $

EAPI=5
PYTHON_COMPAT=( python2_7 )

inherit distutils-r1

DESCRIPTION=""
HOMEPAGE="https://pypi.python.org/pypi/oslo.utils"
SRC_URI="mirror://pypi/${PN:0:1}/oslo.utils/oslo.utils-${PV}.tar.gz"
S="${WORKDIR}/oslo.utils-${PV}"

LICENSE="Apache-2.0"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE="docs test"

DEPEND="
		>=dev-python/Babel-1.3
		>=dev-python/six-1.7.0
		>=dev-python/iso8601-0.1.9
		>=dev-python/oslo-i18n-1.0.0
		>=dev-python/netaddr-0.7.12
		test? (
			>=dev-python/hacking-0.9.1
			<dev-python/hacking-0.10
			>=dev-python/subunit-0.0.18
			>=dev-python/testrepository-0.0.18
			>=dev-python/testscenarios-0.4
			>=dev-python/testtools-0.9.34
			>=dev-python/oslotest-1.2.0
			>=dev-python/coverage-3.6
			>=dev-python/mock-1.0
			)
		docs? (
			>=dev-python/sphinx-1.1.2
			!~dev-python/sphinx-1.2.0
			!~dev-python/sphinx-1.3_beta1
			<dev-python/sphinx-1.3
			>=dev-python/oslo-sphinx-2.2.0
			)
	   "
RDEPENDS=${DEPENDS}

# This time half the doc files are missing; Do you want them?

python_test() {
	nosetests tests/ || die "test failed under ${EPYTHON}"
}
