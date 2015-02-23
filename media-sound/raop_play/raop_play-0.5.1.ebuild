# Copyright 1999-2010 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI=2
inherit flag-o-matic multilib eutils linux-mod

MY_P=${PN/-/_}-${PV}

DESCRIPTION=""
HOMEPAGE="http://raop-play.sourceforge.net/"
#SRC_URI="mirror://sourceforge/${PN}/${MY_P}.tar.gz"
SRC_URI="http://prdownloads.sourceforge.net/raop-play/raop_play-0.5.1.tar.gz?download"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="x86"
IUSE="ogg mp3 aac flac"

RDEPEND="dev-libs/openssl
   media-libs/libid3tag
   media-libs/libsamplerate
   x11-libs/fltk:1.1
   dev-libs/glib:2
   ogg? ( media-sound/vorbis-tools )
   mp3? ( media-sound/mpg321 )
   aac? ( media-libs/faad2 )
   flac? ( media-libs/flac )
"

DEPEND="${RDEPEND}"

S=${WORKDIR}/${MY_P}


pkg_setup() {
        MODULE_NAMES="alsa_raoppcm(sound:${S}/drivers)"
        linux-mod_pkg_setup
}


src_prepare() {
   epatch "${FILESDIR}"/${P}-gcc44.patch
   epatch "${FILESDIR}"/glibsubst.patch

   sed -i \
      -e 's:$(CXX) -o:$(CXX) $(LDFLAGS) $(CXXFLAGS) -o:' \
      aexcl/Makefile.in || die
   sed -i 's!$(KERNEL_2_6):!module:!' drivers/Makefile || die

   sed -i -e '/config.h/d' drivers/alsa_raoppcm.c || die
   sed -i -e 's:snd_card_t:struct snd_card:' drivers/alsa_raoppcm.c  || die
   local x
   for x in "" _substream _runtime _ops _hardware _hw_params; do
        sed -i -e s:snd_pcm${x}_t:\ struct\ snd_pcm${x}: drivers/alsa_raoppcm.c || die
   done

}

src_configure() {
   append-cxxflags "-I/usr/include/fltk-1.1"
   append-ldflags "-L/usr/$(get_libdir)/fltk-1.1 -lglib-2.0"
   econf
}


src_compile() {
        emake || die "emake failed"
        cd drivers
        emake || die "emake failed"
        linux-mod_src_compile || die "failed to build driver "
}


src_install() {
   emake DESTDIR="${D}" install || die "failed to install programs"
   dodoc CHANGELOG README

   cd drivers
   linux-mod_src_install || die "linux-mod_src_install failed"
} 
