################################################################################
#
# toykon-gui
#
################################################################################

TOYKON_GUI_VERSION = 07fe6b927829779602a6bff370668530e02c1650
TOYKON_GUI_SITE = $(call github,poveteen,toykon-gui,$(TOYKON_GUI_VERSION))
TOYKON_GUI_LICENSE = Apache License 2.0

TOYKON_GUI_INSTALL_STAGING = YES
TOYKON_GUI_DEPENDENCIES = host-pkgconf
TOYKON_GUI_SUPPORTS_IN_SOURCE_BUILD = NO

$(eval $(cmake-package))
