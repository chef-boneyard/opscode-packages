# Configuration File For Chef Solo (chef-solo)
#
# The program chef-solo allows you to run Chef as a standalone program
# without connecting to a remote Chef Server.
#
# When invoked without the -c option, chef-solo reads this file by default,
# otherwise it reads the specified file for configuration.
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
# Corresponds to chef-solo -l

log_level          :info

# log_location specifies where the client should log to.
# valid values are: a quoted string specifying a file, or STDOUT with
# no quotes.
# Corresponds to chef-solo -L

log_location       STDOUT

# file_cache_path specifies where solo should look for the cookbooks to use
# valid value is any filesystem directory location. This is slightly
# different from 'normal' client mode as solo is actually downloading (or
# using) the specified cookbooks in this location.

file_cache_path    "/var/cache/chef"

# cookbook_path specifies where solo should look for cookbooks it will use.
# valid value is a string, or array of strings of filesystem directory locations.
# This setting is similar to the server setting of the same name. Solo will use
# this as a search location, in Array order. It should be a subdirectory of
# file_cache_path, above.

cookbook_path      [ "/var/lib/chef/cookbooks" ]

# role_path designates where the server should load role JSON and Ruby DSL
# files from.
# valid values are any filesystem directory location. Roles are a feature
# that allow you to easily reuse lists of recipes and attribute settings.
# Please see the Chef Wiki page for information on how to utilize the feature.
# http://wiki.opscode.com/display/chef/Roles
role_path          [ "/var/lib/chef/roles" ]

# recipe_url specifies a remote URL to retrieve a tarball of cookbooks.
# Corresponds to chef-solo -r

#recipe_url "http://www.example.com/chef/cookbooks.tar.gz"

# json_attribs specifies a local or remote JSON data file that specifies
# attributes and a run_list that Chef will use to configure the system.
# Corresponds to chef-solo -j

#json_attribs "/var/tmp/node.json"
#json_attribs "http://www.example.com/chef/node.json"

# Mixlib::Log::Formatter.show_time specifies whether the log should
# contain timestamps.
# valid values are true or false. The printed timestamp is rfc2822, for example:
# Fri, 31 Jul 2009 19:19:46 -0600

Mixlib::Log::Formatter.show_time = true
