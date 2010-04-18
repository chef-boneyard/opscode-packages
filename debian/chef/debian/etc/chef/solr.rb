# Configuration File For Chef SOLR (chef-solr, chef-solr-indexer)
#
# Both the chef-solr and chef-solr-indexer daemons read this configuration 
# file on startup, as set in /etc/default/chef-solr*.
#
# The chef-solr-indexer program listens to a rabbitmq-server for the /chef
# queue, for data stored in the CouchDB. When data is saved to the chef-server,
# a message is sent to the queue, and the data is indexed and stored by
# chef-solr for search in Chef recipes, or with the 'knife' command-line tool.
#
# chef-solr is a solr-jetty instance.
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
# Corresponds to chef-solr or chef-solr-indexer -l
# Both chef-solr and chef-solr-indexer daemons are configured to log in
#   /etc/default/chef-solr -> /var/log/chef-solr
#   /etc/default/chef-solr-indexer -> /var/log/chef-solr-indexer
# respectively. The jetty log for chef-solr is set in
# /etc/chef/solr-jetty/jetty.xml to /var/log/chef/yyyy_mm_dd.jetty.log.

log_location       STDOUT

# search_index_path specifies where the indexer should store the indexes.
# valid value is any filesystem directory location.

search_index_path    "/var/lib/chef/search_index"

# set the jetty path to use Debian solr-jetty. Additional configuration for
# jetty can be found in /etc/chef/solr-jetty (which is symbolically linked to
# /var/lib/chef/solr/solr-jetty/etc).

solr_jetty_path "/var/lib/chef/solr/solr-jetty"
solr_home_path  "/var/lib/chef/solr"
solr_data_path  "/var/cache/chef/solr/data"
solr_heap_size  "256M"

# specifies the URL of the SOLR instance for the indexer to connect to.
# To change the port, modify the jetty.port setting in
# /etc/chef/solr-jetty/jetty.xml

solr_url        "http://localhost:8983"

# uses the solr_jetty_path option set above, and the etc directory is
# actually a symbolic link to /etc/chef/solr-jetty.

solr_java_opts  "-DSTART=#{Chef::Config[:solr_jetty_path]}/etc/start.config"

# Mixlib::Log::Formatter.show_time specifies whether the log should
# contain timestamps.
# valid values are true or false. The printed timestamp is rfc2822, for example:
# Fri, 31 Jul 2009 19:19:46 -0600

Mixlib::Log::Formatter.show_time = true
