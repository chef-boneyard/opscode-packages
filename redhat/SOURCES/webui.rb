# Configuration File For Chef (chef-server-webui)
#
# chef-server-webui is a Merb application slice that provides a web user
# interface to the Chef Server. The WebUI is optional as of version 0.8.0+,
# and is a client to the API itself, which can be running on the same server,
# or optionally on a different server.
#
# By default, it is configured to run via Thin. It can be run manually as:
#
# chef-server-webui -p 4040 -e production -a thin
#
# This starts up the Chef Server WebUI on port 4040 in production mode using
# the thin server adapter.
#
# This file configures the behavior of the running server-webui itself.
#
# It is a Ruby DSL config file, and can embed regular Ruby code in addition to
# the configuration settings. Some settings use Ruby symbols, which are a value
# that starts with a colon. In Ruby, anything but 'false' or 'nil' is true. To
# set something to false:
#
# some_setting false
#
# log_level specifies the level of verbosity for output.
# valid values are: :debug, :info, :warn, :error, :fatal

log_level          :info

# log_location specifies where the server should log to.
# valid values are: a quoted string specifying a file, or STDOUT with
# no quotes. This is the application log for the Merb workers that get
# spawned. The chef-server-webui daemon is configured to log to
# /var/log/chef/server-webui.log in /etc/chef/sysconfig/chef-server-webui.

log_location       STDOUT

# ssl_verify_mode specifies if the REST client should verify SSL certificates.
# valid values are :verify_none, :verify_peer. The default Chef Server
# installation on Debian will use a self-generated SSL certificate so this
# should be :verify_none unless you replace the certificate.

ssl_verify_mode    :verify_none

# chef_server_url specifies the URL for the server API. The process actually
# listens on 0.0.0.0:PORT.
# valid values are any HTTP URL. If the server API port is changed, this
# value needs to be updated as well.

chef_server_url    "http://localhost:4000"

# file_cache_path specifies where the client should cache cookbooks, server
# cookie ID, and openid registration data.
# valid value is any filesystem directory location.

file_cache_path    "/var/cache/chef"

# openid_store_path specifies a location where to keep openid nonces for clients.
# valid values are any filesystem directory location.
#
# NOTE: OpenID is optionally used in the WebUI to associate OpenIDs with webui
# users.

openid_store_path  "/var/lib/chef/openid/store"

# openid_store_path specifies a location where to keep openid nonces for clients.
# valid values are any filesystem directory location.
#
# NOTE: OpenID is optionally used in the WebUI to associate OpenIDs with webui
# users.

openid_cstore_path "/var/lib/chef/openid/cstore"

# Mixlib::Log::Formatter.show_time specifies whether the chef-client log should
# contain timestamps.
# valid values are true or false. The printed timestamp is rfc2822, for example:
# Fri, 31 Jul 2009 19:19:46 -0600

Mixlib::Log::Formatter.show_time = true

# The following options configure the signing CA so it can be read by
# non-privileged user for the server daemon.

signing_ca_cert "/etc/chef/certificates/cert.pem"
signing_ca_key "/etc/chef/certificates/key.pem"
signing_ca_user "chef"
signing_ca_group "chef"

# web_ui_client_name specifies the user to use when accessing the Chef
# Server API. By default this is already set to "chef-webui".
#
# This user gets created by the chef-server and stored in CouchDB the
# first time the server starts up if the user and key don't exist.

web_ui_client_name "chef-webui"

# web_ui_admin_user_name and web_ui_admin_default_password specify the
# user and password that a human can use to initially log into the
# chef-server-webui when it starts. The default value for the user is 'admin'
# and the default password is'p@ssw0rd1' should be changed immediately on
# login. The web form will display the password reset page on first login.
# During package installation, debconf will prompt for a password, so this
# may differ from the default.

web_ui_admin_user_name "admin"
web_ui_admin_default_password "p@ssw0rd1"

# web_ui_key specifics the file to use for authenticating with the Chef
# Server API. By default this is already set to "/etc/chef/webui.pem".
#
# This file gets created by the chef-server and the public key stored in
# CouchDB the first time the server starts up if the user and key don't
# exist.

web_ui_key "/etc/chef/webui.pem"
