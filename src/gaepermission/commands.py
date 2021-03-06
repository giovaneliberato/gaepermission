# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import users
from gaebusiness.business import Command
from gaecookie import facade
from gaegraph.business_base import DestinationsSearch
from gaepermission.model import GoogleUser, ExternalToMainUser, MainUser


class FakeCommand(Command):
    '''
    This command is used when there is only the need to keep the Command contract
    '''

    def do_business(self, stop_on_error=True):
        pass


class GoogleLogin(Command):
    def __init__(self, google_user, response, user_cookie):
        super(GoogleLogin, self).__init__()
        self.google_user = google_user
        self.user_cookie = user_cookie
        self.response = response
        self._google_user_future = None
        self._save_google_user_future = None

    def set_up(self):
        if self.google_user:
            query = GoogleUser.query_by_google_id(self.google_user.user_id())
            self._google_user_future = query.get_async(keys_only=True)

    def do_business(self, stop_on_error=True):
        if self._google_user_future:
            g_user_key = self._google_user_future.get_result()
            if g_user_key:
                self.result = DestinationsSearch(ExternalToMainUser, g_user_key).execute().result[0]
            else:
                g_user = self.google_user
                self._save_google_user_future = GoogleUser(google_id=g_user.user_id()).put_async()
                self.result = MainUser(name=g_user.nickname(), email=g_user.email())
                self._save_main_user = self.result.put_async()

    def commit(self):
        if self._save_google_user_future:
            google_user_key = self._save_google_user_future.get_result()
            main_user_key = self._save_main_user.get_result()
            facade.write_cookie(self.response, self.user_cookie, {'id': self.result.key.id()}).execute()
            return ExternalToMainUser(origin=google_user_key, destination=main_user_key)
        if self.result:
            facade.write_cookie(self.response, self.user_cookie, {'id': self.result.key.id()}).execute()
