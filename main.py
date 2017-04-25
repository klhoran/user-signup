#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

form = """
<form method = "post">
<div align="center">
    <h1>User Signup</h1>
    <table>
        <tr>
            <td>Username</td>
            <td><input type = "text" name = "username" value = ""></td>
            <td style="color: red">%(er_username)s</td>
        </tr>
        <tr>
            <td>Password</td>
            <td><input type = "password" name = "password" value = ""></td>
            <td style="color: red">%(er_password)s</td>
        </tr>
        <tr>
            <td>Retype Password</td>
            <td><input type = "password" name = "verify" value = ""></td>
            <td style="color: red">%(er_verify)s</td>
        </tr>
        <tr>
            <td>Email (optional)</td>
            <td><input type = "email" name = "email"></td>
            <td style="color: red">%(er_email)s</td>
        </tr>
    </table>
    <br>
    <input type = "Submit">
</div>
</form>
"""


class MainHandler(webapp2.RequestHandler):

    def write_form(self, er_username="", er_password="", er_verify="", er_email=""):


        self.response.out.write(form%{"er_username": er_username, "er_password": er_password, "er_verify": er_verify, "er_email": er_email})

    def get(self):
        self.write_form()


    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        user_name = v_username(username)
        pass_word = v_password(password)
        e_mail = v_email(email)

        er_username = ""
        er_password = ""
        er_verify = ""
        er_email = ""
        error = False


        if not user_name:
            er_username = "Not a valid username"
            error = True

        if not pass_word:
            er_password = "Not a valid password"
            error = True

        if not e_mail:
            er_email = "Not a valid email"
            error = True

        if password != verify:
            er_verify = "Passwords do not match"
            error = True 


        if error:
            self.write_form(er_username, er_password, er_verify, er_email)
        else:
            self.response.out.write("Welcome, " + username)



USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def v_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def v_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def v_email(email):
    return not email or EMAIL_RE.match(email)





app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
