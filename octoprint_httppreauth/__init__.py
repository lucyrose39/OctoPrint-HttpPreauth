# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

from octoprint.users import FilebasedUserManager, User
import uuid
from flask import request
import flask_login


class HttppreauthPlugin(FilebasedUserManager, octoprint.plugin.TemplatePlugin):


    def login_user(self, user):
        self._logger.info("In HttpPruth login_user " + str(user))
        user = FilebasedUserManager.login_user(self, user)
        self._logger.debug("Got from old function " + str(user))
        if user is None:
            self._logger.debug("user is none, checking header")
            preauth_username = request.headers.get("X-Email")
            self._logger.debug("In login_user " + str(preauth_username))
            print(str(request.headers))
            print(preauth_username)
            if preauth_username is None:
                self._logger.debug("no preauth user, returning none")
                return None
            user = FilebasedUserManager.findUser(self, preauth_username)
            if not user:
                self._logger.debug("Creating new user " + preauth_username )
                self.addUser(preauth_username, str(uuid.uuid4()), True)
                user = FilebasedUserManager.findUser(self, preauth_username)
            self._logger.debug("now have user " + str(user))
            #flask_login.current_user = user
            flask_login.login_user(user);
            user = FilebasedUserManager.login_user(self, user)
            self._logger.debug("from old function got " + str(user))
        return user


    def findUser(self, userid=None, session=None):
        self._logger.debug("In findUser")
        user = FilebasedUserManager.findUser(self, userid, session)
        if not user:
            preauth_username = request.headers.get("X-Email")
            self._logger.debug("In findUser " + str(preauth_username))
            if preauth_username is None:
                return None
            #if preauth_username == userid:
            self._logger.debug("Creating new user " + preauth_username )
            self.addUser(preauth_username, str(uuid.uuid4()), True)
            user = FilebasedUserManager.findUser(self, userid, session)
        self._logger.debug("Returning " + str(user))
        return user

    def checkPassword(self, username, password):
        self._logger.debug("In Check Password " + username )
        return True

    def http_preauth_factory(components, settings, *args, **kwargs):
        return HttppreauthPlugin()

__plugin_name__ = "Httppreauth Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = HttppreauthPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
                "octoprint.users.factory": __plugin_implementation__.http_preauth_factory,
	}

