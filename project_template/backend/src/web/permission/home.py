# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import login_not_required


@login_not_required
@no_csrf
def index(_write_tmpl):
    path_infos = facade.web_path_security_info()
    path_infos = sorted(path_infos, key=lambda i: i.path)
    _write_tmpl('permission/security_table.html', {'path_infos': path_infos})
