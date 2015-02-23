# Copyright 1999-2014 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: /var/cvsroot/gentoo-x86/dev-python/oslo-messaging/oslo-messaging-1.3.0.ebuild,v 1.4 2014/08/10 21:14:49 slyfox Exp $

EAPI=5
PYTHON_COMPAT=( python2_7 )

inherit distutils-r1

DESCRIPTION="Oslo Configuration Library"
HOMEPAGE="https://pypi.python.org/pypi/oslo.config"
SRC_URI="mirror://pypi/${PN:0:1}/oslo.config/oslo.config-${PV}.tar.gz"
S="${WORKDIR}/oslo.config-${PV}"

LICENSE="Apache-2.0"
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE="docs test"

DEPEND="
		>=dev-python/netaddr-0.7.12
		>=dev-python/six-1.7.0
		>=dev-python/stevedore-1.1.0
		test? (
			>=dev-python/hacking-0.9.2
			!~dev-python/hacking-0.10
			dev-python/discover
			>=dev-python/fixtures-0.3.14
			>=dev-python/subunit-0.0.18
			>=dev-python/testrepository-0.0.18
			>=dev-python/testscenarios-0.4
			>=dev-python/testtools-0.9.34
			>=dev-python/oslotest-1.2.0
			>=dev-python/coverage-3.6 
			>=dev-python/mock-1.0 )
		docs? (
			>=dev-python/sphinx-1.1.2
			!~dev-python/sphinx-1.2.0
			!>=dev-python/sphinx-1.3
			>=dev-python/oslo-sphinx-2.2.0
			)"
RDEPENDS=${DEPENDS}

# This time half the doc files are missing; Do you want them?

python_test() {
	nosetests tests/ || die "test failed under ${EPYTHON}"
}
