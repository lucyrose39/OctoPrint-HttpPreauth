# OctoPrint-HttpPreauth

For use behind a reverse proxy such as NGINX.

Configure your proxy to authenticate your users via any method you see fit, and add the username as the Remote-User header to all requests to Octoprint.

This plugin will detect that header, create the user if she does not exist in the underlying FilebasedUserManager, and then automatically log her in.

The logout function in Octoprint is non-functional. 

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/bkuker/OctoPrint-HttpPreauth/archive/master.zip


## Configuration

Setup of NGINX or HAProxy is beyond the scope of this document at this time.
