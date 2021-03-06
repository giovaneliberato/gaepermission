# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.middleware import CSRFMiddleware, CSRFInputToDependency
from gaepermission.middleware import LoggedUserMiddleware, PermissionMiddleware
from tmpl_middleware import TemplateMiddleware
from tekton.gae.middleware.email_errors import EmailMiddleware
from tekton.gae.middleware.json_middleware import JsonMiddleare
from tekton.gae.middleware.parameter import RequestParamsMiddleware
from tekton.gae.middleware.router_middleware import RouterMiddleware, ExecutionMiddleware
from tekton.gae.middleware.webapp2_dependencies import Webapp2Dependencies

SENDER_EMAIL = 'renzon@gmail.com'

MIDDLEWARES = [LoggedUserMiddleware,
               TemplateMiddleware,
               JsonMiddleare,
               EmailMiddleware,
               Webapp2Dependencies,
               RequestParamsMiddleware,
               CSRFInputToDependency,
               RouterMiddleware,
               CSRFMiddleware,
               PermissionMiddleware,
               ExecutionMiddleware]

