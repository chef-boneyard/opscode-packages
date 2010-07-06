# Configuration File For Chef SOLR (chef-solr)
#
# chef-solr daemon reads this configuration file on startup, as set in
# /etc/default/chef-solr.
#
# It is a Ruby DSL config file, and can embed regular Ruby code in addition to
# the configuration settings. Some settings use Ruby symbols, which are a value
# that starts with a colon. In Ruby, anything but 'false' or 'nil' is true. To
# set something to false:
#
# some_setting false
#
# log_location specifies where the indexer should log to.
# valid values are: a quoted string specifying a file, or STDOUT with
# no quotes.
# Corresponds to chef-solr -L
# The chef-solr daemon is configured to log to /var/log/chef/solr.log in
# /etc/sysconfig/chef-solr.

log_location       STDOUT

# search_index_path specifies where the indexer should store the indexes.
# valid value is any filesystem directory location.

search_index_path    "/var/lib/chef/search_index"

solr_jetty_path "/var/lib/chef/solr/solr-jetty"
solr_home_path  "/var/lib/chef/solr"
solr_data_path  "/var/cache/chef/solr/data"
solr_heap_size  "256M"

# specifies the URL of the SOLR instance for the indexer to connect to.

solr_url        "http://localhost:8983"

# uses the solr_jetty_path option set above, and the etc directory is
# actually a symbolic link to /etc/chef/solr-jetty.

#solr_java_opts  "-DSTART=#{Chef::Config[:solr_jetty_path]}/etc/start.config"

# Mixlib::Log::Formatter.show_time specifies whether the log should
# contain timestamps.
# valid values are true or false. The printed timestamp is rfc2822, for example:
# Fri, 31 Jul 2009 19:19:46 -0600

Mixlib::Log::Formatter.show_time = true

# pid_file specifies the location of where chef-client daemon should keep the pid
# file.
# valid value is any filesystem file location.

pid_file           "/var/run/chef/solr.pid"

user "chef"
group "chef"
