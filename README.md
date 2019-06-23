gabops.papertrail
=================

Installs and configure papertrail using remote_syslog2 (see 
[Papertrail official documentation](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-text-log-files-in-unix/).
and [remote_syslog2 Github repo](https://github.com/papertrail/remote_syslog2)

Requirements
------------

None

Role Variables
--------------

| Variable                           | Default value            | Description   |
| :---                               | :---                     | :---          |
| papertrail_version                 | "0.20"                   | Version to install. 0.20 is the latest at the moment                      |
| papertrail_config_file_path        | /etc/papertrail_conf.yml | Name of the configuration file for remote_syslog                          |
| papertrail_service_enabled         | true                     | Configure remote_syslog for starting when the system is booted            |
| papertrail_service_started         | true                     | The role will start the service after applying the configuration          |
| papertrail_managed_conf_file       | true                     | If disabled, no configuration will be applied (None of the following variables will be used). Just the installation so far |
| papertrail_custom_hostname         | ""                       | By default remote_syslog2 uses the hostname of the node. This can be this can be overwritten here |
| papertrail_destination_host        | ""                       | The papertrail destination host to send the logs to. Check your papertrail account for it. |
| papertrail_destination_port        | ""                       | The papertrail destination port to connect to the destination host. Check your papertrail account for it.              |
| papertrail_destination_protocol    | tls                      | This value can be tls(encrypted) or tcp (unencrypted)              |
| papertrail_log_facility            | ""                       | The syslog facility to use. See [syslog facility](https://en.wikipedia.org/wiki/Syslog#Facility) |
| papertrail_log_severity            | ""                       | The syslog severity to use. See  [syslog severity](https://en.wikipedia.org/wiki/Syslog#Severity_level) |
| papertrail_new_file_check_interval | ""                       | If a glob pattern for logs files is used this parameter controls the frecuency of checking for new log files in the directory |
| papertrail_files_to_log            | []                       | The file or globs to read. See examples. |
| papertrail_files_to_exclude        | []                       | Files to exclude in a directory. See examples |
| papertrail_exclude_patterns        | []                       | The pattern in the log file you are reading you want to ignore. |

For more detailed information about remote_syslog2 configuration see https://github.com/papertrail/remote_syslog2/blob/master/README.md

---
This role uses internally the next variables (see vars/):

For every os:
- `papertrail_download_url`: "https://github.com/papertrail/remote_syslog2/releases/download/v{{ papertrail_version }}"
- `papertrail_executable`: /usr/local/bin/remote_syslog
- `papertrail_systemd_unit_path`: /etc/systemd/system
- `papertrail_sysvinit_script_path`: /etc/init.d
- `papertrail_pid_directory`: /var/run
- `papertrail_service_name`: remote_syslog

RedHat os family:
- `papertrail_package_name`: "remote_syslog2-{{ papertrail_version }}-1.{{ ansible_architecture }}.rpm"

Debian os family:
- `papertrail_package_name`: "remote-syslog2_{{ papertrail_version }}_{{ installer_arch }}.deb"

> Usually you will not need to modify never any of the previous values but just in case I added the possibility of overwriting them for covering unexpected scenarios.


Dependencies
------------

None

Example Playbook
----------------

```yaml
    - hosts: servers
      vars:
        papertrail_version: "0.19"
        papertrail_config_file_path: /etc/papertrail.yml
        papertrail_destination_host: logs.papertrailapp.com
        papertrail_destination_port: 12345
        papertrail_custom_hostname: "host-01"
        papertrail_destination_protocol: tls
        papertrail_files_to_log:
          - path: /var/log/nginx.log
            tag: nginx
          - path: /var/log/httpd.log
            tag: apache
          - /var/log/yum.log
          - /var/log/audit/*.log
        papertrail_files_to_exclude:
          - /var/log/yum.log
        papertrail_log_facility: local7
        papertrail_log_severity: warn
      roles:
         - { role: papertrail }
```

License
-------

MIT

Author Information
------------------

Gabriel Suarez (gabops)